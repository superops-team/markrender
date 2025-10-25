#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试添加子节点功能
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db.markrender_manager import MarkRenderManager


def test_add_child_nodes():
    """测试添加子节点功能"""
    print("测试添加子节点功能...")
    
    # 创建数据库管理器
    manager = MarkRenderManager()
    
    # 创建根文件夹
    print("创建根文件夹...")
    root_folder_id = manager.create_folder("测试根文件夹")
    print(f"创建根文件夹，ID: {root_folder_id}")
    
    # 在根文件夹中创建子文件夹
    print("在根文件夹中创建子文件夹...")
    sub_folder_id = manager.create_folder("子文件夹1", parent_id=root_folder_id)
    print(f"在根文件夹中创建子文件夹，ID: {sub_folder_id}")
    
    # 在子文件夹中创建 Markdown 文件
    print("在子文件夹中创建 Markdown 文件...")
    markdown_file_id = manager.create_file(
        "测试 Markdown 文件", 
        "# 这是测试内容\n\n这是 Markdown 文件的内容。", 
        parent_id=sub_folder_id, 
        page_type="markdown"
    )
    print(f"在子文件夹中创建 Markdown 文件，ID: {markdown_file_id}")
    
    # 在子文件夹中创建 Excalidraw 文件
    print("在子文件夹中创建 Excalidraw 文件...")
    excalidraw_file_id = manager.create_file(
        "测试 Excalidraw 文件", 
        '{"elements":[],"appState":{}}', 
        parent_id=sub_folder_id, 
        page_type="excalidraw",
        page_engine="excalidraw"
    )
    print(f"在子文件夹中创建 Excalidraw 文件，ID: {excalidraw_file_id}")
    
    # 获取完整的树形结构
    print("\n获取完整的树形结构...")
    tree_data = manager.get_full_tree()
    print("树形结构数据:")
    
    def print_tree(items, level=0):
        """递归打印树形结构"""
        for item in items:
            indent = "  " * level
            folder_indicator = "[文件夹] " if item['is_folder'] else ""
            print(f"{indent}- {folder_indicator}{item['title']} (ID: {item['id']})")
            if 'children' in item and item['children']:
                print_tree(item['children'], level + 1)
    
    print_tree(tree_data)
    
    print("\n测试完成!")


if __name__ == "__main__":
    test_add_child_nodes()