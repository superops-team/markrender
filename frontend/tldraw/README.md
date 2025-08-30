# TLDraw Board

基于tldraw的绘图板功能，专为PySide6应用设计。

## 功能特性

- 完整的绘图板功能（形状、文字、画笔等）
- 实时保存和加载
- WebChannel通信
- 固定文件名构建
- 响应式设计

## 安装和构建

```bash
# 安装依赖
npm install

# 开发模式
npm run dev

# 构建项目
npm run build

# 构建并部署到PySide应用
npm run build-and-deploy
```

## WebChannel API

### Python -> JavaScript

- `setBoardId`: 设置当前画板ID
- `loadTLDrawData`: 加载画板数据
- `clearBoard`: 清空画板

### JavaScript -> Python

- `save_tldraw_board`: 保存画板数据
- `load_tldraw_board`: 加载画板数据
- `export_tldraw_board`: 导出画板为图片