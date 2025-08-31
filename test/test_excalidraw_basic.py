#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试基础Excalidraw功能（无WebChannel通信）
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QUrl, QObject, Slot, Signal, QDir
import sys


class BackendInterface(QObject):
    """简化版后端接口，不实现具体功能"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
    
    @Slot(str, result=str)
    def dispatch_request(self, request):
        """处理前端请求（简化版）"""
        print(f"[Backend] 收到请求: {request}")
        # 返回一个简单的响应
        return '{"success": true, "message": "OK"}'
    
    @Slot()
    def frontend_ready(self):
        """前端就绪通知（简化版）"""
        print("[Backend] 前端已就绪")
    
    @Slot(str)
    def handle_web_response(self, response):
        """处理Web响应（简化版）"""
        print(f"[Backend] 收到Web响应: {response}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("基础Excalidraw测试")
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建WebEngine视图
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        
        # 设置WebChannel
        self.setup_web_channel()
        
        # 加载Excalidraw页面
        self.load_excalidraw()
    
    def setup_web_channel(self):
        """设置WebChannel"""
        self.channel = QWebChannel()
        self.backend_interface = BackendInterface()
        self.channel.registerObject("backendInterface", self.backend_interface)
        self.web_view.page().setWebChannel(self.channel)
    
    def load_excalidraw(self):
        """加载Excalidraw页面"""
        # 获取HTML文件路径
        html_path = project_root / "app" / "editor" / "plugins" / "excalidraw" / "simple.html"
        if html_path.exists():
            url = QUrl.fromLocalFile(str(html_path))
            self.web_view.load(url)
            print(f"加载Excalidraw: {url}")
        else:
            print(f"未找到Excalidraw HTML文件: {html_path}")


def main():
    app = QApplication(sys.argv)
    
    # 确保支持WebChannel
    QDir.addSearchPath("qrc", ":/qtwebchannel")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()