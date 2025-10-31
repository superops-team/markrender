#!/usr/bin/env python3
"""
Sidebar按钮互斥效果测试脚本
验证sidebar按钮的互斥效果，确保同时只能选择一个按钮
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QSplitter
from PySide6.QtCore import Qt

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app.sidebar.sidebar_manager import SidebarManager
from app.preference import AppStyle
from app.preference.style_constants import NEUTRAL_50, NEUTRAL_200

class SidebarMutualExclusionTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sidebar按钮互斥效果测试")
        self.resize(800, 600)
        
        # 设置主窗口样式
        self.setStyleSheet(AppStyle().get_main_style())
        
        # 创建中央部件
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建主分割器
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 创建侧边栏
        self.sidebar = SidebarManager(self)
        self.sidebar.setStyleSheet(AppStyle().get_sidebar())
        self.sidebar.setFixedWidth(59)
        
        # 创建内容区域
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        # 添加测试内容
        test_content = QWidget()
        test_content.setStyleSheet(f"""
            QWidget {{
                background-color: {NEUTRAL_50};
                border: 1px solid {NEUTRAL_200};
                border-radius: 6px;
                min-height: 400px;
            }}
        """)
        content_layout.addWidget(test_content)
        
        # 添加组件到分割器
        main_splitter.addWidget(self.sidebar)
        main_splitter.addWidget(content_widget)
        main_splitter.setSizes([59, 741])
        
        main_layout.addWidget(main_splitter)
        self.setCentralWidget(central_widget)
        
        # 设置窗口背景色
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {NEUTRAL_50};
            }}
        """)

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 创建测试窗口
    window = SidebarMutualExclusionTestWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()