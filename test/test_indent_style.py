#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
折叠区域缩进样式测试文件
用于验证折叠区域缩进不增加特殊颜色渲染的修改是否生效
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import Qt
from app.preference.app_style import AppStyle

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("折叠区域缩进样式测试")
        self.setGeometry(100, 100, 400, 300)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建测试树形控件
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(16)
        
        # 添加测试数据
        root1 = QTreeWidgetItem(self.tree)
        root1.setText(0, "根节点1")
        
        child1 = QTreeWidgetItem(root1)
        child1.setText(0, "子节点1")
        
        child2 = QTreeWidgetItem(root1)
        child2.setText(0, "子节点2")
        
        root2 = QTreeWidgetItem(self.tree)
        root2.setText(0, "根节点2")
        
        # 应用QuickPick面板样式
        app_style = AppStyle()
        self.tree.setStyleSheet(app_style.get_quickpick_panel())
        
        layout.addWidget(self.tree)

def main():
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()