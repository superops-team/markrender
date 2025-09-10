#!/usr/bin/env python3
"""
测试页面切换时先保存再加载的逻辑
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLabel
from PySide6.QtCore import QTimer
from app.editor.editor import MarkRenderEditor
from utils import logger

class PageSwitchingWithSaveTest(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("页面切换保存测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建编辑器
        self.editor = MarkRenderEditor()
        
        # 创建UI
        self.setup_ui()
        
        # 延迟初始化
        QTimer.singleShot(100, self.init_test)
    
    def setup_ui(self):
        """创建UI"""
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # 说明标签
        info_label = QLabel("测试页面切换时先保存再加载的逻辑")
        layout.addWidget(info_label)
        
        # 测试按钮
        test_btn1 = QPushButton("测试Markdown页面切换")
        test_btn1.clicked.connect(self.test_markdown_switch)
        layout.addWidget(test_btn1)
        
        test_btn2 = QPushButton("测试Excalidraw页面切换")
        test_btn2.clicked.connect(self.test_excalidraw_switch)
        layout.addWidget(test_btn2)
        
        test_btn3 = QPushButton("测试Landing页面切换")
        test_btn3.clicked.connect(self.test_landing_switch)
        layout.addWidget(test_btn3)
        
        # 日志区域
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        layout.addWidget(self.log_text)
        
        # 编辑器
        layout.addWidget(self.editor)
        
        self.setCentralWidget(central_widget)
    
    def log_message(self, message):
        """记录日志"""
        self.log_text.append(message)
        logger.info(message)
    
    def init_test(self):
        """初始化测试"""
        self.log_message("🔧 初始化测试...")
    
    def test_markdown_switch(self):
        """测试Markdown页面切换"""
        self.log_message("📝 测试Markdown页面切换...")
        
        # 模拟一个quickpick_item
        quickpick_item = {
            'id': 'test_markdown_1',
            'title': '测试Markdown文档',
            'content': '# 测试标题\n\n这是测试内容',
            'page_type': 'markdown'
        }
        
        # 使用新的切换方法
        self.editor.switch_to_page_with_save("markdown", quickpick_item)
        self.log_message("✅ Markdown页面切换请求已发送")
    
    def test_excalidraw_switch(self):
        """测试Excalidraw页面切换"""
        self.log_message("🎨 测试Excalidraw页面切换...")
        
        # 模拟一个quickpick_item
        quickpick_item = {
            'id': 'test_excalidraw_1',
            'title': '测试画板',
            'content': '{"elements":[],"appState":{}}',
            'page_type': 'excalidraw'
        }
        
        # 使用新的切换方法
        self.editor.switch_to_page_with_save("excalidraw", quickpick_item)
        self.log_message("✅ Excalidraw页面切换请求已发送")
    
    def test_landing_switch(self):
        """测试Landing页面切换"""
        self.log_message("🏠 测试Landing页面切换...")
        
        # 模拟一个quickpick_item
        quickpick_item = {
            'id': 'landing_default',
            'title': '欢迎页面',
            'content': '',
            'page_type': 'landing'
        }
        
        # 使用新的切换方法
        self.editor.switch_to_page_with_save("landing", quickpick_item)
        self.log_message("✅ Landing页面切换请求已发送")

def main():
    app = QApplication(sys.argv)
    window = PageSwitchingWithSaveTest()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()