#!/usr/bin/env python3
"""
调试JavaScript执行错误的测试脚本
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

class JSDebugWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JavaScript错误调试工具")
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
        
        # 测试按钮
        self.test_basic_js_btn = QPushButton("测试基本JS执行")
        self.test_basic_js_btn.clicked.connect(self.test_basic_js)
        
        self.test_error_js_btn = QPushButton("测试错误JS执行")
        self.test_error_js_btn.clicked.connect(self.test_error_js)
        
        self.test_script_manager_btn = QPushButton("测试脚本管理器")
        self.test_script_manager_btn.clicked.connect(self.test_script_manager)
        
        self.clear_log_btn = QPushButton("清空日志")
        self.clear_log_btn.clicked.connect(self.clear_log)
        
        # 添加按钮到布局
        controls_layout.addWidget(self.test_basic_js_btn)
        controls_layout.addWidget(self.test_error_js_btn)
        controls_layout.addWidget(self.test_script_manager_btn)
        controls_layout.addWidget(self.clear_log_btn)
        
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
        print(f"[JS-DEBUG] {message}")
    
    def clear_log(self):
        """清空日志"""
        self.log_output.clear()
    
    def create_page(self):
        """创建页面"""
        try:
            # 设置页面
            page = QWebEnginePage(self.web_view)
            self.web_view.setPage(page)
            
            # 设置后端接口
            self.backend.set_page(page)
            
            # 添加JavaScript控制台消息处理
            page.javaScriptConsoleMessage.connect(self.on_js_console_message)
            
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
    
    def on_js_console_message(self, level, message, line_number, source_id):
        """处理JavaScript控制台消息"""
        level_names = {
            0: "INFO",
            1: "WARNING", 
            2: "ERROR",
            3: "DEBUG"
        }
        level_name = level_names.get(level, "UNKNOWN")
        log_msg = f"JS {level_name}: {message} (Line {line_number} in {source_id})"
        self.log_message(log_msg)
    
    def on_page_loaded(self, success):
        """页面加载完成"""
        if success:
            self.log_message("✅ 页面加载成功")
            # 启用所有测试按钮
            self.test_basic_js_btn.setEnabled(True)
            self.test_error_js_btn.setEnabled(True)
            self.test_script_manager_btn.setEnabled(True)
        else:
            self.log_message("❌ 页面加载失败")
            # 禁用所有测试按钮
            self.test_basic_js_btn.setEnabled(False)
            self.test_error_js_btn.setEnabled(False)
            self.test_script_manager_btn.setEnabled(False)
    
    def test_basic_js(self):
        """测试基本JS执行"""
        self.log_message("测试基本JS执行...")
        
        # 构造一个简单的JavaScript代码来测试执行
        js_code = """
        (function() {
            console.log('基本JS执行测试');
            return 'JS执行成功';
        })();
        """
        
        def handle_result(result):
            self.log_message(f"基本JS执行结果: {result}")
            if result == 'JS执行成功':
                self.log_message("✅ 基本JS执行成功")
            else:
                self.log_message("⚠️  基本JS执行完成但返回值不符合预期")
        
        try:
            self.backend.page.runJavaScript(js_code, handle_result)
            self.log_message("✅ 基本JS执行请求已发送")
        except Exception as e:
            self.log_message(f"❌ 基本JS执行请求发送失败: {e}")
    
    def test_error_js(self):
        """测试错误JS执行"""
        self.log_message("测试错误JS执行...")
        
        # 构造一个会出错的JavaScript代码来测试错误处理
        js_code = """
        (function() {
            console.log('错误JS执行测试');
            // 故意引发一个错误
            undefinedFunction();
            return '这行代码不会执行';
        })();
        """
        
        def handle_result(result):
            self.log_message(f"错误JS执行结果: {result}")
            self.log_message("✅ 错误JS执行完成（错误已被捕获）")
        
        try:
            self.backend.page.runJavaScript(js_code, handle_result)
            self.log_message("✅ 错误JS执行请求已发送")
        except Exception as e:
            self.log_message(f"❌ 错误JS执行请求发送失败: {e}")
    
    def test_script_manager(self):
        """测试脚本管理器"""
        self.log_message("测试脚本管理器...")
        
        # 列出所有可用脚本
        scripts = JSScriptManager.list_scripts()
        self.log_message(f"可用脚本数量: {len(scripts)}")
        for script in scripts:
            self.log_message(f"  - {script}")
            
            # 尝试获取脚本内容
            script_content = JSScriptManager.get_script(script)
            if script_content:
                self.log_message(f"    ✅ 脚本内容获取成功，长度: {len(script_content)} 字符")
            else:
                self.log_message(f"    ❌ 脚本内容获取失败")

def main():
    """主函数"""
    print("启动JavaScript错误调试工具...")
    
    app = QApplication(sys.argv)
    window = JSDebugWindow()
    
    # 初始禁用所有测试按钮
    window.test_basic_js_btn.setEnabled(False)
    window.test_error_js_btn.setEnabled(False)
    window.test_script_manager_btn.setEnabled(False)
    
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()