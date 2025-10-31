#!/usr/bin/env python3
"""
Statusbar标签圆角样式修复测试脚本
验证statusbar上的tag标签正确显示圆角样式
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app.statusbar.status_bar import StatusBar
from app.preference import AppStyle
from app.preference.style_constants import NEUTRAL_50

class StatusBarTagFixTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Statusbar标签圆角样式修复测试")
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
        
        # 添加组件到布局
        layout.addWidget(content_widget)
        self.setCentralWidget(central_widget)
        
        # 创建状态栏
        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet(AppStyle().get_status_bar())
        
        # 测试不同的标签组合
        self.test_tags()
        
        # 设置窗口背景色
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {NEUTRAL_50};
            }}
        """)

    def test_tags(self):
        """测试标签显示"""
        # 测试多种标签组合
        test_cases = [
            "md,pdf,docx",
            "xlsx,pptx,epub",
            "png,jpg,svg",
            "md",
            "pdf,docx,xlsx,pptx,epub,png,jpg,svg"
        ]
        
        import time
        for i, tags in enumerate(test_cases):
            # 延迟更新以便观察效果
            time.sleep(0.5)
            self.status_bar.update_tags(tags)
            QApplication.processEvents()

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 创建测试窗口
    window = StatusBarTagFixTestWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()