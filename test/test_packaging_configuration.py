#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""打包配置回归测试。"""

import unittest
import ast
from pathlib import Path


class TestPackagingConfiguration(unittest.TestCase):
    def test_pyinstaller_collects_numpy_submodules(self):
        """PyInstaller 打包必须收集 numpy 子模块，避免启动时缺少 numpy._core.*。"""
        project_root = Path(__file__).resolve().parents[1]
        makefile = project_root / "Makefile"

        build_script = makefile.read_text(encoding="utf-8")

        self.assertIn(
            '--collect-submodules "numpy"',
            build_script,
            "打包配置缺少 numpy 子模块收集，可能导致 .app 启动即崩溃",
        )

    def test_import_dialog_does_not_import_markitdown_at_startup(self):
        """启动主窗口时不应立即导入 markitdown/magika/numpy 重依赖。"""
        project_root = Path(__file__).resolve().parents[1]
        import_dialog = project_root / "app" / "sidebar" / "import_dialog.py"

        source = import_dialog.read_text(encoding="utf-8")
        module = ast.parse(source)
        module_level_imports = [
            node
            for node in module.body
            if isinstance(node, (ast.Import, ast.ImportFrom))
        ]

        self.assertFalse(
            any(
                isinstance(node, ast.ImportFrom) and node.module == "markitdown"
                for node in module_level_imports
            ),
            "markitdown 应在真正转换文件时再懒加载，避免打包后启动路径因重依赖缺失而闪退",
        )

    def test_dmg_build_uses_non_interactive_hdiutil_packaging(self):
        """DMG 构建应避免依赖 Finder/AppleScript 卸载流程导致资源忙失败。"""
        project_root = Path(__file__).resolve().parents[1]
        makefile = project_root / "Makefile"

        build_script = makefile.read_text(encoding="utf-8")

        self.assertIn(
            "hdiutil create",
            build_script,
            "DMG 构建应使用非交互式 hdiutil create，避免 create-dmg 在自动化环境中卸载失败",
        )

    def test_pyinstaller_includes_editor_js_templates(self):
        """编辑器切换页面时依赖的 JS 模板必须进入 app bundle。"""
        project_root = Path(__file__).resolve().parents[1]
        makefile = project_root / "Makefile"

        build_script = makefile.read_text(encoding="utf-8")

        self.assertIn(
            '--add-data "app/editor/js_templates:app/editor/js_templates"',
            build_script,
            "打包配置缺少 app/editor/js_templates，会导致页面切换时 reset_page_state.js 找不到",
        )


if __name__ == "__main__":
    unittest.main()
