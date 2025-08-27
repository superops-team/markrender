#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Page_type颜色一致性验证脚本
验证对话框中的page_type标签颜色与列表页面保持一致
"""

import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor

try:
    from app.quickpick.edit_dialog import EditItemDialog
    from app.quickpick.item import QuickPickItemDelegate
    HAS_MODULES = True
except ImportError as e:
    print(f"⚠️  模块导入失败: {e}")
    HAS_MODULES = False

class PageTypeColorConsistencyTestWindow(QMainWindow):
    """Page_type颜色一致性测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("✅ Page_type颜色一致性验证")
        self.setGeometry(100, 100, 900, 850)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # 标题
        title = QLabel("✅ Page_type颜色一致性验证")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 需求说明
        requirement_desc = QLabel("""
        📋 用户需求：
        "弹出对话的page_type的颜色需要和列表页面对应的类型的颜色一样"
        
        🎯 一致性原则：
        • 对话框中的文件类型标签应该与列表页面中相同类型使用相同颜色
        • 确保用户在不同界面看到的文件类型颜色保持一致
        • 提升整个应用的视觉连贯性和用户体验
        
        🔧 实现方案：
        • 对话框直接引用列表页面的QuickPickItemDelegate.tag_color_map
        • 动态获取每个文件类型对应的颜色
        • 自动计算边框颜色（比背景色稍深）
        • 完全移除固定的橙色WARNING_500配色
        """)
        requirement_desc.setFont(QFont("Menlo", 11))
        requirement_desc.setStyleSheet("""
            QLabel {
                background-color: #e3f2fd;
                border: 1px solid #bbdefb;
                border-radius: 4px;
                padding: 15px;
                color: #0d47a1;
            }
        """)
        layout.addWidget(requirement_desc)
        
        if HAS_MODULES:
            # 显示颜色映射对比
            color_mapping = QLabel(self._get_color_mapping_comparison())
            color_mapping.setFont(QFont("Menlo", 10))
            color_mapping.setStyleSheet("""
                QLabel {
                    background-color: #f8f9fa;
                    border: 1px solid #dee2e6;
                    border-radius: 4px;
                    padding: 15px;
                    color: #333;
                }
            """)
            layout.addWidget(color_mapping)
            
            # 测试按钮组
            test_buttons_layout = QVBoxLayout()
            
            # 测试不同文件类型
            test_types = [
                ('markdown', 'Markdown文档测试'),
                ('board', '画板文件测试'),
                ('pdf', 'PDF文档测试'),
                ('docx', 'Word文档测试'),
                ('csv', 'CSV数据测试'),
                ('ppt', 'PowerPoint演示测试')
            ]
            
            for file_type, description in test_types:
                btn = QPushButton(f"🧪 {description}")
                btn.clicked.connect(lambda checked, ft=file_type: self.show_edit_dialog(ft))
                
                # 获取对应的颜色作为按钮颜色
                delegate = QuickPickItemDelegate()
                type_color = delegate.tag_color_map.get(file_type, delegate.default_color)
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: rgb({type_color.red()}, {type_color.green()}, {type_color.blue()});
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 10px 16px;
                        font-size: 13px;
                        font-weight: bold;
                        margin: 2px;
                    }}
                    QPushButton:hover {{
                        background-color: rgb({max(0, type_color.red()-20)}, {max(0, type_color.green()-20)}, {max(0, type_color.blue()-20)});
                    }}
                """)
                test_buttons_layout.addWidget(btn)
            
            layout.addLayout(test_buttons_layout)
        
        # 验证清单
        verification_desc = QLabel("""
        📋 验证清单 - 请检查颜色一致性：
        
        🎨 对话框与列表页面颜色对比：
        ☐ markdown类型：对话框和列表页面都应该是绿色 (34, 197, 94)
        ☐ board类型：对话框和列表页面都应该是紫色 (168, 85, 247)
        ☐ pdf类型：对话框和列表页面都应该是蓝色 (59, 130, 246)
        ☐ docx类型：对话框和列表页面都应该是蓝色 (59, 130, 246)
        ☐ csv类型：对话框和列表页面都应该是橙色 (245, 158, 11)
        ☐ ppt类型：对话框和列表页面都应该是红色 (239, 68, 68)
        
        🔍 具体验证步骤：
        ☐ 点击上方任一测试按钮打开对话框
        ☐ 观察"文件类型"标签的颜色
        ☐ 对比该颜色是否与测试按钮颜色一致
        ☐ 测试按钮颜色来自列表页面的颜色映射
        ☐ 如果一致，说明修复成功
        
        ✨ 用户体验优化：
        ☐ 用户在列表页面看到的文件类型颜色
        ☐ 在对话框中应该看到完全相同的颜色
        ☐ 这种一致性增强了界面的专业性
        ☐ 减少用户的认知负担
        
        🎯 技术实现：
        ☐ 对话框动态引用QuickPickItemDelegate.tag_color_map
        ☐ 自动将QColor转换为CSS颜色字符串
        ☐ 自动计算边框颜色（背景色-20的RGB值）
        ☐ 完全移除硬编码的橙色配色
        
        💡 设计原则验证：
        ☐ 遵循一致性原则：相同功能在不同页面使用相同颜色
        ☐ 符合用户期望：文件类型颜色应该全局统一
        ☐ 提升可用性：降低用户的学习成本
        ☐ 增强专业性：细节的一致性体现产品品质
        """)
        verification_desc.setFont(QFont("Menlo", 10))
        verification_desc.setStyleSheet("""
            QLabel {
                background-color: #fff3cd;
                border: 1px solid #ffeaa7;
                border-radius: 4px;
                padding: 15px;
                color: #856404;
            }
        """)
        layout.addWidget(verification_desc)
        
    def _get_color_mapping_comparison(self):
        """获取颜色映射对比信息"""
        if not HAS_MODULES:
            return "❌ 无法加载模块，无法显示颜色映射"
            
        delegate = QuickPickItemDelegate()
        color_info = []
        
        # 主要文件类型的颜色信息
        main_types = ['markdown', 'board', 'pdf', 'docx', 'csv', 'ppt']
        
        for file_type in main_types:
            color = delegate.tag_color_map.get(file_type, delegate.default_color)
            color_info.append(f"• {file_type.upper()}: RGB({color.red()}, {color.green()}, {color.blue()})")
        
        return f"""
        🎨 列表页面颜色映射（标准参考）：
        {chr(10).join(color_info)}
        
        🔄 修复前vs修复后对比：
        
        ❌ 修复前：
        • 对话框page_type标签：固定使用WARNING_500橙色 (#F59E0B)
        • 列表页面：根据文件类型使用不同颜色
        • 结果：同一文件类型在不同界面显示不同颜色
        
        ✅ 修复后：
        • 对话框page_type标签：动态引用列表页面的颜色映射
        • 列表页面：保持原有的颜色映射不变
        • 结果：同一文件类型在所有界面显示相同颜色
        
        🔧 技术实现细节：
        • 导入QuickPickItemDelegate类
        • 使用delegate.tag_color_map.get(page_type.lower(), delegate.default_color)
        • 将QColor转换为CSS rgb()格式
        • 自动生成边框颜色（RGB值各减20）
        
        ✨ 一致性原则体现：
        • markdown → 绿色 (所有界面)
        • board → 紫色 (所有界面)
        • pdf/docx → 蓝色 (所有界面)
        • csv → 橙色 (所有界面)
        • ppt → 红色 (所有界面)
        """
        
    def show_edit_dialog(self, file_type='markdown'):
        """显示编辑对话框"""
        try:
            # 创建不同文件类型的测试数据
            test_data = {
                'id': 1,
                'title': f'{file_type.upper()}文件颜色一致性测试',
                'tags': f'{file_type}, 颜色测试, 一致性验证',
                'page_type': file_type,
                'created_at': datetime(2024, 1, 15, 10, 30, 0),
                'updated_at': datetime(2024, 1, 20, 15, 45, 30),
                'file_size': 2048,
                'content_md5': 'a1b2c3d4e5f6g7h8i9j0'
            }
            
            # 获取该文件类型在列表页面的颜色
            delegate = QuickPickItemDelegate()
            expected_color = delegate.tag_color_map.get(file_type, delegate.default_color)
            
            # 创建并显示对话框
            dialog = EditItemDialog(test_data, self)
            
            print(f"🔍 {file_type.upper()}类型对话框已打开，请验证颜色一致性：")
            print("")
            print(f"📊 预期颜色（列表页面标准）：")
            print(f"   RGB({expected_color.red()}, {expected_color.green()}, {expected_color.blue()})")
            print("")
            print(f"🔍 验证要点：")
            print(f"   1. 观察对话框中'文件类型'标签的颜色")
            print(f"   2. 该颜色应该与测试按钮的颜色完全一致")
            print(f"   3. 测试按钮的颜色来自列表页面的颜色映射")
            print(f"   4. 如果颜色一致，说明修复成功")
            print("")
            print(f"✨ 用户体验提升：")
            print(f"   - 用户看到的{file_type}类型颜色在所有界面保持一致")
            print(f"   - 减少认知负担，提升界面专业性")
            
            result = dialog.exec()
            
            if result:
                print("✅ 对话框正常保存并关闭")
                print(f"最终标题: {dialog.get_new_title()}")
                print(f"最终标签: {dialog.get_new_tags()}")
                print(f"🎉 {file_type.upper()}类型颜色一致性验证完成！")
                print("")
                print("📝 请确认颜色一致性：")
                print(f"   - 对话框page_type标签颜色")
                print(f"   - 应该与列表页面{file_type}类型颜色完全一致")
                print(f"   - RGB({expected_color.red()}, {expected_color.green()}, {expected_color.blue()})")
            else:
                print("❌ 对话框被取消")
                print("💡 请确认取消前是否观察到颜色一致性效果")
                
        except Exception as e:
            print(f"❌ 显示对话框失败: {e}")
            import traceback
            traceback.print_exc()

def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    window = PageTypeColorConsistencyTestWindow()
    window.show()
    
    print("✅ Page_type颜色一致性验证已启动")
    print("🎨 对话框page_type标签现在使用与列表页面相同的颜色映射")
    print("🔍 请点击不同的文件类型测试按钮，验证颜色一致性")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()