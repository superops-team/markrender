/**
 * MarkRender WebChannel 核心通信库（修复 handlePythonMessage 函数问题）
 * 关键：优先定义全局通信函数，确保后端可访问
 */

'use strict';

// 【核心修复1：优先定义全局通信函数，确保最早挂载到 window】
// 提前定义 handlePythonMessage，防止后端调用时函数不存在
if (typeof window.handlePythonMessage !== 'function') {
    window.handlePythonMessage = function(action, data, requestId) {
        // 初始为临时函数，后续再完善逻辑（避免后端早期调用时报错）
        console.warn('[WebChannel] handlePythonMessage 临时函数被调用（初始化中）:', action, requestId);
        // 若有早期消息，暂存到队列，后续处理
        if (!window.__pythonMessageQueue) {
            window.__pythonMessageQueue = [];
        }
        window.__pythonMessageQueue.push({ action, data, requestId });
    };
    console.log('[WebChannel] 全局 handlePythonMessage 临时函数已定义');
}

// 全局WebChannel管理器
window.WebChannelManager = (function() {
    
    // 核心状态管理（保留原有配置）
    const state = {
        backendInterface: null,
        isChannelReady: false,
        callbackMap: new Map(),
        requestCounter: 0,
        retryCount: 0,
        maxRetries: 5,
        pageType: 'unknown',
        initCallbacks: [],
        messageHandlers: new Map(),
        initLock: false,
        ignoreErrors: true
    };

    // 日志工具（保留原有）
    const logger = {
        info: (msg, ...args) => console.log(`[WebChannel-${state.pageType}] ${msg}`, ...args),
        warn: (msg, ...args) => console.warn(`[WebChannel-${state.pageType}] ${msg}`, ...args),
        error: (msg, ...args) => console.error(`[WebChannel-${state.pageType}] ${msg}`, ...args),
        debug: (msg, ...args) => console.debug(`[WebChannel-${state.pageType}] ${msg}`, ...args)
    };

    // 【核心修复2：完善 handlePythonMessage 逻辑，并处理早期暂存的消息】
    function initHandlePythonMessage() {
        // 覆盖临时函数，实现完整逻辑
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
        logger.info('全局 handlePythonMessage 函数已初始化完成');

        // 处理临时队列中暂存的早期消息
        if (window.__pythonMessageQueue && window.__pythonMessageQueue.length > 0) {
            logger.info(`处理早期暂存的消息（共 ${window.__pythonMessageQueue.length} 条）`);
            window.__pythonMessageQueue.forEach(msg => {
                window.handlePythonMessage(msg.action, msg.data, msg.requestId);
            });
            // 清空队列，避免重复处理
            delete window.__pythonMessageQueue;
        }
    }

    // 注册消息处理器（保留原有）
    function registerMessageHandler(action, handler) {
        state.messageHandlers.set(action, handler);
        logger.debug(`注册消息处理器: ${action}`);
    }
    
    // 预先注册兼容性消息处理器（保留原有）
    registerMessageHandler('registerEditorEvents', (data, requestId) => {
        logger.debug('忽略编辑器消息: registerEditorEvents');
    });
    
    registerMessageHandler('setupContentChangeListener', (data, requestId) => {
        logger.debug('忽略编辑器消息: setupContentChangeListener');
    });

    // QWebChannel handleResponse 异常捕获补丁（保留原有）
    function patchQWebChannelHandleResponse() {
        if (!window.QWebChannel) {
            logger.warn('QWebChannel 未加载，无法应用异常捕获补丁');
            return;
        }

        const originalHandleResponse = QWebChannel.prototype.handleResponse;
        QWebChannel.prototype.handleResponse = function(message) {
            try {
                originalHandleResponse.call(this, message);
            } catch (error) {
                reportError({
                    message: `QWebChannel handleResponse 错误: ${error.message}`,
                    stack: error.stack,
                    extra: {
                        messageId: message?.id || '无ID',
                        execCallbacksKeys: Object.keys(this.execCallbacks || {}),
                        execCallbacksCount: Object.keys(this.execCallbacks || {}).length
                    }
                }, 'qwebchannel-handleResponse');
            }
        };
        logger.debug('QWebChannel handleResponse 异常捕获补丁已应用');
    }

    // WebChannel初始化（保留原有逻辑，新增初始化handlePythonMessage）
    function initWebChannel(pageType = 'unknown', ignoreErrors = true) {
        // 确保state对象存在
        if (typeof state === 'undefined') {
            console.error('[WebChannel] state对象未定义');
            return Promise.resolve();
        }
        
        if (state.initLock) {
            logger.warn('WebChannel 初始化已在进行中，跳过重复调用');
            return Promise.resolve();
        }
        state.initLock = true;
        state.ignoreErrors = ignoreErrors;
        state.pageType = pageType;
        logger.info('开始初始化WebChannel...');

        // 【核心修复3：初始化消息处理函数（确保在后端发送消息前完成）】
        initHandlePythonMessage();

        // 验证QWebChannel内置脚本（保留原有）
        if (!window.QWebChannel) {
            logger.error('QWebChannel 内置脚本未加载（禁止手动引入第三方qwebchannel.js）');
            
            if (state.retryCount < state.maxRetries) {
                state.retryCount++;
                logger.info(`重试初始化 ${state.retryCount}/${state.maxRetries}（等待内置脚本加载）`);
                return new Promise(resolve => {
                    setTimeout(() => {
                        initWebChannel(pageType, ignoreErrors).then(resolve);
                        state.initLock = false;
                    }, 300 * state.retryCount);
                });
            } else {
                logger.error('WebChannel 初始化失败：内置脚本始终未加载');
                state.initLock = false;
                return Promise.resolve();
            }
        }

        // 检查传输层可用性（保留原有）
        if (!window.qt || !window.qt.webChannelTransport) {
            logger.error('QWebChannel传输不可用（qt.webChannelTransport不存在）');
            
            if (state.retryCount < state.maxRetries) {
                state.retryCount++;
                logger.info(`WebChannel初始化重试 ${state.retryCount}/${state.maxRetries}`);
                return new Promise(resolve => {
                    setTimeout(() => {
                        initWebChannel(pageType, ignoreErrors).then(resolve);
                        state.initLock = false;
                    }, 200 * state.retryCount);
                });
            } else {
                logger.error('WebChannel初始化最终失败：传输层不可用');
                state.initLock = false;
                return Promise.resolve();
            }
        }

        return new Promise((resolve) => {
            try {
                new QWebChannel(qt.webChannelTransport, (channel) => {
                    state.backendInterface = channel.objects.backendInterface;
                    
                    if (!state.backendInterface) {
                        logger.error('WebChannel初始化警告：backendInterface未找到（后端未注册？）');
                        state.isChannelReady = false;
                    } else {
                        state.isChannelReady = true;
                        logger.info('WebChannel初始化成功（backendInterface已就绪）');

                        // 通知后端前端就绪（失败不阻断）
                        try {
                            if (typeof state.backendInterface.frontend_ready === 'function') {
                                state.backendInterface.frontend_ready();
                            } else {
                                logger.warn('backendInterface.frontend_ready 不是函数（后端方法未定义？）');
                            }
                        } catch (e) {
                            logger.error('通知后端前端就绪失败:', e);
                        }

                        // 执行初始化回调（保留原有）
                        state.initCallbacks.forEach(callback => {
                            try {
                                callback();
                            } catch (error) {
                                logger.error('初始化回调执行失败:', error);
                            }
                        });
                    }

                    state.initLock = false;
                    resolve();
                });
            } catch (error) {
                logger.error('QWebChannel初始化异常:', error);
                
                if (state.retryCount < state.maxRetries) {
                    state.retryCount++;
                    setTimeout(() => {
                        initWebChannel(pageType, ignoreErrors).then(resolve);
                        state.initLock = false;
                    }, 300 * state.retryCount);
                } else {
                    logger.error('WebChannel初始化最终异常:', error);
                    state.initLock = false;
                    resolve();
                }
            }
        });
    }

    // 【核心修复4：添加函数存在性校验，防止后端调用时函数丢失】
    function checkHandlePythonMessage() {
        if (typeof window.handlePythonMessage !== 'function') {
            const errMsg = 'window.handlePythonMessage 不是函数！可能被其他脚本覆盖';
            logger.error(errMsg);
            // 紧急恢复函数定义
            window.handlePythonMessage = function(action, data, requestId) {
                logger.error('恢复的 handlePythonMessage 被调用:', action, requestId);
            };
            reportError(new Error(errMsg), 'function-check');
            return false;
        }
        return true;
    }

    // 发送消息到Python（新增函数存在性校验）
    function sendToPython(action, data = {}, callback = null) {
        // 校验 handlePythonMessage 存在性
        if (!checkHandlePythonMessage()) {
            const errMsg = 'handlePythonMessage 函数异常，无法发送消息';
            logger.error(errMsg);
            if (callback) {
                callback({ success: false, error: errMsg, requestId: `null_${Date.now()}` });
            }
            return Promise.resolve({ success: false, error: errMsg });
        }

        logger.debug('发送到Python:', action, data);

        if (!state.isChannelReady || !state.backendInterface) {
            const errMsg = '通信通道未就绪（isChannelReady=false 或 backendInterface不存在）';
            logger.error(errMsg);
            if (callback) {
                callback({ success: false, error: errMsg, requestId: `null_${Date.now()}` });
            }
            return Promise.resolve({ success: false, error: errMsg });
        }

        if (typeof state.backendInterface.dispatch_request !== 'function') {
            const errMsg = '后端接口方法不存在: dispatch_request（后端未正确注册该方法？）';
            logger.error(errMsg);
            if (callback) {
                callback({ success: false, error: errMsg, requestId: `null_${Date.now()}` });
            }
            return Promise.resolve({ success: false, error: errMsg });
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
                    logger.error(`请求 ${action} 失败:`, error);
                    const errResp = { success: false, error: error.message, requestId };
                    if (callback) {
                        state.callbackMap.delete(requestId);
                        callback(errResp);
                    }
                    return errResp;
                });
        } catch (e) {
            logger.error(`发送请求 ${action} 异常:`, e);
            const errResp = { success: false, error: e.message, requestId };
            if (callback) {
                callback(errResp);
            }
            return Promise.resolve(errResp);
        }
    }

    // 处理Python响应（保留原有）
    function handlePythonResponse(responseJson) {
        try {
            const response = typeof responseJson === 'string' ? 
                JSON.parse(responseJson) : responseJson;
            
            if (!response.requestId) {
                throw new Error(`响应缺少requestId（无效响应格式）: ${JSON.stringify(response)}`);
            }

            logger.debug('收到响应:', response);

            if (response.requestId && state.callbackMap.has(response.requestId)) {
                try {
                    state.callbackMap.get(response.requestId)(response);
                } catch (cbErr) {
                    logger.error(`响应回调执行失败（requestId: ${response.requestId}）:`, cbErr);
                }
                state.callbackMap.delete(response.requestId);
            } else if (response.requestId) {
                logger.warn(`未找到对应回调（requestId: ${response.requestId}，已超时或重复响应？）`);
            }

            return response;
        } catch (e) {
            logger.error('解析响应失败:', e);
            return { success: false, error: `解析响应失败: ${e.message}`, requestId: 'parse_error' };
        }
    }

    // 注销消息处理器（保留原有）
    function unregisterMessageHandler(action) {
        state.messageHandlers.delete(action);
        logger.debug(`注销消息处理器: ${action}`);
    }

    // 注册初始化完成回调（保留原有）
    function onReady(callback) {
        if (typeof callback !== 'function') {
            logger.warn('onReady 注册的不是函数，忽略');
            return;
        }
        if (state.isChannelReady) {
            try {
                callback();
            } catch (e) {
                logger.error('onReady 立即执行回调失败:', e);
            }
        } else {
            state.initCallbacks.push(callback);
        }
    }

    // 获取WebChannel状态（新增函数存在性检查）
    function getStatus() {
        return {
            isReady: state.isChannelReady,
            pageType: state.pageType,
            retryCount: state.retryCount,
            hasBackend: !!state.backendInterface,
            initLock: state.initLock,
            callbackCount: state.callbackMap.size,
            handlePythonMessageExists: typeof window.handlePythonMessage === 'function' // 新增函数状态
        };
    }

    // 发送响应到Python（保留原有）
    function sendResponseToPython(requestId, data) {
        if (!checkHandlePythonMessage()) {
            logger.error('handlePythonMessage 函数异常，无法发送响应');
            return;
        }

        if (!state.isChannelReady || !state.backendInterface) {
            logger.error('WebChannel未就绪，无法发送响应');
            return;
        }
        
        try {
            const responseData = {
                requestId: requestId,
                result: data
            };
            if (typeof state.backendInterface.handle_web_response === 'function') {
                state.backendInterface.handle_web_response(JSON.stringify(responseData));
            } else {
                logger.error('backendInterface.handle_web_response 不是函数（后端方法未定义？）');
            }
        } catch (error) {
            logger.error(`发送响应（requestId: ${requestId}）失败:`, error);
        }
    }

    // 错误报告优化（保留原有）
    function reportError(error, source = 'unknown') {
        try {
            let errorData = {};
            if (typeof error === 'object' && error !== null) {
                errorData = {
                    message: error.message || String(error),
                    source: source,
                    line: error.line || error.lineno || '-',
                    column: error.column || error.colno || '-',
                    stack: error.stack || '无堆栈信息',
                    errorType: error.name || 'UnknownError',
                    extra: error.extra || {},
                    pageType: state.pageType,
                    timestamp: new Date().toISOString()
                };
            } else {
                errorData = {
                    message: String(error),
                    source: source,
                    pageType: state.pageType,
                    timestamp: new Date().toISOString()
                };
            }

            const errorStr = JSON.stringify(errorData, null, 2);
            logger.error(`报告错误:\n${errorStr}`);

            if (state.isChannelReady) {
                sendToPython('reportError', errorData).catch(e => {
                    logger.error('错误报告发送失败:', e);
                });
            }
        } catch (e) {
            console.error('[WebChannel] 错误报告机制异常:', e);
        }
    }

    // 全局错误处理（保留原有）
    window.addEventListener('error', function(event) {
        reportError({
            message: event.message,
            source: event.filename,
            line: event.lineno,
            column: event.colno,
            stack: event.error?.stack || '',
            errorType: event.error?.name || 'GlobalError'
        }, 'global-error');
    });

    window.addEventListener('unhandledrejection', function(event) {
        reportError({
            message: event.reason?.message || String(event.reason),
            stack: event.reason?.stack || '',
            errorType: event.reason?.name || 'UnhandledRejection'
        }, 'promise-rejection');
        event.preventDefault();
    });

    // 页面卸载处理（保留原有）
    window.addEventListener('beforeunload', function() {
        logger.info('页面即将卸载，清理WebChannel资源');
        state.callbackMap.clear();
        state.messageHandlers.clear();
        state.initCallbacks.length = 0;
        state.backendInterface = null;
        state.isChannelReady = false;
    });

    // 初始化QWebChannel补丁（保留原有）
    patchQWebChannelHandleResponse();

    // 公开API（保留原有）
    return {
        init: initWebChannel,
        sendToPython: sendToPython,
        sendResponseToPython: sendResponseToPython,
        registerMessageHandler: registerMessageHandler,
        unregisterMessageHandler: unregisterMessageHandler,
        onReady: onReady,
        getStatus: getStatus,
        isReady: () => state.isChannelReady,
        reportError: reportError,
        logger: logger,
        // 新增：暴露函数检查方法，便于调试
        checkHandlePythonMessage: checkHandlePythonMessage
    };
})();

// 页面加载完成后的通用初始化（保留原有）
document.addEventListener('DOMContentLoaded', function() {
    // 禁用右键菜单
    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
        return false;
    });
    
    console.log('[WebChannel] 核心库加载完成，等待页面特定初始化...');
    
    // 显式初始化WebChannel
    if (window.WCM && typeof window.WCM.init === 'function') {
        // 根据页面类型确定pageType
        let pageType = 'unknown';
        if (window.location.pathname.includes('excalidraw')) {
            pageType = 'excalidraw';
        } else if (window.location.pathname.includes('cherry-markdown')) {
            pageType = 'markdown';
        } else if (window.location.pathname.includes('landing')) {
            pageType = 'landing';
        }
        
        window.WCM.init(pageType, true).then(() => {
            console.log('WebChannel初始化流程完成');
        }).catch((error) => {
            console.error('WebChannel初始化失败:', error);
        });
    } else {
        console.warn('[WebChannel] WCM或init函数未定义，跳过初始化');
    }
});

// 导出到全局作用域
window.WCM = window.WebChannelManager;