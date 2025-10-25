#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试quickpick按钮显示的简单脚本 - 修复版
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from app.quickpick.panel import QuickPickPanel

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuickPick Button Test - Fixed")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建一个简单的mock manager
        class MockManager:
            def get_full_tree(self):
                return [
                    {
                        'id': '1',
                        'title': '测试文件1',
                        'page_type': 'markdown',
                        'updated_at': '2023-01-01 12:00:00',
                        'created_at': '2023-01-01 12:00:00'
                    },
                    {
                        'id': '2',
                        'title': '测试文件2',
                        'page_type': 'excalidraw',
                        'updated_at': '2023-01-02 12:00:00',
                        'created_at': '2023-01-02 12:00:00'
                    }
                ]
            
            def save_item(self, **kwargs):
                pass
                
            def delete_item(self, item_id):
                return True
                
            def create_file(self, title, content, parent_id=None, page_type='markdown', page_engine=None):
                pass
                
            def create_folder(self, title, parent_id=None):
                pass
        
        # 创建quickpick面板
        self.quickpick_panel = QuickPickPanel(MockManager())
        layout.addWidget(self.quickpick_panel)
        
        # 加载测试数据
        self.quickpick_panel.load_quickpick_items()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())