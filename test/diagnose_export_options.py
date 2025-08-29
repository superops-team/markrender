#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
导出选项数量诊断脚本
检查为什么导出菜单只显示3个选项而不是4个
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from app.topbar.button_controller import ButtonController

class ExportOptionsDiagnosisWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.start_diagnosis()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("🔍 导出选项数量诊断")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("🔍 导出选项数量诊断")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 问题说明
        problem_desc = QLabel("""
        🎯 诊断问题：export_btn应该有4个导出选项，为什么实际只有3个？
        
        预期的4个选项：
        1. 导出 HTML
        2. 导出 Markdown
        3. 导出 PDF
        4. 导出 EPUB
        
        需要检查：
        1. 代码中是否定义了4个选项
        2. 菜单创建过程是否正确
        3. 是否有选项被过滤或隐藏
        4. 实际显示的选项内容
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
        
        # 创建实际的TopBar
        topbar_container = QWidget()
        topbar_container.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border: 2px solid #dc3545;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        topbar_layout = QVBoxLayout(topbar_container)
        
        topbar_label = QLabel("📋 实际TopBar - 导出按钮测试")
        topbar_label.setFont(QFont("Arial", 12, QFont.Bold))
        topbar_layout.addWidget(topbar_label)
        
        # 创建依赖对象
        self.quickpick_panel = QWidget()
        self.markrender_editor = MockMarkRenderEditor()
        
        # 创建ButtonController
        self.button_controller = ButtonController(self, self.quickpick_panel, self.markrender_editor)
        topbar_layout.addWidget(self.button_controller)
        
        layout.addWidget(topbar_container)
        
        # 手动测试按钮
        test_btn = QPushButton("🧪 手动显示导出菜单测试")
        test_btn.clicked.connect(self.manual_test_menu)
        test_btn.setStyleSheet("""
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
        layout.addWidget(test_btn)
        
        # 诊断结果显示
        self.diagnosis_label = QLabel("正在诊断导出选项数量...")
        self.diagnosis_label.setFont(QFont("Menlo", 10))
        self.diagnosis_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 15px;
                color: #333;
            }
        """)
        layout.addWidget(self.diagnosis_label)
        
    def start_diagnosis(self):
        """开始诊断"""
        QTimer.singleShot(100, self.diagnose_export_options)
        
    def manual_test_menu(self):
        """手动测试菜单显示"""
        if hasattr(self.button_controller, 'export_btn'):
            export_btn = self.button_controller.export_btn
            menu = export_btn.menu()
            if menu:
                global_pos = export_btn.mapToGlobal(export_btn.rect().bottomLeft())
                menu.exec(global_pos)
                print("手动显示菜单完成")
            else:
                print("❌ 菜单不存在")
        else:
            print("❌ 导出按钮不存在")
        
    def diagnose_export_options(self):
        """诊断导出选项数量"""
        results = []
        results.append("🔍 导出选项数量诊断报告")
        results.append("=" * 50)
        
        # 检查导出按钮是否存在
        if hasattr(self.button_controller, 'export_btn'):
            export_btn = self.button_controller.export_btn
            results.append(f"✅ 导出按钮存在")
            
            # 检查菜单是否存在
            menu = export_btn.menu()
            if menu:
                results.append(f"✅ 导出菜单存在")
                
                # 获取所有菜单动作
                actions = menu.actions()
                results.append(f"\n📋 菜单分析:")
                results.append(f"  实际选项数量: {len(actions)}")
                results.append(f"  预期选项数量: 4")
                
                if len(actions) == 4:
                    results.append(f"  ✅ 选项数量正确")
                else:
                    results.append(f"  ❌ 选项数量不符合预期")
                
                # 详细分析每个选项
                results.append(f"\n📝 详细选项列表:")
                for i, action in enumerate(actions):
                    text = action.text()
                    visible = action.isVisible()
                    enabled = action.isEnabled()
                    tooltip = action.toolTip()
                    
                    results.append(f"  选项{i+1}:")
                    results.append(f"    文本: '{text}'")
                    results.append(f"    可见: {visible}")
                    results.append(f"    启用: {enabled}")
                    results.append(f"    提示: '{tooltip}'")
                    results.append(f"    状态: {'✅' if visible and enabled else '❌'}")
                
                # 检查是否有重复或异常的选项
                texts = [action.text() for action in actions]
                unique_texts = set(texts)
                if len(texts) != len(unique_texts):
                    results.append(f"\n⚠️ 发现重复选项:")
                    duplicates = []
                    for text in texts:
                        if texts.count(text) > 1 and text not in duplicates:
                            duplicates.append(text)
                    for dup in duplicates:
                        results.append(f"  重复项: '{dup}' (出现{texts.count(dup)}次)")
                
                # 检查预期的选项是否都存在
                expected_options = [
                    "导出 HTML",
                    "导出 Markdown", 
                    "导出 PDF",
                    "导出 EPUB"
                ]
                
                results.append(f"\n🎯 预期选项检查:")
                missing_options = []
                for expected in expected_options:
                    if expected in texts:
                        results.append(f"  ✅ '{expected}' - 存在")
                    else:
                        results.append(f"  ❌ '{expected}' - 缺失")
                        missing_options.append(expected)
                
                # 检查额外的选项
                extra_options = []
                for text in texts:
                    if text not in expected_options:
                        extra_options.append(text)
                
                if extra_options:
                    results.append(f"\n⚠️ 发现额外选项:")
                    for extra in extra_options:
                        results.append(f"  额外项: '{extra}'")
                
                # 代码层面验证
                results.append(f"\n💻 代码验证:")
                try:
                    # 检查代码中定义的export_formats
                    results.append(f"  检查create_export_button方法中的export_formats列表...")
                    
                    # 模拟重新创建菜单
                    test_formats = [
                        ('HTML', 'html', '导出为 HTML 网页'),
                        ('Markdown', 'md', '导出为 Markdown 文件'),
                        ('PDF', 'pdf', '导出为 PDF 文档'),
                        ('EPUB', 'epub', '导出为 EPUB 电子书')
                    ]
                    
                    results.append(f"  代码中定义的格式数量: {len(test_formats)}")
                    results.append(f"  代码中定义的格式:")
                    for name, fmt, tip in test_formats:
                        results.append(f"    - 导出 {name} ({fmt})")
                    
                    if len(test_formats) == 4:
                        results.append(f"  ✅ 代码定义正确")
                    else:
                        results.append(f"  ❌ 代码定义有问题")
                        
                except Exception as e:
                    results.append(f"  ❌ 代码验证失败: {e}")
                
                # 问题分析和建议
                results.append(f"\n🔧 问题分析:")
                if len(actions) < 4:
                    results.append(f"  原因可能:")
                    results.append(f"    1. 菜单创建过程中某些选项被跳过")
                    results.append(f"    2. 菜单样式导致某些选项被隐藏")
                    results.append(f"    3. lambda函数闭包问题导致选项创建异常")
                    results.append(f"    4. 菜单尺寸限制导致选项不显示")
                    
                    results.append(f"\n💡 建议修复:")
                    results.append(f"    1. 检查for循环是否正确执行4次")
                    results.append(f"    2. 验证addAction是否成功执行")
                    results.append(f"    3. 检查菜单样式是否影响显示")
                    results.append(f"    4. 重新创建菜单并逐步调试")
                    
                elif len(actions) == 4:
                    results.append(f"  菜单选项数量正确，可能是显示问题")
                    results.append(f"  建议检查菜单样式和尺寸设置")
                    
            else:
                results.append(f"❌ 导出菜单不存在")
                results.append(f"  需要检查create_export_button方法")
                
        else:
            results.append(f"❌ 导出按钮不存在")
            results.append(f"  需要检查setup_buttons方法")
        
        # 显示结果
        result_text = "\\n".join(results)
        self.diagnosis_label.setText(result_text)
        
        # 打印到控制台
        print(result_text)

class MockMarkRenderEditor:
    """模拟的Markdown编辑器"""
    def export_file(self, format_type):
        print(f"导出: {format_type}")

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = ExportOptionsDiagnosisWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()