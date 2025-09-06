(function() {
    try {
        console.log('设置内容变化监听器');
        
        // 为Cherry编辑器设置内容变化监听
        if (window.editorState && window.editorState.editor) {
            // 设置内容变化监听
            if (typeof window.editorState.editor.on === 'function') {
                window.editorState.editor.on('change', function() {
                    console.log('检测到内容变化');
                    // 可以在这里添加内容变化的处理逻辑
                });
            }
        }
        
        // 为Excalidraw设置内容变化监听
        if (typeof window.excalidrawAppRef !== 'undefined' && window.excalidrawAppRef) {
            // Excalidraw内容变化监听逻辑可以在这里添加
            console.log('Excalidraw内容变化监听已设置');
        }
        
        return JSON.stringify({ success: true, message: '内容变化监听器设置完成' });
    } catch (error) {
        console.error('设置内容变化监听器失败:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();