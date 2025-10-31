#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试历史记录面板宽度调整
"""

import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QSplitter
from PySide6.QtCore import Qt
from main import MainWindow

class TestHistoryPanelWidth:
    def __init__(self):
        self.app = QApplication(sys.argv)
        
    def test_panel_widths(self):
        """测试面板宽度调整"""
        print("=== 测试历史记录面板宽度调整 ===")
        
        # 创建主窗口
        main_window = MainWindow()
        main_window.show()
        
        # 获取分割器
        main_splitter = None
        right_splitter = None
        
        # 遍历主窗口的子组件查找分割器
        for child in main_window.findChildren(QSplitter):
            if child.orientation() == Qt.Orientation.Horizontal:
                if main_splitter is None:
                    main_splitter = child
                else:
                    right_splitter = child
                    break
        
        if right_splitter:
            # 获取当前的大小比例
            sizes = right_splitter.sizes()
            total_width = sum(sizes)
            
            if total_width > 0:
                # 计算比例
                quickpick_ratio = sizes[0] / total_width
                editor_ratio = sizes[1] / total_width
                history_ratio = sizes[2] / total_width
                
                print(f"1. QuickPick面板比例: {quickpick_ratio:.2%}")
                print(f"2. 编辑器面板比例: {editor_ratio:.2%}")
                print(f"3. 历史记录面板比例: {history_ratio:.2%}")
                
                # 检查历史记录面板是否为1/5 (20%)
                if abs(history_ratio - 0.2) < 0.01:
                    print("✓ 历史记录面板宽度调整成功 (1/5)")
                else:
                    print(f"✗ 历史记录面板宽度不正确，期望20%，实际{history_ratio:.2%}")
            else:
                print("✗ 无法获取面板尺寸信息")
        else:
            print("✗ 未找到右侧分割器")
        
        main_window.close()
        print("✓ 面板宽度测试完成")
        
    def run(self):
        """运行测试"""
        self.test_panel_widths()
        return self.app

if __name__ == "__main__":
    test_app = TestHistoryPanelWidth()
    app = test_app.run()
    # 运行短暂的时间然后退出
    from PySide6.QtCore import QTimer
    QTimer.singleShot(1000, app.quit)
    sys.exit(app.exec())