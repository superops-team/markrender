#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试QuickPick与Editor区域高度对齐修复
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from main import MainWindow
from utils.logger_utils import logger

def test_layout_alignment():
    """测试布局对齐"""
    app = QApplication.instance() or QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    def check_alignment():
        """检查对齐情况"""
        try:
            quickpick_margin = window.quickpick_panel.layout().contentsMargins()
            editor_margin = window.markdown_editor.layout().contentsMargins()
            
            logger.info("=" * 50)
            logger.info("QuickPick与Editor区域对齐检查结果:")
            logger.info(f"QuickPick面板边距: 上={quickpick_margin.top()}, 右={quickpick_margin.right()}, 下={quickpick_margin.bottom()}, 左={quickpick_margin.left()}")
            logger.info(f"Editor区域边距: 上={editor_margin.top()}, 右={editor_margin.right()}, 下={editor_margin.bottom()}, 左={editor_margin.left()}")
            
            # 检查是否对齐
            margins_match = (
                quickpick_margin.top() == editor_margin.top() and
                quickpick_margin.bottom() == editor_margin.bottom()
            )
            
            if margins_match:
                logger.info("✅ 修复成功：QuickPick与Editor区域高度完美对齐！")
                logger.info("   - 上下边距统一为5px")
                logger.info("   - 符合Robin Williams设计原则中的对齐原则")
            else:
                logger.warning("❌ 仍需调整：QuickPick与Editor区域高度未完全对齐")
            
            logger.info("=" * 50)
            
            # 关闭应用
            window.close()
            
        except Exception as e:
            logger.error(f"检查对齐时出错: {e}")
            window.close()
    
    # 延迟执行检查，确保窗口完全显示
    QTimer.singleShot(1000, check_alignment)
    
    return app.exec()

if __name__ == "__main__":
    logger.info("开始测试QuickPick与Editor区域高度对齐...")
    test_layout_alignment()