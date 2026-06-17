# Tasks

## 0. Scope guard

- [ ] 0.1 不新增长期后台 worker、外部队列、持久 outbox 表。
- [ ] 0.2 不执行破坏性 SQLite schema migration。
- [ ] 0.3 不重写 WebView/plugin 架构，只修现有链路。
- [ ] 0.4 任一阶段改动超过 8 个生产文件时，先拆分为更小 PR。

## 1. Test harness foundation

- [x] 1.1 修复 `test/run_all_tests.py`：导入失败必须导致非 0 退出。
- [x] 1.2 修复 `test/run_all_tests.py`：0 tests 必须导致非 0 退出。
- [x] 1.3 增加 targeted test 入口，先覆盖本 change 相关测试，避免被大量旧 GUI 脚本阻塞。
- [x] 1.4 记录当前环境缺失依赖时的明确错误，例如 PySide6、SQLAlchemy。

## 2. Data safety

- [x] 2.1 为 `MarkRenderManager` 新增 `save_content(item_id, content, *, page_type=None, page_engine=None)`。
- [x] 2.2 修改 `save_item(id=existing)` 为 patch semantics：省略字段不更新，显式传 `''` 才清空。
- [x] 2.3 保持 `save_item(id=None)` 创建路径默认值兼容。
- [x] 2.4 将编辑器自动保存、手动保存、关闭保存改为调用 `save_content()` 或等价安全路径。
- [x] 2.5 增加测试：正文保存不得改变 `file_path`、`converter`、`status`、`tags`、`parent_id`、`order`、`level`、`is_folder`。

## 3. Frontend readiness and empty-content safety

- [x] 3.1 修改 Markdown `getContent.js`：编辑器实例缺失时返回 `success:false`, `ready:false`, `error_code:"EDITOR_NOT_READY"`。
- [x] 3.2 修改 Excalidraw `getContent.js`：编辑器实例缺失时返回 `success:false`, `ready:false`, `error_code:"EDITOR_NOT_READY"`。
- [x] 3.3 修改后端保存逻辑：`success:false` 或 `ready:false` 时不得保存 content。
- [x] 3.4 保留真实清空能力：`success:true`, `ready:true`, `content:''` 或空 scene 仍可保存。
- [x] 3.5 增加测试：editor not ready 时 DB content 保持不变。
- [x] 3.6 增加测试：editor ready 且用户清空时 DB content 可变为空。

## 4. Programmatic load guard

- [x] 4.1 在 `MarkRenderEditor` 添加轻量 `_loading_content` guard。
- [x] 4.2 调整 `set_current_item()` 或新增 `load_item_content()`，程序性加载不触发 dirty/autosave。
- [x] 4.3 确认用户真实编辑仍会设置 dirty 并触发保存调度。
- [x] 4.4 增加测试：加载 DB 内容后 `content_changed` 为 false，autosave timer 未启动。

## 5. Navigation cleanup

- [x] 5.1 为页面切换增加递增 `navigation_token`。
- [x] 5.2 所有 `QTimer.singleShot` 内容设置 callback 必须校验 token 和 item_id。
- [x] 5.3 移除 `main.py` 中无条件 100ms 二次 `set_text_content()`，或改为 token 校验后的单次 page_loaded 兜底。
- [x] 5.4 修改 `get_or_create_page()` / 调用方逻辑：同 page_type 切换不得仅因 item 变化 reset frontend state。
- [x] 5.5 增加测试：同 page_type 文档切换最多触发 1 次 setValue，且不触发 reset。
- [x] 5.6 增加测试：旧 token 的延迟 callback 不覆盖新 item 内容。

## 6. Minimal deferred save

- [x] 6.1 使用现有 QTimer 合并保存请求，不新增线程。
- [x] 6.2 常规文档切换不再为了保存旧内容等待 15s 同步 JS timeout。
- [x] 6.3 关闭窗口时 flush pending save；若 getContent 失败，显示 warning，不写空。
- [x] 6.4 保存失败保留 dirty 状态，并在日志/状态中可见。

## 7. QuickPick tree performance

- [x] 7.1 新增轻量树查询接口，不返回 `content`。
- [x] 7.2 QuickPick 使用轻量树接口，一次查询后内存建树，避免递归 N+1。
- [x] 7.3 打开文档、历史、导出等需要正文的操作继续使用 `get_detail(id)`。
- [x] 7.4 搜索输入增加 debounce。
- [x] 7.5 删除或保护重复 `_setup_drag_drop_support()` 调用。
- [x] 7.6 增加测试：QuickPick 树节点数据不包含全文 content。

## 8. Disk sync and history MVP

- [x] 8.1 `sync_write_localdisk()` 返回 bool 或结构化结果，不只吞日志。
- [x] 8.2 内容清空时也要同步空文件，避免旧 output 残留。
- [x] 8.3 程序性加载不得产生历史记录。
- [x] 8.4 自动保存 debounce 合并高频用户编辑。
- [x] 8.5 历史 diff/压缩/outbox 只记录为后续优化，不在本 change 实现。

## 9. Verification

- [x] 9.1 运行 `python test/run_all_tests.py`，确认导入失败/0 tests 不再假绿。
- [x] 9.2 运行 targeted tests：data safety、editor readiness、programmatic load、navigation token、QuickPick lightweight tree。
- [x] 9.3 手工验证 Markdown：打开、编辑、切换、关闭、重开，内容保留且无明显卡顿。
- [x] 9.4 手工验证 Excalidraw：打开、编辑、切换、关闭、重开，scene 保留且不被空对象覆盖。
- [x] 9.5 手工验证导入文档：导入后编辑保存，`file_path/converter/status` 不被清空。
- [x] 9.6 记录一次同 page_type 切换中的 `getContent`、`setValue`、`reset_page_state` 调用次数。

  - 代码路径核对结果：同 page_type 正常切换链路中 `getContent=0`、`setValue=1`、`reset_page_state=0`。
  - Headless GUI smoke 结果：`QT_QPA_PLATFORM=offscreen` + 临时数据目录打开 Markdown/Excalidraw 并切换后，Markdown content 与 `file_path/converter/status` 保持不变，Excalidraw scene 未被空对象覆盖。

## 10. Schedule

- [x] Day 1: 完成 1.x + 2.x，测试先红后绿。
- [x] Day 2: 完成 3.x + 4.x，锁定不误清空和加载不 dirty。
- [x] Day 3: 完成 5.x + 6.x，收敛切换流程和最小 deferred save。
- [x] Day 4: 完成 7.x，优化 QuickPick 树加载和搜索。
- [x] Day 5: 完成 8.x + 9.x，做磁盘同步状态和手工回归。
