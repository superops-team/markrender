#!/usr/bin/env python3
"""
测试页面切换时的空内容处理功能
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit
from PySide6.QtCore import QTimer
from app.editor.webengine import WebPageManager, PageType
from app.editor.backend_interface import BackendInterface
from app.editor.excalidraw_utils import ExcalidrawDataHandler
from utils import logger

class PageSwitchingTest(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("页面切换空内容处理测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建页面管理器和通信管理器
        self.page_manager = WebPageManager()
        self.markdown_comm = BackendInterface("markdown")
        self.excalidraw_comm = BackendInterface("excalidraw")
        
        # 创建UI
        self.setup_ui()
        
        # 延迟创建页面
        QTimer.singleShot(100, self.create_pages)
    
    def setup_ui(self):
        """创建UI"""
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # 测试按钮
        test_markdown_btn = QPushButton("测试Markdown空内容")
        test_markdown_btn.clicked.connect(self.test_markdown_empty_content)
        layout.addWidget(test_markdown_btn)
        
        test_excalidraw_btn = QPushButton("测试Excalidraw空内容")
        test_excalidraw_btn.clicked.connect(self.test_excalidraw_empty_content)
        layout.addWidget(test_excalidraw_btn)
        
        switch_to_markdown_btn = QPushButton("切换到Markdown页面")
        switch_to_markdown_btn.clicked.connect(self.switch_to_markdown)
        layout.addWidget(switch_to_markdown_btn)
        
        switch_to_excalidraw_btn = QPushButton("切换到Excalidraw页面")
        switch_to_excalidraw_btn.clicked.connect(self.switch_to_excalidraw)
        layout.addWidget(switch_to_excalidraw_btn)
        
        # 日志区域
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        layout.addWidget(self.log_text)
        
        # 页面管理器
        layout.addWidget(self.page_manager)
        
        self.setCentralWidget(central_widget)
    
    def log_message(self, message):
        """记录日志"""
        self.log_text.append(message)
        logger.info(message)
    
    def create_pages(self):
        """创建页面"""
        self.log_message("🔧 创建测试页面...")
        
        # 创建Markdown页面
        markdown_page = self.page_manager.get_or_create_page(PageType.MARKDOWN, self.markdown_comm)
        if markdown_page:
            self.markdown_comm.set_page(markdown_page.view.page())
            self.log_message("✅ Markdown页面创建并绑定成功")
            
        # 创建Excalidraw页面
        excalidraw_page = self.page_manager.get_or_create_page(PageType.EXCALIDRAW, self.excalidraw_comm)
        if excalidraw_page:
            self.excalidraw_comm.set_page(excalidraw_page.view.page())
            self.log_message("✅ Excalidraw页面创建并绑定成功")
    
    def test_markdown_empty_content(self):
        """测试Markdown空内容处理"""
        self.log_message("📝 测试Markdown空内容处理...")
        
        # 模拟从数据库获取的空内容
        empty_content = ""
        self.log_message(f"模拟空内容: '{empty_content}'")
        
        # 设置内容到Markdown页面
        if self.markdown_comm.ready:
            success = self.markdown_comm.send_message('setValue', {
                'content': empty_content
            })
            self.log_message("✅ 空内容发送成功" if success else "❌ 空内容发送失败")
        else:
            self.log_message("⏳ WebChannel未就绪，延迟发送空内容")
            self.markdown_comm.initial_content = empty_content
    
    def test_excalidraw_empty_content(self):
        """测试Excalidraw空内容处理"""
        self.log_message("🎨 测试Excalidraw空内容处理...")
        
        # 模拟从数据库获取的空内容
        empty_content = ""
        self.log_message(f"模拟空内容: '{empty_content}'")
        
        # 发送空数据重置面板
        if self.excalidraw_comm.ready:
            success = self.excalidraw_comm.send_message('loadExcalidrawData', {
                'boardId': 'test_board',
                'drawingData': '{}'  # 发送空的JSON对象以重置面板
            })
            self.log_message("✅ 空Excalidraw数据发送成功" if success else "❌ 空Excalidraw数据发送失败")
        else:
            self.log_message("⏳ WebChannel未就绪，延迟发送空Excalidraw数据")
    
    def switch_to_markdown(self):
        """切换到Markdown页面"""
        self.log_message("➡️ 切换到Markdown页面...")
        success = self.page_manager.switch_to_page(PageType.MARKDOWN)
        self.log_message("✅ 切换成功" if success else "❌ 切换失败")
    
    def switch_to_excalidraw(self):
        """切换到Excalidraw页面"""
        self.log_message("➡️ 切换到Excalidraw页面...")
        success = self.page_manager.switch_to_page(PageType.EXCALIDRAW)
        self.log_message("✅ 切换成功" if success else "❌ 切换失败")

def main():
    app = QApplication(sys.argv)
    window = PageSwitchingTest()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()