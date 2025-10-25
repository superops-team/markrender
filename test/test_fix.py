#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的quickpick模块
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from app.quickpick.panel import QuickPickPanel
from db.markrender_manager import MarkRenderManager

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuickPick Fix Test")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建MarkRenderManager实例
        manager = MarkRenderManager()
        
        # 创建QuickPickPanel实例
        self.quick_pick_panel = QuickPickPanel(manager)
        layout.addWidget(self.quick_pick_panel)
        
        # 加载数据
        self.quick_pick_panel.load_quickpick_items()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())