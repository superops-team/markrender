#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
保存按钮尺寸优化验证脚本
验证编辑对话框中保存按钮的紧凑设计
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

class SaveButtonOptimizationTestWindow(QMainWindow):
    """保存按钮优化测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("✅ 保存按钮尺寸优化验证")
        self.setGeometry(100, 100, 700, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("✅ 保存按钮尺寸优化验证")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 优化说明
        optimization_desc = QLabel("""
        🔧 优化内容：
        进一步减小保存按钮的尺寸，使其更符合对话框的设计规范
        
        ❌ 优化前问题：
        • 按钮高度28px仍然显得过大
        • padding设置过大（12px上下，24px左右）
        • min-height: 36px与setMinimumHeight(28px)冲突
        
        ✅ 优化后效果：
        • 按钮高度降至24px，更加紧凑
        • padding优化为8px上下，12px左右
        • 完全自定义样式，避免样式冲突
        • 保持按钮功能和视觉效果的同时，减少视觉占用
        """)
        optimization_desc.setFont(QFont("Menlo", 11))
        optimization_desc.setStyleSheet("""
            QLabel {
                background-color: #e3f2fd;
                border: 1px solid #bbdefb;
                border-radius: 4px;
                padding: 15px;
                color: #0d47a1;
            }
        """)
        layout.addWidget(optimization_desc)
        
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
        
        # 按钮尺寸对比
        comparison_desc = QLabel("""
        📏 按钮尺寸对比：
        
        原始设计：
        • 高度：44px（过大）
        • padding：12px 24px（过大）
        • min-height：36px（与代码设置冲突）
        
        第一次优化：
        • 高度：28px（BUTTON_HEIGHT_SM）
        • padding：12px 24px（仍然过大）
        • min-height：36px（样式表覆盖代码设置）
        
        最终优化：
        • 高度：24px（更紧凑）
        • padding：8px 12px（减少33%）
        • max-height：24px（强制限制）
        • 完全自定义样式，避免冲突
        """)
        comparison_desc.setFont(QFont("Menlo", 10))
        comparison_desc.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 15px;
                color: #333;
            }
        """)
        layout.addWidget(comparison_desc)
        
        # 验证要点
        verification_desc = QLabel("""
        🔍 验证要点：
        
        1. 保存按钮高度应该明显比之前更小
        2. 按钮文字应该清晰可读
        3. 按钮点击区域足够大，便于操作
        4. 按钮与对话框其他元素比例协调
        5. 悬停和点击效果正常
        6. 按钮样式与设计系统一致
        """)
        verification_desc.setFont(QFont("Menlo", 10))
        verification_desc.setStyleSheet("""
            QLabel {
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 4px;
                padding: 15px;
                color: #856404;
            }
        """)
        layout.addWidget(verification_desc)
        
    def show_edit_dialog(self):
        """显示编辑对话框"""
        try:
            # 创建测试数据
            test_data = {
                'id': 1,
                'title': '保存按钮优化测试',
                'tags': 'UI, 优化, 按钮',
                'page_type': 'markdown',
                'created_at': datetime(2024, 1, 15, 10, 30, 0),
                'updated_at': datetime(2024, 1, 20, 15, 45, 30),
                'file_size': 2048,
                'content_md5': 'a1b2c3d4e5f6g7h8i9j0'
            }
            
            # 创建并显示对话框
            dialog = EditItemDialog(test_data, self)
            
            print("🔍 对话框已打开，请重点关注：")
            print("1. 保存按钮的高度是否比之前更小")
            print("2. 按钮的padding是否更紧凑")
            print("3. 按钮与其他元素的比例是否协调")
            print("4. 按钮是否仍然易于点击和识别")
            
            result = dialog.exec()
            
            if result:
                print("✅ 对话框正常保存并关闭")
                print(f"最终标题: {dialog.get_new_title()}")
                print(f"最终标签: {dialog.get_new_tags()}")
                print("🎉 保存按钮优化验证完成！")
            else:
                print("❌ 对话框被取消")
                
        except Exception as e:
            print(f"❌ 显示对话框失败: {e}")
            import traceback
            traceback.print_exc()

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = SaveButtonOptimizationTestWindow()
    window.show()
    
    print("✅ 保存按钮尺寸优化验证已启动")
    print("🔍 请点击测试按钮查看优化后的按钮尺寸")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()