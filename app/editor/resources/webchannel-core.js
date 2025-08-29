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
        maxRetries: 5,
        pageType: 'unknown',
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

    // 立即定义全局消息处理函数，防止早期调用失败
    window.handlePythonMessage = function(action, data, requestId) {
        logger.debug('收到Python消息:', action, data, 'requestId:', requestId);
        
        // 查找注册的消息处理器
        if (state.messageHandlers.has(action)) {
            try {
                state.messageHandlers.get(action)(data, requestId);
            } catch (error) {
                logger.error(`处理消息 ${action} 时出错:`, error);
            }
        } else {
            logger.warn(`未注册的消息类型: ${action}`);
        }
    };

    // WebChannel初始化（带重试机制）
    function initWebChannel(pageType = 'unknown') {
        state.pageType = pageType;
        logger.info('开始初始化WebChannel...');

        if (!window.qt || !window.qt.webChannelTransport) {
            logger.error('QWebChannel传输不可用，尝试重试...');
            
            if (state.retryCount < state.maxRetries) {
                state.retryCount++;
                logger.info(`WebChannel初始化重试 ${state.retryCount}/${state.maxRetries}`);
                setTimeout(() => initWebChannel(pageType), 200 * state.retryCount);
            } else {
                logger.error('WebChannel初始化最终失败');
            }
            return Promise.reject(new Error('WebChannel传输不可用'));
        }

        return new Promise((resolve, reject) => {
            try {
                new QWebChannel(qt.webChannelTransport, (channel) => {
                    state.backendInterface = channel.objects.backendInterface;
                    state.isChannelReady = true;
                    logger.info('WebChannel初始化成功');

                    // 通知后端前端就绪
                    if (state.backendInterface && state.backendInterface.frontend_ready) {
                        state.backendInterface.frontend_ready();
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
                });
            } catch (error) {
                logger.error('QWebChannel初始化异常:', error);
                
                if (state.retryCount < state.maxRetries) {
                    state.retryCount++;
                    setTimeout(() => {
                        initWebChannel(pageType).then(resolve).catch(reject);
                    }, 300 * state.retryCount);
                } else {
                    reject(error);
                }
            }
        });
    }

    // 标准化消息发送到Python
    function sendToPython(action, data = {}, callback = null) {
        logger.debug('发送到Python:', action, data);

        if (!state.isChannelReady || !state.backendInterface) {
            logger.error('通信通道未就绪');
            return Promise.reject(new Error('通信通道未就绪'));
        }

        if (typeof state.backendInterface.dispatch_request !== 'function') {
            logger.error('后端接口方法不存在: dispatch_request');
            return Promise.reject(new Error('后端接口方法不存在'));
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
                .then(responseJson => handlePythonResponse(responseJson))
                .catch(error => {
                    logger.error('请求失败:', error);
                    if (callback) {
                        state.callbackMap.delete(requestId);
                        callback({ success: false, error: error.message });
                    }
                    throw error;
                });
        } catch (e) {
            logger.error('发送请求失败:', e);
            if (callback) {
                callback({ success: false, error: e.message });
            }
            return Promise.reject(e);
        }
    }

    // 处理Python响应
    function handlePythonResponse(responseJson) {
        try {
            const response = typeof responseJson === 'string' ? 
                JSON.parse(responseJson) : responseJson;
            logger.debug('收到响应:', response);

            if (response.requestId && state.callbackMap.has(response.requestId)) {
                state.callbackMap.get(response.requestId)(response);
                state.callbackMap.delete(response.requestId);
            }

            return response;
        } catch (e) {
            logger.error('解析响应失败:', e);
            throw e;
        }
    }

    // 注册消息处理器
    function registerMessageHandler(action, handler) {
        state.messageHandlers.set(action, handler);
        logger.debug(`注册消息处理器: ${action}`);
    }

    // 注销消息处理器
    function unregisterMessageHandler(action) {
        state.messageHandlers.delete(action);
        logger.debug(`注销消息处理器: ${action}`);
    }

    // 注册初始化完成回调
    function onReady(callback) {
        if (state.isChannelReady) {
            callback();
        } else {
            state.initCallbacks.push(callback);
        }
    }

    // 获取WebChannel状态
    function getStatus() {
        return {
            isReady: state.isChannelReady,
            pageType: state.pageType,
            retryCount: state.retryCount,
            hasBackend: !!state.backendInterface
        };
    }

    // 发送响应到Python（兼容老接口）
    function sendResponseToPython(requestId, data) {
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
    }

    // 错误报告
    function reportError(error, source = 'unknown') {
        const errorData = {
            message: error.message || String(error),
            source: source,
            stack: error.stack || '',
            pageType: state.pageType,
            timestamp: new Date().toISOString()
        };

        logger.error('报告错误:', errorData);

        if (state.isChannelReady) {
            sendToPython('reportError', errorData).catch(e => {
                logger.error('错误报告失败:', e);
            });
        }
    }

    // 全局错误处理
    window.addEventListener('error', function(event) {
        reportError({
            message: event.message,
            source: event.filename,
            line: event.lineno,
            column: event.colno,
            stack: event.error?.stack || ''
        }, 'global');
    });

    window.addEventListener('unhandledrejection', function(event) {
        reportError({
            message: event.reason?.message || String(event.reason),
            stack: event.reason?.stack || ''
        }, 'promise');
    });

    // 页面卸载处理
    window.addEventListener('beforeunload', function() {
        logger.info('页面即将卸载，清理WebChannel资源');
        state.callbackMap.clear();
        state.messageHandlers.clear();
        state.initCallbacks.length = 0;
    });

    // 公开API
    return {
        // 核心功能
        init: initWebChannel,
        sendToPython: sendToPython,
        sendResponseToPython: sendResponseToPython,
        
        // 消息处理
        registerMessageHandler: registerMessageHandler,
        unregisterMessageHandler: unregisterMessageHandler,
        
        // 状态管理
        onReady: onReady,
        getStatus: getStatus,
        isReady: () => state.isChannelReady,
        
        // 错误处理
        reportError: reportError,
        
        // 工具方法
        logger: logger
    };
})();

// 页面加载完成后的通用初始化
document.addEventListener('DOMContentLoaded', function() {
    // 禁用右键菜单（通用需求）
    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
        return false;
    });
    
    console.log('[WebChannel] 核心库加载完成，等待页面特定初始化...');
});

// 导出到全局作用域供其他脚本使用
window.WCM = window.WebChannelManager;