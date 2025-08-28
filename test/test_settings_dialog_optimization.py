#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设置对话框Robin Williams设计原则优化验证脚本
基于四大设计原则验证优化效果：亲密性、对齐、重复和对比
"""

import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

try:
    from app.sidebar.settings_dialog import SettingsDialog
    HAS_MODULES = True
except ImportError as e:
    print(f"⚠️  模块导入失败: {e}")
    HAS_MODULES = False

class SettingsDialogTestWindow(QMainWindow):
    """设置对话框优化测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("✅ 设置对话框Robin Williams设计原则优化验证")
        self.setGeometry(100, 100, 800, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("✅ 设置对话框设计优化验证")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Robin Williams四大设计原则说明
        principles_desc = QLabel("""
        🎨 Robin Williams四大设计原则优化：
        
        ✅ 1. 亲密性 (Proximity)：
        • 相关设置项分组在一起（分组框）
        • 每个Tab页面内部逻辑分区清晰
        • 标签和对应控件紧密排列
        
        ✅ 2. 对齐 (Alignment)：
        • 统一的内边距和间距系统
        • 控件左对齐，视觉线条清晰
        • 按钮区域右对齐，符合操作习惯
        
        ✅ 3. 重复 (Repetition)：
        • 统一的字体、颜色和间距规范
        • 一致的输入框、按钮样式
        • 统一的分组框和标签设计
        
        ✅ 4. 对比 (Contrast)：
        • 突出显示重要功能（深色模式）
        • 层次分明的标题、标签、内容
        • 主要操作（保存）与次要操作（取消）的视觉区分
        """)
        principles_desc.setFont(QFont("Menlo", 11))
        principles_desc.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 20px;
                color: #495057;
                line-height: 1.6;
            }
        """)
        layout.addWidget(principles_desc)
        
        if HAS_MODULES:
            # 测试按钮
            test_btn = QPushButton("🎯 测试优化后的设置对话框")
            test_btn.clicked.connect(self.show_settings_dialog)
            test_btn.setStyleSheet("""
                QPushButton {
                    background-color: #007bff;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 15px 30px;
                    font-size: 16px;
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
        
        📐 亲密性检查：
        ☐ 相关设置项是否聚合在同一分组框内
        ☐ 不同功能区域之间是否有合适的间距分隔
        ☐ 标签和对应控件是否紧密配对
        
        📏 对齐检查：
        ☐ 各个Tab页面的布局是否保持一致的边距
        ☐ 表单元素是否整齐对齐
        ☐ 按钮区域的对齐是否符合操作习惯
        
        🔄 重复检查：
        ☐ 字体大小、颜色是否保持一致
        ☐ 输入框、按钮、分组框样式是否统一
        ☐ 图标和标签的使用是否规范一致
        
        ⚡ 对比检查：
        ☐ 重要功能（如深色模式切换）是否突出显示
        ☐ 标题、正文、辅助文字的层次是否分明
        ☐ 主要操作按钮是否明显区别于次要操作
        ☐ 提示信息的样式是否有效传达信息层级
        
        🎨 整体协调性：
        ☐ 与软件其他对话框的设计语言是否一致
        ☐ 配色方案是否遵循项目的设计令牌系统
        ☐ 圆角、间距等细节是否精确匹配设计规范
        """)
        verification_desc.setFont(QFont("Menlo", 10))
        verification_desc.setStyleSheet("""
            QLabel {
                background-color: #e8f5e8;
                border: 1px solid #c3e6cb;
                border-radius: 8px;
                padding: 20px;
                color: #155724;
                line-height: 1.5;
            }
        """)
        layout.addWidget(verification_desc)
        
    def show_settings_dialog(self):
        """显示设置对话框"""
        try:
            # 创建并显示设置对话框
            dialog = SettingsDialog(self)
            
            print("🔍 设置对话框已打开，请按照Robin Williams四大设计原则验证：")
            print("")
            print("1. 【亲密性】相关功能是否分组合理？")
            print("   - 自动保存设置是否在同一组？")
            print("   - 字体设置是否聚合？")
            print("   - 主题相关选项是否邻近？")
            print("")
            print("2. 【对齐】布局是否整齐有序？")
            print("   - 标签和输入框是否对齐？")
            print("   - Tab页面的内边距是否一致？")
            print("   - 按钮的位置是否符合习惯？")
            print("")
            print("3. 【重复】设计元素是否一致？")
            print("   - 字体、颜色、间距是否统一？")
            print("   - 输入框样式是否保持一致？")
            print("   - 分组框的外观是否规范？")
            print("")
            print("4. 【对比】重要性是否区分明显？")
            print("   - 深色模式开关是否突出？")
            print("   - 保存按钮是否明显于取消按钮？")
            print("   - 文字层次是否分明？")
            print("")
            print("5. 【整体一致性】是否与软件其他部分协调？")
            print("   - 配色是否遵循设计令牌？")
            print("   - 圆角和间距是否精确？")
            print("   - 图标和提示信息是否规范？")
            
            result = dialog.exec()
            
            if result:
                print("✅ 设置保存成功")
                print("🎉 Robin Williams设计原则优化验证完成！")
                print("")
                print("📝 优化效果总结：")
                print("• 通过分组框实现了良好的亲密性")
                print("• 统一的边距和对齐提升了视觉秩序")
                print("• 一致的样式系统强化了重复原则")
                print("• 层次化的设计增强了视觉对比")
                print("• 与项目整体设计语言保持高度一致")
            else:
                print("❌ 设置对话框被取消")
                print("💡 请关注设计优化是否达到预期效果")
                
        except Exception as e:
            print(f"❌ 显示设置对话框失败: {e}")
            import traceback
            traceback.print_exc()

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    print("🎨 Robin Williams设计原则优化验证")
    print("=" * 50)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试目标: 验证设置对话框的设计优化效果")
    print("")
    
    if not HAS_MODULES:
        print("❌ 无法导入必要模块，请检查项目环境")
        return 1
    
    window = SettingsDialogTestWindow()
    window.show()
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())