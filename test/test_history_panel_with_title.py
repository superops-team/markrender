#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试历史记录面板标题显示
"""

import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QTimer
from app.history.history_panel import HistoryPanel


class MockHistoryRecord:
    """模拟历史记录对象"""
    def __init__(self, change_type, change_at):
        self.change_type = change_type
        self.change_at = change_at


class TestHistoryPanelWithTitle(QMainWindow):
    """测试历史记录面板标题显示"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("历史记录面板标题测试")
        self.setGeometry(100, 100, 400, 500)
        
        # 创建中央部件
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # 添加说明标签
        info_label = QLabel("历史记录面板应该显示'编辑历史'标题")
        info_label.setStyleSheet("background-color: lightblue; padding: 10px;")
        
        # 创建历史面板
        self.history_panel = HistoryPanel()
        self.history_panel.show()  # 确保面板可见
        
        # 添加组件到布局
        layout.addWidget(info_label)
        layout.addWidget(self.history_panel)
        
        self.setCentralWidget(central_widget)
        
        # 延迟创建测试数据
        QTimer.singleShot(100, self.create_test_data)
        
    def create_test_data(self):
        """创建测试数据"""
        try:
            # 创建测试历史记录数据
            base_time = datetime.now()
            change_types = ["content_create", "content_update", "title_update", "setting_update"]
            
            # 创建一些测试历史记录对象
            test_records = []
            for i in range(5):
                # 创建模拟的历史记录对象
                record = MockHistoryRecord(
                    change_types[i % len(change_types)],
                    base_time - timedelta(minutes=i*30)
                )
                test_records.append(record)
            
            # 清空历史列表并添加测试记录
            self.history_panel.history_list.clear()
            
            # 添加到列表
            for record in test_records:
                from app.history.history_item import HistoryItemWidget
                item_widget = HistoryItemWidget(record)
                from PySide6.QtWidgets import QListWidgetItem
                list_item = QListWidgetItem(self.history_panel.history_list)
                list_item.setSizeHint(item_widget.sizeHint())
                self.history_panel.history_list.setItemWidget(list_item, item_widget)
            
            print(f"创建了 {len(test_records)} 条测试历史记录")
            
        except Exception as e:
            print(f"创建测试数据失败: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestHistoryPanelWithTitle()
    window.show()
    sys.exit(app.exec())