import React, { useEffect, useState } from 'react';
import { Excalidraw } from '@excalidraw/excalidraw';

function App() {
  const [excalidrawAPI, setExcalidrawAPI] = useState(null);

  // 初始化时就定义window函数，避免未定义错误
  useEffect(() => {
    // 初始化Excalidraw状态
    if (typeof window.excalidrawState === 'undefined') {
      window.excalidrawState = {};
    }

    // 预定义所有函数，避免未定义错误
    window.setValue = (sceneData) => {
      console.log("setValue called with:", sceneData);
      if (excalidrawAPI && sceneData) {
        // 确保 collaborators 是数组格式
        if (sceneData.appState && sceneData.appState.collaborators && typeof sceneData.appState.collaborators === 'object' && !Array.isArray(sceneData.appState.collaborators)) {
          // 如果 collaborators 是对象而不是数组，将其转换为数组
          sceneData.appState.collaborators = Object.values(sceneData.appState.collaborators);
        }
        excalidrawAPI.updateScene(sceneData);
      } else {
        console.warn("Excalidraw API not ready or sceneData is null");
      }
    };

    window.reset = () => {
      console.log("reset called");
      if (excalidrawAPI) {
        excalidrawAPI.resetScene();
      } else {
        console.warn("Excalidraw API not ready");
      }
    };

    window.getContent = () => {
      console.log("getContent called");
      if (excalidrawAPI) {
        const elements = excalidrawAPI.getSceneElements();
        let appState = excalidrawAPI.getAppState();
        const files = excalidrawAPI.getFiles();
        
        // 确保 collaborators 是数组格式
        if (appState && appState.collaborators && typeof appState.collaborators === 'object' && !Array.isArray(appState.collaborators)) {
          // 如果 collaborators 是对象而不是数组，将其转换为数组
          appState = {
            ...appState,
            collaborators: Object.values(appState.collaborators)
          };
        }
        
        // 添加当前itemId到返回数据中
        const itemId = window.excalidrawState.currentItemId || '';
        
        return {
          elements,
          appState,
          files,
          itemId
        };
      } else {
        console.warn("Excalidraw API not ready");
        return { elements: [], appState: {}, files: {}, itemId: '' };
      }
    };

    // itemId 相关函数
    window.getCurrentItemId = () => {
      console.log("getCurrentItemId called");
      // 从excalidrawState获取当前的 itemId
      return window.excalidrawState.currentItemId || '';
    };

    window.setCurrentItemId = (itemId) => {
      console.log("setCurrentItemId called with:", itemId);
      // 设置当前的 itemId 到 excalidrawState
      window.excalidrawState.currentItemId = itemId || '';
    };

    console.log("Excalidraw functions initialized on window");
    console.log("Available functions:", {
      getContent: typeof window.getContent,
      setValue: typeof window.setValue,
      reset: typeof window.reset,
      getCurrentItemId: typeof window.getCurrentItemId,
      setCurrentItemId: typeof window.setCurrentItemId
    });

    // 清理函数
    return () => {
      // 组件卸载时清理window上的函数
      delete window.setValue;
      delete window.reset;
      delete window.getContent;
      delete window.getCurrentItemId;
      delete window.setCurrentItemId;
    };
  }, [excalidrawAPI]); // 依赖excalidrawAPI，当它变化时更新函数实现

  // 当 Excalidraw API 可用时更新状态
  const handleExcalidrawMount = (api) => {
    console.log("Excalidraw mounted with API:", !!api);
    setExcalidrawAPI(api);
  };

  const handleExcalidrawChange = (elements, appState, files) => {
    // 这个回调会在 Excalidraw 组件更新时触发
    // 我们可以在这里处理变化
    console.log("Excalidraw changed");
  };

  return (
    <div style={{ height: '100vh' }}>
      <Excalidraw 
        excalidrawAPI={handleExcalidrawMount}
        onChange={handleExcalidrawChange}
      />
    </div>
  );
}

export default App;