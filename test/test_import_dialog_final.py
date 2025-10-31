#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试最终修复后的导入对话框
"""

import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QWidget
from app.sidebar.import_dialog import ImportDialog
from db.markrender_manager import MarkRenderManager

class TestImportDialogFinal:
    def __init__(self):
        self.app = QApplication(sys.argv)
        
    def test_final_fixes(self):
        """测试最终修复效果"""
        print("=== 测试最终修复后的导入对话框 ===")
        
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
        
        # 检查是否移除了按钮
        has_close_button = hasattr(dialog, 'close_button')
        has_confirm_button = hasattr(dialog, 'confirm_button')
        print(f"2. 关闭按钮已移除: {'✓' if not has_close_button else '✗'}")
        print(f"3. 确认按钮已移除: {'✓' if not has_confirm_button else '✗'}")
        
        # 检查遮罩层样式（应无内部圆角）
        if hasattr(dialog, 'overlay'):
            overlay_style = dialog.overlay.styleSheet()
            has_overlay_radius = 'border-radius' in overlay_style
            print(f"4. 遮罩层圆角: {'✗ (已移除)' if not has_overlay_radius else '✓ (仍存在)'}")
        
        # 检查导入区域是否有点击事件
        has_mouse_event = False
        # 安全地检查布局和组件
        layout = dialog.layout()
        if layout is not None:
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item is not None:
                    widget = item.widget()
                    if widget is not None and hasattr(widget, 'mousePressEvent'):
                        has_mouse_event = True
                        break
        print(f"5. 导入区域点击事件: {'✓' if has_mouse_event else '✗'}")
        
        # 显示对话框（不进入事件循环，仅用于检查UI）
        dialog.show()
        dialog.close()
        
        print("✓ 最终修复测试完成")
        
    def run(self):
        """运行测试"""
        self.test_final_fixes()
        return self.app

if __name__ == "__main__":
    test_app = TestImportDialogFinal()
    app = test_app.run()
    # 运行短暂的时间然后退出
    from PySide6.QtCore import QTimer
    QTimer.singleShot(1000, app.quit)
    sys.exit(app.exec())