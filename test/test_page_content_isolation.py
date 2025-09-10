#!/usr/bin/env python3
"""
测试页面内容隔离和正确切换
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

class PageContentIsolationTest(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("页面内容隔离测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建编辑器
        self.editor = MarkRenderEditor()
        
        # 存储页面内容状态
        self.page_contents = {}
        
        # 创建UI
        self.setup_ui()
        
        # 延迟初始化
        QTimer.singleShot(100, self.init_test)
    
    def setup_ui(self):
        """创建UI"""
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # 说明标签
        info_label = QLabel("测试页面内容隔离和正确切换")
        layout.addWidget(info_label)
        
        # 测试按钮
        test_btn1 = QPushButton("1. 设置Markdown页面内容")
        test_btn1.clicked.connect(lambda: self.set_page_content("markdown", "# Markdown内容\n\n这是Markdown页面的内容"))
        layout.addWidget(test_btn1)
        
        test_btn2 = QPushButton("2. 设置Excalidraw页面内容")
        test_btn2.clicked.connect(lambda: self.set_page_content("excalidraw", '{"elements":[{"id":"rect1","type":"rectangle","x":100,"y":100,"width":200,"height":100}],"appState":{}}'))
        layout.addWidget(test_btn2)
        
        test_btn3 = QPushButton("3. 切换到Markdown页面")
        test_btn3.clicked.connect(lambda: self.switch_to_page("markdown"))
        layout.addWidget(test_btn3)
        
        test_btn4 = QPushButton("4. 切换到Excalidraw页面")
        test_btn4.clicked.connect(lambda: self.switch_to_page("excalidraw"))
        layout.addWidget(test_btn4)
        
        test_btn5 = QPushButton("5. 检查页面内容隔离")
        test_btn5.clicked.connect(self.check_content_isolation)
        layout.addWidget(test_btn5)
        
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
    
    def set_page_content(self, page_type, content):
        """设置页面内容"""
        self.log_message(f"📝 设置{page_type}页面内容...")
        self.page_contents[page_type] = content
        self.log_message(f"✅ {page_type}页面内容已保存: {content[:50]}{'...' if len(content) > 50 else ''}")
    
    def switch_to_page(self, page_type):
        """切换到指定页面"""
        self.log_message(f"🔀 切换到{page_type}页面...")
        
        # 模拟quickpick_item
        quickpick_item = {
            'id': f'test_{page_type}_item',
            'title': f'测试{page_type}项目',
            'content': self.page_contents.get(page_type, ''),
            'page_type': page_type
        }
        
        # 使用编辑器的切换方法
        self.editor.switch_to_page_with_save(page_type, quickpick_item)
        self.log_message(f"✅ 切换到{page_type}页面请求已发送")
    
    def check_content_isolation(self):
        """检查页面内容隔离"""
        self.log_message("🔍 检查页面内容隔离...")
        for page_type, content in self.page_contents.items():
            self.log_message(f"  {page_type}: {content[:50]}{'...' if len(content) > 50 else ''}")
        self.log_message("✅ 页面内容隔离检查完成")

def main():
    app = QApplication(sys.argv)
    window = PageContentIsolationTest()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()