#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整测试树形结构拖拽功能
验证拖拽重新调整树形结构层级功能是否正常工作，包括界面交互逻辑
"""

import sys
import os
import tempfile
import unittest
from unittest.mock import Mock, patch, MagicMock

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from app.quickpick.panel import QuickPickPanel
from db.markrender_manager import MarkRenderManager


class TestTreeDragDropComplete(unittest.TestCase):
    """完整测试树形结构拖拽功能"""

    def setUp(self):
        """测试初始化"""
        # 创建QApplication实例
        if not QApplication.instance():
            self.app = QApplication(sys.argv)
        else:
            self.app = QApplication.instance()
        
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

    def test_update_item_hierarchy_with_level_update(self):
        """测试更新项的层次结构，包括层级更新"""
        # 使用补丁避免创建实际的Qt组件
        with patch('app.quickpick.panel.QTreeWidget'), \
             patch('app.quickpick.panel.QTreeWidgetItem'), \
             patch('app.quickpick.panel.QuickPickItemDelegate'):
            
            # Mock quickpick_list
            mock_quickpick_list = Mock()
            mock_quickpick_list.topLevelItemCount.return_value = 0
            
            # 创建面板实例
            panel = QuickPickPanel(self.manager)
            panel.quickpick_list = mock_quickpick_list
            
            # 测试将子节点移动到另一个根节点下
            # 这会调用我们修复的 _update_item_hierarchy 方法
            panel._update_item_hierarchy(self.child1_id, self.root2_id, -1, None)
            
            # 验证数据库中的变化
            child1_data = self.manager.get_detail(self.child1_id)
            self.assertEqual(child1_data['parent_id'], self.root2_id)
            self.assertEqual(child1_data['level'], 1)  # 移动到根节点下，层级应为1
            
            # 验证孙子节点的层级也相应更新
            grandchild_data = self.manager.get_detail(self.grandchild_id)
            self.assertEqual(grandchild_data['level'], 2)  # 孙子节点层级应为2

    def test_reorder_siblings_complete(self):
        """测试重新排序同级节点完整流程"""
        with patch('app.quickpick.panel.QTreeWidget'), \
             patch('app.quickpick.panel.QTreeWidgetItem'), \
             patch('app.quickpick.panel.QuickPickItemDelegate'):
            
            # Mock quickpick_list
            mock_quickpick_list = Mock()
            mock_quickpick_list.topLevelItemCount.return_value = 0
            
            # 创建面板实例
            panel = QuickPickPanel(self.manager)
            panel.quickpick_list = mock_quickpick_list
            panel.load_quickpick_items()
            
            # 创建Mock父节点
            mock_parent_item = Mock()
            mock_parent_item.childCount.return_value = 2
            mock_child1 = Mock()
            mock_child2 = Mock()
            mock_parent_item.child.side_effect = [mock_child1, mock_child2]
            
            # 设置Mock数据
            mock_child1.data.return_value = {'id': self.child1_id}
            mock_child2.data.return_value = {'id': self.child2_id}
            
            # 测试重新排序
            panel._reorder_siblings(self.root1_id, self.child2_id, 0, mock_parent_item)
            
            # 验证数据库中的顺序更新
            child1_data = self.manager.get_detail(self.child1_id)
            child2_data = self.manager.get_detail(self.child2_id)
            
            # child2应该排在前面（order=1），child1排在后面（order=2）
            self.assertEqual(child2_data['order'], 1)
            self.assertEqual(child1_data['order'], 2)

    def test_is_descendant_check(self):
        """测试后代关系检查"""
        with patch('app.quickpick.panel.QTreeWidget'), \
             patch('app.quickpick.panel.QTreeWidgetItem'), \
             patch('app.quickpick.panel.QuickPickItemDelegate'):
            
            # 创建面板实例
            panel = QuickPickPanel(self.manager)
            
            # 创建Mock节点
            mock_child_item = Mock()
            mock_parent_item = Mock()
            mock_grandparent_item = Mock()
            
            # 设置父子关系
            mock_child_item.parent.return_value = mock_parent_item
            mock_parent_item.parent.return_value = mock_grandparent_item
            mock_grandparent_item.parent.return_value = None
            
            # 测试直接父子关系
            self.assertTrue(panel._is_descendant(mock_child_item, mock_parent_item))
            
            # 测试祖先后代关系
            self.assertTrue(panel._is_descendant(mock_child_item, mock_grandparent_item))
            
            # 测试非后代关系
            mock_unrelated_item = Mock()
            mock_unrelated_item.parent.return_value = None
            self.assertFalse(panel._is_descendant(mock_child_item, mock_unrelated_item))

    def test_move_to_root_with_children(self):
        """测试将带有子节点的节点移动到根节点"""
        with patch('app.quickpick.panel.QTreeWidget'), \
             patch('app.quickpick.panel.QTreeWidgetItem'), \
             patch('app.quickpick.panel.QuickPickItemDelegate'):
            
            # Mock quickpick_list
            mock_quickpick_list = Mock()
            mock_quickpick_list.topLevelItemCount.return_value = 0
            
            # 创建面板实例
            panel = QuickPickPanel(self.manager)
            panel.quickpick_list = mock_quickpick_list
            
            # 将子节点移动到根节点
            panel._update_item_hierarchy(self.child1_id, None, -1, None)
            
            # 验证数据库中的变化
            child1_data = self.manager.get_detail(self.child1_id)
            self.assertIsNone(child1_data['parent_id'])
            self.assertEqual(child1_data['level'], 0)  # 根节点层级应为0
            
            # 验证孙子节点的层级也相应更新
            grandchild_data = self.manager.get_detail(self.grandchild_id)
            self.assertEqual(grandchild_data['level'], 1)  # 孙子节点层级应为1

    def test_get_full_tree_after_move(self):
        """测试移动节点后获取完整树形结构"""
        with patch('app.quickpick.panel.QTreeWidget'), \
             patch('app.quickpick.panel.QTreeWidgetItem'), \
             patch('app.quickpick.panel.QuickPickItemDelegate'):
            
            # Mock quickpick_list
            mock_quickpick_list = Mock()
            mock_quickpick_list.topLevelItemCount.return_value = 0
            
            # 创建面板实例
            panel = QuickPickPanel(self.manager)
            panel.quickpick_list = mock_quickpick_list
            
            # 先移动一个节点
            panel._update_item_hierarchy(self.child1_id, self.root2_id, -1, None)
            
            # 获取完整树形结构
            tree = self.manager.get_full_tree()
            
            # 验证树形结构正确性
            # 查找根节点2
            root2 = None
            for item in tree:
                if item['id'] == self.root2_id:
                    root2 = item
                    break
            
            # 根节点2现在应该有一个子节点（child1）
            self.assertIsNotNone(root2)
            if root2 is not None:
                self.assertIn('children', root2)
                self.assertEqual(len(root2['children']), 1)
                
                # 验证子节点是child1
                moved_child = root2['children'][0]
                self.assertEqual(moved_child['id'], self.child1_id)
                
                # 验证孙子节点也在正确位置
                self.assertIn('children', moved_child)
                self.assertEqual(len(moved_child['children']), 1)
                self.assertEqual(moved_child['children'][0]['id'], self.grandchild_id)


if __name__ == '__main__':
    unittest.main()