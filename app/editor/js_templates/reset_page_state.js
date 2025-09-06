(function() {
    try {
        console.log('开始重置页面状态');
        
        // 重置编辑器状态
        if (window.editorState) {
            window.editorState.currentItemId = null;
            console.log('编辑器状态已重置');
        }
        
        // 重置Excalidraw状态
        if (typeof window.resetExcalidraw === 'function') {
            window.resetExcalidraw();
            console.log('Excalidraw状态已重置');
        }
        
        // 重置其他可能的状态
        if (typeof window.currentItemId !== 'undefined') {
            window.currentItemId = null;
            console.log('当前项目ID已重置');
        }
        
        console.log('页面状态重置完成');
        return JSON.stringify({ success: true, message: '页面状态重置完成' });
    } catch (error) {
        console.error('重置页面状态失败:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();