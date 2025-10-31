#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细调试excalidraw显示问题
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from app.statusbar.status_bar import StatusBar

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Detailed Debug Excalidraw Display")
        self.setGeometry(100, 100, 400, 200)
        
        # 设置状态栏
        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)
        
        # 逐步测试
        print("=== 详细调试excalidraw显示问题 ===")
        
        # 1. 直接设置excalidraw
        print("1. 直接设置excalidraw...")
        self.status_bar.set_page_type("excalidraw")
        print(f"   current_page_type: {self.status_bar.current_page_type}")
        print(f"   current_page_type type: {type(self.status_bar.current_page_type)}")
        print(f"   current_page_type truthiness: {bool(self.status_bar.current_page_type)}")
        if self.status_bar.current_page_type:
            print(f"   current_page_type strip: '{self.status_bar.current_page_type.strip()}'")
            print(f"   current_page_type strip truthiness: {bool(self.status_bar.current_page_type.strip())}")
        
        # 2. 清除标签
        print("2. 清除标签...")
        self.status_bar.update_tags("")
        print(f"   current_tags: '{self.status_bar.current_tags}'")
        print(f"   current_tags type: {type(self.status_bar.current_tags)}")
        print(f"   current_tags truthiness: {bool(self.status_bar.current_tags)}")
        
        # 3. 检查映射函数
        print("3. 检查映射函数...")
        display_text = self.status_bar._get_page_type_display_text("excalidraw")
        print(f"   display_text for excalidraw: '{display_text}'")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())