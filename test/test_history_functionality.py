# -*- coding: utf-8 -*-
import unittest
import tempfile
import os
from db.markrender_manager import MarkRenderManager
from db.models import MarkRenderData, MarkRenderChangeHistory
from db.db_manager import SingletonEngine


class TestHistoryFunctionality(unittest.TestCase):
    def setUp(self):
        # 创建临时数据库用于测试
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, 'test_data.db')
        self.manager = MarkRenderManager(self.db_path)
        
    def tearDown(self):
        # 清理临时文件
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)
    
    def test_create_item_with_history(self):
        """测试创建项目时是否正确记录历史"""
        # 创建新项目
        item_id = self.manager.save_item(
            title='Test Document',
            content='# Hello World\nThis is a test document.',
            tags='test,document',
            page_type='markdown'
        )
        
        # 验证项目已创建
        self.assertIsNotNone(item_id)
        self.assertGreater(item_id, 0)
        
        # 验证历史记录已创建
        history_records = self.manager.get_change_history(item_id)
        self.assertEqual(len(history_records), 1)
        
        # 验证历史记录内容
        history_record = history_records[0]
        self.assertEqual(history_record.change_type, 'content_create')
        self.assertEqual(history_record.old_content, '')
        self.assertEqual(history_record.new_content, '# Hello World\nThis is a test document.')
        
    def test_update_item_with_history(self):
        """测试更新项目时是否正确记录历史"""
        # 创建新项目
        item_id = self.manager.save_item(
            title='Test Document',
            content='# Hello World\nThis is a test document.',
            tags='test,document',
            page_type='markdown'
        )
        
        # 更新项目内容
        updated_id = self.manager.save_item(
            id=item_id,
            title='Test Document Updated',
            content='# Hello World\nThis is an updated test document.',
            tags='test,document,updated',
            page_type='markdown'
        )
        
        # 验证项目已更新
        self.assertEqual(updated_id, item_id)
        
        # 验证历史记录已创建
        history_records = self.manager.get_change_history(item_id)
        # 应该有2条记录：1条创建记录 + 1条更新记录
        self.assertEqual(len(history_records), 2)
        
        # 验证最新的历史记录内容
        latest_history = history_records[0]  # 最新的记录在前面
        self.assertEqual(latest_history.change_type, 'content_update')
        self.assertEqual(latest_history.old_content, '# Hello World\nThis is a test document.')
        self.assertEqual(latest_history.new_content, '# Hello World\nThis is an updated test document.')
        
    def test_update_title_with_history(self):
        """测试更新标题时是否正确记录历史"""
        # 创建新项目
        item_id = self.manager.save_item(
            title='Test Document',
            content='# Hello World\nThis is a test document.',
            tags='test,document',
            page_type='markdown'
        )
        
        # 更新标题
        self.manager.update_title(item_id, 'Updated Test Document')
        
        # 验证历史记录已创建
        history_records = self.manager.get_change_history(item_id)
        # 应该有2条记录：1条创建记录 + 1条标题更新记录
        self.assertEqual(len(history_records), 2)
        
        # 验证最新的历史记录内容
        latest_history = history_records[0]  # 最新的记录在前面
        self.assertEqual(latest_history.change_type, 'title_update')
        self.assertEqual(latest_history.old_content, 'Test Document')
        self.assertEqual(latest_history.new_content, 'Updated Test Document')
        
    def test_no_history_on_unchanged_content(self):
        """测试内容未变化时不记录历史"""
        # 创建新项目
        item_id = self.manager.save_item(
            title='Test Document',
            content='# Hello World\nThis is a test document.',
            tags='test,document',
            page_type='markdown'
        )
        
        # 再次保存相同内容
        updated_id = self.manager.save_item(
            id=item_id,
            title='Test Document',
            content='# Hello World\nThis is a test document.',
            tags='test,document',
            page_type='markdown'
        )
        
        # 验证项目ID相同
        self.assertEqual(updated_id, item_id)
        
        # 验证历史记录数量未增加（仍只有创建记录）
        history_records = self.manager.get_change_history(item_id)
        self.assertEqual(len(history_records), 1)
        self.assertEqual(history_records[0].change_type, 'content_create')


if __name__ == '__main__':
    unittest.main()