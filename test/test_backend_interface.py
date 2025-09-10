#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BackendInterface功能测试用例
测试后端接口的处理器注册、消息发送、请求分发等功能
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtCore import QObject
from app.editor.backend_interface import BackendInterface, RequestModel


class TestBackendInterface(unittest.TestCase):
    """BackendInterface测试类"""
    
    def setUp(self):
        """每个测试方法前的设置"""
        self.backend_interface = BackendInterface("test")
        # 创建模拟的页面对象
        self.mock_page = Mock()
        self.backend_interface.set_page(self.mock_page)
        # 设置为就绪状态
        self.backend_interface.ready = True
    
    def tearDown(self):
        """每个测试方法后的清理"""
        self.backend_interface.cleanup()
    
    def test_backend_interface_creation(self):
        """测试后端接口创建"""
        self.assertEqual(self.backend_interface.page_type, "test")
        self.assertFalse(self.backend_interface.ready)
        self.assertIsNotNone(self.backend_interface.handlers)
        self.assertIsNotNone(self.backend_interface.web_callbacks)
        self.assertIsNone(self.backend_interface.page)
    
    def test_set_page(self):
        """测试设置页面"""
        mock_page = Mock()
        self.backend_interface.set_page(mock_page)
        self.assertEqual(self.backend_interface.page, mock_page)
    
    def test_register_handler(self):
        """测试注册处理器"""
        def test_handler(data):
            return {"result": "test"}
        
        self.backend_interface.register_handler("test_action", test_handler)
        self.assertIn("test_action", self.backend_interface.handlers)
        
        handler, is_async = self.backend_interface.handlers["test_action"]
        self.assertEqual(handler, test_handler)
        self.assertFalse(is_async)
    
    def test_register_async_handler(self):
        """测试注册异步处理器"""
        async def test_async_handler(data):
            return {"result": "async_test"}
        
        self.backend_interface.register_handler("async_action", test_async_handler, is_async=True)
        self.assertIn("async_action", self.backend_interface.handlers)
        
        handler, is_async = self.backend_interface.handlers["async_action"]
        self.assertEqual(handler, test_async_handler)
        self.assertTrue(is_async)
    
    def test_send_message_success(self):
        """测试发送消息成功"""
        self.mock_page.runJavaScript = Mock()
        
        result = self.backend_interface.send_message("test_action", {"data": "test"})
        self.assertTrue(result)
        self.mock_page.runJavaScript.assert_called_once()
    
    def test_send_message_no_page(self):
        """测试页面未设置时发送消息"""
        self.backend_interface.page = None
        result = self.backend_interface.send_message("test_action", {"data": "test"})
        self.assertFalse(result)
    
    def test_send_message_not_ready(self):
        """测试通道未就绪时发送消息"""
        self.backend_interface.ready = False
        result = self.backend_interface.send_message("test_action", {"data": "test"})
        self.assertFalse(result)
    
    def test_send_message_with_callback(self):
        """测试带回调的发送消息"""
        self.mock_page.runJavaScript = Mock()
        
        def test_callback(response):
            pass
        
        result = self.backend_interface.send_message("test_action", {"data": "test"}, test_callback)
        self.assertTrue(result)
        self.assertEqual(len(self.backend_interface.web_callbacks), 1)
    
    def test_request_model_creation(self):
        """测试请求模型创建"""
        request = RequestModel("test_action", {"test": "data"}, "req_123")
        self.assertEqual(request.action, "test_action")
        self.assertEqual(request.data, {"test": "data"})
        self.assertEqual(request.request_id, "req_123")
    
    def test_request_model_from_dict(self):
        """测试从字典创建请求模型"""
        data = {
            "action": "test_action",
            "data": {"test": "data"},
            "requestId": "req_123"
        }
        request = RequestModel.from_dict(data)
        self.assertEqual(request.action, "test_action")
        self.assertEqual(request.data, {"test": "data"})
        self.assertEqual(request.request_id, "req_123")
    
    def test_dispatch_request_sync(self):
        """测试同步请求分发"""
        def test_handler(data):
            return {"result": "success", "data": data}
        
        self.backend_interface.register_handler("test_action", test_handler)
        
        request_json = '{"action": "test_action", "data": {"input": "test"}, "requestId": "req_123"}'
        response_json = self.backend_interface.dispatch_request(request_json)
        
        response = eval(response_json)  # 简单解析响应（实际应该是json.loads）
        self.assertTrue(response["success"])
        self.assertEqual(response["requestId"], "req_123")
        self.assertEqual(response["result"], "success")
        self.assertEqual(response["data"], {"input": "test"})
    
    def test_dispatch_request_async(self):
        """测试异步请求分发"""
        def test_async_handler(data):
            return {"result": "async_success"}
        
        self.backend_interface.register_handler("async_action", test_async_handler, is_async=True)
        
        request_json = '{"action": "async_action", "data": {"input": "test"}, "requestId": "req_123"}'
        response_json = self.backend_interface.dispatch_request(request_json)
        
        response = eval(response_json)  # 简单解析响应
        self.assertTrue(response["success"])
        self.assertEqual(response["requestId"], "req_123")
        self.assertEqual(response["message"], "Request accepted for async processing")
    
    def test_dispatch_request_unknown_action(self):
        """测试未知动作的请求分发"""
        request_json = '{"action": "unknown_action", "data": {}, "requestId": "req_123"}'
        response_json = self.backend_interface.dispatch_request(request_json)
        
        response = eval(response_json)  # 简单解析响应
        self.assertFalse(response["success"])
        self.assertEqual(response["error"], "Unknown action: unknown_action")
    
    def test_dispatch_request_missing_request_id(self):
        """测试缺少请求ID的请求分发"""
        request_json = '{"action": "test_action", "data": {}}'
        response_json = self.backend_interface.dispatch_request(request_json)
        
        response = eval(response_json)  # 简单解析响应
        self.assertFalse(response["success"])
        self.assertEqual(response["error"], "Missing requestId")
    
    def test_cleanup(self):
        """测试清理资源"""
        # 添加一些测试数据
        self.backend_interface.web_callbacks["test"] = Mock()
        self.backend_interface.handlers["test"] = Mock()
        self.backend_interface.item_map["test"] = Mock()
        self.backend_interface.page = Mock()
        self.backend_interface.ready = True
        
        # 执行清理
        self.backend_interface.cleanup()
        
        # 验证清理结果
        self.assertEqual(len(self.backend_interface.web_callbacks), 0)
        self.assertEqual(len(self.backend_interface.handlers), 0)
        self.assertEqual(len(self.backend_interface.item_map), 0)
        self.assertIsNone(self.backend_interface.page)
        self.assertFalse(self.backend_interface.ready)


if __name__ == '__main__':
    unittest.main()