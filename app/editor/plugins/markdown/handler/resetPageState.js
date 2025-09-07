(function() {
    try {
        console.log('开始重置Markdown页面状态');
        
        // 重置Markdown编辑器状态
        if (window.editorState) {
            window.editorState.currentItemId = null;
            console.log('Markdown编辑器状态已重置');
        }
        
        console.log('Markdown页面状态重置完成');
        return JSON.stringify({ success: true, message: 'Markdown页面状态重置完成' });
    } catch (error) {
        console.error('重置Markdown页面状态失败:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();