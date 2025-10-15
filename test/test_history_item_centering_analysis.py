#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析历史记录项居中效果的测试程序
测量文本到选中区域上下边框的距离
"""

import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QPushButton, QLabel, QTextEdit
from PySide6.QtCore import Qt, QSize

from app.history.history_item import HistoryItemWidget
from app.preference.app_style import AppStyle


class MockHistoryRecord:
    """模拟历史记录对象"""
    def __init__(self, change_type, change_at):
        self.change_type = change_type
        self.change_at = change_at


class HistoryItemCenteringAnalysis(QWidget):
    """历史记录项居中效果分析窗口"""
    
    def __init__(self):
        super().__init__()
        self.app_style = AppStyle()
        self.init_ui()
        self.load_test_data()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 创建说明标签
        info_label = QLabel("分析历史记录项居中效果\n测量文本到选中区域上下边框的距离")
        info_label.setStyleSheet("background-color: lightblue; padding: 10px; margin-bottom: 10px;")
        
        # 创建列表用于展示历史记录项
        self.list_widget = QListWidget()
        self.list_widget.setSpacing(8)  # 与实际应用保持一致
        self.list_widget.setUniformItemSizes(True)
        # 应用实际的样式
        self.list_widget.setStyleSheet(self.app_style.get_quickpick_panel())
        
        # 添加测试按钮
        self.test_btn = QPushButton("重新加载测试数据并分析")
        self.test_btn.clicked.connect(self.load_test_data_and_analyze)
        
        # 添加结果显示区域
        self.result_text = QTextEdit()
        self.result_text.setMaximumHeight(200)
        self.result_text.setReadOnly(True)
        
        layout.addWidget(info_label)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.test_btn)
        layout.addWidget(self.result_text)
        self.setWindowTitle('历史记录项居中效果分析')
        self.resize(500, 600)
        
    def load_test_data(self):
        """加载测试数据"""
        # 清空现有数据
        self.list_widget.clear()
        
        # 创建测试历史记录
        now = datetime.now()
        test_records = [
            MockHistoryRecord('content_create', now - timedelta(minutes=5)),
            MockHistoryRecord('content_update', now - timedelta(minutes=10)),
        ]
        
        # 添加到列表
        for i, record in enumerate(test_records):
            item_widget = HistoryItemWidget(record)
            list_item = QListWidgetItem(self.list_widget)
            list_item.setSizeHint(QSize(0, 40))  # 使用40px高度
            self.list_widget.setItemWidget(list_item, item_widget)
            
            # 选中第一个项进行测试
            if i == 0:
                item_widget.set_selected(True)
                
    def load_test_data_and_analyze(self):
        """加载测试数据并分析居中效果"""
        self.load_test_data()
        
        # 分析第一个选中项的布局
        if self.list_widget.count() > 0:
            first_item = self.list_widget.item(0)
            item_widget = self.list_widget.itemWidget(first_item)
            
            if item_widget:
                self.analyze_layout(item_widget)
                
    def analyze_layout(self, item_widget):
        """分析布局并显示结果"""
        # 获取各种尺寸信息
        widget_height = item_widget.height()
        widget_width = item_widget.width()
        
        # 获取标签信息
        type_label = item_widget.type_label
        time_label = item_widget.time_label
        
        type_label_height = type_label.height()
        time_label_height = time_label.height()
        
        type_label_y = type_label.y()
        time_label_y = time_label.y()
        
        # 计算文本到上下边框的距离
        distance_to_top = type_label_y
        distance_to_bottom = widget_height - (time_label_y + time_label_height)
        
        # 计算垂直中心点
        widget_center_y = widget_height / 2
        content_center_y = (type_label_y + type_label_height / 2 + time_label_y + time_label_height / 2) / 2
        
        # 计算偏移量
        offset = abs(widget_center_y - content_center_y)
        
        # 准备分析结果
        analysis_result = f"""
历史记录项居中效果分析结果:

=== 基本尺寸信息 ===
- 历史记录项总高度: {widget_height}px
- 历史记录项总宽度: {widget_width}px
- 变更类型标签高度: {type_label_height}px
- 变更时间标签高度: {time_label_height}px

=== 位置信息 ===
- 变更类型标签Y坐标: {type_label_y}px
- 变更时间标签Y坐标: {time_label_y}px

=== 距离测量 ===
- 文本到上边框距离: {distance_to_top}px
- 文本到下边框距离: {distance_to_bottom}px

=== 居中分析 ===
- 历史记录项垂直中心点: {widget_center_y:.1f}px
- 内容垂直中心点: {content_center_y:.1f}px
- 中心偏移量: {offset:.1f}px

=== 评估结果 ===
"""
        
        # 评估居中效果
        if abs(distance_to_top - distance_to_bottom) <= 2:
            analysis_result += "✓ 居中效果良好 - 上下距离基本相等\n"
        elif distance_to_top < distance_to_bottom:
            analysis_result += "↓ 内容偏向上方 - 需要向下调整\n"
        else:
            analysis_result += "↑ 内容偏向下方 - 需要向上调整\n"
            
        if offset <= 2:
            analysis_result += "✓ 完美居中 - 中心点重合\n"
        elif offset <= 5:
            analysis_result += "○ 接近居中 - 偏移较小\n"
        else:
            analysis_result += "✗ 未居中 - 偏移较大\n"
        
        # 显示结果
        self.result_text.setText(analysis_result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test_window = HistoryItemCenteringAnalysis()
    test_window.show()
    sys.exit(app.exec())