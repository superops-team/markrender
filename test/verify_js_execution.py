#!/usr/bin/env python3
"""
验证直接JavaScript执行的完整测试
"""

import sys
import os
import json
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QHBoxLayout
from PySide6.QtCore import QTimer, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage

from app.editor.backend_interface import BackendInterface
from app.editor.js_scripts import JSScriptManager
from utils import logger

class JSExecutionTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JavaScript执行验证测试")
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建通信管理器
        self.backend = BackendInterface("markdown")
        
        # 创建UI
        self.setup_ui()
        
        # 延迟创建页面
        QTimer.singleShot(100, self.create_page)
    
    def setup_ui(self):
        """设置UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 创建Web视图
        self.web_view = QWebEngineView()
        
        # 控制按钮区域
        controls_layout = QHBoxLayout()
        
        # Markdown测试按钮
        self.test_markdown_btn = QPushButton("测试Markdown设置内容")
        self.test_markdown_btn.clicked.connect(self.test_markdown_set_content)
        
        self.get_markdown_btn = QPushButton("测试Markdown获取内容")
        self.get_markdown_btn.clicked.connect(self.test_markdown_get_content)
        
        # Excalidraw测试按钮
        self.test_excalidraw_btn = QPushButton("测试Excalidraw设置内容")
        self.test_excalidraw_btn.clicked.connect(self.test_excalidraw_set_content)
        
        self.get_excalidraw_btn = QPushButton("测试Excalidraw获取内容")
        self.get_excalidraw_btn.clicked.connect(self.test_excalidraw_get_content)
        
        # 通用测试按钮
        self.test_js_btn = QPushButton("测试通用JS执行")
        self.test_js_btn.clicked.connect(self.test_generic_js)
        
        self.list_scripts_btn = QPushButton("列出可用脚本")
        self.list_scripts_btn.clicked.connect(self.list_scripts)
        
        # 添加按钮到布局
        controls_layout.addWidget(self.test_markdown_btn)
        controls_layout.addWidget(self.get_markdown_btn)
        controls_layout.addWidget(self.test_excalidraw_btn)
        controls_layout.addWidget(self.get_excalidraw_btn)
        controls_layout.addWidget(self.test_js_btn)
        controls_layout.addWidget(self.list_scripts_btn)
        
        # 日志输出
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        
        # 添加控件到主布局
        main_layout.addWidget(self.web_view, stretch=3)
        main_layout.addLayout(controls_layout)
        main_layout.addWidget(self.log_output, stretch=1)
    
    def log_message(self, message):
        """记录消息到日志输出"""
        self.log_output.append(message)
        print(f"[JS-TEST] {message}")
    
    def create_page(self):
        """创建页面"""
        try:
            # 设置页面
            page = QWebEnginePage(self.web_view)
            self.web_view.setPage(page)
            
            # 设置后端接口
            self.backend.set_page(page)
            
            # 加载HTML文件
            html_path = os.path.abspath("app/editor/plugins/markdown/index.html")
            if os.path.exists(html_path):
                self.web_view.load(QUrl.fromLocalFile(html_path))
                self.web_view.loadFinished.connect(self.on_page_loaded)
                self.log_message(f"加载页面: {html_path}")
            else:
                self.log_message(f"页面文件不存在: {html_path}")
                
        except Exception as e:
            self.log_message(f"创建页面时出错: {e}")
            import traceback
            self.log_message(f"详细错误: {traceback.format_exc()}")
    
    def on_page_loaded(self, success):
        """页面加载完成"""
        if success:
            self.log_message("✅ 页面加载成功")
            # 启用所有测试按钮
            self.test_markdown_btn.setEnabled(True)
            self.get_markdown_btn.setEnabled(True)
            self.test_excalidraw_btn.setEnabled(True)
            self.get_excalidraw_btn.setEnabled(True)
            self.test_js_btn.setEnabled(True)
            self.list_scripts_btn.setEnabled(True)
        else:
            self.log_message("❌ 页面加载失败")
            # 禁用所有测试按钮
            self.test_markdown_btn.setEnabled(False)
            self.get_markdown_btn.setEnabled(False)
            self.test_excalidraw_btn.setEnabled(False)
            self.get_excalidraw_btn.setEnabled(False)
            self.test_js_btn.setEnabled(False)
            self.list_scripts_btn.setEnabled(False)
    
    def test_markdown_set_content(self):
        """测试Markdown设置内容"""
        self.log_message("测试Markdown设置内容...")
        
        test_content = "# Markdown JavaScript执行测试\n\n这是通过直接执行JavaScript设置的Markdown内容！\n\n- 列表项1\n- 列表项2\n\n**粗体文本**"
        
        # 使用新的send_message方法
        success = self.backend.send_message("setValue", {"content": test_content})
        
        if success:
            self.log_message("✅ Markdown内容设置成功")
        else:
            self.log_message("❌ Markdown内容设置失败")
    
    def test_markdown_get_content(self):
        """测试Markdown获取内容"""
        self.log_message("测试Markdown获取内容...")
        
        def handle_content(content):
            self.log_message(f"获取到的Markdown内容: {content[:100]}...")
            if content:
                self.log_message("✅ Markdown内容获取成功")
            else:
                self.log_message("⚠️  Markdown内容获取成功但为空")
        
        # 使用新的send_message方法获取内容
        success = self.backend.send_message("getContent", {}, handle_content)
        
        if success:
            self.log_message("✅ Markdown内容获取请求已发送")
        else:
            self.log_message("❌ Markdown内容获取请求发送失败")
    
    def test_excalidraw_set_content(self):
        """测试Excalidraw设置内容"""
        self.log_message("测试Excalidraw设置内容...")
        
        # 模拟Excalidraw数据
        test_content = json.dumps([
            {
                "id": "test-1",
                "type": "rectangle",
                "x": 100,
                "y": 100,
                "width": 200,
                "height": 100,
                "strokeColor": "#000000"
            },
            {
                "id": "test-2", 
                "type": "text",
                "x": 150,
                "y": 150,
                "text": "测试文本",
                "strokeColor": "#FF0000"
            }
        ])
        
        # 使用新的send_message方法
        success = self.backend.send_message("setValue", {"content": test_content})
        
        if success:
            self.log_message("✅ Excalidraw内容设置成功")
        else:
            self.log_message("❌ Excalidraw内容设置失败")
    
    def test_excalidraw_get_content(self):
        """测试Excalidraw获取内容"""
        self.log_message("测试Excalidraw获取内容...")
        
        def handle_content(content):
            self.log_message(f"获取到的Excalidraw内容: {content[:100]}...")
            if content:
                self.log_message("✅ Excalidraw内容获取成功")
            else:
                self.log_message("⚠️  Excalidraw内容获取成功但为空")
        
        # 使用新的send_message方法获取内容
        success = self.backend.send_message("getContent", {}, handle_content)
        
        if success:
            self.log_message("✅ Excalidraw内容获取请求已发送")
        else:
            self.log_message("❌ Excalidraw内容获取请求发送失败")
    
    def test_generic_js(self):
        """测试通用JS执行"""
        self.log_message("测试通用JS执行...")
        
        # 构造一个简单的JavaScript代码来测试执行
        js_code = """
        (function() {
            console.log('通用JS执行测试');
            return 'JS执行成功';
        })();
        """
        
        def handle_result(result):
            self.log_message(f"通用JS执行结果: {result}")
            if result == 'JS执行成功':
                self.log_message("✅ 通用JS执行成功")
            else:
                self.log_message("⚠️  通用JS执行完成但返回值不符合预期")
        
        try:
            self.backend.page.runJavaScript(js_code, handle_result)
            self.log_message("✅ 通用JS执行请求已发送")
        except Exception as e:
            self.log_message(f"❌ 通用JS执行请求发送失败: {e}")
    
    def list_scripts(self):
        """列出可用脚本"""
        self.log_message("可用的JS脚本:")
        scripts = JSScriptManager.list_scripts()
        for script in scripts:
            self.log_message(f"  - {script}")
        self.log_message(f"总计: {len(scripts)} 个脚本")

def main():
    """主函数"""
    print("启动JavaScript执行验证测试...")
    
    app = QApplication(sys.argv)
    window = JSExecutionTestWindow()
    
    # 初始禁用所有测试按钮
    window.test_markdown_btn.setEnabled(False)
    window.get_markdown_btn.setEnabled(False)
    window.test_excalidraw_btn.setEnabled(False)
    window.get_excalidraw_btn.setEnabled(False)
    window.test_js_btn.setEnabled(False)
    window.list_scripts_btn.setEnabled(False)
    
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()