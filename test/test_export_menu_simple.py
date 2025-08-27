#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导出菜单高度自适应测试脚本（简化版）
验证修复后的导出菜单能够根据菜单项数量自动调整高度
"""

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                              QWidget, QLabel, QPushButton, QHBoxLayout, 
                              QMenu, QToolButton, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class ExportMenuAdaptiveHeightTestSimple(QMainWindow):
    """导出菜单高度自适应测试窗口（简化版）"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("🧪 导出菜单高度自适应测试（简化版）")
        self.setGeometry(100, 100, 900, 700)
        
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
        🎯 测试目标：验证导出菜单高度能够根据菜单项数量自动调整
        
        ✅ 修复前问题：
        • 菜单设置了固定的 min-height: 140px 和 max-height: 200px
        • 即使只有2个菜单项，菜单也会显示140px高度，造成空白区域
        
        🔧 修复方案：
        • 移除固定的 min-height 和 max-height 设置
        • 让Qt自动根据菜单项数量计算最佳高度
        
        📋 测试方法：
        点击下方不同的测试按钮，观察菜单高度是否根据选项数量自动调整
        """)
        test_desc.setFont(QFont("Menlo", 11))
        test_desc.setStyleSheet("""
            QLabel {
                background-color: #e8f4fd;
                border: 1px solid #bee5eb;
                border-radius: 6px;
                padding: 15px;
                color: #0c5460;
            }
        """)
        layout.addWidget(test_desc)
        
        # 创建测试区域
        test_frame = QFrame()
        test_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 2px solid #007AFF;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        test_layout = QVBoxLayout(test_frame)
        
        # 测试标签
        test_label = QLabel("📋 菜单高度自适应测试")
        test_label.setFont(QFont("Arial", 13, QFont.Bold))
        test_layout.addWidget(test_label)
        
        # 创建不同菜单项数量的测试按钮
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        
        # 自适应高度菜单样式（修复后）
        adaptive_style = """
        QMenu {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            padding: 8px;
            min-width: 140px;
        }
        QMenu::item {
            color: #333333;
            padding: 10px 14px;
            margin: 2px;
            border-radius: 4px;
            font-size: 13px;
            min-height: 24px;
        }
        QMenu::item:selected {
            background-color: #e3f2fd;
            color: #1976d2;
        }
        QMenu::item:pressed {
            background-color: #bbdefb;
        }
        """
        
        # 固定高度菜单样式（修复前）
        fixed_style = """
        QMenu {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            padding: 8px;
            min-width: 140px;
            min-height: 140px;
            max-height: 200px;
        }
        QMenu::item {
            color: #333333;
            padding: 10px 14px;
            margin: 2px;
            border-radius: 4px;
            font-size: 13px;
            min-height: 24px;
        }
        QMenu::item:selected {
            background-color: #e3f2fd;
            color: #1976d2;
        }
        QMenu::item:pressed {
            background-color: #bbdefb;
        }
        """
        
        # 创建对比测试
        self.create_comparison_section(test_layout, "修复后（自适应高度）", adaptive_style, True)
        self.create_comparison_section(test_layout, "修复前（固定高度）", fixed_style, False)
        
        layout.addWidget(test_frame)
        
        # 结果说明
        result_desc = QLabel("""
        🔍 观察要点：
        
        ✅ 修复后（自适应高度）:
        • 2个选项: 菜单高度紧凑，无多余空白
        • 3个选项: 菜单高度适中
        • 4个选项: 菜单高度合理增加
        • 6个选项: 菜单高度达到合适大小
        
        ❌ 修复前（固定高度）:
        • 所有菜单都是140px固定高度
        • 2个选项菜单有大量空白区域
        • 浪费屏幕空间，用户体验差
        
        💡 修复效果：
        移除固定高度限制，菜单现在能够根据内容自动调整大小，
        提供更好的用户体验和更合理的空间利用。
        """)
        result_desc.setFont(QFont("Menlo", 10))
        result_desc.setStyleSheet("""
            QLabel {
                background-color: #d4edda;
                border: 1px solid #c3e6cb;
                border-radius: 6px;
                padding: 15px;
                color: #155724;
            }
        """)
        layout.addWidget(result_desc)
        
    def create_comparison_section(self, layout, title, menu_style, is_adaptive):
        """创建对比测试区域"""
        section_label = QLabel(f"📊 {title}")
        section_label.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(section_label)
        
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        
        # 创建不同菜单项数量的测试按钮
        test_configs = [
            ("2个选项", 2, ["HTML", "PDF"]),
            ("3个选项", 3, ["HTML", "PDF", "Markdown"]),
            ("4个选项", 4, ["HTML", "PDF", "Markdown", "EPUB"]),
            ("6个选项", 6, ["HTML", "PDF", "Markdown", "EPUB", "DOCX", "TXT"])
        ]
        
        for label, count, formats in test_configs:
            btn = self.create_test_menu_button(label, formats, menu_style, is_adaptive)
            button_layout.addWidget(btn)
        
        layout.addWidget(button_container)
        
        # 添加间距
        spacer = QWidget()
        spacer.setFixedHeight(10)
        layout.addWidget(spacer)
        
    def create_test_menu_button(self, label, formats, menu_style, is_adaptive):
        """创建测试菜单按钮"""
        btn = QToolButton()
        btn.setText(label)
        btn.setPopupMode(QToolButton.InstantPopup)
        
        # 创建菜单
        menu = QMenu(btn)
        menu.setStyleSheet(menu_style)
        
        # 添加菜单项
        for fmt in formats:
            action = menu.addAction(f'导出 {fmt}')
            action.triggered.connect(
                lambda checked, f=fmt, adaptive=is_adaptive: 
                self.on_export_action(f, adaptive, len(formats))
            )
        
        btn.setMenu(menu)
        
        # 设置按钮样式
        color = "#28a745" if is_adaptive else "#dc3545"
        btn.setStyleSheet(f"""
            QToolButton {{
                background-color: #ffffff;
                border: 2px solid {color};
                border-radius: 6px;
                padding: 8px 12px;
                margin: 4px;
                font-weight: bold;
                color: {color};
                min-width: 80px;
            }}
            QToolButton:hover {{
                background-color: {color};
                color: white;
            }}
        """)
        
        return btn
        
    def on_export_action(self, format_type, is_adaptive, item_count):
        """处理导出动作"""
        adaptive_text = "自适应高度" if is_adaptive else "固定高度"
        print(f"✅ 测试导出: {format_type} (菜单类型: {adaptive_text}, 菜单项数: {item_count})")

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = ExportMenuAdaptiveHeightTestSimple()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()