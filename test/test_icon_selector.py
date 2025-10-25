#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试图标选择器功能
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.quickpick.icon_selector import IconSelectorWidget

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("图标选择器测试")
        self.setGeometry(100, 100, 400, 300)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建标签显示选中的图标
        self.selected_icon_label = QLabel("选中的图标: 无")
        layout.addWidget(self.selected_icon_label)
        
        # 创建图标选择器
        self.icon_selector = IconSelectorWidget()
        self.icon_selector.icon_changed.connect(self.on_icon_changed)
        layout.addWidget(self.icon_selector)
        
        # 创建测试按钮
        test_button = QPushButton("测试图标选择")
        test_button.clicked.connect(self.test_icon_selection)
        layout.addWidget(test_button)
        
    def on_icon_changed(self, icon_name):
        """处理图标改变事件"""
        self.selected_icon_label.setText(f"选中的图标: {icon_name}")
        
    def test_icon_selection(self):
        """测试图标选择功能"""
        selected_icon = self.icon_selector.get_selected_icon()
        print(f"当前选中的图标: {selected_icon}")

def main():
    app = QApplication(sys.argv)
    
    window = TestWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()