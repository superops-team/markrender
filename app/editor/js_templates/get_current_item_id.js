(function() {
    try {
        console.log('开始获取当前项目ID');
        
        // 获取当前项目ID
        let currentItemId = '';
        if (window.editorState && window.editorState.currentItemId !== undefined) {
            currentItemId = window.editorState.currentItemId;
        } else if (typeof window.getCurrentItemId === 'function') {
            currentItemId = window.getCurrentItemId();
        }
        
        console.log('获取到当前项目ID:', currentItemId);
        return JSON.stringify({ success: true, item_id: currentItemId });
    } catch (error) {
        console.error('获取当前项目ID失败:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();