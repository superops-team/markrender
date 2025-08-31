# Excalidraw 部署与集成指南

## 概述

本文档详细说明了如何在MarkRender项目中构建、部署和测试Excalidraw组件，解决了在浏览器中直接打开dist文件出现白屏的问题。

## 项目结构

```
markrender/
├── app/editor/plugins/excalidraw/     # Qt WebEngine插件目录
├── frontend/excalidraw/               # Excalidraw前端源码
│   ├── src/                          # React源码
│   ├── dist/                         # 构建输出目录
│   ├── browser/                      # 浏览器兼容版本
│   └── scripts/
│       ├── deploy.js                 # 基础部署脚本
│       └── build-and-deploy.js       # 增强版构建部署脚本
├── scripts/
│   └── build-and-deploy-excalidraw.js # 项目级构建部署脚本
├── test/
│   └── test_excalidraw_integration.py # 集成测试脚本
└── docs/
    └── excalidraw-deployment-guide.md # 本文档
```

## 构建与部署流程

### 1. 基础构建

```bash
# 进入Excalidraw前端目录
cd frontend/excalidraw

# 构建React应用
npm run build
```

### 2. 自动化部署

项目提供了两种部署方式：

#### 方式一：基础部署（原有功能）
```bash
# 构建并部署
npm run build-and-deploy
```

#### 方式二：增强部署（解决浏览器兼容性问题）
```bash
# 使用增强版构建部署脚本
npm run build-and-deploy-enhanced
```

### 3. 项目级自动化部署
```bash
# 使用项目级构建部署脚本
node scripts/build-and-deploy-excalidraw.js
```

## 解决的浏览器白屏问题

### 问题原因

1. **Qt特有协议**：原始HTML文件引用了`qrc:/qtwebchannel/qwebchannel.js`，在普通浏览器中无法解析
2. **WebChannel缺失**：浏览器环境中没有QWebChannel对象，导致JavaScript初始化失败
3. **相对路径问题**：file://协议下的相对路径解析与HTTP协议不同
4. **CORS限制**：浏览器安全策略限制本地文件访问

### 解决方案

增强版部署脚本会自动完成以下任务：

1. **生成浏览器兼容版本**：
   - 移除Qt特有的`qrc:/`协议引用
   - 生成独立的浏览器版本目录`frontend/excalidraw/browser/`

2. **添加WebChannel模拟**：
   - 为浏览器环境提供QWebChannel模拟实现
   - 确保JavaScript可以正常初始化和运行

3. **优化资源引用**：
   - 自动更新HTML模板中的JS/CSS文件引用
   - 确保webchannel-core.js正确引用

## 浏览器版本使用方法

### 1. 启动HTTP服务器

```bash
# 进入浏览器版本目录
cd frontend/excalidraw/browser

# 启动Python HTTP服务器
python -m http.server 8000

# 或使用Node.js服务器
npx serve .
```

### 2. 访问页面

在浏览器中访问：http://localhost:8000

## 测试验证

### 运行集成测试

```bash
python test/test_excalidraw_integration.py
```

测试脚本会验证：
- Qt WebEngine版本页面加载
- 浏览器兼容版本页面加载
- WebChannel通信功能
- 页面内容渲染状态

### 手动测试

1. **Qt版本测试**：
   - 运行MarkRender应用
   - 创建新的Board项目
   - 验证Excalidraw白板是否正常显示

2. **浏览器版本测试**：
   - 启动HTTP服务器
   - 在浏览器中访问
   - 验证页面是否正常显示且无错误

## 关键技术细节

### WebChannel模拟实现

浏览器版本的HTML文件包含了以下WebChannel模拟代码：

```javascript
// 模拟QWebChannel对象
if (typeof QWebChannel === 'undefined') {
  window.QWebChannel = function(transport, callback) {
    // 模拟后端接口
    const mockBackend = {
      backendInterface: {
        dispatch_request: function(request) {
          // 模拟请求处理
        },
        frontend_ready: function() {
          // 模拟前端就绪
        }
      }
    };
    
    // 模拟异步初始化
    setTimeout(() => {
      callback(mockBackend);
    }, 100);
  };
}
```

### 资源路径优化

部署脚本会自动更新HTML模板中的资源引用：

```html
<!-- 更新前 -->
<script type="module" crossorigin src="./assets/index.js"></script>

<!-- 更新后 -->
<script type="module" crossorigin src="./assets/index-CCgCxBZc.js"></script>
```

## 常见问题与解决方案

### 1. 页面仍然白屏

**可能原因**：
- webchannel-core.js未正确引用
- JS/CSS资源文件缺失
- WebChannel初始化时序问题

**解决方案**：
- 检查HTML文件中的资源引用
- 确保所有必要文件都已复制到目标目录
- 验证WebChannel模拟实现

### 2. JavaScript错误

**可能原因**：
- QWebChannel对象未正确模拟
- React组件初始化失败

**解决方案**：
- 检查浏览器控制台错误信息
- 验证WebChannel模拟实现
- 确保React组件正确加载

### 3. 资源加载失败

**可能原因**：
- 相对路径解析错误
- CORS限制

**解决方案**：
- 使用HTTP服务器而非直接打开文件
- 检查资源文件路径
- 验证文件权限

## 最佳实践

### 1. 开发流程

1. 修改Excalidraw React源码
2. 运行`npm run build-and-deploy-enhanced`构建部署
3. 测试Qt WebEngine版本
4. 测试浏览器版本
5. 运行集成测试验证

### 2. 调试技巧

1. **使用浏览器开发者工具**：
   - 检查控制台错误
   - 查看网络请求状态
   - 调试JavaScript代码

2. **查看日志信息**：
   - 关注WebChannel初始化日志
   - 检查资源加载状态
   - 验证通信消息

3. **对比版本差异**：
   - 对比Qt版本和浏览器版本的HTML文件
   - 检查资源文件完整性
   - 验证功能一致性

## 维护与更新

### 1. 更新Excalidraw版本

```bash
# 进入Excalidraw目录
cd frontend/excalidraw

# 更新依赖
npm update @excalidraw/excalidraw

# 重新构建部署
npm run build-and-deploy-enhanced
```

### 2. 修改构建脚本

如需修改构建部署逻辑，请更新以下文件：
- `frontend/excalidraw/scripts/build-and-deploy.js`
- `scripts/build-and-deploy-excalidraw.js`

### 3. 扩展测试用例

在`test/test_excalidraw_integration.py`中添加新的测试用例，验证特定功能。

## 总结

通过增强版构建部署脚本，我们成功解决了Excalidraw在浏览器中白屏的问题，实现了以下目标：

1. ✅ Qt WebEngine版本正常工作
2. ✅ 浏览器版本可直接访问
3. ✅ 自动化部署流程
4. ✅ 完整的测试验证机制
5. ✅ 详细的文档说明

这为MarkRender项目的Excalidraw集成提供了完整的解决方案，确保了在不同环境下的兼容性和稳定性。