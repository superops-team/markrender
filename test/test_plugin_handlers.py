#!/usr/bin/env python3
"""
测试插件处理器功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock需要的模块
import types
import sys

# Mock PySide6模块
sys.modules['PySide6'] = types.ModuleType('PySide6')
sys.modules['PySide6.QtCore'] = types.ModuleType('QtCore')
sys.modules['PySide6.QtWidgets'] = types.ModuleType('QtWidgets')

# Mock SQLAlchemy
sys.modules['sqlalchemy'] = types.ModuleType('sqlalchemy')
sys.modules['sqlalchemy.sql'] = types.ModuleType('sqlalchemy.sql')
sys.modules['sqlalchemy.sql'] = types.ModuleType('sqlalchemy.sql')
sys.modules['sqlalchemy.sql.func'] = types.ModuleType('sqlalchemy.sql.func')
sys.modules['sqlalchemy.sql.func'].now = lambda: None

# Mock utils模块
import logging
class MockLogger:
    def error(self, msg):
        print(f"ERROR: {msg}")
    def warning(self, msg):
        print(f"WARNING: {msg}")
    def info(self, msg):
        print(f"INFO: {msg}")
    def debug(self, msg):
        print(f"DEBUG: {msg}")

# 创建mock的utils模块
mock_utils = types.ModuleType('utils')
mock_utils.logger = MockLogger()
sys.modules['utils'] = mock_utils

# Mock db模块
mock_db = types.ModuleType('db')
mock_db.markrender_manager = types.ModuleType('markrender_manager')
sys.modules['db'] = mock_db
sys.modules['db.markrender_manager'] = mock_db.markrender_manager

# Mock db.base
mock_db_base = types.ModuleType('base')
mock_db_base.Base = type('Base', (), {})
sys.modules['db.base'] = mock_db_base

# Mock enum
sys.modules['enum'] = types.ModuleType('enum')

# Mock jinja2
sys.modules['jinja2'] = types.ModuleType('jinja2')
from jinja2 import Environment, FileSystemLoader, Undefined

def test_plugin_handlers():
    """测试插件处理器功能"""
    print("测试插件处理器功能...")
    
    # 直接测试JSScriptManager
    from app.editor.js_scripts import JSScriptManager
    
    # 测试获取Markdown插件的getContent脚本
    print("\n1. 测试获取Markdown插件的getContent脚本:")
    script = JSScriptManager.get_script("getContent", page_type="markdown")
    if script:
        print("✓ 成功获取Markdown插件的getContent脚本")
        print(f"  脚本长度: {len(script)} 字符")
        # 检查是否包含Markdown特定的内容
        if "Cherry编辑器" in script:
            print("  ✓ 脚本包含Markdown特定逻辑")
        else:
            print("  ✗ 脚本可能不包含Markdown特定逻辑")
    else:
        print("✗ 获取Markdown插件的getContent脚本失败")
    
    # 测试获取Excalidraw插件的getContent脚本
    print("\n2. 测试获取Excalidraw插件的getContent脚本:")
    script = JSScriptManager.get_script("getContent", page_type="excalidraw")
    if script:
        print("✓ 成功获取Excalidraw插件的getContent脚本")
        print(f"  脚本长度: {len(script)} 字符")
        # 检查是否包含Excalidraw特定的内容
        if "Excalidraw" in script:
            print("  ✓ 脚本包含Excalidraw特定逻辑")
        else:
            print("  ✗ 脚本可能不包含Excalidraw特定逻辑")
    else:
        print("✗ 获取Excalidraw插件的getContent脚本失败")
    
    # 测试获取Markdown插件的setValue脚本
    print("\n3. 测试获取Markdown插件的setValue脚本:")
    script = JSScriptManager.get_script("setValue", page_type="markdown", content="# Test", item_id="test-id")
    if script:
        print("✓ 成功获取Markdown插件的setValue脚本")
        print(f"  脚本长度: {len(script)} 字符")
    else:
        print("✗ 获取Markdown插件的setValue脚本失败")
    
    # 测试获取Excalidraw插件的setValue脚本
    print("\n4. 测试获取Excalidraw插件的setValue脚本:")
    script = JSScriptManager.get_script("setValue", page_type="excalidraw", content="[]", item_id="test-id")
    if script:
        print("✓ 成功获取Excalidraw插件的setValue脚本")
        print(f"  脚本长度: {len(script)} 字符")
    else:
        print("✗ 获取Excalidraw插件的setValue脚本失败")
    
    # 测试获取不存在页面类型的脚本（应该回退到通用脚本）
    print("\n5. 测试获取不存在页面类型的脚本:")
    script = JSScriptManager.get_script("getContent", page_type="unknown")
    if script:
        print("✓ 成功获取通用getContent脚本（回退）")
        print(f"  脚本长度: {len(script)} 字符")
    else:
        print("✗ 获取通用getContent脚本失败")

if __name__ == "__main__":
    test_plugin_handlers()