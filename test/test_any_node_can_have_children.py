#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试任意节点都能添加子节点的功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.markrender_manager import MarkRenderManager

def test_any_node_can_have_children():
    """测试任意节点都能添加子节点的功能"""
    print("测试任意节点都能添加子节点的功能...")
    
    # 创建数据库管理器
    manager = MarkRenderManager()
    
    # 创建一个普通的文件（但is_folder应该被设置为1）
    print("\n1. 创建普通文件:")
    file_id = manager.create_file(
        title='普通文件',
        content='# 普通文件\n这是一个普通文件',
        page_type='markdown'
    )
    print(f"   创建文件ID: {file_id}")
    
    # 获取文件详情
    print("\n2. 获取文件详情:")
    file_detail = manager.get_detail(file_id)
    print(f"   文件标题: {file_detail['title']}")
    print(f"   是否为文件夹: {file_detail.get('is_folder', 0)}")
    print(f"   页面类型: {file_detail.get('page_type', 'N/A')}")
    
    # 在普通文件中创建一个子文件
    print("\n3. 在普通文件中创建子文件:")
    child_file_id = manager.create_file(
        title='子文件',
        content='# 子文件\n这是子文件',
        parent_id=file_id,
        page_type='markdown'
    )
    print(f"   创建子文件ID: {child_file_id}")
    
    # 获取子文件详情
    print("\n4. 获取子文件详情:")
    child_file_detail = manager.get_detail(child_file_id)
    print(f"   子文件标题: {child_file_detail['title']}")
    print(f"   是否为文件夹: {child_file_detail.get('is_folder', 0)}")
    print(f"   父节点ID: {child_file_detail.get('parent_id', 'N/A')}")
    
    # 获取父文件的子节点
    print("\n5. 获取父文件的子节点:")
    children = manager.get_children(file_id)
    print(f"   子节点数量: {len(children)}")
    for child in children:
        folder_status = "📁" if child.get('is_folder') else "📄"
        print(f"   {folder_status} {child['title']} (ID: {child['id']})")
    
    # 获取完整的树形结构
    print("\n6. 获取完整的树形结构:")
    tree_structure = manager.get_full_tree()
    
    # 查找并打印测试文件及其子节点
    def find_and_print_node(nodes, node_id, level=0):
        for node in nodes:
            if node['id'] == node_id:
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
                if find_and_print_node(node['children'], node_id, level + 1):
                    return True
        return False
    
    find_and_print_node(tree_structure, file_id)
    
    print("\n测试完成!")

if __name__ == "__main__":
    test_any_node_can_have_children()