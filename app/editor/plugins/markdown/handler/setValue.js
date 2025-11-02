(function() {
    try {
        // 使用default过滤器为未定义的变量提供默认值
        const content = {{ content|default('')|tojson }};
        const itemId = {{ item_id|default('')|tojson }};
        console.log('开始设置Markdown编辑器内容和项目ID:', itemId);
        
        // 设置当前项目ID
        if (window.editorState) {
            window.editorState.currentItemId = itemId;
            console.log('当前项目ID已设置:', itemId);
        }
        
        // 处理Cherry编辑器
        if (window.editorState && window.editorState.editor && typeof window.editorState.editor.setValue === 'function') {
            // 检查内容长度，避免过大的内容导致性能问题
            if (content && content.length > 5000000) {  // 5MB限制
                console.warn('内容过大，跳过设置以避免性能问题，长度:', content.length);
                return JSON.stringify({ success: false, error: '内容过大，跳过设置以避免性能问题' });
            }
            
            // 添加延迟设置，避免在编辑器初始化过程中出现问题
            setTimeout(() => {
                try {
                    // 先检查是否已经有相同内容，避免不必要的更新
                    const currentContent = window.editorState.editor.getValue() || '';
                    
                    // 对于大内容，只比较长度和前1000个字符
                    let shouldUpdate = false;
                    if (content && currentContent) {
                        if (content.length > 100000 || currentContent.length > 100000) {
                            // 大内容只比较长度和前1000个字符
                            shouldUpdate = (content.length !== currentContent.length) || 
                                         (content.substring(0, 1000) !== currentContent.substring(0, 1000));
                        } else {
                            // 小内容正常比较
                            shouldUpdate = content !== currentContent;
                        }
                    } else {
                        // 如果任一内容为空，则比较是否都为空
                        shouldUpdate = content !== currentContent;
                    }
                    
                    if (shouldUpdate) {
                        window.editorState.editor.setValue(content || '');
                        console.log('Cherry编辑器内容已设置，长度:', (content || '').length);
                    } else {
                        console.log('内容未变化，跳过设置');
                    }
                } catch (e) {
                    console.error('设置编辑器内容时出错:', e);
                }
            }, 10);
            return JSON.stringify({ success: true, item_id: itemId });
        } 
        // 处理其他可能的编辑器
        else {
            console.warn('未找到支持的Markdown编辑器实例');
            return JSON.stringify({ success: false, error: '未找到支持的Markdown编辑器实例' });
        }
    } catch (error) {
        console.error('设置Markdown编辑器内容失败:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();