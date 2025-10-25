#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试QuickPick功能与图标路径修复
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.quickpick.panel import QuickPickPanel
from db.markrender_manager import MarkRenderManager

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuickPick 图标测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建数据库管理器
        self.markrender_manager = MarkRenderManager()
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建QuickPick面板
        self.quickpick_panel = QuickPickPanel(self.markrender_manager)
        layout.addWidget(self.quickpick_panel)
        
        # 初始化测试数据
        self.init_test_data()
        
        # 刷新显示
        self.quickpick_panel.load_quickpick_items()

    def init_test_data(self):
        """初始化测试数据"""
        manager = self.markrender_manager
        
        # 创建带自定义图标的文件
        manager.create_file(
            title='调色板文件',
            content='# 调色板\n这是一个带调色板图标的文件',
            page_type='markdown',
            icon_path='icons/palette.svg'
        )
        
        manager.create_file(
            title='文件夹示例',
            content='# 文件夹\n这是一个带文件夹图标的文件',
            page_type='markdown',
            icon_path='icons/folder.svg'
        )
        
        manager.create_file(
            title='文本文件',
            content='# 文本\n这是一个带文本图标的文件',
            page_type='markdown',
            icon_path='icons/file-earmark-text.svg'
        )
        
        manager.create_file(
            title='文本区域',
            content='# 文本区域\n这是一个带文本区域图标的文件',
            page_type='markdown',
            icon_type='textarea'
        )
        
        # 创建带自定义图标的目录
        folder_id = manager.create_folder(
            title='图标目录',
            icon_path='icons/folder.svg'
        )
        
        # 在目录中创建子文件
        manager.create_file(
            title='子文件',
            content='# 子文件\n这是目录中的文件',
            parent_id=folder_id,
            page_type='markdown',
            icon_path='icons/file-earmark-text.svg'
        )

def main():
    app = QApplication(sys.argv)
    
    window = TestWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()