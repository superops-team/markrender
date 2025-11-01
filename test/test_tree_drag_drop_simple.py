#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化测试树形结构拖拽功能核心逻辑
验证拖拽重新调整树形结构层级功能是否正常工作
"""

import sys
import os
import tempfile
import unittest

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.markrender_manager import MarkRenderManager


class TestTreeDragDropSimple(unittest.TestCase):
    """简化测试树形结构拖拽功能"""

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

    def test_move_item_function(self):
        """测试移动节点功能"""
        # 测试将子节点移动到另一个根节点下
        result = self.manager.move_item(self.child1_id, self.root2_id)
        self.assertTrue(result)
        
        # 验证数据库中的变化
        child1_data = self.manager.get_detail(self.child1_id)
        self.assertEqual(child1_data['parent_id'], self.root2_id)

    def test_update_item_level_function(self):
        """测试更新项层级功能"""
        # 添加更新项层级的方法测试
        # 首先移动节点
        self.manager.move_item(self.child1_id, self.root2_id)
        
        # 手动更新层级（模拟修复后的逻辑）
        child1_data = self.manager.get_detail(self.child1_id)
        # 移动到根节点下，层级应为1
        self.assertEqual(child1_data['level'], 1)
        
        # 孙子节点的层级应为2
        grandchild_data = self.manager.get_detail(self.grandchild_id)
        self.assertEqual(grandchild_data['level'], 2)

    def test_reorder_siblings_function(self):
        """测试重新排序同级节点功能"""
        # 获取初始顺序
        child1_data = self.manager.get_detail(self.child1_id)
        child2_data = self.manager.get_detail(self.child2_id)
        
        # 更新顺序
        result1 = self.manager.update_order(self.child1_id, 2)
        result2 = self.manager.update_order(self.child2_id, 1)
        
        self.assertTrue(result1)
        self.assertTrue(result2)
        
        # 验证顺序更新
        child1_data = self.manager.get_detail(self.child1_id)
        child2_data = self.manager.get_detail(self.child2_id)
        
        self.assertEqual(child2_data['order'], 1)
        self.assertEqual(child1_data['order'], 2)

    def test_move_item_to_root(self):
        """测试将节点移动到根节点"""
        # 将子节点移动到根节点
        result = self.manager.move_item(self.child1_id, None)
        self.assertTrue(result)
        
        # 验证数据库中的变化
        child1_data = self.manager.get_detail(self.child1_id)
        self.assertIsNone(child1_data['parent_id'])
        self.assertEqual(child1_data['level'], 0)  # 根节点层级应为0

    def test_get_full_tree_structure(self):
        """测试获取完整树形结构"""
        # 获取完整树形结构
        tree = self.manager.get_full_tree()
        
        # 验证树形结构
        self.assertEqual(len(tree), 2)  # 应该有两个根节点
        
        # 查找根节点1
        root1 = None
        for item in tree:
            if item['id'] == self.root1_id:
                root1 = item
                break
        
        self.assertIsNotNone(root1)
        if root1 is not None:
            self.assertIn('children', root1)
            self.assertEqual(len(root1['children']), 2)  # 根节点1应该有两个子节点
        
        # 验证子节点
        child1 = None
        if root1 is not None and 'children' in root1:
            for child in root1['children']:
                if child['id'] == self.child1_id:
                    child1 = child
                    break
        
        self.assertIsNotNone(child1)
        if child1 is not None:
            self.assertIn('children', child1)
            self.assertEqual(len(child1['children']), 1)  # 子节点1应该有一个子节点（孙子节点）


if __name__ == '__main__':
    unittest.main()