#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TopBar问题诊断脚本
专门诊断截图中显示的具体问题：
1. 按钮上下距离不一致
2. 导出按钮小黑点重叠
3. 导出按钮菜单不响应
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

class TopBarDiagnosisWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.start_diagnosis()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("🔍 TopBar问题诊断 - 针对截图问题")
        self.setGeometry(100, 100, 900, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("🔍 TopBar问题专项诊断")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 问题说明
        problem_desc = QLabel("""
        🎯 诊断目标：
        1. 按钮上下距离不一致 (截图显示的对齐问题)
        2. 导出按钮有小黑点重叠 (菜单指示器问题)
        3. 点击导出按钮没有下拉菜单 (交互失效)
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
        
        # 创建测试TopBar
        test_container = QWidget()
        test_container.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border: 2px solid #007AFF;
                border-radius: 6px;
                margin: 10px;
            }
        """)
        test_layout = QVBoxLayout(test_container)
        test_layout.setContentsMargins(10, 10, 10, 10)
        
        # 标签
        test_label = QLabel("📋 实际TopBar测试 (与截图对比)")
        test_label.setFont(QFont("Arial", 12, QFont.Bold))
        test_layout.addWidget(test_label)
        
        # 创建模拟的依赖对象
        self.quickpick_panel = QWidget()
        self.markdown_editor = MockMarkdownEditor()
        
        # 创建实际的ButtonController
        self.button_controller = ButtonController(self, self.quickpick_panel, self.markdown_editor)
        self.button_controller.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border: 1px solid #dee2e6;
                border-radius: 4px;
            }
        """)
        test_layout.addWidget(self.button_controller)
        
        layout.addWidget(test_container)
        
        # 诊断信息显示区域
        self.info_label = QLabel("正在诊断TopBar问题...")
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
        
        # 添加菜单测试按钮
        test_btn = QPushButton("🧪 手动测试导出菜单")
        test_btn.clicked.connect(self.test_export_menu)
        test_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        layout.addWidget(test_btn)
        
    def start_diagnosis(self):
        """开始诊断"""
        # 延迟执行诊断，确保UI完全初始化
        QTimer.singleShot(100, self.diagnose_issues)
        
    def test_export_menu(self):
        """手动测试导出菜单"""
        try:
            export_btn = self.button_controller.export_btn
            menu = export_btn.menu()
            if menu:
                # 手动显示菜单
                button_rect = export_btn.geometry()
                global_pos = export_btn.mapToGlobal(export_btn.rect().bottomLeft())
                menu.exec(global_pos)
                print("✅ 手动菜单测试成功")
            else:
                print("❌ 未找到菜单对象")
        except Exception as e:
            print(f"❌ 菜单测试失败: {e}")
            
    def diagnose_issues(self):
        """诊断具体问题"""
        results = []
        results.append("🔍 TopBar问题专项诊断报告")
        results.append("=" * 60)
        results.append("📋 针对截图反馈的三个具体问题进行诊断")
        
        # 问题1: 按钮上下距离诊断
        results.append(f"\n❗ 问题1: 按钮上下距离不一致")
        results.append("-" * 40)
        
        container_height = self.button_controller.height()
        layout = self.button_controller.layout()
        
        # 检查所有按钮的垂直位置
        buttons = [
            ("历史面板按钮", getattr(self.button_controller, 'quickpick_btn', None)),
            ("模式切换按钮", getattr(self.button_controller, 'mode_btn', None)),
            ("导出按钮", getattr(self.button_controller, 'export_btn', None))
        ]
        
        button_positions = []
        for name, button in buttons:
            if button:
                rect = button.geometry()
                top_space = rect.y()
                bottom_space = container_height - (rect.y() + rect.height())
                button_positions.append((name, top_space, bottom_space, rect.height()))
                
                results.append(f"  {name}:")
                results.append(f"    位置: y={rect.y()}, 高度={rect.height()}")
                results.append(f"    上方空间: {top_space}px")
                results.append(f"    下方空间: {bottom_space}px")
                results.append(f"    垂直居中偏差: {top_space - bottom_space}px")
        
        # 检查一致性
        if button_positions:
            top_spaces = [pos[1] for pos in button_positions]
            bottom_spaces = [pos[2] for pos in button_positions]
            
            if len(set(top_spaces)) == 1 and len(set(bottom_spaces)) == 1:
                results.append(f"  ✅ 所有按钮垂直位置一致")
            else:
                results.append(f"  ❌ 按钮垂直位置不一致!")
                results.append(f"      上方空间: {top_spaces}")
                results.append(f"      下方空间: {bottom_spaces}")
        
        # 问题2: 小黑点诊断
        results.append(f"\n❗ 问题2: 导出按钮小黑点重叠")
        results.append("-" * 40)
        
        if hasattr(self.button_controller, 'export_btn'):
            export_btn = self.button_controller.export_btn
            popup_mode = export_btn.popupMode()
            results.append(f"  导出按钮弹出模式: {popup_mode}")
            
            # 检查样式设置
            style_sheet = export_btn.styleSheet()
            if "menu-indicator" in style_sheet and "width: 0px" in style_sheet:
                results.append(f"  ✅ CSS已隐藏菜单指示器")
            else:
                results.append(f"  ❌ CSS未正确隐藏菜单指示器")
                
            # 检查菜单按钮样式
            if "menu-button" in style_sheet and "width: 0px" in style_sheet:
                results.append(f"  ✅ CSS已隐藏菜单按钮")
            else:
                results.append(f"  ❌ CSS未正确隐藏菜单按钮")
                
            # 建议修复方案
            if popup_mode == 1:  # MenuButtonPopup
                results.append(f"  ⚠️  MenuButtonPopup模式可能显示箭头指示器")
                results.append(f"  💡 建议: 改为InstantPopup模式或DelayedPopup模式")
        
        # 问题3: 菜单响应诊断
        results.append(f"\n❗ 问题3: 导出按钮菜单不响应")
        results.append("-" * 40)
        
        if hasattr(self.button_controller, 'export_btn'):
            export_btn = self.button_controller.export_btn
            menu = export_btn.menu()
            
            if menu:
                actions = menu.actions()
                results.append(f"  ✅ 菜单对象存在: {len(actions)}个动作")
                results.append(f"  📋 菜单动作列表:")
                for i, action in enumerate(actions):
                    results.append(f"    {i+1}. {action.text()}")
                    
                # 检查信号连接
                results.append(f"  🔌 检查信号连接:")
                connected_count = 0
                for action in actions:
                    # 这里无法直接检查信号连接，但可以检查action是否有效
                    if action.isEnabled():
                        connected_count += 1
                        
                results.append(f"    启用的动作数量: {connected_count}/{len(actions)}")
                
                # 检查菜单样式
                menu_style = menu.styleSheet()
                if menu_style:
                    results.append(f"  ✅ 菜单已应用样式")
                else:
                    results.append(f"  ⚠️  菜单未应用样式")
                    
            else:
                results.append(f"  ❌ 菜单对象不存在!")
        
        # 综合诊断和修复建议
        results.append(f"\n🔧 综合诊断和修复建议")
        results.append("=" * 40)
        
        results.append(f"📋 基于截图问题的修复方案:")
        results.append(f"  1. 上下距离问题:")
        results.append(f"     - 检查容器布局的垂直对齐设置")
        results.append(f"     - 确认所有按钮使用相同的尺寸设置")
        results.append(f"     - 验证CSS样式没有影响垂直位置")
        
        results.append(f"  2. 小黑点问题:")
        results.append(f"     - 改变菜单弹出模式为InstantPopup")
        results.append(f"     - 强化CSS隐藏菜单指示器")
        results.append(f"     - 添加!important标记确保样式生效")
        
        results.append(f"  3. 菜单不响应问题:")
        results.append(f"     - 验证菜单事件处理")
        results.append(f"     - 检查clicked信号连接")
        results.append(f"     - 测试菜单显示位置")
        
        results.append(f"\n💡 建议立即执行的修复:")
        results.append(f"  1. 将导出按钮改为InstantPopup模式")
        results.append(f"  2. 强化CSS菜单指示器隐藏")
        results.append(f"  3. 添加按钮点击事件调试")
        
        # 显示结果
        result_text = "\n".join(results)
        self.info_label.setText(result_text)
        
        # 打印到控制台
        print(result_text)

class MockMarkdownEditor:
    """模拟的Markdown编辑器，用于测试"""
    def export_file(self, format_type):
        print(f"模拟导出: {format_type}")

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = TopBarDiagnosisWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()