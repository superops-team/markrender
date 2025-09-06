try {
    console.log('检查编辑器就绪状态');
    // 检查Cherry编辑器
    if (window.editorState && window.editorState.editor && typeof window.editorState.editor.getValue === 'function') {
        console.log('Cherry编辑器已就绪');
        return true;
    } 
    // 检查Excalidraw
    else if (typeof window.excalidrawAppRef !== 'undefined' && window.excalidrawAppRef) {
        console.log('Excalidraw已就绪');
        return true;
    }
    // 其他情况
    else {
        console.log('未检测到已就绪的编辑器');
        return false;
    }
} catch (error) {
    console.error('检查编辑器就绪状态失败:', error);
    return false;
}