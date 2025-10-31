#!/usr/bin/env python3
"""
Statusbar标签圆角样式测试脚本
验证statusbar上的tag标签使用圆角样式
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app.statusbar.status_bar import StatusBar
from app.preference import AppStyle
from app.preference.style_constants import NEUTRAL_50

class StatusBarTagTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Statusbar标签圆角样式测试")
        self.resize(600, 400)
        
        # 创建中央部件
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建测试内容
        content_widget = QWidget()
        content_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {NEUTRAL_50};
                min-height: 300px;
            }}
        """)
        
        # 创建按钮来测试标签更新
        button_layout = QHBoxLayout()
        self.update_tags_btn = QPushButton("更新标签")
        self.update_tags_btn.clicked.connect(self.update_tags)
        self.clear_tags_btn = QPushButton("清除标签")
        self.clear_tags_btn.clicked.connect(self.clear_tags)
        
        button_layout.addWidget(self.update_tags_btn)
        button_layout.addWidget(self.clear_tags_btn)
        button_layout.addStretch()
        
        # 添加组件到布局
        layout.addWidget(content_widget)
        layout.addLayout(button_layout)
        self.setCentralWidget(central_widget)
        
        # 创建状态栏
        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet(AppStyle().get_status_bar())
        
        # 初始标签
        self.status_bar.update_tags("md,pdf,docx")
        
        # 设置窗口背景色
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {NEUTRAL_50};
            }}
        """)

    def update_tags(self):
        """更新标签"""
        # 模拟不同的标签组合
        import random
        tag_options = ["md", "pdf", "docx", "xlsx", "pptx", "epub", "png", "jpg"]
        selected_tags = random.sample(tag_options, random.randint(1, 4))
        tags_string = ",".join(selected_tags)
        self.status_bar.update_tags(tags_string)
    
    def clear_tags(self):
        """清除标签"""
        self.status_bar.update_tags("")

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 创建测试窗口
    window = StatusBarTagTestWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()