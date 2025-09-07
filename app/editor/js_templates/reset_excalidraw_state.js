(function() {
    try {
        console.log('开始重置Excalidraw特定状态');
        
        // 重置Excalidraw场景
        if (typeof window.updateScene === 'function') {
            window.updateScene({ elements: [] });
        } else if (window.excalidrawAppRef && typeof window.excalidrawAppRef.updateScene === 'function') {
            window.excalidrawAppRef.updateScene({ elements: [] });
        }
        
        // 清空localStorage中的Excalidraw数据
        if (typeof localStorage !== 'undefined') {
            for (let key in localStorage) {
                if (key.startsWith('excalidraw-') || key.includes('excalidraw')) {
                    localStorage.removeItem(key);
                }
            }
        }
        
        console.log('Excalidraw特定状态已重置');
        return JSON.stringify({ success: true, message: 'Excalidraw特定状态重置完成' });
    } catch (error) {
        console.error('重置Excalidraw特定状态失败:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();