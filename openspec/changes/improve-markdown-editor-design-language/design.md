# Design: Markdown editor design language and interface polish

## Design Review Summary

本方案不追求“换皮”，而是收敛现有界面的设计语言。当前产品的结构是对的，但视觉系统由多套样式共同输出。最小收益路径是先用 characterization tests 锁住关键行为，再统一 token 与状态，桥接 Cherry Markdown 的运行时 CSS，最后精修排版与左侧导航层级。

## Goals

- 让 Qt 外壳、QuickPick、Cherry Markdown 共享同一套语义 token。
- 让 Markdown 预览区具备可长期阅读的排版质量。
- 让 Cherry 工具栏像 MarkRender 原生桌面控件，而不是第三方网页工具条。
- 让 QuickPick 左侧文档树更像写作空间导航，而不是文件类型列表。
- 让新建入口语义符合 Markdown 编辑器用户直觉，并保持 Markdown、画布、文件夹三类创建能力。

## Non-Goals

- 不重写 Cherry Markdown。
- 不替换 PySide6 / QWebEngineView 架构。
- 不新增完整暗色主题。
- 不迁移数据库。
- 不修改正文保存、历史记录、页面通信协议。
- 不把设计 token 做成跨语言生成系统；本 change 只允许手写最小 CSS variables bridge。
- 不新增长期维护的截图 fixture 或视觉回归系统。

## Key Design Principle

产品界面默认使用克制的生产力工具风格。设计应服务长时间阅读、编辑和导航，不使用装饰性渐变、玻璃拟态、大面积高饱和背景或无意义动效。

每个视觉改动必须回答一个问题：用户是否更快知道当前文档、当前状态、可点击控件或正文层级。如果不能回答，就不做。

## Proposed Architecture

### 0. Verification-first guardrails

在改视觉前先补 characterization tests，避免“样式改动”误伤行为：

- QuickPick 主加号点击应触发现有 `show_create_menu()`，菜单包含新建 Markdown、新建画布、新建文件夹。
- 主加号 tooltip 应描述“新建”菜单，而不是单一“新建文件夹”。
- Markdown 插件入口应加载包含 MarkRender theme bridge 的运行时 CSS。
- 已有 Markdown 打开、编辑、切换、关闭、重开流程的 targeted tests 必须继续通过。

这些测试优先覆盖可自动判定的行为和字符串/样式约束，不引入截图测试。

### 1. Semantic token layer

在 `style_constants.py` 中补齐语义 token，避免组件直接消费某个色阶作为语义。

建议新增或整理：

```python
SURFACE_BASE = NEUTRAL_0
SURFACE_SUBTLE = NEUTRAL_50
SURFACE_MUTED = NEUTRAL_100
SURFACE_HOVER = PRIMARY_50
SURFACE_SELECTED = PRIMARY_50

BORDER_SUBTLE = NEUTRAL_200
BORDER_DEFAULT = NEUTRAL_300
BORDER_ACCENT = PRIMARY_300

TEXT_PRIMARY = NEUTRAL_900
TEXT_SECONDARY = NEUTRAL_600
TEXT_MUTED = NEUTRAL_500
TEXT_DISABLED = NEUTRAL_400

ACCENT = PRIMARY_500
ACCENT_HOVER = PRIMARY_600
ACCENT_ACTIVE = PRIMARY_700
ACCENT_SOFT = PRIMARY_50

FOCUS_BORDER = PRIMARY_400
FOCUS_SHADOW = PRIMARY_100
```

规则：

- 组件样式使用语义 token，不直接使用 `PRIMARY_500` 等色阶，除非定义语义 token 本身。
- Legacy 常量可保留兼容，但主路径不得引用 legacy 蓝。
- `app_style.py` 只拼接样式，不重新声明颜色系统。
- 不新增 token 生成脚本；CSS 端首版手写 bridge，接受少量重复以换取低风险。

### 2. Qt control state matrix

统一控件状态：

| State | Visual rule |
|-------|-------------|
| default | surface base, subtle border, primary text |
| hover | surface hover, accent-soft border when interactive |
| pressed | accent-soft background with stronger border |
| selected | selected surface, accent text, optional current marker |
| current | selected plus explicit marker, used for active document |
| focus | visible border/shadow treatment separate from hover; do not rely on unsupported CSS `outline` in QSS |
| disabled | muted text, muted surface, no accent |

