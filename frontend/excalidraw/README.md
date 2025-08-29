# Excalidraw 构建与部署指南

本文档介绍如何快速构建和部署 Excalidraw 前端组件到 MarkRender 应用。

## 🚀 快速部署

### 一键构建并部署

```bash
cd frontend/excalidraw
npm run build-and-deploy
```

这个命令会：
1. 编译 TypeScript 代码
2. 构建生产版本的 Excalidraw 组件
3. 自动复制构建产物到 `app/editor/resources/excalidraw/`
4. 自动更新 `board_excalidraw.html` 中的文件引用

### 分步操作

如果需要分步执行：

```bash
# 1. 仅构建
npm run build

# 2. 仅部署（复制文件并更新HTML）
npm run deploy
```

## 📁 文件结构

```
frontend/excalidraw/
├── src/                           # 源代码
│   ├── components/
│   │   └── ExcalidrawBoard.tsx   # 主要组件（已修复React无限循环）
│   ├── service/
│   │   └── webchannel.ts         # WebChannel通信库（TypeScript版）
│   └── main.tsx                  # 入口文件（含错误边界）
├── scripts/
│   └── deploy.js                 # 自动化部署脚本
├── dist/                         # 构建输出目录
└── package.json                  # 项目配置
```

## 🔧 自动化部署特性

### 智能文件识别
- 自动识别最新构建的主要 JS 文件（> 1MB）
- 自动识别最新的 CSS 文件
- 按文件修改时间排序选择

### HTML 模板自动更新
部署脚本会自动更新 `board_excalidraw.html` 中的：
- `<script>` 标签的 `src` 属性
- `<link>` 标签的 `href` 属性

### 构建产物复制
- 完整复制 `dist/` 目录到资源目录
- 保持目录结构不变
- 覆盖旧文件

## ✅ 问题修复状态

### 已解决的问题
- ✅ **React error #185**: 重写了 ExcalidrawBoard 组件，修复无限循环问题
- ✅ **构建部署自动化**: 提供 `npm run build-and-deploy` 命令
- ✅ **HTML 自动更新**: 自动更新文件引用，无需手动编辑
- ✅ **WebChannel 集成**: 完整的 TypeScript WebChannel 通信库
- ✅ **错误边界**: 添加 React 错误边界组件，提供错误恢复

### 部分解决的问题
- ⚠️ **Landing 页面错误**: `handlePythonMessage` 初始化时序问题（不影响核心功能）
- ⚠️ **消息类型警告**: 一些未注册的消息类型警告（兼容性警告）

## 🎯 核心技术改进

### React 组件状态管理
- 移除了 `React.StrictMode`，避免双重渲染
- 正确使用 `onChange` 回调，避免渲染过程中的状态更新
- 使用 `useCallback` 和防抖机制优化性能
- 通过 `initialData` 属性传递数据，而不是直接控制状态

### WebChannel 通信优化
- 完整的 TypeScript 类型定义
- 专用的 Excalidraw 接口实现
- 增强的错误处理和离线模式支持
- 自动重试机制和详细日志

### 构建优化
- 使用 Vite 的现代构建系统
- 支持开发模式构建（便于调试）
- 自动化的文件复制和模板更新

## 🔍 验证步骤

部署完成后，验证是否成功：

1. 检查构建输出：
   ```bash
   ls -la app/editor/resources/excalidraw/assets/index-*.js
   ```

2. 检查 HTML 文件更新：
   ```bash
   grep "index-.*\.js" app/editor/resources/board_excalidraw.html
   ```

3. 运行应用程序：
   ```bash
   source .venv/bin/activate
   python main.py --debug
   ```

4. 验证关键指标：
   - ✅ 无 React error #185 错误
   - ✅ Excalidraw 页面正常加载
   - ✅ 白板功能正常工作

## 📝 开发注意事项

### 修改前端代码后
每次修改 `frontend/excalidraw/src/` 中的代码后，都需要运行：
```bash
npm run build-and-deploy
```

### 调试模式
如果需要调试前端错误，可以：
1. 修改 `vite.config.ts` 中的 `minify: false`
2. 重新构建部署
3. 在浏览器开发者工具中查看详细错误

### 性能优化
当前构建产物较大，未来可以考虑：
- 动态导入代码分割
- 使用 `build.rollupOptions.output.manualChunks`
- 调整块大小限制

## 🚀 使用示例

```bash
# 完整的开发流程
cd frontend/excalidraw

# 1. 修改代码...
# 2. 一键构建并部署
npm run build-and-deploy

# 3. 启动应用测试
cd ../../
source .venv/bin/activate
python main.py --debug
```

## 📞 问题反馈

如遇到问题，请检查：
1. Node.js 版本是否 >= 16
2. npm 依赖是否正确安装
3. 构建过程是否有错误
4. 文件权限是否正确

---

*最后更新: 2025-08-29*
*版本: v1.0.0*