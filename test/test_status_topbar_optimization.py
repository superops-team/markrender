#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Status Bar 和 Top Bar 样式优化验证测试

此测试验证以下优化内容：
1. Status Bar 样式统一和功能增强
2. Top Bar 工具按钮样式规范化
3. 设计令牌系统的一致性应用
4. 对齐、间距和视觉层次的改进
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PySide6.QtCore import QTimer, Qt

from app.statusbar.status_bar import StatusBar
from app.topbar.button_controller import ButtonController
from db.markdown_manager import MarkdownManager


class StatusTopBarTestWindow(QMainWindow):
    """Status Bar 和 Top Bar 测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_test_data()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("Status Bar & Top Bar 样式优化测试")
        self.setGeometry(100, 100, 900, 600)
        
        # 创建中央组件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 创建模拟的markdown editor
        self.markdown_editor = self.create_mock_editor()
        
        # 创建模拟的history panel
        self.history_panel = QWidget()
        self.history_panel.setFixedWidth(200)
        self.history_panel.setStyleSheet("background-color: #f8f9fa; border: 1px solid #e9ecef;")
        
        try:
            # 创建MarkdownManager实例（用于ButtonController）
            self.markdown_manager = MarkdownManager()
            
            # 创建TopBar（ButtonController）
            self.top_bar = ButtonController(self, self.history_panel, self.markdown_editor)
            self.top_bar.setStyleSheet("""
                QWidget {
                    background-color: #ffffff;
                    border-bottom: 1px solid #e9ecef;
                }
            """)
            
            # 创建主内容区域
            content_widget = QWidget()
            content_layout = QHBoxLayout(content_widget)
            content_layout.setContentsMargins(0, 0, 0, 0)
            content_layout.addWidget(self.history_panel)
            content_layout.addWidget(self.markdown_editor)
            
            # 添加组件到主布局
            layout.addWidget(self.top_bar)
            layout.addWidget(content_widget)
            
            # 创建StatusBar
            self.status_bar = StatusBar(self)
            self.setStatusBar(self.status_bar)
            
        except Exception as e:
            print(f"初始化组件失败: {e}")
            # 创建简化版本用于测试
            self.create_fallback_components(layout)
        
    def create_mock_editor(self):
        """创建模拟的markdown编辑器"""
        editor = QWidget()
        editor.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border: 1px solid #e9ecef;
                padding: 20px;
            }
        """)
        
        # 添加模拟的export_file方法
        def mock_export(format_type):
            print(f"模拟导出为 {format_type.upper()} 格式")
            
        editor.export_file = mock_export
        return editor
        
    def create_fallback_components(self, layout):
        """创建备用组件用于测试"""
        # 简化的top bar
        top_bar = QWidget()
        top_bar.setFixedHeight(36)
        top_bar.setStyleSheet("background-color: #ffffff; border-bottom: 1px solid #e9ecef;")
        
        # 简化的content
        content = QWidget()
        content.setStyleSheet("background-color: #f8f9fa;")
        
        layout.addWidget(top_bar)
        layout.addWidget(content)
        
        # 创建简化的status bar
        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)
        
    def setup_test_data(self):
        """设置测试数据"""
        QTimer.singleShot(500, self.run_status_tests)
        
    def run_status_tests(self):
        """运行状态栏测试"""
        print("🚀 开始 Status Bar & Top Bar 样式优化测试...")
        
        # 测试状态栏信息更新
        test_cases = [
            ("小文件", 256, 50, "markdown"),
            ("中等文件", 1024 * 5, 800, "board"),
            ("大文件", 1024 * 1024 * 2, 50000, "html"),
            ("超大文件", 1024 * 1024 * 10, 500000, "pdf")
        ]
        
        for i, (name, size, words, doc_type) in enumerate(test_cases):
            QTimer.singleShot(1000 * (i + 1), 
                            lambda n=name, s=size, w=words, t=doc_type: self.test_status_update(n, s, w, t))
        
        # 测试状态消息
        QTimer.singleShot(6000, lambda: self.status_bar.show_message("正在保存文档...", 2000))
        QTimer.singleShot(8000, lambda: self.status_bar.show_message("保存成功！", 2000))
        QTimer.singleShot(10000, lambda: self.status_bar.set_ready_status())
        
        # 显示测试指导
        QTimer.singleShot(1500, self.show_test_guide)
        
    def test_status_update(self, name, size, words, doc_type):
        """测试状态更新"""
        print(f"📊 测试 {name}: {size} bytes, {words} 字, 类型: {doc_type}")
        self.status_bar.update_file_info(name, size, words, doc_type)
        
    def show_test_guide(self):
        """显示测试指导"""
        from PySide6.QtWidgets import QMessageBox
        
        msg = QMessageBox(self)
        msg.setWindowTitle("测试指导")
        msg.setIcon(QMessageBox.Information)
        msg.setText("Status Bar & Top Bar 样式优化验证")
        msg.setInformativeText("""
🎯 测试内容：

✅ Status Bar 优化验证：
• 统一的设计令牌应用
• 改进的状态信息显示（文件大小、字数、类型）
• 智能的单位换算（B/KB/MB, K/M）
• 悬停交互效果
• 状态消息提示

✅ Top Bar 优化验证：
• 工具按钮样式统一
• 规范的间距和对齐
• 导出菜单样式改进
• 按钮状态反馈
• 固定尺寸确保一致性

📋 验证要点：
• 颜色系统：统一的中性色和主题色
• 间距系统：4px/8px 的规范间距
• 字体系统：12px 的统一字体大小
• 圆角系统：4px 的统一圆角
• 交互反馈：悬停和按下状态

🔧 设计改进：
• 更好的视觉层次
• 一致的交互体验
• 企业级的专业外观
• 符合设计原则的布局
        """)
        msg.exec()


def main():
    """主函数"""
    print("🚀 启动 Status Bar & Top Bar 样式优化测试...")
    
    app = QApplication(sys.argv)
    app.setApplicationName("StatusTopBarTest")
    
    # 创建测试窗口
    window = StatusTopBarTestWindow()
    window.show()
    
    print("✨ 测试窗口已启动")
    print("📌 请观察 Status Bar 和 Top Bar 的样式效果")
    print("🔍 检查设计令牌系统的一致性应用")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()