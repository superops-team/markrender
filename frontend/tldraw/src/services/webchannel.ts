/**
 * TLDraw WebChannel通信服务
 * 基于webchannel-core.js实现的标准化通信
 */

interface BoardData {
  snapshot: any;
  metadata: {
    elementsCount: number;
    timestamp: string;
    lastModified: string;
  };
}

interface WebChannelResponse {
  success: boolean;
  data?: any;
  error?: string;
}

class TLDrawWebChannelManager {
  private static instance: TLDrawWebChannelManager;
  private isInitialized = false;

  private constructor() {}

  static getInstance(): TLDrawWebChannelManager {
    if (!TLDrawWebChannelManager.instance) {
      TLDrawWebChannelManager.instance = new TLDrawWebChannelManager();
    }
    return TLDrawWebChannelManager.instance;
  }

  // 初始化WebChannel
  initWebChannel(pageType: string) {
    if (this.isInitialized) return;
    
    if (typeof window !== 'undefined' && window.WebChannelManager) {
      window.WebChannelManager.initWebChannel(pageType).then(() => {
        this.isInitialized = true;
        console.log('TLDraw WebChannel已初始化');
      }).catch((error: Error) => {
        console.error('TLDraw WebChannel初始化失败:', error);
      });
    }
  }

  // 注册消息处理器
  on(action: string, handler: Function) {
    if (typeof window !== 'undefined' && window.WebChannelManager) {
      window.WebChannelManager.registerMessageHandler(action, handler);
    }
  }

  // 注销消息处理器 - 简化实现，移除未使用的参数
  off(action: string) {
    if (typeof window !== 'undefined' && window.WebChannelManager) {
      window.WebChannelManager.unregisterMessageHandler(action);
    }
  }

  // 发送消息到Python
  async sendToBackend(action: string, data: any): Promise<WebChannelResponse> {
    if (typeof window !== 'undefined' && window.WebChannelManager) {
      try {
        const response = await window.WebChannelManager.sendToBackend(action, data);
        return response as WebChannelResponse;
      } catch (error) {
        console.error('发送消息失败:', error);
        return { success: false, error: error instanceof Error ? error.message : 'Unknown error' };
      }
    }
    return { success: false, error: 'WebChannel not available' };
  }

  // 保存TLDraw画板
  async saveTLDrawBoard(boardId: string, drawingData: BoardData): Promise<WebChannelResponse> {
    return this.sendToBackend('save_tldraw_board', {
      boardId,
      drawingData: JSON.stringify(drawingData)
    });
  }

  // 加载TLDraw画板
  async loadTLDrawBoard(boardId: string): Promise<WebChannelResponse> {
    return this.sendToBackend('load_tldraw_board', { boardId });
  }

  // 导出TLDraw画板
  async exportTLDrawBoard(boardId: string, format: string, imageData: string): Promise<WebChannelResponse> {
    return this.sendToBackend('export_tldraw_board', {
      boardId,
      format,
      imageData
    });
  }

  // 检查WebChannel是否就绪
  isReady(): boolean {
    return this.isInitialized;
  }
}

// 导出单例实例
export const WebChannelManager = TLDrawWebChannelManager.getInstance();

// 兼容性导出
export default WebChannelManager;