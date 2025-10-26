#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试图标颜色在UI中的显示效果
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt
from db.markrender_manager import MarkRenderManager
from app.quickpick.panel import QuickPickPanel

class TestIconColorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("图标颜色显示测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建标题
        title_label = QLabel("图标颜色显示测试")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)
        
        # 说明文本
        description = QLabel("请查看下方的QuickPick面板，确认图标颜色是否正确显示")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setStyleSheet("font-size: 14px; margin: 10px;")
        layout.addWidget(description)
        
        # 创建数据库管理器
        self.manager = MarkRenderManager()
        
        # 创建QuickPick面板
        self.quickpick_panel = QuickPickPanel(self.manager)
        layout.addWidget(self.quickpick_panel)
        
        # 加载测试数据
        self.load_test_data()

    def load_test_data(self):
        """加载测试数据"""
        # 创建带不同颜色的测试文件
        test_files = [
            {
                'title': '红色图标文件',
                'content': '# 红色图标测试',
                'page_type': 'markdown',
                'icon_path': 'icons/palette.svg',
                'icon_color': '#FF0000'  # 红色
            },
            {
                'title': '绿色图标文件',
                'content': '# 绿色图标测试',
                'page_type': 'markdown',
                'icon_path': 'icons/palette.svg',
                'icon_color': '#00FF00'  # 绿色
            },
            {
                'title': '蓝色图标文件',
                'content': '# 蓝色图标测试',
                'page_type': 'markdown',
                'icon_path': 'icons/palette.svg',
                'icon_color': '#0000FF'  # 蓝色
            }
        ]
        
        # 保存测试文件到数据库
        for file_data in test_files:
            self.manager.create_file(**file_data)
        
        # 重新加载QuickPick面板数据
        self.quickpick_panel.load_quickpick_items()

def main():
    app = QApplication(sys.argv)
    
    window = TestIconColorWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()