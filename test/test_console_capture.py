#!/usr/bin/env python3
"""
测试控制台日志捕获功能
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
sys.modules['PySide6.QtWebEngineWidgets'] = types.ModuleType('QtWebEngineWidgets')
sys.modules['PySide6.QtWebEngineCore'] = types.ModuleType('QtWebEngineCore')

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
mock_db.db_manager = types.ModuleType('db_manager')
sys.modules['db'] = mock_db
sys.modules['db.db_manager'] = mock_db.db_manager

# Mock db.base
mock_db_base = types.ModuleType('base')
mock_db_base.Base = type('Base', (), {})
sys.modules['db.base'] = mock_db_base

# Mock enum
sys.modules['enum'] = types.ModuleType('enum')

# Mock app.editor.js_scripts
mock_js_scripts = types.ModuleType('js_scripts')
sys.modules['app.editor.js_scripts'] = mock_js_scripts

def test_console_capture():
    """测试控制台日志捕获功能"""
    print("测试控制台日志捕获功能...")
    
    # 直接测试CustomWebEnginePage类
    from app.editor.webengine import CustomWebEnginePage
    
    # 创建CustomWebEnginePage实例
    page = CustomWebEnginePage()
    page.page_type = "test-page"
    
    # 模拟JavaScript控制台消息
    print("\n1. 测试Info级别消息:")
    page._on_javascript_console_message(
        0,  # InfoMessageLevel
        "This is an info message",
        10,
        "test.js"
    )
    
    print("\n2. 测试Warning级别消息:")
    page._on_javascript_console_message(
        1,  # WarningMessageLevel
        "This is a warning message",
        20,
        "test.js"
    )
    
    print("\n3. 测试Error级别消息:")
    page._on_javascript_console_message(
        2,  # ErrorMessageLevel
        "This is an error message",
        30,
        "test.js"
    )
    
    print("\n4. 测试Debug级别消息:")
    page._on_javascript_console_message(
        3,  # OtherMessageLevel (treated as debug)
        "This is a debug message",
        40,
        "test.js"
    )
    
    print("\n5. 测试无页面类型的消息:")
    page.page_type = None
    page._on_javascript_console_message(
        0,  # InfoMessageLevel
        "This is a message without page type",
        50,
        "test.js"
    )

if __name__ == "__main__":
    test_console_capture()