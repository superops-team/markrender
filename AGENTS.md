# MarkRender开发原则与指南

## WebChannel通信原则

### 1. 直接QWebChannel优先
- **原则**: 优先使用直接QWebChannel实现，避免中间层
- **理由**: 减少依赖，提高稳定性，便于调试
- **实现**: 每个页面独立实现QWebChannel初始化

### 2. 状态管理规范
- **全局状态命名**: 使用`window.[page]State`格式
  - Markdown: `window.editorState`
  - Landing: `window.appState`
  - Excalidraw: `window.appState`
- **状态验证**: 每次使用前验证状态存在性
- **错误处理**: 所有状态访问都应有错误处理

### 3. 消息格式统一
- **Request格式**:
  ```json
  {
    "requestId": "item_id",
    "action": "action_name",
    "data": {...}
  }
  ```
- **Response格式**:
  ```json
  {
    "requestId": "item_id",
    "result": {...}
  }
  ```
- **原则**: 严格使用item_id作为request_id，不生成随机ID

### 4. 错误处理策略
- **防御式编程**: 所有接口调用都应有try-catch
- **优雅降级**: 提供后备方案
- **用户提示**: 重要错误应有用户可见提示

## 前端开发指南

### JavaScript最佳实践

#### 1. 初始化流程
```javascript
// 标准初始化模板
function initWebChannel() {
    if (typeof QWebChannel === 'undefined') {
        console.error('QWebChannel未定义');
        return false;
    }
    
    new QWebChannel(window.qt.webChannelTransport, function(channel) {
        const backend = channel.objects.backendInterface;
        if (backend && typeof backend.handle_web_response === 'function') {
            // 初始化成功
            window.appState.backend = backend;
            // 延迟通知确保就绪
            setTimeout(() => {
                if (backend.frontend_ready) {
                    backend.frontend_ready();
                }
            }, 50);
        }
    });
}
```

#### 2. 消息处理
```javascript
// 标准消息处理函数
function handleBackendMessage(action, data, requestId) {
    try {
        switch(action) {
            case 'action_name':
                // 处理逻辑
                if (window.appState.backend) {
                    window.appState.backend.handle_web_response(JSON.stringify({
                        requestId: requestId,
                        result: { success: true }
                    }));
                }
                break;
        }
    } catch (error) {
        console.error('处理消息失败:', error);
    }
}
```

#### 3. 状态验证
```javascript
// 状态验证模板
function validateState() {
    return window.appState && 
           window.appState.backend && 
           typeof window.appState.backend.handle_web_response === 'function';
}
```

#### 4. 禁用Promise处理webchannel消息

- **原则**: 不使用Promise处理webchannel消息
- **理由**: 避免阻塞UI线程，影响响应性能
- **实现**: 直接使用回调函数处理消息

### 5. 接口命名统一

- **参数命名**: 统一使用 `item_id` 作为标识符
- **方法命名**: 统一使用 `setCurrentItemId` 代替 `setBoardId`
- **状态管理**: 统一使用 `itemId` 代替 `boardId`
- **消息格式**: 统一使用 `item_id` 作为参数名

#### 统一接口示例
```javascript
// 标准消息格式
{
  requestId: "item-id-123",  // 使用item_id作为request_id
  action: "setCurrentItemId",
  data: { item_id: "item-id-123" }
}

// 标准状态管理
window.appState = {
  itemId: "item-id-123",  // 统一使用itemId
  backend: backendInterface
};
```

### React集成指南

#### 1. WebChannel类设计
- **单一职责**: 每个类只负责通信
- **状态隔离**: 不直接操作React状态
- **错误边界**: 提供错误处理机制
- **不用Promise**: 直接使用回调函数处理消息

#### 2. 组件集成
```javascript
// React组件集成示例
useEffect(() => {
    const initChannel = async () => {
        const success = await window.excalidrawChannel.init();
        if (success) {
            setIsReady(true);
        }
    };
    initChannel();
}, []);
```

#### 3. 全局API暴露
```javascript
// 标准API暴露
window.loadExcalidrawData = (content) => {
    // 实现逻辑
};

window.getExcalidrawData = () => {
    // 实现逻辑
    return JSON.stringify(elements);
};
```

## Python后端指南

### 1. 接口定义
```python
from PySide6.QtCore import QObject, Slot

class BackendInterface(QObject):
    @Slot(str)
    def handle_web_response(self, response_json):
        """处理前端响应"""
        pass
    
    @Slot()
    def frontend_ready(self):
        """前端就绪回调"""
        pass
```

### 2. 错误处理
- **异常捕获**: 所有槽函数都应有异常处理
- **日志记录**: 详细记录通信日志
- **超时处理**: 实现请求超时机制

### 3. 状态管理
- **线程安全**: 确保Qt线程安全
- **资源清理**: 正确清理WebChannel资源
- **内存管理**: 避免内存泄漏

## 测试策略

### 1. 单元测试
- **通信测试**: 测试基本消息发送接收
- **边界测试**: 测试空数据、大数据
- **错误测试**: 测试各种错误情况

### 2. 集成测试
- **端到端测试**: 完整流程测试
- **跨平台测试**: 不同操作系统测试
- **性能测试**: 大量数据测试

### 3. 调试工具
- **日志系统**: 详细的通信日志
- **调试页面**: 提供调试接口
- **监控工具**: 实时监控通信状态

## 部署检查清单

### 1. 文件验证
- [ ] 所有index.html已移除webchannel-core.js引用
- [ ] QWebChannel.js正确加载
- [ ] 资源路径正确

### 2. 功能验证
- [ ] 基本通信正常
- [ ] 数据同步正确
- [ ] 错误处理有效

### 3. 性能验证
- [ ] 初始化时间<2秒
- [ ] 消息延迟<100ms
- [ ] 内存使用正常

## 故障排查指南

### 常见问题

#### QWebChannel未定义
```bash
# 检查文件路径
ls -la app/editor/plugins/*/index.html | grep qwebchannel
```

#### 后端接口未找到
```bash
# 检查Python端注册
python -c "from app.editor.backend_interface import BackendInterface; print('OK')"
```

#### 通信失败
1. 检查浏览器控制台
2. 验证Qt WebChannel设置
3. 确认Slot装饰器使用正确

### 调试步骤
1. **检查加载顺序**: 确保QWebChannel.js最先加载
2. **验证接口**: 确认backendInterface正确注册
3. **测试消息**: 使用简单消息测试通信
4. **检查错误**: 查看浏览器和Python日志

## 版本兼容性

### 支持的Qt版本
- Qt 6.2+
- PySide6 6.2+

### 浏览器兼容性
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## 性能优化建议

### 1. 初始化优化
- 延迟加载非关键资源
- 并行初始化多个组件
- 缓存静态资源

### 2. 通信优化
- 批量处理消息
- 压缩传输数据
- 实现心跳机制

### 3. 内存优化
- 及时清理引用
- 避免内存泄漏
- 监控内存使用

## 安全考虑

### 1. 输入验证
- 验证所有输入数据
- 防止XSS攻击
- 限制数据大小

### 2. 权限控制
- 最小权限原则
- 验证用户身份
- 记录操作日志

## 文档维护

### 1. 更新频率
- 代码变更时同步更新
- 重大重构时全面更新
- 定期审查准确性

### 2. 文档结构
- 保持一致的格式
- 提供代码示例
- 包含故障排除

### 3. 版本控制
- 记录变更历史
- 标记兼容性
- 提供迁移指南