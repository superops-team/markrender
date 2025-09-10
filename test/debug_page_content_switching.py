#!/usr/bin/env python3
"""
调试页面内容切换问题
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLabel
from PySide6.QtCore import QTimer
from app.quickpick.panel import QuickPickPanel
from db.markrender_manager import MarkRenderManager
from utils import logger

class DebugPageContentSwitching(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("调试页面内容切换")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建数据库管理器
        self.markrender_manager = MarkRenderManager()
        
        # 创建QuickPick面板
        self.quickpick_panel = QuickPickPanel(self.markrender_manager, self)
        
        # 设置当前项
        self.current_item = None
        
        # 创建UI
        self.setup_ui()
        
        # 延迟初始化
        QTimer.singleShot(100, self.init_test)
    
    def setup_ui(self):
        """创建UI"""
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # 说明标签
        info_label = QLabel("调试页面内容切换问题")
        layout.addWidget(info_label)
        
        # 测试按钮
        test_btn1 = QPushButton("1. 加载测试数据")
        test_btn1.clicked.connect(self.load_test_data)
        layout.addWidget(test_btn1)
        
        test_btn2 = QPushButton("2. 显示第一个项目内容")
        test_btn2.clicked.connect(self.show_first_item)
        layout.addWidget(test_btn2)
        
        test_btn3 = QPushButton("3. 显示第二个项目内容")
        test_btn3.clicked.connect(self.show_second_item)
        layout.addWidget(test_btn3)
        
        test_btn4 = QPushButton("4. 显示第三个项目内容")
        test_btn4.clicked.connect(self.show_third_item)
        layout.addWidget(test_btn4)
        
        # 日志区域
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        layout.addWidget(self.log_text)
        
        # QuickPick面板
        layout.addWidget(self.quickpick_panel)
        
        self.setCentralWidget(central_widget)
        
        # 连接信号
        self.quickpick_panel.quickpick_item_selected.connect(self.on_item_selected)
    
    def log_message(self, message):
        """记录日志"""
        self.log_text.append(message)
        logger.info(message)
    
    def init_test(self):
        """初始化测试"""
        self.log_message("🔧 初始化测试...")
    
    def load_test_data(self):
        """加载测试数据"""
        self.log_message("📂 加载测试数据...")
        self.quickpick_panel.load_quickpick_items()
        self.log_message(f"✅ 加载完成，共有 {self.quickpick_panel.quickpick_list.count()} 个项目")
    
    def show_first_item(self):
        """显示第一个项目"""
        self.log_message("1️⃣ 显示第一个项目...")
        if self.quickpick_panel.quickpick_list.count() > 0:
            index = self.quickpick_panel.quickpick_list.model().index(0, 0)
            self.quickpick_panel.on_item_clicked(index)
        else:
            self.log_message("❌ 没有项目可显示")
    
    def show_second_item(self):
        """显示第二个项目"""
        self.log_message("2️⃣ 显示第二个项目...")
        if self.quickpick_panel.quickpick_list.count() > 1:
            index = self.quickpick_panel.quickpick_list.model().index(1, 0)
            self.quickpick_panel.on_item_clicked(index)
        else:
            self.log_message("❌ 没有足够的项目")
    
    def show_third_item(self):
        """显示第三个项目"""
        self.log_message("3️⃣ 显示第三个项目...")
        if self.quickpick_panel.quickpick_list.count() > 2:
            index = self.quickpick_panel.quickpick_list.model().index(2, 0)
            self.quickpick_panel.on_item_clicked(index)
        else:
            self.log_message("❌ 没有足够的项目")
    
    def on_item_selected(self, quickpick_item):
        """处理项目选择事件"""
        self.log_message(f"🎯 项目已选择: {quickpick_item.get('title')}")
        self.log_message(f"📄 页面类型: {quickpick_item.get('page_type')}")
        content = quickpick_item.get('content', '')
        self.log_message(f"📝 内容预览: {content[:100]}{'...' if len(content) > 100 else ''}")
        self.log_message(f"📏 内容长度: {len(content)}")
        
        self.current_item = quickpick_item
        
        # 模拟更新编辑器和预览器
        self.update_editor_and_previewer(quickpick_item)
    
    def update_editor_and_previewer(self, quickpick_item):
        """模拟更新编辑区和预览区内容"""
        self.log_message(f"🔄 模拟更新编辑器内容: {quickpick_item.get('title')}")

def main():
    app = QApplication(sys.argv)
    window = DebugPageContentSwitching()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()