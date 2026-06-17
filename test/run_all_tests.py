#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行所有测试用例的脚本
"""

import sys
import os
import unittest
import argparse
import importlib.util

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEFAULT_TEST_MODULES = [
    'test.test_webpage_manager',
    'test.test_backend_interface',
    'test.test_excalidraw_utils',
    'test.test_page_switching'
]

TARGETED_TEST_MODULES = [
    'test.test_editor_data_navigation_performance',
    'test.test_markdown_editor_design_language',
    'test.test_packaging_configuration'
]


def _import_test_module(module_name):
    try:
        return __import__(module_name, fromlist=[''])
    except ModuleNotFoundError as import_error:
        relative_path = os.path.join(*module_name.split('.')) + '.py'
        module_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            relative_path,
        )
        if not os.path.exists(module_path):
            raise import_error

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


def run_all_tests(test_modules=None):
    """运行所有测试用例"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    if test_modules is None:
        test_modules = DEFAULT_TEST_MODULES
    import_errors = []
    
    for module_name in test_modules:
        try:
            module = _import_test_module(module_name)
            suite.addTests(loader.loadTestsFromModule(module))
            print(f"✓ 已加载测试模块: {module_name}")
        except ImportError as e:
            print(f"✗ 无法导入测试模块: {module_name} - {e}")
            import_errors.append((module_name, e))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if import_errors:
        print("\n导入失败的测试模块:")
        for module_name, error in import_errors:
            print(f"- {module_name}: {error}")
    if result.testsRun == 0:
        print("\n未执行任何测试。")
    
    # 返回测试结果
    return result.wasSuccessful() and not import_errors and result.testsRun > 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="运行 MarkRender 测试用例")
    parser.add_argument(
        '--targeted',
        action='store_true',
        help='仅运行当前优化变更相关的 targeted tests'
    )
    args = parser.parse_args()

    print("开始运行所有测试用例...")
    print("=" * 50)
    
    modules = TARGETED_TEST_MODULES if args.targeted else None
    success = run_all_tests(test_modules=modules)
    
    print("=" * 50)
    if success:
        print("✅ 所有测试通过!")
        sys.exit(0)
    else:
        print("❌ 部分测试失败!")
        sys.exit(1)
