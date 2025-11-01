#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试UI层面的拖拽功能
模拟panel.py中的拖拽处理逻辑
"""

import sys
import os
import tempfile
import unittest
from unittest.mock import Mock, patch

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.markrender_manager import MarkRenderManager


class TestUIDragDrop(unittest.TestCase):
    """测试UI层面的拖拽功能"""

    def setUp(self):
        """测试初始化"""
        # 创建临时数据库
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db.close()
        
        # 初始化数据库管理器
        self.manager = MarkRenderManager(self.temp_db.name)
        
        # 创建测试数据
        self._create_test_data()

    def tearDown(self):
        """测试清理"""
        # 删除临时数据库文件
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)

    def _create_test_data(self):
        """创建测试数据"""
        # 创建根节点
        self.root1_id = self.manager.save_item(
            title="根节点1",
            content="根节点1内容",
            is_folder=1
        )
        
        self.root2_id = self.manager.save_item(
            title="根节点2",
            content="根节点2内容",
            is_folder=1
        )
        
        # 创建子节点
        self.child1_id = self.manager.save_item(
            title="子节点1",
            content="子节点1内容",
            parent_id=self.root1_id
        )
        
        # 创建孙子节点
        self.grandchild_id = self.manager.save_item(
            title="孙子节点",
            content="孙子节点内容",
            parent_id=self.child1_id
        )

    def test_update_item_hierarchy(self):
        """测试更新项层次结构的方法"""
        # 模拟panel.py中的_update_item_hierarchy方法的逻辑
        item_id = self.child1_id
        new_parent_id = self.root2_id
        insert_position = -1
        target_parent_item = None  # 在实际UI中这会是一个QTreeWidgetItem对象
        
        # 显示初始状态
        print("\n=== 初始状态 ===")
        self._print_items([self.root1_id, self.root2_id, self.child1_id, self.grandchild_id])
        
        # 使用数据库管理器的move_item方法来处理层级更新和父ID更新
        # 这会自动处理层级的递归更新
        result = self.manager.move_item(item_id, new_parent_id)
        self.assertTrue(result)
        
        # 计算并更新顺序（模拟_reorder_siblings和_set_as_last_child方法）
        if insert_position >= 0:
            # 重新计算并更新所有同级节点的顺序
            pass  # 在这个测试中我们不测试顺序更新
        else:
            # 如果没有指定位置，则将其设置为最后一个
            # 获取所有同级节点中的最大顺序值
            max_order = 0
            all_items = self.manager.get_full_tree()
            
            def find_max_order(items, parent_id):
                nonlocal max_order
                for item in items:
                    if item.get('parent_id') == parent_id:
                        if item.get('order', 0) > max_order:
                            max_order = item.get('order', 0)
                    if 'children' in item and item['children']:
                        find_max_order(item['children'], parent_id)
            
            find_max_order(all_items, new_parent_id)
            
            # 设置为最后一个子节点
            self.manager.save_item(
                id=item_id,
                order=max_order + 1
            )
        
        print(f"成功更新项 {item_id} 的层次结构，父ID: {new_parent_id}, 位置: {insert_position}")
        
        # 验证更新后的状态
        print("\n=== 更新后状态 ===")
        self._print_items([self.root1_id, self.root2_id, self.child1_id, self.grandchild_id])
        
        # 获取更新后的数据
        child1_data = self.manager.get_detail(self.child1_id)
        grandchild_data = self.manager.get_detail(self.grandchild_id)
        
        # 验证父ID更新
        self.assertEqual(child1_data['parent_id'], self.root2_id)
        
        # 验证层级更新
        self.assertEqual(child1_data['level'], 1)  # 在根节点2下，层级为1
        self.assertEqual(grandchild_data['level'], 2)  # 孙子节点层级为2

    def _print_items(self, item_ids):
        """打印指定ID的项信息"""
        for item_id in item_ids:
            data = self.manager.get_detail(item_id)
            print(f"ID={data['id']}, 标题={data['title']}, 层级={data['level']}, 父ID={data['parent_id']}, 顺序={data['order']}")


if __name__ == '__main__':
    unittest.main()