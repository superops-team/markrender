#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试历史记录面板设计原则应用效果
展示Robin Williams设计原则（亲密性、对齐、重复、对比）的应用
"""

import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QPushButton, QLabel, QTextEdit
from PySide6.QtCore import Qt, QSize

from app.history.history_item import HistoryItemWidget
from app.history.history_panel import HistoryPanel
from app.preference.app_style import AppStyle


class MockHistoryRecord:
    """模拟历史记录对象"""
    def __init__(self, change_type, change_at):
        self.change_type = change_type
        self.change_at = change_at


class HistoryDesignPrinciplesTest(QWidget):
    """历史记录设计原则测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.app_style = AppStyle()
        self.init_ui()
        self.load_test_data()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 创建说明标签
        info_label = QLabel("测试历史记录面板设计原则应用效果\nRobin Williams设计原则：亲密性、对齐、重复、对比")
        info_label.setStyleSheet("background-color: lightblue; padding: 10px; margin-bottom: 10px;")
        
        # 创建历史记录面板
        self.history_panel = HistoryPanel()
        
        # 添加测试按钮
        self.test_btn = QPushButton("重新加载测试数据")
        self.test_btn.clicked.connect(self.load_test_data)
        
        # 添加设计原则说明
        self.principles_text = QTextEdit()
        self.principles_text.setMaximumHeight(200)
        self.principles_text.setReadOnly(True)
        self.update_principles_text()
        
        layout.addWidget(info_label)
        layout.addWidget(self.history_panel)
        layout.addWidget(self.test_btn)
        layout.addWidget(self.principles_text)
        self.setWindowTitle('历史记录设计原则测试')
        self.resize(500, 700)
        
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
        
        # 清空现有数据
        self.history_panel.history_list.clear()
        
        # 添加到列表
        for i, record in enumerate(test_records):
            item_widget = HistoryItemWidget(record)
            list_item = QListWidgetItem(self.history_panel.history_list)
            list_item.setSizeHint(QSize(0, 48))  # 使用48px高度
            self.history_panel.history_list.setItemWidget(list_item, item_widget)
            
            # 选中第一个项进行测试
            if i == 0:
                item_widget.set_selected(True)
                
    def update_principles_text(self):
        """更新设计原则说明文本"""
        principles = """
Robin Williams设计原则在历史记录面板中的应用：

1. 亲密性 (Proximity)
   - 标题与列表紧密组织在一起
   - 相关的UI元素保持适当的间距
   - 项与项之间通过分割线分组

2. 对齐 (Alignment)
   - 标题左对齐，与列表内容保持一致
   - 文本在项内垂直居中对齐
   - 左右边距统一，保持视觉平衡

3. 重复 (Repetition)
   - 所有历史记录项使用统一的高度和样式
   - 字体、颜色、间距在整个面板中保持一致
   - 选中和悬停状态的视觉效果统一

4. 对比 (Contrast)
   - 标题使用更大字体和半粗体，与内容形成对比
   - 变更类型使用蓝色强调，时间使用灰色
   - 选中状态使用浅蓝色背景，与默认状态形成对比

设计效果：
- 视觉层次清晰：标题 > 变更类型 > 时间
- 信息组织合理：相关项分组，不同项区分
- 交互反馈明确：悬停和选中状态明显
- 界面风格统一：与应用程序其他部分保持一致
        """
        self.principles_text.setText(principles)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test_window = HistoryDesignPrinciplesTest()
    test_window.show()
    sys.exit(app.exec())