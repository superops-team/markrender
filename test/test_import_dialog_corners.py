#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试导入对话框圆角样式修复
"""

import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QWidget
from app.sidebar.import_dialog import ImportDialog
from db.markrender_manager import MarkRenderManager

class TestImportDialogCorners:
    def __init__(self):
        self.app = QApplication(sys.argv)
        
    def test_corner_styles(self):
        """测试导入对话框圆角样式修复"""
        print("=== 测试导入对话框圆角样式修复 ===")
        
        # 创建模拟的依赖对象
        class MockParent(QWidget):
            pass
            
        class MockQuickPickPanel:
            def load_quickpick_items(self):
                pass
        
        parent = MockParent()
        markrender_manager = MarkRenderManager()
        quickpick_panel = MockQuickPickPanel()
        
        # 创建导入对话框
        dialog = ImportDialog(parent, markrender_manager, quickpick_panel)
        
        # 检查对话框样式
        dialog_style = dialog.styleSheet()
        has_dialog_radius = 'border-radius' in dialog_style and '6px' in dialog_style
        print(f"1. 对话框圆角样式: {'✓' if has_dialog_radius else '✗'}")
        
        # 检查导入区域样式（应无内部圆角）
        # 直接检查已知的content_widget属性
        if hasattr(dialog, 'overlay'):
            overlay_style = dialog.overlay.styleSheet()
            has_overlay_radius = 'border-radius' in overlay_style
            print(f"2. 遮罩层圆角: {'✗ (已移除)' if not has_overlay_radius else '✓ (仍存在)'}")
        
        # 显示对话框（不进入事件循环，仅用于检查UI）
        dialog.show()
        dialog.close()
        
        print("✓ 圆角样式测试完成")
        
    def run(self):
        """运行测试"""
        self.test_corner_styles()
        return self.app

if __name__ == "__main__":
    test_app = TestImportDialogCorners()
    app = test_app.run()
    # 运行短暂的时间然后退出
    from PySide6.QtCore import QTimer
    QTimer.singleShot(1000, app.quit)
    sys.exit(app.exec())