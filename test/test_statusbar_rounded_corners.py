#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试statusbar标签圆角效果
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PySide6.QtCore import Qt
from app.statusbar.status_bar import StatusBar

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Statusbar标签圆角效果测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 添加测试说明
        info_label = QLabel("测试Statusbar标签圆角效果")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)
        
        # 添加测试按钮
        test_btn1 = QPushButton("设置圆角标签: feature, bug, enhancement")
        test_btn1.clicked.connect(lambda: self.update_tags("feature, bug, enhancement"))
        layout.addWidget(test_btn1)
        
        test_btn2 = QPushButton("设置圆角标签: urgent, review, done")
        test_btn2.clicked.connect(lambda: self.update_tags("urgent, review, done"))
        layout.addWidget(test_btn2)
        
        test_btn3 = QPushButton("清空标签")
        test_btn3.clicked.connect(lambda: self.update_tags(""))
        layout.addWidget(test_btn3)
        
        test_btn4 = QPushButton("设置单个圆角标签")
        test_btn4.clicked.connect(lambda: self.update_tags("single"))
        layout.addWidget(test_btn4)
        
        # 添加说明
        note_label = QLabel("观察statusbar标签是否显示圆角效果")
        note_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(note_label)
        
        # 设置状态栏
        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)
        
        # 初始标签
        self.update_tags("initial, test")

    def update_tags(self, tags_str):
        """更新statusbar标签测试"""
        print(f"设置标签: '{tags_str}'")
        self.status_bar.update_tags(tags_str)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())