(function() {
    try {
        // 使用default过滤器为未定义的变量提供默认值
        const response = {{ response|default({})|tojson }};
        const callbackId = {{ callback_id|default('')|tojson }};
        
        console.log('处理后端响应:', callbackId, response);
        
        // 查找并执行回调函数
        if (window.webCallbacks && window.webCallbacks[callbackId]) {
            window.webCallbacks[callbackId](response);
            delete window.webCallbacks[callbackId];
            return JSON.stringify({ success: true });
        } else {
            console.warn('未找到回调函数:', callbackId);
            return JSON.stringify({ success: false, error: '未找到回调函数' });
        }
    } catch (error) {
        console.error('处理后端响应失败:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();