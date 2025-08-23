import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Excalidraw } from '@excalidraw/excalidraw';
import { webChannel } from '../service/webchannel';

const ExcalidrawBoard: React.FC = () => {
  const [elements, setElements] = useState<any[]>([]);
  const [appState, setAppState] = useState<{ 
    theme: 'light' | 'dark'; 
    viewModeEnabled: boolean;
  }>({
    theme: 'light',
    viewModeEnabled: false,
  });

  const excalidrawRef = useRef<HTMLDivElement>(null);
  
  // 使用useCallback包装处理函数
  const handleSetExcalidrawData = useCallback((data: any) => {
    console.log('Received setExcalidrawData:', data);
    if (data.elements) {
      setElements(data.elements);
    }
    if (data.appState) {
      setAppState(prev => ({ ...prev, ...data.appState }));
    }
  }, []);

  const handleGetExcalidrawData = useCallback(() => {
    webChannel.send('excalidrawData', {
      elements,
      appState
    });
  }, [elements, appState]);

  // 初始化WebChannel监听
  useEffect(() => {
    // 添加事件监听器
    webChannel.on('setExcalidrawData', handleSetExcalidrawData);
    webChannel.on('getExcalidrawData', handleGetExcalidrawData);

    // 发送初始化完成消息
    webChannel.send('frontendReady', {});

    // 清理函数，移除事件监听器
    return () => {
      webChannel.off('setExcalidrawData', handleSetExcalidrawData);
      webChannel.off('getExcalidrawData', handleGetExcalidrawData);
    };
  }, [handleSetExcalidrawData, handleGetExcalidrawData]);

  return (
    <div ref={excalidrawRef} style={{ width: '100%', height: '100vh' }}>
      <Excalidraw
        elements={elements}
        setElements={setElements}
        appState={appState}
        setAppState={setAppState}
        theme={appState.theme}
      />
    </div>
  );
};

export default ExcalidrawBoard;