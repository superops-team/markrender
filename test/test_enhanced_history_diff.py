#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强历史记录差异功能测试
验证增强后的历史记录差异功能是否正常工作
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from main import MainWindow

def test_enhanced_history_diff():
    """测试增强后的历史记录差异功能"""
    print("🚀 启动增强历史记录差异功能测试...")
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    print("✅ 主窗口已显示")
    print("📋 测试步骤：")
    print("   1. 观察窗口是否正常显示")
    print("   2. 点击右上角的历史记录按钮显示历史面板")
    print("   3. 选择一个历史记录项")
    print("   4. 观察是否弹出差异对比对话框")
    print("   5. 检查是否有字段变更区域显示")
    print("   6. 检查内容差异是否正确显示")
    print("   7. 点击'使用历史版本'或'取消'按钮")
    
    # 运行应用15秒后自动关闭以避免阻塞
    from PySide6.QtCore import QTimer
    timer = QTimer()
    timer.setSingleShot(True)
    timer.timeout.connect(lambda: [
        print("⏰ 测试时间到，退出应用"),
        app.quit()
    ])
    timer.start(15000)  # 15秒后自动关闭
    
    result = app.exec()
    print("✅ 增强历史记录差异功能测试完成")
    return result

if __name__ == "__main__":
    test_enhanced_history_diff()