# Change: Improve Markdown editor design language and interface polish

## Why

MarkRender 的 Markdown 编辑器已经具备正确的信息架构：左侧文档树、中间编辑、右侧预览。当前短板不是功能缺失，而是设计语言没有收口。Qt 外壳、QuickPick、Cherry Markdown、legacy QSS 同时输出颜色、字号、圆角和状态样式，导致界面像“可用的内部工具”，而不像“有审美纪律的桌面 Markdown 编辑器”。

本 change 的目标是用可分阶段验证的小改动，把现有界面从“工程可用”提升到“产品精致”：统一设计 token，桥接 Cherry 运行时主题，精修 Markdown 排版，重做 QuickPick 视觉层级，并修正新建入口语义。

## Current State

已验证的关键现状：

| Area | Current behavior | Evidence |
|------|------------------|----------|
| 设计 token | `style_constants.py` 已有颜色、间距、圆角、字体 token，但 `app_style.py` 仍重复定义兼容颜色和 legacy 样式 | `app/preference/style_constants.py:14`, `app/preference/style_constants.py:108`, `app/preference/app_style.py:14`, `app/preference/app_style.py:31` |
| 多套主色 | 主色同时存在 `#3B82F6`、`#3582fb`、`#0052d9`、`#0d6efd` 等多种蓝色 | `app/preference/style_constants.py:20`, `app/editor/plugins/markdown/assets/cherry-markdown.css:596`, `app/preference/app_style.py:391`, `app/preference/app_style.py:342` |
| Cherry 运行时主题断层 | Markdown 插件实际加载 `cherry-markdown.min.css`，Cherry 内部定义独立 CSS 变量，HTML body 写死白底，没有映射到应用 token | `app/editor/plugins/markdown/index.html:8`, `app/editor/plugins/markdown/index.html:16`, `app/editor/plugins/markdown/assets/cherry-markdown.min.css` |
| Markdown 排版 | 预览区使用 `word-break: break-all`，引用块 `border-left: 10px`，标题行高偏紧；实现时必须确认改动进入运行时加载的 CSS | `app/editor/plugins/markdown/assets/cherry-markdown.css:1345`, `app/editor/plugins/markdown/assets/cherry-markdown.css:1366`, `app/editor/plugins/markdown/assets/cherry-markdown.css:1544`, `app/editor/plugins/markdown/index.html:8` |
| 工具栏 | Cherry 工具栏使用自带阴影、按钮半径、分组线和 hover 规则 | `app/editor/plugins/markdown/assets/cherry-markdown.css:4990`, `app/editor/plugins/markdown/assets/cherry-markdown.css:5055`, `app/editor/plugins/markdown/assets/cherry-markdown.css:5070` |
| QuickPick 列表 | 列表项由 QSS 和 delegate 同时控制 hover/selected，图标权重大，每项都有分割线 | `app/preference/app_style.py:410`, `app/quickpick/item.py:209`, `app/quickpick/item.py:240`, `app/quickpick/item.py:348` |
| 新建入口 | 左上加号按钮 tooltip 是“新建文件夹”，点击绑定创建文件夹；同文件已存在 `show_create_menu()`，但未接入主按钮 | `app/quickpick/panel.py:101`, `app/quickpick/panel.py:126`, `app/quickpick/panel.py:128`, `app/quickpick/panel.py:1404` |

## What Changes

### MVP-A: runtime-safe convergence

1. 建立 MarkRender 应用级语义 token，覆盖 surface、text、border、accent、state、focus、control size。
2. 收口 `app_style.py` 中 editor shell / QuickPick 主路径的 legacy、duplicated、hardcoded 样式，让 Qt 控件统一走 token。
3. 固定 QuickPick 主加号行为为“打开新建菜单”，复用现有 `show_create_menu()`，并让 tooltip 与菜单行为一致。
4. 明确 QuickPick item 状态归属：推荐 QSS 只管容器，delegate 负责 item hover/selected/current 主视觉。
5. 在 Markdown 插件运行时 CSS 中增加 Cherry theme bridge，把 Cherry CSS 变量映射到 MarkRender token；`index.html` 的 body 背景改用主题变量。
6. 增加或更新可自动化验证的 characterization tests，先锁定新建入口、关键 token/helper、运行时 CSS 加载路径和既有保存/导航不回归。

