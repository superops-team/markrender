#!/usr/bin/env python3
"""
简化的WebChannel双向通信测试
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

class SimpleBidirectionalTest(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("简化双向通信测试")
        self.setGeometry(100, 100, 1000, 700)
        
        # 创建页面管理器和通信管理器
        self.page_manager = WebPageManager()
        self.web_comm = WebCommunicationManager("markdown")
        
        # 设置测试处理器
        self.setup_handlers()
        
        # 创建UI
        self.setup_ui()
        
        # 延迟创建页面
        QTimer.singleShot(100, self.create_page)
    
    def setup_handlers(self):
        """设置消息处理器"""
        def handle_auto_save(data):
            content = data.get('content', '')
            self.log_message(f"✅ 收到自动保存请求，内容长度: {len(content)}")
            return {"success": True, "saved": True}
        
        # 注册处理器
        self.web_comm.register_python_handler('autoSave', handle_auto_save)
        self.web_comm.channel_ready.connect(lambda: self.log_message("🎉 WebChannel通道就绪！"))
    
    def setup_ui(self):
        """创建UI"""
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # 测试按钮
        test_btn = QPushButton("测试JS自动保存")
        test_btn.clicked.connect(self.test_js_autosave)
        layout.addWidget(test_btn)
        
        # 日志区域
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        layout.addWidget(self.log_text)
        
        # 页面管理器
        layout.addWidget(self.page_manager)
        
        self.setCentralWidget(central_widget)
    
    def log_message(self, message):
        """记录日志"""
        self.log_text.append(message)
        logger.info(message)
    
    def create_page(self):
        """创建页面"""
        self.log_message("🔧 创建测试页面...")
        
        view = self.page_manager.create_page("markdown", self.web_comm)
        if view:
            self.web_comm.set_page(view.page())
            self.log_message("✅ 页面创建并绑定成功")
            
            success = self.page_manager.load_html("markdown", "markdown/index.html", self.on_loaded)
            if success:
                self.log_message("📄 开始加载HTML...")
        else:
            self.log_message("❌ 页面创建失败")
    
    def on_loaded(self, success):
        """页面加载完成"""
        if success:
            self.log_message("✅ 页面加载成功")
            QTimer.singleShot(2000, self.run_test)
        else:
            self.log_message("❌ 页面加载失败")
    
    def run_test(self):
        """运行测试"""
        if self.web_comm.ready:
            self.log_message("🚀 开始测试Python→JS消息...")
            success = self.web_comm.send_message('setValue', {
                'content': '# WebChannel修复成功！\\n\\n通信正常工作中...'
            })
            self.log_message("✅ 消息发送成功" if success else "❌ 消息发送失败")
        else:
            self.log_message("⏳ WebChannel未就绪")
    
    def test_js_autosave(self):
        """测试JS自动保存"""
        self.log_message("🔄 触发JS自动保存测试...")
        
        js_code = """
        if (window.WebChannelManager && window.WebChannelManager.sendToPython) {
            window.WebChannelManager.sendToPython('autoSave', {
                content: '来自前端的测试内容',
                timestamp: new Date().toISOString()
            });
            '自动保存请求已发送';
        } else {
            'WebChannelManager不可用';
        }
        """
        
        self.web_comm.page.runJavaScript(js_code, lambda result: 
            self.log_message(f"📡 JS执行结果: {result}"))

def main():
    app = QApplication(sys.argv)
    window = SimpleBidirectionalTest()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()