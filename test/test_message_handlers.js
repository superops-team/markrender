/**
 * 测试消息处理器注册
 */
 
// 模拟WebChannelManager对象
const testWebChannelManager = {
    messageHandlers: new Map(),
    
    registerMessageHandler(action, handler) {
        this.messageHandlers.set(action, handler);
        console.log(`注册消息处理器: ${action}`);
    },
    
    handleBackendMessage(action, data, requestId) {
        console.log(`收到Python消息: ${action}`, data, requestId);
        
        if (this.messageHandlers.has(action)) {
            try {
                this.messageHandlers.get(action)(data, requestId);
                console.log(`成功处理消息: ${action}`);
            } catch (error) {
                console.error(`处理消息 ${action} 时出错:`, error);
            }
        } else {
            console.warn(`未注册的消息类型: ${action}`);
        }
    }
};

// 预注册常用消息处理器
const commonHandlers = [
    'textChanged',
    'setCurrentItemId', 
    'setValue',
    'getContent',
    'registerEditorEvents',
    'setupContentChangeListener'
];

commonHandlers.forEach(handler => {
    testWebChannelManager.registerMessageHandler(handler, (data, requestId) => {
        console.log(`处理消息: ${handler}`, data, requestId);
    });
});

// 测试消息处理
console.log("开始测试消息处理器...");

const testMessages = [
    { action: 'textChanged', data: { content: '测试内容' } },
    { action: 'setCurrentItemId', data: { item_id: 'test123' } },
    { action: 'setValue', data: { content: '# 标题\n内容' } },
    { action: 'getContent', data: {} },
    { action: 'unknownMessage', data: {} }  // 测试未注册的消息
];

testMessages.forEach(msg => {
    testWebChannelManager.handleBackendMessage(msg.action, msg.data, 'test_request_id');
});

console.log("测试完成");