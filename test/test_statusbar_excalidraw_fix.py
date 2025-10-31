#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试statusbar中excalidraw类型文件的显示修复
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QComboBox
from PySide6.QtCore import Qt
from app.statusbar.status_bar import StatusBar

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Statusbar Excalidraw修复测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 添加测试说明
        info_label = QLabel("测试Statusbar中excalidraw类型文件显示board而不是md")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)
        
        # 添加页面类型选择
        page_type_layout = QVBoxLayout()
        page_type_label = QLabel("选择页面类型:")
        self.page_type_combo = QComboBox()
        self.page_type_combo.addItems(["markdown", "excalidraw", "pdf", "png", "csv", "docx", "ppt", "epub"])
        self.page_type_combo.currentTextChanged.connect(self.set_page_type)
        page_type_layout.addWidget(page_type_label)
        page_type_layout.addWidget(self.page_type_combo)
        layout.addLayout(page_type_layout)
        
        # 添加标签控制按钮
        tag_control_layout = QVBoxLayout()
        set_tags_btn = QPushButton("设置标签: feature, bug, enhancement")
        set_tags_btn.clicked.connect(lambda: self.update_tags("feature, bug, enhancement"))
        clear_tags_btn = QPushButton("清除标签")
        clear_tags_btn.clicked.connect(lambda: self.update_tags(""))
        tag_control_layout.addWidget(set_tags_btn)
        tag_control_layout.addWidget(clear_tags_btn)
        layout.addLayout(tag_control_layout)
        
        # 添加清除所有按钮
        clear_all_btn = QPushButton("清除页面类型和标签")
        clear_all_btn.clicked.connect(self.clear_all)
        layout.addWidget(clear_all_btn)
        
        # 添加说明
        note_label = QLabel("观察statusbar中excalidraw类型文件无标签时显示'board'而不是'md'")
        note_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(note_label)
        
        # 设置状态栏
        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)
        
        # 初始设置为excalidraw
        self.set_page_type("excalidraw")
        self.update_tags("")

    def set_page_type(self, page_type):
        """设置页面类型"""
        print(f"设置页面类型: '{page_type}'")
        self.status_bar.set_page_type(page_type)

    def update_tags(self, tags_str):
        """更新标签"""
        print(f"更新标签: '{tags_str}'")
        self.status_bar.update_tags(tags_str)

    def clear_all(self):
        """清除所有内容"""
        print("清除所有内容")
        self.page_type_combo.setCurrentIndex(0)  # 重置为第一个选项
        self.status_bar.set_page_type(None)
        self.status_bar.update_tags("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())