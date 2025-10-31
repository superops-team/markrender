#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试main.py中excalidraw显示修复
"""

import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from main import MainWindow

class TestApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()
        
    def test_excalidraw_display(self):
        """测试excalidraw显示"""
        print("=== 测试main.py中excalidraw显示修复 ===")
        
        # 模拟一个excalidraw类型的quickpick_item
        quickpick_item = {
            'id': 'test_excalidraw',
            'title': 'Test Excalidraw',
            'page_type': 'excalidraw',
            'tags': ''
        }
        
        print(f"模拟切换到excalidraw项目: {quickpick_item['title']}")
        print(f"项目page_type: {quickpick_item['page_type']}")
        
        # 调用更新方法
        self.main_window._continue_update_editor_and_previewer(quickpick_item)
        
        print(f"status_bar current_page_type: {self.main_window.status_bar.current_page_type}")
        print("检查statusbar是否显示'board'而不是'md'")
        
    def run(self):
        """运行测试"""
        self.test_excalidraw_display()
        # 显示窗口但不进入事件循环
        self.main_window.show()
        return self.app

if __name__ == "__main__":
    test_app = TestApp()
    app = test_app.run()
    # 运行短暂的时间然后退出
    from PySide6.QtCore import QTimer
    QTimer.singleShot(1000, app.quit)
    sys.exit(app.exec())