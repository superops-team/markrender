#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试搜索设置功能
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_search_settings():
    """测试搜索设置功能"""
    from PySide6.QtWidgets import QApplication
    from app.sidebar.settings_dialog import SettingsDialog
    from db.settings_manager import SettingsManager
    
    # 创建 QApplication 实例
    app = QApplication(sys.argv)
    
    # 创建设置管理器
    settings_manager = SettingsManager()
    
    # 创建设置对话框
    dialog = SettingsDialog()
    
    # 显示对话框
    dialog.show()
    
    # 运行应用程序
    app.exec()

if __name__ == "__main__":
    test_search_settings()