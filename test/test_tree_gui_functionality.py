#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试树形结构GUI功能，验证父子节点关系和添加按钮功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PySide6.QtCore import Qt
from app.quickpick.panel import QuickPickPanel
from db.markrender_manager import MarkRenderManager

class TestTreeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("树形结构GUI功能测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 添加说明标签
        info_label = QLabel("测试说明：\n1. 每个节点最右侧有两个按钮（三个点和加号）\n2. 加号按钮只能添加当前节点的子节点\n3. 右键菜单也能添加子节点\n4. 验证父子关系正确性")
        info_label.setStyleSheet("background-color: #f0f0f0; padding: 10px; border-radius: 5px;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # 创建MarkRenderManager实例
        manager = MarkRenderManager()
        
        # 创建测试数据按钮
        test_data_btn = QPushButton("创建测试数据")
        test_data_btn.clicked.connect(lambda: self.create_test_data(manager))
        layout.addWidget(test_data_btn)
        
        # 创建QuickPickPanel实例
        self.quick_pick_panel = QuickPickPanel(manager, self)
        layout.addWidget(self.quick_pick_panel)
        
        # 设置当前项为None
        self.current_item = None
        
        # 刷新按钮
        refresh_btn = QPushButton("刷新列表")
        refresh_btn.clicked.connect(self.quick_pick_panel.load_quickpick_items)
        layout.addWidget(refresh_btn)

    def create_test_data(self, manager):
        """创建测试数据"""
        try:
            # 创建根文件夹
            root_folder_id = manager.create_folder(
                title="GUI测试根文件夹",
                icon_type="folder",
                icon_path="icons/folder.svg",
                display_name="GUI根文件夹"
            )
            print(f"创建GUI测试根文件夹，ID: {root_folder_id}")
            
            # 在根文件夹下创建子文件夹
            sub_folder_id = manager.create_folder(
                title="GUI测试子文件夹",
                parent_id=root_folder_id,
                icon_type="folder",
                icon_path="icons/folder.svg",
                display_name="GUI子文件夹"
            )
            print(f"创建GUI测试子文件夹，ID: {sub_folder_id}")
            
            # 在根文件夹下创建文件
            root_file_id = manager.create_file(
                title="GUI测试根文件.md",
                content="# GUI测试根文件\n\n这是GUI测试根文件夹中的文件",
                parent_id=root_folder_id,
                page_type="markdown",
                icon_type="textarea",
                icon_path="icons/file-earmark-text.svg",
                display_name="GUI根文件"
            )
            print(f"创建GUI测试根文件，ID: {root_file_id}")
            
            # 重新加载数据
            self.quick_pick_panel.load_quickpick_items()
            print("测试数据创建完成并刷新列表")
            
        except Exception as e:
            print(f"创建GUI测试数据时出错: {e}")

    def update_editor_and_previewer(self, item_data):
        """模拟父窗口的update_editor_and_previewer方法"""
        print(f"切换到项目: {item_data.get('title', 'Unknown')}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestTreeWindow()
    window.show()
    sys.exit(app.exec())