import React, { useState, useRef, useCallback, useEffect } from 'react';
import { Tldraw } from '@tldraw/tldraw';
import '@tldraw/tldraw/tldraw.css';
// 移除WebChannelManager导入

interface BoardState {
  boardId: string | null;
  connectionStatus: 'connecting' | 'connected' | 'error';
  isLoading: boolean;
  unsavedChanges: boolean;
  saveInProgress: boolean;
}

const TLDrawBoard: React.FC = () => {
  const [boardState, setBoardState] = useState<BoardState>({
    boardId: null,
    connectionStatus: 'connected', // 默认为已连接状态
    isLoading: false,
    unsavedChanges: false,
    saveInProgress: false,
  });

  const editorRef = useRef<any>(null);
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

  // 保存画板
  const saveBoard = useCallback(async () => {
    if (!boardState.boardId || boardState.saveInProgress) {
      console.warn('无法保存：没有boardId或正在保存中');
      return;
    }

    console.log('💾 开始保存TLDraw画板:', boardState.boardId);
    setBoardState(prev => ({ ...prev, saveInProgress: true }));

    try {
      const snapshot = editorRef.current?.getSnapshot();
      if (!snapshot) {
        console.error('无法获取画板快照');
        return;
      }

      const drawingData = {
        snapshot: snapshot,
        metadata: {
          elementsCount: snapshot.store.length || 0,
          timestamp: new Date().toISOString(),
          lastModified: new Date().toISOString(),
        }
      };

      // 移除对WebChannelManager的调用，改为使用全局handleBackendMessage函数
      if (typeof window.handleBackendMessage === 'function') {
        const response = window.handleBackendMessage('saveTLDrawBoard', {
          boardId: boardState.boardId,
          drawingData: drawingData
        });
        
        if (response && response.success) {
          console.log('✅ 画板保存成功');
          setBoardState(prev => ({ ...prev, unsavedChanges: false }));
        } else {
          console.error('❌ 画板保存失败:', response?.error || '未知错误');
        }
      } else {
        console.error('❌ handleBackendMessage函数未定义');
      }
    } catch (error) {
      console.error('保存画板时出错:', error);
    } finally {
      setBoardState(prev => ({ ...prev, saveInProgress: false }));
    }
  }, [boardState.boardId, boardState.saveInProgress]);

  // 加载画板
  const loadBoard = useCallback(async (boardId: string) => {
    console.log('📂 开始加载TLDraw画板:', boardId);
    setBoardState(prev => ({ ...prev, isLoading: true }));

    try {
      // 移除对WebChannelManager的调用，改为使用全局handleBackendMessage函数
      if (typeof window.handleBackendMessage === 'function') {
        const response = window.handleBackendMessage('loadTLDrawBoard', {
          boardId: boardId
        });
        
        if (response && response.success && response.data?.drawingData) {
          const loadedData = response.data.drawingData;
          console.log('📝 画板数据加载成功:', loadedData);
          
          if (loadedData.snapshot && editorRef.current) {
            editorRef.current.loadSnapshot(loadedData.snapshot);
          }
          
          setBoardState(prev => ({ ...prev, unsavedChanges: false }));
        } else if (response && response.success && !response.data) {
          console.log('📋 新建画板');
          // 新建画板，使用默认数据
          setBoardState(prev => ({ ...prev, unsavedChanges: false }));
        } else {
          console.error('❌ 画板加载失败:', response?.error || '未知错误');
        }
      } else {
        console.error('❌ handleBackendMessage函数未定义');
      }
    } catch (error) {
      console.error('加载画板时出错:', error);
    } finally {
      setBoardState(prev => ({ ...prev, isLoading: false }));
    }
  }, []);

  // 处理设置boardId
  const handleSetBoardId = useCallback((data: any) => {
    console.log('🏷️ 设置画板ID:', data.boardId);
    setBoardState(prev => ({
      ...prev,
      boardId: data.boardId,
    }));
    
    // 自动加载画板数据
    if (data.boardId) {
      loadBoard(data.boardId);
    }
  }, [loadBoard]);

  // 处理编辑器变化 - 注意：Tldraw组件没有onChange属性，使用自定义方式处理变化
  const handleEditorChange = useCallback(() => {
    if (boardState.isLoading) return;
    
    console.log('📝 画板数据变化');
    setBoardState(prev => ({ ...prev, unsavedChanges: true }));
    autoSave();
  }, [autoSave, boardState.isLoading]);

  // 移除WebChannel监听相关的useEffect，改为直接初始化
  useEffect(() => {
    console.log('🔄 TLDrawBoard初始化完成');
    
    // 设置为已连接状态
    setBoardState(prev => ({ ...prev, connectionStatus: 'connected' }));
    
    // 如果有boardId，尝试加载数据
    // 实际的加载应该通过后端主动调用handleBackendMessage来触发
    
    return () => {
      if (autoSaveTimeoutRef.current) {
        clearTimeout(autoSaveTimeoutRef.current);
      }
    };
  }, []);

  // 初始化编辑器后设置变化检测
  useEffect(() => {
    if (editorRef.current && !boardState.isLoading) {
      // 这里可以添加自定义的变化检测逻辑
      const checkChanges = () => {
        handleEditorChange();
      };
      
      // 模拟变化检测（实际项目中应根据Tldraw API实现）
      const interval = setInterval(checkChanges, 1000);
      
      return () => clearInterval(interval);
    }
  }, [editorRef.current, boardState.isLoading, handleEditorChange]);

  return (
    <div style={{ width: '100%', height: '100vh', position: 'relative' }}>
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