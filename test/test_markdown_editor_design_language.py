#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


def read_project_file(*parts):
    with open(os.path.join(PROJECT_ROOT, *parts), "r", encoding="utf-8") as file:
        return file.read()


def function_region(source, function_name, next_function_name=None):
    start = source.index(f"def {function_name}")
    if next_function_name:
        end = source.index(f"def {next_function_name}", start)
    else:
        end = len(source)
    return source[start:end]


class TestSemanticTokenContract(unittest.TestCase):
    def test_style_constants_define_editor_semantic_tokens(self):
        source = read_project_file("app", "preference", "style_constants.py")

        required_names = [
            "SURFACE_BASE",
            "SURFACE_SUBTLE",
            "SURFACE_MUTED",
            "SURFACE_HOVER",
            "SURFACE_SELECTED",
            "BORDER_SUBTLE",
            "BORDER_DEFAULT",
            "BORDER_ACCENT",
            "TEXT_PRIMARY",
            "TEXT_SECONDARY",
            "TEXT_MUTED",
            "TEXT_DISABLED",
            "ACCENT",
            "ACCENT_HOVER",
            "ACCENT_ACTIVE",
            "ACCENT_SOFT",
            "FOCUS_BORDER",
            "FOCUS_SHADOW",
        ]

        missing = [name for name in required_names if f"{name} =" not in source]
        self.assertEqual(missing, [])

    def test_app_style_primary_paths_use_semantic_helpers(self):
        source = read_project_file("app", "preference", "app_style.py")

        self.assertIn("def get_quickpick_create_button", source)
        self.assertIn("return LINE_EDIT", function_region(source, "get_line_edit", "get_sidebar"))
        self.assertIn("return SIDEBAR_BUTTON", function_region(source, "get_sidebar_button_style", "get_dialog_border_radius"))

        for region_name, end_name in [
            ("get_line_edit", "get_sidebar"),
            ("get_sidebar_button_style", "get_dialog_border_radius"),
            ("get_quickpick_panel", "get_format_label"),
        ]:
            region = function_region(source, region_name, end_name)
            for legacy_color in ["#0052d9", "#0d6efd", "#3582fb"]:
                self.assertNotIn(legacy_color, region)

    def test_qt_focus_styles_do_not_use_unsupported_outline(self):
        source = read_project_file("app", "preference", "app_style.py")
        line_edit_region = function_region(source, "get_line_edit", "get_sidebar")

        self.assertNotIn("outline:", line_edit_region)

    def test_maximize_button_has_one_authoritative_definition(self):
        source = read_project_file("app", "preference", "app_style.py")

        self.assertEqual(source.count("\nMAXIMIZE_BUTTON ="), 1)


class TestQuickPickCreateAndStateContract(unittest.TestCase):
    def test_primary_create_button_opens_complete_menu(self):
        source = read_project_file("app", "quickpick", "panel.py")
        init_ui_region = function_region(source, "init_ui", "edit_item")
        menu_region = function_region(source, "show_create_menu", "create_new_markdown_item")

        self.assertIn("self.new_btn.clicked.connect(self.show_create_menu)", init_ui_region)
        self.assertNotIn("self.new_btn.clicked.connect(self.create_new_folder_item)", init_ui_region)
        self.assertIn('self.new_btn.setToolTip("新建")', init_ui_region)
        self.assertIn("self.app_style.get_quickpick_create_button()", init_ui_region)

        self.assertIn("create_new_markdown_item", menu_region)
        self.assertIn("create_new_board_item", menu_region)
        self.assertIn("create_new_folder_item", menu_region)

    def test_quickpick_qss_does_not_own_item_state_backgrounds(self):
        source = read_project_file("app", "preference", "app_style.py")
        region = function_region(source, "get_quickpick_panel", "get_format_label")
        constants_source = read_project_file("app", "preference", "style_constants.py")

        self.assertNotIn("QTreeWidget::item:selected", region)
        self.assertNotIn("QTreeWidget::item:hover", region)
        self.assertIn("QUICKPICK_PANEL_BASE", region)
        self.assertIn("QTreeWidget::branch", constants_source)

    def test_delegate_has_current_marker_and_quieter_items(self):
        source = read_project_file("app", "quickpick", "item.py")

        self.assertIn("CURRENT_MARKER_WIDTH", source)
        self.assertIn("drawRect", source)
        self.assertIn("icon_bg_width = 28", source)
        self.assertIn("icon_bg_height = 28", source)
        self.assertNotIn("drawLine(option_rect.left()", source)
        self.assertIn("return QSize(option.rect.width(), 52)", source)


class TestMarkdownRuntimeThemeBridgeContract(unittest.TestCase):
    def test_index_loads_markrender_theme_after_cherry_css(self):
        html = read_project_file("app", "editor", "plugins", "markdown", "index.html")

        cherry_index = html.index("cherry-markdown.min.css")
        theme_index = html.index("markrender-theme.css")
        self.assertLess(cherry_index, theme_index)
        self.assertIn("background: var(--mr-surface-base)", html)
        self.assertNotIn("background: #ffffff", html)

    def test_markrender_theme_bridge_maps_cherry_variables(self):
        theme = read_project_file("app", "editor", "plugins", "markdown", "assets", "markrender-theme.css")

        for expected in [
            "--mr-surface-base",
            "--mr-text-primary",
            "--mr-border-subtle",
            "--mr-accent",
            "--primary-color: var(--mr-accent)",
            "--base-font-color: var(--mr-text-primary)",
            "--base-border-color: var(--mr-border-subtle)",
            "--base-editor-bg: var(--mr-surface-base)",
            "--base-previewer-bg: var(--mr-surface-base)",
            "--toolbar-bg: var(--mr-surface-base)",
        ]:
            self.assertIn(expected, theme)

    def test_markdown_typography_and_toolbar_overrides_are_present(self):
        theme = read_project_file("app", "editor", "plugins", "markdown", "assets", "markrender-theme.css")

        self.assertIn(".cherry-markdown", theme)
        self.assertIn("word-break: normal", theme)
        self.assertIn("overflow-wrap: break-word", theme)
        self.assertIn("blockquote", theme)
        self.assertIn("border-left: 4px", theme)
        self.assertIn(".cherry-toolbar", theme)
        self.assertIn("box-shadow: none", theme)
        self.assertIn(".cherry-toolbar", theme)
        self.assertIn(".cherry-table", theme)
        self.assertNotIn("var(--color-error)", theme)


if __name__ == "__main__":
    unittest.main()
