# Design: Editor data/navigation performance optimization

## Engineering Review Summary

本方案从“架构重构”收敛为“小步修复 + 可测试边界”。核心判断：当前代码处在“repaying debt”状态，应该先修数据安全和切换路径，而不是一次性引入完整异步保存系统。最小收益路径是：先让保存不会误写，读取失败不会误清空，加载不会触发 autosave，切换不会重复 setValue。

## Goals

- 正文保存只更新正文，不修改导入来源、转换状态、标签、树结构等元数据。
- 前端读取失败和真实空文档可区分。
- 程序性内容加载不触发用户编辑 dirty/autosave。
- 页面切换过程中，同一 logical navigation 只对当前 item 应用一次内容。
- 文档树加载使用轻量节点，避免 N+1 查询和正文复制。
- 测试入口能真实反映失败。

## Non-Goals

- 不重写整个编辑器插件系统。
- 不迁移 SQLite 到其他数据库。
- 不引入新的长期后台 worker、进程或外部队列。
- 不删除或重建现有历史数据。
- 不改变 Markdown/Excalidraw 的用户可见编辑功能。
- 不在 MVP 中实现历史 diff、压缩 blob、content-addressed storage 或持久 outbox。

## Key Design Principle

优先使用现有 PySide6 / QTimer / SQLAlchemy 结构。新增概念必须满足两个条件：

1. 能直接消除当前已验证风险。
2. 能被小测试覆盖，不依赖 GUI 人工观察。

如果一个设计需要新增 2 个以上长期维护类，或需要跨线程 SQLite 写入，默认视为过重，必须降级为更小实现。

## Proposed Architecture

### 1. Persistence API split

新增轻量正文保存接口：

```python
def save_content(self, item_id, content, *, page_type=None, page_engine=None):
    """只保存正文、content_md5、updated_at；不更新任何元数据字段。"""
```

保留 `save_item()` 兼容创建、导入、编辑元数据流程，但更新逻辑必须变成 patch 语义：

- 可选更新参数默认 `None`。
- `None` 表示不更新。
- 空字符串 `''` 只在调用方显式传入时表示清空字段。
- 编辑器正文保存不得调用会覆盖元数据的通用路径。

#### Why this is minimal

不新增表，不改 schema，不要求调用方一次性全部迁移。先把最危险的误覆盖切断。

### 2. Frontend getContent contract

保持现有 handler 文件和 action 名称，只改返回语义。

Ready response:

```json
{
  "success": true,
  "ready": true,
  "content": "...",
  "item_id": "123"
}
```

Not ready response:

```json
{
  "success": false,
  "ready": false,
  "error_code": "EDITOR_NOT_READY",
  "error": "Editor instance is not ready",
  "item_id": "123"
}
```

Backend rule:

- `success=false`：不得调用保存。
- `error_code=EDITOR_NOT_READY`：保留当前 dirty 状态，允许导航继续。
- `success=true` 且 `ready=true` 且 content 为空：才表示用户真实清空。

### 3. Programmatic load guard

在 `MarkRenderEditor` 内使用一个简单 guard，而不是新状态机框架：

```text
set_current_item_from_db
  -> _loading_content = True
  -> set item_id/page_type
  -> set frontend content once
  -> _loading_content = False

on_item_text_changed
  -> if _loading_content: do not dirty, do not autosave
  -> else: mark dirty and schedule save
```

这个 guard 需要覆盖：

- `set_current_item(...)`
- `set_text_content(...)` 的程序性调用
- 页面 loaded 后的初始内容注入

### 4. Navigation token

不新增大型状态机类，只在 `MainWindow` 或 `MarkRenderEditor` 维护递增 token：

```text
navigation_token += 1
token = navigation_token
load target item
async/delayed callback -> if token != navigation_token: return
```

Rules:

- `QTimer.singleShot` callback 必须校验 token。
- JS callback 必须校验 token 和 item_id。
- 同 page_type 切换不得调用 `_reset_page_state()`。
- 不再无条件执行 `main.py` 中 100ms 二次 setValue。

### 5. Deferred save, MVP version

原 spec 的 “SaveQueue(serial worker)” 容易过度设计。MVP 改为更轻的 pending-save：

```text
user edit
  -> update in-memory latest_content_snapshot
  -> mark dirty
  -> QTimer debounce
  -> save_content on timeout

navigation
  -> if dirty snapshot exists: schedule immediate save via QTimer.singleShot(0, save)
  -> switch UI using target content
```

首版限制：

- 不新增线程。
- 不跨线程使用 SQLite session。
- 不新增持久 outbox 表。
- 关闭窗口时仍可同步 flush，但必须遵守 getContent failure contract。

后续如果卡顿仍明显，再评估真正的 worker 与 WAL/busy timeout。

### 6. QuickPick lightweight tree

新增轻量查询：

```python
def load_tree_nodes(self):
    """一次查询树展示所需字段，不返回 content。"""
```

每个节点只返回：

