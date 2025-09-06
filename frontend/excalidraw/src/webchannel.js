// 移除WebChannel相关代码，仅保留空的类定义以保持兼容性
class ExcalidrawWebChannel {
  constructor() {
    // 移除所有WebChannel相关属性
  }

  // 移除所有WebChannel相关方法
  sendMessage(action, data, callback = null, itemId = null) {
    // 不再实际发送消息到后端，仅记录日志
    console.log('sendMessage调用（已禁用WebChannel）:', action, data);
    // 如果有回调，直接调用
    if (callback) {
      callback({ success: true, message: 'WebChannel已禁用' });
    }
    return true;
  }
  
  // 保存数据到后端（简化版）
  saveData(data) {
    console.log('saveData调用（已禁用WebChannel）:', data);
    return true;
  }
}

// 创建全局实例
if (typeof window !== 'undefined') {
  window.excalidrawChannel = new ExcalidrawWebChannel();
  
  // 添加全局handleBackendMessage函数，与markdown页面保持一致
  window.handleBackendMessage = function(action, data, requestId) {
    console.log('收到后端消息:', action, data);
    
    let result = { success: true };
    
    // 处理特定的后端消息
    switch(action) {
      case 'loadExcalidrawData':
        if (typeof window.loadExcalidrawData === 'function') {
          window.loadExcalidrawData(data.content);
        }
        break;
        
      case 'setCurrentItemId':
        if (typeof window.setCurrentItemId === 'function') {
          window.setCurrentItemId(data.item_id);
        }
        break;
        
      case 'setValue':
        // 处理setValue消息，设置Excalidraw内容
        if (typeof window.loadExcalidrawData === 'function') {
          window.loadExcalidrawData(data.content);
        }
        break;
        
      case 'getContent':
        // 处理getContent消息，获取Excalidraw内容
        if (typeof window.getExcalidrawData === 'function') {
          const content = window.getExcalidrawData();
          result = { content: content };
        }
        break;
        
      case 'registerEditorEvents':
        // 注册编辑器事件
        console.log('注册Excalidraw编辑器事件');
        // 可以在这里添加Excalidraw特定的事件注册逻辑
        break;
        
      case 'setupContentChangeListener':
        // 设置内容变化监听器
        console.log('设置Excalidraw内容变化监听器');
        // 可以在这里添加Excalidraw特定的内容变化监听逻辑
        break;
        
      case 'textChanged':
        // 处理文本变化
        console.log('处理Excalidraw文本变化');
        // 可以在这里添加Excalidraw特定的文本变化处理逻辑
        break;
        
      default:
        console.log('未知的后端消息类型:', action);
    }
    
    // 不再发送响应到后端，但返回结果
    return result;
  };
}

export default ExcalidrawWebChannel;