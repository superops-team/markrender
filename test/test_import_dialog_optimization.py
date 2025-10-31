#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试优化后的导入对话框
"""

import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QWidget
from app.sidebar.import_dialog import ImportDialog
from db.markrender_manager import MarkRenderManager

class TestImportDialog:
    def __init__(self):
        self.app = QApplication(sys.argv)
        
    def test_import_dialog_ui(self):
        """测试导入对话框UI优化效果"""
        print("=== 测试优化后的导入对话框 ===")
        
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
        
        # 检查对话框属性
        print(f"1. 对话框标题: {dialog.windowTitle()}")
        print(f"2. 对话框尺寸: {dialog.width()}x{dialog.height()}")
        
        # 检查主要组件是否存在
        if hasattr(dialog, 'import_label'):
            print(f"3. 导入标签文本: {dialog.import_label.text()}")
            
        if hasattr(dialog, 'format_label'):
            print(f"4. 格式标签文本: {dialog.format_label.text()}")
            
        if hasattr(dialog, 'confirm_button'):
            print(f"5. 确认按钮文本: {dialog.confirm_button.text()}")
            
        if hasattr(dialog, 'close_button'):
            print(f"6. 关闭按钮文本: {dialog.close_button.text()}")
        
        # 检查样式应用
        dialog_style = dialog.styleSheet()
        if "border-radius" in dialog_style:
            print("7. ✓ 对话框圆角样式已应用")
        else:
            print("7. ✗ 对话框圆角样式未应用")
            
        # 显示对话框（不进入事件循环，仅用于检查UI）
        dialog.show()
        
        # 检查组件样式
        if hasattr(dialog, 'confirm_button'):
            button_style = dialog.confirm_button.styleSheet()
            if "background-color" in button_style and "border-radius" in button_style:
                print("8. ✓ 主要按钮样式已正确应用")
            else:
                print("8. ✗ 主要按钮样式存在问题")
                
        if hasattr(dialog, 'close_button'):
            button_style = dialog.close_button.styleSheet()
            if "background-color" in button_style and "border-radius" in button_style:
                print("9. ✓ 次要按钮样式已正确应用")
            else:
                print("9. ✗ 次要按钮样式存在问题")
        
        dialog.close()
        print("✓ 导入对话框UI测试完成")
        
    def run(self):
        """运行测试"""
        self.test_import_dialog_ui()
        return self.app

if __name__ == "__main__":
    test_app = TestImportDialog()
    app = test_app.run()
    # 运行短暂的时间然后退出
    from PySide6.QtCore import QTimer
    QTimer.singleShot(1000, app.quit)
    sys.exit(app.exec())