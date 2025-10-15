#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
历史记录项布局测试
验证历史记录项是否按照指定的ASCII样式展示
"""

import sys
from datetime import datetime, timedelta
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt, QSize

# 添加项目根目录到Python路径
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.history.history_item import HistoryItemWidget


class MockHistoryRecord:
    """模拟历史记录对象"""
    def __init__(self, change_type, change_at):
        self.change_type = change_type
        self.change_at = change_at


class HistoryItemLayoutTest(QWidget):
    """历史记录项布局测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_test_data()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 创建列表用于展示历史记录项
        self.list_widget = QListWidget()
        self.list_widget.setSpacing(0)  # 紧凑排列
        self.list_widget.setUniformItemSizes(True)
        
        layout.addWidget(self.list_widget)
        self.setWindowTitle('历史记录项布局测试')
        self.resize(400, 300)
        
    def load_test_data(self):
        """加载测试数据"""
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
    test_window = HistoryItemLayoutTest()
    test_window.show()
    sys.exit(app.exec())