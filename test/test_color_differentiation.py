#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标签和按钮颜色差异化验证脚本
验证tag、page_type和保存按钮的颜色区分效果
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

class ColorDifferentiationTestWindow(QMainWindow):
    """颜色差异化测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("✅ 标签和按钮颜色差异化验证")
        self.setGeometry(100, 100, 800, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("✅ 标签和按钮颜色差异化验证")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 问题描述
        problem_desc = QLabel("""
        🎨 用户反馈问题：
        "添加tag后tag的颜色和保存设置的按钮的颜色一样，还有page_type的样式的颜色也和保存按钮的颜色一样"
        
        📊 原始设计问题：
        • 用户添加的Tag使用PRIMARY_500蓝色
        • Page_type标签使用PRIMARY_500蓝色  
        • 保存按钮使用PRIMARY_500蓝色
        • 三种不同功能的组件使用相同颜色，缺乏视觉层次
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
        
        # 颜色方案优化
        color_scheme = QLabel("""
        🎨 优化后的颜色方案：
        
        🔵 保存按钮（主要操作）：
        • 保持使用PRIMARY_500 (#259DF0) 蓝色系
        • 作为主要操作按钮，应该保持最高的视觉优先级
        
        🟢 用户添加的Tag（用户内容）：
        • 优化为SUCCESS_500 (#22C55E) 绿色系
        • 边框使用SUCCESS_600 (#16A34A) 深绿色
        • 表示用户创建的标签内容，与系统信息区分
        
        🟠 Page_type标签（系统信息）：
        • 优化为WARNING_500 (#F59E0B) 橙色系
        • 边框使用WARNING_600 (#D97706) 深橙色
        • 表示文件类型等系统属性信息，使用大写显示
        
        ✨ 设计原则：
        • 蓝色：主要操作，最高优先级
        • 绿色：用户内容，次要但重要
        • 橙色：系统信息，辅助说明
        """)
        color_scheme.setFont(QFont("Menlo", 10))
        color_scheme.setStyleSheet("""
            QLabel {
                background-color: #e3f2fd;
                border: 1px solid #bbdefb;
                border-radius: 4px;
                padding: 15px;
                color: #0d47a1;
            }
        """)
        layout.addWidget(color_scheme)
        
        if HAS_MODULES:
            # 测试按钮
            test_btn = QPushButton("🧪 测试颜色差异化效果")
            test_btn.clicked.connect(self.show_edit_dialog)
            test_btn.setStyleSheet("""
                QPushButton {
                    background-color: #6f42c1;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 12px 24px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #5a32a3;
                }
            """)
            layout.addWidget(test_btn)
        
        # 验证要点
        verification_desc = QLabel("""
        🔍 验证要点 - 请重点观察以下颜色区分：
        
        📝 标签编辑区域：
        ☐ 用户添加的标签应该显示为绿色背景
        ☐ 标签删除按钮应该是白色半透明覆盖
        ☐ 多个标签的颜色应该保持一致
        
        📋 文件属性区域：
        ☐ "文件类型"标签应该显示为橙色背景
        ☐ 文件类型文字应该是大写字母（如MARKDOWN）
        ☐ 橙色应该明显区别于绿色和蓝色
        
        💾 保存按钮区域：
        ☐ 保存按钮应该保持蓝色背景
        ☐ 蓝色应该是三种颜色中最突出的
        ☐ 按钮高度应该保持紧凑（24px）
        
        🎨 整体视觉效果：
        ☐ 三种颜色应该形成清晰的视觉层次
        ☐ 蓝色（操作）> 绿色（内容）> 橙色（信息）
        ☐ 颜色搭配应该和谐，不产生视觉冲突
        ☐ 符合无障碍设计，对比度足够
        """)
        verification_desc.setFont(QFont("Menlo", 10))
        verification_desc.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 15px;
                color: #333;
            }
        """)
        layout.addWidget(verification_desc)
        
    def show_edit_dialog(self):
        """显示编辑对话框"""
        try:
            # 创建测试数据，包含多个标签用于验证颜色效果
            test_data = {
                'id': 1,
                'title': '颜色差异化测试文档',
                'tags': 'Python, Qt, UI设计, 颜色测试, 用户体验',  # 多个标签
                'page_type': 'markdown',
                'created_at': datetime(2024, 1, 15, 10, 30, 0),
                'updated_at': datetime(2024, 1, 20, 15, 45, 30),
                'file_size': 2048,
                'content_md5': 'a1b2c3d4e5f6g7h8i9j0'
            }
            
            # 创建并显示对话框
            dialog = EditItemDialog(test_data, self)
            
            print("🔍 对话框已打开，请重点观察颜色差异：")
            print("")
            print("🟢 绿色标签：")
            print("   - 应该看到多个绿色的用户标签")
            print("   - 绿色应该表示用户添加的内容")
            print("")
            print("🟠 橙色文件类型：")
            print("   - 'MARKDOWN'应该显示为橙色标签")
            print("   - 橙色应该表示系统属性信息")
            print("")
            print("🔵 蓝色保存按钮：")
            print("   - 保存按钮应该保持蓝色")
            print("   - 蓝色应该是最突出的颜色")
            print("")
            print("✨ 整体效果：")
            print("   - 三种颜色应该清晰区分，形成视觉层次")
            print("   - 可以尝试添加新标签，观察绿色效果")
            
            result = dialog.exec()
            
            if result:
                print("✅ 对话框正常保存并关闭")
                print(f"最终标题: {dialog.get_new_title()}")
                print(f"最终标签: {dialog.get_new_tags()}")
                print("🎉 颜色差异化验证完成！")
                print("")
                print("📝 请确认颜色区分效果：")
                print("   - 绿色标签（用户内容）")
                print("   - 橙色文件类型（系统信息）") 
                print("   - 蓝色保存按钮（主要操作）")
            else:
                print("❌ 对话框被取消")
                print("💡 请确认取消前是否观察到颜色差异化效果")
                
        except Exception as e:
            print(f"❌ 显示对话框失败: {e}")
            import traceback
            traceback.print_exc()

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = ColorDifferentiationTestWindow()
    window.show()
    
    print("✅ 标签和按钮颜色差异化验证已启动")
    print("🎨 请点击测试按钮，观察三种组件的颜色区分效果")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()