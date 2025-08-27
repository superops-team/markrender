#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编辑对话框修复验证脚本
验证Tag输入和保存按钮的修复效果
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

class EditDialogFixTestWindow(QMainWindow):
    """编辑对话框修复测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("✅ 编辑对话框修复验证")
        self.setGeometry(100, 100, 700, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("✅ 编辑对话框修复验证")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 修复说明
        fix_desc = QLabel("""
        🔧 修复内容：
        
        1. Tag输入导致对话框退出问题：
           ❌ 问题：首次输入tag时按回车会意外关闭对话框
           ✅ 修复：设置保存按钮的autoDefault=False，防止回车键触发保存
           ✅ 优化：增强tag输入错误处理和用户反馈
        
        2. 保存按钮过大问题：
           ❌ 问题：按钮高度44px过大，不符合设计规范
           ✅ 修复：调整为36px，符合统一的按钮高度规范
        
        🎯 验证要点：
        • Tag输入框中按回车只会添加标签，不会关闭对话框
        • 重复标签会显示提示信息
        • 保存按钮高度适中，符合设计规范
        • 对话框只能通过点击保存按钮或ESC键关闭
        """)
        fix_desc.setFont(QFont("Menlo", 11))
        fix_desc.setStyleSheet("""
            QLabel {
                background-color: #e8f5e8;
                border: 1px solid #c3e6cb;
                border-radius: 4px;
                padding: 15px;
                color: #155724;
            }
        """)
        layout.addWidget(fix_desc)
        
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
        
        # 测试指南
        test_guide = QLabel("""
        📋 测试步骤：
        
        1. 点击上方按钮打开编辑对话框
        2. 在"标签"输入框中输入一个标签名称，然后按回车
        3. 验证：标签应该被添加，对话框不应该关闭
        4. 尝试输入相同的标签名称并按回车
        5. 验证：应该显示"标签已存在"的提示
        6. 输入多个不同的标签，验证都能正常添加
        7. 检查保存按钮的大小是否合适（不会显得过大）
        8. 最后点击保存按钮关闭对话框
        
        ✅ 预期结果：
        • 所有tag输入操作都不会意外关闭对话框
        • 标签重复时会有友好的提示信息
        • 保存按钮大小适中，符合设计规范
        """)
        test_guide.setFont(QFont("Menlo", 10))
        test_guide.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 15px;
                color: #333;
            }
        """)
        layout.addWidget(test_guide)
        
    def show_edit_dialog(self):
        """显示编辑对话框"""
        try:
            # 创建测试数据
            test_data = {
                'id': 1,
                'title': '测试文档 - 修复验证',
                'tags': 'Python, Qt',  # 预设一些标签用于测试重复标签功能
                'page_type': 'markdown',
                'created_at': datetime(2024, 1, 15, 10, 30, 0),
                'updated_at': datetime(2024, 1, 20, 15, 45, 30),
                'file_size': 2048,
                'content_md5': 'a1b2c3d4e5f6g7h8i9j0'
            }
            
            # 创建并显示对话框
            dialog = EditItemDialog(test_data, self)
            
            print("🔍 对话框已打开，请进行以下测试：")
            print("1. 在标签输入框中输入新标签并按回车")
            print("2. 尝试输入重复标签（如'Python'或'Qt'）")
            print("3. 检查保存按钮的大小是否合适")
            print("4. 验证只有点击保存按钮才能关闭对话框")
            
            result = dialog.exec()
            
            if result:
                print("✅ 对话框正常保存并关闭")
                print(f"最终标题: {dialog.get_new_title()}")
                print(f"最终标签: {dialog.get_new_tags()}")
                print("🎉 修复验证完成！")
            else:
                print("❌ 对话框被取消")
                
        except Exception as e:
            print(f"❌ 显示对话框失败: {e}")
            import traceback
            traceback.print_exc()

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = EditDialogFixTestWindow()
    window.show()
    
    print("✅ 编辑对话框修复验证已启动")
    print("🔍 请点击测试按钮验证修复效果")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()