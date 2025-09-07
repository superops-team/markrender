(function() {
    try {
        console.log('开始重置Excalidraw编辑器');
        
        // 重置Excalidraw
        if (typeof window.loadExcalidrawData === 'function') {
            window.loadExcalidrawData('[]');
            console.log('Excalidraw内容已重置');
            return JSON.stringify({ success: true });
        }
        // 其他情况
        else {
            console.warn('未找到支持的Excalidraw编辑器实例');
            return JSON.stringify({ success: false, error: '未找到支持的Excalidraw编辑器实例' });
        }
    } catch (error) {
        console.error('重置Excalidraw编辑器失败:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();