- `id`
- `title`
- `tags`
- `page_type`
- `page_engine`
- `parent_id`
- `order`
- `level`
- `is_folder`
- `icon_type`
- `icon_path`
- `icon_color`
- `display_name`
- `updated_at`
- `created_at`

树构建方式：

```text
records = load_tree_nodes()
by_parent = group by parent_id
build children recursively in memory
```

这保留现有 QTreeWidget，不引入虚拟列表或新 UI 控件。

### 7. History and disk sync policy

MVP 只做三件事：

1. 程序性加载不触发历史。
2. 自动保存使用 debounce 合并。
3. `sync_write_localdisk()` 返回成功/失败，不只吞日志。

不在 MVP 中做：

- 历史 diff 存储。
- 历史压缩。
- Excalidraw blob 拆分。
- 持久 outbox。

### 8. SDD/TDD adaptation

SDD 落地方式：

- OpenSpec requirement 先定义行为边界。
- 每个 requirement 对应至少一个 characterization test。
- 实现只满足当前 scenario，不引入未来扩展点。

TDD 顺序：

```text
1. 写失败测试：save_content preserves metadata
2. 实现 save_content / save_item patch semantics
3. 写失败测试：getContent not ready does not save empty content
4. 修改 JS handler + backend guard
5. 写失败测试：programmatic load does not dirty
6. 添加 loading guard
7. 写失败测试：same page_type switch setValue once
8. 添加 navigation token / 移除重复 setValue
9. 写失败测试：tree nodes exclude content
10. 添加 lightweight tree query
```

## Risk Analysis

| Risk | Impact | Mitigation |
|------|--------|------------|
| `save_item()` 默认值改动影响创建流程 | 新建文档默认字段可能变化 | 创建路径保留 `create_item()` 或在 `save_item(id=None)` 分支保持原默认值 |
| `getContent` 改为失败可能阻断关闭保存 | 关闭时用户可能看到 warning | warning 比误清空安全；保留 dirty 状态，不写空 |
| 移除同 page_type reset 可能保留旧前端状态 | Markdown/Excalidraw 内部状态可能串文档 | set item_id + setValue 后验证内容；仅 page_type 变化时 reset |
| 移除 100ms 二次 setValue 可能暴露页面未 ready 问题 | 首次加载内容可能没写入 | 使用 page_loaded + token guard 的单次兜底，而不是固定重复写 |
| QuickPick 不加载 content 影响依赖节点 content 的旧逻辑 | 某些右键/拖拽流程可能假设 item 中有 content | 仅树展示用 lightweight node；打开详情仍调用 `get_detail()` |
| 测试入口改为失败可能暴露大量旧测试问题 | CI/本地会从假绿变红 | 这是正确结果；可先建立小的 targeted test command，再逐步修旧测试 |

## Compatibility Notes

- `save_item(id=None)` 创建行为必须保持兼容。
- `save_item(id=existing)` 更新行为改为 patch semantics，需要检查调用方是否依赖“省略字段即清空”。若存在，需要改为显式传 `''`。
- JS handler action 名称不变，避免破坏 `BackendInterface._construct_js_code()`。
- `content` 从 QuickPick 树节点移除后，任何需要正文的操作必须显式调用 `get_detail(id)`。

## Development Plan

### Layer 0: Harness and safety tests

目标：让测试能真实失败。

输出：修复 `test/run_all_tests.py`，新增 targeted tests。

### Layer 1: Data correctness

目标：不误覆盖、不误清空。

输出：`save_content()`、`save_item()` patch semantics、JS not-ready contract、backend no-save guard。

### Layer 2: Navigation correctness

目标：加载不 dirty，切换不重复 setValue。

输出：programmatic load guard、navigation token、移除无条件二次 setValue、限制 reset。

### Layer 3: Performance cleanup

目标：树加载轻量化，保存 debounce。

输出：`load_tree_nodes()`、内存建树、搜索 debounce、pending-save debounce。

### Layer 4: Observability hardening

目标：磁盘同步失败可见。

输出：`sync_write_localdisk()` 返回状态，UI/日志可观测。

## Schedule

| Day | Work | Expected Output |
|-----|------|-----------------|
| Day 1 | Test harness + data safety tests | 测试入口不再假绿，metadata/empty-content 测试先红后绿 |
| Day 2 | `save_content` + getContent contract + backend guard | 正文保存不覆盖元数据，editor not ready 不清空 |
| Day 3 | Programmatic load guard + navigation token | 加载不触发 autosave，同 page_type 切换单次 setValue |
| Day 4 | QuickPick lightweight tree + debounce | 树节点不带 content，搜索/刷新更轻 |
| Day 5 | Disk sync status + manual verification | 磁盘失败可观测，完成 Markdown/Excalidraw 手工回归 |

## Rollback

- 每层独立提交。
- 如果 navigation token 改动引入显示问题，可回退 Layer 2，同时保留 Layer 1 的数据安全修复。
- 如果 lightweight tree 影响旧逻辑，可临时保留旧 `get_full_tree()`，让 QuickPick 使用新接口，其他调用方不变。
- 不执行破坏性 schema migration，因此 DB 回滚为代码级 revert。
