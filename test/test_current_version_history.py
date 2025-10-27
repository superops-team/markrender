#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试历史记录模块当前版本功能
"""

import sys
import os
from datetime import datetime, timedelta
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt, QSize

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.history.history_item import HistoryItemWidget
from app.history.history_panel import HistoryPanel
from app.preference.app_style import AppStyle


class MockHistoryRecord:
    """模拟历史记录对象"""
    def __init__(self, change_type, change_at):
        self.change_type = change_type
        self.change_at = change_at


class CurrentVersionHistoryTest(QWidget):
    """当前版本历史记录测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.app_style = AppStyle()
        self.init_ui()
        self.load_test_data()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        self.setWindowTitle("当前版本历史记录功能测试")
        self.resize(600, 800)
        
        # 创建历史记录面板
        self.history_panel = HistoryPanel()
        layout.addWidget(self.history_panel)
        
    def load_test_data(self):
        """加载测试数据"""
        # 创建测试数据
        now = datetime.now()
        test_records = [
            MockHistoryRecord('content_create', now - timedelta(minutes=5)),
            MockHistoryRecord('content_update', now - timedelta(minutes=10)),
            MockHistoryRecord('title_update', now - timedelta(hours=1)),
            MockHistoryRecord('setting_update', now - timedelta(days=1)),
            MockHistoryRecord('page_engine_update', now - timedelta(days=2)),
        ]
        
        # 模拟加载历史记录
        for record in test_records:
            item_widget = HistoryItemWidget(record)
            list_item = QListWidgetItem(self.history_panel.history_list)
            list_item.setSizeHint(QSize(0, 56))  # 与HistoryItemWidget高度保持一致
            self.history_panel.history_list.setItemWidget(list_item, item_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test_window = CurrentVersionHistoryTest()
    test_window.show()
    sys.exit(app.exec())