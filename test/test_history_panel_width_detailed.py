#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细测试历史记录面板宽度调整
"""

import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QSplitter
from PySide6.QtCore import Qt, QTimer
from main import MainWindow

class TestHistoryPanelWidthDetailed:
    def __init__(self):
        self.app = QApplication(sys.argv)
        
    def test_panel_widths_detailed(self):
        """详细测试面板宽度调整"""
        print("=== 详细测试历史记录面板宽度调整 ===")
        
        # 创建主窗口
        main_window = MainWindow()
        main_window.show()
        
        # 等待窗口完全初始化
        QTimer.singleShot(500, lambda: self.check_panel_widths(main_window))
        
        # 运行应用
        self.app.exec()
        
    def check_panel_widths(self, main_window):
        """检查面板宽度"""
        try:
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
                        
                    # 检查比例总和是否为100%
                    total_ratio = quickpick_ratio + editor_ratio + history_ratio
                    if abs(total_ratio - 1.0) < 0.01:
                        print("✓ 面板比例总和正确 (100%)")
                    else:
                        print(f"✗ 面板比例总和不正确，期望100%，实际{total_ratio:.2%}")
                else:
                    print("✗ 无法获取面板尺寸信息")
            else:
                print("✗ 未找到右侧分割器")
                
        except Exception as e:
            print(f"✗ 检查面板宽度时出错: {e}")
        finally:
            main_window.close()
            print("✓ 面板宽度详细测试完成")
            self.app.quit()

    def run(self):
        """运行测试"""
        self.test_panel_widths_detailed()
        return self.app

if __name__ == "__main__":
    test_app = TestHistoryPanelWidthDetailed()
    app = test_app.run()
    sys.exit(app.exec())