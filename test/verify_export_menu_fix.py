#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导出菜单修复验证脚本
验证所有菜单选项都能正常显示
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from app.topbar.button_controller import ButtonController

class ExportMenuVerificationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.start_verification()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("✅ 导出菜单修复验证")
        self.setGeometry(100, 100, 700, 400)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("✅ 导出菜单修复验证")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 成功提示
        success_desc = QLabel("""
        🎉 修复内容：
        1. 菜单最小宽度：80px → 120px
        2. 菜单最小高度：新增 120px
        3. 菜单项内边距：4px 8px → 8px 12px  
        4. 菜单项最小高度：新增 20px
        5. 整体边距：4px → 6px
        
        预期效果：所有4个导出选项都能正常显示
        """)
        success_desc.setFont(QFont("Menlo", 11))
        success_desc.setStyleSheet("""
            QLabel {
                background-color: #d4edda;
                border: 1px solid #c3e6cb;
                border-radius: 4px;
                padding: 15px;
                color: #155724;
            }
        """)
        layout.addWidget(success_desc)
        
        # 创建实际的TopBar
        topbar_container = QWidget()
        topbar_container.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border: 2px solid #28a745;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        topbar_layout = QVBoxLayout(topbar_container)
        
        topbar_label = QLabel("📋 实际TopBar - 请点击导出按钮测试")
        topbar_label.setFont(QFont("Arial", 12, QFont.Bold))
        topbar_layout.addWidget(topbar_label)
        
        # 创建依赖对象
        self.quickpick_panel = QWidget()
        self.markdown_editor = MockMarkdownEditor()
        
        # 创建ButtonController
        self.button_controller = ButtonController(self, self.quickpick_panel, self.markdown_editor)
        topbar_layout.addWidget(self.button_controller)
        
        layout.addWidget(topbar_container)
        
        # 验证按钮
        verify_btn = QPushButton("🧪 验证菜单显示")
        verify_btn.clicked.connect(self.verify_menu_display)
        verify_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        layout.addWidget(verify_btn)
        
        # 验证结果显示
        self.result_label = QLabel("点击验证按钮查看结果...")
        self.result_label.setFont(QFont("Menlo", 10))
        self.result_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 15px;
                color: #333;
            }
        """)
        layout.addWidget(self.result_label)
        
    def start_verification(self):
        """开始验证"""
        QTimer.singleShot(100, self.initial_check)
        
    def initial_check(self):
        """初始检查"""
        results = []
        results.append("🔍 导出菜单修复效果验证")
        results.append("=" * 40)
        
        if hasattr(self.button_controller, 'export_btn'):
            export_btn = self.button_controller.export_btn
            menu = export_btn.menu()
            
            if menu:
                # 检查菜单尺寸
                menu_size = menu.size()
                results.append(f"📐 菜单尺寸: {menu_size.width()}×{menu_size.height()}px")
                
                # 检查改进效果
                if menu_size.width() >= 120:
                    results.append("✅ 菜单宽度已优化 (≥120px)")
                else:
                    results.append("❌ 菜单宽度仍需优化")
                    
                if menu_size.height() >= 120:
                    results.append("✅ 菜单高度已优化 (≥120px)")
                else:
                    results.append("❌ 菜单高度仍需优化")
                
                # 检查菜单项
                actions = menu.actions()
                results.append(f"\n📋 菜单项检查:")
                results.append(f"  总数: {len(actions)}个")
                
                all_visible = True
                for i, action in enumerate(actions):
                    visible = action.isVisible()
                    enabled = action.isEnabled()
                    status = "✅" if visible and enabled else "❌"
                    results.append(f"  {i+1}. {action.text()} {status}")
                    if not (visible and enabled):
                        all_visible = False
                
                if all_visible:
                    results.append("\n🎉 所有菜单项状态正常!")
                else:
                    results.append("\n⚠️ 部分菜单项状态异常")
                
                # 提供测试指引
                results.append(f"\n🧪 请手动测试:")
                results.append(f"  1. 点击右上角的导出按钮 📥")
                results.append(f"  2. 确认能看到所有4个选项:")
                results.append(f"     - 导出 HTML")
                results.append(f"     - 导出 Markdown")
                results.append(f"     - 导出 PDF")
                results.append(f"     - 导出 EPUB")
                results.append(f"  3. 选择任一选项测试功能")
                
            else:
                results.append("❌ 菜单对象不存在")
        else:
            results.append("❌ 导出按钮不存在")
            
        result_text = "\\n".join(results)
        self.result_label.setText(result_text)
        
    def verify_menu_display(self):
        """验证菜单显示"""
        if hasattr(self.button_controller, 'export_btn'):
            export_btn = self.button_controller.export_btn
            menu = export_btn.menu()
            
            if menu:
                # 手动显示菜单进行验证
                global_pos = export_btn.mapToGlobal(export_btn.rect().bottomLeft())
                menu.exec(global_pos)
                
                # 更新验证结果
                results = []
                results.append("✅ 菜单显示测试完成")
                results.append("-" * 30)
                results.append("如果您能看到所有4个选项，说明修复成功！")
                results.append("")
                results.append("🎯 修复前后对比:")
                results.append("  修复前: 菜单尺寸小，可能只显示1个选项")
                results.append("  修复后: 菜单尺寸大，显示全部4个选项")
                results.append("")
                results.append("📊 具体改进:")
                results.append("  • 菜单宽度: 80px → 120px (+50%)")
                results.append("  • 菜单高度: 自动 → 最小120px")
                results.append("  • 菜单项高度: 自动 → 最小20px")
                results.append("  • 菜单项边距: 4px 8px → 8px 12px")
                
                result_text = "\\n".join(results)
                self.result_label.setText(result_text)
            else:
                self.result_label.setText("❌ 无法找到菜单对象")
        else:
            self.result_label.setText("❌ 无法找到导出按钮")

class MockMarkdownEditor:
    """模拟的Markdown编辑器"""
    def export_file(self, format_type):
        print(f"✅ 导出功能测试成功: {format_type}")

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = ExportMenuVerificationWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()