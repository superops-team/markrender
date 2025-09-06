(function() {
    try {
        console.log('设置内容变化监听器');
        
        // 初始化editorState对象
        if (!window.editorState) {
            window.editorState = {};
        }
        
        // 为Excalidraw设置内容变化监听
        if (typeof window.excalidrawAppRef !== 'undefined' && window.excalidrawAppRef) {
            // Excalidraw内容变化监听逻辑
            console.log('Excalidraw内容变化监听已设置');
            
            // 如果Excalidraw提供了场景变化监听接口
            if (window.excalidrawAppRef && typeof window.excalidrawAppRef.onSceneChange === 'function') {
                window.excalidrawAppRef.onSceneChange(function() {
                    console.log('检测到Excalidraw场景变化');
                });
            }
        }
        
        return JSON.stringify({ success: true, message: '内容变化监听器设置完成' });
    } catch (error) {
        console.error('设置内容变化监听器失败:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();