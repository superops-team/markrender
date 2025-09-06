(function() {
    try {
        // 使用default过滤器为未定义的变量提供默认值
        const action = {{ action|default('')|tojson }};
        const data = {{ data|default({})|tojson }};
        const requestId = {{ request_id|default('')|tojson }};
        
        if (typeof window.handleBackendMessage === 'function') {
            const result = window.handleBackendMessage(action, data, requestId);
            console.log('handleBackendMessage执行成功');
            // 如果结果已经是JSON字符串，直接返回；否则转换为JSON字符串
            if (typeof result === 'string' && (result.startsWith('{') || result.startsWith('['))) {
                return result;
            } else {
                return JSON.stringify({ success: true, result: result });
            }
        } else {
            console.warn('handleBackendMessage函数未定义');
            return JSON.stringify({ success: false, error: 'handleBackendMessage函数未定义' });
        }
    } catch (error) {
        console.error('执行handleBackendMessage时出错:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();