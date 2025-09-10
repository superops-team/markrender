#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebPageManager功能测试用例
测试页面管理器的预加载、页面创建、切换等功能
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

from app.editor.webengine import WebPageManager, PageType, PageConfig, PageInstance
from app.editor.backend_interface import BackendInterface


class TestWebPageManager(unittest.TestCase):
    """WebPageManager测试类"""
    
    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        # 创建QApplication实例（Qt测试需要）
        if not QApplication.instance():
            cls.app = QApplication(sys.argv)
        else:
            cls.app = QApplication.instance()
    
    def setUp(self):
        """每个测试方法前的设置"""
        self.page_manager = WebPageManager()
        self.backend_interface = BackendInterface("test")
    
    def tearDown(self):
        """每个测试方法后的清理"""
        # 清理页面实例
        for page_type in list(self.page_manager.page_instances.keys()):
            self.page_manager.remove_page(page_type)
    
    def test_page_type_enum(self):
        """测试页面类型枚举"""
        self.assertIn("markdown", PageType.all_types())
        self.assertIn("excalidraw", PageType.all_types())
        self.assertIn("landing", PageType.all_types())
    
    def test_page_config_creation(self):
        """测试页面配置创建"""
        config = PageConfig(
            page_type="markdown",
            backend_interface=self.backend_interface,
            preload=True,
            cache_enabled=True,
            performance_mode=True
        )
        
        self.assertEqual(config.page_type, "markdown")
        self.assertEqual(config.backend_interface, self.backend_interface)
        self.assertTrue(config.preload)
        self.assertTrue(config.cache_enabled)
        self.assertTrue(config.performance_mode)
    
    def test_page_instance_creation(self):
        """测试页面实例创建"""
        view = QWebEngineView()
        page_instance = PageInstance("markdown", view, self.backend_interface)
        
        self.assertEqual(page_instance.page_type, "markdown")
        self.assertEqual(page_instance.view, view)
        self.assertEqual(page_instance.backend_interface, self.backend_interface)
        self.assertFalse(page_instance.ready)
        self.assertEqual(page_instance.content, "")
    
    def test_page_instance_ready_state(self):
        """测试页面实例就绪状态"""
        view = QWebEngineView()
        page_instance = PageInstance("markdown", view)
        
        self.assertFalse(page_instance.is_ready())
        page_instance.set_ready(True)
        self.assertTrue(page_instance.is_ready())
        page_instance.set_ready(False)
        self.assertFalse(page_instance.is_ready())
    
    def test_page_instance_content(self):
        """测试页面实例内容管理"""
        view = QWebEngineView()
        page_instance = PageInstance("markdown", view)
        
        test_content = "# Test Content\nThis is a test."
        page_instance.set_content(test_content)
        self.assertEqual(page_instance.get_content(), test_content)
    
    def test_create_page(self):
        """测试创建页面"""
        with patch('app.editor.webengine.CustomWebEnginePage.initialize_web_channel'):
            page_instance = self.page_manager.create_page("markdown", self.backend_interface)
            
            self.assertIsNotNone(page_instance)
            self.assertIn("markdown", self.page_manager.page_instances)
            self.assertEqual(self.page_manager.page_instances["markdown"], page_instance)
            self.assertEqual(page_instance.page_type, "markdown")
    
    def test_get_or_create_page(self):
        """测试获取或创建页面"""
        with patch('app.editor.webengine.CustomWebEnginePage.initialize_web_channel'):
            # 第一次创建
            page_instance1 = self.page_manager.get_or_create_page("markdown", self.backend_interface)
            self.assertIsNotNone(page_instance1)
            
            # 第二次获取（应该复用现有实例）
            page_instance2 = self.page_manager.get_or_create_page("markdown", self.backend_interface)
            self.assertEqual(page_instance1, page_instance2)
    
    def test_preload_page_type(self):
        """测试预加载页面类型"""
        with patch('app.editor.webengine.CustomWebEnginePage.initialize_web_channel'):
            with patch.object(self.page_manager, 'load_html') as mock_load_html:
                self.page_manager.preload_page_type("markdown", self.backend_interface)
                
                # 验证页面实例已创建
                self.assertIn("markdown", self.page_manager.page_instances)
                
                # 验证load_html被调用
                mock_load_html.assert_called_once_with("markdown", "markdown/index.html")
    
    def test_switch_to_page(self):
        """测试页面切换"""
        with patch('app.editor.webengine.CustomWebEnginePage.initialize_web_channel'):
            # 创建两个页面
            markdown_page = self.page_manager.create_page("markdown", self.backend_interface)
            landing_page = self.page_manager.create_page("landing", self.backend_interface)
            
            # 切换到markdown页面
            result = self.page_manager.switch_to_page("markdown")
            self.assertTrue(result)
            self.assertEqual(self.page_manager.current_page_type, "markdown")
            
            # 切换到landing页面
            result = self.page_manager.switch_to_page("landing")
            self.assertTrue(result)
            self.assertEqual(self.page_manager.current_page_type, "landing")
    
    def test_remove_page(self):
        """测试移除页面"""
        with patch('app.editor.webengine.CustomWebEnginePage.initialize_web_channel'):
            # 创建页面
            page_instance = self.page_manager.create_page("markdown", self.backend_interface)
            self.assertIn("markdown", self.page_manager.page_instances)
            
            # 移除页面
            result = self.page_manager.remove_page("markdown")
            self.assertTrue(result)
            self.assertNotIn("markdown", self.page_manager.page_instances)
    
    def test_set_backend_interface(self):
        """测试设置后端接口"""
        with patch('app.editor.webengine.CustomWebEnginePage.initialize_web_channel'):
            # 创建页面
            page_instance = self.page_manager.create_page("markdown")
            self.assertIsNone(page_instance.backend_interface)
            
            # 设置后端接口
            result = self.page_manager.set_backend_interface("markdown", self.backend_interface)
            self.assertTrue(result)
            self.assertEqual(page_instance.backend_interface, self.backend_interface)
    
    def test_get_backend_interface(self):
        """测试获取后端接口"""
        with patch('app.editor.webengine.CustomWebEnginePage.initialize_web_channel'):
            # 创建页面并设置后端接口
            page_instance = self.page_manager.create_page("markdown", self.backend_interface)
            
            # 获取后端接口
            backend_interface = self.page_manager.get_backend_interface("markdown")
            self.assertEqual(backend_interface, self.backend_interface)
            
            # 获取不存在页面的后端接口
            backend_interface = self.page_manager.get_backend_interface("nonexistent")
            self.assertIsNone(backend_interface)


if __name__ == '__main__':
    unittest.main()