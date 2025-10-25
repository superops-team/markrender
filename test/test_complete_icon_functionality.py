#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整测试icon功能，包括Bootstrap Icons的使用
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.markrender_manager import MarkRenderManager

def test_complete_icon_functionality():
    """测试完整的图标功能"""
    print("开始测试完整的图标功能...")
    
    # 创建MarkRenderManager实例
    manager = MarkRenderManager()
    
    # 1. 测试创建带不同图标类型的文件夹
    print("1. 测试创建带不同图标类型的文件夹...")
    
    # 使用默认图标类型
    folder1_id = manager.create_folder(
        title="默认图标文件夹",
        icon_type="folder",
        display_name="默认文件夹"
    )
    print(f"   创建默认图标文件夹，ID: {folder1_id}")
    
    # 使用Bootstrap Icons
    folder2_id = manager.create_folder(
        title="Bootstrap图标文件夹",
        icon_type="folder",
        icon_path="icons/folder.svg",
        display_name="Bootstrap文件夹"
    )
    print(f"   创建Bootstrap图标文件夹，ID: {folder2_id}")
    
    # 2. 测试创建带不同图标类型的文件
    print("2. 测试创建带不同图标类型的文件...")
    
    # 使用默认图标类型
    file1_id = manager.create_file(
        title="默认图标文件.md",
        content="# 默认图标测试\n\n这是使用默认图标的测试文件",
        page_type="markdown",
        icon_type="textarea",
        display_name="默认Markdown文件"
    )
    print(f"   创建默认图标文件，ID: {file1_id}")
    
    # 使用Bootstrap Icons
    file2_id = manager.create_file(
        title="Bootstrap图标文件.md",
        content="# Bootstrap图标测试\n\n这是使用Bootstrap图标的测试文件",
        page_type="markdown",
        icon_type="textarea",
        icon_path="icons/file-earmark-text.svg",
        display_name="Bootstrap Markdown文件"
    )
    print(f"   创建Bootstrap图标文件，ID: {file2_id}")
    
    # 使用不同的Bootstrap Icons
    excalidraw_id = manager.create_file(
        title="画布文件",
        content="{}",  # Excalidraw内容
        page_type="excalidraw",
        icon_type="excalidraw",
        icon_path="icons/palette.svg",
        display_name="画布文件"
    )
    print(f"   创建画布文件，ID: {excalidraw_id}")
    
    # 3. 测试修改图标路径
    print("3. 测试修改图标路径...")
    
    # 修改文件的图标路径
    manager.save_item(
        id=file1_id,
        icon_path="icons/file-earmark-text.svg"  # 改为Bootstrap Icons
    )
    print(f"   修改文件 {file1_id} 的图标路径为 Bootstrap Icons")
    
    # 4. 获取并验证数据
    print("4. 获取并验证数据...")
    tree = manager.get_full_tree()
    
    # 查找我们创建的项目
    test_items = {}
    item_ids = [folder1_id, folder2_id, file1_id, file2_id, excalidraw_id]
    
    # 遍历所有项目查找我们创建的
    def find_items(items):
        for item in items:
            if item['id'] in item_ids:
                test_items[item['id']] = item
            # 递归查找子项
            if 'children' in item and item['children']:
                find_items(item['children'])
    
    find_items(tree)
    
    # 验证每个项目
    if folder1_id in test_items:
        item = test_items[folder1_id]
        print(f"   默认图标文件夹: {item['title']}, 图标类型: {item.get('icon_type')}, 图标路径: {item.get('icon_path')}, 显示名称: {item.get('display_name')}")
    
    if folder2_id in test_items:
        item = test_items[folder2_id]
        print(f"   Bootstrap图标文件夹: {item['title']}, 图标类型: {item.get('icon_type')}, 图标路径: {item.get('icon_path')}, 显示名称: {item.get('display_name')}")
    
    if file1_id in test_items:
        item = test_items[file1_id]
        print(f"   修改后的文件: {item['title']}, 图标类型: {item.get('icon_type')}, 图标路径: {item.get('icon_path')}, 显示名称: {item.get('display_name')}, 内容类型: {item.get('page_type')}")
    
    if file2_id in test_items:
        item = test_items[file2_id]
        print(f"   Bootstrap图标文件: {item['title']}, 图标类型: {item.get('icon_type')}, 图标路径: {item.get('icon_path')}, 显示名称: {item.get('display_name')}, 内容类型: {item.get('page_type')}")
    
    if excalidraw_id in test_items:
        item = test_items[excalidraw_id]
        print(f"   画布文件: {item['title']}, 图标类型: {item.get('icon_type')}, 图标路径: {item.get('icon_path')}, 显示名称: {item.get('display_name')}, 内容类型: {item.get('page_type')}")
    
    print("完整的图标功能测试完成!")

if __name__ == "__main__":
    test_complete_icon_functionality()