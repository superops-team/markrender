/**
 * Excalidraw编辑器消息处理器
 * 为Excalidraw页面提供特定的消息处理逻辑
 */

'use strict';

// 确保在DOM加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 等待WebChannelManager就绪
    function waitForWebChannelManager(callback, maxRetries = 50, interval = 100) {
        let retries = 0;
        const check = () => {
            if (window.WebChannelManager && window.WebChannelManager.isReady && window.WebChannelManager.isReady()) {
                callback();
            } else if (retries < maxRetries) {
                retries++;
                setTimeout(check, interval);
            } else {
                console.error('[ExcalidrawHandler] WebChannelManager未就绪，无法注册消息处理器');
            }
        };
        check();
    }

    // 注册Excalidraw特定的消息处理器
    function registerExcalidrawHandlers() {
        if (!window.WebChannelManager) {
            console.error('[ExcalidrawHandler] WebChannelManager未定义，无法注册消息处理器');
            return;
        }

        // setValue消息处理器 - 清空或设置Excalidraw场景
        window.WebChannelManager.registerMessageHandler('setValue', (data, requestId) => {
            try {
                window.WebChannelManager.logger.info('收到setValue请求:', data);
                
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
                        window.WebChannelManager.logger.warn('setValue内容不是有效的JSON格式:', data.content);
                    }
                    
                    // 更新场景
                    if (typeof window.updateScene === 'function') {
                        window.updateScene({ elements: elements });
                        window.WebChannelManager.logger.info('Excalidraw场景已更新');
                    } else {
                        window.WebChannelManager.logger.error('updateScene函数不可用');
                    }
                } else {
                    // 清空场景
                    if (typeof window.ExcalidrawLib !== 'undefined' && typeof window.ExcalidrawLib.clearScene === 'function') {
                        window.ExcalidrawLib.clearScene();
                        window.WebChannelManager.logger.info('Excalidraw场景已清空 (使用ExcalidrawLib.clearScene)');
                    } else if (typeof window.updateScene === 'function') {
                        window.updateScene({ elements: [] });
                        window.WebChannelManager.logger.info('Excalidraw场景已清空 (使用updateScene)');
                    } else {
                        window.WebChannelManager.logger.error('无法清空Excalidraw场景，缺少必要的函数');
                    }
                }
            } catch (error) {
                window.WebChannelManager.logger.error('处理setValue请求时出错:', error);
                if (window.WebChannelManager.reportError) {
                    window.WebChannelManager.reportError(error, 'setValue');
                }
            }
        });

        // getContent消息处理器 - 获取当前Excalidraw场景数据
        window.WebChannelManager.registerMessageHandler('getContent', (data, requestId) => {
            try {
                window.WebChannelManager.logger.info('收到getContent请求');
                
                // 获取当前场景元素
                if (typeof window.getSceneElements === 'function') {
                    const elements = window.getSceneElements();
                    const content = JSON.stringify(elements);
                    
                    // 发送响应
                    window.WebChannelManager.sendResponseToPython(requestId, {
                        content: content
                    });
                    window.WebChannelManager.logger.info('Excalidraw内容已发送');
                } else {
                    window.WebChannelManager.logger.error('getSceneElements函数不可用');
                    window.WebChannelManager.sendResponseToPython(requestId, {
                        error: '无法获取Excalidraw内容'
                    });
                }
            } catch (error) {
                window.WebChannelManager.logger.error('处理getContent请求时出错:', error);
                if (window.WebChannelManager.reportError) {
                    window.WebChannelManager.reportError(error, 'getContent');
                }
                window.WebChannelManager.sendResponseToPython(requestId, {
                    error: '获取内容时出错: ' + error.message
                });
            }
        });

        window.WebChannelManager.logger.info('Excalidraw消息处理器注册完成');
    }

    // 启动处理器注册
    waitForWebChannelManager(registerExcalidrawHandlers);
});