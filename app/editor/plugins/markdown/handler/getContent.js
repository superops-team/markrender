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
            return JSON.stringify({ success: true, content: content || '', item_id: currentItemId });
        } 
        // 其他情况 - 返回空内容而不是错误
        else {
            console.warn('未找到支持的Markdown编辑器实例，返回空内容');
            return JSON.stringify({ success: true, content: '', item_id: currentItemId });
        }
    } catch (error) {
        console.error('获取Markdown编辑器内容失败:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();