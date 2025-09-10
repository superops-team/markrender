(function() {
    try {
        // 使用default过滤器为未定义的变量提供默认值
        const itemId = {{ item_id|default('')|tojson }};
        console.log('开始设置Excalidraw当前项目ID:', itemId);
        
        // 设置Excalidraw特定的项目ID状态
        if (typeof window.excalidrawState === 'undefined') {
            window.excalidrawState = {};
        }
        window.excalidrawState.currentItemId = itemId;
        console.log('Excalidraw当前项目ID已设置:', itemId);
        
        // 同时更新通用的editorState
        if (window.editorState) {
            window.editorState.currentItemId = itemId;
            console.log('通用当前项目ID已设置:', itemId);
        }
        
        // 如果Excalidraw API可用，也可以存储在Excalidraw的某个状态中
        if (window.excalidrawAPI) {
            // 可以选择将item_id存储在Excalidraw的某个状态中
            console.log('Excalidraw API可用，item_id已同步');
        }
        
        return JSON.stringify({ success: true });
    } catch (error) {
        console.error('设置Excalidraw当前项目ID失败:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();