"""
WebEngine重构测试用例
验证页面-通道绑定架构的正确性和功能完整性
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch

# 添加项目根目录到sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# 在导入Qt相关模块之前设置环境变量
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from app.editor.webengine import PageType, PageConfig, PageChannelBinding
from app.editor.backend_interface import BackendInterface, CommonHandlers
from app.editor.handler_interface import HandlerInterface, DefaultHandler
from app.editor.request_model import RequestModel
from app.editor.common_handlers import CommonHandlers as CommonHandlersClass
from app.editor.js_scripts import JSScriptManager

class TestWebEngineRefactor(unittest.TestCase):
    """WebEngine重构测试类"""
    
    def setUp(self):
        """测试初始化"""
        pass
    
    def tearDown(self):
        """测试清理"""
        pass
    
    def test_page_type_enum(self):
        """测试页面类型枚举"""
        # 验证页面类型枚举的正确性
        self.assertEqual(PageType.MARKDOWN, "markdown")
        self.assertEqual(PageType.EXCALIDRAW, "excalidraw")
        self.assertEqual(PageType.LANDING, "landing")
        
        # 验证获取所有类型的方法
        all_types = PageType.all_types()
        self.assertIn("markdown", all_types)
        self.assertIn("excalidraw", all_types)
        self.assertIn("landing", all_types)
    
    def test_page_config(self):
        """测试页面配置类"""
        config = PageConfig(
            page_type="markdown",
            preload=True,
            cache_enabled=False,
            performance_mode=False
        )
        
        self.assertEqual(config.page_type, "markdown")
        self.assertTrue(config.preload)
        self.assertFalse(config.cache_enabled)
        self.assertFalse(config.performance_mode)
    
    def test_page_channel_binding(self):
        """测试页面-通道绑定类"""
        # 创建模拟对象
        mock_view = Mock()
        mock_channel = Mock()
        
        # 创建绑定
        binding = PageChannelBinding("markdown", mock_view, mock_channel)
        
        # 验证绑定属性
        self.assertEqual(binding.page_type, "markdown")
        self.assertEqual(binding.view, mock_view)
        self.assertEqual(binding.channel, mock_channel)
        self.assertFalse(binding.is_ready)
        
        # 验证设置就绪状态
        binding.set_ready(True)
        self.assertTrue(binding.is_ready)
    
    def test_backend_interface_creation(self):
        """测试BackendInterface创建"""
        backend_interface = BackendInterface("markdown")
        
        # 验证属性
        self.assertEqual(backend_interface.page_type, "markdown")
        self.assertFalse(backend_interface.ready)
        
        # 验证通用handlers已注册
        common_handlers = CommonHandlersClass.get_common_handlers()
        for action in common_handlers.keys():
            self.assertIn(action, backend_interface.handlers)
    
    def test_common_handlers(self):
        """测试通用handlers"""
        # 获取通用handlers
        common_handlers = CommonHandlersClass.get_common_handlers()
        
        # 验证必要的handlers存在
        self.assertIn('frontendReady', common_handlers)
        self.assertIn('reportError', common_handlers)
        self.assertIn('setValue', common_handlers)
        self.assertIn('getContent', common_handlers)
        
        # 测试handler执行
        result = common_handlers['frontendReady']({})
        self.assertTrue(result['success'])
        
        result = common_handlers['setValue']({'content': 'test'})
        self.assertTrue(result['success'])
        
        result = common_handlers['getContent']({})
        self.assertTrue(result['success'])
    
    def test_handler_interface(self):
        """测试处理器接口"""
        # 测试抽象接口
        with self.assertRaises(NotImplementedError):
            handler = HandlerInterface("test")
            handler.handle({})
        
        # 测试默认处理器
        def test_func(data):
            return {"result": "success"}
        
        handler = DefaultHandler("test", test_func)
        result = handler.handle({})
        self.assertEqual(result["result"], "success")
        
        # 测试异常处理
        def error_func(data):
            raise Exception("Test error")
        
        handler = DefaultHandler("test", error_func)
        result = handler.handle({})
        self.assertFalse(result['success'])
        self.assertIn('error', result)
    
    def test_request_model(self):
        """测试请求模型"""
        # 测试创建请求模型
        request = RequestModel("testAction", {"key": "value"}, "12345")
        self.assertEqual(request.action, "testAction")
        self.assertEqual(request.data, {"key": "value"})
        self.assertEqual(request.request_id, "12345")
        
        # 测试从字典创建
        data = {
            "action": "testAction2",
            "data": {"key2": "value2"},
            "requestId": "67890"
        }
        request = RequestModel.from_dict(data)
        self.assertEqual(request.action, "testAction2")
        self.assertEqual(request.data, {"key2": "value2"})
        self.assertEqual(request.request_id, "67890")

if __name__ == '__main__':
    unittest.main()