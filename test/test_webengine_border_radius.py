#!/usr/bin/env python3
"""
测试WebEngineView圆角样式应用
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.editor.webengine import WebPageManager
from app.preference.style_constants import EDITOR_RADIUS, NEUTRAL_300, EDITOR_BORDER_WIDTH

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WebEngineView圆角样式测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建WebPageManager
        self.web_manager = WebPageManager()
        
        # 创建页面
        self.view = self.web_manager.create_page("markdown")
        if self.view:
            # 加载测试内容
            self.view.setHtml("""
            <html>
            <head>
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                        padding: 20px;
                        background-color: #ffffff;
                    }
                    h1 {
                        color: #1a1a1a;
                    }
                    p {
                        color: #333;
                        line-height: 1.6;
                    }
                </style>
            </head>
            <body>
                <h1>WebEngineView圆角样式测试</h1>
                <p>这是一个测试页面，用于验证WebEngineView的圆角样式是否正确应用。</p>
                <p>如果看到圆角效果，说明样式已正确应用。</p>
            </body>
            </html>
            """)
            
            layout.addWidget(self.view)
            
            # 打印样式信息用于调试
            print(f"EDITOR_RADIUS: {EDITOR_RADIUS}")
            print(f"EDITOR_BORDER_WIDTH: {EDITOR_BORDER_WIDTH}")
            print(f"NEUTRAL_300: {NEUTRAL_300}")
            print(f"应用的样式: {self.view.styleSheet()}")

def main():
    app = QApplication(sys.argv)
    
    window = TestWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()