#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TopBar按钮对齐和菜单功能验证测试

此测试验证以下修复内容：
1. TopBar按钮的完美垂直居中对齐
2. hover状态下的对齐保持
3. 下拉菜单的正常显示和功能
4. 菜单样式的优化效果
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import QTimer, Qt

from main import MainWindow


class TopBarAlignmentTestWindow(QMainWindow):
    """TopBar对齐和菜单测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("TopBar按钮对齐和菜单功能验证测试")
        self.setGeometry(100, 100, 500, 400)
        
        # 创建中央组件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 启动主窗口测试按钮
        launch_btn = QPushButton("🚀 启动主窗口测试")
        launch_btn.clicked.connect(self.launch_main_window)
        launch_btn.setStyleSheet("""
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
        layout.addWidget(launch_btn)
        
        # 显示测试指导按钮
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
            print("✅ 主窗口已启动，请进行TopBar测试")
            
            # 延迟显示测试要点
            QTimer.singleShot(1000, self.show_test_points)
            
        except Exception as e:
            print(f"❌ 启动主窗口失败: {e}")
            
    def show_test_points(self):
        """显示测试要点"""
        print("\n🔍 TopBar按钮对齐和菜单功能验证要点:")
        print("=" * 50)
        
        print("📐 按钮对齐验证:")
        print("  1. 检查3个按钮（sidebar、columns、download）是否垂直居中")
        print("  2. 按钮尺寸应为24×24px（包含1px透明边框）")
        print("  3. 按钮间距应为2px")
        print("  4. 上下空间应各为3px")
        
        print("\n🎨 hover状态验证:")
        print("  1. 悬停时按钮应有蓝色背景和边框")
        print("  2. 悬停时按钮位置不应发生跳动")
        print("  3. 按钮应保持完美的垂直居中")
        
        print("\n📋 下拉菜单验证:")
        print("  1. 点击下载按钮应显示下拉菜单")
        print("  2. 菜单应包含：HTML、Markdown、PDF、EPUB选项")
        print("  3. 菜单应有紧凑的样式（减小尺寸和内边距）")
        print("  4. 菜单项悬停应有高亮效果")
        
        print("\n✨ 设计规范验证:")
        print("  - 符合TopBar设计规范记忆要求")
        print("  - 按钮垂直居中对齐")
        print("  - 固定高度确保一致性")
        print("  - 模块化样式系统")
        print("  - 符合苹果设计规范")
        
        print("\n💡 测试技巧:")
        print("  - 多次悬停按钮观察对齐稳定性")
        print("  - 尝试快速点击下载按钮测试菜单响应")
        print("  - 观察菜单的尺寸和间距是否紧凑合理")
        
    def show_test_guide(self):
        """显示测试指导"""
        from PySide6.QtWidgets import QMessageBox
        
        msg = QMessageBox(self)
        msg.setWindowTitle("测试指导")
        msg.setIcon(QMessageBox.Information)
        msg.setText("TopBar按钮对齐和菜单功能验证")
        msg.setInformativeText("""
🎯 测试目标：
验证TopBar按钮对齐修复和菜单功能恢复效果

❌ 原始问题：
• TopBar按钮没有完美居中
• hover后按钮位置不稳定，上下对齐异常
• 点击下载按钮时下拉菜单不显示
• 下拉菜单样式未优化

✅ 修复方案：
• 调整布局边距：上下边距设为0px，让按钮占满容器高度
• 修复菜单模式：从InstantPopup改为MenuButtonPopup
• 优化按钮样式：使用透明边框避免hover时位置跳动
• 优化菜单样式：减小尺寸和内边距，符合设计规范

📋 验证步骤：
1. 点击"启动主窗口测试"
2. 观察右上角3个按钮的垂直对齐
3. 悬停按钮测试对齐稳定性
4. 点击下载按钮测试菜单显示
5. 检查菜单样式和交互效果

🔧 技术改进：
• 布局边距优化：setContentsMargins(6, 0, 6, 0)
• 菜单模式修复：MenuButtonPopup替代InstantPopup
• 边框一致性：所有状态使用1px边框（透明/可见）
• 菜单尺寸优化：min-width: 80px，padding减少

🎨 设计标准：
• 符合TopBar设计规范记忆
• 完美的垂直居中对齐
• 统一的设计令牌系统
• 紧凑的菜单设计
        """)
        msg.exec()


def main():
    """主函数"""
    print("🚀 启动TopBar按钮对齐和菜单功能验证测试...")
    
    app = QApplication(sys.argv)
    app.setApplicationName("TopBarAlignmentTest")
    
    # 创建测试窗口
    window = TopBarAlignmentTestWindow()
    window.show()
    
    print("✨ 测试窗口已启动")
    print("📌 请点击按钮启动主窗口进行测试")
    print("🔍 验证TopBar按钮对齐和菜单功能")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()