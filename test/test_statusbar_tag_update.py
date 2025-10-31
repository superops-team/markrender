#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试状态栏标签更新功能
"""

import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PySide6.QtCore import Qt
from main import MainWindow

class TestApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()
        
    def test_statusbar_tag_update(self):
        """测试状态栏标签更新"""
        print("=== 测试状态栏标签更新功能 ===")
        
        # 模拟一个项目
        test_item = {
            'id': 'test_item_001',
            'title': 'Test Item',
            'page_type': 'markdown',
            'tags': 'initial, test'
        }
        
        print(f"1. 初始状态 - 标签: '{test_item['tags']}'")
        
        # 模拟切换到该项目
        self.main_window._continue_update_editor_and_previewer(test_item)
        print(f"   状态栏当前标签: '{self.main_window.status_bar.current_tags}'")
        
        # 模拟更新标签
        updated_tags = "feature, bug, enhancement"
        print(f"2. 更新标签 - 新标签: '{updated_tags}'")
        
        # 模拟在edit_item中更新标签后的逻辑
        if self.main_window.current_item:
            self.main_window.current_item['tags'] = updated_tags
            
        # 模拟调用状态栏更新方法
        self.main_window.status_bar.update_tags(updated_tags)
        print(f"   状态栏更新后标签: '{self.main_window.status_bar.current_tags}'")
        
        # 验证标签是否正确更新
        if self.main_window.status_bar.current_tags == updated_tags:
            print("   ✓ 状态栏标签更新成功")
        else:
            print("   ✗ 状态栏标签更新失败")
        
    def run(self):
        """运行测试"""
        self.test_statusbar_tag_update()
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