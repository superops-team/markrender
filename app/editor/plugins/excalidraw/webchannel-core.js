/**
 * MarkRender WebChannel 核心通信库
 * 提供标准化的WebChannel通信协议和重试机制
 * 必须作为第一个JS文件加载，确保通信时序正确
 */

'use strict';

// 全局WebChannel管理器
window.WebChannelManager = (function() {
    
    // 核心状态管理
    const state = {
        backendInterface: null,
        isChannelReady: false,
        callbackMap: new Map(),
        requestCounter: 0,
        retryCount: 0,
        maxRetries: 10,
        pageType: 'excalidraw',
        initCallbacks: [],
        messageHandlers: new Map()
    };

    // 日志工具
    const logger = {
        info: (msg, ...args) => console.log(`[WebChannel-${state.pageType}] ${msg}`, ...args),
        warn: (msg, ...args) => console.warn(`[WebChannel-${state.pageType}] ${msg}`, ...args),
        error: (msg, ...args) => console.error(`[WebChannel-${state.pageType}] ${msg}`, ...args),
        debug: (msg, ...args) => console.debug(`[WebChannel-${state.pageType}] ${msg}`, ...args)
    };

    // 注册消息处理器
    function registerMessageHandler(action, handler) {
        try {
            state.messageHandlers.set(action, handler);
            logger.debug(`注册消息处理器: ${action}`);
        } catch (error) {
            logger.error(`注册消息处理器失败: ${action}`, error);
            // 不抛出异常，确保不影响主流程
        }
    }

    // 立即定义全局消息处理函数，防止早期调用失败
    window.handleBackendMessage = function(action, data, requestId) {
        try {
            logger.debug('收到Python消息:', action, data, 'requestId:', requestId);
            
            // 查找注册的消息处理器
            if (state.messageHandlers.has(action)) {
                try {
                    state.messageHandlers.get(action)(data, requestId);
                } catch (error) {
                    logger.error(`处理消息 ${action} 时出错:`, error);
                    // 不抛出异常，确保不影响主流程
                }
            } else {
                logger.warn(`未注册的消息类型: ${action}`);
            }
        } catch (error) {
            logger.error('处理Python消息时发生异常:', error);
            // 不抛出异常，确保不影响主流程
        }
    };

    // WebChannel初始化（带重试机制）
    function initWebChannel(pageType = 'excalidraw') {
        try {
            state.pageType = pageType;
            logger.info('开始初始化excalidraw WebChannel...');

            if (!window.qt || !window.qt.webChannelTransport) {
                logger.error('QWebChannel传输不可用，尝试重试...');
                
                if (state.retryCount < state.maxRetries) {
                    state.retryCount++;
                    logger.info(`WebChannel初始化重试 ${state.retryCount}/${state.maxRetries}`);
                    setTimeout(() => {
                        initWebChannel(pageType).catch(err => {
                            logger.error('WebChannel初始化重试失败:', err);
                        });
                    }, 200 * state.retryCount);
                } else {
                    logger.error('WebChannel初始化最终失败');
                }
                // 不返回Promise.reject，确保不影响主流程
                return Promise.resolve();
            }

            return new Promise((resolve) => {
                try {
                    new QWebChannel(qt.webChannelTransport, (channel) => {
                        try {
                            state.backendInterface = channel.objects.backendInterface;
                            state.isChannelReady = true;
                            logger.info('WebChannel初始化成功');

                            // 通知后端前端就绪
                            if (state.backendInterface && state.backendInterface.frontend_ready) {
                                try {
                                    state.backendInterface.frontend_ready();
                                } catch (error) {
                                    logger.error('通知前端就绪失败:', error);
                                }
                            }

                            // 执行初始化回调
                            state.initCallbacks.forEach(callback => {
                                try {
                                    callback();
                                } catch (error) {
                                    logger.error('初始化回调执行失败:', error);
                                }
                            });

                            resolve();
                        } catch (error) {
                            logger.error('QWebChannel回调处理异常:', error);
                            resolve(); // 不reject，确保不影响主流程
                        }
                    });
                } catch (error) {
                    logger.error('QWebChannel初始化异常:', error);
                    
                    if (state.retryCount < state.maxRetries) {
                        state.retryCount++;
                        setTimeout(() => {
                            initWebChannel(pageType).then(resolve).catch(() => resolve());
                        }, 300 * state.retryCount);
                    } else {
                        resolve(); // 不reject，确保不影响主流程
                    }
                }
            });
        } catch (error) {
            logger.error('WebChannel初始化过程异常:', error);
            // 不抛出异常，确保不影响主流程
            return Promise.resolve();
        }
    }

    // 标准化消息发送到Python
    function sendToBackend(action, data = {}, callback = null) {
        try {
            logger.debug('发送到Python:', action, data);

            if (!state.isChannelReady || !state.backendInterface) {
                logger.error('通信通道未就绪');
                // 不抛出异常，确保不影响主流程
                return Promise.resolve({ success: false, error: '通信通道未就绪' });
            }

            if (typeof state.backendInterface.dispatch_request !== 'function') {
                logger.error('后端接口方法不存在: dispatch_request');
                // 不抛出异常，确保不影响主流程
                return Promise.resolve({ success: false, error: '后端接口方法不存在' });
            }

            const requestId = `${state.pageType}_req_${Date.now()}_${state.requestCounter++}`;
            if (callback) state.callbackMap.set(requestId, callback);

            const request = {
                requestId: requestId,
                action: action,
                data: data,
                pageType: state.pageType
            };

            try {
                return state.backendInterface.dispatch_request(JSON.stringify(request))
                    .then(responseJson => {
                        try {
                            return handleBackendResponse(responseJson);
                        } catch (error) {
                            logger.error('处理Python响应失败:', error);
                            return { success: false, error: '处理响应失败' };
                        }
                    })
                    .catch(error => {
                        logger.error('请求失败:', error);
                        if (callback) {
                            state.callbackMap.delete(requestId);
                            try {
                                callback({ success: false, error: error.message });
                            } catch (cbError) {
                                logger.error('回调执行失败:', cbError);
                            }
                        }
                        // 不抛出异常，确保不影响主流程
                        return { success: false, error: error.message };
                    });
            } catch (e) {
                logger.error('发送请求失败:', e);
                if (callback) {
                    try {
                        callback({ success: false, error: e.message });
                    } catch (cbError) {
                        logger.error('回调执行失败:', cbError);
                    }
                }
                // 不抛出异常，确保不影响主流程
                return Promise.resolve({ success: false, error: e.message });
            }
        } catch (error) {
            logger.error('sendToBackend执行异常:', error);
            // 不抛出异常，确保不影响主流程
            return Promise.resolve({ success: false, error: '执行异常' });
        }
    }

    // 处理Python响应
    function handleBackendResponse(responseJson) {
        try {
            const response = typeof responseJson === 'string' ? 
                JSON.parse(responseJson) : responseJson;
            logger.debug('收到响应:', response);

            if (response.requestId && state.callbackMap.has(response.requestId)) {
                try {
                    state.callbackMap.get(response.requestId)(response);
                } catch (error) {
                    logger.error('回调执行失败:', error);
                }
                state.callbackMap.delete(response.requestId);
            }

            return response;
        } catch (e) {
            logger.error('解析响应失败:', e);
            // 不抛出异常，确保不影响主流程
            return { success: false, error: '解析响应失败' };
        }
    }

    // 注销消息处理器
    function unregisterMessageHandler(action) {
        try {
            state.messageHandlers.delete(action);
            logger.debug(`注销消息处理器: ${action}`);
        } catch (error) {
            logger.error(`注销消息处理器失败: ${action}`, error);
            // 不抛出异常，确保不影响主流程
        }
    }

    // 注册初始化完成回调
    function onReady(callback) {
        try {
            if (state.isChannelReady) {
                callback();
            } else {
                state.initCallbacks.push(callback);
            }
        } catch (error) {
            logger.error('注册初始化回调失败:', error);
            // 不抛出异常，确保不影响主流程
        }
    }

    // 获取WebChannel状态
    function getStatus() {
        try {
            return {
                isReady: state.isChannelReady,
                pageType: state.pageType,
                retryCount: state.retryCount,
                hasBackend: !!state.backendInterface
            };
        } catch (error) {
            logger.error('获取状态失败:', error);
            // 返回默认状态，确保不影响主流程
            return {
                isReady: false,
                pageType: 'unknown',
                retryCount: 0,
                hasBackend: false
            };
        }
    }

    // 发送响应到Python（兼容老接口）
    function sendResponseToBackend(requestId, data) {
        try {
            if (!state.isChannelReady || !state.backendInterface) {
                logger.error('WebChannel未就绪，无法发送响应');
                return;
            }
            
            try {
                const responseData = {
                    requestId: requestId,
                    result: data
                };
                state.backendInterface.handle_web_response(JSON.stringify(responseData));
            } catch (error) {
                logger.error('发送响应失败:', error);
            }
        } catch (error) {
            logger.error('sendResponseToBackend执行异常:', error);
            // 不抛出异常，确保不影响主流程
        }
    }

    // 错误报告
    function reportError(error, source = 'unknown') {
        try {
            const errorData = {
                message: error.message || String(error),
                source: source,
                stack: error.stack || '',
                pageType: state.pageType,
                timestamp: new Date().toISOString()
            };

            logger.error('报告错误:', errorData);

            if (state.isChannelReady) {
                sendToBackend('reportError', errorData).catch(e => {
                    logger.error('错误报告失败:', e);
                });
            }
        } catch (reportError) {
            logger.error('错误报告过程异常:', reportError);
            // 不抛出异常，确保不影响主流程
        }
    }

    // 全局错误处理
    window.addEventListener('error', function(event) {
        try {
            reportError({
                message: event.message,
                source: event.filename,
                line: event.lineno,
                column: event.colno,
                stack: event.error?.stack || ''
            }, 'global');
        } catch (error) {
            logger.error('全局错误处理异常:', error);
        }
    });

    window.addEventListener('unhandledrejection', function(event) {
        try {
            reportError({
                message: event.reason?.message || String(event.reason),
                stack: event.reason?.stack || ''
            }, 'promise');
        } catch (error) {
            logger.error('未处理Promise拒绝异常:', error);
        }
    });

    // 页面卸载处理
    window.addEventListener('beforeunload', function() {
        try {
            logger.info('页面即将卸载，清理WebChannel资源');
            state.callbackMap.clear();
            state.messageHandlers.clear();
            state.initCallbacks.length = 0;
        } catch (error) {
            logger.error('页面卸载处理异常:', error);
        }
    });

    // 公开API
    return {
        // 核心功能
        init: initWebChannel,
        sendToBackend: sendToBackend,
        sendResponseToBackend: sendResponseToBackend,
        
        // 消息处理
        registerMessageHandler: registerMessageHandler,
        unregisterMessageHandler: unregisterMessageHandler,
        
        // 状态管理
        onReady: onReady,
        getStatus: getStatus,
        isReady: () => {
            try {
                return state.isChannelReady;
            } catch (error) {
                logger.error('检查就绪状态异常:', error);
                return false;
            }
        },
        
        // 错误处理
        reportError: reportError,
        
        // 工具方法
        logger: logger
    };
})();

// 页面加载完成后的通用初始化
document.addEventListener('DOMContentLoaded', function() {
    try {
        // 禁用右键菜单（通用需求）
        document.addEventListener('contextmenu', function(e) {
            e.preventDefault();
            return false;
        });
        
        console.log('[WebChannel] 核心库加载完成，等待页面特定初始化...');
    } catch (error) {
        console.error('[WebChannel] 页面初始化异常:', error);
    }
});

// 导出到全局作用域供其他脚本使用
window.WCM = window.WebChannelManager;