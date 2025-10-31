#!/usr/bin/env python3
"""
Sidebar布局测试脚本
验证sidebar贯穿到软件最底部的布局效果
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app.sidebar.sidebar_manager import SidebarManager
from app.statusbar.status_bar import StatusBar
from app.preference import AppStyle
from app.preference.style_constants import NEUTRAL_50

class SidebarLayoutTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sidebar布局测试")
        self.resize(800, 600)
        
        # 创建一个模拟的quickpick_panel属性
        self.quickpick_panel = MockQuickPickPanel()
        
        # 创建中央部件
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建主分割器
        from PySide6.QtWidgets import QSplitter
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 创建侧边栏
        self.sidebar = SidebarManager(self)
        self.sidebar.setStyleSheet(AppStyle().get_sidebar())
        self.sidebar.setFixedWidth(59)
        
        # 创建内容区域
        content_widget = QWidget()
        content_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {NEUTRAL_50};
                min-height: 400px;
            }}
        """)
        
        # 添加组件到分割器
        main_splitter.addWidget(self.sidebar)
        main_splitter.addWidget(content_widget)
        main_splitter.setSizes([59, 741])
        
        main_layout.addWidget(main_splitter)
        self.setCentralWidget(central_widget)
        
        # 创建状态栏
        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet(AppStyle().get_status_bar())
        
        # 测试标签显示
        self.status_bar.update_tags("md,pdf,docx")
        
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
    
    def hide(self):
        self.visible = False

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 创建测试窗口
    window = SidebarLayoutTestWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()