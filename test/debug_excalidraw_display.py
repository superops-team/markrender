#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试excalidraw显示问题
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from app.statusbar.status_bar import StatusBar

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Debug Excalidraw Display")
        self.setGeometry(100, 100, 400, 200)
        
        # 设置状态栏
        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)
        
        # 测试excalidraw显示
        print("Testing excalidraw display...")
        self.status_bar.set_page_type("excalidraw")
        self.status_bar.update_tags("")
        
        # 检查显示文本
        display_text = self.status_bar._get_page_type_display_text("excalidraw")
        print(f"Display text for excalidraw: '{display_text}'")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())