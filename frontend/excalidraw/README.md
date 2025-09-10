# Excalidraw 项目说明

这个项目是 MarkRender 应用中的 Excalidraw 插件，用于在应用中集成 Excalidraw 绘图功能。

## 项目结构

- `src/main.js`: Excalidraw 的初始化和功能实现
- `index.html`: 主页面文件
- `vite.config.js`: Vite 构建配置
- `scripts/deploy.js`: 部署脚本

## 功能说明

在 `src/main.js` 中，我们在 `window` 对象上提供了以下三个方法：

1. `getContent()`: 获取 Excalidraw 当前的内容
2. `setValue(content)`: 设置 Excalidraw 画布的内容
3. `reset()`: 重置 Excalidraw 画布

## 构建和部署

### 开发模式
```bash
npm run dev
```

### 构建项目
```bash
npm run build
```

### 部署项目
```bash
npm run deploy
```

部署脚本会自动构建项目并将生成的文件复制到 `app/editor/plugins/excalidraw` 目录中，这是 MarkRender 应用加载插件的位置。

## 配置说明

- `EXCALIDRAW_ASSETS_PATH`: 在 `vite.config.js` 中定义，用于设置 Excalidraw 资源的路径
- 资源文件会被打包到 `assets` 目录中
- 所有路径都使用相对路径，以确保在 MarkRender 应用中正确加载