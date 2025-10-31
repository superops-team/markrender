#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细测试Statusbar标签圆角样式问题
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PySide6.QtCore import Qt
from app.statusbar.status_bar import StatusBar

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Statusbar圆角标签测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 添加测试说明
        info_label = QLabel("测试Statusbar标签圆角样式")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)
        
        # 添加测试按钮
        test_btn = QPushButton("更新标签为: test, debug, release")
        test_btn.clicked.connect(self.update_tags)
        layout.addWidget(test_btn)
        
        # 设置状态栏
        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)
        
        # 初始标签
        self.status_bar.update_tags("initial, test")

    def update_tags(self):
        """更新标签测试"""
        self.status_bar.update_tags("test, debug, release")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())
