#!/usr/bin/env python3
"""
诊断Excalidraw切换item时的问题
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

class ExcalidrawItemSwitchDiagnostic(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excalidraw Item切换诊断工具")
        self.setGeometry(100, 100, 1000, 700)
        
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
        title_label = QLabel("Excalidraw Item切换诊断工具")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px 0;")
        self.layout.addWidget(title_label)
        
        # 说明文本
        info_label = QLabel(
            "此工具用于诊断Excalidraw在切换item时的问题。\n"
            "模拟切换不同item的操作，检查关键函数和状态。"
        )
        info_label.setStyleSheet("margin: 5px 0;")
        self.layout.addWidget(info_label)
        
        # 控制按钮
        button_layout = QVBoxLayout()
        
        self.load_page_btn = QPushButton("1. 加载Excalidraw页面")
        self.load_page_btn.clicked.connect(self.load_excalidraw_page)
        button_layout.addWidget(self.load_page_btn)
        
        self.test_item1_btn = QPushButton("2. 模拟加载Item 1")
        self.test_item1_btn.clicked.connect(lambda: self.simulate_item_load("item1", "[]"))
        button_layout.addWidget(self.test_item1_btn)
        
        self.test_item2_btn = QPushButton("3. 模拟加载Item 2")
        self.test_item2_btn.clicked.connect(lambda: self.simulate_item_load("item2", '[{"id":"test","type":"rectangle","x":100,"y":100,"width":200,"height":100}]'))
        button_layout.addWidget(self.test_item2_btn)
        
        self.test_switch_btn = QPushButton("4. 模拟切换Item")
        self.test_switch_btn.clicked.connect(self.simulate_item_switch)
        button_layout.addWidget(self.test_switch_btn)
        
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
    
    def simulate_item_load(self, item_id, content):
        """模拟加载item"""
        self.log_message(f"🔄 模拟加载Item: {item_id}")
        
        # 发送setValue消息到前端
        js_code = f"""
        (function() {{
            try {{
                if (typeof window.handleBackendMessage === 'function') {{
                    const result = window.handleBackendMessage('setValue', {{
                        content: {json.dumps(content)},
                        itemId: '{item_id}'
                    }}, 'test_request_id');
                    return {{ success: true, message: 'setValue消息已发送', result: result }};
                }} else {{
                    return {{ success: false, message: 'handleBackendMessage函数不可用' }};
                }}
            }} catch (e) {{
                return {{ success: false, error: e.message }};
            }}
        }})();
        """
        
        def handle_result(result):
            if result is not None:
                if isinstance(result, dict):
                    self.log_message(f"  {result.get('message', result.get('error', '未知结果'))}")
                    if 'result' in result:
                        self.log_message(f"    返回结果: {result['result']}")
                elif isinstance(result, str) and result == "":
                    self.log_message(f"  JavaScript执行成功，但返回空字符串")
                else:
                    self.log_message(f"  JavaScript返回结果: {result} (类型: {type(result)})")
            else:
                self.log_message("  ❌ 无法执行JavaScript代码或JavaScript返回null")
        
        self.web_view.page().runJavaScript(js_code, handle_result)
    
    def simulate_item_switch(self):
        """模拟切换item"""
        self.log_message("🔄 模拟切换Item...")
        
        # 先获取当前数据
        js_code = """
        (function() {
            try {
                if (typeof window.getExcalidrawData === 'function') {
                    const data = window.getExcalidrawData();
                    return { success: true, data: data };
                } else {
                    return { success: false, message: 'getExcalidrawData函数不可用' };
                }
            } catch (e) {
                return { success: false, error: e.message };
            }
        })();
        """
        
        def handle_result(result):
            if result is not None:
                if isinstance(result, dict):
                    if result.get('success'):
                        self.log_message(f"  当前数据获取成功，长度: {len(result.get('data', ''))}")
                        # 然后模拟切换到新item
                        self.simulate_item_load("item3", '[{"id":"switch_test","type":"ellipse","x":50,"y":50,"width":150,"height":150}]')
                    else:
                        self.log_message(f"  {result.get('message', result.get('error', '未知错误'))}")
                elif isinstance(result, str) and result == "":
                    self.log_message(f"  JavaScript执行成功，但返回空字符串")
                else:
                    self.log_message(f"  JavaScript返回结果: {result} (类型: {type(result)})")
            else:
                self.log_message("  ❌ 无法执行JavaScript代码或JavaScript返回null")
        
        self.web_view.page().runJavaScript(js_code, handle_result)

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
        print(log_msg)
        
        # 如果是错误消息，也在诊断工具中显示
        if level == QWebEnginePage.ErrorMessageLevel:
            # 这里可以将错误消息发送到诊断窗口，但由于作用域限制，我们只打印到控制台
            pass

def main():
    """主函数"""
    print("启动Excalidraw Item切换诊断工具...")
    
    app = QApplication(sys.argv)
    window = ExcalidrawItemSwitchDiagnostic()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()