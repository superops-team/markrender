#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
截图测试历史记录项居中效果
"""

import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap

from app.history.history_item import HistoryItemWidget
from app.preference.app_style import AppStyle

class MockHistoryRecord:
    """模拟历史记录对象"""
    def __init__(self, change_type, change_at):
        self.change_type = change_type
        self.change_at = change_at

def create_screenshot():
    """创建截图"""
    app = QApplication.instance() or QApplication(sys.argv)
    
    # 创建主窗口
    window = QWidget()
    window.setWindowTitle("历史记录项居中测试")
    window.resize(500, 300)
    
    # 创建布局
    layout = QVBoxLayout(window)
    
    # 创建列表部件
    list_widget = QListWidget()
    list_widget.setSpacing(8)
    list_widget.setUniformItemSizes(True)
    
    # 应用样式
    app_style = AppStyle()
    list_widget.setStyleSheet(app_style.get_quickpick_panel())
    
    # 创建测试数据
    now = datetime.now()
    test_records = [
        MockHistoryRecord('content_create', now - timedelta(minutes=5)),
        MockHistoryRecord('content_update', now - timedelta(minutes=10)),
        MockHistoryRecord('title_update', now - timedelta(hours=1)),
        MockHistoryRecord('setting_update', now - timedelta(days=1)),
    ]
    
    # 添加到列表
    for i, record in enumerate(test_records):
        item_widget = HistoryItemWidget(record)
        list_item = QListWidgetItem(list_widget)
        list_item.setSizeHint(QSize(400, 40))
        list_widget.setItemWidget(list_item, item_widget)
        
        # 选中第一个项进行测试
        if i == 0:
            item_widget.set_selected(True)
    
    layout.addWidget(list_widget)
    
    # 显示窗口
    window.show()
    
    # 等待窗口完全渲染
    app.processEvents()
    
    # 创建截图
    pixmap = QPixmap(window.size())
    window.render(pixmap)
    
    # 保存截图
    screenshot_path = "/tmp/history_centered_test.png"
    pixmap.save(screenshot_path)
    print(f"截图已保存到: {screenshot_path}")
    
    return screenshot_path

if __name__ == '__main__':
    screenshot_path = create_screenshot()
    print("测试完成，请查看截图文件")