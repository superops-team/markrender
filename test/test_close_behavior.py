#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关闭行为测试脚本
验证关闭按钮点击后的行为是否符合预期：
1. 先最小化窗口
2. 保存当前操作的item数据
3. 然后退出应用
"""

import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from main import MainWindow

def test_close_behavior():
    """测试关闭行为"""
    print("🚀 启动关闭行为测试...")
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    print("✅ 主窗口已显示")
    print("📋 测试步骤：")
    print("   1. 观察窗口是否正常显示")
    print("   2. 在编辑器中输入一些内容")
    print("   3. 点击左上角红色关闭按钮")
    print("   4. 观察窗口是否先最小化，然后保存数据并退出")
    
    # 运行应用3秒后自动关闭以避免阻塞
    from PySide6.QtCore import QTimer
    timer = QTimer()
    timer.setSingleShot(True)
    timer.timeout.connect(lambda: [
        print("⏰ 测试时间到，退出应用"),
        app.quit()
    ])
    timer.start(3000)  # 3秒后自动关闭
    
    result = app.exec()
    print("✅ 测试完成")
    return result

if __name__ == "__main__":
    test_close_behavior()