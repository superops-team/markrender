#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试GUI中Bootstrap Icons的显示
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from app.quickpick.panel import QuickPickPanel
from db.markrender_manager import MarkRenderManager

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bootstrap Icons GUI Test")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建MarkRenderManager实例
        manager = MarkRenderManager()
        
        # 创建QuickPickPanel实例
        self.quick_pick_panel = QuickPickPanel(manager, self)
        layout.addWidget(self.quick_pick_panel)
        
        # 设置当前项为None
        self.current_item = None
        
        # 测试创建一些使用Bootstrap Icons的数据
        self.create_test_data(manager)

    def create_test_data(self, manager):
        """创建测试数据"""
        try:
            # 创建使用Bootstrap Icons的文件夹
            folder_id = manager.create_folder(
                title="GUI Bootstrap文件夹",
                icon_type="folder",
                icon_path="icons/folder.svg",  # 使用Bootstrap Icons
                display_name="GUI文件夹"
            )
            print(f"创建GUI Bootstrap文件夹，ID: {folder_id}")
            
            # 创建使用Bootstrap Icons的文件
            file_id = manager.create_file(
                title="GUI Bootstrap文件.md",
                content="# GUI Bootstrap测试\n\n这是GUI中使用Bootstrap Icons的测试文件",
                page_type="markdown",
                icon_type="textarea",
                icon_path="icons/file-earmark-text.svg",  # 使用Bootstrap Icons
                display_name="GUI Markdown文件"
            )
            print(f"创建GUI Bootstrap文件，ID: {file_id}")
            
            # 重新加载数据
            self.quick_pick_panel.load_quickpick_items()
            
        except Exception as e:
            print(f"创建GUI测试数据时出错: {e}")

    def update_editor_and_previewer(self, item_data):
        """模拟父窗口的update_editor_and_previewer方法"""
        print(f"切换到项目: {item_data.get('title', 'Unknown')}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())