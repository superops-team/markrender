import React, { useEffect, useRef, useState } from 'react';
import { Excalidraw } from "@excalidraw/excalidraw";
import "./App.css";
import "./webchannel.js";  // 导入webchannel.js确保handleBackendMessage函数被定义

// 在组件定义之前就设置 Excalidraw 的资源路径
if (typeof window !== 'undefined') {
  // 确保 Excalidraw 使用本地资源而不是 CDN
  window.EXCALIDRAW_ASSET_PATH = "./assets/";
  window.EXCALIDRAW_EXPORT_SOURCE = "";
  
  // 初始化全局状态对象
  window.editorState = window.editorState || {};
  window.editorState.currentItemId = null;
  
  // 设置全局API供后端调用
  window.loadExcalidrawData = (content) => {
    if (window.excalidrawAppRef) {
      try {
        const data = JSON.parse(content || '[]');
        window.excalidrawAppRef.updateScene({ elements: data });
        console.log('已加载Excalidraw数据:', data.length, '个元素');
      } catch (error) {
        console.error('加载数据失败:', error);
      }
    }
  };
  
  window.getExcalidrawData = () => {
    if (window.excalidrawAppRef) {
      try {
        const elements = window.excalidrawAppRef.getSceneElements();
        return JSON.stringify(elements);
      } catch (error) {
        console.error('获取数据失败:', error);
        return '[]';
      }
    }
    return '[]';
  };
  
  window.setCurrentItemId = (itemId) => {
    if (window.editorState) {
      window.editorState.currentItemId = itemId;
      console.log('当前项目ID已设置:', itemId);
    }
  };
  
  window.resetExcalidraw = () => {
    try {
      console.log('重置Excalidraw状态');
      
      // 重置当前项目ID
      window.currentItemId = null;
      if (window.editorState) {
        window.editorState.currentItemId = null;
      }
      
      // 清空场景
      if (window.excalidrawAppRef && typeof window.excalidrawAppRef.updateScene === 'function') {
        window.excalidrawAppRef.updateScene({ elements: [] });
        console.log('Excalidraw场景已清空');
      }
      
      console.log('Excalidraw状态重置完成');
    } catch (error) {
      console.error('重置Excalidraw状态失败:', error);
    }
  };
  
  // 确保函数始终存在，即使在初始化之前被调用
  if (typeof window.getExcalidrawData !== 'function') {
    window.getExcalidrawData = () => {
      if (window.excalidrawAppRef) {
        try {
          const elements = window.excalidrawAppRef.getSceneElements();
          return JSON.stringify(elements);
        } catch (error) {
          console.error('获取数据失败:', error);
          return '[]';
        }
      }
      console.warn('Excalidraw尚未初始化，返回空数据');
      return '[]';
    };
  }
}

function App() {
  const excalidrawRef = useRef(null);
  const [isReady, setIsReady] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // 将ref暴露给全局，以便在handleBackendMessage中使用
    window.excalidrawAppRef = excalidrawRef.current;
    
    // 移除WebChannel初始化相关代码
    // 直接设置为就绪状态
    setIsReady(true);
    setIsLoading(false);
    console.log('✅ Excalidraw已初始化（WebChannel已禁用）');

    // 添加全局Promise拒绝处理器
    const handlePromiseRejection = (event) => {
      console.error('❌ 未捕获的Promise拒绝:', event.reason);
    };

    window.addEventListener('unhandledrejection', handlePromiseRejection);

    return () => {
      // 清理
      window.removeEventListener('unhandledrejection', handlePromiseRejection);
    };
  }, []);

  const handleChange = (elements, state) => {
    console.log("Excalidraw元素已更改:", elements.length, "个元素");
    
    // 移除自动保存到后端的代码
    // 仅记录日志
    console.log("元素变化已记录");
  };

  if (isLoading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>正在加载Excalidraw...</p>
      </div>
    );
  }

  return (
    <div className="App">
      <div className="excalidraw-wrapper">
        {isReady ? (
          <Excalidraw 
            ref={excalidrawRef}
            onChange={handleChange}
            UIOptions={{
              canvasActions: {
                export: {
                  saveFileToDisk: true
                }
              }
            }}
          />
        ) : (
          <div className="error-container">
            <h2>初始化失败</h2>
            <p>Excalidraw初始化失败。</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;