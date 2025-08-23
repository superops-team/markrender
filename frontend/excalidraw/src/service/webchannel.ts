// 真实的QWebChannel实现 - 基于app/editor/resources/index.html重写
// 移除所有mock逻辑，使用真实的QWebChannel

// 全局状态管理
interface AppState {
  isChannelReady: boolean;
  backendInterface: any;
  callbackMap: Map<string, Function>;
  requestCounter: number;
  currentDocumentId?: string;
}

const appState: AppState = {
  isChannelReady: false,
  backendInterface: null,
  callbackMap: new Map(),
  requestCounter: 0
};

// 后端接口定义
interface BackendInterface {
  frontend_ready(): void;
  dispatch_request(request: string): Promise<string>;
  handle_web_response(response: string): void;
}

// 发送响应给后端
function sendResponseToBackend(requestId: string, data: any) {
  if (!appState.isChannelReady || !appState.backendInterface) {
    console.error('WebChannel未就绪，无法发送响应');
    return;
  }
  
  try {
    const responseData = {
      requestId: requestId,
      result: data
    };
    appState.backendInterface.handle_web_response(JSON.stringify(responseData));
  } catch (error) {
    console.error('发送响应失败:', error);
  }
}

// 初始化QWebChannel
function initWebChannel() {
  if (!window.qt || !window.qt.webChannelTransport) {
    console.error('QWebChannel传输不可用');
    return;
  }

  new QWebChannel(window.qt.webChannelTransport, (channel: any) => {
    appState.backendInterface = channel.objects.backendInterface;
    appState.isChannelReady = true;
    console.log('QWebChannel初始化完成');

    // 通知后端前端就绪
    appState.backendInterface.frontend_ready();
  });
}

// 处理后端发送的消息
window.handleBackendMessage = function(action: string, data: any, requestId?: string) {
  console.log('收到后端消息:', action, data, 'requestId:', requestId);
  
  // 触发对应的事件监听器
  const callbacks = webChannel.callbacks.get(action);
  if (callbacks) {
    callbacks.forEach(callback => callback(data));
  }
  
  // 如果有requestId，表示需要响应
  if (requestId) {
    // 根据action处理不同的请求
    switch (action) {
      case 'getExcalidrawData':
        // 触发getExcalidrawData事件，由前端处理
        const getDataCallbacks = webChannel.callbacks.get('getExcalidrawData');
        if (getDataCallbacks) {
          getDataCallbacks.forEach(callback => {
            const result = callback(data);
            if (result !== undefined) {
              sendResponseToBackend(requestId, { success: true, data: result });
            }
          });
        }
        break;
      default:
        // 其他action的处理
        break;
    }
  }
};

// WebChannel类定义
class WebChannel {
  public callbacks: Map<string, Set<Function>> = new Map();
  
  // 注册事件监听器
  on(event: string, callback: Function) {
    if (!this.callbacks.has(event)) {
      this.callbacks.set(event, new Set());
    }
    this.callbacks.get(event)!.add(callback);
  }

  // 移除事件监听器
  off(event: string, callback: Function) {
    if (this.callbacks.has(event)) {
      this.callbacks.get(event)!.delete(callback);
      if (this.callbacks.get(event)!.size === 0) {
        this.callbacks.delete(event);
      }
    }
  }

  // 发送消息到后端
  send(action: string, data?: any, callback?: Function) {
    if (!appState.isChannelReady || !appState.backendInterface) {
      console.error('通信通道未就绪');
      return;
    }

    // 检查后端方法是否存在
    if (typeof appState.backendInterface.dispatch_request !== 'function') {
      console.error('后端接口方法不存在: dispatch_request');
      return;
    }

    // 生成唯一请求ID
    const requestId = `req_${Date.now()}_${appState.requestCounter++}`;
    if (callback) appState.callbackMap.set(requestId, callback);

    // 标准请求格式
    const request = {
      requestId: requestId,
      action: action,
      data: data || {}
    };

    try {
      appState.backendInterface.dispatch_request(JSON.stringify(request))
        .then((responseJson: string) => handleBackendResponse(responseJson))
        .catch((error: any) => console.error('请求失败:', error));
    } catch (e) {
      console.error('发送请求失败:', e);
    }
  }

  // 发送响应给后端
  sendResponse(action: string, data: any) {
    if (!appState.isChannelReady || !appState.backendInterface) {
      console.error('通信通道未就绪');
      return;
    }

    const requestId = `resp_${Date.now()}`;
    sendResponseToBackend(requestId, { success: true, data });
  }
}

// 处理后端响应
function handleBackendResponse(responseJson: string) {
  try {
    const response = JSON.parse(responseJson);
    
    // 处理回调
    if (response.requestId && appState.callbackMap.has(response.requestId)) {
      const callback = appState.callbackMap.get(response.requestId);
      callback?.(response.result);
      appState.callbackMap.delete(response.requestId);
    }
    
    // 触发对应的事件
    if (response.action) {
      const callbacks = webChannel.callbacks.get(response.action);
      if (callbacks) {
        callbacks.forEach(callback => callback(response.result?.data || response.result));
      }
    }
  } catch (e) {
    console.error('解析响应失败:', e);
  }
}

// 创建全局webChannel实例
export const webChannel = new WebChannel();

// 初始化应用
function initApp() {
  initWebChannel();
}

// 暴露到全局
declare global {
  interface Window {
    webChannel: WebChannel;
    qt: {
      webChannelTransport: any;
    };
    QWebChannel: any;
    handleBackendMessage: (action: string, data: any, requestId?: string) => void;
  }
}

if (typeof window !== 'undefined') {
  window.webChannel = webChannel;
  window.handleBackendMessage = handleBackendMessage;
  
  // 页面加载完成后初始化
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
  } else {
    initApp();
  }
}