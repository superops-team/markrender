#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Excalidraw集成测试脚本
验证Excalidraw页面在Qt WebEngine和浏览器中的加载情况
"""

import sys
import os
import json
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QHBoxLayout, QTabWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QUrl, QObject, Slot, Signal, QTimer
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
                "data": {"message": "测试响应", "timestamp": "2025-08-30T10:00:00Z"}
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


class ExcalidrawIntegrationTestWindow(QMainWindow):
    """Excalidraw集成测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excalidraw集成测试工具")
        self.setGeometry(100, 100, 1400, 900)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # 创建Qt WebEngine测试页
        self.create_qt_test_page()
        
        # 创建浏览器测试页
        self.create_browser_test_page()
        
        # 创建控制面板
        self.create_control_panel()
        
        # 创建日志输出
        self.create_log_panel()
        
        # 初始化后端接口
        self.backend_interface = TestBackendInterface(self.log_message)
        
        self.log_message("Excalidraw集成测试工具初始化完成")
        self.check_file_structure()
        
    def create_qt_test_page(self):
        """创建Qt WebEngine测试页"""
        qt_page = QWidget()
        layout = QVBoxLayout(qt_page)
        
        # 创建按钮
        button_layout = QHBoxLayout()
        self.load_qt_btn = QPushButton("加载Qt版本Excalidraw")
        self.load_qt_btn.clicked.connect(self.load_qt_excalidraw)
        button_layout.addWidget(self.load_qt_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # 创建Web视图
        self.qt_web_view = QWebEngineView()
        layout.addWidget(self.qt_web_view)
        
        # 连接页面事件
        page = self.qt_web_view.page()
        original_console_message = page.javaScriptConsoleMessage
        
        def custom_console_message(level, message, line_number, source_id):
            self.on_js_console_message("Qt", level, message, line_number, source_id)
            original_console_message(level, message, line_number, source_id)
            
        page.javaScriptConsoleMessage = custom_console_message
        
        # 启用必要的设置
        settings = page.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        
        self.tab_widget.addTab(qt_page, "Qt WebEngine测试")
        
    def create_browser_test_page(self):
        """创建浏览器测试页"""
        browser_page = QWidget()
        layout = QVBoxLayout(browser_page)
        
        # 创建按钮
        button_layout = QHBoxLayout()
        self.load_browser_btn = QPushButton("加载浏览器版本Excalidraw")
        self.load_browser_btn.clicked.connect(self.load_browser_excalidraw)
        button_layout.addWidget(self.load_browser_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # 创建Web视图
        self.browser_web_view = QWebEngineView()
        layout.addWidget(self.browser_web_view)
        
        # 连接页面事件
        page = self.browser_web_view.page()
        original_console_message = page.javaScriptConsoleMessage
        
        def custom_console_message(level, message, line_number, source_id):
            self.on_js_console_message("Browser", level, message, line_number, source_id)
            original_console_message(level, message, line_number, source_id)
            
        page.javaScriptConsoleMessage = custom_console_message
        
        # 启用必要的设置
        settings = page.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        
        self.tab_widget.addTab(browser_page, "浏览器兼容测试")
        
    def create_control_panel(self):
        """创建控制面板"""
        # 控制面板将在日志面板中创建
        
    def create_log_panel(self):
        """创建日志面板"""
        # 这里我们已经在主布局中添加了标签页，日志输出将作为主窗口的一部分
        
    def log_message(self, message):
        """记录消息到日志输出"""
        # 由于我们没有单独的日志面板，直接打印到控制台
        print(f"[TEST] {message}")
        
    def on_js_console_message(self, source, level, message, line_number, source_id):
        """处理JavaScript控制台消息"""
        level_names = {
            0: "INFO",
            1: "WARNING", 
            2: "ERROR",
            3: "DEBUG"
        }
        level_name = level_names.get(level, "UNKNOWN")
        log_msg = f"JS {source} {level_name}: {message} (Line {line_number} in {source_id})"
        self.log_message(log_msg)
        
    def check_file_structure(self):
        """检查文件结构"""
        self.log_message("检查Excalidraw文件结构...")
        
        # 检查Qt版本文件
        qt_dir = project_root / "app" / "editor" / "plugins" / "excalidraw"
        self.check_directory_structure("Qt版本", qt_dir)
        
        # 检查浏览器版本文件
        browser_dir = project_root / "frontend" / "excalidraw" / "browser"
        self.check_directory_structure("浏览器版本", browser_dir)
        
    def check_directory_structure(self, version_name, directory):
        """检查目录结构"""
        if not directory.exists():
            self.log_message(f"❌ {version_name}目录不存在: {directory}")
            return
            
        self.log_message(f"📁 {version_name}目录: {directory}")
        
        # 检查主要文件
        files_to_check = [
            "index.html",
            "webchannel-core.js"
        ]
        
        for file_name in files_to_check:
            file_path = directory / file_name
            if file_path.exists():
                size = file_path.stat().st_size
                self.log_message(f"  ✅ {file_name} - {size} 字节")
            else:
                self.log_message(f"  ❌ {file_name} - 不存在")
                
        # 检查assets目录
        assets_dir = directory / "assets"
        if assets_dir.exists():
            asset_files = list(assets_dir.iterdir())
            self.log_message(f"  ✅ assets目录 - 包含 {len(asset_files)} 个文件")
        else:
            self.log_message(f"  ❌ assets目录 - 不存在")
        
    def load_qt_excalidraw(self):
        """加载Qt版本Excalidraw"""
        try:
            self.log_message("开始加载Qt版本Excalidraw...")
            
            # 构建Excalidraw页面路径
            excalidraw_path = project_root / "app" / "editor" / "plugins" / "excalidraw" / "index.html"
            
            if not excalidraw_path.exists():
                self.log_message(f"❌ Qt版本Excalidraw页面文件不存在: {excalidraw_path}")
                return
                
            self.log_message(f"Qt版本Excalidraw页面路径: {excalidraw_path}")
            
            # 设置WebChannel
            channel = QWebChannel()
            channel.registerObject("backendInterface", self.backend_interface)
            self.qt_web_view.page().setWebChannel(channel)
            
            self.log_message("Qt版本WebChannel已设置")
            
            # 加载页面
            url = QUrl.fromLocalFile(str(excalidraw_path))
            self.log_message(f"加载URL: {url.toString()}")
            self.qt_web_view.load(url)
            
            # 连接加载完成信号
            self.qt_web_view.loadFinished.connect(self.on_qt_page_loaded)
            
            self.log_message("Qt版本页面加载请求已发送")
            
        except Exception as e:
            error_msg = f"加载Qt版本Excalidraw页面时出错: {e}\n{traceback.format_exc()}"
            self.log_message(error_msg)
            
    def on_qt_page_loaded(self, success):
        """Qt版本页面加载完成回调"""
        if success:
            self.log_message("✅ Qt版本Excalidraw页面加载成功")
            
            # 延迟检查页面内容
            QTimer.singleShot(2000, lambda: self.check_page_content("Qt", self.qt_web_view))
        else:
            self.log_message("❌ Qt版本Excalidraw页面加载失败")
            
    def load_browser_excalidraw(self):
        """加载浏览器版本Excalidraw"""
        try:
            self.log_message("开始加载浏览器版本Excalidraw...")
            
            # 构建Excalidraw页面路径
            excalidraw_path = project_root / "frontend" / "excalidraw" / "browser" / "index.html"
            
            if not excalidraw_path.exists():
                self.log_message(f"❌ 浏览器版本Excalidraw页面文件不存在: {excalidraw_path}")
                return
                
            self.log_message(f"浏览器版本Excalidraw页面路径: {excalidraw_path}")
            
            # 设置WebChannel
            channel = QWebChannel()
            channel.registerObject("backendInterface", self.backend_interface)
            self.browser_web_view.page().setWebChannel(channel)
            
            self.log_message("浏览器版本WebChannel已设置")
            
            # 加载页面
            url = QUrl.fromLocalFile(str(excalidraw_path))
            self.log_message(f"加载URL: {url.toString()}")
            self.browser_web_view.load(url)
            
            # 连接加载完成信号
            self.browser_web_view.loadFinished.connect(self.on_browser_page_loaded)
            
            self.log_message("浏览器版本页面加载请求已发送")
            
        except Exception as e:
            error_msg = f"加载浏览器版本Excalidraw页面时出错: {e}\n{traceback.format_exc()}"
            self.log_message(error_msg)
            
    def on_browser_page_loaded(self, success):
        """浏览器版本页面加载完成回调"""
        if success:
            self.log_message("✅ 浏览器版本Excalidraw页面加载成功")
            
            # 延迟检查页面内容
            QTimer.singleShot(2000, lambda: self.check_page_content("Browser", self.browser_web_view))
        else:
            self.log_message("❌ 浏览器版本Excalidraw页面加载失败")
            
    def check_page_content(self, version, web_view):
        """检查页面内容"""
        self.log_message(f"检查{version}版本页面内容...")
        
        # 获取页面标题
        def get_title(title):
            self.log_message(f"{version}版本页面标题: {title}")
            
        web_view.page().titleChanged.connect(get_title)
        web_view.page().titleChanged.emit(web_view.page().title())
        
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
                    self.log_message(f"{version}版本页面内容分析:")
                    for key, value in data.items():
                        self.log_message(f"  {key}: {value}")
                else:
                    self.log_message(f"无法获取{version}版本页面内容分析结果")
            except Exception as e:
                self.log_message(f"解析{version}版本页面内容结果时出错: {e}")
                
        web_view.page().runJavaScript(js_code, handle_result)


def main():
    """主函数"""
    print("启动Excalidraw集成测试工具...")
    
    app = QApplication(sys.argv)
    window = ExcalidrawIntegrationTestWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()