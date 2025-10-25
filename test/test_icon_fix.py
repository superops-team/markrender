#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试图标路径修复功能
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.quickpick.item import QuickPickItemDelegate
from utils.path import get_icon_path

def test_icon_path_resolution():
    """测试图标路径解析"""
    print("测试图标路径解析...")
    
    # 创建应用实例
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # 创建委托实例
    delegate = QuickPickItemDelegate()
    
    # 测试相对路径图标
    print("\n1. 测试相对路径图标:")
    relative_icon_path = "icons/palette.svg"
    icon = delegate._get_icon_for_file_type("test", icon_path=relative_icon_path)
    print(f"   图标路径: {relative_icon_path}")
    print(f"   图标对象: {icon}")
    print(f"   图标是否为空: {icon.isNull()}")
    
    # 测试绝对路径图标
    print("\n2. 测试绝对路径图标:")
    absolute_icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "icons", "folder.svg")
    icon = delegate._get_icon_for_file_type("test", icon_path=absolute_icon_path)
    print(f"   图标路径: {absolute_icon_path}")
    print(f"   图标对象: {icon}")
    print(f"   图标是否为空: {icon.isNull()}")
    
    # 测试不存在的图标
    print("\n3. 测试不存在的图标:")
    non_existent_icon_path = "icons/non-existent.svg"
    icon = delegate._get_icon_for_file_type("test", icon_path=non_existent_icon_path)
    print(f"   图标路径: {non_existent_icon_path}")
    print(f"   图标对象: {icon}")
    print(f"   图标是否为空: {icon.isNull()}")
    
    # 测试默认图标类型
    print("\n4. 测试默认图标类型:")
    icon = delegate._get_icon_for_file_type("markdown")
    print(f"   文件类型: markdown")
    print(f"   图标对象: {icon}")
    print(f"   图标是否为空: {icon.isNull()}")
    
    print("\n测试完成!")

if __name__ == "__main__":
    test_icon_path_resolution()