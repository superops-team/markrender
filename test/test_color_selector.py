#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试颜色选择器功能
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.quickpick.color_selector import ColorSelectorWidget

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("颜色选择器测试")
        self.setGeometry(100, 100, 400, 300)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建标签显示选中的颜色
        self.selected_color_label = QLabel("选中的颜色: 无")
        layout.addWidget(self.selected_color_label)
        
        # 创建颜色选择器
        self.color_selector = ColorSelectorWidget()
        self.color_selector.color_changed.connect(self.on_color_changed)
        layout.addWidget(self.color_selector)
        
        # 创建测试按钮
        test_button = QPushButton("测试颜色选择")
        test_button.clicked.connect(self.test_color_selection)
        layout.addWidget(test_button)
        
    def on_color_changed(self, color_hex):
        """处理颜色改变事件"""
        self.selected_color_label.setText(f"选中的颜色: {color_hex}")
        # 更新标签的文本颜色以显示效果
        self.selected_color_label.setStyleSheet(f"color: {color_hex}; font-size: 16px; font-weight: bold;")
        
    def test_color_selection(self):
        """测试颜色选择功能"""
        selected_color = self.color_selector.get_selected_color()
        print(f"当前选中的颜色: {selected_color}")

def main():
    app = QApplication(sys.argv)
    
    window = TestWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()