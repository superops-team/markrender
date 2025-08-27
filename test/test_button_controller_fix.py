#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
右上角按钮控制器显示修复验证测试

此测试验证以下问题的修复：
1. 主窗口右上角小按钮优化后无法展示的问题
2. 标题栏高度与按钮控制器高度不匹配导致的显示问题
3. 按钮控制器的布局和功能是否正常

修复内容：
- 修复了main.py中button_controller的高度设置冲突（20px -> 36px）
- 调整了title_bar的高度以适应36px的按钮控制器（30px -> 44px）
- 优化了标题栏的内边距配置
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import QTimer, Qt

from main import MainWindow


class ButtonControllerTestWindow(QMainWindow):
    """按钮控制器测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("右上角按钮控制器显示修复测试")
        self.setGeometry(100, 100, 400, 300)
        
        # 创建中央组件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 添加测试指导按钮
        test_btn = QPushButton("🔧 启动主窗口测试")
        test_btn.clicked.connect(self.launch_main_window)
        test_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        layout.addWidget(test_btn)
        
        # 添加测试指导按钮
        guide_btn = QPushButton("📋 显示测试指导")
        guide_btn.clicked.connect(self.show_test_guide)
        guide_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #1e7e34;
            }
        """)
        layout.addWidget(guide_btn)
        
    def launch_main_window(self):
        """启动主窗口进行测试"""
        try:
            self.main_window = MainWindow()
            self.main_window.show()
            print("✅ 主窗口已启动，请检查右上角按钮控制器")
            
            # 延迟显示测试要点
            QTimer.singleShot(1000, self.show_button_test_info)
            
        except Exception as e:
            print(f"❌ 启动主窗口失败: {e}")
            
    def show_button_test_info(self):
        """显示按钮测试信息"""
        print("\n🔍 按钮控制器验证要点:")
        print("1. 检查右上角是否显示3个小按钮（sidebar、columns、download图标）")
        print("2. 按钮尺寸应该是28×28px，间距为4px")
        print("3. 悬停时应该有高亮效果（蓝色背景）")
        print("4. 点击导出按钮应该显示下拉菜单")
        print("5. 标题栏高度应该足够容纳按钮（44px）")
        
    def show_test_guide(self):
        """显示测试指导"""
        from PySide6.QtWidgets import QMessageBox
        
        msg = QMessageBox(self)
        msg.setWindowTitle("测试指导")
        msg.setIcon(QMessageBox.Information)
        msg.setText("右上角按钮控制器显示修复验证")
        msg.setInformativeText("""
🎯 测试目标：
验证右上角按钮控制器在样式优化后能正常显示和工作

❌ 问题原因：
• main.py中button_controller高度被错误设置为20px
• ButtonController内部设计高度为36px，造成冲突
• title_bar高度30px无法容纳36px的按钮控制器

✅ 修复方案：
• 将main.py中button_controller高度修改为36px
• 调整title_bar高度从30px增加到44px  
• 优化title_bar内边距以正确对齐

📋 验证步骤：
1. 点击"启动主窗口测试"按钮
2. 观察主窗口右上角是否显示按钮控制器
3. 检查按钮间距、对齐和交互效果
4. 测试导出菜单功能

🔧 修复效果：
• 按钮控制器现在应该完全可见
• 3个工具按钮（侧边栏、模式切换、导出）正常显示
• 悬停和点击交互正常工作
• 与整体UI风格保持一致
        """)
        msg.exec()


def main():
    """主函数"""
    print("🚀 启动右上角按钮控制器显示修复验证测试...")
    
    app = QApplication(sys.argv)
    app.setApplicationName("ButtonControllerTest")
    
    # 创建测试窗口
    window = ButtonControllerTestWindow()
    window.show()
    
    print("✨ 测试窗口已启动")
    print("📌 请点击按钮启动主窗口测试")
    print("🔍 验证右上角按钮控制器是否正常显示")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()