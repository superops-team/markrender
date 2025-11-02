(function() {
    try {
        console.log('开始重置页面状态');
        
        // 重置Markdown编辑器状态
        if (window.editorState) {
            window.editorState.currentItemId = null;
            console.log('Markdown编辑器状态已重置');
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
        
        // 重置Excalidraw特定状态
        try {
            // 清空Excalidraw场景
            if (typeof window.updateScene === 'function') {
                window.updateScene({ elements: [] });
            } else if (window.excalidrawAppRef && typeof window.excalidrawAppRef.updateScene === 'function') {
                window.excalidrawAppRef.updateScene({ elements: [] });
            }
            
            // 安全地清空localStorage中的Excalidraw数据
            if (typeof localStorage !== 'undefined') {
                // 创建要删除的键的副本，避免在迭代时修改对象
                const keysToRemove = [];
                for (let i = 0; i < localStorage.length; i++) {
                    const key = localStorage.key(i);
                    if (key && (key.startsWith('excalidraw-') || key.includes('excalidraw'))) {
                        keysToRemove.push(key);
                    }
                }
                
                // 删除收集到的键
                keysToRemove.forEach(key => {
                    localStorage.removeItem(key);
                });
            }
            
            console.log('Excalidraw特定状态已重置');
        } catch (e) {
            console.warn('重置Excalidraw特定状态时出错:', e);
        }
        
        console.log('页面状态重置完成');
        return JSON.stringify({ success: true, message: '页面状态重置完成' });
    } catch (error) {
        console.error('重置页面状态失败:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();