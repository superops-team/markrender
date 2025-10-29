#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试历史记录差异对话框
验证HistoryDiffDialog在真实场景下的工作情况
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication
from app.history.history_diff_dialog import HistoryDiffDialog

def test_history_diff_dialog():
    """测试HistoryDiffDialog在真实场景下的工作情况"""
    print("🚀 启动HistoryDiffDialog调试...")
    
    app = QApplication(sys.argv)
    
    # 模拟真实使用场景的数据
    # 当前内容（用户正在编辑的内容）
    current_content = """# 项目计划书

## 项目概述

这是一个重要的项目，旨在解决当前市场中的关键问题。

## 目标

- 提高效率
- 降低成本
- 增强用户体验

## 实施步骤

1. 需求分析
2. 设计阶段
3. 开发阶段
4. 测试阶段
5. 部署上线

## 预算

总预算为100万元。"""
    
    # 历史内容（用户选择的历史版本）
    history_content = """# 项目计划书初稿

## 项目概述

这是一个重要的项目，旨在解决市场中的问题。

## 目标

- 提高效率
- 降低成本

## 实施步骤

1. 需求分析
2. 设计阶段
3. 开发阶段
4. 测试阶段

## 预算

总预算为50万元。"""
    
    print("当前内容长度:", len(current_content))
    print("历史内容长度:", len(history_content))
    
    # 创建并显示差异对话框
    dialog = HistoryDiffDialog(current_content, history_content)
    dialog.show()
    
    print("✅ 差异对比对话框已显示")
    print("📋 调试步骤：")
    print("   1. 观察对话框是否正常显示")
    print("   2. 检查差异是否正确显示")
    print("   3. 红色应该是当前内容中独有的部分")
    print("   4. 绿色应该是历史内容中独有的部分")
    print("   5. 窗口应该显示20秒")
    
    # 运行应用20秒后自动关闭以避免阻塞
    from PySide6.QtCore import QTimer
    timer = QTimer()
    timer.setSingleShot(True)
    timer.timeout.connect(lambda: [
        print("⏰ 调试时间到，退出应用"),
        app.quit()
    ])
    timer.start(20000)  # 20秒后自动关闭
    
    result = app.exec()
    print("✅ 调试完成")
    return result

if __name__ == "__main__":
    test_history_diff_dialog()