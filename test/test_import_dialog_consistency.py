#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试导入对话框与history面板样式一致性
"""

import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QWidget
from app.sidebar.import_dialog import ImportDialog
from db.markrender_manager import MarkRenderManager

class TestImportDialogConsistency:
    def __init__(self):
        self.app = QApplication(sys.argv)
        
    def test_style_consistency(self):
        """测试导入对话框与history面板样式一致性"""
        print("=== 测试导入对话框与history面板样式一致性 ===")
        
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
        print(f"1. 对话框背景色检查: {'✓' if 'background-color' in dialog_style else '✗'}")
        print(f"2. 对话框边框检查: {'✓' if 'border' in dialog_style else '✗'}")
        
        # 检查按钮样式一致性
        if hasattr(dialog, 'confirm_button'):
            confirm_style = dialog.confirm_button.styleSheet()
            has_primary_color = 'background-color' in confirm_style and '#3B82F6' in confirm_style
            has_border_radius = 'border-radius' in confirm_style and '6px' in confirm_style
            has_padding = 'padding' in confirm_style
            print(f"3. 主要按钮样式一致性: {'✓' if all([has_primary_color, has_border_radius, has_padding]) else '✗'}")
            
        if hasattr(dialog, 'close_button'):
            close_style = dialog.close_button.styleSheet()
            has_secondary_color = 'background-color' in close_style and '#F9FAFB' in close_style
            has_border_radius = 'border-radius' in close_style and '6px' in close_style
            has_padding = 'padding' in close_style
            print(f"4. 次要按钮样式一致性: {'✓' if all([has_secondary_color, has_border_radius, has_padding]) else '✗'}")
        
        # 检查导入区域样式
        if hasattr(dialog, 'import_label'):
            label_style = dialog.import_label.styleSheet()
            has_text_color = 'color' in label_style and '#374151' in label_style
            has_font_weight = 'font-weight' in label_style and '600' in label_style
            print(f"5. 导入标签样式一致性: {'✓' if all([has_text_color, has_font_weight]) else '✗'}")
            
        # 检查布局和间距
        print(f"6. 对话框最小尺寸: {dialog.minimumWidth()}x{dialog.minimumHeight()}")
        
        # 显示对话框（不进入事件循环，仅用于检查UI）
        dialog.show()
        dialog.close()
        
        print("✓ 样式一致性测试完成")
        
    def run(self):
        """运行测试"""
        self.test_style_consistency()
        return self.app

if __name__ == "__main__":
    test_app = TestImportDialogConsistency()
    app = test_app.run()
    # 运行短暂的时间然后退出
    from PySide6.QtCore import QTimer
    QTimer.singleShot(1000, app.quit)
    sys.exit(app.exec())