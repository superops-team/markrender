(function() {
    try {
        console.log('开始获取编辑器内容和项目ID');
        
        // 获取当前项目ID
        let currentItemId = '';
        if (window.editorState && window.editorState.currentItemId !== undefined) {
            currentItemId = window.editorState.currentItemId;
        } else if (typeof window.getCurrentItemId === 'function') {
            currentItemId = window.getCurrentItemId();
        }
        
        // 默认返回空内容
        console.warn('使用了通用的编辑器内容获取方法，返回空内容');
        return JSON.stringify({ success: true, content: '', item_id: currentItemId });
    } catch (error) {
        console.error('获取编辑器内容失败:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();