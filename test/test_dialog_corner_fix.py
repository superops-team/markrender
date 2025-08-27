#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对话框圆角问题修复验证脚本
专门验证截图中显示的内部容器圆角问题是否解决
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

class DialogCornerFixTestWindow(QMainWindow):
    """对话框圆角问题修复测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("✅ 对话框圆角问题修复验证")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("✅ 对话框圆角问题修复验证")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 问题确认
        problem_confirm = QLabel("""
        📸 根据用户截图反馈：
        • 在弹出对话框的左上角关闭按钮下方可以看到内部容器的圆角
        • 这些小圆角在对话框内部挨着四个角，影响视觉协调性
        • 用户期望对话框内部应该是平整的，不应该有多余的圆角装饰
        """)
        problem_confirm.setFont(QFont("Menlo", 11))
        problem_confirm.setStyleSheet("""
            QLabel {
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 4px;
                padding: 15px;
                color: #856404;
            }
        """)
        layout.addWidget(problem_confirm)
        
        # 根本原因分析
        root_cause = QLabel("""
        🔍 根本原因分析：
        
        1. QTabWidget样式残留：
           • create_dialog_style()函数中包含QTabWidget::pane样式
           • 设置了border-radius: 8px (RADIUS_MD)
           • 虽然移除了Tab结构，但样式定义仍在影响界面
        
        2. 样式继承问题：
           • QTabWidget::pane样式可能被其他Widget继承
           • 导致在对话框内部出现意外的圆角边框
           • 特别是在左上角等边缘位置更容易被察觉
        
        3. 视觉层次混乱：
           • 对话框外层: 12px圆角 (RADIUS_LG)
           • 内部容器: 8px圆角 (QTabWidget::pane残留)
           • 造成多层圆角嵌套，破坏整体协调性
        """)
        root_cause.setFont(QFont("Menlo", 10))
        root_cause.setStyleSheet("""
            QLabel {
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
                border-radius: 4px;
                padding: 15px;
                color: #721c24;
            }
        """)
        layout.addWidget(root_cause)
        
        # 修复方案
        fix_solution = QLabel("""
        🔧 修复方案：
        
        ✅ 移除过时的QTabWidget样式：
        • 从create_dialog_style()中完全移除QTabWidget::pane样式
        • 移除QTabBar相关的所有样式定义
        • 只保留纯净的QDialog基础样式
        
        ✅ 样式精简化：
        • 对话框样式只包含必要的背景色、边框和圆角
        • 避免定义不再使用的组件样式
        • 防止样式污染和意外继承
        
        ✅ 验证要点：
        • 对话框四个角附近不应该有内部圆角可见
        • 左上角关闭按钮下方区域应该是平整的
        • 整体视觉效果应该简洁统一
        """)
        fix_solution.setFont(QFont("Menlo", 10))
        fix_solution.setStyleSheet("""
            QLabel {
                background-color: #d4edda;
                border: 1px solid #c3e6cb;
                border-radius: 4px;
                padding: 15px;
                color: #155724;
            }
        """)
        layout.addWidget(fix_solution)
        
        if HAS_MODULES:
            # 测试按钮
            test_btn = QPushButton("🧪 测试修复后的对话框")
            test_btn.clicked.connect(self.show_edit_dialog)
            test_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 12px 24px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
            """)
            layout.addWidget(test_btn)
        
        # 验证清单
        verification_checklist = QLabel("""
        📋 验证清单 - 请仔细检查以下要点：
        
        🔍 关键验证区域：
        ☐ 左上角macOS关闭按钮(红色圆点)下方区域是否平整
        ☐ 右上角对话框边缘是否只有外层圆角
        ☐ 左下角和右下角是否无内部圆角可见
        ☐ 整个对话框内容区域是否视觉统一
        
        ✅ 期望效果：
        ☐ 只有对话框外边框有圆角(12px)
        ☐ 内部所有容器都是直角或无圆角
        ☐ 视觉层次清晰，无多余装饰
        ☐ 特别注意标签容器区域应该是直角边框
        
        ❌ 问题指标：
        ☐ 如果仍能看到内部小圆角，说明还有其他样式污染
        ☐ 如果四个角附近有圆角轮廓，需要进一步排查
        """)
        verification_checklist.setFont(QFont("Menlo", 10))
        verification_checklist.setStyleSheet("""
            QLabel {
                background-color: #e2e3e5;
                border: 1px solid #d6d8db;
                border-radius: 4px;
                padding: 15px;
                color: #383d41;
            }
        """)
        layout.addWidget(verification_checklist)
        
    def show_edit_dialog(self):
        """显示编辑对话框"""
        try:
            # 创建测试数据
            test_data = {
                'id': 1,
                'title': '圆角问题修复验证',
                'tags': '修复验证, 圆角, QTabWidget, 样式清理',
                'page_type': 'markdown',
                'created_at': datetime(2024, 1, 15, 10, 30, 0),
                'updated_at': datetime(2024, 1, 20, 15, 45, 30),
                'file_size': 2048,
                'content_md5': 'a1b2c3d4e5f6g7h8i9j0'
            }
            
            # 创建并显示对话框
            dialog = EditItemDialog(test_data, self)
            
            print("🔍 对话框已打开，请重点检查：")
            print("1. 【关键】左上角红色关闭按钮下方是否还有圆角轮廓")
            print("2. 【关键】对话框四个角附近是否只有外层圆角")
            print("3. 【关键】标签容器是否使用直角边框(无圆角)")
            print("4. 【整体】内容区域是否视觉统一，无多余圆角")
            print("5. 【对比】与之前截图对比，圆角问题是否已解决")
            
            result = dialog.exec()
            
            if result:
                print("✅ 对话框正常保存并关闭")
                print(f"最终标题: {dialog.get_new_title()}")
                print(f"最终标签: {dialog.get_new_tags()}")
                print("🎉 圆角问题修复验证完成！")
                print("💡 请确认是否还能看到截图中提到的内部小圆角")
            else:
                print("❌ 对话框被取消")
                print("💡 请确认取消前是否观察到圆角问题已解决")
                
        except Exception as e:
            print(f"❌ 显示对话框失败: {e}")
            import traceback
            traceback.print_exc()

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = DialogCornerFixTestWindow()
    window.show()
    
    print("✅ 对话框圆角问题修复验证已启动")
    print("🔍 请点击测试按钮，仔细观察修复效果")
    print("📸 请与原始截图对比，确认问题是否解决")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()