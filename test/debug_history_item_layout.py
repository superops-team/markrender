#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试历史记录项布局问题
"""

import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QPushButton, QLabel, QFrame
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor

from app.history.history_item import HistoryItemWidget
from app.preference.app_style import AppStyle
from app.preference.style_constants import SPACING_MD


class MockHistoryRecord:
    """模拟历史记录对象"""
    def __init__(self, change_type, change_at):
        self.change_type = change_type
        self.change_at = change_at


class DebugHistoryItemLayout(QWidget):
    """调试历史记录项布局窗口"""
    
    def __init__(self):
        super().__init__()
        self.app_style = AppStyle()
        self.init_ui()
        self.load_test_data()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # 创建说明标签
        info_label = QLabel("调试历史记录项布局问题\n显示边框以便观察布局")
        info_label.setStyleSheet("background-color: lightblue; padding: 10px; margin-bottom: 10px;")
        
        # 创建列表用于展示历史记录项
        self.list_widget = QListWidget()
        self.list_widget.setSpacing(8)  # 与实际应用保持一致
        self.list_widget.setUniformItemSizes(True)
        # 应用实际的样式
        self.list_widget.setStyleSheet(self.app_style.get_quickpick_panel())
        
        # 添加测试按钮
        self.test_btn = QPushButton("重新加载测试数据")
        self.test_btn.clicked.connect(self.load_test_data)
        
        # 添加调试按钮
        self.debug_btn = QPushButton("显示调试信息")
        self.debug_btn.clicked.connect(self.show_debug_info)
        
        layout.addWidget(info_label)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.test_btn)
        layout.addWidget(self.debug_btn)
        self.setWindowTitle('调试历史记录项布局')
        self.resize(400, 500)
        
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
        for i, record in enumerate(test_records):
            item_widget = HistoryItemWidget(record)
            list_item = QListWidgetItem(self.list_widget)
            list_item.setSizeHint(QSize(0, item_widget.height()))  # 使用历史记录项的实际高度
            self.list_widget.setItemWidget(list_item, item_widget)
            
            # 选中第一个项进行测试
            if i == 0:
                item_widget.set_selected(True)
                
    def show_debug_info(self):
        """显示调试信息"""
        if self.list_widget.count() > 0:
            first_item = self.list_widget.item(0)
            item_widget = self.list_widget.itemWidget(first_item)
            if item_widget:
                info = f"""
历史记录项调试信息:
- 固定高度: {item_widget.height()}px
- SPACING_MD: {SPACING_MD}px
- 计算高度: 40 + 2 * {SPACING_MD} = {40 + 2 * SPACING_MD}px
- QListWidget 项目数: {self.list_widget.count()}
                """
                debug_label = QLabel(info)
                debug_label.setStyleSheet("background-color: #ffffcc; padding: 10px; border: 1px solid #cccccc;")
                debug_label.setWordWrap(True)
                debug_label.setObjectName("debug_label")  # 设置对象名以便识别
                
                # 将调试信息添加到窗口底部
                layout = self.layout()
                if layout is not None:
                    # 检查是否已经存在调试标签
                    debug_exists = False
                    for i in range(layout.count()):
                        item = layout.itemAt(i)
                        if item and item.widget() and item.widget().objectName() == "debug_label":
                            debug_exists = True
                            # 移除旧的调试标签
                            widget = layout.takeAt(i).widget()
                            if widget:
                                widget.deleteLater()
                            break
                    
                    # 添加新的调试标签
                    layout.addWidget(debug_label)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    test_window = DebugHistoryItemLayout()
    test_window.show()
    sys.exit(app.exec())