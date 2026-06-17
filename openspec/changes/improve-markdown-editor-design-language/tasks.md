# Tasks

## 0. Scope guard

- [x] 0.1 不重写 Cherry Markdown、QWebEngineView 或 QuickPick 数据架构。
- [x] 0.2 不修改数据库 schema、保存协议或历史记录格式。
- [x] 0.3 不在本 change 中实现完整深色模式。
- [x] 0.4 不在本 change 中实现 token 生成脚本、截图 fixture 系统或视觉回归平台。
- [x] 0.5 非编辑器页面仅允许最小兼容性收敛，不做整页视觉重设。
- [x] 0.6 任一阶段改动超过 8 个生产文件时，先拆分为更小 PR。

## 1. Characterization tests first

- [x] 1.1 先补或更新测试，锁定 QuickPick 主加号入口行为：点击触发菜单，而不是直接新建文件夹。
- [x] 1.2 先补或更新测试，锁定菜单包含新建 Markdown、新建画布、新建文件夹三种路径。
- [x] 1.3 先补或更新测试，锁定主加号 tooltip 与菜单行为一致。
- [x] 1.4 先补或更新测试，锁定 Markdown 插件运行时加载的 CSS 文件包含 MarkRender theme bridge 或等价 bridge 加载链路。
- [x] 1.5 复跑现有保存/导航 targeted tests，确认设计改动的保护网先存在。

## 2. MVP-A token convergence

- [x] 2.1 盘点 `app_style.py` 中 editor shell / QuickPick 主路径裸 hex，至少覆盖按钮、滚动条、splitter、tab、QuickPick。
- [x] 2.2 在 `style_constants.py` 增加或整理语义 token：surface、text、border、accent、state、focus。
- [x] 2.3 移除 `app_style.py` 中重复的颜色真相，保留兼容 alias 但主路径不再重新声明 token。
- [x] 2.4 清理重复定义，例如被后定义覆盖的 `MAXIMIZE_BUTTON`。
- [x] 2.5 将 `LINE_EDIT`、`SIDEBAR_BUTTON`、`SCROLLBAR_STYLE`、`TAB_STYLE` 的主路径颜色改为语义 token。
- [x] 2.6 验证非编辑器页面未因 token 收敛出现明显破坏性样式变化。

## 3. MVP-A QuickPick semantics and state ownership

- [x] 3.1 将 `QuickPickPanel` 新建按钮样式从 `panel.py` 手写 QSS 移到 `AppStyle` 或 token 化 helper。
- [x] 3.2 统一搜索框、新建按钮、树容器的 border、radius、hover、pressed、focus 规则。
- [x] 3.3 固定 QuickPick item 状态来源：QSS 只管容器，delegate 负责 item hover/selected/current 主视觉。
- [x] 3.4 为当前文档增加明确 current marker，例如 2px accent marker 或等价方案。
- [x] 3.5 降低图标背景权重，验证标题优先于文件类型图标。
- [x] 3.6 删除每项强分割线，或改为只在分组边界出现。
- [x] 3.7 将主加号点击接到现有 `show_create_menu()`，固定为菜单方案。
- [x] 3.8 将主加号 tooltip 从“新建文件夹”改为与菜单行为一致的文案。
- [x] 3.9 验证新建 Markdown、新建画布、新建文件夹均可通过主加号菜单到达。

## 4. MVP-A Cherry runtime bridge

- [x] 4.1 确认运行时 CSS 落点：`index.html` 当前加载 `./assets/cherry-markdown.min.css`。
- [x] 4.2 在运行时 CSS 加载链路中新增 MarkRender theme bridge block，集中定义 `--mr-*` CSS variables。
- [x] 4.3 将 Cherry 的 `--primary-color`、`--base-font-color`、`--base-border-color`、`--base-editor-bg`、`--base-previewer-bg` 映射到 `--mr-*`。
- [x] 4.4 将 toolbar 背景、hover、active、disabled、border 映射到同一套变量。
- [x] 4.5 移除或覆盖 `index.html` 中写死白底的 body 样式，改用主题变量。
- [x] 4.6 如果项目继续维护未压缩 `cherry-markdown.css`，同步追加同一 bridge block 并注明其非运行时真相地位。
- [x] 4.7 确保 Markdown 和 Excalidraw 插件加载不受 CSS 变量变更影响。

## 5. MVP-B Markdown preview typography polish

- [x] 5.1 将 `.cherry-markdown` 全局 `word-break: break-all` 改为更适合阅读的断词策略。
- [x] 5.2 调整 H1/H2/H3/H4 的字号、行高、上下 margin，形成稳定阅读节奏。
- [x] 5.3 调整正文段落、列表、hr 的间距，避免默认主题的机械感。
- [x] 5.4 将 blockquote 左边框降到不超过 4px，并使用轻背景和中性文字色。
- [x] 5.5 调整 inline code 和 code block，使其不使用错误语义色作为默认正文表达。
- [x] 5.6 为 table header、border、cell padding 定义独立 token 或独立样式语义，避免复用 inline-code 背景。
- [x] 5.7 验证长链接、长英文、中文段落、代码块、表格不会出现不可读断行或横向溢出。

## 6. MVP-B Toolbar and interaction states

- [x] 6.1 降低 Cherry toolbar shadow，改为底部分割线或极轻 elevation。
- [x] 6.2 统一 toolbar button 高度、padding、radius。
- [x] 6.3 为 preview toggle、codeTheme 等模式按钮增加明确 active 态。
- [x] 6.4 为 toolbar button、dropdown item、bubble menu 增加一致 hover/pressed/focus/disabled 样式。
- [x] 6.5 用间距优先表达工具栏分组，弱化显眼分割线。

## 7. Verification and regression gate

- [x] 7.1 增加或更新样式/token 单元测试，确保关键 QSS 不再含 legacy 主色裸 hex。
- [x] 7.2 增加 QuickPick 行为测试：主加号入口打开菜单，且三种创建路径存在。
- [x] 7.3 增加运行时 CSS 校验：bridge 存在于实际加载链路，而不是只存在于未加载源文件。
- [x] 7.4 运行现有 targeted tests，确认保存、切换、QuickPick 交互不回归。
- [x] 7.5 手工验证 Markdown 示例：标题、段落、列表、引用、代码块、表格、长链接。
- [x] 7.6 手工验证核心流程：打开 Markdown、编辑、切换文档、关闭、重开，内容不丢失。
- [x] 7.7 手工验证 QuickPick：hover、selected、current、搜索、新建、右键菜单、拖拽不退化。
- [x] 7.8 运行 `openspec validate --strict` 并修复校验问题。

## 8. Delivery layering and schedule

- [x] Day 1 AM：完成 1.x，先建立 characterization tests 与运行时 CSS guardrail。
- [x] Day 1 PM：完成 2.1-2.5，收口 token 与 Qt 主路径样式。
- [x] Day 2：完成 3.x，统一 QuickPick 控件、状态归属和新建入口语义。
- [x] Day 3：完成 4.x，桥接 Cherry 运行时主题并处理 body 背景。
- [x] Day 4：完成 5.x + 6.x，精修 Markdown 预览排版与工具栏状态。
- [x] Day 5 AM：完成 7.1-7.4，跑自动化验证与 OpenSpec 校验。
- [x] Day 5 PM：完成 7.5-7.7，做手工回归并决定是否只先发布 MVP-A。
