(function() {
    try {
        console.log('开始获取Excalidraw编辑器内容和项目ID');
        
        // 获取当前项目ID - 优先使用新的接口
        let currentItemId = '';
        if (typeof window.getCurrentItemId === 'function') {
            currentItemId = window.getCurrentItemId();
            console.log('通过新接口获取到当前项目ID:', currentItemId);
        } else if (window.editorState && window.editorState.currentItemId !== undefined) {
            currentItemId = window.editorState.currentItemId;
            console.log('通过editorState获取到当前项目ID:', currentItemId);
        }
        
        // 获取Excalidraw内容 - 使用新的接口
        if (typeof window.getContent === 'function') {
            try {
                const content = window.getContent();
                console.log('通过新接口获取到Excalidraw内容:', content);
                
                // 新接口直接返回对象，不需要额外的JSON处理
                if (content) {
                    // 如果内容中包含itemId，则使用它
                    if (content.itemId !== undefined) {
                        currentItemId = content.itemId;
                    }
                    
                    // 确保 collaborators 是数组格式（修复之前的错误）
                    let processedContent = content;
                    if (content.appState && content.appState.collaborators && typeof content.appState.collaborators === 'object' && !Array.isArray(content.appState.collaborators)) {
                        processedContent = {
                            ...content,
                            appState: {
                                ...content.appState,
                                collaborators: Object.values(content.appState.collaborators)
                            }
                        };
                    }
                    
                    return JSON.stringify({ 
                        success: true, 
                        ready: true,
                        content: processedContent, 
                        item_id: currentItemId 
                    });
                } else {
                    return JSON.stringify({ success: true, ready: true, content: {}, item_id: currentItemId });
                }
            } catch (e) {
                console.error("getContent error:", e);
                return JSON.stringify({ success: false, ready: false, error: e.message });
            }
        }
        // 兼容旧的接口
        else if (typeof window.getExcalidrawData === 'function') {
            const content = window.getExcalidrawData();
            console.log('获取到Excalidraw内容，长度:', content ? content.length : 0);
            return JSON.stringify({ success: true, ready: true, content: content || '[]', item_id: currentItemId });
        }
        // 检查Excalidraw的其他可能状态
        else if (typeof window.excalidrawAppRef !== 'undefined' && window.excalidrawAppRef) {
            try {
                const elements = window.excalidrawAppRef.getSceneElements();
                const content = JSON.stringify(elements);
                console.log('通过excalidrawAppRef获取到Excalidraw内容，长度:', content ? content.length : 0);
                return JSON.stringify({ success: true, ready: true, content: content || '[]', item_id: currentItemId });
            } catch (ex) {
                console.warn('通过excalidrawAppRef获取Excalidraw内容失败:', ex);
                // 返回错误信息
                return JSON.stringify({ success: false, ready: false, error: '获取Excalidraw内容失败: ' + ex.message });
            }
        }
        // 其他情况 - 编辑器实例未就绪，必须返回失败，避免后端误保存空内容
        else {
            console.warn('未找到支持的Excalidraw编辑器实例，编辑器未就绪');
            // 添加更多调试信息
            console.log('当前window对象状态:', {
                hasEditorState: !!window.editorState,
                hasExcalidrawAppRef: typeof window.excalidrawAppRef !== 'undefined',
                hasGetExcalidrawData: typeof window.getExcalidrawData === 'function',
                hasGetContent: typeof window.getContent === 'function',
                hasGetCurrentItemId: typeof window.getCurrentItemId === 'function'
            });
            return JSON.stringify({
                success: false,
                ready: false,
                error_code: 'EDITOR_NOT_READY',
                error: 'Editor instance is not ready',
                item_id: currentItemId
            });
        }
    } catch (error) {
        console.error('获取Excalidraw编辑器内容失败:', error);
        return JSON.stringify({ success: false, ready: false, error: error.message });
    }
})();
