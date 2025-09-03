# 前后端通信接口文档

## 概述
本文档详细描述了MarkRender应用中前端(JavaScript)与后端(Python)之间的通信接口规范，基于Qt的QWebChannel实现。

## 通信基础
- **通信协议**：QWebChannel
- **数据格式**：JSON
- **核心通道**：`window.bridge.channel` (前端) 与 `BackendInterface` (后端)
- **文档隔离**：所有通信均包含`item_id`参数以支持多文档并发编辑

## 后端接口 (Python)

### BackendInterface类
位于<mcfile name="channel.py" path="/Users/bytedance/workspace/github/markrender/app/editor/channel.py"></mcfile>中的核心通信管理类，实现为单例模式。

#### 主要方法
- **register_web_handler(event_name, handler)**
  注册前端事件处理器
  - 参数: `event_name` (str) - 事件名称, `handler` (callable) - 处理函数

- **send_message(action, data, callback=None)**
  发送请求到前端
  - 参数: `action` (str) - 前端方法名, `data` (dict) - 请求数据, `callback` (callable) - 响应回调

- **unregister_document(item_id)**
  解除文档与通信通道的关联
  - 参数: `item_id` (str) - 文档唯一标识

#### 内置事件处理器
- **contentChanged**：处理前端内容变更通知
- **requestSave**：处理前端保存请求
- **reportError**：处理前端错误报告

## 前端接口 (JavaScript)

### 初始化
```javascript
new QWebChannel(qt.webChannelTransport, function(channel) {
    window.bridge = {
        channel: channel.objects.document,
        currentItemId: null
    };
    // 注册事件监听器
    setupEventListeners();
});
```

#### 核心方法
- **setDocumentId(item_id)**
  设置当前活动文档ID
  - 参数: `item_id` (str) - 文档唯一标识

- **sendContentChanged(content)**
  发送内容变更事件到后端
  - 参数: `content` (str) - Markdown内容
  - 示例: `window.bridge.channel.contentChanged(window.bridge.currentItemId, content)`

- **requestSave()**
  请求后端保存文档
  - 示例: `window.bridge.channel.requestSave(window.bridge.currentItemId)`

- **reportError(message)**
  向后端报告错误
  - 参数: `message` (str) - 错误信息
  - 示例: `window.bridge.channel.reportError(message)`

## 数据模型

### RequestModel
请求数据验证模型:
```python
class RequestModel(BaseModel):
    item_id: str
    method: str
    params: dict = Field(default_factory=dict)
```

### 标准响应格式
```json
{
    "success": true,
    "data": {},
    "error": null
}
```

## 通信流程示例

### 1. 内容变更通知
```javascript
// 前端发送内容变更
editor.on('change', () => {
    const content = editor.getValue();
    window.bridge.channel.contentChanged(window.bridge.currentItemId, content);
});
```

```python
# 后端处理
@BackendInterface.register_web_handler('contentChanged')
def handle_content_changed(item_id, content):
    document = MarkdownDocument.get(item_id)
    document.set_content(content)
    return {'status': 'received'}
```

### 2. 保存文档
```javascript
// 前端请求保存
function saveDocument() {
    return new Promise((resolve) => {
        window.bridge.channel.requestSave(window.bridge.currentItemId, (response) => {
            resolve(response);
        });
    });
}
```

```python
# 后端处理保存
@BackendInterface.register_web_handler('requestSave')
def handle_request_save(item_id):
    document = MarkdownDocument.get(item_id)
    success = document.save()
    return {'success': success}
```

## 错误处理
- 后端通过`_send_web_error()`发送错误响应
- 前端通过`window.onerror`捕获并报告错误
- 标准错误格式:
```json
{
    "success": false,
    "data": null,
    "error": {
        "code": "ERROR_CODE",
        "message": "Human readable error message"
    }
}
```

## 多文档管理
- 所有通信必须包含`item_id`参数
- 切换文档时调用`setDocumentId()`更新上下文
- 关闭文档时后端调用`unregister_document()`清理资源

## 兼容性说明
- 支持Qt WebChannel协议版本1.0+
- 所有异步操作使用回调或Promise处理
- 大文件传输建议使用分片机制