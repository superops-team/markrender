#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合测试statusbar中page_type和tag的显示及联动更新
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QComboBox, QLineEdit
from PySide6.QtCore import Qt
from app.statusbar.status_bar import StatusBar

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Statusbar综合测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 添加测试说明
        info_label = QLabel("综合测试Statusbar中PageType和Tag的显示及联动更新")
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
        self.tag_input = QLineEdit()
        self.tag_input.setText("feature, bug, enhancement")
        set_tags_btn = QPushButton("设置标签")
        set_tags_btn.clicked.connect(self.set_tags_from_input)
        tag_layout.addWidget(tag_label)
        tag_layout.addWidget(self.tag_input)
        tag_layout.addWidget(set_tags_btn)
        layout.addLayout(tag_layout)
        
        # 添加预设标签按钮
        preset_layout = QVBoxLayout()
        preset_label = QLabel("预设标签:")
        preset_btn1 = QPushButton("设置标签: urgent, review, done")
        preset_btn1.clicked.connect(lambda: self.update_tags("urgent, review, done"))
        preset_btn2 = QPushButton("清除标签")
        preset_btn2.clicked.connect(lambda: self.update_tags(""))
        preset_layout.addWidget(preset_label)
        preset_layout.addWidget(preset_btn1)
        preset_layout.addWidget(preset_btn2)
        layout.addLayout(preset_layout)
        
        # 添加清除所有按钮
        clear_all_btn = QPushButton("清除页面类型和标签")
        clear_all_btn.clicked.connect(self.clear_all)
        layout.addWidget(clear_all_btn)
        
        # 添加说明
        note_label = QLabel("观察statusbar中PageType标签(带颜色)作为首个标签显示，并且标签能够正确联动更新")
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

    def set_tags_from_input(self):
        """从输入框设置标签"""
        tags_str = self.tag_input.text()
        print(f"从输入框设置标签: '{tags_str}'")
        self.update_tags(tags_str)

    def update_tags(self, tags_str):
        """更新标签"""
        print(f"更新标签: '{tags_str}'")
        self.status_bar.update_tags(tags_str)

    def clear_all(self):
        """清除所有内容"""
        print("清除所有内容")
        self.page_type_combo.setCurrentIndex(0)  # 重置为第一个选项
        self.tag_input.setText("")
        self.status_bar.set_page_type(None)
        self.status_bar.update_tags("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())