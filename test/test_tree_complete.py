#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的树形结构功能测试脚本
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
        self.setWindowTitle("QuickPick Tree Structure Test")
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
        
        # 测试创建一些数据
        self.create_test_data(manager)

    def create_test_data(self, manager):
        """创建测试数据"""
        try:
            # 创建根文件夹
            root_folder_id = manager.create_folder("测试根文件夹")
            print(f"创建根文件夹，ID: {root_folder_id}")
            
            # 在根文件夹下创建子文件夹
            sub_folder_id = manager.create_folder("子文件夹1", parent_id=root_folder_id)
            print(f"创建子文件夹，ID: {sub_folder_id}")
            
            # 在子文件夹下创建Markdown文件
            markdown_file_id = manager.create_file(
                title="测试Markdown文件",
                content="# 这是一个测试文件\n\n测试内容",
                parent_id=sub_folder_id,
                page_type='markdown'
            )
            print(f"创建Markdown文件，ID: {markdown_file_id}")
            
            # 在子文件夹下创建Excalidraw文件
            excalidraw_file_id = manager.create_file(
                title="测试Excalidraw文件",
                content="{}",
                parent_id=sub_folder_id,
                page_type='excalidraw',
                page_engine='excalidraw'
            )
            print(f"创建Excalidraw文件，ID: {excalidraw_file_id}")
            
            # 在根目录下创建文件
            root_file_id = manager.create_file(
                title="根目录文件",
                content="# 根目录文件\n\n这是根目录下的文件",
                parent_id=None,
                page_type='markdown'
            )
            print(f"创建根目录文件，ID: {root_file_id}")
            
            # 重新加载数据
            self.quick_pick_panel.load_quickpick_items()
            
        except Exception as e:
            print(f"创建测试数据时出错: {e}")

    def update_editor_and_previewer(self, item_data):
        """模拟父窗口的update_editor_and_previewer方法"""
        print(f"切换到项目: {item_data.get('title', 'Unknown')}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())