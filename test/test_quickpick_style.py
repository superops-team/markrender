#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QuickPick样式测试文件
用于验证选中状态一致性的修改是否生效
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from app.quickpick.panel import QuickPickPanel
from app.preference.app_style import AppStyle

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuickPick样式测试")
        self.setGeometry(100, 100, 400, 600)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建QuickPick面板
        self.quickpick_panel = QuickPickPanel(None)
        layout.addWidget(self.quickpick_panel)
        
        # 应用样式
        app_style = AppStyle()
        self.setStyleSheet(app_style.get_main_style())

def main():
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()