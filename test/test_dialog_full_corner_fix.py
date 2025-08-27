#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对话框完整圆角修复验证脚本
专门验证对话框四个角的圆角显示是否完整
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

class DialogFullCornerTestWindow(QMainWindow):
    """对话框完整圆角测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("✅ 对话框完整圆角修复验证")
        self.setGeometry(100, 100, 800, 650)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("✅ 对话框完整圆角修复验证")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 问题描述
        problem_desc = QLabel("""
        📸 用户反馈问题：
        "圆角设置上只有左上方和右上方有，下面没有"
        
        🔍 问题表现：
        • 对话框左上角和右上角有正常的圆角
        • 对话框左下角和右下角显示为直角
        • 圆角不完整，影响视觉一致性
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
        
        # 修复方案
        fix_desc = QLabel("""
        🔧 修复方案：
        
        1. 明确四角圆角设置：
           • 在QDialog样式中显式设置四个角的圆角
           • border-top-left-radius: 12px
           • border-top-right-radius: 12px
           • border-bottom-left-radius: 12px
           • border-bottom-right-radius: 12px
        
        2. 调整布局边距：
           • 减少主布局的内边距从20px到16px
           • 避免内容过于贴近边缘影响圆角显示
        
        3. 保存按钮优化：
           • 增加保存按钮的底部边距
           • 确保按钮不会覆盖对话框下方的圆角
        """)
        fix_desc.setFont(QFont("Menlo", 11))
        fix_desc.setStyleSheet("""
            QLabel {
                background-color: #d4edda;
                border: 1px solid #c3e6cb;
                border-radius: 4px;
                padding: 15px;
                color: #155724;
            }
        """)
        layout.addWidget(fix_desc)
        
        if HAS_MODULES:
            # 测试按钮
            test_btn = QPushButton("🧪 测试修复后的完整圆角")
            test_btn.clicked.connect(self.show_edit_dialog)
            test_btn.setStyleSheet("""
                QPushButton {
                    background-color: #28a745;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 12px 24px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #218838;
                }
            """)
            layout.addWidget(test_btn)
        
        # 验证清单
        verification_desc = QLabel("""
        📋 验证清单 - 请仔细检查四个角：
        
        🔍 左上角检查：
        ☐ 左上角应该有清晰的圆角（12px半径）
        ☐ 圆角应该平滑过渡，无锯齿
        
        🔍 右上角检查：
        ☐ 右上角应该有清晰的圆角（12px半径）
        ☐ 与左上角圆角保持一致
        
        🔍 左下角检查：
        ☐ 左下角应该有清晰的圆角（12px半径）
        ☐ 不应该是直角或方形
        
        🔍 右下角检查：
        ☐ 右下角应该有清晰的圆角（12px半径）
        ☐ 与其他三个角保持一致
        
        ✅ 整体检查：
        ☐ 四个角的圆角大小完全一致
        ☐ 保存按钮不会遮挡下方圆角
        ☐ 对话框整体呈现统一的圆角矩形
        ☐ 视觉效果协调美观
        
        ❌ 如果问题仍然存在：
        ☐ 检查是否macOS系统层面的限制
        ☐ 可能需要调整Qt窗口标志
        ☐ 考虑使用自定义绘制方案
        """)
        verification_desc.setFont(QFont("Menlo", 10))
        verification_desc.setStyleSheet("""
            QLabel {
                background-color: #e2e3e5;
                border: 1px solid #d6d8db;
                border-radius: 4px;
                padding: 15px;
                color: #383d41;
            }
        """)
        layout.addWidget(verification_desc)
        
    def show_edit_dialog(self):
        """显示编辑对话框"""
        try:
            # 创建测试数据
            test_data = {
                'id': 1,
                'title': '完整圆角修复验证',
                'tags': '圆角修复, 四角检查, Qt样式',
                'page_type': 'markdown',
                'created_at': datetime(2024, 1, 15, 10, 30, 0),
                'updated_at': datetime(2024, 1, 20, 15, 45, 30),
                'file_size': 2048,
                'content_md5': 'a1b2c3d4e5f6g7h8i9j0'
            }
            
            # 创建并显示对话框
            dialog = EditItemDialog(test_data, self)
            
            print("🔍 对话框已打开，请逐一检查四个角：")
            print("1. 【左上角】应该有12px圆角，平滑过渡")
            print("2. 【右上角】应该有12px圆角，与左上角一致")
            print("3. 【左下角】应该有12px圆角，不是直角！")
            print("4. 【右下角】应该有12px圆角，与其他角一致")
            print("5. 【整体】四个角应该完全对称，形成统一的圆角矩形")
            print("")
            print("💡 如果下方仍然是直角，可能需要进一步的系统级修复")
            
            result = dialog.exec()
            
            if result:
                print("✅ 对话框正常保存并关闭")
                print(f"最终标题: {dialog.get_new_title()}")
                print(f"最终标签: {dialog.get_new_tags()}")
                print("🎉 完整圆角修复验证完成！")
                print("")
                print("📝 请确认四个角的圆角是否都正常显示：")
                print("   - 如果都正常：✅ 修复成功")
                print("   - 如果下方仍是直角：❌ 需要进一步调查")
            else:
                print("❌ 对话框被取消")
                print("💡 请确认取消前是否观察到四个角的圆角状态")
                
        except Exception as e:
            print(f"❌ 显示对话框失败: {e}")
            import traceback
            traceback.print_exc()

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = DialogFullCornerTestWindow()
    window.show()
    
    print("✅ 对话框完整圆角修复验证已启动")
    print("🔍 请点击测试按钮，重点观察四个角的圆角显示")
    print("📸 请与用户截图对比，确认下方圆角是否已修复")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()