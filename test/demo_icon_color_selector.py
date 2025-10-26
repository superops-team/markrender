#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图标和颜色选择器功能演示
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout, QFrame

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.quickpick.icon_selector import IconSelectorWidget
from app.quickpick.color_selector import ColorSelectorWidget

class DemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("图标和颜色选择器功能演示")
        self.setGeometry(100, 100, 600, 500)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 标题
        title_label = QLabel("图标和颜色选择器功能演示")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)
        
        # 说明文本
        description = QLabel("使用下方的控件选择图标和颜色，预览效果将实时显示")
        description.setStyleSheet("font-size: 14px; margin: 10px;")
        layout.addWidget(description)
        
        # 创建预览区域
        preview_frame = QFrame()
        preview_frame.setStyleSheet("""
            QFrame {
                border: 2px dashed #cccccc;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
            }
        """)
        preview_layout = QVBoxLayout(preview_frame)
        
        self.preview_label = QLabel("图标预览区域")
        self.preview_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                min-height: 100px;
                border: 1px solid #eeeeee;
                border-radius: 5px;
                padding: 20px;
            }
        """)
        preview_layout.addWidget(self.preview_label)
        
        layout.addWidget(preview_frame)
        
        # 创建控制面板
        control_panel = QFrame()
        control_panel.setStyleSheet("""
            QFrame {
                border: 1px solid #dddddd;
                border-radius: 8px;
                padding: 15px;
                margin: 10px;
            }
        """)
        control_layout = QVBoxLayout(control_panel)
        
        # 图标选择器
        icon_layout = QHBoxLayout()
        icon_label = QLabel("选择图标:")
        icon_label.setFixedWidth(80)
        self.icon_selector = IconSelectorWidget()
        self.icon_selector.icon_changed.connect(self.update_preview)
        icon_layout.addWidget(icon_label)
        icon_layout.addWidget(self.icon_selector)
        control_layout.addLayout(icon_layout)
        
        # 颜色选择器
        color_layout = QHBoxLayout()
        color_label = QLabel("选择颜色:")
        color_label.setFixedWidth(80)
        self.color_selector = ColorSelectorWidget()
        self.color_selector.color_changed.connect(self.update_preview)
        color_layout.addWidget(color_label)
        color_layout.addWidget(self.color_selector)
        control_layout.addLayout(color_layout)
        
        layout.addWidget(control_panel)
        
        # 状态显示
        self.status_label = QLabel("状态: 等待选择")
        self.status_label.setStyleSheet("font-size: 14px; color: #666666; margin: 10px;")
        layout.addWidget(self.status_label)
        
        # 初始化预览
        self.update_preview()
        
    def update_preview(self):
        """更新预览显示"""
        selected_icon = self.icon_selector.get_selected_icon()
        selected_color = self.color_selector.get_selected_color()
        
        # 构建状态信息
        status_text = []
        if selected_icon:
            status_text.append(f"图标: {selected_icon}")
        else:
            status_text.append("图标: 未选择")
            
        if selected_color:
            status_text.append(f"颜色: {selected_color}")
        else:
            status_text.append("颜色: 未选择")
            
        self.status_label.setText(f"状态: {', '.join(status_text)}")
        
        # 更新预览显示
        if selected_icon and selected_color:
            self.preview_label.setText(f"图标: {selected_icon}\n颜色: {selected_color}")
            self.preview_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 16px;
                    min-height: 100px;
                    border: 2px solid {selected_color};
                    border-radius: 5px;
                    padding: 20px;
                    background-color: #ffffff;
                    color: {selected_color};
                    font-weight: bold;
                }}
            """)
        elif selected_icon:
            self.preview_label.setText(f"图标: {selected_icon}\n颜色: 未选择")
            self.preview_label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    min-height: 100px;
                    border: 1px solid #cccccc;
                    border-radius: 5px;
                    padding: 20px;
                    background-color: #ffffff;
                }
            """)
        elif selected_color:
            self.preview_label.setText(f"图标: 未选择\n颜色: {selected_color}")
            self.preview_label.setStyleSheet(f"""
                QLabel {{
                    font-size: 16px;
                    min-height: 100px;
                    border: 2px solid {selected_color};
                    border-radius: 5px;
                    padding: 20px;
                    background-color: #ffffff;
                    color: {selected_color};
                }}
            """)
        else:
            self.preview_label.setText("请选择图标和颜色")
            self.preview_label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    min-height: 100px;
                    border: 1px solid #eeeeee;
                    border-radius: 5px;
                    padding: 20px;
                    background-color: #f9f9f9;
                    color: #999999;
                }
            """)

def main():
    app = QApplication(sys.argv)
    
    window = DemoWindow()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())

if __name__ == "__main__":
    main()