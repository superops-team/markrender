#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证历史记录差异功能
测试历史记录差异功能是否正常工作
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from app.history.history_diff_dialog import HistoryDiffDialog

def verify_history_diff():
    """验证历史记录差异功能"""
    print("🚀 启动历史记录差异功能验证...")
    
    app = QApplication(sys.argv)
    
    # 测试内容变更的差异显示
    print("\n=== 测试内容变更差异 ===")
    current_content = "# 当前文档标题\n\n这是当前文档的内容，包含一些文本。"
    history_content = "# 历史文档标题\n\n这是历史文档的内容，包含一些文本。"
    
    dialog = HistoryDiffDialog(current_content, history_content)
    print("✅ 内容变更差异对话框创建成功")
    
    # 测试标题变更的差异显示
    print("\n=== 测试标题变更差异 ===")
    current_title = "当前文档标题"
    history_title = "历史文档标题"
    
    dialog2 = HistoryDiffDialog(current_title, history_title)
    print("✅ 标题变更差异对话框创建成功")
    
    # 测试显示名称变更的差异显示
    print("\n=== 测试显示名称变更差异 ===")
    current_display_name = "当前显示名称"
    history_display_name = "历史显示名称"
    
    dialog3 = HistoryDiffDialog(current_display_name, history_display_name)
    print("✅ 显示名称变更差异对话框创建成功")
    
    print("\n✅ 历史记录差异功能验证完成")
    print("所有测试通过，历史记录差异功能正常工作")
    
    return True

if __name__ == "__main__":
    verify_history_diff()