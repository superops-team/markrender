#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QuickPick编辑对话框优化验证脚本
验证移除Tab容器后的单页面编辑对话框
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

class EditDialogTestWindow(QMainWindow):
    """编辑对话框测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("✅ QuickPick编辑对话框优化验证")
        self.setGeometry(100, 100, 600, 400)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("✅ QuickPick编辑对话框优化验证")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 优化说明
        optimization_desc = QLabel("""
        🔧 优化内容：
        移除了多Tab页面设计，改为单页面直接展示所有内容
        
        ❌ 优化前问题：
        • 使用QTabWidget容器，但只有一个Tab页面
        • 界面设计冗余，用户体验不佳
        • Tab标签占用不必要的空间
        
        ✅ 优化后效果：
        • 移除Tab容器，直接展示内容
        • 编辑信息和文件属性在同一页面
        • 使用分隔线区分不同区域
        • 界面更加简洁，操作更加直观
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
        
        # 验证要点
        verification_desc = QLabel("""
        🔍 验证要点：
        
        1. 对话框应该只有一个页面，没有Tab标签
        2. 编辑信息区域在上方（标题、标签输入）
        3. 文件属性区域在下方（文件类型、时间、大小等）
        4. 两个区域之间应该有分隔线
        5. 所有功能都能正常使用
        6. 界面布局简洁美观
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
            # 创建测试数据
            test_data = {
                'id': 1,
                'title': '测试文档标题',
                'tags': 'Python, Qt, GUI',
                'page_type': 'markdown',
                'created_at': datetime(2024, 1, 15, 10, 30, 0),
                'updated_at': datetime(2024, 1, 20, 15, 45, 30),
                'file_size': 2048,
                'content_md5': 'a1b2c3d4e5f6g7h8i9j0'
            }
            
            # 创建并显示对话框
            dialog = EditItemDialog(test_data, self)
            result = dialog.exec()
            
            if result:
                print("✅ 对话框保存成功")
                print(f"新标题: {dialog.get_new_title()}")
                print(f"新标签: {dialog.get_new_tags()}")
            else:
                print("❌ 对话框取消")
                
        except Exception as e:
            print(f"❌ 显示对话框失败: {e}")
            import traceback
            traceback.print_exc()

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = EditDialogTestWindow()
    window.show()
    
    print("✅ QuickPick编辑对话框优化验证已启动")
    print("🔍 请点击测试按钮查看优化后的对话框")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()