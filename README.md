# MarkRender

<p align="center">
  <a href="#features">功能特点</a> •
  <a href="#tech-stack">技术栈</a> •
  <a href="#quick-start">快速开始</a> •
  <a href="#usage">使用指南</a> •
  <a href="#contributing">贡献指南</a>
</p>

## 🌐 Language / 语言
- [中文](#zh-cn)
- [English](#en-us)

---

## <a name="zh-cn"></a>📝 中文介绍

### 🚀 项目简介

MarkRender 是一个功能强大的多格式文档处理平台，集文件转换、Markdown编辑、图形绘制和文档管理于一体。它完美支持 Tencent Cherry Markdown 富文本编辑和 Excalidraw 白板绘制，并提供树形文档结构和完整的文件编辑历史管理功能。

### ✨ 功能特点

- 📄 **多格式转换**: 支持 PDF、DOCX、EPUB、XLSX 等格式转换为 Markdown
- 📝 **专业Markdown编辑**: 完美集成 [Tencent Cherry Markdown](https://github.com/Tencent/cherry-markdown)，提供丰富的富文本编辑功能
- 🎨 **图形绘制**: 内置 [Excalidraw v0.17.6](https://github.com/excalidraw/excalidraw/tree/v0.17.6) 白板功能，支持手绘风格的图表和示意图创作
- 📁 **树形文档结构**: 直观的文档组织系统，支持层级分类和快速导航
- 📜 **完整编辑历史**: 自动记录文件的每一次编辑历史，支持版本回溯和对比
- 📤 **多格式导出**: 支持 Markdown、PDF、EPUB 等格式导出
- 🎨 **现代UI**: 基于PySide6的原生桌面应用，提供流畅的用户体验
- 🔍 **智能搜索**: 强大的文档检索功能，支持自定义排序（按创建时间、更新时间或名称）
- ⚙️ **个性化设置**: 丰富的主题和偏好配置选项

### 🛠️ 技术栈

- **前端**: PySide6 + Web组件
  - [Tencent Cherry Markdown](https://github.com/Tencent/cherry-markdown): 提供富文本编辑、实时预览和扩展语法支持
  - [Excalidraw v0.17.6](https://github.com/excalidraw/excalidraw/tree/v0.17.6): 手绘风格白板绘图组件
- **后端**: Python 3.11+ + SQLAlchemy
- **数据库**: SQLite (用于存储文档内容、元数据和编辑历史)
- **构建**: PyInstaller + Makefile
- **样式**: 统一的设计令牌系统 (TDesign风格)

### 🎯 核心功能特性

#### Cherry Markdown 集成
MarkRender 深度集成了 Tencent Cherry Markdown，提供：
- 丰富的 Markdown 扩展语法支持
- 实时预览与编辑
- 自定义工具栏和快捷键
- 表格、代码块、数学公式等高级编辑功能
- 多主题切换支持

#### Excalidraw 白板功能
基于 Excalidraw v0.17.6 版本，提供：
- 简洁直观的手绘风格绘图体验
- 丰富的形状库和模板
- 实时协作编辑基础架构
- 导入/导出 SVG、PNG 等格式
- 暗色模式支持

#### 树形文档管理
- 层级化的文档组织系统
- 拖拽式文档管理
- 标签和分类支持
- 智能排序和过滤
- 快速导航和跳转

#### 文件编辑历史
- 自动记录每次编辑的完整历史
- 版本对比和差异显示
- 一键回溯到任意历史版本
- 编辑时间和操作记录
- 历史版本管理和清理

### 🚀 快速开始

#### 环境要求
- Python 3.11+
- PySide6
- Node.js（用于前端构建）

#### 安装依赖
```bash
# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装Python依赖
pip install -r requirements.txt
```

#### 运行应用
```bash
# 开发模式
python main.py --debug

# 正常模式  
python main.py
```

#### 构建发布版本
```bash
make dmg
```

### 📁 项目结构

```
markrender/
├── app/                    # 主应用模块
│   ├── editor/            # Markdown编辑器组件
│   ├── preference/        # 应用偏好设置与样式系统
│   ├── quickpick/         # 快速选择面板
│   ├── sidebar/           # 侧边栏管理
│   ├── statusbar/         # 状态栏
│   └── topbar/            # 顶部工具栏
├── db/                     # 数据库模块
│   ├── models/            # 数据模型定义
│   └── managers/          # 数据管理器
├── frontend/               # 前端组件
│   ├── excalidraw/        # 白板功能(React+TS)
│   └── milkdown/          # Markdown编辑器(Vue+TS)
├── utils/                  # 工具类模块
├── docs/                   # 📚 项目文档
├── test/                   # 🧪 测试文件
├── icons/                  # 图标资源
└── main.py                # 应用入口
```

### 🛠️ 前端组件构建

#### Milkdown编辑器
Milkdown编辑器是MarkRender的默认Markdown编辑器，基于Vue和TypeScript构建。

需要二次开发的可以参考下面方式，如果不需要二次开发，可以跳过本部分，因为已经打包为插件集成到软件里了；

```bash
# 进入milkdown目录
cd frontend/milkdown

# 安装依赖
npm install

# 开发模式
npm run start

# 构建并部署
npm run build-and-deploy
```

#### Excalidraw白板
Excalidraw白板组件用于图形绘制功能。

需要二次开发的可以参考下面方式，如果不需要二次开发，可以跳过本部分，因为已经打包为插件集成到软件里了；

```bash
# 进入excalidraw目录
cd frontend/excalidraw

# 安装依赖
npm install

# 开发模式
npm run start

# 构建并部署
npm run build-and-deploy
```

### 📚 文档

所有项目文档都位于 [`docs/`](docs/) 目录中：

- **[文档索引](docs/INDEX.md)** - 完整的文档导航
- **[项目README](docs/README.md)** - 项目详细说明
- **[样式重构报告](docs/STYLE_REFACTOR_REPORT.md)** - 样式系统重构文档
- **[Qt兼容性修复](docs/QT_STYLE_COMPATIBILITY_FIX.md)** - Qt样式表兼容性修复报告
- **UI优化系列文档** - Sidebar对齐、边框优化等技术文档

### 🧪 测试

所有测试文件都位于 [`test/`](test/) 目录中：

- **[测试说明](test/README.md)** - 测试文件使用指南
- **功能测试** - UI组件和交互功能测试
- **测量工具** - 精确的像素级测量和验证工具
- **集成测试** - 综合功能验证

运行测试：
```bash
# 运行特定测试
python test/test_sidebar_alignment.py

# 运行测量工具
python test/measure_sidebar_spacing.py
```

### 📖 开发指南

#### 代码规范
- 遵循PEP 8 Python代码规范
- 使用统一的设计令牌系统 (见 `app/preference/style_constants.py`)
- 组件样式通过样式生成器复用 (见 `app/preference/style_utils.py`)

#### 贡献指南
1. Fork 项目
2. 创建功能分支
3. 编写测试用例
4. 提交变更
5. 发起 Pull Request

### 📄 许可证

本项目采用 [LICENSE](LICENSE) 许可证。

### 🤝 支持

如有问题或建议，请查看 [文档](docs/) 或提交 Issue。

---

## <a name="en-us"></a>📝 English Introduction

### 🚀 Project Overview

MarkRender is a powerful multi-format document processing platform that integrates file conversion, Markdown editing, graphic drawing, and document management. It perfectly supports Tencent Cherry Markdown rich text editing and Excalidraw whiteboard drawing, and provides tree-structured document organization and comprehensive file editing history management.

### ✨ Features

- 📄 **Multi-format Conversion**: Support PDF, DOCX, EPUB, XLSX conversion to Markdown
- 📝 **Professional Markdown Editing**: Perfect integration with [Tencent Cherry Markdown](https://github.com/Tencent/cherry-markdown), providing rich rich text editing capabilities
- 🎨 **Graphic Drawing**: Built-in [Excalidraw v0.17.6](https://github.com/excalidraw/excalidraw/tree/v0.17.6) whiteboard function, supporting hand-drawn style charts and diagrams
- 📁 **Tree-structured Document Organization**: Intuitive document organization system with hierarchical classification and quick navigation
- 📜 **Complete Editing History**: Automatically records every edit history, supporting version rollback and comparison
- 📤 **Multi-format Export**: Support exporting to Markdown, PDF, EPUB, and other formats
- 🎨 **Modern UI**: Native desktop application based on PySide6, providing smooth user experience
- 🔍 **Intelligent Search**: Powerful document retrieval function with custom sorting (by creation time, update time, or name)
- ⚙️ **Personalized Settings**: Rich theme and preference configuration options

### 🛠️ Tech Stack

- **Frontend**: PySide6 + Web Components
  - [Tencent Cherry Markdown](https://github.com/Tencent/cherry-markdown): Provides rich text editing, real-time preview, and extended syntax support
  - [Excalidraw v0.17.6](https://github.com/excalidraw/excalidraw/tree/v0.17.6): Hand-drawn style whiteboard drawing component
- **Backend**: Python 3.11+ + SQLAlchemy
- **Database**: SQLite (for storing document content, metadata, and editing history)
- **Build**: PyInstaller + Makefile
- **Style**: Unified design token system (TDesign style)

### 🎯 Core Functionality

#### Cherry Markdown Integration
MarkRender deeply integrates Tencent Cherry Markdown, providing:
- Rich Markdown extended syntax support
- Real-time preview and editing
- Customizable toolbar and shortcuts
- Advanced editing features (tables, code blocks, mathematical formulas)
- Multi-theme switching support

#### Excalidraw Whiteboard Function
Based on Excalidraw v0.17.6 version, providing:
- Clean and intuitive hand-drawn style drawing experience
- Rich shape library and templates
- Real-time collaboration editing infrastructure
- Import/export SVG, PNG, and other formats
- Dark mode support

#### Tree-structured Document Management
- Hierarchical document organization system
- Drag-and-drop document management
- Tag and classification support
- Intelligent sorting and filtering
- Quick navigation and jumping

#### File Editing History
- Automatically records complete history of each edit
- Version comparison and difference display
- One-click rollback to any historical version
- Editing time and operation records
- Historical version management and cleanup

### 🚀 Quick Start

#### Environment Requirements
- Python 3.11+
- PySide6
- Node.js (for frontend building)

#### Install Dependencies
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

#### Run Application
```bash
# Development mode
python main.py --debug

# Normal mode  
python main.py
```

#### Build Release Version
```bash
make dmg
```

### 📁 Project Structure

```
markrender/
├── app/                    # Main application module
│   ├── editor/            # Markdown editor component
│   ├── preference/        # Application preferences and style system
│   ├── quickpick/         # Quick selection panel
│   ├── sidebar/           # Sidebar management
│   ├── statusbar/         # Status bar
│   └── topbar/            # Top toolbar
├── db/                     # Database module
│   ├── models/            # Data model definitions
│   └── managers/          # Data managers
├── frontend/               # Frontend components
│   ├── excalidraw/        # Whiteboard function (React+TS)
│   └── milkdown/          # Markdown editor (Vue+TS)
├── utils/                  # Utility modules
├── docs/                   # 📚 Project documentation
├── test/                   # 🧪 Test files
├── icons/                  # Icon resources
└── main.py                # Application entry point
```

### 🛠️ Frontend Component Building

#### Milkdown Editor
Milkdown editor is MarkRender's default Markdown editor, built based on Vue and TypeScript.

For secondary development, you can refer to the following methods. If you don't need secondary development, you can skip this section as it has been packaged as a plugin and integrated into the software.

```bash
# Enter milkdown directory
cd frontend/milkdown

# Install dependencies
npm install

# Development mode
npm run start

# Build and deploy
npm run build-and-deploy
```

#### Excalidraw Whiteboard
Excalidraw whiteboard component is used for graphic drawing functionality.

For secondary development, you can refer to the following methods. If you don't need secondary development, you can skip this section as it has been packaged as a plugin and integrated into the software.

```bash
# Enter excalidraw directory
cd frontend/excalidraw

# Install dependencies
npm install

# Development mode
npm run start

# Build and deploy
npm run build-and-deploy
```

### 📚 Documentation

All project documentation is located in the [`docs/`](docs/) directory:

- **[Documentation Index](docs/INDEX.md)** - Complete documentation navigation
- **[Project README](docs/README.md)** - Detailed project description
- **[Style Refactoring Report](docs/STYLE_REFACTOR_REPORT.md)** - Style system refactoring documentation
- **[Qt Compatibility Fixes](docs/QT_STYLE_COMPATIBILITY_FIX.md)** - Qt stylesheet compatibility fix report
- **UI Optimization Series Documents** - Technical documents for sidebar alignment, border optimization, etc.

### 🧪 Testing

All test files are located in the [`test/`](test/) directory:

- **[Test Instructions](test/README.md)** - Test file usage guide
- **Functional Tests** - UI component and interaction function tests
- **Measurement Tools** - Precise pixel-level measurement and verification tools
- **Integration Tests** - Comprehensive function verification

Run tests:
```bash
# Run specific test
python test/test_sidebar_alignment.py

# Run measurement tool
python test/measure_sidebar_spacing.py
```

### 📖 Development Guide

#### Code Standards
- Follow PEP 8 Python code standards
- Use unified design token system (see `app/preference/style_constants.py`)
- Component styles are reused through style generators (see `app/preference/style_utils.py`)

#### Contribution Guide
1. Fork the project
2. Create a feature branch
3. Write test cases
4. Commit changes
5. Submit a Pull Request

### 📄 License

This project is licensed under the [LICENSE](LICENSE) license.

### 🤝 Support

If you have any questions or suggestions, please check the [documentation](docs/) or submit an Issue.

---

> 💡 **Tip**: It is recommended to first read [docs/INDEX.md](docs/INDEX.md) to understand the complete document structure, and [test/README.md](test/README.md) to understand the testing system.