#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图标选择器功能演示
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.quickpick.icon_selector import IconSelectorDialog, IconSelectorWidget

class DemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("图标选择器功能演示")
        self.setGeometry(100, 100, 500, 400)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 标题
        title_label = QLabel("图标选择器功能演示")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)
        
        # 说明文本
        description = QLabel("点击下方按钮打开图标选择对话框，选择一个图标进行预览")
        description.setStyleSheet("font-size: 14px; margin: 10px;")
        layout.addWidget(description)
        
        # 创建图标显示区域
        icon_display_layout = QHBoxLayout()
        icon_display_layout.setContentsMargins(20, 20, 20, 20)
        
        self.icon_label = QLabel("选中的图标将显示在这里")
        self.icon_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #cccccc;
                border-radius: 10px;
                padding: 20px;
                font-size: 16px;
                text-align: center;
                min-height: 100px;
            }
        """)
        icon_display_layout.addWidget(self.icon_label)
        
        layout.addLayout(icon_display_layout)
        
        # 创建按钮区域
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(20, 20, 20, 20)
        
        # 图标选择器组件
        self.icon_selector = IconSelectorWidget()
        self.icon_selector.icon_changed.connect(self.on_icon_changed)
        button_layout.addWidget(self.icon_selector)
        
        # 直接打开对话框的按钮
        open_dialog_button = QPushButton("打开图标选择对话框")
        open_dialog_button.clicked.connect(self.open_icon_dialog)
        button_layout.addWidget(open_dialog_button)
        
        layout.addLayout(button_layout)
        
        # 状态标签
        self.status_label = QLabel("状态: 等待选择图标")
        self.status_label.setStyleSheet("font-size: 14px; color: #666666; margin: 10px;")
        layout.addWidget(self.status_label)
        
    def on_icon_changed(self, icon_name):
        """处理图标改变事件"""
        self.status_label.setText(f"状态: 已选择图标 '{icon_name}'")
        self.icon_label.setText(f"选中的图标: {icon_name}")
        
    def open_icon_dialog(self):
        """打开图标选择对话框"""
        dialog = IconSelectorDialog(parent=self)
        if dialog.exec():
            selected_icon = dialog.get_selected_icon()
            if selected_icon:
                self.status_label.setText(f"状态: 通过对话框选择了图标 '{selected_icon}'")
                self.icon_label.setText(f"选中的图标: {selected_icon}")
                # 更新图标选择器组件
                self.icon_selector.set_icon(selected_icon)

def main():
    app = QApplication(sys.argv)
    
    window = DemoWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()