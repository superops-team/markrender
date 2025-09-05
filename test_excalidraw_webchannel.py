#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Excalidraw WebChannel测试脚本
"""

import sys
import os
import time

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.editor.webengine import WebPageManager
from app.editor.backend_interface import WebCommunicationManager
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit
from PySide6.QtCore import QTimer

class ExcalidrawWebChannelTestApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excalidraw WebChannel测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 初始化组件
        self.page_manager = WebPageManager()
        self.web_comm_excalidraw = WebCommunicationManager("excalidraw")
        
        # 连接信号
        self.web_comm_excalidraw.channel_ready.connect(self.on_excalidraw_channel_ready)
        
        # 连接页面管理器信号
        self.page_manager.page_loaded.connect(self.on_page_loaded)
        self.page_manager.page_switched.connect(self.on_page_switched)
        
        self.setup_ui()
        
        # 创建测试页面
        QTimer.singleShot(1000, self.create_test_pages)
    
    def setup_ui(self):
        """创建测试界面"""
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # 创建日志显示区域
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        layout.addWidget(self.log_text)
        
        # 创建测试按钮
        excalidraw_btn = QPushButton("测试Excalidraw页面")
        excalidraw_btn.clicked.connect(lambda: self.test_page("excalidraw"))
        layout.addWidget(excalidraw_btn)
        
        # 页面管理器将在这里显示
        layout.addWidget(self.page_manager)
        
        self.setCentralWidget(central_widget)
    
    def log_message(self, message):
        """记录日志消息"""
        self.log_text.append(message)
        print(message)
    
    def create_test_pages(self):
        """创建测试页面"""
        self.log_message("🔧 开始创建Excalidraw测试页面...")
        
        # 创建excalidraw页面
        view_excalidraw = self.page_manager.create_page(
            page_type="excalidraw",
            backend_interface=self.web_comm_excalidraw
        )
        
        if view_excalidraw:
            self.log_message("✅ Excalidraw页面创建成功")
            self.web_comm_excalidraw.set_page(view_excalidraw.page())
            
            # 加载页面内容
            self.page_manager.load_html("excalidraw", "excalidraw/index.html")
    
    def on_excalidraw_channel_ready(self):
        """Excalidraw WebChannel就绪回调"""
        self.log_message("🟢 Excalidraw WebChannel已就绪")
        # 测试发送消息
        self.test_webchannel("excalidraw")
    
    def on_page_loaded(self, page_type, success):
        """页面加载完成回调"""
        if success:
            self.log_message(f"✅ {page_type} 页面加载成功")
        else:
            self.log_message(f"❌ {page_type} 页面加载失败")
    
    def on_page_switched(self, from_page_type, to_page_type):
        """页面切换完成回调"""
        self.log_message(f"🔄 页面切换完成: {from_page_type} -> {to_page_type}")
    
    def test_page(self, page_type):
        """测试页面切换和通信"""
        self.log_message(f"🔄 切换到 {page_type} 页面")
        
        # 切换页面
        success = self.page_manager.switch_to_page(page_type)
        if success:
            self.log_message(f"✅ 成功切换到 {page_type} 页面")
        else:
            self.log_message(f"❌ 切换到 {page_type} 页面失败")
    
    def test_webchannel(self, page_type):
        """测试WebChannel通信"""
        self.log_message(f"📨 测试 {page_type} 页面WebChannel通信...")
        
        # 选择对应的通信管理器
        web_comm = self.web_comm_excalidraw
        
        # 检查WebChannel是否就绪
        if not web_comm.ready:
            self.log_message(f"⚠️  {page_type} WebChannel未就绪，等待...")
            # 等待一段时间再尝试
            QTimer.singleShot(2000, lambda: self.test_webchannel_when_ready(page_type, web_comm))
            return
        
        # 测试发送消息
        success = web_comm.send_message(
            action="testMessage",
            data={"test": f"Hello from Python to {page_type}!", "page_type": page_type},
            callback=lambda response: self.on_test_response(page_type, response)
        )
        
        if success:
            self.log_message(f"✅ {page_type} 页面消息发送成功")
        else:
            self.log_message(f"❌ {page_type} 页面消息发送失败")
    
    def test_webchannel_when_ready(self, page_type, web_comm):
        """当WebChannel就绪时测试通信"""
        self.log_message(f"🔄 检查 {page_type} WebChannel状态...")
        if web_comm.ready:
            self.log_message(f"✅ {page_type} WebChannel现在已就绪")
            self.test_webchannel(page_type)
        else:
            self.log_message(f"⚠️  {page_type} WebChannel仍未就绪，再次检查...")
            # 再次检查
            QTimer.singleShot(2000, lambda: self.test_webchannel_when_ready(page_type, web_comm))
    
    def on_test_response(self, page_type, response):
        """测试响应回调"""
        self.log_message(f"📥 {page_type} 页面收到响应: {response}")

def main():
    app = QApplication(sys.argv)
    window = ExcalidrawWebChannelTestApp()
    window.show()
    
    # 20秒后退出
    QTimer.singleShot(20000, app.quit)
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()