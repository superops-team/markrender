#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导出菜单问题诊断脚本
检查菜单只显示第一个选项的问题
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                               QHBoxLayout, QLabel, QPushButton, QToolButton, QMenu)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QIcon

from app.topbar.button_controller import ButtonController
from app.preference.style_constants import TOOLBAR_HEIGHT, TOOLBAR_BUTTON_SIZE
from app.preference.style_utils import create_toolbar_menu_style

class ExportMenuDiagnosisWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.start_diagnosis()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("🔍 导出菜单问题诊断")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("🔍 导出菜单显示问题诊断")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 问题说明
        problem_desc = QLabel("""
        🎯 诊断问题：导出按钮只能展示第一个导出项，其他选项不显示
        
        可能原因：
        1. 菜单高度设置问题
        2. 菜单样式导致项目被隐藏
        3. 菜单容器尺寸限制
        4. CSS样式冲突
        """)
        problem_desc.setFont(QFont("Menlo", 11))
        problem_desc.setStyleSheet("""
            QLabel {
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 4px;
                padding: 10px;
                color: #856404;
            }
        """)
        layout.addWidget(problem_desc)
        
        # 创建测试区域
        test_container = QWidget()
        test_container.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border: 2px solid #007AFF;
                border-radius: 6px;
            }
        """)
        test_layout = QVBoxLayout(test_container)
        test_layout.setContentsMargins(15, 15, 15, 15)
        
        # 原始ButtonController测试
        original_label = QLabel("📋 原始TopBar - ButtonController")
        original_label.setFont(QFont("Arial", 12, QFont.Bold))
        test_layout.addWidget(original_label)
        
        # 创建模拟依赖
        self.quickpick_panel = QWidget()
        self.markrender_editor =  MockMarkRenderEditor()
        
        # 创建原始ButtonController
        self.button_controller = ButtonController(self, self.quickpick_panel, self.markrender_editor)
        test_layout.addWidget(self.button_controller)
        
        # 独立菜单测试
        standalone_label = QLabel("🧪 独立菜单测试")
        standalone_label.setFont(QFont("Arial", 12, QFont.Bold))
        test_layout.addWidget(standalone_label)
        
        # 创建独立的菜单测试按钮
        self.create_standalone_menu_test(test_layout)
        
        layout.addWidget(test_container)
        
        # 诊断信息显示
        self.info_label = QLabel("正在诊断导出菜单问题...")
        self.info_label.setFont(QFont("Menlo", 10))
        self.info_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 15px;
                color: #333;
            }
        """)
        layout.addWidget(self.info_label)
        
    def create_standalone_menu_test(self, layout):
        """创建独立的菜单测试"""
        test_row = QWidget()
        test_row_layout = QHBoxLayout(test_row)
        test_row_layout.setContentsMargins(0, 0, 0, 0)
        
        # 测试1: 默认样式菜单
        default_btn = QPushButton("默认样式菜单")
        default_btn.clicked.connect(self.show_default_menu)
        test_row_layout.addWidget(default_btn)
        
        # 测试2: 当前样式菜单
        current_btn = QPushButton("当前样式菜单")
        current_btn.clicked.connect(self.show_current_style_menu)
        test_row_layout.addWidget(current_btn)
        
        # 测试3: 修复样式菜单
        fixed_btn = QPushButton("修复样式菜单")
        fixed_btn.clicked.connect(self.show_fixed_style_menu)
        test_row_layout.addWidget(fixed_btn)
        
        # 测试4: 调试信息菜单
        debug_btn = QPushButton("调试信息")
        debug_btn.clicked.connect(self.show_debug_info)
        test_row_layout.addWidget(debug_btn)
        
        layout.addWidget(test_row)
        
    def show_default_menu(self):
        """显示默认样式菜单"""
        menu = QMenu(self)
        # 不设置任何自定义样式
        
        export_formats = [
            '导出 HTML',
            '导出 Markdown', 
            '导出 PDF',
            '导出 EPUB'
        ]
        
        for fmt in export_formats:
            action = menu.addAction(fmt)
            action.triggered.connect(lambda checked, f=fmt: print(f"选择了: {f}"))
        
        # 显示在按钮下方
        sender = self.sender()
        menu.exec(sender.mapToGlobal(sender.rect().bottomLeft()))
        
    def show_current_style_menu(self):
        """显示当前样式菜单"""
        menu = QMenu(self)
        menu.setStyleSheet(create_toolbar_menu_style())
        
        export_formats = [
            '导出 HTML',
            '导出 Markdown',
            '导出 PDF', 
            '导出 EPUB'
        ]
        
        for fmt in export_formats:
            action = menu.addAction(fmt)
            action.triggered.connect(lambda checked, f=fmt: print(f"选择了: {f}"))
        
        sender = self.sender()
        menu.exec(sender.mapToGlobal(sender.rect().bottomLeft()))
        
    def show_fixed_style_menu(self):
        """显示修复样式菜单"""
        menu = QMenu(self)
        
        # 修复的菜单样式 - 增加高度和宽度
        fixed_style = """
        QMenu {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            padding: 4px;
            min-width: 120px;
            min-height: 100px;
        }
        QMenu::item {
            color: #333333;
            padding: 8px 12px;
            margin: 1px;
            border-radius: 3px;
            font-size: 13px;
            min-height: 20px;
        }
        QMenu::item:selected {
            background-color: #e3f2fd;
            color: #1976d2;
        }
        QMenu::item:pressed {
            background-color: #bbdefb;
        }
        """
        
        menu.setStyleSheet(fixed_style)
        
        export_formats = [
            '导出 HTML',
            '导出 Markdown',
            '导出 PDF',
            '导出 EPUB'
        ]
        
        for fmt in export_formats:
            action = menu.addAction(fmt)
            action.triggered.connect(lambda checked, f=fmt: print(f"选择了: {f}"))
        
        sender = self.sender()
        menu.exec(sender.mapToGlobal(sender.rect().bottomLeft()))
        
    def show_debug_info(self):
        """显示调试信息"""
        if hasattr(self.button_controller, 'export_btn'):
            export_btn = self.button_controller.export_btn
            menu = export_btn.menu()
            
            if menu:
                print("\n=== 导出菜单调试信息 ===")
                print(f"菜单对象: {menu}")
                print(f"菜单父对象: {menu.parent()}")
                print(f"菜单尺寸: {menu.size()}")
                print(f"菜单可见: {menu.isVisible()}")
                
                actions = menu.actions()
                print(f"菜单动作数量: {len(actions)}")
                
                for i, action in enumerate(actions):
                    print(f"  动作{i+1}: {action.text()}")
                    print(f"    可见: {action.isVisible()}")
                    print(f"    启用: {action.isEnabled()}")
                    
                # 检查菜单样式
                style = menu.styleSheet()
                print(f"菜单样式长度: {len(style)}")
                if style:
                    print("菜单样式片段:")
                    print(style[:200] + "..." if len(style) > 200 else style)
                    
                # 手动显示菜单进行测试
                print("手动显示菜单...")
                global_pos = export_btn.mapToGlobal(export_btn.rect().bottomLeft())
                print(f"显示位置: {global_pos}")
                menu.exec(global_pos)
            else:
                print("❌ 菜单对象不存在")
        else:
            print("❌ 导出按钮不存在")
        
    def start_diagnosis(self):
        """开始诊断"""
        QTimer.singleShot(100, self.diagnose_menu_issues)
        
    def diagnose_menu_issues(self):
        """诊断菜单问题"""
        results = []
        results.append("🔍 导出菜单问题诊断报告")
        results.append("=" * 50)
        
        if hasattr(self.button_controller, 'export_btn'):
            export_btn = self.button_controller.export_btn
            menu = export_btn.menu()
            
            if menu:
                results.append(f"\n✅ 菜单对象存在")
                
                # 检查菜单尺寸
                menu_size = menu.size()
                results.append(f"📐 菜单尺寸: {menu_size.width()}×{menu_size.height()}")
                
                # 检查动作
                actions = menu.actions()
                results.append(f"📋 菜单动作数量: {len(actions)}")
                
                for i, action in enumerate(actions):
                    results.append(f"  动作{i+1}: {action.text()}")
                    results.append(f"    可见: {'✅' if action.isVisible() else '❌'}")
                    results.append(f"    启用: {'✅' if action.isEnabled() else '❌'}")
                
                # 检查样式问题
                style = menu.styleSheet()
                results.append(f"\n🎨 样式分析:")
                results.append(f"  样式长度: {len(style)}字符")
                
                # 分析可能的问题
                potential_issues = []
                
                if "min-width: 80px" in style:
                    potential_issues.append("菜单宽度可能过窄")
                    
                if "padding: 2px" in style or "padding: 4px" in style:
                    potential_issues.append("内边距可能过小")
                    
                if "margin: 1px" in style:
                    potential_issues.append("边距设置可能影响显示")
                    
                if not any(["min-height" in style, "height" in style]):
                    potential_issues.append("缺少明确的高度设置")
                    
                if potential_issues:
                    results.append(f"\n⚠️ 可能的问题:")
                    for issue in potential_issues:
                        results.append(f"  - {issue}")
                else:
                    results.append(f"\n✅ 样式设置看起来正常")
                
                # 修复建议
                results.append(f"\n🔧 修复建议:")
                results.append(f"  1. 增加菜单最小宽度到120px")
                results.append(f"  2. 增加菜单项内边距到8px 12px")
                results.append(f"  3. 设置菜单项最小高度为20px")
                results.append(f"  4. 增加菜单整体最小高度")
                
            else:
                results.append(f"\n❌ 菜单对象不存在")
                
        else:
            results.append(f"\n❌ 导出按钮不存在")
            
        # 显示结果
        result_text = "\n".join(results)
        self.info_label.setText(result_text)
        print(result_text)

class MockMarkRenderEditor:
    """模拟的MarkRender编辑器"""
    def export_file(self, format_type):
        print(f"模拟导出: {format_type}")

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = ExportMenuDiagnosisWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()