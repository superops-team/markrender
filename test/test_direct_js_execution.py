#!/usr/bin/env python3
"""
测试直接执行JavaScript的简化通信方式
"""

import sys
import os
import json
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit
from PySide6.QtCore import QTimer, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage

from app.editor.backend_interface import BackendInterface
from utils import logger

class DirectJSTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("直接JavaScript执行测试")
        self.setGeometry(100, 100, 1000, 700)
        
        # 创建通信管理器
        self.backend = BackendInterface("markdown")
        
        # 创建UI
        self.setup_ui()
        
        # 延迟创建页面
        QTimer.singleShot(100, self.create_page)
    
    def setup_ui(self):
        """设置UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 创建Web视图
        self.web_view = QWebEngineView()
        
        # 控制按钮
        self.test_btn = QPushButton("测试设置内容")
        self.test_btn.clicked.connect(self.test_set_content)
        
        self.get_btn = QPushButton("测试获取内容")
        self.get_btn.clicked.connect(self.test_get_content)
        
        # 日志输出
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        
        # 添加控件到布局
        layout.addWidget(self.web_view)
        layout.addWidget(self.test_btn)
        layout.addWidget(self.get_btn)
        layout.addWidget(self.log_output)
    
    def log_message(self, message):
        """记录消息到日志输出"""
        self.log_output.append(message)
        print(f"[TEST] {message}")
    
    def create_page(self):
        """创建页面"""
        try:
            # 设置页面
            page = QWebEnginePage(self.web_view)
            self.web_view.setPage(page)
            
            # 设置后端接口
            self.backend.set_page(page)
            
            # 加载HTML文件
            html_path = os.path.abspath("app/editor/plugins/markdown/index.html")
            if os.path.exists(html_path):
                self.web_view.load(QUrl.fromLocalFile(html_path))
                self.web_view.loadFinished.connect(self.on_page_loaded)
                self.log_message(f"加载页面: {html_path}")
            else:
                self.log_message(f"页面文件不存在: {html_path}")
                
        except Exception as e:
            self.log_message(f"创建页面时出错: {e}")
    
    def on_page_loaded(self, success):
        """页面加载完成"""
        if success:
            self.log_message("页面加载成功")
        else:
            self.log_message("页面加载失败")
    
    def test_set_content(self):
        """测试设置内容"""
        self.log_message("测试设置内容...")
        
        test_content = "# 直接JavaScript执行测试\n\n这是通过直接执行JavaScript设置的内容！"
        
        # 使用新的send_message方法
        success = self.backend.send_message("setValue", {"content": test_content})
        
        if success:
            self.log_message("✅ 内容设置成功")
        else:
            self.log_message("❌ 内容设置失败")
    
    def test_get_content(self):
        """测试获取内容"""
        self.log_message("测试获取内容...")
        
        def handle_content(content):
            self.log_message(f"获取到的内容: {content[:100]}...")
        
        # 使用新的send_message方法获取内容
        success = self.backend.send_message("getContent", {}, handle_content)
        
        if success:
            self.log_message("✅ 内容获取请求已发送")
        else:
            self.log_message("❌ 内容获取请求发送失败")

def main():
    """主函数"""
    print("启动直接JavaScript执行测试...")
    
    app = QApplication(sys.argv)
    window = DirectJSTestWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()