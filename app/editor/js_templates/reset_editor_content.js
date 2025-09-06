(function() {
    try {
        console.log('开始重置编辑器');
        let resetCount = 0;
        // 重置Cherry编辑器
        if (window.editorState && window.editorState.editor && typeof window.editorState.editor.setValue === 'function') {
            window.editorState.editor.setValue('');
            console.log('Cherry编辑器内容已重置');
            resetCount++;
        } 
        // 重置Excalidraw
        else if (typeof window.loadExcalidrawData === 'function') {
            window.loadExcalidrawData('[]');
            console.log('Excalidraw内容已重置');
            resetCount++;
        }
        // 清理本地存储（在data: URL中可能不可用）
        try {
            if (typeof localStorage !== 'undefined') {
                localStorage.clear();
                console.log('本地存储已清理');
            }
        } catch (e) {
            console.warn('无法访问localStorage:', e.message);
        }
        console.log('编辑器重置完成，重置了', resetCount, '个组件');
        return JSON.stringify({ success: true, resetCount: resetCount });
    } catch (error) {
        console.error('重置编辑器失败:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();