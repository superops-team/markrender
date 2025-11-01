#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试拖拽功能问题的脚本
验证拖拽调整层级是否生效
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
        
        grandchild_id = manager.save_item(
            title="孙子节点",
            content="孙子节点内容",
            parent_id=child1_id
        )
        print(f"创建孙子节点，ID: {grandchild_id}")
        
        # 显示初始状态
        print("\n=== 初始状态 ===")
        print_items(manager, [root1_id, root2_id, child1_id, grandchild_id])
        
        # 尝试移动子节点1到根节点2下
        print("\n=== 移动子节点1到根节点2下 ===")
        print("调用 move_item 方法...")
        result = manager.move_item(child1_id, root2_id)
        print(f"移动结果: {result}")
        
        # 显示移动后的状态
        print("\n=== 移动后状态 ===")
        print_items(manager, [root1_id, root2_id, child1_id, grandchild_id])
        
        # 再次获取完整树形结构
        print("\n=== 完整树形结构 ===")
        tree = manager.get_full_tree()
        print_tree(tree, 0)
        
    finally:
        # 删除临时数据库文件
        if os.path.exists(temp_db.name):
            os.unlink(temp_db.name)


def print_items(manager, item_ids):
    """打印指定ID的项信息"""
    for item_id in item_ids:
        data = manager.get_detail(item_id)
        print(f"ID={data['id']}, 标题={data['title']}, 层级={data['level']}, 父ID={data['parent_id']}")


def print_tree(items, level):
    """打印树形结构"""
    for item in items:
        indent = "  " * level
        print(f"{indent}- {item['title']} (ID: {item['id']}, 层级: {item['level']}, 父ID: {item['parent_id']})")
        if 'children' in item and item['children']:
            print_tree(item['children'], level + 1)


if __name__ == '__main__':
    main()