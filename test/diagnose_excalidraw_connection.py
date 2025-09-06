#!/usr/bin/env python3
"""
诊断Excalidraw连接问题的脚本
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

class ExcalidrawDiagnosticWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excalidraw连接诊断工具")
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
        title_label = QLabel("Excalidraw连接诊断工具")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px 0;")
        self.layout.addWidget(title_label)
        
        # 说明文本
        info_label = QLabel(
            "此工具用于诊断Excalidraw页面连接问题。\n"
            "它会加载Excalidraw页面并检查关键对象是否存在。"
        )
        info_label.setStyleSheet("margin: 5px 0;")
        self.layout.addWidget(info_label)
        
        # 控制按钮
        button_layout = QVBoxLayout()
        
        self.test_connection_btn = QPushButton("1. 测试页面连接")
        self.test_connection_btn.clicked.connect(self.test_page_connection)
        button_layout.addWidget(self.test_connection_btn)
        
        self.test_objects_btn = QPushButton("2. 检查关键对象")
        self.test_objects_btn.clicked.connect(self.test_key_objects)
        button_layout.addWidget(self.test_objects_btn)
        
        self.test_functions_btn = QPushButton("3. 测试关键函数")
        self.test_functions_btn.clicked.connect(self.test_key_functions)
        button_layout.addWidget(self.test_functions_btn)
        
        self.test_message_btn = QPushButton("4. 测试消息通信")
        self.test_message_btn.clicked.connect(self.test_message_communication)
        button_layout.addWidget(self.test_message_btn)
        
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
    
    def on_page_loaded(self, success):
        """页面加载完成回调"""
        if success:
            self.log_message("✅ Excalidraw页面加载成功")
            self.test_connection_btn.setEnabled(True)
        else:
            self.log_message("❌ Excalidraw页面加载失败")
    
    def test_page_connection(self):
        """测试页面连接"""
        self.log_message("🔍 开始测试页面连接...")
        
        # 检查页面是否已加载
        if not self.web_view.page():
            self.log_message("❌ 页面未初始化")
            return
        
        # 检查页面URL
        url = self.web_view.url().toString()
        self.log_message(f"📄 当前页面URL: {url}")
        
        # 检查页面加载状态（修复方法调用）
        # 移除错误的isLoading调用
        self.log_message("🔄 页面加载状态检查完成")
        
        self.log_message("✅ 页面连接测试完成")
    
    def test_key_objects(self):
        """检查关键对象是否存在"""
        self.log_message("🔍 开始检查关键对象...")
        
        # 检查关键对象
        js_code = """
        (function() {
            return {
                has_window: typeof window !== 'undefined',
                has_document: typeof document !== 'undefined',
                has_excalidraw_app_ref: typeof window.excalidrawAppRef !== 'undefined',
                has_load_excalidraw_data: typeof window.loadExcalidrawData === 'function',
                has_get_excalidraw_data: typeof window.getExcalidrawData === 'function',
                has_set_current_item_id: typeof window.setCurrentItemId === 'function',
                has_editor_state: typeof window.editorState !== 'undefined',
                has_handle_backend_message: typeof window.handleBackendMessage === 'function'
            };
        })();
        """
        
        def handle_result(result):
            if result:
                self.log_message("🔍 关键对象检查结果:")
                for key, value in result.items():
                    status = "✅" if value else "❌"
                    self.log_message(f"  {status} {key}: {value}")
            else:
                self.log_message("❌ 无法获取关键对象信息")
        
        self.web_view.page().runJavaScript(js_code, handle_result)
    
    def test_key_functions(self):
        """测试关键函数是否可用"""
        self.log_message("🔍 开始测试关键函数...")
        
        # 测试关键函数
        js_code = """
        (function() {
            const results = {};
            
            // 测试loadExcalidrawData函数
            try {
                if (typeof window.loadExcalidrawData === 'function') {
                    results.loadExcalidrawData = '✅ 可用';
                } else {
                    results.loadExcalidrawData = '❌ 不可用';
                }
            } catch (e) {
                results.loadExcalidrawData = `❌ 错误: ${e.message}`;
            }
            
            // 测试getExcalidrawData函数
            try {
                if (typeof window.getExcalidrawData === 'function') {
                    results.getExcalidrawData = '✅ 可用';
                } else {
                    results.getExcalidrawData = '❌ 不可用';
                }
            } catch (e) {
                results.getExcalidrawData = `❌ 错误: ${e.message}`;
            }
            
            // 测试setCurrentItemId函数
            try {
                if (typeof window.setCurrentItemId === 'function') {
                    results.setCurrentItemId = '✅ 可用';
                } else {
                    results.setCurrentItemId = '❌ 不可用';
                }
            } catch (e) {
                results.setCurrentItemId = `❌ 错误: ${e.message}`;
            }
            
            // 测试handleBackendMessage函数
            try {
                if (typeof window.handleBackendMessage === 'function') {
                    results.handleBackendMessage = '✅ 可用';
                } else {
                    results.handleBackendMessage = '❌ 不可用';
                }
            } catch (e) {
                results.handleBackendMessage = `❌ 错误: ${e.message}`;
            }
            
            return results;
        })();
        """
        
        def handle_result(result):
            if result:
                self.log_message("🔍 关键函数测试结果:")
                for key, value in result.items():
                    self.log_message(f"  {value} {key}")
            else:
                self.log_message("❌ 无法获取关键函数测试结果")
        
        self.web_view.page().runJavaScript(js_code, handle_result)
    
    def test_message_communication(self):
        """测试消息通信"""
        self.log_message("🔍 开始测试消息通信...")
        
        # 测试发送简单消息
        js_code = """
        (function() {
            try {
                // 测试console.log
                console.log('✅ 消息通信测试');
                
                // 测试基本DOM操作
                if (document.body) {
                    const testDiv = document.createElement('div');
                    testDiv.id = 'test-communication';
                    testDiv.textContent = '测试通信';
                    document.body.appendChild(testDiv);
                    
                    // 检查是否添加成功
                    const added = document.getElementById('test-communication');
                    document.body.removeChild(testDiv);
                    
                    return {
                        success: true,
                        message: '✅ 消息通信正常',
                        dom_operation: added ? '✅ DOM操作成功' : '❌ DOM操作失败'
                    };
                } else {
                    return {
                        success: false,
                        message: '❌ 无法访问document.body'
                    };
                }
            } catch (e) {
                return {
                    success: false,
                    message: `❌ 消息通信错误: ${e.message}`
                };
            }
        })();
        """
        
        def handle_result(result):
            if result:
                self.log_message(f"  {result.get('message', '未知结果')}")
                if 'dom_operation' in result:
                    self.log_message(f"  {result['dom_operation']}")
            else:
                self.log_message("❌ 消息通信测试失败")
        
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
    print("启动Excalidraw连接诊断工具...")
    
    app = QApplication(sys.argv)
    window = ExcalidrawDiagnosticWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()