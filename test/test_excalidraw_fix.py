#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试修复后的Excalidraw页面
"""

import sys
import os
import json
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QHBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QUrl, QObject, Slot, Signal
import traceback


class TestBackendInterface(QObject):
    """测试用的后端接口"""
    
    def __init__(self, log_callback):
        super().__init__()
        self.log_callback = log_callback
        self.messages = []
    
    @Slot(str)
    def dispatch_request(self, request_json):
        """处理前端请求"""
        try:
            request_data = json.loads(request_json)
            log_msg = f"收到前端请求: {request_data}"
            self.log_callback(log_msg)
            self.messages.append(request_data)
            
            # 返回模拟响应
            response = {
                "success": True,
                "requestId": request_data.get("requestId", ""),
                "data": {"message": "测试响应"}
            }
            return json.dumps(response)
        except Exception as e:
            error_msg = f"处理请求时出错: {e}"
            self.log_callback(error_msg)
            return json.dumps({"success": False, "error": str(e)})
    
    @Slot()
    def frontend_ready(self):
        """前端就绪信号"""
        log_msg = "前端已就绪信号收到"
        self.log_callback(log_msg)
        self.messages.append({"type": "frontend_ready"})


class ExcalidrawTestWindow(QMainWindow):
    """Excalidraw测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excalidraw修复测试")
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建按钮
        button_layout = QHBoxLayout()
        self.load_btn = QPushButton("加载修复后的Excalidraw页面")
        self.load_btn.clicked.connect(self.load_excalidraw_page)
        button_layout.addWidget(self.load_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # 创建Web视图
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        
        # 创建日志输出
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)
        
        # 初始化后端接口
        self.backend_interface = TestBackendInterface(self.log_message)
        
        # 连接页面事件
        page = self.web_view.page()
        # 重写javaScriptConsoleMessage方法来捕获控制台消息
        original_console_message = page.javaScriptConsoleMessage
        
        def custom_console_message(level, message, line_number, source_id):
            self.on_js_console_message(level, message, line_number, source_id)
            # 调用原始方法
            original_console_message(level, message, line_number, source_id)
            
        page.javaScriptConsoleMessage = custom_console_message
        
        # 启用必要的设置
        settings = page.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        
        self.log_message("Excalidraw测试工具初始化完成")
        
    def log_message(self, message):
        """记录消息到日志输出"""
        self.log_output.append(message)
        print(f"[TEST] {message}")
        
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
        
    def load_excalidraw_page(self):
        """加载修复后的Excalidraw页面进行测试"""
        try:
            self.log_message("开始加载修复后的Excalidraw页面...")
            
            # 构建Excalidraw页面路径
            excalidraw_path = project_root / "app" / "editor" / "plugins" / "excalidraw" / "index.html"
            
            if not excalidraw_path.exists():
                self.log_message(f"错误: Excalidraw页面文件不存在: {excalidraw_path}")
                return
                
            self.log_message(f"Excalidraw页面路径: {excalidraw_path}")
            
            # 读取并分析index.html文件
            try:
                with open(excalidraw_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.log_message(f"index.html文件大小: {len(content)} 字符")
                    
                    # 检查关键内容
                    if "qrc:/qtwebchannel/qwebchannel.js" in content:
                        self.log_message("✓ 找到QWebChannel引用")
                    else:
                        self.log_message("✗ 未找到QWebChannel引用")
                        
                    if "webchannel-core.js" in content:
                        self.log_message("✓ 找到webchannel-core.js引用")
                    else:
                        self.log_message("✗ 未找到webchannel-core.js引用")
                        
                    if "excalidraw-simple.js" in content:
                        self.log_message("✓ 找到excalidraw-simple.js引用")
                    else:
                        self.log_message("ℹ️ 未找到excalidraw-simple.js引用（可能已打包）")
                        
            except Exception as e:
                self.log_message(f"读取index.html时出错: {e}")
            
            # 设置WebChannel
            channel = QWebChannel()
            channel.registerObject("backendInterface", self.backend_interface)
            self.web_view.page().setWebChannel(channel)
            
            self.log_message("WebChannel已设置")
            
            # 加载页面
            url = QUrl.fromLocalFile(str(excalidraw_path))
            self.log_message(f"加载URL: {url.toString()}")
            self.web_view.load(url)
            
            # 连接加载完成信号
            self.web_view.loadFinished.connect(self.on_page_loaded)
            
            self.log_message("页面加载请求已发送")
            
        except Exception as e:
            error_msg = f"加载Excalidraw页面时出错: {e}\n{traceback.format_exc()}"
            self.log_message(error_msg)
            
    def on_page_loaded(self, success):
        """页面加载完成回调"""
        if success:
            self.log_message("✅ Excalidraw页面加载成功")
            
            # 延迟检查页面内容
            from PySide6.QtCore import QTimer
            QTimer.singleShot(2000, self.check_page_content)
        else:
            self.log_message("❌ Excalidraw页面加载失败")
            
    def check_page_content(self):
        """检查页面内容"""
        self.log_message("检查页面内容...")
        
        # 获取页面标题
        def get_title(title):
            self.log_message(f"页面标题: {title}")
            
        self.web_view.page().titleChanged.connect(get_title)
        self.web_view.page().titleChanged.emit(self.web_view.page().title())
        
        # 执行JavaScript检查页面元素
        js_code = """
        (function() {
            var result = {
                url: window.location.href,
                title: document.title,
                body_children: document.body.children.length,
                has_root: document.getElementById('root') !== null,
                has_qwebchannel: typeof QWebChannel !== 'undefined',
                has_window_handle: typeof window.handleBackendMessage !== 'undefined',
                has_webchannel_manager: typeof window.WebChannelManager !== 'undefined'
            };
            
            // 检查是否有可见元素
            var visible_elements = 0;
            var elements = document.querySelectorAll('*');
            for (var i = 0; i < elements.length; i++) {
                var style = window.getComputedStyle(elements[i]);
                if (style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0') {
                    visible_elements++;
                }
            }
            result.visible_elements = visible_elements;
            
            return JSON.stringify(result);
        })();
        """
        
        def handle_result(result):
            try:
                if result:
                    data = json.loads(result)
                    self.log_message(f"页面内容分析: {json.dumps(data, indent=2, ensure_ascii=False)}")
                else:
                    self.log_message("无法获取页面内容分析结果")
            except Exception as e:
                self.log_message(f"解析页面内容结果时出错: {e}")
                
        self.web_view.page().runJavaScript(js_code, handle_result)
        
        # 检查关键对象是否存在
        diagnostics = self.web_view.page().runJavaScript("""
        (function() {
            return {
                // 移除对WebChannelManager的检查
                has_qt: typeof window.qt !== 'undefined',
                has_webchannel_transport: window.qt && typeof window.qt.webChannelTransport !== 'undefined',
                has_handle_backend_message: typeof window.handleBackendMessage === 'function',
                has_update_scene: typeof window.updateScene === 'function',
                has_get_scene_elements: typeof window.getSceneElements === 'function'
            };
        })();
        """)
        diagnostics.connect(self.log_diagnostics)
        
    def log_diagnostics(self, result):
        """记录诊断信息"""
        try:
            if result:
                data = json.loads(result)
                self.log_message(f"诊断信息: {json.dumps(data, indent=2, ensure_ascii=False)}")
            else:
                self.log_message("无法获取诊断信息")
        except Exception as e:
            self.log_message(f"解析诊断信息时出错: {e}")


def main():
    """主函数"""
    print("启动Excalidraw修复测试工具...")
    
    app = QApplication(sys.argv)
    window = ExcalidrawTestWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()