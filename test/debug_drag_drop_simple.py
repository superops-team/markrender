#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的拖拽功能调试脚本
验证拖拽重新调整树形结构层级功能的实际效果
"""

import sys
import os
import tempfile

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.markrender_manager import MarkRenderManager


def main():
    """主函数"""
    # 创建临时数据库
    temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
    temp_db.close()
    
    try:
        # 初始化数据库管理器
        manager = MarkRenderManager(temp_db.name)
        
        # 创建测试数据
        print("创建测试数据...")
        root1_id = manager.save_item(
            title="根节点1",
            content="根节点1内容",
            is_folder=1
        )
        print(f"创建根节点1，ID: {root1_id}")
        
        root2_id = manager.save_item(
            title="根节点2",
            content="根节点2内容",
            is_folder=1
        )
        print(f"创建根节点2，ID: {root2_id}")
        
        child1_id = manager.save_item(
            title="子节点1",
            content="子节点1内容",
            parent_id=root1_id
        )
        print(f"创建子节点1，ID: {child1_id}")
        
        child2_id = manager.save_item(
            title="子节点2",
            content="子节点2内容",
            parent_id=root1_id
        )
        print(f"创建子节点2，ID: {child2_id}")
        
        grandchild_id = manager.save_item(
            title="孙子节点",
            content="孙子节点内容",
            parent_id=child1_id
        )
        print(f"创建孙子节点，ID: {grandchild_id}")
        
        # 显示初始状态
        print("\n=== 初始状态 ===")
        root1_data = manager.get_detail(root1_id)
        root2_data = manager.get_detail(root2_id)
        child1_data = manager.get_detail(child1_id)
        child2_data = manager.get_detail(child2_id)
        grandchild_data = manager.get_detail(grandchild_id)
        
        print(f"根节点1: ID={root1_data['id']}, 标题={root1_data['title']}, 层级={root1_data['level']}, 父ID={root1_data['parent_id']}")
        print(f"根节点2: ID={root2_data['id']}, 标题={root2_data['title']}, 层级={root2_data['level']}, 父ID={root2_data['parent_id']}")
        print(f"子节点1: ID={child1_data['id']}, 标题={child1_data['title']}, 层级={child1_data['level']}, 父ID={child1_data['parent_id']}")
        print(f"子节点2: ID={child2_data['id']}, 标题={child2_data['title']}, 层级={child2_data['level']}, 父ID={child2_data['parent_id']}")
        print(f"孙子节点: ID={grandchild_data['id']}, 标题={grandchild_data['title']}, 层级={grandchild_data['level']}, 父ID={grandchild_data['parent_id']}")
        
        # 移动子节点1到根节点2下
        print("\n=== 移动子节点1到根节点2下 ===")
        result = manager.move_item(child1_id, root2_id)
        print(f"移动结果: {result}")
        
        # 显示移动后的状态
        child1_data = manager.get_detail(child1_id)
        grandchild_data = manager.get_detail(grandchild_id)
        
        print(f"子节点1: ID={child1_data['id']}, 标题={child1_data['title']}, 层级={child1_data['level']}, 父ID={child1_data['parent_id']}")
        print(f"孙子节点: ID={grandchild_data['id']}, 标题={grandchild_data['title']}, 层级={grandchild_data['level']}, 父ID={grandchild_data['parent_id']}")
        
        # 将子节点1移回根节点
        print("\n=== 将子节点1移回根节点 ===")
        result = manager.move_item(child1_id, None)
        print(f"移动结果: {result}")
        
        # 显示移回后的状态
        child1_data = manager.get_detail(child1_id)
        grandchild_data = manager.get_detail(grandchild_id)
        
        print(f"子节点1: ID={child1_data['id']}, 标题={child1_data['title']}, 层级={child1_data['level']}, 父ID={child1_data['parent_id']}")
        print(f"孙子节点: ID={grandchild_data['id']}, 标题={grandchild_data['title']}, 层级={grandchild_data['level']}, 父ID={grandchild_data['parent_id']}")
        
        # 显示完整树形结构
        print("\n=== 完整树形结构 ===")
        tree = manager.get_full_tree()
        print_tree(tree, 0)
        
    finally:
        # 删除临时数据库文件
        if os.path.exists(temp_db.name):
            os.unlink(temp_db.name)


def print_tree(items, level):
    """打印树形结构"""
    for item in items:
        indent = "  " * level
        print(f"{indent}- {item['title']} (ID: {item['id']}, 层级: {item['level']})")
        if 'children' in item and item['children']:
            print_tree(item['children'], level + 1)


if __name__ == '__main__':
    main()