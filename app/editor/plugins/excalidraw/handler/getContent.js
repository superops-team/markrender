(function() {
    try {
        console.log('开始获取Excalidraw编辑器内容和项目ID');
        
        // 获取当前项目ID
        let currentItemId = '';
        if (window.editorState && window.editorState.currentItemId !== undefined) {
            currentItemId = window.editorState.currentItemId;
        } else if (typeof window.getCurrentItemId === 'function') {
            currentItemId = window.getCurrentItemId();
        }
        
        // 获取Excalidraw内容
        if (typeof window.getExcalidrawData === 'function') {
            const content = window.getExcalidrawData();
            console.log('获取到Excalidraw内容，长度:', content ? content.length : 0);
            return JSON.stringify({ success: true, content: content || '[]', item_id: currentItemId });
        }
        // 检查Excalidraw的其他可能状态
        else if (typeof window.excalidrawAppRef !== 'undefined' && window.excalidrawAppRef) {
            try {
                const elements = window.excalidrawAppRef.getSceneElements();
                const content = JSON.stringify(elements);
                console.log('通过excalidrawAppRef获取到Excalidraw内容，长度:', content ? content.length : 0);
                return JSON.stringify({ success: true, content: content || '[]', item_id: currentItemId });
            } catch (ex) {
                console.warn('通过excalidrawAppRef获取Excalidraw内容失败:', ex);
                // 返回错误信息
                return JSON.stringify({ success: false, error: '获取Excalidraw内容失败: ' + ex.message });
            }
        }
        // 其他情况 - 返回空内容而不是错误
        else {
            console.warn('未找到支持的Excalidraw编辑器实例，返回空内容');
            // 添加更多调试信息
            console.log('当前window对象状态:', {
                hasEditorState: !!window.editorState,
                hasExcalidrawAppRef: typeof window.excalidrawAppRef !== 'undefined',
                hasGetExcalidrawData: typeof window.getExcalidrawData === 'function'
            });
            return JSON.stringify({ success: true, content: '[]', item_id: currentItemId });
        }
    } catch (error) {
        console.error('获取Excalidraw编辑器内容失败:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();