落地点：

- `LINE_EDIT`
- `SIDEBAR_BUTTON`
- `QUICKPICK_PANEL`
- `SCROLLBAR_STYLE`
- `TAB_STYLE`
- QuickPick new action button

Focus 的 Qt 实现优先使用 QSS 支持稳定的 border/background/padding 或控件属性方案；不得把 Web CSS 的 `outline` 当作必然可用能力。

### 3. Cherry runtime theme bridge

Markdown 插件入口 `app/editor/plugins/markdown/index.html` 当前加载 `./assets/cherry-markdown.min.css`。因此 bridge 必须进入运行时加载链路：

- 推荐方案：在 `cherry-markdown.min.css` 末尾追加 MarkRender theme bridge block，并在未压缩 `cherry-markdown.css` 同步同一 block，避免维护者只看源文件时丢失上下文。
- 可接受方案：新增独立 `markrender-theme.css` 并在 `index.html` 中位于 Cherry CSS 之后加载；如果采用该方案，需同步更新 Impact 和测试，确保加载顺序被验证。
- 禁止方案：只修改 `cherry-markdown.css` 而不改变运行时加载文件。

示意：

```css
:root {
  --mr-surface-base: #ffffff;
  --mr-surface-subtle: #f9fafb;
  --mr-border-subtle: #e5e7eb;
  --mr-text-primary: #111827;
  --mr-text-secondary: #4b5563;
  --mr-accent: #3b82f6;
  --mr-accent-hover: #2563eb;
  --mr-accent-soft: #eff6ff;
}

.cherry {
  --primary-color: var(--mr-accent);
  --base-font-color: var(--mr-text-primary);
  --base-sub-font-color: var(--mr-text-secondary);
  --base-border-color: var(--mr-border-subtle);
  --base-editor-bg: var(--mr-surface-base);
  --base-previewer-bg: var(--mr-surface-base);
  --toolbar-bg: var(--mr-surface-base);
  --toolbar-btn-hover-bg: var(--mr-accent-soft);
  --toolbar-btn-hover-color: var(--mr-accent-hover);
}

body {
  background: var(--mr-surface-base);
}
```

首版可以手写 CSS variables。后续如果 token 漂移明显，再另起 change 做 Python 到 CSS 的生成脚本。

### 4. Markdown preview typography

预览区目标：长文可读，结构清楚，中英混排自然。

规则：

- `.cherry-markdown` 不使用全局 `word-break: break-all`。
- 长链接和长 token 使用局部 overflow/wrap 规则，不能让普通英文单词被不自然打断。
- 正文行宽控制在可读范围。双栏预览可使用容器 padding 与 max-width，避免长行横跨整个右栏。
- H1/H2/H3/H4 使用不同 margin rhythm，不用单一固定 `30px`。
- 标题行高使用 1.2 到 1.3。
- blockquote 左边框 3 到 4px，背景轻，文字不使用警告语义色。
- inline code 使用中性轻背景，不用错误语义作为默认文字色。
- table header 使用独立表格 token，不复用 inline-code 背景。

### 5. Cherry toolbar normalization

工具栏目标：桌面编辑器控件感，低干扰，高可识别。

规则：

- toolbar 不使用强阴影，改为底部分割线或极轻 elevation。
- toolbar button 高度统一到 28 到 32px。
- hover、pressed、active、disabled 使用 state matrix。
- preview toggle、code theme 等模式按钮必须有 active 态。
- 分组优先用间距，不依赖显眼分割线。
- focus 态可见，支持键盘用户；Web CSS 可使用 outline/box-shadow，但 Qt QSS 不套用同一写法。

### 6. QuickPick navigation polish

QuickPick 目标：当前文档明确，列表安静，内容标题优先。

调整方向：

- 图标背景从 32x32 降到 28x28，降低图标抢眼程度。
- item 高度选择紧凑型 48px 或舒展型 60px，但不能停留在图标权重偏大的中间态。
- 当前项使用 selected background 加 2px accent marker，或等价明确方案。
- 删除每项底部分割线，或仅在分组之间显示。
- QSS 与 delegate 只保留一个状态色来源。推荐且本 change 固定采用：QSS 管容器，delegate 管 item hover/selected/current 绘制。
- 搜索框和新建按钮走同一套 QuickPick token。

