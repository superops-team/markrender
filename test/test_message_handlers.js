/**
 * 测试消息处理器注册
 */
 
// 移除模拟WebChannelManager对象，改为直接使用全局handleBackendMessage函数

// 预注册常用消息处理器到全局handleBackendMessage函数
window.handleBackendMessage = function(action, data, requestId) {
    console.log(`收到Python消息: ${action}`, data, requestId);
    
    // 处理各种消息类型
    switch(action) {
        case 'textChanged':
            console.log(`处理消息: textChanged`, data, requestId);
            return { success: true };
            
        case 'setCurrentItemId':
            console.log(`处理消息: setCurrentItemId`, data, requestId);
            return { success: true };
            
        case 'setValue':
            console.log(`处理消息: setValue`, data, requestId);
            return { success: true };
            
        case 'getContent':
            console.log(`处理消息: getContent`, data, requestId);
            return { content: '# 测试内容' };
            
        case 'registerEditorEvents':
            console.log(`处理消息: registerEditorEvents`, data, requestId);
            return { success: true };
            
        case 'setupContentChangeListener':
            console.log(`处理消息: setupContentChangeListener`, data, requestId);
            return { success: true };
            
        default:
            console.warn(`未注册的消息类型: ${action}`);
            return { error: `未注册的消息类型: ${action}` };
    }
};

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
    const result = window.handleBackendMessage(msg.action, msg.data, 'test_request_id');
    console.log(`消息 ${msg.action} 处理结果:`, result);
});

console.log("测试完成");