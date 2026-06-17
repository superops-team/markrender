# Change: Optimize editor data persistence, navigation, and performance

## Why

MarkRender 当前的核心风险不是单个函数慢，而是数据保存、页面切换、WebView 通信、历史记录和本地磁盘同步被串在同一条 UI 主路径上。用户点击文档时，现有流程会先同步读取前端内容，再写 DB、写历史、写 output 文件，然后才继续切换页面。该链路会造成卡顿、重复 reset/setValue、导入元数据被正文保存覆盖、编辑器未 ready 时空内容误保存、QuickPick 树加载随文档量放大、测试入口假绿灯。

本 change 的目标是用小而可验证的改动先修复数据安全和切换卡顿主因，而不是重写编辑器或引入大型新架构。优先保证：不丢数据、不误清空、不重复刷新、测试能失败。

## Current State

已验证的关键现状：

| Area | Current behavior | Evidence |
|------|------------------|----------|
| 页面切换前保存 | QuickPick 点击后先调用同步保存，再切换文档 | `app/quickpick/panel.py:1110`, `app/quickpick/panel.py:1173`, `app/editor/editor.py:279`, `app/editor/editor.py:289` |
| 同步 JS 阻塞 UI | `send_message_sync()` 使用 `QEventLoop.exec()` 等待 JS，默认超时 15s | `app/editor/backend_interface.py:27`, `app/editor/backend_interface.py:50`, `app/editor/backend_interface.py:62`, `app/editor/backend_interface.py:94` |
| 普通保存会覆盖元数据 | `save_item()` 默认 `file_path=''`, `converter=''`, `status=''`，更新时 `is not None` 即覆盖 | `db/markrender_manager.py:108`, `db/markrender_manager.py:115`, `db/markrender_manager.py:176`, `db/markrender_manager.py:178`, `db/markrender_manager.py:182` |
| DB 与磁盘非事务一致 | DB commit 后 finally 同步写 output，写失败只打日志 | `db/markrender_manager.py:213`, `db/markrender_manager.py:294`, `db/markrender_manager.py:437`, `db/markrender_manager.py:458`, `db/markrender_manager.py:460` |
| 重复 reset/setValue | 复用页面时 reset，切换后 setValue，100ms 后再次 setValue | `app/editor/webengine.py:302`, `app/editor/webengine.py:376`, `main.py:263`, `main.py:269` |
| 加载内容触发 autosave | DB 内容加载走 `item.set_text()`，再触发 `on_item_text_changed()` 和 autosave timer | `app/editor/editor.py:273`, `app/editor/editor.py:277`, `app/editor/editor.py:132`, `app/editor/editor.py:143` |
| 编辑器未 ready 可能返回空成功 | Markdown/Excalidraw handler 找不到实例时返回 `success: true` + 空内容 | `app/editor/plugins/markdown/handler/getContent.js:18`, `app/editor/plugins/markdown/handler/getContent.js:21`, `app/editor/plugins/excalidraw/handler/getContent.js:72`, `app/editor/plugins/excalidraw/handler/getContent.js:83` |
| 历史表全量复制 | 每次内容变化保存完整 `old_content` 和 `new_content` | `db/models.py:67`, `db/models.py:68`, `db/models.py:125`, `db/models.py:157`, `db/models.py:158` |
| 树加载 N+1 且带全文 | `get_full_tree()` 递归调用 `get_children()`，`get_children()` 返回 `content` | `db/markrender_manager.py:952`, `db/markrender_manager.py:972`, `db/markrender_manager.py:1096`, `db/markrender_manager.py:1100` |
| 测试入口假绿灯 | 聚合脚本导入失败只打印，0 tests 仍成功 | `test/run_all_tests.py:21`, `test/run_all_tests.py:33`, `test/run_all_tests.py:41` |

## Review Corrections Applied

本轮校验后，对原 spec 做出以下收敛：

