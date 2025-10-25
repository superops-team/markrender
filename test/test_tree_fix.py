#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的树形结构功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from db.markrender_manager import MarkRenderManager

def test_tree_structure():
    """测试树形结构功能"""
    print("开始测试树形结构功能...")
    
    # 创建MarkRenderManager实例
    manager = MarkRenderManager()
    
    # 创建测试数据
    print("1. 创建根文件夹...")
    root_folder_id = manager.create_folder("测试根文件夹")
    print(f"   创建根文件夹，ID: {root_folder_id}")
    
    print("2. 在根文件夹下创建子文件夹...")
    sub_folder_id = manager.create_folder("子文件夹1", parent_id=root_folder_id)
    print(f"   创建子文件夹，ID: {sub_folder_id}")
    
    print("3. 在子文件夹下创建Markdown文件...")
    markdown_file_id = manager.create_file(
        title="测试Markdown文件",
        content="# 这是一个测试文件\n\n测试内容",
        parent_id=sub_folder_id,
        page_type='markdown'
    )
    print(f"   创建Markdown文件，ID: {markdown_file_id}")
    
    print("4. 在子文件夹下创建Excalidraw文件...")
    excalidraw_file_id = manager.create_file(
        title="测试Excalidraw文件",
        content="{}",  # Excalidraw内容通常是JSON格式
        parent_id=sub_folder_id,
        page_type='excalidraw',
        page_engine='excalidraw'
    )
    print(f"   创建Excalidraw文件，ID: {excalidraw_file_id}")
    
    print("5. 在根目录下创建文件...")
    root_file_id = manager.create_file(
        title="根目录文件",
        content="# 根目录文件\n\n这是根目录下的文件",
        parent_id=None,
        page_type='markdown'
    )
    print(f"   创建根目录文件，ID: {root_file_id}")
    
    print("6. 获取完整树形结构...")
    tree = manager.get_full_tree()
    print(f"   树形结构: {tree}")
    
    print("7. 测试删除功能...")
    # 删除根目录文件
    result = manager.delete_item(root_file_id)
    print(f"   删除根目录文件结果: {result}")
    
    print("测试完成!")

if __name__ == "__main__":
    # 初始化QApplication（某些功能可能需要）
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    test_tree_structure()