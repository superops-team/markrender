#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试quickpick功能的修改
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from db.markrender_manager import MarkRenderManager

def test_quickpick_features():
    """测试quickpick功能"""
    print("开始测试quickpick功能...")
    
    # 创建MarkRenderManager实例
    manager = MarkRenderManager()
    
    # 创建带图标类型的文件夹
    print("1. 创建带图标类型的文件夹...")
    folder_id = manager.create_folder(
        title="测试文件夹",
        icon_type="folder",
        display_name="我的文件夹"
    )
    print(f"   创建文件夹，ID: {folder_id}")
    
    # 创建带图标类型的文件
    print("2. 创建带图标类型的文件...")
    file_id = manager.create_file(
        title="测试文件.md",
        content="# 测试内容\n\n这是测试文件的内容",
        page_type="markdown",
        icon_type="textarea",
        display_name="我的Markdown文件"
    )
    print(f"   创建文件，ID: {file_id}")
    
    # 获取树形结构
    print("3. 获取树形结构...")
    tree = manager.get_full_tree()
    
    # 查找我们创建的项目
    test_folder = None
    test_file = None
    for item in tree:
        if item['id'] == folder_id:
            test_folder = item
        if item['id'] == file_id:
            test_file = item
    
    if test_folder:
        print(f"   文件夹: {test_folder['title']}, 图标类型: {test_folder.get('icon_type')}, 显示名称: {test_folder.get('display_name')}")
    if test_file:
        print(f"   文件: {test_file['title']}, 图标类型: {test_file.get('icon_type')}, 显示名称: {test_file.get('display_name')}, 内容类型: {test_file.get('page_type')}")
    
    print("测试完成!")

if __name__ == "__main__":
    # 初始化QApplication（某些功能可能需要）
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    test_quickpick_features()