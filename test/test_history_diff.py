#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
历史记录差异对比测试脚本
验证历史记录差异对比功能是否正常工作
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from app.history.history_diff_dialog import HistoryDiffDialog

def test_history_diff():
    """测试历史记录差异对比功能"""
    print("🚀 启动历史记录差异对比测试...")
    
    app = QApplication(sys.argv)
    
    # 测试数据
    current_content = """# 这是当前版本的标题

这是一个当前版本的文档内容，包含一些文本。

## 当前版本的章节

这里有一些当前版本特有的内容。"""
    
    history_content = """# 这是历史版本的标题

这是一个历史版本的文档内容，包含一些文本。

## 历史版本的章节

这里有一些历史版本特有的内容。"""
    
    # 创建并显示差异对话框
    dialog = HistoryDiffDialog(current_content, history_content)
    dialog.show()
    
    print("✅ 差异对比对话框已显示")
    print("📋 测试步骤：")
    print("   1. 观察对话框是否正常显示")
    print("   2. 检查差异是否正确显示（红色表示删除，绿色表示新增）")
    print("   3. 点击'使用历史版本'或'取消'按钮")
    
    # 运行应用10秒后自动关闭以避免阻塞
    from PySide6.QtCore import QTimer
    timer = QTimer()
    timer.setSingleShot(True)
    timer.timeout.connect(lambda: [
        print("⏰ 测试时间到，退出应用"),
        app.quit()
    ])
    timer.start(10000)  # 10秒后自动关闭
    
    result = app.exec()
    print("✅ 测试完成")
    return result

if __name__ == "__main__":
    test_history_diff()