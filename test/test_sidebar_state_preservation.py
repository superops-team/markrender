#!/usr/bin/env python3
"""
Sidebar按钮状态保留测试脚本
验证sidebar按钮在互斥操作后能保留各自的状态
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app.sidebar.sidebar_manager import SidebarManager
from app.preference import AppStyle
from app.preference.style_constants import NEUTRAL_50

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

class SidebarStatePreservationTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sidebar按钮状态保留测试")
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
        
        # 添加状态显示标签
        self.status_label = QLabel("状态: 等待测试")
        self.status_label.setStyleSheet("padding: 10px; color: #333;")
        
        # 添加组件到布局
        layout.addWidget(self.sidebar)
        layout.addWidget(self.status_label)
        self.setCentralWidget(central_widget)
        
        # 设置窗口背景色
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {NEUTRAL_50};
            }}
        """)
        
        # 连接按钮状态变化信号（用于测试）
        self.sidebar.toggle_quickpick_btn.toggled.connect(self.on_quickpick_toggled)
        self.sidebar.import_btn.toggled.connect(self.on_import_toggled)
        self.sidebar.settings_btn.toggled.connect(self.on_settings_toggled)
    
    def on_quickpick_toggled(self, checked):
        status = "展开" if checked else "折叠"
        self.status_label.setText(f"状态: QuickPick按钮{status}")
        print(f"QuickPick按钮状态: {status}")
    
    def on_import_toggled(self, checked):
        status = "选中" if checked else "未选中"
        self.status_label.setText(f"状态: 导入按钮{status}")
        print(f"导入按钮状态: {status}")
    
    def on_settings_toggled(self, checked):
        status = "选中" if checked else "未选中"
        self.status_label.setText(f"状态: 设置按钮{status}")
        print(f"设置按钮状态: {status}")

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 创建测试窗口
    window = SidebarStatePreservationTestWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()