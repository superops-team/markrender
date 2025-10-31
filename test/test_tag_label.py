#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试TagLabel控件圆角样式
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt
from app.statusbar.status_bar import TagLabel

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TagLabel圆角测试")
        self.setGeometry(100, 100, 400, 200)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 添加测试说明
        info_label = QLabel("测试TagLabel圆角样式")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)
        
        # 创建几个测试标签
        tag1 = TagLabel("test")
        tag2 = TagLabel("debug")
        tag3 = TagLabel("release")
        
        layout.addWidget(tag1)
        layout.addWidget(tag2)
        layout.addWidget(tag3)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())