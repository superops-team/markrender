#!/usr/bin/env python3
"""
测试WebChannel通信修复效果
验证QStackedWidget重构后的前后端通信是否正常工作
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit
from PySide6.QtCore import QTimer
from app.editor.webengine import WebPageManager
from app.editor.channel import WebCommunicationManager
from utils import logger

class WebChannelTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WebChannel通信修复测试")
        self.setGeometry(100, 100, 1000, 700)
        
        # 创建页面管理器和通信管理器
        self.page_manager = WebPageManager()
        self.web_comm = WebCommunicationManager("markdown")
        
        # 设置测试处理器
        self.setup_test_handlers()
        
        # 创建UI
        self.setup_ui()
        
        # 延迟创建页面，确保UI已初始化
        QTimer.singleShot(100, self.create_test_page)
    
    def setup_test_handlers(self):
        """设置测试用的消息处理器"""
        def handle_test_message(data):
            self.log_message(f"✅ 收到测试消息: {data}")
            return {"status": "success", "message": "测试消息处理成功"}
        
        def handle_auto_save(data):
            self.log_message(f"✅ 收到自动保存请求: {data}")
            return {"status": "success", "saved": True}
        
        # 注册处理器
        self.web_comm.register_python_handler('test', handle_test_message)
        self.web_comm.register_python_handler('autoSave', handle_auto_save)
        
        # 监听通道就绪信号
        self.web_comm.channel_ready.connect(self.on_channel_ready)
    
    def setup_ui(self):
        """创建测试界面"""
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # 创建日志显示区域
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        layout.addWidget(self.log_text)
        
        # 创建测试按钮
        test_btn = QPushButton("测试发送消息到前端")
        test_btn.clicked.connect(self.test_send_message)
        layout.addWidget(test_btn)
        
        # 页面管理器将在这里显示
        layout.addWidget(self.page_manager)
        
        self.setCentralWidget(central_widget)
    
    def log_message(self, message):
        """记录日志消息"""
        self.log_text.append(message)
        logger.info(message)
    
    def create_test_page(self):
        """创建测试页面"""
        self.log_message("🔧 开始创建测试页面...")
        
        # 创建markdown页面
        view = self.page_manager.create_page(
            page_type="markdown",
            backend_interface=self.web_comm
        )
        
        if view:
            self.log_message("✅ 页面创建成功")
            
            # 手动设置页面对象，确保通信管理器关联正确
            self.web_comm.set_page(view.page())
            self.log_message("✅ 通信管理器页面对象已设置")
            
            # 加载HTML文件
            success = self.page_manager.load_html(
                "markdown", 
                "markdown/index.html",
                callback=self.on_page_loaded
            )
            
            if success:
                self.log_message("📄 开始加载HTML文件...")
            else:
                self.log_message("❌ HTML文件加载失败")
        else:
            self.log_message("❌ 页面创建失败")
    
    def on_page_loaded(self, success):
        """页面加载完成回调"""
        if success:
            self.log_message("✅ HTML页面加载成功")
            # 延迟测试WebChannel，给前端初始化时间
            QTimer.singleShot(1000, self.test_webchannel)
        else:
            self.log_message("❌ HTML页面加载失败")
    
    def on_channel_ready(self):
        """WebChannel通道就绪回调"""
        self.log_message("🎉 WebChannel通道就绪！")
    
    def test_webchannel(self):
        """测试WebChannel连接"""
        self.log_message("🧪 开始测试WebChannel连接...")
        
        # 检查页面对象是否设置
        if self.web_comm.page:
            self.log_message("✅ WebCommunicationManager页面对象已设置")
        else:
            self.log_message("❌ WebCommunicationManager页面对象未设置")
            return
        
        # 检查通道是否就绪
        if self.web_comm.ready:
            self.log_message("✅ WebChannel通道已就绪")
        else:
            self.log_message("⏳ WebChannel通道尚未就绪，等待前端初始化...")
            # 再次延迟测试
            QTimer.singleShot(2000, self.test_webchannel)
            return
        
        # 测试JavaScript函数存在性
        js_check_code = """
        (function() {
            if (typeof window.handlePythonMessage === 'function') {
                return 'handlePythonMessage函数存在';
            } else {
                return 'handlePythonMessage函数不存在';
            }
        })();
        """
        
        def on_js_check(result):
            self.log_message(f"🔍 JavaScript检查结果: {result}")
            if "存在" in str(result):
                self.test_message_sending()
            else:
                self.log_message("❌ JavaScript函数检查失败，无法继续测试")
        
        self.web_comm.page.runJavaScript(js_check_code, on_js_check)
    
    def test_message_sending(self):
        """测试消息发送"""
        self.log_message("📨 测试发送消息到前端...")
        
        # 发送测试消息
        success = self.web_comm.send_message(
            'setValue', 
            {'content': '# WebChannel通信测试\n\n这是通过WebChannel发送的测试内容！'}
        )
        
        if success:
            self.log_message("✅ 消息发送成功")
        else:
            self.log_message("❌ 消息发送失败")
    
    def test_send_message(self):
        """按钮点击测试"""
        self.log_message("🔄 手动测试发送消息...")
        self.test_message_sending()

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = WebChannelTestWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()