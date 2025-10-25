#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试使用Bootstrap Icons
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.markrender_manager import MarkRenderManager

def test_bootstrap_icons():
    """测试使用Bootstrap Icons"""
    print("开始测试Bootstrap Icons...")
    
    # 创建MarkRenderManager实例
    manager = MarkRenderManager()
    
    # 创建使用Bootstrap Icons的文件夹
    print("1. 创建使用Bootstrap Icons的文件夹...")
    folder_id = manager.create_folder(
        title="Bootstrap文件夹",
        icon_type="folder",  # 保留原有图标类型
        icon_path="icons/folder.svg",  # 使用Bootstrap Icons中的folder图标
        display_name="Bootstrap文件夹"
    )
    print(f"   创建文件夹，ID: {folder_id}")
    
    # 创建使用Bootstrap Icons的文件
    print("2. 创建使用Bootstrap Icons的文件...")
    file_id = manager.create_file(
        title="Bootstrap文件.md",
        content="# Bootstrap测试\n\n这是使用Bootstrap Icons的测试文件",
        page_type="markdown",
        icon_type="textarea",  # 保留原有图标类型
        icon_path="icons/file-earmark-text.svg",  # 使用Bootstrap Icons中的文本文件图标
        display_name="Bootstrap Markdown文件"
    )
    print(f"   创建文件，ID: {file_id}")
    
    # 创建使用不同Bootstrap Icons的文件
    print("3. 创建使用不同Bootstrap Icons的文件...")
    excalidraw_id = manager.create_file(
        title="Bootstrap画布",
        content="{}",  # Excalidraw内容
        page_type="excalidraw",
        icon_type="excalidraw",  # 保留原有图标类型
        icon_path="icons/palette.svg",  # 使用Bootstrap Icons中的调色板图标
        display_name="Bootstrap画布文件"
    )
    print(f"   创建Excalidraw文件，ID: {excalidraw_id}")
    
    # 获取树形结构
    print("4. 获取树形结构...")
    tree = manager.get_full_tree()
    
    # 查找我们创建的项目
    test_folder = None
    test_file = None
    test_excalidraw = None
    
    # 遍历所有项目查找我们创建的
    def find_items(items):
        nonlocal test_folder, test_file, test_excalidraw
        for item in items:
            if item['id'] == folder_id:
                test_folder = item
            if item['id'] == file_id:
                test_file = item
            if item['id'] == excalidraw_id:
                test_excalidraw = item
            # 递归查找子项
            if 'children' in item and item['children']:
                find_items(item['children'])
    
    find_items(tree)
    
    if test_folder:
        print(f"   文件夹: {test_folder['title']}, 图标路径: {test_folder.get('icon_path')}")
    if test_file:
        print(f"   Markdown文件: {test_file['title']}, 图标路径: {test_file.get('icon_path')}")
    if test_excalidraw:
        print(f"   Excalidraw文件: {test_excalidraw['title']}, 图标路径: {test_excalidraw.get('icon_path')}")
    
    print("Bootstrap Icons测试完成!")

if __name__ == "__main__":
    test_bootstrap_icons()