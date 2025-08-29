/**
 * MarkRender WebChannel 核心通信库 - TypeScript版本
 * 提供标准化的WebChannel通信协议和重试机制
 * 专为Excalidraw白板功能优化
 */

// 类型定义
interface QWebChannel {
  objects: {
    backendInterface: {
      dispatch_request: (request: string) => Promise<string>;
      frontend_ready: () => void;
      handle_web_response: (response: string) => void;
    };
  };
}

interface QtWebChannelTransport {
  webChannelTransport: any;
}

interface ExcalidrawWebChannelState {
  backendInterface: QWebChannel['objects']['backendInterface'] | null;
  isChannelReady: boolean;
  callbackMap: Map<string, Function>;
  requestCounter: number;
  retryCount: number;
  maxRetries: number;
  pageType: string;
  initCallbacks: Function[];
  messageHandlers: Map<string, Function>;
}

interface ExcalidrawData {
  elements: any[];
  appState: any;
  files?: any;
}

interface BoardMetadata {
  elementsCount: number;
  timestamp: string;
  lastModified?: string;
  version?: string;
}

interface WebChannelRequest {
  requestId: string;
  action: string;
  data: any;
  pageType: string;
}

interface WebChannelResponse {
  success: boolean;
  data?: any;
  error?: string;
  requestId?: string;
  board_id?: string;
  metadata?: any;
}

// 全局类型扩展
declare global {
  interface Window {
    qt?: QtWebChannelTransport;
    QWebChannel?: any;
    handlePythonMessage?: (action: string, data: any, requestId?: string) => void;
    webChannelManager?: ExcalidrawWebChannelManager;
    pendingMessages?: Array<{ action: string; data: any; requestId?: string }>;
    pendingExcalidrawMessages?: Array<{ action: string; data: any; requestId?: string }>;
  }
}

// Excalidraw WebChannel管理器类
class ExcalidrawWebChannelManager {
  public state: ExcalidrawWebChannelState = {
    backendInterface: null,
    isChannelReady: false,
    callbackMap: new Map(),
    requestCounter: 0,
    retryCount: 0,
    maxRetries: 5,
    pageType: 'excalidraw',  // 修复：设置正确的页面类型
    initCallbacks: [],
    messageHandlers: new Map()
  };

  // 日志工具
  private logger = {
    info: (msg: string, ...args: any[]) => console.log(`[WebChannel-${this.state.pageType}] ${msg}`, ...args),
    warn: (msg: string, ...args: any[]) => console.warn(`[WebChannel-${this.state.pageType}] ${msg}`, ...args),
    error: (msg: string, ...args: any[]) => console.error(`[WebChannel-${this.state.pageType}] ${msg}`, ...args),
    debug: (msg: string, ...args: any[]) => console.debug(`[WebChannel-${this.state.pageType}] ${msg}`, ...args)
  };

  constructor() {
    this.setupGlobalMessageHandler();
    this.setupGlobalErrorHandlers();
  }

  // 设置全局消息处理函数
  private setupGlobalMessageHandler(): void {
    // 立即定义全局消息处理函数，防止早期调用失败
    window.handlePythonMessage = (action: string, data: any, requestId?: string) => {
      this.logger.debug('收到Python消息:', action, data, 'requestId:', requestId);
      
      if (this.state.messageHandlers.has(action)) {
        try {
          this.state.messageHandlers.get(action)!(data, requestId);
        } catch (error) {
          this.logger.error(`处理消息 ${action} 时出错:`, error);
        }
      } else {
        this.logger.warn(`未注册的消息类型: ${action}`);
      }
    };

    // 确保全局函数立即可用
    if (typeof window.handlePythonMessage !== 'function') {
      this.logger.error('全局消息处理函数设置失败');
    } else {
      this.logger.debug('全局消息处理函数设置成功');
    }
    
    // 处理可能缓存的消息
    if (window.pendingMessages && Array.isArray(window.pendingMessages)) {
      this.logger.info(`处理 ${window.pendingMessages.length} 条通用缓存消息`);
      window.pendingMessages.forEach((msg: any) => {
        if (window.handlePythonMessage) {
          window.handlePythonMessage(msg.action, msg.data, msg.requestId);
        }
      });
      window.pendingMessages = [];
    }
    
    // 处理Excalidraw特定的缓存消息
    if (window.pendingExcalidrawMessages && Array.isArray(window.pendingExcalidrawMessages)) {
      this.logger.info(`处理 ${window.pendingExcalidrawMessages.length} 条Excalidraw缓存消息`);
      window.pendingExcalidrawMessages.forEach((msg: any) => {
        if (window.handlePythonMessage) {
          window.handlePythonMessage(msg.action, msg.data, msg.requestId);
        }
      });
      window.pendingExcalidrawMessages = [];
    }
  }

