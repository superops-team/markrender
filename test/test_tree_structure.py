#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试树形结构功能
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db.markrender_manager import MarkRenderManager
from app.quickpick.panel import QuickPickPanel
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import sys


def test_tree_structure():
    """测试树形结构功能"""
    print("测试树形结构功能...")
    
    # 创建数据库管理器
    manager = MarkRenderManager()
    
    # 创建一些测试数据
    print("创建测试数据...")
    
    # 创建根文件夹
    folder1_id = manager.create_folder("文件夹1")
    print(f"创建文件夹1，ID: {folder1_id}")
    
    # 在文件夹1中创建文件
    file1_id = manager.create_file("文件1", "这是文件1的内容", parent_id=folder1_id, page_type="markdown")
    print(f"在文件夹1中创建文件1，ID: {file1_id}")
    
    # 创建另一个根文件夹
    folder2_id = manager.create_folder("文件夹2")
    print(f"创建文件夹2，ID: {folder2_id}")
    
    # 在文件夹2中创建文件
    file2_id = manager.create_file("文件2", "这是文件2的内容", parent_id=folder2_id, page_type="markdown")
    print(f"在文件夹2中创建文件2，ID: {file2_id}")
    
    # 创建根文件
    file3_id = manager.create_file("根文件", "这是根文件的内容", page_type="markdown")
    print(f"创建根文件，ID: {file3_id}")
    
    # 获取完整的树形结构
    print("\n获取完整的树形结构...")
    tree_data = manager.get_full_tree()
    print("树形结构数据:")
    for item in tree_data:
        print(f"  - {item['title']} (ID: {item['id']}, is_folder: {item['is_folder']})")
        if 'children' in item and item['children']:
            for child in item['children']:
                print(f"    - {child['title']} (ID: {child['id']}, is_folder: {child['is_folder']})")
    
    print("\n测试完成!")


if __name__ == "__main__":
    test_tree_structure()