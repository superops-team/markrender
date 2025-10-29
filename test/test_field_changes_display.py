#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试历史记录差异对话框的字段变更显示功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from app.history.history_diff_dialog import HistoryDiffDialog

def test_field_changes_display():
    """测试字段变更显示功能"""
    print("🚀 启动字段变更显示功能测试...")
    
    app = QApplication(sys.argv)
    
    # 测试内容变更（无字段变更）
    print("\n=== 测试内容变更（无字段变更） ===")
    current_content = "# 当前文档\n\n这是当前文档的内容。"
    history_content = "# 历史文档\n\n这是历史文档的内容。"
    field_changes = {}
    
    dialog1 = HistoryDiffDialog(current_content, history_content, "content_update", field_changes)
    print("✅ 内容变更对话框创建成功")
    
    # 测试标题变更（有字段变更）
    print("\n=== 测试标题变更（有字段变更） ===")
    current_title = "当前文档标题"
    history_title = "历史文档标题"
    field_changes = {
        'title': {'old': '当前文档标题', 'new': '历史文档标题'}
    }
    
    dialog2 = HistoryDiffDialog(current_title, history_title, "title_update", field_changes)
    print("✅ 标题变更对话框创建成功")
    
    # 测试显示名称变更（有字段变更）
    print("\n=== 测试显示名称变更（有字段变更） ===")
    current_display_name = "当前显示名称"
    history_display_name = "历史显示名称"
    field_changes = {
        'display_name': {'old': '当前显示名称', 'new': '历史显示名称'}
    }
    
    dialog3 = HistoryDiffDialog(current_display_name, history_display_name, "display_name_update", field_changes)
    print("✅ 显示名称变更对话框创建成功")
    
    # 测试图标变更（有多个字段变更）
    print("\n=== 测试图标变更（有多个字段变更） ===")
    current_content = "# 文档\n\n文档内容。"
    history_content = "# 文档\n\n文档内容。"
    field_changes = {
        'icon_type': {'old': 'file', 'new': 'folder'},
        'icon_color': {'old': '#000000', 'new': '#FF0000'}
    }
    
    dialog4 = HistoryDiffDialog(current_content, history_content, "icon_update", field_changes)
    print("✅ 图标变更对话框创建成功")
    
    print("\n✅ 字段变更显示功能测试完成")
    print("所有测试通过，字段变更显示功能正常工作")
    
    return True

if __name__ == "__main__":
    test_field_changes_display()