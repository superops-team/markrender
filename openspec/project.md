# Project: MarkRender

## Purpose

MarkRender 是一个基于 PySide6 的桌面文档处理平台，集成 Markdown 编辑、Excalidraw 白板、树形文档管理、历史记录、导入导出与 SQLite 本地存储。

## Stack

- Python 3.11+
- PySide6 / QWebEngineView
- SQLAlchemy / SQLite
- 前端插件：Cherry Markdown、Excalidraw
- 本地数据目录：`~/.markdown_render/MarkRender`

## Conventions

- Python 后端负责文档 CRUD、历史记录、页面调度与 WebView 通信。
- Web 编辑器通过 `BackendInterface` 执行 JS handler 完成 `getContent` / `setValue` / `setCurrentItemId` 等动作。
- 文档树使用 `QuickPickPanel` 和 `MarkRenderManager` 读取 SQLite 数据。
- 前端状态命名遵循仓库 `AGENTS.md`：Markdown 使用 `window.editorState`，其他页面使用 `window.appState`。
- Python 与 JS 消息应使用 `item_id` / `itemId` 作为文档身份边界，禁止生成随机 request id。

## Constraints

- 不能因页面切换造成用户编辑内容丢失。
- 不能把“编辑器未 ready / JS 读取失败”误保存为空文档。
- 不能在 UI 主线程执行长时间 DB、磁盘、JS 同步等待。
- 需要兼容现有 SQLite 数据和用户本地 output 文件。

