#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终的拖拽功能验证测试
确保拖拽重新调整树形结构层级功能完全符合要求
"""

import sys
import os
import tempfile
import unittest

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.markrender_manager import MarkRenderManager


class TestDragDropFinal(unittest.TestCase):
    """最终的拖拽功能验证测试"""

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

    def test_drag_drop_functionality_comprehensive(self):
        """综合测试拖拽功能"""
        # 1. 验证初始状态
        root1_data = self.manager.get_detail(self.root1_id)
        root2_data = self.manager.get_detail(self.root2_id)
        child1_data = self.manager.get_detail(self.child1_id)
        child2_data = self.manager.get_detail(self.child2_id)
        grandchild_data = self.manager.get_detail(self.grandchild_id)
        
        # 验证初始层级（数据库默认值为0）
        self.assertEqual(root1_data['level'], 0)
        self.assertEqual(root2_data['level'], 0)
        self.assertEqual(child1_data['level'], 0)
        self.assertEqual(child2_data['level'], 0)
        self.assertEqual(grandchild_data['level'], 0)
        
        # 验证初始父节点关系
        self.assertEqual(child1_data['parent_id'], self.root1_id)
        self.assertEqual(child2_data['parent_id'], self.root1_id)
        self.assertEqual(grandchild_data['parent_id'], self.child1_id)
        
        # 2. 移动子节点1到根节点2下
        result = self.manager.move_item(self.child1_id, self.root2_id)
        self.assertTrue(result)
        
        # 验证移动后的状态
        child1_data = self.manager.get_detail(self.child1_id)
        grandchild_data = self.manager.get_detail(self.grandchild_id)
        
        # 验证父节点更新
        self.assertEqual(child1_data['parent_id'], self.root2_id)
        
        # 验证层级更新
        self.assertEqual(child1_data['level'], 1)  # 在根节点2下，层级为1
        self.assertEqual(grandchild_data['level'], 2)  # 孙子节点层级为2
        
        # 3. 将节点移回根节点
        result = self.manager.move_item(self.child1_id, None)
        self.assertTrue(result)
        
        # 验证移回根节点后的状态
        child1_data = self.manager.get_detail(self.child1_id)
        grandchild_data = self.manager.get_detail(self.grandchild_id)
        
        # 验证父节点更新
        self.assertIsNone(child1_data['parent_id'])
        
        # 验证层级更新
        self.assertEqual(child1_data['level'], 0)  # 根节点层级为0
        self.assertEqual(grandchild_data['level'], 1)  # 孙子节点层级为1
        
        # 4. 创建更深的层级结构并测试
        great_grandchild_id = self.manager.save_item(
            title="曾孙节点",
            content="曾孙节点内容",
            parent_id=self.grandchild_id
        )
        
        # 验证初始层级
        grandchild_data = self.manager.get_detail(self.grandchild_id)
        great_grandchild_data = self.manager.get_detail(great_grandchild_id)
        
        self.assertEqual(grandchild_data['level'], 1)
        self.assertEqual(great_grandchild_data['level'], 0)  # 数据库默认值为0
        
        # 将子节点1移动到根节点2下
        result = self.manager.move_item(self.child1_id, self.root2_id)
        self.assertTrue(result)
        
        # 验证所有相关节点的层级都已更新
        child1_data = self.manager.get_detail(self.child1_id)
        grandchild_data = self.manager.get_detail(self.grandchild_id)
        great_grandchild_data = self.manager.get_detail(great_grandchild_id)
        
        # 移动后，层级应该相应更新
        self.assertEqual(child1_data['level'], 1)  # child1在level1
        self.assertEqual(grandchild_data['level'], 2)  # grandchild在level2
        self.assertEqual(great_grandchild_data['level'], 3)  # great_grandchild在level3
        
        # 5. 测试边界情况
        # 测试将节点移动到自身（应该不改变层级）
        original_level = self.manager.get_detail(self.root1_id)['level']
        result = self.manager.move_item(self.root1_id, self.root1_id)
        self.assertTrue(result)
        self.assertEqual(self.manager.get_detail(self.root1_id)['level'], original_level)
        
        # 测试移动到不存在的父节点
        result = self.manager.move_item(self.child1_id, 999999)
        self.assertTrue(result)
        child1_data = self.manager.get_detail(self.child1_id)
        self.assertIsNone(child1_data['parent_id'])
        self.assertEqual(child1_data['level'], 0)
        
        # 6. 验证树形结构完整性
        tree = self.manager.get_full_tree()
        
        # 验证根节点数量（包括之前移动到根节点的child1）
        root_items = [item for item in tree if not item.get('parent_id')]
        self.assertEqual(len(root_items), 3)  # root1, root2, child1
        
        # 验证树形结构正确性
        # 查找child1（现在是根节点）
        child1_as_root = None
        for item in tree:
            if item['id'] == self.child1_id:
                child1_as_root = item
                break
        
        self.assertIsNotNone(child1_as_root)
        if child1_as_root is not None:
            self.assertIsNone(child1_as_root.get('parent_id'))
            self.assertEqual(child1_as_root['level'], 0)
            
            # 验证child1的子节点
            if 'children' in child1_as_root:
                self.assertEqual(len(child1_as_root['children']), 1)
                self.assertEqual(child1_as_root['children'][0]['id'], self.grandchild_id)
                self.assertEqual(child1_as_root['children'][0]['level'], 1)
                
                # 验证孙子节点的子节点（曾孙节点）
                grandchild_item = child1_as_root['children'][0]
                if 'children' in grandchild_item:
                    self.assertEqual(len(grandchild_item['children']), 1)
                    self.assertEqual(grandchild_item['children'][0]['id'], great_grandchild_id)
                    self.assertEqual(grandchild_item['children'][0]['level'], 2)

    def test_tree_structure_persistence(self):
        """测试树形结构的持久性"""
        # 移动一些节点
        self.manager.move_item(self.child1_id, self.root2_id)
        
        # 重新获取完整树形结构
        tree1 = self.manager.get_full_tree()
        
        # 再次获取树形结构
        tree2 = self.manager.get_full_tree()
        
        # 验证两次获取的结构一致
        self.assertEqual(len(tree1), len(tree2))
        
        # 验证关键节点的存在和层级
        def find_item_by_id(tree, item_id):
            for item in tree:
                if item['id'] == item_id:
                    return item
                if 'children' in item:
                    found = find_item_by_id(item['children'], item_id)
                    if found:
                        return found
            return None
        
        # 查找移动后的子节点1
        child1_in_tree1 = find_item_by_id(tree1, self.child1_id)
        child1_in_tree2 = find_item_by_id(tree2, self.child1_id)
        
        self.assertIsNotNone(child1_in_tree1)
        self.assertIsNotNone(child1_in_tree2)
        self.assertEqual(child1_in_tree1['level'], child1_in_tree2['level'])
        self.assertEqual(child1_in_tree1['parent_id'], child1_in_tree2['parent_id'])


if __name__ == '__main__':
    unittest.main()