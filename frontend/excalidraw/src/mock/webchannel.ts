// WebChannel Mock实现
class WebChannelMock {
  private callbacks: Map<string, Set<Function>> = new Map(); // 改为使用Set存储多个回调
  private isReady: boolean = false;

  constructor() {
    // 模拟初始化延迟
    setTimeout(() => {
      this.isReady = true;
      console.log('WebChannel initialized');
    }, 1000);
  }

  // 注册回调
  on(event: string, callback: Function) {
    if (!this.callbacks.has(event)) {
      this.callbacks.set(event, new Set());
    }
    this.callbacks.get(event)!.add(callback);
  }

  // 移除回调（新增）
  off(event: string, callback: Function) {
    if (this.callbacks.has(event)) {
      this.callbacks.get(event)!.delete(callback);
      // 如果没有更多回调，则删除该事件
      if (this.callbacks.get(event)!.size === 0) {
        this.callbacks.delete(event);
      }
    }
  }

  // 发送消息
  send(action: string, data: any) {
    if (!this.isReady) {
      console.error('WebChannel not ready');
      return;
    }

    console.log('Sending message:', action, data);
    // 模拟后端响应
    setTimeout(() => {
      const callback = this.callbacks.get('response');
      if (callback) {
        callback.forEach(cb => cb({ action, data: { success: true, ...data } }));
      }
    }, 500);
  }

  // 处理来自后端的消息
  handleMessage(action: string, data: any) {
    console.log('Received message from backend:', action, data);
    const callbacks = this.callbacks.get(action);
    if (callbacks) {
      callbacks.forEach(callback => callback(data));
    }
  }
}

export const webChannel = new WebChannelMock();

// 将webChannel暴露到window对象上，以便调试和外部访问
declare global {
  interface Window {
    webChannel: WebChannelMock;
  }
}

if (typeof window !== 'undefined') {
  window.webChannel = webChannel;
}