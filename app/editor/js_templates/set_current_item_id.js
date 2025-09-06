(function() {
    try {
        // 使用default过滤器为未定义的变量提供默认值
        const itemId = {{ item_id|default('')|tojson }};
        console.log('开始设置当前项目ID:', itemId);
        // 设置当前项目ID
        if (window.editorState) {
            window.editorState.currentItemId = itemId;
            console.log('当前项目ID已设置:', itemId);
        }
        // Excalidraw特定处理
        if (typeof window.setCurrentItemId === 'function') {
            window.setCurrentItemId(itemId);
            console.log('Excalidraw当前项目ID已设置:', itemId);
        }
        return JSON.stringify({ success: true });
    } catch (error) {
        console.error('设置当前项目ID失败:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();