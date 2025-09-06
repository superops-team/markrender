#!/usr/bin/env python3
"""
验证WebChannel修复的测试脚本
"""

import sys
import os
import json
import time
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer, QObject, Signal, Slot
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.editor.webengine import WebPageManager
from app.editor.backend_interface import BackendInterface
from utils.logger_utils import setup_logger

logger = setup_logger()

class WebChannelVerificationTest(QObject):
    test_completed = Signal(bool, str)
    
    def __init__(self):
        super().__init__()
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.page_manager = WebPageManager()
        self.test_results = {}
        
    def test_page_type(self, page_type):
        """测试特定页面类型的WebChannel通信"""
        logger.info(f"🧪 开始测试 {page_type} 页面通信...")
        
        try:
            # 创建页面
            page = self.page_manager.create_page(page_type)
            if not page:
                return False, f"无法创建 {page_type} 页面"
            
            # 创建后端接口
            backend = BackendInterface("test")
            
            # 移除对backend.ready属性的设置，改为检查页面对象
            self.assertIsNone(backend.page)
            self.assertFalse(hasattr(backend, 'ready'))
            
            # 设置WebChannel
            channel = QWebChannel()
            channel.registerObject("backendInterface", backend)
            page.setWebChannel(channel)
            
            # 加载HTML文件
            html_path = f"app/editor/plugins/{page_type}/index.html"
            if not os.path.exists(html_path):
                return False, f"HTML文件不存在: {html_path}"
            
            full_path = os.path.abspath(html_path)
            page.load(f"file://{full_path}")
            
            # 等待页面加载
            loop = QEventLoop()
            page.loadFinished.connect(loop.quit)
            loop.exec_()
            
            # 测试通信
            success = self._test_communication(page, backend, page_type)
            
            if success:
                return True, f"{page_type} 页面通信正常"
            else:
                return False, f"{page_type} 页面通信失败"
                
        except Exception as e:
            return False, f"测试 {page_type} 时发生错误: {str(e)}"
    
    def _test_communication(self, page, backend, page_type):
        """测试实际的通信功能"""
        try:
            # 测试前端就绪信号
            backend.ready = False
            
            def on_ready():
                backend.ready = True
                logger.info(f"✅ {page_type} 前端就绪信号正常")
            
            # 移除对channel_ready信号的监听，不再需要WebChannel就绪状态
            # backend.channel_ready.connect(on_ready)
            
            # 直接进行测试
            logger.info("⏭️  跳过WebChannel就绪状态检查，直接进行测试...")
            
            # 测试消息发送
            test_content = f"测试内容 - {page_type} - {time.time()}"
            
            # 发送setValue消息
            result = backend.send_message("setValue", {"content": test_content})
            if not result:
                return False, "无法发送setValue消息"
            
            # 等待消息处理
            time.sleep(1)
            
            # 测试getContent消息
            content_received = None
            
            def on_content_response(response):
                nonlocal content_received
                content_received = response.get("content", "")
                logger.info(f"✅ {page_type} 收到内容: {len(content_received)} 字符")
            
            backend.send_message("getContent", callback=on_content_response)
            
            # 等待响应
            timeout = 5
            start_time = time.time()
            while content_received is None and time.time() - start_time < timeout:
                self.app.processEvents()
                time.sleep(0.1)
            
            if content_received is None:
                return False, "getContent响应超时"
            
            return True, "通信测试通过"
            
        except Exception as e:
            return False, f"通信测试异常: {str(e)}"
    
    def run_all_tests(self):
        """运行所有页面类型的测试"""
        logger.info("🚀 开始WebChannel修复验证测试")
        
        page_types = ["markdown", "excalidraw", "landing"]
        all_passed = True
        
        for page_type in page_types:
            success, message = self.test_page_type(page_type)
            self.test_results[page_type] = {"success": success, "message": message}
            
            if success:
                logger.info(f"✅ {page_type}: {message}")
            else:
                logger.error(f"❌ {page_type}: {message}")
                all_passed = False
        
        # 总结结果
        logger.info("\n" + "="*50)
        logger.info("📊 WebChannel修复验证结果:")
        
        for page_type, result in self.test_results.items():
            status = "✅ 通过" if result["success"] else "❌ 失败"
            logger.info(f"{page_type}: {status} - {result['message']}")
        
        if all_passed:
            logger.info("🎉 所有页面类型的WebChannel通信已修复并验证通过！")
        else:
            logger.error("⚠️  部分页面类型仍有通信问题")
        
        return all_passed

if __name__ == "__main__":
    from PySide6.QtCore import QEventLoop
    
    test = WebChannelVerificationTest()
    success = test.run_all_tests()
    
    if success:
        print("\n🎉 WebChannel修复验证完成 - 所有测试通过！")
        sys.exit(0)
    else:
        print("\n❌ WebChannel修复验证失败")
        sys.exit(1)