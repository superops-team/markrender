#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终按钮显示测试脚本
创建一个可运行的测试来验证按钮显示效果
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                              QWidget, QLabel, QPushButton, QHBoxLayout,
                              QToolButton, QMenu, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon

class MockMarkdownEditor:
    """模拟Markdown编辑器"""
    def export_content(self, format_type):
        print(f"✅ 模拟导出: {format_type}")

class ButtonDisplayTestWindow(QMainWindow):
    """按钮显示测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("🧪 最终按钮显示测试")
        self.setGeometry(100, 100, 1000, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("🧪 按钮显示完整性测试")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 测试说明
        test_desc = QLabel("""
        🎯 测试目标：验证修复后的按钮控制器显示效果
        
        ✅ 已完成的修复：
        • 移除了main.py中重复的setFixedHeight设置
        • 导出菜单高度已改为自适应
        
        🔍 本次测试：
        • 模拟实际的ButtonController布局
        • 使用真实的样式常量值
        • 检查按钮是否完整显示
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
        self.create_test_sections(layout)
        
    def create_test_sections(self, layout):
        """创建测试区域"""
        
        # 测试1：模拟当前设置
        current_section = QFrame()
        current_section.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 2px solid #28a745;
                border-radius: 6px;
                padding: 15px;
            }
        """)
        current_layout = QVBoxLayout(current_section)
        
        current_label = QLabel("📋 当前设置测试 (TOOLBAR_HEIGHT=32px, BUTTON_SIZE=24px)")
        current_label.setFont(QFont("Arial", 12, QFont.Bold))
        current_layout.addWidget(current_label)
        
        current_toolbar = self.create_test_toolbar(
            height=32, 
            button_size=24, 
            margins=(6, 0, 6, 0),
            alignment=Qt.AlignRight | Qt.AlignVCenter
        )
        current_layout.addWidget(current_toolbar)
        layout.addWidget(current_section)
        
        # 测试2：优化边距设置
        improved_section = QFrame()
        improved_section.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 2px solid #007AFF;
                border-radius: 6px;
                padding: 15px;
            }
        """)
        improved_layout = QVBoxLayout(improved_section)
        
        improved_label = QLabel("🔧 优化边距测试 (上下边距2px，确保居中)")
        improved_label.setFont(QFont("Arial", 12, QFont.Bold))
        improved_layout.addWidget(improved_label)
        
        improved_toolbar = self.create_test_toolbar(
            height=32, 
            button_size=24, 
            margins=(6, 2, 6, 2),  # 添加上下边距
            alignment=Qt.AlignRight | Qt.AlignVCenter
        )
        improved_layout.addWidget(improved_toolbar)
        layout.addWidget(improved_section)
        
        # 测试3：增加工具栏高度
        larger_section = QFrame()
        larger_section.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 2px solid #ffc107;
                border-radius: 6px;
                padding: 15px;
            }
        """)
        larger_layout = QVBoxLayout(larger_section)
        
        larger_label = QLabel("📏 增加高度测试 (TOOLBAR_HEIGHT=36px)")
        larger_label.setFont(QFont("Arial", 12, QFont.Bold))
        larger_layout.addWidget(larger_label)
        
        larger_toolbar = self.create_test_toolbar(
            height=36, 
            button_size=24, 
            margins=(6, 4, 6, 4),  # 更大的上下边距
            alignment=Qt.AlignRight | Qt.AlignVCenter
        )
        larger_layout.addWidget(larger_toolbar)
        layout.addWidget(larger_section)
        
        # 结果说明
        result_desc = QLabel("""
        🔍 观察要点：
        
        ✅ 正常显示特征：
        • 3个按钮都完整可见
        • 按钮在容器中垂直居中
        • 悬停效果正常工作
        • 导出菜单能正常弹出
        
        ❌ 异常显示特征：
        • 按钮被部分裁切
        • 按钮位置偏上或偏下
        • 悬停效果不正常
        • 容器边界可见但按钮不可见
        
        💡 如果当前设置有问题，建议采用优化边距或增加高度的方案。
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
        
    def create_test_toolbar(self, height, button_size, margins, alignment):
        """创建测试工具栏"""
        toolbar = QWidget()
        toolbar.setFixedHeight(height)
        toolbar.setStyleSheet(f"""
            QWidget {{
                background-color: #ffffff;
                border: 1px solid #dee2e6;
                border-radius: 4px;
            }}
        """)
        
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(*margins)
        layout.setSpacing(2)
        layout.setAlignment(alignment)
        
        # 创建3个测试按钮
        buttons = []
        button_configs = [
            ('sidebar', '历史面板'),
            ('columns', '模式切换'), 
            ('download', '导出')
        ]
        
        for icon_name, tooltip in button_configs:
            if icon_name == 'download':
                # 导出按钮（带菜单）
                btn = QToolButton()
                btn.setPopupMode(QToolButton.InstantPopup)
                
                # 创建菜单
                menu = QMenu(btn)
                menu.setStyleSheet("""
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
                """)
                
                menu.addAction('导出 Markdown')
                menu.addAction('导出 PDF')
                btn.setMenu(menu)
            else:
                btn = QToolButton()
                
            btn.setToolTip(tooltip)
            btn.setFixedSize(button_size, button_size)
            
            # 设置按钮样式
            btn.setStyleSheet(f"""
                QToolButton {{
                    border: 1px solid transparent;
                    border-radius: 4px;
                    background-color: transparent;
                    color: #697077;
                    padding: 0px;
                    margin: 0px;
                }}
                QToolButton:hover {{
                    background-color: #e8f4fd;
                    color: #2591ff;
                    border: 1px solid #a1d2f8;
                }}
                QToolButton:pressed {{
                    background-color: #c3e2fb;
                    color: #1e7ce8;
                    border: 1px solid #7ec0f5;
                }}
                QToolButton::menu-indicator {{
                    image: none;
                    width: 0px;
                    height: 0px;
                }}
                QToolButton::menu-button {{
                    border: none;
                    background-color: transparent;
                    width: 0px;
                    height: 0px;
                }}
            """)
            
            # 添加点击事件
            btn.clicked.connect(lambda checked, name=tooltip: print(f"✅ 点击了: {name}"))
            
            layout.addWidget(btn)
            buttons.append(btn)
        
        return toolbar

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = ButtonDisplayTestWindow()
    window.show()
    
    print("🧪 按钮显示测试已启动")
    print("🔍 请观察三个测试区域中的按钮显示效果")
    print("💡 如果当前设置区域的按钮显示有问题，可以参考其他区域的设置")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()