#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按钮显示问题诊断脚本
检查实际运行时按钮显示不完整的问题
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                              QWidget, QLabel, QPushButton, QHBoxLayout)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

try:
    from app.topbar.button_controller import ButtonController
    from app.preference.style_utils import create_toolbar_menu_style, create_toolbar_button_style
    from app.preference.style_constants import TOOLBAR_BUTTON_SIZE, TOOLBAR_HEIGHT
    HAS_MODULES = True
except ImportError as e:
    print(f"⚠️  模块导入失败: {e}")
    HAS_MODULES = False

class MockMarkRenderEditor:
    """模拟MarkRender编辑器"""
    def export_content(self, format_type):
        print(f"✅ 模拟导出: {format_type}")

class ButtonDisplayDiagnostic(QMainWindow):
    """按钮显示问题诊断窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        if HAS_MODULES:
            QTimer.singleShot(100, self.start_diagnosis)
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("🔍 按钮显示问题诊断")
        self.setGeometry(100, 100, 900, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("🔍 按钮显示问题诊断")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 问题描述
        problem_desc = QLabel("""
        🎯 诊断目标：
        检查实际运行时按钮显示不完整的问题
        
        ❌ 可能的原因：
        • 菜单样式修改影响了按钮容器尺寸
        • 按钮控制器的高度或宽度设置问题
        • CSS样式冲突导致按钮被裁切
        • 父容器尺寸限制
        
        🔍 诊断重点：
        • 按钮控制器的实际尺寸
        • 单个按钮的显示状态
        • 容器的布局参数
        • 样式表的影响
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
        
        if HAS_MODULES:
            # 创建测试ButtonController
            test_container = QWidget()
            test_container.setStyleSheet("""
                QWidget {
                    background-color: #f8f9fa;
                    border: 2px solid #007AFF;
                    border-radius: 6px;
                    padding: 15px;
                }
            """)
            test_layout = QVBoxLayout(test_container)
            
            test_label = QLabel("📋 实际ButtonController测试")
            test_label.setFont(QFont("Arial", 12, QFont.Bold))
            test_layout.addWidget(test_label)
            
            # 创建模拟依赖
            self.quickpick_panel = QWidget()
            self.markdown_editor = MockMarkdownEditor()
            
            # 创建ButtonController
            self.button_controller = ButtonController(self, self.quickpick_panel, self.markdown_editor)
            test_layout.addWidget(self.button_controller)
            
            layout.addWidget(test_container)
        
        # 诊断结果显示
        self.diagnosis_label = QLabel("模块加载中..." if HAS_MODULES else "❌ 无法加载必要模块进行诊断")
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
        
        # 手动诊断按钮
        if HAS_MODULES:
            manual_btn = QPushButton("🔍 手动触发诊断")
            manual_btn.clicked.connect(self.manual_diagnosis)
            manual_btn.setStyleSheet("""
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
            layout.addWidget(manual_btn)
        
    def start_diagnosis(self):
        """开始诊断"""
        if not HAS_MODULES:
            return
            
        results = []
        results.append("🔍 按钮显示问题诊断报告")
        results.append("=" * 50)
        
        # 1. 检查ButtonController基本信息
        results.append("\n📊 ButtonController基本信息:")
        results.append("-" * 30)
        if hasattr(self, 'button_controller'):
            bc = self.button_controller
            results.append(f"  容器尺寸: {bc.width()}×{bc.height()}px")
            results.append(f"  容器位置: ({bc.x()}, {bc.y()})")
            results.append(f"  可见状态: {bc.isVisible()}")
            results.append(f"  启用状态: {bc.isEnabled()}")
            
            # 检查样式设置
            style_sheet = bc.styleSheet()
            if style_sheet:
                results.append(f"  样式表长度: {len(style_sheet)}字符")
            else:
                results.append("  ⚠️  未设置样式表")
        
        # 2. 检查单个按钮状态
        results.append("\n🔍 单个按钮详细信息:")
        results.append("-" * 30)
        
        buttons_info = [
            ('quickpick_btn', '历史面板按钮'),
            ('mode_btn', '模式切换按钮'),
            ('export_btn', '导出按钮')
        ]
        
        for btn_attr, btn_name in buttons_info:
            if hasattr(self.button_controller, btn_attr):
                btn = getattr(self.button_controller, btn_attr)
                results.append(f"\n  {btn_name}:")
                results.append(f"    尺寸: {btn.width()}×{btn.height()}px")
                results.append(f"    位置: ({btn.x()}, {btn.y()})")
                results.append(f"    可见: {btn.isVisible()}")
                results.append(f"    启用: {btn.isEnabled()}")
                
                # 检查固定尺寸设置
                size_hint = btn.sizeHint()
                min_size = btn.minimumSize()
                max_size = btn.maximumSize()
                results.append(f"    建议尺寸: {size_hint.width()}×{size_hint.height()}px")
                results.append(f"    最小尺寸: {min_size.width()}×{min_size.height()}px")
                results.append(f"    最大尺寸: {max_size.width()}×{max_size.height()}px")
                
                # 检查样式
                btn_style = btn.styleSheet()
                if btn_style:
                    results.append(f"    样式表: 已设置({len(btn_style)}字符)")
                else:
                    results.append(f"    样式表: ❌ 未设置")
            else:
                results.append(f"\n  {btn_name}: ❌ 不存在")
        
        # 3. 检查样式常量
        results.append("\n📏 样式常量检查:")
        results.append("-" * 30)
        try:
            results.append(f"  TOOLBAR_BUTTON_SIZE: {TOOLBAR_BUTTON_SIZE}px")
            results.append(f"  TOOLBAR_HEIGHT: {TOOLBAR_HEIGHT}px")
        except:
            results.append("  ❌ 无法获取样式常量")
        
        # 4. 分析可能的问题
        results.append("\n🔍 问题分析:")
        results.append("-" * 30)
        
        # 检查容器高度是否足够
        if hasattr(self, 'button_controller'):
            bc_height = self.button_controller.height()
            try:
                expected_height = TOOLBAR_HEIGHT
                if bc_height < expected_height:
                    results.append(f"  ❌ 容器高度不足: {bc_height}px < {expected_height}px")
                else:
                    results.append(f"  ✅ 容器高度充足: {bc_height}px >= {expected_height}px")
            except:
                results.append("  ⚠️  无法比较容器高度")
        
        # 检查按钮是否被裁切
        for btn_attr, btn_name in buttons_info:
            if hasattr(self.button_controller, btn_attr):
                btn = getattr(self.button_controller, btn_attr)
                btn_right = btn.x() + btn.width()
                container_width = self.button_controller.width()
                
                if btn_right > container_width:
                    results.append(f"  ❌ {btn_name}可能被裁切: 右边界{btn_right}px > 容器宽度{container_width}px")
                
                btn_bottom = btn.y() + btn.height()
                container_height = self.button_controller.height()
                
                if btn_bottom > container_height:
                    results.append(f"  ❌ {btn_name}可能被裁切: 下边界{btn_bottom}px > 容器高度{container_height}px")
        
        # 5. 修复建议
        results.append("\n💡 修复建议:")
        results.append("-" * 30)
        results.append("  1. 检查main.py中ButtonController的高度设置")
        results.append("  2. 确认TOOLBAR_HEIGHT常量值是否合适")
        results.append("  3. 验证CSS样式是否影响按钮显示")
        results.append("  4. 检查父容器的布局约束")
        results.append("  5. 确认按钮的setFixedSize设置是否生效")
        
        result_text = "\n".join(results)
        self.diagnosis_label.setText(result_text)
        
    def manual_diagnosis(self):
        """手动触发诊断"""
        self.start_diagnosis()

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = ButtonDisplayDiagnostic()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()