  // 设置全局错误处理
  private setupGlobalErrorHandlers(): void {
    window.addEventListener('error', (event) => {
      this.reportError({
        message: event.message,
        source: event.filename,
        line: event.lineno,
        column: event.colno,
        stack: event.error?.stack || ''
      }, 'global');
    });

    window.addEventListener('unhandledrejection', (event) => {
      this.reportError({
        message: event.reason?.message || String(event.reason),
        stack: event.reason?.stack || ''
      }, 'promise');
    });

    window.addEventListener('beforeunload', () => {
      this.logger.info('页面即将卸载，清理WebChannel资源');
      this.cleanup();
    });
  }

  // WebChannel初始化（带重试机制）
  async initWebChannel(): Promise<void> {
    this.logger.info('开始初始化WebChannel...');

    // 检查QWebChannel是否可用
    if (!window.qt?.webChannelTransport) {
      this.logger.error('QWebChannel传输不可用，尝试重试...');
      
      if (this.state.retryCount < this.state.maxRetries) {
        this.state.retryCount++;
        this.logger.info(`WebChannel初始化重试 ${this.state.retryCount}/${this.state.maxRetries}`);
        await new Promise(resolve => setTimeout(resolve, 200 * this.state.retryCount));
        return this.initWebChannel();
      } else {
        this.logger.error('WebChannel初始化最终失败，切换到离线模式');
        // 设置为离线模式，但不抛出错误
        this.setupOfflineMode();
        return;
      }
    }

    // 检查QWebChannel构造函数是否可用
    if (typeof window.QWebChannel !== 'function') {
      this.logger.error('QWebChannel构造函数不可用');
      this.setupOfflineMode();
      return;
    }

    return new Promise((resolve, reject) => {
      try {
        // @ts-ignore - QWebChannel is loaded externally
        new QWebChannel(window.qt.webChannelTransport, (channel: QWebChannel) => {
          this.state.backendInterface = channel.objects.backendInterface;
          this.state.isChannelReady = true;
          this.logger.info('WebChannel初始化成功');

          // 通知后端前端就绪
          if (this.state.backendInterface?.frontend_ready) {
            try {
              this.state.backendInterface.frontend_ready();
            } catch (error) {
              this.logger.warn('通知后端前端就绪失败:', error);
            }
          }

          // 执行初始化回调
          this.state.initCallbacks.forEach(callback => {
            try {
              callback();
            } catch (error) {
              this.logger.error('初始化回调执行失败:', error);
            }
          });

          resolve();
        });
      } catch (error) {
        this.logger.error('QWebChannel初始化异常:', error);
        
        if (this.state.retryCount < this.state.maxRetries) {
          this.state.retryCount++;
          setTimeout(() => {
            this.initWebChannel().then(resolve).catch(reject);
          }, 300 * this.state.retryCount);
        } else {
          this.logger.error('WebChannel初始化最终失败，切换到离线模式');
          this.setupOfflineMode();
          resolve(); // 不抛出错误，允许应用继续运行
        }
      }
    });
  }

  // 设置离线模式
  private setupOfflineMode(): void {
    this.logger.warn('设置离线模式，部分功能将不可用');
    this.state.isChannelReady = false;
    this.state.backendInterface = null;
    
    // 执行初始化回调，即使在离线模式下
    this.state.initCallbacks.forEach(callback => {
      try {
        callback();
      } catch (error) {
        this.logger.error('离线模式初始化回调执行失败:', error);
      }
    });
  }

  // 标准化消息发送到Python
  async sendToPython(action: string, data: any = {}, callback?: Function): Promise<WebChannelResponse> {
    this.logger.debug('发送到Python:', action, data);

    if (!this.state.isChannelReady || !this.state.backendInterface) {
      const errorMsg = '通信通道未就绪（离线模式）';
      this.logger.warn(errorMsg);
      
      const offlineResponse: WebChannelResponse = {
        success: false,
        error: errorMsg,
        data: null
      };
      
      if (callback) {
        callback(offlineResponse);
      }
      
      return offlineResponse;
    }

    if (typeof this.state.backendInterface.dispatch_request !== 'function') {
      this.logger.error('后端接口方法不存在: dispatch_request');
      throw new Error('后端接口方法不存在');
    }

    const requestId = `${this.state.pageType}_req_${Date.now()}_${this.state.requestCounter++}`;
    if (callback) this.state.callbackMap.set(requestId, callback);

    const request: WebChannelRequest = {
      requestId: requestId,
      action: action,
      data: data,
      pageType: this.state.pageType
    };

    try {
      const responseJson = await this.state.backendInterface.dispatch_request(JSON.stringify(request));
      return this.handlePythonResponse(responseJson);
    } catch (error) {
      this.logger.error('请求失败:', error);
      if (callback) {
        this.state.callbackMap.delete(requestId);
        callback({ success: false, error: (error as Error).message });
      }
      throw error;
    }
  }

  // 处理Python响应
  private handlePythonResponse(responseJson: string): WebChannelResponse {
    try {
      const response: WebChannelResponse = typeof responseJson === 'string' ? 
          JSON.parse(responseJson) : responseJson;
      this.logger.debug('收到响应:', response);

      if (response.requestId && this.state.callbackMap.has(response.requestId)) {
        this.state.callbackMap.get(response.requestId)!(response);
        this.state.callbackMap.delete(response.requestId);
      }

      return response;
    } catch (e) {
      this.logger.error('解析响应失败:', e);
      throw e;
    }
  }

