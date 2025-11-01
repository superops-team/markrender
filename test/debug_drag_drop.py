#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试拖拽功能
"""

import sys
import os
import tempfile

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.markrender_manager import MarkRenderManager

def debug_drag_drop():
    """调试拖拽功能"""
    # 创建临时数据库
    temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
    temp_db.close()
    
    # 初始化数据库管理器
    manager = MarkRenderManager(temp_db.name)
    
    # 创建测试数据
    # 创建根节点
    root1_id = manager.save_item(
        title="根节点1",
        content="根节点1内容",
        is_folder=1
    )
    
    root2_id = manager.save_item(
        title="根节点2",
        content="根节点2内容",
        is_folder=1
    )
    
    # 创建子节点
    child1_id = manager.save_item(
        title="子节点1",
        content="子节点1内容",
        parent_id=root1_id
    )
    
    # 创建孙子节点
    grandchild_id = manager.save_item(
        title="孙子节点",
        content="孙子节点内容",
        parent_id=child1_id
    )
    
    # 创建曾孙节点
    great_grandchild_id = manager.save_item(
        title="曾孙节点",
        content="曾孙节点内容",
        parent_id=grandchild_id
    )
    
    print("初始状态:")
    root1_data = manager.get_detail(root1_id)
    root2_data = manager.get_detail(root2_id)
    child1_data = manager.get_detail(child1_id)
    grandchild_data = manager.get_detail(grandchild_id)
    great_grandchild_data = manager.get_detail(great_grandchild_id)
    
    print(f"根节点1: ID={root1_data['id']}, Level={root1_data['level']}")
    print(f"根节点2: ID={root2_data['id']}, Level={root2_data['level']}")
    print(f"子节点1: ID={child1_data['id']}, Parent={child1_data['parent_id']}, Level={child1_data['level']}")
    print(f"孙子节点: ID={grandchild_data['id']}, Parent={grandchild_data['parent_id']}, Level={grandchild_data['level']}")
    print(f"曾孙节点: ID={great_grandchild_data['id']}, Parent={great_grandchild_data['parent_id']}, Level={great_grandchild_data['level']}")
    
    print("\n移动子节点1到根节点2下:")
    result = manager.move_item(child1_id, root2_id)
    print(f"移动结果: {result}")
    
    # 检查移动后的状态
    child1_data = manager.get_detail(child1_id)
    grandchild_data = manager.get_detail(grandchild_id)
    great_grandchild_data = manager.get_detail(great_grandchild_id)
    
    print(f"子节点1: ID={child1_data['id']}, Parent={child1_data['parent_id']}, Level={child1_data['level']}")
    print(f"孙子节点: ID={grandchild_data['id']}, Parent={grandchild_data['parent_id']}, Level={grandchild_data['level']}")
    print(f"曾孙节点: ID={great_grandchild_data['id']}, Parent={great_grandchild_data['parent_id']}, Level={great_grandchild_data['level']}")
    
    # 清理
    if os.path.exists(temp_db.name):
        os.unlink(temp_db.name)

if __name__ == '__main__':
    debug_drag_drop()