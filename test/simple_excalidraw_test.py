#!/usr/bin/env python3
"""
简单的Excalidraw测试脚本
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLabel
from PySide6.QtCore import QTimer, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
import json
import os

class SimpleExcalidrawTest(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("简单Excalidraw测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建UI
        self.setup_ui()
        
        # 创建Web视图
        self.web_view = QWebEngineView()
        self.web_page = CustomWebEnginePage(self.web_view)
        self.web_view.setPage(self.web_page)
        
        # 添加到布局
        self.layout.addWidget(self.web_view)
        
        # 延迟加载页面
        QTimer.singleShot(100, self.load_excalidraw_page)
    
    def setup_ui(self):
        """创建用户界面"""
        central_widget = QWidget()
        self.layout = QVBoxLayout(central_widget)
        
        # 标题
        title_label = QLabel("简单Excalidraw测试")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px 0;")
        self.layout.addWidget(title_label)
        
        # 控制按钮
        button_layout = QVBoxLayout()
        
        self.test_functions_btn = QPushButton("测试关键函数")
        self.test_functions_btn.clicked.connect(self.test_key_functions)
        button_layout.addWidget(self.test_functions_btn)
        
        self.test_set_value_btn = QPushButton("测试setValue")
        self.test_set_value_btn.clicked.connect(self.test_set_value)
        button_layout.addWidget(self.test_set_value_btn)
        
        self.layout.addLayout(button_layout)
        
        # 日志显示区域
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        self.log_text.setReadOnly(True)
        self.layout.addWidget(self.log_text)
        
        self.setCentralWidget(central_widget)
    
    def log_message(self, message):
        """记录日志消息"""
        self.log_text.append(message)
        print(message)
    
    def load_excalidraw_page(self):
        """加载Excalidraw页面"""
        self.log_message("📂 开始加载Excalidraw页面...")
        
        # 获取HTML文件路径
        html_path = os.path.abspath("app/editor/plugins/excalidraw/index.html")
        if not os.path.exists(html_path):
            html_path = os.path.join(project_root, "app/editor/plugins/excalidraw/index.html")
        
        if os.path.exists(html_path):
            url = QUrl.fromLocalFile(html_path)
            self.web_view.load(url)
            self.log_message(f"✅ 开始加载: {html_path}")
        else:
            self.log_message(f"❌ 未找到Excalidraw页面: {html_path}")
    
    def wait_for_page_load(self, callback):
        """等待页面加载完成后再执行回调"""
        def check_page():
            js_code = """
            (function() {
                return typeof window.handleBackendMessage !== 'undefined';
            })();
            """
            
            def handle_result(result):
                if result:
                    callback()
                else:
                    # 继续等待
                    QTimer.singleShot(500, check_page)
            
            self.web_view.page().runJavaScript(js_code, handle_result)
        
        check_page()
    
    def test_key_functions(self):
        """测试关键函数是否存在"""
        self.log_message("🔍 测试关键函数...")
        
        def execute_test():
            js_code = """
            (function() {
                const functions = [
                    'handleBackendMessage',
                    'loadExcalidrawData', 
                    'getExcalidrawData',
                    'setCurrentItemId'
                ];
                
                const results = {};
                functions.forEach(func => {
                    results[func] = typeof window[func] === 'function';
                });
                
                return results;
            })();
            """
            
            def handle_result(result):
                if result:
                    self.log_message("🔍 函数检查结果:")
                    for func, exists in result.items():
                        status = "✅" if exists else "❌"
                        self.log_message(f"  {status} {func}: {'存在' if exists else '不存在'}")
                else:
                    self.log_message("❌ 无法获取函数检查结果")
            
            self.web_view.page().runJavaScript(js_code, handle_result)
        
        self.wait_for_page_load(execute_test)
    
    def test_set_value(self):
        """测试setValue功能"""
        self.log_message("🔄 测试setValue功能...")
        
        def execute_test():
            js_code = """
            (function() {
                try {
                    if (typeof window.handleBackendMessage === 'function') {
                        const testData = '[{"id":"test1","type":"rectangle","x":100,"y":100,"width":200,"height":100,"strokeColor":"#000000"}]';
                        const result = window.handleBackendMessage('setValue', {
                            content: testData,
                            itemId: 'test_item'
                        });
                        return {
                            success: true,
                            message: 'setValue执行完成',
                            result: result
                        };
                    } else {
                        return {
                            success: false,
                            message: 'handleBackendMessage函数不存在'
                        };
                    }
                } catch (e) {
                    return {
                        success: false,
                        message: '执行出错: ' + e.message
                    };
                }
            })();
            """
            
            def handle_result(result):
                if result:
                    if isinstance(result, dict):
                        self.log_message(f"  {result.get('message', '未知结果')}")
                        if 'result' in result:
                            self.log_message(f"    返回结果: {result['result']}")
                    else:
                        self.log_message(f"  返回结果: {result}")
                else:
                    self.log_message("  ❌ 无返回结果")
            
            self.web_view.page().runJavaScript(js_code, handle_result)
        
        self.wait_for_page_load(execute_test)

class CustomWebEnginePage(QWebEnginePage):
    """自定义WebEnginePage，用于捕获控制台消息"""
    
    def javaScriptConsoleMessage(self, level, message, line_number, source_id):
        """处理JavaScript控制台消息"""
        level_map = {
            QWebEnginePage.InfoMessageLevel: "INFO",
            QWebEnginePage.WarningMessageLevel: "WARNING",
            QWebEnginePage.ErrorMessageLevel: "ERROR"
        }
        log_level = level_map.get(level, "UNKNOWN")
        
        # 格式化日志消息
        log_msg = f"🌐 JS {log_level}: {message} (at line {line_number} in {source_id})"
        logger.info(log_msg)

def main():
    """主函数"""
    print("启动简单Excalidraw测试...")
    
    app = QApplication(sys.argv)
    window = SimpleExcalidrawTest()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()