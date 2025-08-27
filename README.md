# MarkRender

MarkRender 是一个强大的文件转换工具，旨在将多种格式的文件（如 PDF、DOCX、EPUB、XLSX）转换为 Markdown，并支持导出为 Markdown、PDF、EPUB 等可读格式。

## 🚀 快速开始

### 环境要求
- Python 3.11+
- PySide6
- Node.js（用于前端构建）

### 安装依赖
```bash
# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 安装Python依赖
pip install -r requirements.txt
```

### 运行应用
```bash
# 开发模式
python main.py --debug

# 正常模式  
python main.py
```

### 构建发布版本
```bash
make dmg
```

## 📁 项目结构

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

## 📚 文档

所有项目文档都位于 [`docs/`](docs/) 目录中：

- **[文档索引](docs/INDEX.md)** - 完整的文档导航
- **[项目README](docs/README.md)** - 项目详细说明
- **[样式重构报告](docs/STYLE_REFACTOR_REPORT.md)** - 样式系统重构文档
- **[Qt兼容性修复](docs/QT_STYLE_COMPATIBILITY_FIX.md)** - Qt样式表兼容性修复报告
- **UI优化系列文档** - Sidebar对齐、边框优化等技术文档

## 🧪 测试

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

## ✨ 主要功能

- 📄 **多格式支持**: PDF、DOCX、EPUB、XLSX → Markdown
- 📝 **Markdown编辑**: 实时预览和编辑
- 📤 **多格式导出**: Markdown、PDF、EPUB
- 🎨 **现代UI**: 基于PySide6的原生桌面应用
- 🔍 **快速搜索**: 智能文档检索和管理
- 🎛️ **个性化**: 主题和偏好设置系统

## 🛠️ 技术架构

- **前端**: PySide6 + Web组件 (Cherry Markdown/Milkdown)
- **后端**: Python 3.11+ + SQLAlchemy
- **数据库**: SQLite
- **构建**: PyInstaller + Makefile
- **样式**: 统一的设计令牌系统

## 📖 开发指南

### 代码规范
- 遵循PEP 8 Python代码规范
- 使用统一的设计令牌系统 (见 `app/preference/style_constants.py`)
- 组件样式通过样式生成器复用 (见 `app/preference/style_utils.py`)

### 贡献指南
1. Fork 项目
2. 创建功能分支
3. 编写测试用例
4. 提交变更
5. 发起 Pull Request

## 📄 许可证

本项目采用 [LICENSE](LICENSE) 许可证。

## 🤝 支持

如有问题或建议，请查看 [文档](docs/) 或提交 Issue。

---

> 💡 **提示**: 推荐先阅读 [docs/INDEX.md](docs/INDEX.md) 了解完整的文档结构，以及 [test/README.md](test/README.md) 了解测试体系。