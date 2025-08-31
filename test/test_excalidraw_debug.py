#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Excalidraw白屏问题诊断测试脚本
"""

import sys
import os
import json
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QUrl, QObject, Slot, Signal
import traceback


class TestBackendInterface(QObject):
    """测试用的后端接口"""
    
    def __init__(self):
        super().__init__()
        self.messages = []
    
    @Slot(str)
    def dispatch_request(self, request_json):
        """处理前端请求"""
        try:
            request_data = json.loads(request_json)
            print(f"收到前端请求: {request_data}")
            self.messages.append(request_data)
            
            # 返回模拟响应
            response = {
                "success": True,
                "requestId": request_data.get("requestId", ""),
                "data": {"message": "测试响应"}
            }
            return json.dumps(response)
        except Exception as e:
            print(f"处理请求时出错: {e}")
            return json.dumps({"success": False, "error": str(e)})
    
    @Slot()
    def frontend_ready(self):
        """前端就绪信号"""
        print("前端已就绪")
        self.messages.append({"type": "frontend_ready"})


class DebugWindow(QMainWindow):
    """调试窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excalidraw调试工具")
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 创建按钮
        self.load_btn = QPushButton("加载Excalidraw页面")
        self.load_btn.clicked.connect(self.load_excalidraw_page)
        layout.addWidget(self.load_btn)
        
        # 创建Web视图
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        
        # 创建日志输出
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)
        
        # 初始化后端接口
        self.backend_interface = TestBackendInterface()
        
        # 连接JavaScript控制台消息（正确的方式）
        page = self.web_view.page()
        # 重写javaScriptConsoleMessage方法来捕获控制台消息
        original_console_message = page.javaScriptConsoleMessage
        
        def custom_console_message(level, message, line_number, source_id):
            self.on_js_console_message(level, message, line_number, source_id)
            # 调用原始方法
            original_console_message(level, message, line_number, source_id)
            
        page.javaScriptConsoleMessage = custom_console_message
        
    def log_message(self, message):
        """记录消息到日志输出"""
        self.log_output.append(message)
        print(message)
        
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
        """加载Excalidraw页面进行测试"""
        try:
            # 构建Excalidraw页面路径
            excalidraw_path = project_root / "app" / "editor" / "plugins" / "excalidraw" / "index.html"
            
            if not excalidraw_path.exists():
                self.log_message(f"错误: Excalidraw页面文件不存在: {excalidraw_path}")
                return
                
            self.log_message(f"加载Excalidraw页面: {excalidraw_path}")
            
            # 设置WebChannel
            channel = QWebChannel()
            channel.registerObject("backendInterface", self.backend_interface)
            self.web_view.page().setWebChannel(channel)
            
            # 加载页面
            self.web_view.load(QUrl.fromLocalFile(str(excalidraw_path)))
            
            # 连接加载完成信号
            self.web_view.loadFinished.connect(self.on_page_loaded)
            
        except Exception as e:
            error_msg = f"加载Excalidraw页面时出错: {e}\n{traceback.format_exc()}"
            self.log_message(error_msg)
            
    def on_page_loaded(self, success):
        """页面加载完成回调"""
        if success:
            self.log_message("Excalidraw页面加载成功")
            # 尝试调用前端就绪方法
            js_code = "if (window.backendInterface && window.backendInterface.frontend_ready) window.backendInterface.frontend_ready();"
            self.web_view.page().runJavaScript(js_code)
        else:
            self.log_message("Excalidraw页面加载失败")


def main():
    """主函数"""
    print("启动Excalidraw白屏问题诊断工具...")
    
    app = QApplication(sys.argv)
    window = DebugWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()