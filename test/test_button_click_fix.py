#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试按钮点击修复
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from app.quickpick.panel import QuickPickPanel
from db.markrender_manager import MarkRenderManager

def test_button_click_fix():
    """测试按钮点击修复"""
    print("开始测试按钮点击修复...")
    
    # 创建 QApplication 实例
    app = QApplication(sys.argv)
    
    # 创建 MarkRenderManager 实例
    manager = MarkRenderManager()
    
    # 创建 QuickPickPanel 实例
    panel = QuickPickPanel(manager)
    
    # 测试方法是否存在
    methods_to_test = [
        'show_add_menu',
        'show_more_menu'
    ]
    
    print("测试方法是否存在:")
    for method_name in methods_to_test:
        if hasattr(panel, method_name):
            print(f"  ✓ {method_name} 方法存在")
        else:
            print(f"  ✗ {method_name} 方法不存在")
    
    print("按钮点击修复测试完成!")

if __name__ == "__main__":
    test_button_click_fix()