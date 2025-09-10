(function() {
    try {
        console.log('开始重置Excalidraw编辑器');
        
        // 重置Excalidraw - 使用新的接口
        if (typeof window.reset === 'function') {
            try {
                console.log("reset called");
                window.reset();
                console.log('通过新接口重置Excalidraw内容完成');
                return JSON.stringify({ success: true });
            } catch (e) {
                console.error("reset error:", e);
                return JSON.stringify({ success: false, error: e.message });
            }
        }
        // 兼容旧的接口
        else if (typeof window.loadExcalidrawData === 'function') {
            window.loadExcalidrawData('[]');
            console.log('通过旧接口重置Excalidraw内容完成');
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