#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试QuickPick树形结构增量更新功能
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QTextEdit
from PySide6.QtCore import Qt
from app.quickpick.panel import QuickPickPanel
from db.markrender_manager import MarkRenderManager

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuickPick Tree Incremental Update Test")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 添加说明标签
        info_label = QLabel("测试说明：\n1. 点击设置按钮编辑item并保存后，应该只更新该节点而不是刷新整个树\n2. 树形结构应该保持不变\n3. 其他节点的状态（展开/折叠）应该保持不变")
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
        
        # 日志显示区域
        self.log_area = QTextEdit()
        self.log_area.setMaximumHeight(100)
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)
        
        # 创建测试数据按钮
        test_data_btn = QPushButton("创建测试数据")
        test_data_btn.clicked.connect(self.create_test_data)
        layout.addWidget(test_data_btn)
        
        # 刷新按钮
        refresh_btn = QPushButton("刷新列表")
        refresh_btn.clicked.connect(self.quick_pick_panel.load_quickpick_items)
        layout.addWidget(refresh_btn)
        
    def log_message(self, message):
        """记录日志消息"""
        self.log_area.append(message)
        print(message)
        
    def create_test_data(self):
        """创建测试数据"""
        try:
            self.log_message("开始创建测试数据...")
            
            # 创建根文件夹
            root_folder_id = self.manager.create_folder("测试根文件夹")
            self.log_message(f"创建根文件夹，ID: {root_folder_id}")
            
            # 在根文件夹下创建子文件夹
            sub_folder_id = self.manager.create_folder("测试子文件夹", parent_id=root_folder_id)
            self.log_message(f"创建子文件夹，ID: {sub_folder_id}")
            
            # 在子文件夹下创建文件
            file_id = self.manager.create_file(
                title="测试文件.md",
                content="# 测试文件\n\n这是测试文件的内容",
                parent_id=sub_folder_id,
                page_type='markdown'
            )
            self.log_message(f"创建文件，ID: {file_id}")
            
            # 重新加载数据
            self.quick_pick_panel.load_quickpick_items()
            self.log_message("测试数据创建完成并刷新列表")
            
        except Exception as e:
            self.log_message(f"创建测试数据时出错: {e}")
            
    def update_editor_and_previewer(self, item_data):
        """模拟父窗口的update_editor_and_previewer方法"""
        self.log_message(f"切换到项目: {item_data.get('title', 'Unknown')} (ID: {item_data.get('id', 'N/A')})")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())