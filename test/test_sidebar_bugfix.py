#!/usr/bin/env python3
"""
Sidebar按钮互斥效果bug修复测试脚本
验证sidebar按钮互斥效果的bug修复
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app.sidebar.sidebar_manager import SidebarManager
from app.preference import AppStyle
from app.preference.style_constants import NEUTRAL_50

class SidebarBugfixTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sidebar按钮互斥效果bug修复测试")
        self.resize(600, 400)
        
        # 创建一个模拟的quickpick_panel属性
        self.quickpick_panel = MockQuickPickPanel()
        
        # 创建中央部件
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建侧边栏
        self.sidebar = SidebarManager(self)
        self.sidebar.setStyleSheet(AppStyle().get_sidebar())
        self.sidebar.setFixedWidth(59)
        
        # 添加侧边栏到布局
        layout.addWidget(self.sidebar)
        self.setCentralWidget(central_widget)
        
        # 设置窗口背景色
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {NEUTRAL_50};
            }}
        """)

class MockQuickPickPanel:
    """模拟的QuickPickPanel类，用于测试"""
    def __init__(self):
        self.visible = True
    
    def show(self):
        self.visible = True
        print("QuickPick面板已显示")
    
    def hide(self):
        self.visible = False
        print("QuickPick面板已隐藏")

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 创建测试窗口
    window = SidebarBugfixTestWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()