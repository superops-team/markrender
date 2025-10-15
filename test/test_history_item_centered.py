#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试历史记录项纵向居中效果
"""

import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QPushButton, QLabel
from PySide6.QtCore import Qt, QSize

from app.history.history_item import HistoryItemWidget


class MockHistoryRecord:
    """模拟历史记录对象"""
    def __init__(self, change_type, change_at):
        self.change_type = change_type
        self.change_at = change_at


class HistoryItemCenteredTest(QWidget):
    """历史记录项纵向居中测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_test_data()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 创建说明标签
        info_label = QLabel("测试历史记录项纵向居中效果\n点击任意项可查看选中状态下的居中效果")
        info_label.setStyleSheet("background-color: lightblue; padding: 10px; margin-bottom: 10px;")
        
        # 创建列表用于展示历史记录项
        self.list_widget = QListWidget()
        self.list_widget.setSpacing(0)  # 紧凑排列
        self.list_widget.setUniformItemSizes(True)
        
        # 添加测试按钮
        self.test_btn = QPushButton("重新加载测试数据")
        self.test_btn.clicked.connect(self.load_test_data)
        
        layout.addWidget(info_label)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.test_btn)
        self.setWindowTitle('历史记录项纵向居中测试')
        self.resize(400, 300)
        
    def load_test_data(self):
        """加载测试数据"""
        # 清空现有数据
        self.list_widget.clear()
        
        # 创建测试历史记录
        now = datetime.now()
        test_records = [
            MockHistoryRecord('content_create', now - timedelta(minutes=5)),
            MockHistoryRecord('content_update', now - timedelta(minutes=10)),
            MockHistoryRecord('title_update', now - timedelta(hours=1)),
            MockHistoryRecord('setting_update', now - timedelta(days=1)),
        ]
        
        # 添加到列表
        for record in test_records:
            item_widget = HistoryItemWidget(record)
            list_item = QListWidgetItem(self.list_widget)
            list_item.setSizeHint(QSize(0, 40))  # 与HistoryItemWidget高度一致
            self.list_widget.setItemWidget(list_item, item_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test_window = HistoryItemCenteredTest()
    test_window.show()
    sys.exit(app.exec())