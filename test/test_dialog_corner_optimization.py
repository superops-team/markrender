#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对话框圆角协调性验证脚本
验证编辑对话框内部布局圆角优化效果
"""

import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

try:
    from app.quickpick.edit_dialog import EditItemDialog
    HAS_MODULES = True
except ImportError as e:
    print(f"⚠️  模块导入失败: {e}")
    HAS_MODULES = False

class DialogCornerOptimizationTestWindow(QMainWindow):
    """对话框圆角优化测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("✅ 对话框圆角协调性验证")
        self.setGeometry(100, 100, 700, 550)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("✅ 对话框圆角协调性验证")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 问题描述
        problem_desc = QLabel("""
        🎯 用户反馈问题：
        "弹出的对话框layout的布局有一个非常小的圆角在对话框内部能够看到，整体不是很协调"
        
        🔍 问题分析：
        • 对话框本身使用了大圆角（RADIUS_LG = 12px）
        • 标签容器使用了中等圆角（RADIUS_MD = 8px）
        • 在已有圆角的对话框内部又出现圆角容器，造成视觉层次混乱
        • 多层圆角嵌套破坏了整体的设计协调性
        """)
        problem_desc.setFont(QFont("Menlo", 11))
        problem_desc.setStyleSheet("""
            QLabel {
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 4px;
                padding: 15px;
                color: #856404;
            }
        """)
        layout.addWidget(problem_desc)
        
        # 优化方案
        solution_desc = QLabel("""
        🔧 优化方案：
        
        1. 主内容区域样式重置：
           • 明确设置 background-color: transparent
           • 设置 border: none 和 border-radius: 0px
           • 确保主内容区域不产生视觉干扰
        
        2. 标签容器圆角移除：
           • 将 border-radius 从 8px 改为 0px
           • 保留边框和背景色，维持容器边界
           • 避免与对话框圆角产生视觉冲突
        
        3. 设计原则遵循：
           • 外层容器使用圆角，内层容器使用直角
           • 保持视觉层次清晰简洁
           • 避免过度装饰，专注内容展示
        """)
        solution_desc.setFont(QFont("Menlo", 11))
        solution_desc.setStyleSheet("""
            QLabel {
                background-color: #e8f5e8;
                border: 1px solid #c3e6cb;
                border-radius: 4px;
                padding: 15px;
                color: #155724;
            }
        """)
        layout.addWidget(solution_desc)
        
        if HAS_MODULES:
            # 测试按钮
            test_btn = QPushButton("🧪 测试编辑对话框")
            test_btn.clicked.connect(self.show_edit_dialog)
            test_btn.setStyleSheet("""
                QPushButton {
                    background-color: #007bff;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 12px 24px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
            """)
            layout.addWidget(test_btn)
        
        # 验证要点
        verification_desc = QLabel("""
        🔍 验证要点：
        
        ✅ 视觉协调性检查：
        • 对话框整体应该只有外边框的圆角
        • 内部容器应该使用直角边框，不产生视觉冲突
        • 标签容器边框清晰但不突兀
        
        ✅ 层次结构检查：
        • 主内容区域背景透明，无多余装饰
        • 标签容器有明确的区域划分但不过度装饰
        • 整体布局简洁统一，专注内容展示
        
        ✅ 用户体验检查：
        • 对话框打开时视觉舒适，无突兀感
        • 内容区域层次清晰，易于阅读
        • 整体设计协调，符合现代UI设计原则
        """)
        verification_desc.setFont(QFont("Menlo", 10))
        verification_desc.setStyleSheet("""
            QLabel {
                background-color: #e3f2fd;
                border: 1px solid #bbdefb;
                border-radius: 4px;
                padding: 15px;
                color: #0d47a1;
            }
        """)
        layout.addWidget(verification_desc)
        
    def show_edit_dialog(self):
        """显示编辑对话框"""
        try:
            # 创建测试数据
            test_data = {
                'id': 1,
                'title': '圆角协调性优化测试',
                'tags': 'UI设计, 圆角, 协调性, 优化',
                'page_type': 'markdown',
                'created_at': datetime(2024, 1, 15, 10, 30, 0),
                'updated_at': datetime(2024, 1, 20, 15, 45, 30),
                'file_size': 2048,
                'content_md5': 'a1b2c3d4e5f6g7h8i9j0'
            }
            
            # 创建并显示对话框
            dialog = EditItemDialog(test_data, self)
            
            print("🔍 对话框已打开，请重点观察：")
            print("1. 对话框内部是否还有多余的小圆角")
            print("2. 标签容器是否使用了直角边框")
            print("3. 整体视觉效果是否更加协调")
            print("4. 主内容区域是否背景透明，无视觉干扰")
            print("5. 布局层次是否清晰简洁")
            
            result = dialog.exec()
            
            if result:
                print("✅ 对话框正常保存并关闭")
                print(f"最终标题: {dialog.get_new_title()}")
                print(f"最终标签: {dialog.get_new_tags()}")
                print("🎉 圆角协调性优化验证完成！")
            else:
                print("❌ 对话框被取消")
                
        except Exception as e:
            print(f"❌ 显示对话框失败: {e}")
            import traceback
            traceback.print_exc()

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = DialogCornerOptimizationTestWindow()
    window.show()
    
    print("✅ 对话框圆角协调性验证已启动")
    print("🔍 请点击测试按钮查看优化后的视觉效果")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()