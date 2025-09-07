(function() {
    try {
        console.log('开始重置Markdown编辑器');
        
        // 重置Cherry编辑器
        if (window.editorState && window.editorState.editor && typeof window.editorState.editor.setValue === 'function') {
            window.editorState.editor.setValue('');
            console.log('Cherry编辑器内容已重置');
            return JSON.stringify({ success: true });
        } 
        // 其他情况
        else {
            console.warn('未找到支持的Markdown编辑器实例');
            return JSON.stringify({ success: false, error: '未找到支持的Markdown编辑器实例' });
        }
    } catch (error) {
        console.error('重置Markdown编辑器失败:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();