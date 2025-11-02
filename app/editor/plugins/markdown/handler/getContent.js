git a(function() {
    try {
        console.log('开始获取Markdown编辑器内容和项目ID');
        
        // 获取当前项目ID
        let itemId = '';
        if (window.editorState && window.editorState.currentItemId) {
            itemId = window.editorState.currentItemId;
            console.log('通过新接口获取到当前项目ID:', itemId);
        } else if (typeof window.getCurrentItemId === 'function') {
            itemId = window.getCurrentItemId();
            console.log('通过旧接口获取到当前项目ID:', itemId);
        } else {
            console.warn('无法获取当前项目ID');
        }
        
        // 获取编辑器内容
        if (window.editorState && window.editorState.editor && typeof window.editorState.editor.getValue === 'function') {
            const content = window.editorState.editor.getValue() || '';
            
            // 检查内容长度，避免过大的内容导致性能问题
            if (content.length > 5000000) {  // 5MB限制
                console.warn('内容过大，可能影响性能，长度:', content.length);
            }
            
            console.log('通过新接口获取到Markdown内容，长度:', content.length);
            return JSON.stringify({ success: true, content: content, item_id: itemId });
        } 
        // 处理其他可能的编辑器
        else {
            console.warn('未找到支持的Markdown编辑器实例');
            return JSON.stringify({ success: false, error: '未找到支持的Markdown编辑器实例' });
        }
    } catch (error) {
        console.error('获取Markdown编辑器内容失败:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();