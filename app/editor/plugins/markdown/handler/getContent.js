(function() {
    try {
        console.log('开始获取Markdown编辑器内容和项目ID');
        
        // 获取当前项目ID
        let currentItemId = '';
        if (window.editorState && window.editorState.currentItemId !== undefined) {
            currentItemId = window.editorState.currentItemId;
        } else if (typeof window.getCurrentItemId === 'function') {
            currentItemId = window.getCurrentItemId();
        }
        
        // 获取Cherry编辑器内容
        if (window.editorState && window.editorState.editor && typeof window.editorState.editor.getValue === 'function') {
            const content = window.editorState.editor.getValue();
            return JSON.stringify({ success: true, ready: true, content: content || '', item_id: currentItemId });
        } 
        // 其他情况 - 编辑器实例未就绪，必须返回失败，避免后端误保存空内容
        else {
            console.warn('未找到支持的Markdown编辑器实例，编辑器未就绪');
            return JSON.stringify({
                success: false,
                ready: false,
                error_code: 'EDITOR_NOT_READY',
                error: 'Editor instance is not ready',
                item_id: currentItemId
            });
        }
    } catch (error) {
        console.error('获取Markdown编辑器内容失败:', error);
        return JSON.stringify({ success: false, ready: false, error: error.message });
    }
})();
