#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试statusbar标签样式与edit_dialog标签样式的一致性
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from app.statusbar.status_bar import StatusBar
from app.quickpick.edit_dialog import EditItemDialog

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Statusbar vs EditDialog标签样式对比测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 添加测试说明
        info_label = QLabel("对比测试Statusbar标签样式与EditDialog标签样式的一致性")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)
        
        # 添加测试按钮
        test_btn1 = QPushButton("更新Statusbar标签为: feature, bug, enhancement")
        test_btn1.clicked.connect(lambda: self.update_statusbar_tags("feature, bug, enhancement"))
        layout.addWidget(test_btn1)
        
        test_btn2 = QPushButton("更新Statusbar标签为: urgent, review, done")
        test_btn2.clicked.connect(lambda: self.update_statusbar_tags("urgent, review, done"))
        layout.addWidget(test_btn2)
        
        test_btn3 = QPushButton("清空Statusbar标签")
        test_btn3.clicked.connect(lambda: self.update_statusbar_tags(""))
        layout.addWidget(test_btn3)
        
        # 添加对比说明
        compare_label = QLabel("下面显示EditDialog中的标签样式（用于对比）:")
        layout.addWidget(compare_label)
        
        # 创建EditDialog标签样式对比区域
        self.create_edit_dialog_tag_examples(layout)
        
        # 设置状态栏
        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)
        
        # 初始标签
        self.update_statusbar_tags("initial, test")

    def create_edit_dialog_tag_examples(self, parent_layout):
        """创建EditDialog标签样式示例"""
        container = QWidget()
        container_layout = QVBoxLayout(container)
        
        # 创建一个水平布局来展示标签示例
        tag_layout = QHBoxLayout()
        tag_layout.setSpacing(12)
        
        # 创建几个示例标签，模拟EditDialog中的标签样式
        example_tags = ["feature", "bug", "enhancement"]
        for tag_text in example_tags:
            # 模拟EditDialog中的_make_tag_widget方法
            tag_button = QPushButton(tag_text)
            tag_button.setStyleSheet(f'''
                QPushButton {{
                    background-color: #F3F4F6;  /* NEUTRAL_100 */
                    border: 1px solid #E5E7EB;  /* NEUTRAL_200 */
                    border-radius: 16px;
                    color: #374151;  /* NEUTRAL_700 */
                    padding: 6px 12px;
                    font-size: 12px;  /* FONT_SIZE_SM */
                    font-weight: 500;
                    text-align: center;
                    min-height: 20px;
                }}
                QPushButton:hover {{
                    background-color: #E5E7EB;  /* NEUTRAL_200 */
                }}
            ''')
            tag_button.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
            tag_layout.addWidget(tag_button)
        
        tag_layout.addStretch()
        container_layout.addLayout(tag_layout)
        parent_layout.addWidget(container)

    def update_statusbar_tags(self, tags_str):
        """更新statusbar标签测试"""
        self.status_bar.update_tags(tags_str)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())