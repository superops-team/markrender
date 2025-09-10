(function() {
    try {
        console.log('开始重置Excalidraw页面状态');
        
        // 重置Excalidraw状态 - 使用新的接口
        if (typeof window.reset === 'function') {
            window.reset();
            console.log('通过新接口重置Excalidraw状态完成');
        }
        // 兼容旧的接口
        else if (typeof window.resetExcalidraw === 'function') {
            window.resetExcalidraw();
            console.log('通过旧接口重置Excalidraw状态完成');
        }
        
        // 重置项目ID - 使用新的接口
        if (typeof window.setCurrentItemId === 'function') {
            window.setCurrentItemId(null);
            console.log('通过新接口重置当前项目ID');
        } else if (typeof window.editorState !== 'undefined') {
            window.editorState.currentItemId = null;
            console.log('通过editorState重置当前项目ID');
        }
        
        // 重置其他可能的状态
        if (typeof window.currentItemId !== 'undefined') {
            window.currentItemId = null;
            console.log('重置window.currentItemId');
        }
        
        // 重置Excalidraw特定状态
        try {
            // 清空Excalidraw场景 - 使用新的接口
            if (typeof window.updateScene === 'function') {
                window.updateScene({ elements: [] });
            } else if (window.excalidrawAppRef && typeof window.excalidrawAppRef.updateScene === 'function') {
                window.excalidrawAppRef.updateScene({ elements: [] });
            }
            
            // 清空localStorage中的Excalidraw数据
            if (typeof localStorage !== 'undefined') {
                for (let key in localStorage) {
                    if (key.startsWith('excalidraw-') || key.includes('excalidraw')) {
                        localStorage.removeItem(key);
                    }
                }
            }
            
            console.log('Excalidraw特定状态已重置');
        } catch (e) {
            console.warn('重置Excalidraw特定状态时出错:', e);
        }
        
        console.log('Excalidraw页面状态重置完成');
        return JSON.stringify({ success: true, message: 'Excalidraw页面状态重置完成' });
    } catch (error) {
        console.error('重置Excalidraw页面状态失败:', error);
        return JSON.stringify({ success: false, error: error.message });
    }
})();