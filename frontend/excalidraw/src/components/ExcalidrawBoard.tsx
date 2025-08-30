import React, { useState, useEffect, useRef, useCallback } from 'react';
import { Excalidraw } from '@excalidraw/excalidraw';
import { webChannelManager, webChannel } from '../service/webchannel';
import type { ExcalidrawData, BoardMetadata } from '../service/webchannel';

// 组件状态接口
interface BoardState {
  boardId: string | null;
  connectionStatus: 'connecting' | 'connected' | 'error';
  isLoading: boolean;
  unsavedChanges: boolean;
  saveInProgress: boolean;
}

const ExcalidrawBoard: React.FC = () => {
  // Excalidraw数据状态
  const [excalidrawData, setExcalidrawData] = useState<ExcalidrawData>({
    elements: [],
    appState: {
      theme: 'light',
      viewModeEnabled: false,
      zenModeEnabled: false,
      gridSize: null,
    },
    files: {},
  });

  // 白板状态
  const [boardState, setBoardState] = useState<BoardState>({
    boardId: null,
    connectionStatus: 'connecting',
    isLoading: false,
    unsavedChanges: false,
    saveInProgress: false,
  });

  const excalidrawRef = useRef<any>(null);
  const autoSaveTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // 自动保存函数（防抖）
  const autoSave = useCallback(() => {
    if (autoSaveTimeoutRef.current) {
      clearTimeout(autoSaveTimeoutRef.current);
    }
    
    autoSaveTimeoutRef.current = setTimeout(() => {
      if (boardState.unsavedChanges && boardState.boardId && !boardState.saveInProgress) {
        saveBoard();
      }
    }, 2000);
  }, [boardState.unsavedChanges, boardState.boardId, boardState.saveInProgress]);

  // 保存白板
  const saveBoard = useCallback(async () => {
    if (!boardState.boardId || boardState.saveInProgress) {
      console.warn('无法保存：没有boardId或正在保存中');
      return;
    }

    console.log('💾 开始保存白板:', boardState.boardId);
    setBoardState(prev => ({ ...prev, saveInProgress: true }));

    try {
      const metadata: BoardMetadata = {
        elementsCount: excalidrawData.elements.length,
        timestamp: new Date().toISOString(),
        lastModified: new Date().toISOString(),
      };

      const response = await webChannelManager.saveExcalidrawBoard(
        boardState.boardId,
        excalidrawData,
        metadata
      );

      if (response.success) {
        console.log('✅ 白板保存成功');
        setBoardState(prev => ({ ...prev, unsavedChanges: false }));
      } else {
        console.error('❌ 白板保存失败:', response.error);
      }
    } catch (error) {
      console.error('保存白板时出错:', error);
    } finally {
      setBoardState(prev => ({ ...prev, saveInProgress: false }));
    }
  }, [boardState.boardId, boardState.saveInProgress, excalidrawData]);

  // 加载白板
  const loadBoard = useCallback(async (boardId: string) => {
    console.log('📂 开始加载白板:', boardId);
    setBoardState(prev => ({ ...prev, isLoading: true }));

    try {
      const response = await webChannelManager.loadExcalidrawBoard(boardId);
      
      if (response.success && response.data?.drawingData) {
        const loadedData = response.data.drawingData;
        console.log('📝 白板数据加载成功:', loadedData);
        
        setExcalidrawData({
          elements: loadedData.elements || [],
          appState: {
            ...excalidrawData.appState,
            ...loadedData.appState,
          },
          files: loadedData.files || {},
        });
        
        setBoardState(prev => ({ ...prev, unsavedChanges: false }));
      } else if (response.success && !response.data) {
        console.log('📋 新建白板');
        // 新建白板，使用默认数据
        setExcalidrawData({
          elements: [],
          appState: {
            theme: 'light',
            viewModeEnabled: false,
            zenModeEnabled: false,
            gridSize: null,
          },
          files: {},
        });
        setBoardState(prev => ({ ...prev, unsavedChanges: false }));
      } else {
        console.error('❌ 白板加载失败:', response.error);
      }
    } catch (error) {
      console.error('加载白板时出错:', error);
    } finally {
      setBoardState(prev => ({ ...prev, isLoading: false }));
    }
  }, [excalidrawData.appState]);

  // 导出白板
  const exportBoard = useCallback(async (format: string = 'png') => {
    if (!boardState.boardId) {
      console.warn('无法导出：没有boardId');
      return;
    }

    console.log('📷 开始导出白板:', format);
    
    try {
      // 使用Excalidraw的exportToBlob函数
      const { exportToBlob } = await import('@excalidraw/excalidraw');
      
      const blob = await exportToBlob({
        elements: excalidrawData.elements,
        appState: excalidrawData.appState,
        files: excalidrawData.files,
        mimeType: `image/${format}`,
        quality: 1,
      });

      const reader = new FileReader();
      reader.onload = async () => {
        try {
          const response = await webChannelManager.exportExcalidrawBoard(
            boardState.boardId!,
            format,
            reader.result as string
          );

          if (response.success) {
            console.log('✅ 白板导出成功:', response);
          } else {
            console.error('❌ 白板导出失败:', response.error);
          }
        } catch (error) {
          console.error('❌ 导出请求失败:', error);
        }
      };
      reader.readAsDataURL(blob);
    } catch (error) {
      console.error('导出白板时出错:', error);
    }
  }, [boardState.boardId, excalidrawData]);

  // 清空白板
  const clearBoard = useCallback(() => {
    if (confirm('确定要清空白板吗？此操作无法撤销。')) {
      console.log('🗑️ 清空白板');
      setExcalidrawData(prev => ({
        ...prev,
        elements: [],
      }));
      setBoardState(prev => ({ ...prev, unsavedChanges: true }));
    }
  }, []);

  // 处理设置boardId
  const handleSetBoardId = useCallback((data: any) => {
    console.log('🏷️ 设置白板ID:', data.boardId);
    setBoardState(prev => ({
      ...prev,
      boardId: data.boardId,
    }));
    
    // 自动加载白板数据
    if (data.boardId) {
      loadBoard(data.boardId);
    }
  }, [loadBoard]);

  // 处理加载白板数据请求
  const handleLoadExcalidrawData = useCallback((data: any) => {
    console.log('📝 处理加载白板数据请求:', data);
    if (data.boardId) {
      loadBoard(data.boardId);
    } else if (data.drawingData) {
      try {
        const parsedData = typeof data.drawingData === 'string' 
          ? JSON.parse(data.drawingData) 
          : data.drawingData;

        setExcalidrawData({
          elements: parsedData.elements || [],
          appState: {
            ...excalidrawData.appState,
            ...parsedData.appState,
          },
          files: parsedData.files || {},
        });

        setBoardState(prev => ({ ...prev, unsavedChanges: false }));
        console.log('✅ 白板数据加载完成');
      } catch (error) {
        console.error('❌ 解析白板数据失败:', error);
      }
    }
  }, [loadBoard, excalidrawData.appState]);

  // ⚠️ 关键修复：正确处理Excalidraw的onChange事件，避免无限循环
  const handleExcalidrawChange = useCallback((elements: readonly any[], appState: any, files: any) => {
    // 防止无意义的更新
    if (boardState.isLoading) return;
    
    console.log('📝 白板数据变化:', {
      elementsCount: elements.length,
      hasFiles: !!files && Object.keys(files).length > 0
    });
    
    setExcalidrawData({ elements: [...elements], appState, files });
    setBoardState(prev => ({ ...prev, unsavedChanges: true }));
    autoSave();
  }, [autoSave, boardState.isLoading]);

  // 快捷键处理
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if ((event.ctrlKey || event.metaKey) && event.key === 's') {
        event.preventDefault();
        console.log('⌨️ 快捷键保存');
        saveBoard();
      } else if ((event.ctrlKey || event.metaKey) && event.key === 'e') {
        event.preventDefault();
        console.log('⌨️ 快捷键导出');
        exportBoard();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [saveBoard, exportBoard]);

  // 页面卸载前检查未保存更改
  useEffect(() => {
    const handleBeforeUnload = (event: BeforeUnloadEvent) => {
      if (boardState.unsavedChanges) {
        event.preventDefault();
        event.returnValue = '您有未保存的更改，确定要离开吗？';
        return '您有未保存的更改，确定要离开吗？';
      }
    };

    window.addEventListener('beforeunload', handleBeforeUnload);
    return () => window.removeEventListener('beforeunload', handleBeforeUnload);
  }, [boardState.unsavedChanges]);

  // 初始化WebChannel监听
  useEffect(() => {
    console.log('🔄 初始化ExcalidrawBoard WebChannel监听器');
    
    // 添加事件监听器
    webChannel.on('setBoardId', handleSetBoardId);
    webChannel.on('loadExcalidrawData', handleLoadExcalidrawData);
    webChannel.on('clearBoard', clearBoard);
    webChannel.on('connectionReady', () => {
      console.log('🟢 WebChannel连接就绪');
      setBoardState(prev => ({ ...prev, connectionStatus: 'connected' }));
    });

    // 注册Editor相关消息处理器（兼容性处理）
    webChannel.on('registerEditorEvents', (data: any, _requestId?: string) => {
      console.log('📝 收到registerEditorEvents消息（Excalidraw页面忽略）:', data);
      // Excalidraw页面不需要处理Editor事件，静默忽略
    });
    
    webChannel.on('setupContentChangeListener', (data: any, _requestId?: string) => {
      console.log('📝 收到setupContentChangeListener消息（Excalidraw页面忽略）:', data);
      // Excalidraw页面不需要处理内容变化监听器，静默忽略
    });

    // 等待WebChannel就绪后发送前端就绪消息
    const initializeWebChannel = async () => {
      try {
        console.log('🔄 开始初始化WebChannel连接...');
        
        // 检查WebChannel是否真正就绪
        const maxRetries = 10;
        let retryCount = 0;
        
        const checkConnection = async (): Promise<boolean> => {
          if (webChannelManager.isReady()) {
            try {
              console.log('📤 发送前端就绪消息');
              const response = await webChannelManager.sendFrontendReady();
              console.log('📥 前端就绪响应:', response);
              
              // 更健壮的响应判断逻辑
              if (response && response.success) {
                console.log('✅ WebChannel连接验证成功');
                setBoardState(prev => ({ ...prev, connectionStatus: 'connected' }));
                return true;
              } else {
                const errorMsg = response?.error || '未知错误';
                console.warn('⚠️ 前端就绪响应失败:', errorMsg);
                return false;
              }
            } catch (error) {
              console.error('❌ 发送前端就绪消息失败:', error);
              return false;
            }
          } else {
            console.log(`⏳ WebChannel未就绪，重试 ${retryCount + 1}/${maxRetries}`);
            return false;
          }
        };
        
        // 连接验证循环
        while (retryCount < maxRetries) {
          setBoardState(prev => ({ ...prev, connectionStatus: 'connecting' }));
          
          if (await checkConnection()) {
            return; // 连接成功，退出函数
          }
          
          retryCount++;
          if (retryCount < maxRetries) {
            await new Promise(resolve => setTimeout(resolve, 300));
          }
        }
        
        // 所有重试都失败，设置为错误状态
        console.warn('❌ WebChannel连接验证最终失败，使用离线模式');
        setBoardState(prev => ({ ...prev, connectionStatus: 'error' }));
        
      } catch (error) {
        console.error('❌ WebChannel初始化异常:', error);
        setBoardState(prev => ({ ...prev, connectionStatus: 'error' }));
      }
    };

    // 立即检查或等待就绪
    if (webChannelManager.isReady()) {
      console.log('🚀 WebChannel已就绪，立即初始化');
      initializeWebChannel();
    } else {
      console.log('⏳ WebChannel未就绪，注册就绪回调');
      setBoardState(prev => ({ ...prev, connectionStatus: 'connecting' }));
      webChannelManager.onReady(() => {
        console.log('🔔 收到WebChannel就绪通知');
        initializeWebChannel();
      });
    }

    // 清理函数
    return () => {
      webChannel.off('setBoardId', handleSetBoardId);
      webChannel.off('loadExcalidrawData', handleLoadExcalidrawData);
      webChannel.off('clearBoard', clearBoard);
      webChannel.off('registerEditorEvents', () => {});
      webChannel.off('setupContentChangeListener', () => {});
      
      if (autoSaveTimeoutRef.current) {
        clearTimeout(autoSaveTimeoutRef.current);
      }
    };
  }, [handleSetBoardId, handleLoadExcalidrawData, clearBoard]);

  // 渲染组件
  return (
    <div ref={excalidrawRef} style={{ width: '100%', height: '100vh', position: 'relative' }}>
      {/* 连接状态指示器 */}
      <div style={{
        position: 'absolute',
        top: 10,
        right: 10,
        zIndex: 1000,
        padding: '4px 8px',
        borderRadius: '4px',
        fontSize: '12px',
        fontWeight: 'bold',
        color: 'white',
        backgroundColor: boardState.connectionStatus === 'connected' ? '#28a745' : 
                        boardState.connectionStatus === 'connecting' ? '#ffc107' : '#dc3545',
      }}>
        {boardState.connectionStatus === 'connected' ? '🟢 已连接' :
         boardState.connectionStatus === 'connecting' ? '🟡 连接中' : '🔴 离线'}
      </div>

      {/* 保存状态指示器 */}
      {boardState.unsavedChanges && (
        <div style={{
          position: 'absolute',
          top: 10,
          left: 10,
          zIndex: 1000,
          padding: '4px 8px',
          borderRadius: '4px',
          fontSize: '12px',
          color: 'white',
          backgroundColor: boardState.saveInProgress ? '#007bff' : '#ffc107',
        }}>
          {boardState.saveInProgress ? '💾 保存中...' : '⚠️ 有未保存更改'}
        </div>
      )}

      {/* Excalidraw组件 */}
      <Excalidraw
        initialData={{
          elements: excalidrawData.elements,
          appState: excalidrawData.appState,
          files: excalidrawData.files,
        }}
        onChange={handleExcalidrawChange}
        theme={excalidrawData.appState.theme || 'light'}
      />
    </div>
  );
};

export default ExcalidrawBoard;