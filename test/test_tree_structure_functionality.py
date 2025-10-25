#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试树形结构功能，验证父子节点关系
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.markrender_manager import MarkRenderManager

def test_tree_structure_functionality():
    """测试树形结构功能"""
    print("开始测试树形结构功能...")
    
    # 创建MarkRenderManager实例
    manager = MarkRenderManager()
    
    # 1. 创建根文件夹
    print("1. 创建根文件夹...")
    root_folder_id = manager.create_folder(
        title="根文件夹",
        icon_type="folder",
        icon_path="icons/folder.svg",
        display_name="根文件夹"
    )
    print(f"   创建根文件夹，ID: {root_folder_id}")
    
    # 2. 在根文件夹下创建子文件夹
    print("2. 在根文件夹下创建子文件夹...")
    sub_folder_id = manager.create_folder(
        title="子文件夹",
        parent_id=root_folder_id,
        icon_type="folder",
        icon_path="icons/folder.svg",
        display_name="子文件夹"
    )
    print(f"   创建子文件夹，ID: {sub_folder_id}")
    
    # 3. 在根文件夹下创建文件
    print("3. 在根文件夹下创建文件...")
    root_file_id = manager.create_file(
        title="根文件.md",
        content="# 根文件\n\n这是根文件夹中的文件",
        parent_id=root_folder_id,
        page_type="markdown",
        icon_type="textarea",
        icon_path="icons/file-earmark-text.svg",
        display_name="根文件"
    )
    print(f"   创建根文件，ID: {root_file_id}")
    
    # 4. 在子文件夹下创建文件
    print("4. 在子文件夹下创建文件...")
    sub_file_id = manager.create_file(
        title="子文件.md",
        content="# 子文件\n\n这是子文件夹中的文件",
        parent_id=sub_folder_id,
        page_type="markdown",
        icon_type="textarea",
        icon_path="icons/file-earmark-text.svg",
        display_name="子文件"
    )
    print(f"   创建子文件，ID: {sub_file_id}")
    
    # 5. 获取完整的树形结构
    print("5. 获取完整的树形结构...")
    tree = manager.get_full_tree()
    
    # 查找根文件夹及其子项
    root_folder = None
    for item in tree:
        if item['id'] == root_folder_id:
            root_folder = item
            break
    
    if root_folder:
        print(f"   根文件夹: {root_folder['title']}")
        print(f"   根文件夹的父ID: {root_folder.get('parent_id')}")
        print(f"   根文件夹的子项数量: {len(root_folder.get('children', []))}")
        
        # 验证根文件夹的子项
        children = root_folder.get('children', [])
        for child in children:
            print(f"     子项: {child['title']}, 类型: {'文件夹' if child.get('is_folder') else '文件'}, 父ID: {child.get('parent_id')}")
            
            # 如果是子文件夹，验证其子项
            if child.get('is_folder') and child.get('id') == sub_folder_id:
                sub_children = child.get('children', [])
                print(f"     子文件夹的子项数量: {len(sub_children)}")
                for sub_child in sub_children:
                    print(f"       子项: {sub_child['title']}, 类型: {'文件夹' if sub_child.get('is_folder') else '文件'}, 父ID: {sub_child.get('parent_id')}")
    
    # 6. 验证特定节点的子项
    print("6. 验证特定节点的子项...")
    
    # 获取根文件夹的直接子项
    root_children = manager.get_children(root_folder_id)
    print(f"   根文件夹的直接子项数量: {len(root_children)}")
    for child in root_children:
        print(f"     直接子项: {child['title']}, 类型: {'文件夹' if child.get('is_folder') else '文件'}")
    
    # 获取子文件夹的直接子项
    sub_children = manager.get_children(sub_folder_id)
    print(f"   子文件夹的直接子项数量: {len(sub_children)}")
    for child in sub_children:
        print(f"     直接子项: {child['title']}, 类型: {'文件夹' if child.get('is_folder') else '文件'}")
    
    # 获取根节点（没有父节点的项）
    root_items = manager.get_children(None)
    print(f"   根节点数量: {len(root_items)}")
    for item in root_items:
        print(f"     根节点: {item['title']}, 类型: {'文件夹' if item.get('is_folder') else '文件'}")
    
    print("树形结构功能测试完成!")

if __name__ == "__main__":
    test_tree_structure_functionality()