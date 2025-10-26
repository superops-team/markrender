#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文件夹功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.markrender_manager import MarkRenderManager

def test_folder_functionality():
    """测试文件夹功能"""
    print("测试文件夹功能...")
    
    # 创建数据库管理器
    manager = MarkRenderManager()
    
    # 创建一个测试文件夹
    print("\n1. 创建测试文件夹:")
    folder_id = manager.create_folder(
        title='测试文件夹',
        page_type='markdown'
    )
    print(f"   创建文件夹ID: {folder_id}")
    
    # 获取文件夹详情
    print("\n2. 获取文件夹详情:")
    folder_detail = manager.get_detail(folder_id)
    print(f"   文件夹标题: {folder_detail['title']}")
    print(f"   是否为文件夹: {folder_detail.get('is_folder', 0)}")
    print(f"   页面类型: {folder_detail.get('page_type', 'N/A')}")
    
    # 在文件夹中创建一个文件
    print("\n3. 在文件夹中创建文件:")
    file_id = manager.create_file(
        title='测试文件',
        content='# 测试文件\n这是一个测试文件',
        parent_id=folder_id,
        page_type='markdown'
    )
    print(f"   创建文件ID: {file_id}")
    
    # 获取文件详情
    print("\n4. 获取文件详情:")
    file_detail = manager.get_detail(file_id)
    print(f"   文件标题: {file_detail['title']}")
    print(f"   是否为文件夹: {file_detail.get('is_folder', 0)}")
    print(f"   父节点ID: {file_detail.get('parent_id', 'N/A')}")
    
    # 获取文件夹的子节点
    print("\n5. 获取文件夹的子节点:")
    children = manager.get_children(folder_id)
    print(f"   子节点数量: {len(children)}")
    for child in children:
        folder_status = "📁" if child.get('is_folder') else "📄"
        print(f"   {folder_status} {child['title']} (ID: {child['id']})")
    
    # 获取完整的树形结构
    print("\n6. 获取完整的树形结构:")
    tree_structure = manager.get_full_tree()
    
    # 查找并打印测试文件夹及其子节点
    def find_and_print_folder(nodes, folder_id, level=0):
        for node in nodes:
            if node['id'] == folder_id:
                indent = "  " * level
                folder_status = "📁" if node.get('is_folder') else "📄"
                print(f"{indent}{folder_status} {node['title']} (ID: {node['id']})")
                if 'children' in node and node['children']:
                    for child in node['children']:
                        child_indent = "  " * (level + 1)
                        child_folder_status = "📁" if child.get('is_folder') else "📄"
                        print(f"{child_indent}{child_folder_status} {child['title']} (ID: {child['id']})")
                return True
            if 'children' in node and node['children']:
                if find_and_print_folder(node['children'], folder_id, level + 1):
                    return True
        return False
    
    find_and_print_folder(tree_structure, folder_id)
    
    print("\n测试完成!")

if __name__ == "__main__":
    test_folder_functionality()