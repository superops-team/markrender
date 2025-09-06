/**
 * Excalidraw编辑器消息处理器
 * 为Excalidraw页面提供特定的消息处理逻辑
 */

'use strict';

// 确保在DOM加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 移除waitForWebChannelManager函数，不再需要等待WebChannelManager就绪
    
    // 注册Excalidraw特定的消息处理器
    function registerExcalidrawHandlers() {
        // 移除对WebChannelManager的检查，直接注册处理器
        
        // setValue消息处理器 - 清空或设置Excalidraw场景
        // 修改为使用全局handleBackendMessage函数
        window.handleBackendMessage = function(action, data, requestId) {
            try {
                if (action === 'setValue') {
                    console.log('收到setValue请求:', data);
                    
                    // 如果有内容数据，则尝试加载
                    if (data.content) {
                        // 尝试解析内容为JSON（Excalidraw数据通常是JSON格式）
                        let elements = [];
                        try {
                            const parsed = JSON.parse(data.content);
                            if (Array.isArray(parsed)) {
                                elements = parsed;
                            } else if (parsed.elements && Array.isArray(parsed.elements)) {
                                elements = parsed.elements;
                            }
                        } catch (e) {
                            // 如果不是有效的JSON，忽略内容
                            console.warn('setValue内容不是有效的JSON格式:', data.content);
                        }
                        
                        // 更新场景
                        if (typeof window.updateScene === 'function') {
                            window.updateScene({ elements: elements });
                            console.log('Excalidraw场景已更新');
                        } else {
                            console.error('updateScene函数不可用');
                        }
                    } else {
                        // 清空场景
                        if (typeof window.ExcalidrawLib !== 'undefined' && typeof window.ExcalidrawLib.clearScene === 'function') {
                            window.ExcalidrawLib.clearScene();
                            console.log('Excalidraw场景已清空 (使用ExcalidrawLib.clearScene)');
                        } else if (typeof window.updateScene === 'function') {
                            window.updateScene({ elements: [] });
                            console.log('Excalidraw场景已清空 (使用updateScene)');
                        } else {
                            console.error('无法清空Excalidraw场景，缺少必要的函数');
                        }
                    }
                } else if (action === 'getContent') {
                    console.log('收到getContent请求');
                    
                    // 获取当前场景元素
                    if (typeof window.getSceneElements === 'function') {
                        const elements = window.getSceneElements();
                        const content = JSON.stringify(elements);
                        return { content: content };
                    } else {
                        console.error('getSceneElements函数不可用');
                        return { error: '无法获取Excalidraw内容' };
                    }
                }
            } catch (error) {
                console.error('处理消息时出错:', error);
                return { error: '处理消息时出错: ' + error.message };
            }
        };

        console.log('Excalidraw消息处理器注册完成');
    }

    // 直接注册处理器
    registerExcalidrawHandlers();
});