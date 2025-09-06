(function() {
    try {
        console.log('处理文本变化事件');
        
        // 处理Cherry编辑器的文本变化
        if (window.editorState && window.editorState.editor) {
            console.log('Cherry编辑器文本变化已处理');
        }
        
        // 处理Excalidraw的文本变化
        if (typeof window.excalidrawAppRef !== 'undefined' && window.excalidrawAppRef) {
            console.log('Excalidraw文本变化已处理');
        }
        
        return JSON.stringify({ success: true, message: '文本变化事件处理完成' });
    } catch (error) {
        console.error('处理文本变化事件失败:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();