#!/usr/bin/env python3
"""
深度诊断WebChannel连接问题的脚本
"""

import sys
import os
import time
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QUrl, QTimer
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel

sys.path.insert(0, '.')
from app.editor.webengine import WebPageManager
from app.editor.backend_interface import BackendInterface

class WebChannelDebugger:
    def __init__(self):
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.manager = WebPageManager()
        
    def debug_markdown_page(self):
        """深度诊断markdown页面"""
        print("🔍 深度诊断markdown页面WebChannel连接...")
        
        # 创建页面
        page_type = "markdown"
        backend = BackendInterface(page_type)
        
        # 创建页面
        view = self.manager.create_page(page_type, backend_interface=backend)
        
        if not view:
            print("❌ 页面创建失败")
            return
            
        print(f"✅ 页面创建成功: {page_type}")
        
        # 获取页面
        page = view.page()
        
        # 检查WebChannel状态
        print("📊 WebChannel状态检查:")
        
        # 检查页面是否已加载
        def check_load_status():
            print(f"📄 页面加载状态: {page.isLoading()}")
            
            # 移除对WebChannel就绪状态的检查
            print("⚠️  WebChannel相关检查已移除")
                
            # 检查后端接口
            if backend.page:
                print(f"🔗 后端接口页面: {backend.page}")
            else:
                print("❌ 后端接口页面未设置")
                
        # 延迟检查
        QTimer.singleShot(1000, check_load_status)
        
        # 加载HTML
        html_path = os.path.abspath("app/editor/plugins/markdown/index.html")
        print(f"📁 加载HTML: {html_path}")
        
        view.load(QUrl.fromLocalFile(html_path))
        
        # 等待加载完成
        def on_load_finished(success):
            print(f"📊 页面加载结果: {success}")
            if success:
                # 初始化WebChannel
                page.initialize_web_channel(backend)
                print("✅ WebChannel初始化已触发")
                
                # 检查前端状态
                page.runJavaScript("console.log('前端检查:', window.qt, window.qt?.webChannelTransport)")
                
                # 检查全局变量
                page.runJavaScript("console.log('全局状态:', typeof window.handleBackendMessage)")
            else:
                print("❌ 页面加载失败")
                
        view.loadFinished.connect(on_load_finished)
        
        # 运行事件循环
        QTimer.singleShot(3000, self.app.quit)
        self.app.exec_()

if __name__ == "__main__":
    debugger = WebChannelDebugger()
    debugger.debug_markdown_page()
    print("🎉 诊断完成")