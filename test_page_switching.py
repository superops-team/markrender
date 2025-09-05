#!/usr/bin/env python3
"""
页面切换测试脚本
验证WebPageManager的页面切换功能和数据隔离
"""

import sys
import os
import time

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit
from PySide6.QtCore import QTimer

from app.editor.webengine import WebPageManager
from app.editor.backend_interface import BackendInterface


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("页面切换测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建按钮
        self.markdown_btn = QPushButton("切换到Markdown页面")
        self.excalidraw_btn = QPushButton("切换到Excalidraw页面")
        self.landing_btn = QPushButton("切换到Landing页面")
        
        # 创建页面容器
        self.page_container = QWidget()
        self.page_container.setStyleSheet("background-color: white;")
        self.page_container_layout = QVBoxLayout(self.page_container)
        self.page_container_layout.setContentsMargins(0, 0, 0, 0)
        
        # 添加控件到布局
        layout.addWidget(self.markdown_btn)
        layout.addWidget(self.excalidraw_btn)
        layout.addWidget(self.landing_btn)
        layout.addWidget(self.page_container)
        
        # 连接按钮信号
        self.markdown_btn.clicked.connect(lambda: self.switch_to_page("markdown", "item1"))
        self.excalidraw_btn.clicked.connect(lambda: self.switch_to_page("excalidraw", "item2"))
        self.landing_btn.clicked.connect(lambda: self.switch_to_page("landing", "item3"))
        
        # 初始化页面管理器
        self.page_manager = WebPageManager()
        self.page_manager.set_container(self.page_container)
        
        # 预加载页面
        self.page_manager.preload_page_type("markdown")
        self.page_manager.preload_page_type("excalidraw")
        self.page_manager.preload_page_type("landing")
        
        print("测试窗口初始化完成")
    
    def switch_to_page(self, page_type, item_id):
        """切换页面"""
        print(f"切换到页面: {page_type}, 项目ID: {item_id}")
        success = self.page_manager.switch_to_page(page_type, item_id)
        if success:
            print(f"成功切换到 {page_type} 页面")
        else:
            print(f"切换到 {page_type} 页面失败")


def main():
    app = QApplication(sys.argv)
    
    # 创建测试窗口
    window = TestWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()