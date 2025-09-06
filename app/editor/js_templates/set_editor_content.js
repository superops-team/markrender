(function() {
    try {
        // 使用default过滤器为未定义的变量提供默认值
        const content = {{ content|default('')|tojson }};
        console.log('开始设置编辑器内容');
        // 处理Cherry编辑器
        if (window.editorState && window.editorState.editor && typeof window.editorState.editor.setValue === 'function') {
            window.editorState.editor.setValue(content);
            console.log('Cherry编辑器内容已设置');
            return JSON.stringify({ success: true });
        } 
        // 处理Excalidraw
        else if (typeof window.loadExcalidrawData === 'function') {
            window.loadExcalidrawData(content);
            console.log('Excalidraw内容已设置');
            return JSON.stringify({ success: true });
        }
        // 处理其他可能的编辑器
        else {
            console.warn('未找到支持的编辑器实例');
            return JSON.stringify({ success: false, error: '未找到支持的编辑器实例' });
        }
    } catch (error) {
        console.error('设置编辑器内容失败:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();