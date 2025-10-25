#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全面测试图标路径修复功能
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.quickpick.item import QuickPickItemDelegate
from utils.path import get_icon_path

def test_comprehensive_icon_resolution():
    """全面测试图标路径解析"""
    print("全面测试图标路径解析...")
    
    # 创建应用实例
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # 创建委托实例
    delegate = QuickPickItemDelegate()
    
    # 测试1: 相对路径图标 (存在)
    print("\n1. 测试相对路径图标 (存在):")
    relative_icon_path = "icons/palette.svg"
    icon = delegate._get_icon_for_file_type("test", icon_path=relative_icon_path)
    print(f"   图标路径: {relative_icon_path}")
    print(f"   图标是否为空: {icon.isNull()}")
    if not icon.isNull():
        print(f"   图标尺寸: {icon.availableSizes()}")
    
    # 测试2: 相对路径图标 (存在)
    print("\n2. 测试相对路径图标 (存在):")
    relative_icon_path = "icons/folder.svg"
    icon = delegate._get_icon_for_file_type("test", icon_path=relative_icon_path)
    print(f"   图标路径: {relative_icon_path}")
    print(f"   图标是否为空: {icon.isNull()}")
    if not icon.isNull():
        print(f"   图标尺寸: {icon.availableSizes()}")
    
    # 测试3: 相对路径图标 (存在)
    print("\n3. 测试相对路径图标 (存在):")
    relative_icon_path = "icons/file-earmark-text.svg"
    icon = delegate._get_icon_for_file_type("test", icon_path=relative_icon_path)
    print(f"   图标路径: {relative_icon_path}")
    print(f"   图标是否为空: {icon.isNull()}")
    if not icon.isNull():
        print(f"   图标尺寸: {icon.availableSizes()}")
    
    # 测试4: 绝对路径图标
    print("\n4. 测试绝对路径图标:")
    absolute_icon_path = os.path.join(os.getcwd(), "icons", "textarea.svg")
    icon = delegate._get_icon_for_file_type("test", icon_path=absolute_icon_path)
    print(f"   图标路径: {absolute_icon_path}")
    print(f"   图标是否为空: {icon.isNull()}")
    if not icon.isNull():
        print(f"   图标尺寸: {icon.availableSizes()}")
    
    # 测试5: 不存在的图标
    print("\n5. 测试不存在的图标:")
    non_existent_icon_path = "icons/non-existent.svg"
    icon = delegate._get_icon_for_file_type("test", icon_path=non_existent_icon_path)
    print(f"   图标路径: {non_existent_icon_path}")
    print(f"   图标是否为空: {icon.isNull()}")
    
    # 测试6: 使用icon_type字段
    print("\n6. 测试icon_type字段:")
    icon = delegate._get_icon_for_file_type("test", icon_type="folder")
    print(f"   icon_type: folder")
    print(f"   图标是否为空: {icon.isNull()}")
    if not icon.isNull():
        print(f"   图标尺寸: {icon.availableSizes()}")
    
    # 测试7: 使用文件类型
    print("\n7. 测试文件类型:")
    icon = delegate._get_icon_for_file_type("markdown")
    print(f"   文件类型: markdown")
    print(f"   图标是否为空: {icon.isNull()}")
    if not icon.isNull():
        print(f"   图标尺寸: {icon.availableSizes()}")
    
    # 测试8: 缓存功能
    print("\n8. 测试缓存功能:")
    icon1 = delegate._get_icon_for_file_type("test", icon_path="icons/palette.svg")
    icon2 = delegate._get_icon_for_file_type("test", icon_path="icons/palette.svg")
    print(f"   第一次获取: {icon1}")
    print(f"   第二次获取: {icon2}")
    print(f"   是否为同一对象: {icon1 is icon2}")
    
    print("\n全面测试完成!")

if __name__ == "__main__":
    test_comprehensive_icon_resolution()