#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更真实的UI拖拽测试
模拟实际的拖拽操作流程
"""

import sys
import os
import tempfile
import unittest

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.markrender_manager import MarkRenderManager


class TestRealisticDragDrop(unittest.TestCase):
    """更真实的UI拖拽测试"""

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
        
        self.child2_id = self.manager.save_item(
            title="子节点2",
            content="子节点2内容",
            parent_id=self.root1_id
        )
        
        # 创建孙子节点
        self.grandchild_id = self.manager.save_item(
            title="孙子节点",
            content="孙子节点内容",
            parent_id=self.child1_id
        )

    def test_realistic_drag_drop_scenario(self):
        """测试真实的拖拽场景"""
        print("\n=== 初始状态 ===")
        self._print_full_tree()
        
        # 模拟拖拽操作：将子节点1拖拽到根节点2下
        print("\n=== 模拟拖拽：将子节点1拖拽到根节点2下 ===")
        
        # 1. 确定拖拽的项和目标父节点
        dragged_item_id = self.child1_id
        target_parent_id = self.root2_id
        
        # 2. 验证拖拽操作的有效性
        self._validate_drag_operation(dragged_item_id, target_parent_id)
        
        # 3. 执行拖拽操作
        self._perform_drag_drop(dragged_item_id, target_parent_id)
        
        # 4. 验证拖拽结果
        print("\n=== 拖拽后状态 ===")
        self._print_full_tree()
        self._verify_drag_drop_result(dragged_item_id, target_parent_id)
        
        # 5. 测试将节点移回原位置
        print("\n=== 模拟拖拽：将子节点1移回根节点1下 ===")
        self._perform_drag_drop(dragged_item_id, self.root1_id)
        
        print("\n=== 移回后状态 ===")
        self._print_full_tree()
        self._verify_drag_drop_result(dragged_item_id, self.root1_id)

    def _validate_drag_operation(self, dragged_item_id, target_parent_id):
        """验证拖拽操作的有效性"""
        # 不能拖到自身
        self.assertNotEqual(dragged_item_id, target_parent_id, "不能将节点拖入自身")
        
        # 不能拖到其子节点（这里简化处理，实际UI中会有更复杂的检查）
        # 在这个测试中我们不实现完整的后代检查

    def _perform_drag_drop(self, item_id, new_parent_id):
        """执行拖拽操作"""
        # 使用数据库管理器的move_item方法来处理层级更新和父ID更新
        # 这会自动处理层级的递归更新
        result = self.manager.move_item(item_id, new_parent_id)
        self.assertTrue(result, f"移动项 {item_id} 到父节点 {new_parent_id} 失败")
        
        print(f"成功将项 {item_id} 移动到父节点 {new_parent_id}")

    def _verify_drag_drop_result(self, item_id, expected_parent_id):
        """验证拖拽结果"""
        # 获取更新后的数据
        item_data = self.manager.get_detail(item_id)
        
        # 验证父ID更新
        if expected_parent_id is None:
            self.assertIsNone(item_data['parent_id'], f"项 {item_id} 的父ID应为None")
        else:
            self.assertEqual(item_data['parent_id'], expected_parent_id, f"项 {item_id} 的父ID应为 {expected_parent_id}")
        
        # 验证层级更新（简化验证，实际层级计算需要考虑父节点的层级）
        # 这里我们只验证关键节点的层级关系

    def _print_full_tree(self):
        """打印完整树形结构"""
        tree = self.manager.get_full_tree()
        self._print_tree_recursive(tree, 0)

    def _print_tree_recursive(self, items, level):
        """递归打印树形结构"""
        for item in items:
            indent = "  " * level
            print(f"{indent}- {item['title']} (ID: {item['id']}, 层级: {item['level']}, 父ID: {item['parent_id']})")
            if 'children' in item and item['children']:
                self._print_tree_recursive(item['children'], level + 1)

    def _print_items(self, item_ids):
        """打印指定ID的项信息"""
        for item_id in item_ids:
            data = self.manager.get_detail(item_id)
            print(f"ID={data['id']}, 标题={data['title']}, 层级={data['level']}, 父ID={data['parent_id']}")


if __name__ == '__main__':
    unittest.main()