(function() {
    try {
        // 使用default过滤器为未定义的变量提供默认值
        const content = {{ content|default('{}')|tojson }};
        const itemId = {{ item_id|default('')|tojson }};
        console.log('开始设置Excalidraw编辑器内容和项目ID:', itemId);
        
        // 设置当前项目ID - 使用新的接口
        if (typeof window.setCurrentItemId === 'function') {
            window.setCurrentItemId(itemId);
            console.log('通过新接口设置Excalidraw当前项目ID:', itemId);
        } else if (typeof window.editorState !== 'undefined') {
            window.editorState.currentItemId = itemId;
            console.log('通过editorState设置Excalidraw当前项目ID:', itemId);
        }
        
        // 处理Excalidraw - 使用新的接口
        if (typeof window.setValue === 'function') {
            // 解析内容
            let parsedContent = null;
            try {
                parsedContent = JSON.parse(content);
                // 确保内容中包含itemId
                if (parsedContent && typeof parsedContent === 'object') {
                    parsedContent.itemId = itemId;
                }
                
                // 确保 collaborators 是数组格式（修复之前的错误）
                if (parsedContent.appState && parsedContent.appState.collaborators && typeof parsedContent.appState.collaborators === 'object' && !Array.isArray(parsedContent.appState.collaborators)) {
                    parsedContent.appState = {
                        ...parsedContent.appState,
                        collaborators: Object.values(parsedContent.appState.collaborators)
                    };
                }
            } catch (e) {
                console.warn('解析Excalidraw内容失败，使用空内容:', e);
                parsedContent = { elements: [], appState: {}, itemId: itemId };
            }
            
            try {
                window.setValue(parsedContent);
                console.log('通过新接口设置Excalidraw内容完成');
                return JSON.stringify({ success: true, item_id: itemId });
            } catch (e) {
                console.error("setValue error:", e);
                return JSON.stringify({ success: false, error: e.message });
            }
        }
        // 兼容旧的接口
        else if (typeof window.loadExcalidrawData === 'function') {
            window.loadExcalidrawData(content);
            console.log('通过旧接口设置Excalidraw内容完成');
            return JSON.stringify({ success: true, item_id: itemId });
        }
        // 处理其他可能的编辑器
        else {
            console.warn('未找到支持的Excalidraw编辑器实例');
            return JSON.stringify({ success: false, error: '未找到支持的Excalidraw编辑器实例' });
        }
    } catch (error) {
        console.error('设置Excalidraw编辑器内容失败:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();