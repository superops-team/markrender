#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行所有测试用例的脚本
"""

import sys
import os
import unittest

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_all_tests():
    """运行所有测试用例"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加所有测试用例
    test_modules = [
        'test.test_webpage_manager',
        'test.test_backend_interface',
        'test.test_excalidraw_utils',
        'test.test_page_switching'
    ]
    
    for module_name in test_modules:
        try:
            module = __import__(module_name, fromlist=[''])
            suite.addTests(loader.loadTestsFromModule(module))
            print(f"✓ 已加载测试模块: {module_name}")
        except ImportError as e:
            print(f"✗ 无法导入测试模块: {module_name} - {e}")
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回测试结果
    return result.wasSuccessful()

if __name__ == '__main__':
    print("开始运行所有测试用例...")
    print("=" * 50)
    
    success = run_all_tests()
    
    print("=" * 50)
    if success:
        print("✅ 所有测试通过!")
        sys.exit(0)
    else:
        print("❌ 部分测试失败!")
        sys.exit(1)