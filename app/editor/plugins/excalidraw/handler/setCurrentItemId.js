(function() {
    try {
        // 使用default过滤器为未定义的变量提供默认值
        const itemId = {{ item_id|default('')|tojson }};
        console.log('开始设置Excalidraw当前项目ID:', itemId);
        
        // 设置Excalidraw特定的项目ID状态
        if (typeof window.excalidrawState === 'undefined') {
            window.excalidrawState = {};
        }
        window.e