  // =================================================================
  // Excalidraw专用接口实现
  // =================================================================

  // 保存Excalidraw白板数据
  async saveExcalidrawBoard(boardId: string, drawingData: ExcalidrawData, metadata: BoardMetadata): Promise<WebChannelResponse> {
    this.logger.info(`保存Excalidraw白板: ${boardId}`);
    
    return this.sendToPython('save_excalidraw_board', {
      boardId: boardId,
      drawingData: JSON.stringify(drawingData),
      metadata: {
        ...metadata,
        savedAt: new Date().toISOString()
      }
    });
  }

  // 加载Excalidraw白板数据
  async loadExcalidrawBoard(boardId: string): Promise<WebChannelResponse> {
    this.logger.info(`加载Excalidraw白板: ${boardId}`);
    
    return this.sendToPython('load_excalidraw_board', {
      boardId: boardId
    });
  }

  // 导出Excalidraw白板
  async exportExcalidrawBoard(boardId: string, format: string = 'png', imageData?: string): Promise<WebChannelResponse> {
    this.logger.info(`导出Excalidraw白板: ${boardId} -> ${format}`);
    
    return this.sendToPython('export_excalidraw_board', {
      boardId: boardId,
      format: format,
      imageData: imageData
    });
  }

  // 设置当前白板ID
  async setBoardId(boardId: string): Promise<WebChannelResponse> {
    this.logger.info(`设置白板ID: ${boardId}`);
    
    return this.sendToPython('setBoardId', {
      boardId: boardId
    });
  }

  // 发送前端就绪消息
  async sendFrontendReady(): Promise<WebChannelResponse> {
    this.logger.info('发送前端就绪消息');
    
    return this.sendToPython('frontendReady', {
      pageType: this.state.pageType,
      timestamp: new Date().toISOString()
    });
  }

  // 注册消息处理器
  registerMessageHandler(action: string, handler: Function): void {
    this.state.messageHandlers.set(action, handler);
    this.logger.debug(`注册消息处理器: ${action}`);
  }

  // 注销消息处理器
  unregisterMessageHandler(action: string): void {
    this.state.messageHandlers.delete(action);
    this.logger.debug(`注销消息处理器: ${action}`);
  }

  // 注册初始化完成回调
  onReady(callback: Function): void {
    if (this.state.isChannelReady) {
      callback();
    } else {
      this.state.initCallbacks.push(callback);
    }
  }

  // 判断是否就绪
  isReady(): boolean {
    return this.state.isChannelReady;
  }

  // 错误报告
  reportError(error: any, source: string = 'unknown'): void {
    const errorData = {
      message: error.message || String(error),
      source: source,
      stack: error.stack || '',
      pageType: this.state.pageType,
      timestamp: new Date().toISOString()
    };

    this.logger.error('报告错误:', errorData);

    if (this.state.isChannelReady) {
      this.sendToPython('reportError', errorData).catch(e => {
        this.logger.error('错误报告失败:', e);
      });
    }
  }

  // 清理资源
  private cleanup(): void {
    this.state.callbackMap.clear();
    this.state.messageHandlers.clear();
    this.state.initCallbacks.length = 0;
  }
}

// 创建全局实例
const webChannelManager = new ExcalidrawWebChannelManager();

// 立即设置到window对象上，供模板中的handlePythonMessage使用
window.webChannelManager = webChannelManager;

// 立即设置正确的页面类型
webChannelManager.state.pageType = 'excalidraw';
console.log('🎨 Excalidraw WebChannel管理器初始化，页面类型:', webChannelManager.state.pageType);

// 简化的接口对象，与原有Mock接口兼容
const webChannel = {
  // 事件监听接口（兼容性）
  on: (event: string, callback: Function) => {
    webChannelManager.registerMessageHandler(event, callback);
  },
  
  off: (event: string, _callback: Function) => {
    webChannelManager.unregisterMessageHandler(event);
  },
  
  // 发送消息接口（兼容性）
  send: (action: string, data?: any, callback?: Function) => {
    if (webChannelManager.isReady()) {
      return webChannelManager.sendToPython(action, data, callback);
    } else {
      console.warn('WebChannel未就绪，等待初始化...');
      webChannelManager.onReady(() => {
        webChannelManager.sendToPython(action, data, callback);
      });
    }
  },
  
  // 直接暴露manager的方法
  manager: webChannelManager
};

// 自动初始化
webChannelManager.initWebChannel().then(() => {
  console.log('🟢 Excalidraw WebChannel初始化完成');
  webChannelManager.sendFrontendReady();
}).catch(error => {
  console.error('❌ Excalidraw WebChannel初始化失败:', error);
});

// 导出
export { webChannelManager, webChannel, ExcalidrawWebChannelManager };
export default webChannel;
export type { ExcalidrawData, BoardMetadata, WebChannelResponse };