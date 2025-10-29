#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编辑器圆角样式验证脚本
验证编辑器区域是否正确应用了圆角样式
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton
from PySide6.QtCore import Qt
from app.preference.app_style import AppStyle
from app.preference.style_constants import EDITOR_RADIUS, RADIUS_MD

class EditorBorderRadiusTestWindow(QMainWindow):
    """编辑器圆角样式测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("编辑器圆角样式验证")
        self.setGeometry(100, 100, 600, 400)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("编辑器圆角样式验证")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 说明文本
        desc = QLabel("""
此脚本用于验证编辑器区域是否正确应用了圆角样式。

期望效果：
- 编辑器父容器应具有 {}px 的圆角
- 样式应与项目整体设计保持一致
        """.format(EDITOR_RADIUS))
        layout.addWidget(desc)
        
        # 显示当前编辑器样式
        style_label = QLabel("当前编辑器父容器样式:")
        layout.addWidget(style_label)
        
        editor_style = AppStyle().get_editor_parent()
        style_text = QLabel(editor_style)
        style_text.setStyleSheet("background-color: #f0f0f0; padding: 10px; font-family: monospace;")
        style_text.setWordWrap(True)
        layout.addWidget(style_text)
        
        # 验证按钮
        verify_btn = QPushButton("验证圆角样式")
        verify_btn.clicked.connect(self.verify_border_radius)
        layout.addWidget(verify_btn)
        
    def verify_border_radius(self):
        """验证圆角样式"""
        editor_style = AppStyle().get_editor_parent()
        if f"border-radius: {EDITOR_RADIUS}px" in editor_style:
            print("✅ 编辑器圆角样式正确应用")
        else:
            print("❌ 编辑器圆角样式未正确应用")

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = EditorBorderRadiusTestWindow()
    window.show()
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())