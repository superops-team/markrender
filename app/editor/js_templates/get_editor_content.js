(function() {
    try {
        console.log('开始获取编辑器内容');
        
        // 首先尝试使用防抖机制确保获取到最新内容
        if (window.editorState && window.editorState.lastContent) {
            console.log('使用缓存的最新内容，长度:', window.editorState.lastContent.length);
            return JSON.stringify({ success: true, content: window.editorState.lastContent });
        }
        
        // 获取Cherry编辑器内容
        if (window.editorState && window.editorState.editor && typeof window.editorState.editor.getValue === 'function') {
            const content = window.editorState.editor.getValue();
            console.log('获取到Cherry编辑器内容，长度:', content ? content.length : 0);
            return JSON.stringify({ success: true, content: content || '' });
        } 
        // 获取Excalidraw内容
        else if (typeof window.getExcalidrawData === 'function') {
            const content = window.getExcalidrawData();
            console.log('获取到Excalidraw内容，长度:', content ? content.length : 0);
            return JSON.stringify({ success: true, content: content || '[]' });
        }
        // 检查Excalidraw的其他可能状态
        else if (typeof window.excalidrawAppRef !== 'undefined' && window.excalidrawAppRef) {
            try {
                const elements = window.excalidrawAppRef.getSceneElements();
                const content = JSON.stringify(elements);
                console.log('通过excalidrawAppRef获取到Excalidraw内容，长度:', content ? content.length : 0);
                return JSON.stringify({ success: true, content: content || '[]' });
            } catch (ex) {
                console.warn('通过excalidrawAppRef获取Excalidraw内容失败:', ex);
            }
        }
        // 其他情况 - 返回空内容而不是错误
        else {
            console.warn('未找到支持的编辑器实例，返回空内容');
            // 添加更多调试信息
            console.log('当前window对象状态:', {
                hasEditorState: !!window.editorState,
                hasExcalidrawAppRef: typeof window.excalidrawAppRef !== 'undefined',
                hasGetExcalidrawData: typeof window.getExcalidrawData === 'function'
            });
            return JSON.stringify({ success: true, content: '' });
        }
    } catch (error) {
        console.error('获取编辑器内容失败:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();