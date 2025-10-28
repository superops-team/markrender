#!/usr/bin/env python3
"""
测试外部链接在浏览器中打开的功能
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.editor.webengine import CustomWebEnginePage

class ExternalLinkTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("外部链接测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建Web视图
        self.web_view = QWebEngineView()
        
        # 创建自定义页面
        custom_page = CustomWebEnginePage(self.web_view)
        self.web_view.setPage(custom_page)
        
        # 测试HTML内容，包含外部链接
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>外部链接测试</title>
        </head>
        <body>
            <h1>外部链接测试页面</h1>
            <p>点击以下链接应该在系统默认浏览器中打开：</p>
            <ul>
                <li><a href="https://www.google.com">Google</a></li>
                <li><a href="https://www.github.com">GitHub</a></li>
                <li><a href="https://www.stackoverflow.com">Stack Overflow</a></li>
            </ul>
            <p>以下链接应该在当前页面中打开（本地链接）：</p>
            <ul>
                <li><a href="#section1">跳转到章节1</a></li>
                <li><a href="#section2">跳转到章节2</a></li>
            </ul>
            <h2 id="section1">章节1</h2>
            <p>这是章节1的内容。</p>
            <h2 id="section2">章节2</h2>
            <p>这是章节2的内容。</p>
        </body>
        </html>
        """
        
        # 设置HTML内容
        self.web_view.setHtml(html_content)
        
        # 添加控件到布局
        layout.addWidget(self.web_view)
        
        print("外部链接测试窗口已创建")
        print("请在Web视图中点击外部链接（如Google、GitHub等）")
        print("这些链接应该在系统默认浏览器中打开，而不是在当前应用中打开")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExternalLinkTestWindow()
    window.show()
    sys.exit(app.exec())