#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试 QuickPickPanel 的右键菜单功能
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from app.quickpick.panel import QuickPickPanel
from db.markrender_manager import MarkRenderManager


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuickPickPanel 右键菜单测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建数据库管理器
        manager = MarkRenderManager()
        
        # 创建 QuickPickPanel
        self.quickpick_panel = QuickPickPanel(manager, self)
        layout.addWidget(self.quickpick_panel)


def main():
    app = QApplication(sys.argv)
    
    # 创建测试窗口
    window = TestWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()