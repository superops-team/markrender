#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新的树形结构功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.markrender_manager import MarkRenderManager

def test_new_tree_functionality():
    """测试新的树形结构功能"""
    print("开始测试新的树形结构功能...")
    
    # 创建MarkRenderManager实例
    manager = MarkRenderManager()
    
    # 1. 创建根文件夹（默认page_type为folder）
    print("1. 创建根文件夹（默认page_type为folder）...")
    root_folder_id = manager.create_folder(
        title="测试根文件夹",
        icon_type="folder",
        icon_path="icons/folder.svg"
    )
    print(f"   创建根文件夹，ID: {root_folder_id}")
    
    # 验证根文件夹的page_type
    root_folder_data = manager.get_detail(root_folder_id)
    print(f"   根文件夹的page_type: {root_folder_data.get('page_type')}")
    
    # 2. 创建子文件夹（指定page_type为markdown）
    print("2. 创建子文件夹（指定page_type为markdown）...")
    sub_folder_id = manager.create_folder(
        title="测试子文件夹",
        parent_id=root_folder_id,
        icon_type="folder",
        icon_path="icons/folder.svg",
        page_type="markdown"  # 指定page_type为markdown
    )
    print(f"   创建子文件夹，ID: {sub_folder_id}")
    
    # 验证子文件夹的page_type
    sub_folder_data = manager.get_detail(sub_folder_id)
    print(f"   子文件夹的page_type: {sub_folder_data.get('page_type')}")
    
    # 3. 验证父子关系
    print("3. 验证父子关系...")
    children = manager.get_children(root_folder_id)
    print(f"   根文件夹的子项数量: {len(children)}")
    for child in children:
        print(f"     子项: {child['title']}, ID: {child['id']}, 父ID: {child['parent_id']}, page_type: {child['page_type']}")
    
    print("新的树形结构功能测试完成!")

if __name__ == "__main__":
    test_new_tree_functionality()