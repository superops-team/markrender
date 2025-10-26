#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试单击展开功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from db.markrender_manager import MarkRenderManager
from app.quickpick.panel import QuickPickPanel

class TestSingleClickExpandWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("单击展开功能测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建数据库管理器
        self.manager = MarkRenderManager()
        
        # 创建QuickPick面板
        self.quickpick_panel = QuickPickPanel(self.manager)
        layout.addWidget(self.quickpick_panel)

def main():
    app = QApplication(sys.argv)
    
    window = TestSingleClickExpandWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()