#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试QuickPick树形结构点击事件修复
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PySide6.QtCore import Qt
from app.quickpick.panel import QuickPickPanel
from db.markrender_manager import MarkRenderManager

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuickPick Tree Click Test")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 添加说明标签
        info_label = QLabel("测试说明：\n1. 点击任意层级的文件夹item，应该能展开/折叠\n2. 点击第三层级的文件夹item也应该能展开/折叠\n3. 点击文件item应该能切换到对应文件")
        info_label.setStyleSheet("background-color: #f0f0f0; padding: 10px; border-radius: 5px;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # 创建MarkRenderManager实例
        self.manager = MarkRenderManager()
        
        # 创建QuickPickPanel实例
        self.quick_pick_panel = QuickPickPanel(self.manager, self)
        layout.addWidget(self.quick_pick_panel)
        
        # 设置当前项为None
        self.current_item = None
        
        # 刷新按钮
        refresh_btn = QPushButton("刷新列表")
        refresh_btn.clicked.connect(self.quick_pick_panel.load_quickpick_items)
        layout.addWidget(refresh_btn)
        
        # 创建测试数据按钮
        test_data_btn = QPushButton("创建测试数据（三层结构）")
        test_data_btn.clicked.connect(self.create_test_data)
        layout.addWidget(test_data_btn)
        
    def create_test_data(self):
        """创建三层结构的测试数据"""
        try:
            print("创建三层结构测试数据...")
            
            # 创建根文件夹
            root_folder_id = self.manager.create_folder("测试根文件夹")
            print(f"创建根文件夹，ID: {root_folder_id}")
            
            # 在根文件夹下创建子文件夹
            sub_folder_id = self.manager.create_folder("测试子文件夹", parent_id=root_folder_id)
            print(f"创建子文件夹，ID: {sub_folder_id}")
            
            # 在子文件夹下创建第三层文件夹
            third_folder_id = self.manager.create_folder("测试第三层文件夹", parent_id=sub_folder_id)
            print(f"创建第三层文件夹，ID: {third_folder_id}")
            
            # 在第三层文件夹下创建文件
            file_id = self.manager.create_file(
                title="测试第三层文件.md",
                content="# 第三层文件\n\n这是第三层文件夹中的文件",
                parent_id=third_folder_id,
                page_type='markdown'
            )
            print(f"创建第三层文件，ID: {file_id}")
            
            # 重新加载数据
            self.quick_pick_panel.load_quickpick_items()
            print("测试数据创建完成并刷新列表")
            
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