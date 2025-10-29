#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设置对话框优化效果验证脚本
验证设置对话框的样式优化是否符合设计规范
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from app.sidebar.settings_dialog import SettingsDialog

class SettingsDialogTestWindow(QMainWindow):
    """设置对话框优化测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("设置对话框优化效果验证")
        self.setGeometry(100, 100, 400, 300)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 添加测试按钮
        test_button = QPushButton("打开设置对话框")
        test_button.clicked.connect(self.show_settings_dialog)
        layout.addWidget(test_button)
        
    def show_settings_dialog(self):
        """显示设置对话框"""
        dialog = SettingsDialog(self)
        dialog.exec()

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = SettingsDialogTestWindow()
    window.show()
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())