| Concern | Correction |
|---------|------------|
| “保存队列 / outbox / worker” 表述偏重，容易被大模型理解成新建复杂后台系统 | 改为两阶段：MVP 只做 Qt 主线程内的轻量 pending-save 与 QTimer 合并；真正 worker/outbox 仅作为后续扩展，不是首版必做 |
| “异步保存”容易被理解为必须引入线程和跨线程 SQLite 写 | 明确首版不新增线程，不引入新 DB 表，不做 schema migration；先消除同步 JS 等待和重复 setValue |
| “可观测”“可重试”偏抽象 | 明确首版标准：函数返回失败状态、UI 日志/状态字段可见、关闭时弹出 warning；持久 outbox 延后 |
| “状态机”可能被理解成新框架 | 明确为现有 `MainWindow` / `MarkRenderEditor` 上的布尔 guard 与递增 token，不新增大型状态机类 |
| 历史压缩/diff 容易扩大范围 | 明确历史压缩为后续阶段；MVP 只保证程序性加载不写历史，自动保存做 debounce 合并 |
| SDD/TDD 适配不清 | 增加“先写 characterization tests，再改实现”的任务顺序和测试分层 |

## What Changes

### MVP scope: data safety + navigation stability

1. 将正文保存与元数据更新分离，保证编辑器保存不会清空导入元数据、标签或树结构字段。
2. 修正前端 `getContent` 协议，编辑器未 ready 时返回失败，后端不得把读取失败保存为空内容。
3. 区分程序性加载与用户编辑，加载 DB 内容时不设置 dirty、不启动 autosave。
4. 收敛页面切换流程：同 page_type 切换不 reset；一次切换只允许当前 token 执行一次 setValue。
5. QuickPick 树改用轻量节点查询，不加载正文 content。
6. 修复测试入口：导入失败或 0 tests 必须失败。

### Follow-up scope: performance hardening

1. 保存操作可逐步改为 pending-save + QTimer 合并，减少切换路径同步等待。
2. SQLite 可启用 WAL / busy timeout，降低锁冲突风险。
3. 磁盘同步失败从“只写日志”升级为返回失败状态和 UI 可见提示。
4. 历史记录压缩、diff 或持久 outbox 不进入 MVP，单独评估。

## Out of Scope

- 不重写编辑器插件系统。
- 不引入新的后台服务、进程或长期运行 worker。
- 不新增破坏性 SQLite schema migration。
- 不删除、重建或迁移既有历史记录。
- 不改变 Markdown/Excalidraw 的用户可见编辑能力。
- 不在本 change 中实现历史 diff 存储、压缩 blob、云同步、多端协作。

## Compatibility

- Existing calls to `save_item()` must keep working for create/import/edit-dialog flows.
- Existing SQLite rows remain readable without migration.
- Existing output files under user data dir remain valid.
- Existing plugin `setValue` / `getContent` entrypoint names remain unchanged; only response semantics become stricter.
- Existing tests and ad-hoc scripts may need dependency setup, but the runner must not report false success.

## Impact

- Affected code:
  - `main.py`
  - `app/editor/editor.py`
  - `app/editor/backend_interface.py`
  - `app/editor/webengine.py`
  - `app/editor/plugins/markdown/handler/getContent.js`
  - `app/editor/plugins/excalidraw/handler/getContent.js`
  - `app/quickpick/panel.py`
  - `db/markrender_manager.py`
  - `test/run_all_tests.py`
  - targeted tests under `test/`
- Defer unless needed:
  - `db/models.py` history storage layout
  - `db/db_manager.py` WAL / busy timeout
  - persistent disk-sync outbox

## Success Metrics

- Calling the editor content-save path does not change `file_path`、`converter`、`status`、`tags`、`parent_id`、`order`、`level`、`is_folder`。
- Markdown/Excalidraw editor not ready returns `success:false` and does not update DB content.
- Loading DB content into the editor leaves `content_changed=false` and does not start autosave.
- Same page type document switch performs no reset solely due to item change and calls `setValue` at most once for the current token.
- QuickPick tree loading uses node dictionaries without `content`.
- `python test/run_all_tests.py` exits non-zero on import failure or zero executed tests.
- No existing Markdown/Excalidraw document becomes unreadable after the change.