### 7. New action semantics

主加号入口固定为“打开新建菜单”，不再保留二选一方案。

```text
点击 +
  -> 调用 QuickPickPanel.show_create_menu()
    -> 新建 Markdown
    -> 新建画布
    -> 新建文件夹
```

原因：

- 现有代码已具备 `show_create_menu()`，落地成本低。
- 菜单方案同时保留三类创建能力，不破坏文件夹创建入口。
- tooltip 可稳定写为“新建”，语义不再和点击行为冲突。

## Risk Analysis

| Risk | Impact | Mitigation |
|------|--------|------------|
| 统一 token 影响其他窗口 | 设置、导入、历史等页面视觉变化 | 主路径先改编辑器和 QuickPick，其他页面只消除明显 legacy 蓝，不做大范围重设；新增非编辑器页面 guard |
| Cherry CSS 是第三方产物，直接改动难维护 | 后续升级可能覆盖样式 | 将 MarkRender 覆盖集中放在文件末尾或独立 theme block，验证运行时加载文件，避免散改库代码 |
| 只改未压缩 CSS 导致运行时无效 | spec 通过但产品无变化 | 测试 `index.html` 加载路径与 bridge 所在文件，明确 `cherry-markdown.min.css` 是当前 runtime target |
| QuickPick delegate 与 QSS 状态冲突 | hover/selected/current 双重渲染 | 固定 delegate owns item states，QSS owns container states，并用代码审查检查冲突 selector |
| 新建入口行为变化影响习惯 | 习惯单击新建文件夹的用户需要多一步 | tooltip 与菜单清楚表达，保留新建文件夹能力，复用现有菜单 |
| 排版变更影响复杂 Markdown | 表格、代码块、长链接可能溢出 | 对长链接、代码块、表格单独定义 overflow 规则，手工验证 fixture 内容但不新增长期 fixture 系统 |

## Development Plan

### Layer 0: Characterization tests and inventory

目标：先锁定新建入口、运行时 CSS 文件、裸 hex 清单、Cherry 变量、QuickPick 状态来源和保存/导航回归边界。

输出：失败优先的测试或静态检查清单，避免漏改或误删兼容层。

### Layer 1: MVP-A token and Qt style convergence

目标：让 Qt editor shell / QuickPick 主路径控件使用语义 token。

输出：`style_constants.py` 语义 token，`app_style.py` 去重，按钮、输入框、滚动条、splitter、tab 使用统一状态；非编辑器页面只接受最小兼容改动。

### Layer 2: MVP-A QuickPick create action and item state ownership

目标：修正入口语义，消除 QSS/delegate 状态冲突。

输出：主加号绑定 `show_create_menu()`，tooltip 与行为一致，delegate 负责 item hover/selected/current 主视觉，current marker 可代码审查。

### Layer 3: MVP-A Cherry runtime theme bridge

目标：消除 Qt 外壳和 Cherry 内核断层，并确保改动进入运行时。

输出：运行时 CSS theme bridge，body 背景、toolbar、editor、previewer 主变量统一；源 CSS 是否同步由实现方式明确。

### Layer 4: MVP-B Markdown preview and toolbar polish

目标：提升阅读体验并降低工具栏第三方感。

输出：断词、标题、段落、blockquote、code、table 排版规则；toolbar hover/active/focus/disabled 和分组规则。

### Layer 5: MVP-B QuickPick visual polish

目标：提升左侧导航质感。

输出：文档树 item 高度、图标权重、分割线、搜索与操作按钮一致性。

### Layer 6: Verification and release gate

目标：保证视觉改动不破坏核心编辑流程。

输出：targeted tests、OpenSpec validate、手工验证记录。若 MVP-B 视觉 polish 触发行为风险，可先发布 MVP-A。

## Rollback

- 每层独立提交。
- 如果 Cherry theme bridge 出现显示问题，可回退 Layer 3，保留 Qt token 与 QuickPick create 修复。
- 如果 QuickPick delegate 调整影响点击、拖拽或右键菜单，可回退 Layer 5，保留新建入口语义修复。
- 所有改动为样式和入口行为层，不涉及 DB schema，回滚为代码级 revert。
