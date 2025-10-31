#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试statusbar中page_type标签和tag标签的显示
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QComboBox
from PySide6.QtCore import Qt
from app.statusbar.status_bar import StatusBar

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Statusbar PageType和Tag标签测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 添加测试说明
        info_label = QLabel("测试Statusbar中PageType标签和Tag标签的显示")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)
        
        # 添加页面类型选择
        page_type_layout = QVBoxLayout()
        page_type_label = QLabel("选择页面类型:")
        self.page_type_combo = QComboBox()
        self.page_type_combo.addItems(["markdown", "pdf", "png", "csv", "docx", "ppt", "epub", "board"])
        self.page_type_combo.currentTextChanged.connect(self.set_page_type)
        page_type_layout.addWidget(page_type_label)
        page_type_layout.addWidget(self.page_type_combo)
        layout.addLayout(page_type_layout)
        
        # 添加标签输入
        tag_layout = QVBoxLayout()
        tag_label = QLabel("设置标签 (用逗号分隔):")
        self.tag_input = QPushButton("设置标签: feature, bug, enhancement")
        self.tag_input.clicked.connect(lambda: self.update_tags("feature, bug, enhancement"))
        tag_layout.addWidget(tag_label)
        tag_layout.addWidget(self.tag_input)
        layout.addLayout(tag_layout)
        
        # 添加清除按钮
        clear_layout = QVBoxLayout()
        clear_tags_btn = QPushButton("清除标签")
        clear_tags_btn.clicked.connect(lambda: self.update_tags(""))
        clear_all_btn = QPushButton("清除页面类型和标签")
        clear_all_btn.clicked.connect(self.clear_all)
        clear_layout.addWidget(clear_tags_btn)
        clear_layout.addWidget(clear_all_btn)
        layout.addLayout(clear_layout)
        
        # 添加说明
        note_label = QLabel("观察statusbar中PageType标签(带颜色)和Tag标签的显示效果")
        note_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(note_label)
        
        # 设置状态栏
        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)
        
        # 初始设置
        self.set_page_type("markdown")
        self.update_tags("initial, test")

    def set_page_type(self, page_type):
        """设置页面类型"""
        print(f"设置页面类型: '{page_type}'")
        self.status_bar.set_page_type(page_type)

    def update_tags(self, tags_str):
        """更新标签"""
        print(f"设置标签: '{tags_str}'")
        self.status_bar.update_tags(tags_str)

    def clear_all(self):
        """清除所有内容"""
        print("清除所有内容")
        self.status_bar.set_page_type(None)
        self.status_bar.update_tags("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())