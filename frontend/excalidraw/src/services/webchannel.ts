// WebChannel 服务，用于与后端通信

class ExcalidrawWebChannelManager {
  private static instance: ExcalidrawWebChannelManager | null = null
  private webChannel: any = null

  private constructor() {
    // 私有构造函数，实现单例模式
  }

  public static getInstance(): ExcalidrawWebChannelManager {
    if (!ExcalidrawWebChannelManager.instance) {
      ExcalidrawWebChannelManager.instance = new ExcalidrawWebChannelManager()
    }
    return ExcalidrawWebChannelManager.instance
  }

  // 初始化 WebChannel 连接
  public async initWebChannel(): Promise<void> {
    try {
      // 等待 webchannel-core.js 加载完成
      await new Promise<void>((resolve) => {
        const checkWebChannel = () => {
          if (window.WebChannelManager) {
            resolve()
          } else {
            setTimeout(checkWebChannel, 100)
          }
        }
        checkWebChannel()
      })

      // 初始化 WebChannel
      if (window.WebChannelManager) {
        await window.WebChannelManager.initWebChannel('excalidraw')
        this.webChannel = window.WebChannelManager
        console.log('Excalidraw WebChannel initialized')
      }
    } catch (error) {
      console.error('Failed to initialize Excalidraw WebChannel:', error)
    }
  }

  // 保存白板数据到后端
  public async saveExcalidrawData(data: any): Promise<any> {
    try {
      if (this.webChannel) {
        return await this.webChannel.sendToPython('save_excalidraw', data)
      } else {
        console.warn('WebChannel not initialized')
        return null
      }
    } catch (error) {
      console.error('Failed to save Excalidraw data:', error)
      throw error
    }
  }

  // 从后端加载白板数据
  public async loadExcalidrawData(id: string): Promise<any> {
    try {
      if (this.webChannel) {
        return await this.webChannel.sendToPython('load_excalidraw', { id })
      } else {
        console.warn('WebChannel not initialized')
        return null
      }
    } catch (error) {
      console.error('Failed to load Excalidraw data:', error)
      throw error
    }
  }
}

export default ExcalidrawWebChannelManager