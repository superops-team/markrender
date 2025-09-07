(function() {
    try {
        // 使用default过滤器为未定义的变量提供默认值
        const content = {{ content|default('')|tojson }};
        const itemId = {{ item_id|default('')|tojson }};
        console.log('开始设置编辑器内容和项目ID:', itemId);
        
        // 设置当前项目ID
        if (window.editorState) {
            window.editorState.currentItemId = itemId;
            console.log('当前项目ID已设置:', itemId);
        }
        
        // 默认情况 - 未找到支持的编辑器实例
        console.warn('使用了通用的编辑器内容设置方法，未找到支持的编辑器实例');
        return JSON.stringify({ success: false, error: '未找到支持的编辑器实例' });
    } catch (error) {
        console.error('设置编辑器内容失败:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();