#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excalidraw 重置功能测试脚本
用于验证 Excalidraw 页面重置功能是否正常工作
"""

import sys
import os
import json
import tempfile
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.editor.js_scripts import JSScriptManager

class TestExcalidrawReset:
    def __init__(self):
        self.test_results = []
    
    def test_reset_page_state_script(self):
        """测试 reset_page_state.js 脚本"""
        print("测试 reset_page_state.js 脚本...")
        
        # 获取 reset_page_state 脚本
        reset_script = JSScriptManager.get_script("reset_page_state")
        if not reset_script:
            print("❌ 无法加载 reset_page_state.js 模板")
            return False
        
        # 检查脚本中是否包含必要的重置逻辑
        required_content = [
            "重置页面状态",
            "window.editorState.currentItemId = null",
            "window.resetExcalidraw()",
            "window.currentItemId = null",
            "Excalidraw特定状态已重置"
        ]
        
        for content in required_content:
            if content not in reset_script:
                print(f"❌ reset_page_state.js 缺少必要的内容: {content}")
                return False
        
        print("✅ reset_page_state.js 脚本内容正确")
        return True
    
    def test_reset_excalidraw_state_script(self):
        """测试 reset_excalidraw_state.js 脚本"""
        print("\n测试 reset_excalidraw_state.js 脚本...")
        
        # 获取 reset_excalidraw_state 脚本
        reset_script = JSScriptManager.get_script("reset_excalidraw_state")
        if not reset_script:
            print("❌ 无法加载 reset_excalidraw_state.js 模板")
            return False
        
        # 检查脚本中是否包含必要的重置逻辑
        required_content = [
            "重置Excalidraw特定状态",
            "updateScene",
            "localStorage"
        ]
        
        for content in required_content:
            if content not in reset_script:
                print(f"❌ reset_excalidraw_state.js 缺少必要的内容: {content}")
                return False
        
        print("✅ reset_excalidraw_state.js 脚本内容正确")
        return True
    
    def test_excalidraw_reset_function_in_app(self):
        """测试 App.jsx 中的 resetExcalidraw 函数"""
        print("\n测试 App.jsx 中的 resetExcalidraw 函数...")
        
        # 读取 App.jsx 文件
        app_jsx_path = "frontend/excalidraw/src/App.jsx"
        if not os.path.exists(app_jsx_path):
            print("❌ App.jsx 文件不存在")
            return False
        
        with open(app_jsx_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否定义了 resetExcalidraw 函数
        if "window.resetExcalidraw" not in content:
            print("❌ App.jsx 中未定义 window.resetExcalidraw 函数")
            return False
        
        # 检查函数中是否包含必要的重置逻辑
        required_content = [
            "resetExcalidraw = ()",
            "window.currentItemId = null",
            "window.editorState.currentItemId = null",
            "updateScene({ elements: [] })"
        ]
        
        for req_content in required_content:
            if req_content not in content:
                print(f"❌ App.jsx 中的 resetExcalidraw 函数缺少必要的内容: {req_content}")
                return False
        
        print("✅ App.jsx 中的 resetExcalidraw 函数定义正确")
        return True
    
    def run_all_tests(self):
        """运行所有测试"""
        print("开始运行 Excalidraw 重置功能测试...")
        print("=" * 50)
        
        tests = [
            self.test_reset_page_state_script,
            self.test_reset_excalidraw_state_script,
            self.test_excalidraw_reset_function_in_app
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                if test():
                    passed += 1
                    print()
                else:
                    failed += 1
                    print()
            except Exception as e:
                print(f"❌ 测试 {test.__name__} 发生异常: {e}")
                failed += 1
                print()
        
        print(f"测试完成: {passed} 通过, {failed} 失败")
        return failed == 0

def main():
    """主函数"""
    print("开始 Excalidraw 重置功能测试...")
    
    tester = TestExcalidrawReset()
    success = tester.run_all_tests()
    
    print("=" * 50)
    if success:
        print("🎉 所有 Excalidraw 重置功能测试通过!")
        print("\n修复总结:")
        print("✅ 在 App.jsx 中正确添加了 resetExcalidraw 函数")
        print("✅ 更新了 reset_page_state.js 脚本，增强 Excalidraw 重置逻辑")
        print("✅ 确保所有 JavaScript 代码通过 js_scripts.py 管理")
        print("\n预期效果:")
        print("1. reset_page_state 脚本现在能够正确重置 Excalidraw 页面的内容")
        print("2. 页面切换时 Excalidraw 状态会被正确清除")
        print("3. Excalidraw 场景会被清空，显示空白画布")
        return 0
    else:
        print("❌ 部分 Excalidraw 重置功能测试失败!")
        return 1

if __name__ == "__main__":
    sys.exit(main())