### MVP-B: visual polish after guardrails

1. 精修 Markdown 预览排版：断词、标题节奏、段落宽度、引用块、代码块、表格。
2. 统一 Cherry 工具栏的按钮、分组、active、hover、focus、disabled 规则，让其像桌面编辑器原生控件。
3. 调整 QuickPick 左侧文档树视觉层级：当前项 marker、图标权重、分割线、搜索与操作按钮一致性。
4. 对 Markdown 示例、核心编辑流程、QuickPick 交互做手工验证并记录结果。

### Follow-up scope: deeper design system extraction

1. Python token 到 CSS variables 的自动生成或同步脚本。
2. 深色模式完整设计，不只做颜色反转。
3. 视觉回归截图测试。
4. 可配置编辑器排版主题。

## Out of Scope

- 不重写 Cherry Markdown 编辑器。
- 不替换 QTreeWidget 或引入虚拟列表。
- 不改变 Markdown/Excalidraw 的内容保存协议。
- 不改变数据库 schema。
- 不做深色模式完整重设。
- 不新增品牌营销页面或非编辑器页面改版。
- 不引入第三方设计系统依赖。
- 不在本 change 实现 token 生成脚本。
- 不新增长期维护的截图测试 fixture 或视觉回归系统。

## Compatibility

- 现有 `AppStyle` 调用方必须继续可用；兼容 alias 可保留，但不能作为新主路径。
- 现有 Markdown 插件入口 `index.html` 和 Cherry 初始化逻辑保持可运行。
- Cherry theme bridge 必须作用于运行时实际加载的 CSS；如果维护未压缩源 CSS，也必须明确同步方式，避免只改源文件而运行时无效。
- 现有 QuickPick 文档打开、搜索、右键菜单、拖拽逻辑不得退化。
- 现有图标资源和 `get_icon_path()` 调用保持兼容。
- 新建入口行为变更必须保留“新建 Markdown / 新建画布 / 新建文件夹”三种路径，只是调整入口层级。
- 非编辑器页面（设置、导入、历史等）不得因 token 收敛发生大范围布局或语义变化；本 change 只允许消除明显 legacy 主色或共享基础 token。

## Impact

- Affected code:
  - `app/preference/style_constants.py`
  - `app/preference/app_style.py`
  - `app/editor/plugins/markdown/index.html`
  - `app/editor/plugins/markdown/assets/cherry-markdown.min.css`
  - `app/editor/plugins/markdown/assets/cherry-markdown.css`（仅当项目继续维护未压缩源文件时同步）
  - `app/quickpick/panel.py`
  - `app/quickpick/item.py`
  - targeted tests under `test/`
- Explicitly not part of MVP implementation:
  - token export/generation scripts
  - new screenshot fixture system
  - complete dark mode

## Success Metrics

- Qt editor shell / QuickPick 主路径样式不再出现裸主色 hex，例如 `#0d6efd`、`#0052d9`、`#3582fb`，除 legacy 常量注释、兼容 alias 或第三方原始区块外。
- Cherry Markdown 运行时主色、边框、正文、背景、toolbar hover 映射到 MarkRender token，且 `index.html` 加载的 CSS 文件包含或引用该 bridge。
- Markdown 插件 body 背景不再独立写死为白色。
- Markdown 预览区不再全局使用 `word-break: break-all`。
- Blockquote 左边框不超过 4px，且不再呈现警示块视觉。
- QuickPick 当前项有可代码审查的明确标识，例如 2px accent marker 或等价实现；hover、selected、current 三态由单一层级负责主视觉，不互相覆盖。
- QuickPick 新建按钮点击打开包含“新建 Markdown / 新建画布 / 新建文件夹”的菜单，tooltip 描述该菜单行为。
- Markdown 打开、编辑、切换、关闭、重开流程不发生内容保存或页面切换回归。
