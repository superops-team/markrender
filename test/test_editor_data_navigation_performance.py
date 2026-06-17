#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import tempfile
import types
import unittest
import importlib.util

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


def load_run_all_tests_module():
    module_path = os.path.join(PROJECT_ROOT, "test", "run_all_tests.py")
    spec = importlib.util.spec_from_file_location("markrender_run_all_tests", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_project_file(*parts):
    with open(os.path.join(PROJECT_ROOT, *parts), "r", encoding="utf-8") as file:
        return file.read()


class TestRunAllTestsHarness(unittest.TestCase):
    def test_import_failure_makes_run_unsuccessful(self):
        run_all_tests = load_run_all_tests_module()

        success = run_all_tests.run_all_tests(
            test_modules=["test.module_that_does_not_exist_for_contract"]
        )

        self.assertFalse(success)

    def test_zero_discovered_tests_makes_run_unsuccessful(self):
        run_all_tests = load_run_all_tests_module()

        module_name = "empty_contract_test_module"
        sys.modules[module_name] = types.ModuleType(module_name)
        try:
            success = run_all_tests.run_all_tests(test_modules=[module_name])
        finally:
            del sys.modules[module_name]

        self.assertFalse(success)


class TestContentPersistenceContract(unittest.TestCase):
    def setUp(self):
        try:
            from db.markrender_manager import MarkRenderManager
        except ModuleNotFoundError as exc:
            if exc.name == "sqlalchemy":
                self.skipTest("SQLAlchemy is required for persistence contract tests")
            raise

        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        os.environ["MARKDOWN_RENDER_DATA"] = self.temp_dir.name
        self.addCleanup(lambda: os.environ.pop("MARKDOWN_RENDER_DATA", None))
        self.manager = MarkRenderManager(
            db_path=os.path.join(self.temp_dir.name, "contract.db")
        )

    def test_save_content_updates_body_without_metadata(self):
        item_id = self.manager.save_item(
            title="Imported document",
            content="original",
            tags="alpha,beta",
            file_path="/tmp/imported.md",
            converter="pandoc",
            status="processed",
            page_type="markdown",
            page_engine="markdown",
            parent_id=7,
            order=3,
            level=2,
            is_folder=0,
            icon_type="emoji",
            icon_path="doc.svg",
            icon_color="#ff0000",
            display_name="Imported",
        )

        self.manager.save_content(item_id, "changed")
        detail = self.manager.get_detail(item_id)

        self.assertEqual(detail["content"], "changed")
        self.assertEqual(detail["file_path"], "/tmp/imported.md")
        self.assertEqual(detail["converter"], "pandoc")
        self.assertEqual(detail["status"], "processed")
        self.assertEqual(detail["tags"], "alpha,beta")
        self.assertEqual(detail["parent_id"], 7)
        self.assertEqual(detail["order"], 3)
        self.assertEqual(detail["level"], 2)
        self.assertEqual(detail["is_folder"], 0)
        self.assertEqual(detail["icon_type"], "emoji")
        self.assertEqual(detail["icon_path"], "doc.svg")
        self.assertEqual(detail["icon_color"], "#ff0000")
        self.assertEqual(detail["display_name"], "Imported")

    def test_save_item_omitted_optional_fields_keep_existing_values(self):
        item_id = self.manager.save_item(
            title="Imported document",
            content="original",
            tags="alpha,beta",
            file_path="/tmp/imported.md",
            converter="pandoc",
            status="processed",
            page_type="markdown",
            page_engine="markdown",
        )

        self.manager.save_item(id=item_id, content="changed")
        detail = self.manager.get_detail(item_id)

        self.assertEqual(detail["content"], "changed")
        self.assertEqual(detail["file_path"], "/tmp/imported.md")
        self.assertEqual(detail["converter"], "pandoc")
        self.assertEqual(detail["status"], "processed")
        self.assertEqual(detail["tags"], "alpha,beta")

    def test_save_item_explicit_empty_string_clears_metadata(self):
        item_id = self.manager.save_item(
            title="Imported document",
            content="original",
            tags="alpha,beta",
            page_type="markdown",
            page_engine="markdown",
        )

        self.manager.save_item(id=item_id, tags="")
        detail = self.manager.get_detail(item_id)

        self.assertEqual(detail["tags"], "")

    def test_create_path_keeps_default_values(self):
        item_id = self.manager.save_item(title="New document", content="body")
        detail = self.manager.get_detail(item_id)

        self.assertEqual(detail["status"], "processed")
        self.assertEqual(detail["page_type"], "markdown")
        self.assertEqual(detail["page_engine"], "markdown")


class TestFrontendReadinessContract(unittest.TestCase):
    def test_markdown_get_content_reports_not_ready_without_empty_success(self):
        script = read_project_file(
            "app", "editor", "plugins", "markdown", "handler", "getContent.js"
        )

        self.assertIn("EDITOR_NOT_READY", script)
        self.assertIn("ready: false", script)
        self.assertIn("success: false", script)
        self.assertNotIn("未找到支持的Markdown编辑器实例，返回空内容", script)

    def test_excalidraw_get_content_reports_not_ready_without_empty_success(self):
        script = read_project_file(
            "app", "editor", "plugins", "excalidraw", "handler", "getContent.js"
        )

        self.assertIn("EDITOR_NOT_READY", script)
        self.assertIn("ready: false", script)
        self.assertIn("success: false", script)
        self.assertNotIn("未找到支持的Excalidraw编辑器实例，返回空内容", script)

    def test_backend_save_paths_require_ready_successful_content(self):
        source = read_project_file("app", "editor", "editor.py")

        self.assertIn("def _is_content_response_ready", source)
        self.assertIn("not parsed_data.get('ready', False)", source)
        self.assertNotIn("即使获取内容失败，也要尝试保存", source)
        self.assertNotIn('content = ""\n                frontend_item_id', source)


class TestProgrammaticLoadGuardContract(unittest.TestCase):
    def test_editor_has_loading_guard_around_current_item_loads(self):
        source = read_project_file("app", "editor", "editor.py")

        self.assertIn("self._loading_content = False", source)
        self.assertIn("if self._loading_content:", source)
        self.assertIn("self._loading_content = True", source)
        self.assertIn("self._loading_content = False", source)
        self.assertIn("finally:", source)

    def test_programmatic_load_does_not_start_autosave_or_dirty(self):
        source = read_project_file("app", "editor", "editor.py")
        guard_index = source.index("if self._loading_content:")
        timer_index = source.index("self.content_change_timer.start(1000)")

        self.assertLess(guard_index, timer_index)


class TestNavigationDeferredSaveContract(unittest.TestCase):
    def test_main_window_uses_navigation_token_for_delayed_content_apply(self):
        source = read_project_file("main.py")

        self.assertIn("self._navigation_token = 0", source)
        self.assertIn("def _next_navigation_token", source)
        self.assertIn("def _is_active_navigation", source)
        self.assertIn("navigation_token", source)
        self.assertNotIn("QTimer.singleShot(100, lambda: self.editor.set_text_content(content))", source)

    def test_same_page_type_get_or_create_does_not_reset_frontend_state(self):
        source = read_project_file("app", "editor", "webengine.py")

        self.assertNotIn("self._reset_page_state(preloaded_view, page_type)", source)

    def test_quickpick_switch_uses_deferred_save_without_sync_gate(self):
        source = read_project_file("app", "quickpick", "panel.py")

        save_current_item_body = source[source.index("def save_current_item") : source.index("def _save_with_callback")]
        self.assertIn("request_deferred_save", save_current_item_body)
        self.assertIn("self._execute_switch()", save_current_item_body)
        self.assertNotIn("editor.save_current_item()", save_current_item_body)

    def test_editor_has_non_blocking_deferred_save_path_for_navigation(self):
        source = read_project_file("app", "editor", "editor.py")

        self.assertIn("def request_deferred_save", source)
        deferred_save_region = source[source.index("def request_deferred_save") : source.index("def save_current_item")]
        self.assertIn("self.get_content", deferred_save_region)
        self.assertIn("self.markrender_manager.save_content", deferred_save_region)
        self.assertNotIn("send_message_sync", deferred_save_region)
        self.assertNotIn("while", deferred_save_region)

    def test_deferred_save_requests_are_coalesced_by_qtimer(self):
        source = read_project_file("app", "editor", "editor.py")

        self.assertIn("self._deferred_save_timer = QTimer()", source)
        self.assertIn("self._deferred_save_timer.setSingleShot(True)", source)
        self.assertIn("self._deferred_save_timer.start", source)
        self.assertIn("def _flush_deferred_save", source)

    def test_navigation_save_forces_content_read_without_dirty_gate(self):
        panel_source = read_project_file("app", "quickpick", "panel.py")
        editor_source = read_project_file("app", "editor", "editor.py")

        save_current_item_body = panel_source[panel_source.index("def save_current_item") : panel_source.index("def _save_with_callback")]
        request_deferred_region = editor_source[editor_source.index("def request_deferred_save") : editor_source.index("def _flush_deferred_save")]

        self.assertIn("request_deferred_save(force=True, callback=handle_deferred_save_done)", save_current_item_body)
        self.assertIn("def request_deferred_save(self, force=False, callback=None):", request_deferred_region)
        self.assertIn("if not force and not (self.content_changed and self.item.item_id):", request_deferred_region)
        self.assertIn("if force:", request_deferred_region)
        self.assertIn("self._flush_deferred_save(callback=callback)", request_deferred_region)

    def test_quickpick_executes_switch_only_after_deferred_save_callback(self):
        panel_source = read_project_file("app", "quickpick", "panel.py")
        save_current_item_body = panel_source[panel_source.index("def save_current_item") : panel_source.index("def _save_with_callback")]

        self.assertIn("def handle_deferred_save_done(save_success):", save_current_item_body)
        self.assertIn("if save_success:", save_current_item_body)
        self.assertIn("self._execute_switch()", save_current_item_body)
        self.assertIn("return", save_current_item_body)

    def test_navigation_save_reads_editor_item_id_instead_of_item_object_truthiness(self):
        panel_source = read_project_file("app", "quickpick", "panel.py")
        save_current_item_body = panel_source[
            panel_source.index("def save_current_item") : panel_source.index("def _save_with_callback")
        ]

        self.assertIn("editor_item = getattr(editor, 'item', None)", save_current_item_body)
        self.assertIn("editor_item_id = getattr(editor_item, 'item_id', '')", save_current_item_body)
        self.assertNotIn("editor_item_id = getattr(editor, 'item', '')", save_current_item_body)

    def test_deferred_save_reads_and_saves_only_matching_item_id(self):
        source = read_project_file("app", "editor", "editor.py")

        flush_region = source[source.index("def _flush_deferred_save") : source.index("def save_current_item")]
        get_content_region = source[source.index("def get_content") : source.index("def get_content_with_retry")]

        self.assertIn("frontend_item_id = parsed_data.get('item_id', item_id)", flush_region)
        self.assertIn("frontend_item_id != item_id", flush_region)
        self.assertIn("self.get_content(handle_content_response, item_id=item_id)", flush_region)
        self.assertIn("def get_content(self, callback, item_id=None):", get_content_region)
        self.assertIn("target_item_id = item_id or self.item.item_id", get_content_region)
        self.assertIn("item_id=target_item_id", get_content_region)

    def test_get_content_timeout_timer_has_editor_owned_lifetime(self):
        source = read_project_file("app", "editor", "editor.py")
        get_content_region = source[source.index("def get_content") : source.index("def get_content_with_retry")]

        self.assertIn("self._content_timeout_timers = []", source)
        self.assertIn("timeout_timer = QTimer(self)", get_content_region)
        self.assertIn("self._content_timeout_timers.append(timeout_timer)", get_content_region)
        self.assertIn("self._content_timeout_timers.remove(timeout_timer)", get_content_region)
        self.assertIn("'item_id': target_item_id", get_content_region)

    def test_deferred_and_close_paths_retry_disk_sync_even_when_database_content_matches(self):
        editor_source = read_project_file("app", "editor", "editor.py")
        main_source = read_project_file("main.py")
        flush_region = editor_source[editor_source.index("def _flush_deferred_save") : editor_source.index("def flush_pending_deferred_save")]
        close_region = main_source[main_source.index("def _perform_save_on_close") : main_source.index("# 移除自定义的窗口拖动功能")]

        self.assertIn("if content != old_content or self.content_changed:", flush_region)
        self.assertIn("if content != old_content or self.editor.content_changed:", close_region)

    def test_auto_save_uses_captured_item_id_and_preserves_dirty_on_stale_or_not_ready(self):
        source = read_project_file("app", "editor", "editor.py")
        auto_save_region = source[source.index("def _auto_save_history") : source.index("def _reset_frontend_state")]

        self.assertIn("target_item_id = self.item.item_id", auto_save_region)
        self.assertIn("target_generation = self._content_change_generation", auto_save_region)
        self.assertIn("self.get_content(handle_content_response, item_id=target_item_id)", auto_save_region)
        self.assertIn("frontend_item_id = parsed_data.get('item_id', target_item_id)", auto_save_region)
        self.assertIn("frontend_item_id != target_item_id", auto_save_region)
        self.assertIn("self.content_changed = True", auto_save_region)
        self.assertIn("self._mark_auto_save_clean(target_generation)", auto_save_region)

    def test_close_save_blocks_close_when_frontend_not_ready(self):
        source = read_project_file("main.py")
        close_region = source[source.index("def closeEvent") : source.index("def handle_close_button")]

        self.assertIn("save_completed = self._perform_save_on_close()", close_region)
        self.assertIn("if not save_completed:", close_region)
        self.assertIn("event.ignore()", close_region)
        self.assertIn("return", close_region)
        self.assertIn("return False", close_region)

    def test_close_save_flushes_pending_deferred_save_before_current_item(self):
        source = read_project_file("main.py")
        close_region = source[source.index("def _perform_save_on_close") : source.index("# 移除自定义的窗口拖动功能")]

        self.assertIn("flush_pending_deferred_save", close_region)
        self.assertIn("if not self.editor.flush_pending_deferred_save(timeout_ms=3000):", close_region)
        self.assertIn("return False", close_region)


class TestQuickPickTreePerformanceContract(unittest.TestCase):
    def test_lightweight_tree_excludes_full_content_but_detail_keeps_it(self):
        try:
            from db.markrender_manager import MarkRenderManager
        except ModuleNotFoundError as exc:
            if exc.name == "sqlalchemy":
                self.skipTest("SQLAlchemy is required for QuickPick tree contract tests")
            raise

        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        os.environ["MARKDOWN_RENDER_DATA"] = temp_dir.name
        self.addCleanup(lambda: os.environ.pop("MARKDOWN_RENDER_DATA", None))
        manager = MarkRenderManager(
            db_path=os.path.join(temp_dir.name, "quickpick_contract.db")
        )

        parent_id = manager.save_item(
            title="Folder",
            content="folder body should not be loaded into tree",
            is_folder=1,
            order=1,
        )
        child_id = manager.save_item(
            title="Child",
            content="large child body should only be loaded by get_detail",
            parent_id=parent_id,
            order=2,
        )

        tree = manager.get_lightweight_tree()

        def assert_tree_is_lightweight(nodes):
            for node in nodes:
                self.assertNotIn("content", node)
                self.assertNotIn("page_settings", node)
                self.assertIn("content_md5", node)
                assert_tree_is_lightweight(node.get("children", []))

        assert_tree_is_lightweight(tree)
        self.assertEqual(
            manager.get_detail(child_id)["content"],
            "large child body should only be loaded by get_detail",
        )

    def test_lightweight_tree_is_built_from_one_query_not_recursive_children_calls(self):
        source = read_project_file("db", "markrender_manager.py")

        self.assertIn("def get_lightweight_tree", source)
        lightweight_region = source[source.index("def get_lightweight_tree") : source.index("def delete_node")]
        self.assertIn("session.query", lightweight_region)
        self.assertNotIn("self.get_children", lightweight_region)

    def test_quickpick_load_uses_lightweight_tree_and_detail_only_for_body_actions(self):
        source = read_project_file("app", "quickpick", "panel.py")

        load_region = source[source.index("def load_quickpick_items") : source.index("def filter_quickpick")]
        self.assertIn("get_lightweight_tree", load_region)
        self.assertNotIn("get_full_tree", load_region)
        self.assertIn("get_detail", source)

    def test_search_input_uses_debounced_filtering(self):
        source = read_project_file("app", "quickpick", "panel.py")

        self.assertIn("self._filter_timer = QTimer(self)", source)
        self.assertIn("self._filter_timer.setSingleShot(True)", source)
        self.assertIn("def request_filter_quickpick", source)
        self.assertIn("self.search_input.textChanged.connect(self.request_filter_quickpick)", source)
        self.assertNotIn("self.search_input.textChanged.connect(self.filter_quickpick)", source)

    def test_drag_drop_setup_is_idempotent(self):
        source = read_project_file("app", "quickpick", "panel.py")

        drag_setup_region = source[source.index("def _setup_drag_drop_support") : source.index("def eventFilter")]
        self.assertIn("if getattr(self, '_drag_drop_setup', False):", drag_setup_region)
        self.assertIn("return", drag_setup_region)
        self.assertEqual(source.count("_setup_drag_drop_support()"), 1)


class TestDiskSyncAndHistoryContract(unittest.TestCase):
    def test_sync_write_localdisk_returns_true_and_writes_empty_file(self):
        try:
            from db.db_manager import get_user_data_dir
            from db.markrender_manager import MarkRenderManager
        except ModuleNotFoundError as exc:
            if exc.name == "sqlalchemy":
                self.skipTest("SQLAlchemy is required for disk sync contract tests")
            raise

        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        os.environ["MARKDOWN_RENDER_DATA"] = temp_dir.name
        self.addCleanup(lambda: os.environ.pop("MARKDOWN_RENDER_DATA", None))
        manager = MarkRenderManager(
            db_path=os.path.join(temp_dir.name, "disk_sync_contract.db")
        )

        result = manager.sync_write_localdisk(42, "", page_engine="markdown")

        output_path = os.path.join(get_user_data_dir(), "output", "42.md")
        self.assertTrue(result)
        self.assertTrue(os.path.exists(output_path))
        with open(output_path, "r", encoding="utf-8") as file:
            self.assertEqual(file.read(), "")

    def test_save_content_surfaces_disk_sync_failure(self):
        try:
            from db.markrender_manager import MarkRenderManager
        except ModuleNotFoundError as exc:
            if exc.name == "sqlalchemy":
                self.skipTest("SQLAlchemy is required for disk sync contract tests")
            raise

        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        os.environ["MARKDOWN_RENDER_DATA"] = temp_dir.name
        self.addCleanup(lambda: os.environ.pop("MARKDOWN_RENDER_DATA", None))
        manager = MarkRenderManager(
            db_path=os.path.join(temp_dir.name, "disk_failure_contract.db")
        )
        item_id = manager.save_item(title="Disk warning", content="old body")
        manager.sync_write_localdisk = lambda *args, **kwargs: False

        result = manager.save_content(item_id, "new body")

        self.assertFalse(result)

    def test_save_item_empty_content_updates_disk_to_empty_file(self):
        try:
            from db.db_manager import get_user_data_dir
            from db.markrender_manager import MarkRenderManager
        except ModuleNotFoundError as exc:
            if exc.name == "sqlalchemy":
                self.skipTest("SQLAlchemy is required for disk sync contract tests")
            raise

        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        os.environ["MARKDOWN_RENDER_DATA"] = temp_dir.name
        self.addCleanup(lambda: os.environ.pop("MARKDOWN_RENDER_DATA", None))
        manager = MarkRenderManager(
            db_path=os.path.join(temp_dir.name, "empty_sync_contract.db")
        )
        item_id = manager.save_item(title="Clearable", content="old body")

        manager.save_item(id=item_id, content="")

        output_path = os.path.join(get_user_data_dir(), "output", f"{item_id}.md")
        with open(output_path, "r", encoding="utf-8") as file:
            self.assertEqual(file.read(), "")

    def test_programmatic_load_path_does_not_persist_or_create_history(self):
        source = read_project_file("app", "editor", "editor.py")

        load_region = source[source.index("def set_current_item") : source.index("def request_deferred_save")]
        self.assertIn("self._loading_content = True", load_region)
        self.assertIn("self.content_changed = False", load_region)
        self.assertNotIn("save_content", load_region)
        self.assertNotIn("save_item", load_region)

    def test_user_autosave_remains_debounced_by_qtimer(self):
        source = read_project_file("app", "editor", "editor.py")

        self.assertIn("self.content_change_timer = QTimer()", source)
        self.assertIn("self.content_change_timer.setSingleShot(True)", source)
        self.assertIn("self.content_change_timer.stop()", source)
        self.assertIn("self.content_change_timer.start(1000)", source)


if __name__ == "__main__":
    unittest.main()
