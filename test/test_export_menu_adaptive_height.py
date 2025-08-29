#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导出菜单高度自适应测试脚本
验证修复后的导出菜单能够根据菜单项数量自动调整高度
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                              QWidget, QLabel, QPushButton, QHBoxLayout, 
                              QMenu, QToolButton, QMessageBox)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QIcon

from app.topbar.button_controller import ButtonController
from app.preference.style_utils import create_toolbar_menu_style
from utils.path import get_icon_path

class MockMarkRenderEditor:
    """模拟Markdown编辑器"""
    def export_content(self, format_type):
        print(f"✅ 模拟导出: {format_type}")

class ExportMenuAdaptiveHeightTest(QMainWindow):
    """导出菜单高度自适应测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        QTimer.singleShot(100, self.start_test)
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("🧪 导出菜单高度自适应测试")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("🧪 导出菜单高度自适应测试")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 测试说明
        test_desc = QLabel("""
        🎯 测试目标：
        验证导出菜单高度能够根据菜单项数量自动调整
        
        ✅ 修复前问题：
        • 菜单设置了固定的 min-height: 140px 和 max-height: 200px
        • 即使只有2个菜单项，菜单也会显示140px高度，造成空白区域
        
        🔧 修复方案：
        • 移除固定的 min-height 和 max-height 设置
        • 让Qt自动根据菜单项数量计算最佳高度
        • 保持最小宽度确保菜单美观
        """)
        test_desc.setFont(QFont("Menlo", 11))
        test_desc.setStyleSheet("""
            QLabel {
                background-color: #e8f4fd;
                border: 1px solid #bee5eb;
                border-radius: 4px;
                padding: 15px;
                color: #0c5460;
            }
        """)
        layout.addWidget(test_desc)
        
        # 创建测试区域
        test_container = QWidget()
        test_container.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border: 2px solid #007AFF;
                border-radius: 6px;
                padding: 15px;
            }
        """)
        test_layout = QVBoxLayout(test_container)
        
        # 测试标签
        test_label = QLabel("📋 实际导出菜单测试")
        test_label.setFont(QFont("Arial", 12, QFont.Bold))
        test_layout.addWidget(test_label)
        
        # 创建不同菜单项数量的测试按钮
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        
        # 2个选项的菜单
        self.create_test_menu(button_layout, "2个选项", 2)
        
        # 3个选项的菜单  
        self.create_test_menu(button_layout, "3个选项", 3)
        
        # 4个选项的菜单
        self.create_test_menu(button_layout, "4个选项", 4)
        
        # 6个选项的菜单
        self.create_test_menu(button_layout, "6个选项", 6)
        
        test_layout.addWidget(button_container)
        
        # 创建实际的ButtonController用于对比
        bc_label = QLabel("📋 实际ButtonController导出菜单")
        bc_label.setFont(QFont("Arial", 12, QFont.Bold))
        test_layout.addWidget(bc_label)
        
        # 创建模拟依赖
        self.quickpick_panel = QWidget()
        self.markrender_editor = MockMarkRenderEditor()
        
        # 创建ButtonController
        self.button_controller = ButtonController(self, self.quickpick_panel, self.markrender_editor)
        test_layout.addWidget(self.button_controller)
        
        layout.addWidget(test_container)
        
        # 结果显示区域
        self.result_label = QLabel("点击测试按钮查看效果...")
        self.result_label.setFont(QFont("Menlo", 10))
        self.result_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 15px;
                color: #333;
            }
        """)
        layout.addWidget(self.result_label)
        
    def create_test_menu(self, layout, label, item_count):
        """创建测试菜单按钮"""
        btn = QToolButton()
        btn.setText(label)
        btn.setPopupMode(QToolButton.InstantPopup)
        btn.setIcon(QIcon(get_icon_path('download')))
        
        # 创建菜单
        menu = QMenu(btn)
        menu.setStyleSheet(create_toolbar_menu_style())
        
        # 添加指定数量的菜单项
        formats = ['HTML', 'Markdown', 'PDF', 'EPUB', 'DOCX', 'TXT']
        for i in range(item_count):
            if i < len(formats):
                action = menu.addAction(f'导出 {formats[i]}')
                action.triggered.connect(
                    lambda checked, fmt=formats[i]: self.test_export(fmt, item_count)
                )
        
        btn.setMenu(menu)
        btn.clicked.connect(lambda: self.show_test_result(label, item_count))
        
        # 设置按钮样式
        btn.setStyleSheet("""
            QToolButton {
                background-color: #ffffff;
                border: 1px solid #007AFF;
                border-radius: 4px;
                padding: 8px 12px;
                margin: 2px;
                font-weight: bold;
            }
            QToolButton:hover {
                background-color: #e3f2fd;
            }
        """)
        
        layout.addWidget(btn)
        
    def test_export(self, format_type, item_count):
        """测试导出功能"""
        self.result_label.setText(f"✅ 测试导出成功: {format_type} (来自{item_count}项菜单)")
        
    def show_test_result(self, label, item_count):
        """显示测试结果"""
        self.result_label.setText(f"""
🧪 菜单高度自适应测试结果

📊 当前测试: {label}
📝 菜单项数量: {item_count}个

✅ 验证要点:
• 菜单高度应该根据菜单项数量自动调整
• 菜单不应该有多余的空白区域
• 菜单项之间间距合理，易于点击
• 菜单边框和圆角正常显示

🔍 观察指标:
• 2个选项: 菜单高度最小，紧凑显示
• 3-4个选项: 菜单高度适中  
• 6个选项: 菜单高度最大，但不会超出屏幕

💡 修复效果:
移除固定高度限制后，菜单现在能够：
• 自动计算合适的高度
• 避免不必要的空白区域
• 提供更好的用户体验
        """)
        
    def start_test(self):
        """开始测试"""
        self.result_label.setText("""
🚀 导出菜单高度自适应测试已启动

📋 测试指南:
1. 点击不同的测试按钮，观察菜单高度变化
2. 验证菜单高度是否根据选项数量自动调整
3. 检查是否还有多余的空白区域
4. 对比实际ButtonController的导出菜单效果

✅ 期望结果:
• 2个选项菜单: 紧凑高度，无空白
• 4个选项菜单: 适中高度，布局合理  
• 6个选项菜单: 较大高度，但仍然合理
• 所有菜单都应该美观易用
        """)

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = ExportMenuAdaptiveHeightTest()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()