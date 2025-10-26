#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试树形结构修复功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.markrender_manager import MarkRenderManager

def test_tree_structure_fix():
    """测试树形结构修复功能"""
    print("测试树形结构修复功能...")
    
    # 创建数据库管理器
    manager = MarkRenderManager()
    
    # 创建一个测试文件夹
    print("\n1. 创建测试文件夹:")
    folder_id = manager.create_folder(
        title='测试文件夹',
        page_type='markdown'
    )
    print(f"   创建文件夹ID: {folder_id}")
    
    # 在文件夹中创建一个带颜色的文件
    print("\n2. 在文件夹中创建带颜色的文件:")
    file_id = manager.create_file(
        title='测试文件',
        content='# 测试文件\n这是一个测试文件',
        parent_id=folder_id,
        page_type='markdown',
        icon_path='icons/palette.svg',
        icon_color='#FF5733'  # 橙色
    )
    print(f"   创建文件ID: {file_id}")
    
    # 获取完整的树形结构
    print("\n3. 获取完整的树形结构:")
    tree_structure = manager.get_full_tree()
    print(f"   树形结构节点数: {len(tree_structure)}")
    
    # 打印树形结构
    def print_tree(nodes, level=0):
        for node in nodes:
            indent = "  " * level
            folder_status = "📁" if node.get('is_folder') else "📄"
            print(f"{indent}{folder_status} {node['title']} (ID: {node['id']})")
            if 'children' in node and node['children']:
                print_tree(node['children'], level + 1)
    
    print_tree(tree_structure)
    
    # 更新文件的图标颜色
    print("\n4. 更新文件的图标颜色:")
    manager.save_item(
        id=file_id,
        icon_color='#3357FF'  # 蓝色
    )
    print("   图标颜色已更新为蓝色")
    
    # 再次获取完整的树形结构，验证结构是否保持完整
    print("\n5. 验证树形结构完整性:")
    updated_tree_structure = manager.get_full_tree()
    print(f"   更新后树形结构节点数: {len(updated_tree_structure)}")
    
    # 检查文件夹和文件的父子关系是否保持
    def find_node_by_id(nodes, node_id):
        for node in nodes:
            if node['id'] == node_id:
                return node
            if 'children' in node and node['children']:
                found = find_node_by_id(node['children'], node_id)
                if found:
                    return found
        return None
    
    folder_node = find_node_by_id(updated_tree_structure, folder_id)
    file_node = find_node_by_id(updated_tree_structure, file_id)
    
    if folder_node and file_node:
        print(f"   文件夹节点ID: {folder_node['id']}, 父ID: {folder_node.get('parent_id')}")
        print(f"   文件节点ID: {file_node['id']}, 父ID: {file_node.get('parent_id')}")
        if file_node.get('parent_id') == folder_id:
            print("   ✅ 父子关系保持完整")
        else:
            print("   ❌ 父子关系被破坏")
    else:
        print("   ❌ 无法找到节点")
    
    print("\n测试完成!")

if __name__ == "__main__":
    test_tree_structure_fix()