#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建按钮下拉菜单修复验证测试

此测试验证以下问题的修复：
1. 创建按钮下拉菜单不符合设计规范
2. 创建按钮下拉菜单透明无法查看
3. 只有鼠标hover后才能看到子按钮

修复内容：
- 修复菜单样式中 QMenu::item 的 color: transparent 问题
- 优化菜单布局，增加图标和文本标签
- 改进交互体验和视觉设计
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

from app.quickpick.panel import QuickPickPanel
from db.markrender_manager import MarkRenderManager
from utils.path import get_icon_path


class CreateMenuTestWindow(QMainWindow):
    """创建菜单测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("创建按钮下拉菜单修复测试")
        self.setGeometry(100, 100, 400, 600)
        
        # 创建中央组件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 创建说明文本
        info_widget = QWidget()
        info_widget.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 20px;
            }
        """)
        
        # 创建MarkRenderManager实例
        try:
            self.markdown_manager = MarkRenderManager()
        except Exception as e:
            print(f"创建MarkRenderManager失败: {e}")
            self.markdown_manager = None
        
        # 创建QuickPickPanel实例
        if self.markdown_manager:
            self.quickpick_panel = QuickPickPanel(self.markdown_manager, self)
            layout.addWidget(self.quickpick_panel)
        
        # 添加测试指导
        test_btn = QPushButton("📝 测试指导")
        test_btn.clicked.connect(self.show_test_guide)
        test_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        layout.addWidget(test_btn)
        
    def show_test_guide(self):
        """显示测试指导"""
        from PySide6.QtWidgets import QMessageBox
        
        msg = QMessageBox(self)
        msg.setWindowTitle("测试指导")
        msg.setIcon(QMessageBox.Information)
        msg.setText("创建按钮下拉菜单修复验证")
        msg.setInformativeText("""
🎯 测试目标：
验证创建按钮下拉菜单的修复效果

✅ 测试步骤：
1. 点击右上角的创建按钮（铅笔图标）
2. 观察下拉菜单是否正常显示
3. 检查菜单项是否可见（不透明）
4. 测试悬停和点击效果

📋 验证要点：
• 菜单背景：白色背景，清晰边框
• 菜单项：图标+文本标签，清晰可见
• 交互效果：悬停有高亮反馈
• 功能正常：点击能创建对应类型的文档

🔧 修复内容：
• 修复了 QMenu::item 的透明度问题
• 优化了菜单布局和视觉设计
• 改进了交互体验和可访问性
        """)
        msg.exec()


def main():
    """主函数"""
    print("🚀 启动创建按钮下拉菜单修复验证测试...")
    
    app = QApplication(sys.argv)
    app.setApplicationName("CreateMenuTest")
    
    # 创建测试窗口
    window = CreateMenuTestWindow()
    window.show()
    
    print("✨ 测试窗口已启动")
    print("📌 请点击界面中的创建按钮测试下拉菜单功能")
    print("🔍 检查菜单是否可见且符合设计规范")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()