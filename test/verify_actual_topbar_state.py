#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TopBar实际状态验证脚本
检查实际运行时的按钮居中状态和菜单功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from app.topbar.button_controller import ButtonController
from app.preference.style_constants import TOOLBAR_HEIGHT, TOOLBAR_BUTTON_SIZE

class TopBarVerificationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.start_verification()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("TopBar实际状态验证")
        self.setGeometry(100, 100, 800, 400)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("🔍 TopBar实际状态验证")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 创建模拟的history panel和markdown editor
        self.history_panel = QWidget()
        self.markrender_editor = MockMarkRenderEditor()
        
        # 创建实际的ButtonController
        self.button_controller = ButtonController(self, self.history_panel, self.markrender_editor)
        self.button_controller.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border: 2px solid #007AFF;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.button_controller)
        
        # 验证信息显示区域
        self.info_label = QLabel("正在验证TopBar状态...")
        self.info_label.setFont(QFont("Menlo", 11))
        self.info_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 15px;
                color: #333;
            }
        """)
        layout.addWidget(self.info_label)
        
    def start_verification(self):
        """开始验证"""
        # 延迟执行验证，确保UI完全初始化
        QTimer.singleShot(100, self.verify_topbar_state)
        
    def verify_topbar_state(self):
        """验证TopBar状态"""
        results = []
        results.append("🔍 TopBar实际状态验证报告")
        results.append("=" * 50)
        
        # 1. 验证ButtonController容器尺寸
        controller_height = self.button_controller.height()
        expected_height = TOOLBAR_HEIGHT
        results.append(f"\n📐 容器尺寸验证:")
        results.append(f"  ButtonController高度: {controller_height}px")
        results.append(f"  期望高度: {expected_height}px")
        results.append(f"  状态: {'✅ 正确' if controller_height == expected_height else '❌ 错误'}")
        
        # 2. 验证按钮数量和属性
        tool_buttons = []
        all_children = self.button_controller.findChildren(QWidget)
        for child in all_children:
            if hasattr(child, 'setIcon') and hasattr(child, 'setToolTip') and hasattr(child, 'toolTip'):
                tool_buttons.append(child)
        
        results.append(f"\n🔘 按钮验证:")
        results.append(f"  发现按钮数量: {len(tool_buttons)}")
        results.append(f"  期望按钮数量: 3")
        
        # 显示所有按钮的详细信息
        results.append(f"\n  所有按钮详情:")
        for i, button in enumerate(tool_buttons):
            tooltip = button.toolTip() if hasattr(button, 'toolTip') else "未知"
            button_rect = button.geometry()
            button_size = button.size()
            class_name = button.__class__.__name__
            
            results.append(f"    按钮{i+1} ({class_name}):")
            results.append(f"      提示文本: {tooltip}")
            results.append(f"      尺寸: {button_size.width()}×{button_size.height()}px")
            results.append(f"      位置: x={button_rect.x()}, y={button_rect.y()}")
            results.append(f"      可见: {'✅' if button.isVisible() else '❌'}")
            results.append(f"      可用: {'✅' if button.isEnabled() else '❌'}")
            
            # 检查是否有菜单
            if hasattr(button, 'menu') and button.menu():
                menu = button.menu()
                actions = menu.actions()
                results.append(f"      菜单: ✅ 已设置 ({len(actions)}个选项)")
                if actions:
                    results.append(f"      菜单选项:")
                    for action in actions:
                        results.append(f"        - {action.text()}")
            else:
                results.append(f"      菜单: ❌ 无菜单")
        
        # 3. 验证布局信息
        layout = self.button_controller.layout()
        if layout:
            margins = layout.contentsMargins()
            spacing = layout.spacing()
            results.append(f"\n📏 布局信息:")
            results.append(f"  内边距: 左={margins.left()}, 上={margins.top()}, 右={margins.right()}, 下={margins.bottom()}")
            results.append(f"  间距: {spacing}px")
            results.append(f"  对齐方式: {layout.alignment()}")
        
        # 4. 计算垂直居中状态
        if tool_buttons:
            container_height = self.button_controller.height()
            first_button = tool_buttons[0]
            button_rect = first_button.geometry()
            button_height = button_rect.height()
            
            # 计算上方和下方空间
            top_space = button_rect.y()
            bottom_space = container_height - (button_rect.y() + button_height)
            center_offset = top_space - bottom_space
            
            results.append(f"\n📍 垂直居中分析:")
            results.append(f"  容器高度: {container_height}px")
            results.append(f"  按钮高度: {button_height}px")
            results.append(f"  上方空间: {top_space}px")
            results.append(f"  下方空间: {bottom_space}px")
            results.append(f"  垂直偏差: {center_offset}px")
            
            if abs(center_offset) <= 1:
                results.append(f"  居中状态: ✅ 完美居中")
            elif abs(center_offset) <= 3:
                results.append(f"  居中状态: ⚠️ 基本居中")
            else:
                results.append(f"  居中状态: ❌ 未居中")
        
        # 5. 问题诊断
        issues = []
        if controller_height != expected_height:
            issues.append("容器高度不符合期望")
        if len(tool_buttons) != 3:
            issues.append(f"按钮数量不正确（期望3个，实际{len(tool_buttons)}个）")
        
        # 检查前3个按钮的尺寸
        for i, button in enumerate(tool_buttons[:3]):
            size = button.size()
            if size.width() != TOOLBAR_BUTTON_SIZE or size.height() != TOOLBAR_BUTTON_SIZE:
                issues.append(f"按钮{i+1}尺寸不正确")
        
        if issues:
            results.append(f"\n⚠️ 发现问题:")
            for issue in issues:
                results.append(f"  - {issue}")
        else:
            results.append(f"\n✅ 所有检查通过!")
        
        # 6. 建议修复方案
        if issues:
            results.append(f"\n🔧 建议修复:")
            if len(tool_buttons) > 3:
                results.append(f"  1. 检查是否有隐藏的或重复的按钮")
                results.append(f"  2. 验证ButtonController.setup_buttons()方法")
            results.append(f"  3. 检查style_constants.py中的常量值")
            results.append(f"  4. 验证button_controller.py中的尺寸设置顺序")
            results.append(f"  5. 确认CSS样式没有覆盖固定尺寸")
            results.append(f"  6. 检查菜单是否正确设置")
        
        # 显示结果
        result_text = "\n".join(results)
        self.info_label.setText(result_text)
        
        # 打印到控制台
        print(result_text)

class MockMarkRenderEditor:
    """模拟的Markdown编辑器，用于测试"""
    def export_file(self, format_type):
        print(f"模拟导出: {format_type}")

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = TopBarVerificationWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()