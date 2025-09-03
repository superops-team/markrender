#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Excalidraw白屏问题详细诊断脚本
"""

import sys
import os
import json
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QHBoxLayout, QLabel
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QUrl, QObject, Slot, Signal, QTimer
import traceback


class DiagnosticBackendInterface(QObject):
    """诊断用的后端接口"""
    
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
                "data": {"message": "诊断响应"}
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


class ExcalidrawDiagnosticWindow(QMainWindow):
    """Excalidraw诊断窗口"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excalidraw白屏问题诊断工具")
        self.setGeometry(100, 100, 1400, 900)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # 创建控制面板
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)
        
        self.load_btn = QPushButton("1. 加载Excalidraw页面")
        self.load_btn.clicked.connect(self.load_excalidraw_page)
        
        self.check_resources_btn = QPushButton("2. 检查资源加载")
        self.check_resources_btn.clicked.connect(self.check_resources)
        self.check_resources_btn.setEnabled(False)
        
        self.test_communication_btn = QPushButton("3. 测试WebChannel通信")
        self.test_communication_btn.clicked.connect(self.test_webchannel)
        self.test_communication_btn.setEnabled(False)
        
        control_layout.addWidget(self.load_btn)
        control_layout.addWidget(self.check_resources_btn)
        control_layout.addWidget(self.test_communication_btn)
        control_layout.addStretch()
        
        main_layout.addWidget(control_panel)
        
        # 创建信息显示区域
        info_panel = QWidget()
        info_layout = QHBoxLayout(info_panel)
        
        # 左侧：文件信息
        file_info_group = QWidget()
        file_info_layout = QVBoxLayout(file_info_group)
        file_info_layout.addWidget(QLabel("文件信息:"))
        self.file_info = QTextEdit()
        self.file_info.setReadOnly(True)
        file_info_layout.addWidget(self.file_info)
        
        # 右侧：诊断日志
        log_group = QWidget()
        log_layout = QVBoxLayout(log_group)
        log_layout.addWidget(QLabel("诊断日志:"))
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        log_layout.addWidget(self.log_output)
        
        info_layout.addWidget(file_info_group, 1)
        info_layout.addWidget(log_group, 2)
        
        main_layout.addWidget(info_panel)
        
        # 创建Web视图（较小尺寸以便观察）
        web_group = QWidget()
        web_layout = QVBoxLayout(web_group)
        web_layout.addWidget(QLabel("页面预览:"))
        self.web_view = QWebEngineView()
        self.web_view.setMinimumHeight(400)
        web_layout.addWidget(self.web_view)
        main_layout.addWidget(web_group, 2)
        
        # 初始化后端接口
        self.backend_interface = DiagnosticBackendInterface(self.log_message)
        
        # 连接页面事件
        page = self.web_view.page()
        # 重写javaScriptConsoleMessage方法来捕获控制台消息
        original_console_message = page.javaScriptConsoleMessage
        
        def custom_console_message(level, message, line_number, source_id):
            self.on_js_console_message(level, message, line_number, source_id)
            # 调用原始方法
            original_console_message(level, message, line_number, source_id)
            
        page.javaScriptConsoleMessage = custom_console_message
        
        # 启用开发者工具和调试选项
        settings = page.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        # 注释掉可能不兼容的设置
        # settings.setAttribute(QWebEngineSettings.WebAttribute.DeveloperExtrasEnabled, True)
        
        self.log_message("Excalidraw诊断工具初始化完成")
        self.check_file_structure()
        
    def log_message(self, message):
        """记录消息到日志输出"""
        self.log_output.append(message)
        print(f"[DIAGNOSTIC] {message}")
        
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
        
    def check_file_structure(self):
        """检查文件结构"""
        self.log_message("检查Excalidraw文件结构...")
        
        # 检查主要文件
        excalidraw_dir = project_root / "app" / "editor" / "plugins" / "excalidraw"
        files_to_check = [
            "index.html",
            "webchannel-core.js",
            "excalidraw-simple.js"
        ]
        
        file_info_text = "=== 文件结构检查 ===\n"
        for file_name in files_to_check:
            file_path = excalidraw_dir / file_name
            if file_path.exists():
                file_info_text += f"✓ {file_name} - 存在\n"
                # 检查文件大小
                size = file_path.stat().st_size
                file_info_text += f"  大小: {size} 字节\n"
                
                # 读取文件前几行进行检查
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        first_lines = [next(f) for _ in range(5)]
                        file_info_text += f"  前几行: {''.join(first_lines[:3])}\n"
                except Exception as e:
                    file_info_text += f"  读取错误: {e}\n"
            else:
                file_info_text += f"✗ {file_name} - 不存在\n"
                
        # 检查assets目录
        assets_dir = excalidraw_dir / "assets"
        if assets_dir.exists():
            file_info_text += f"\n✓ assets目录 - 存在\n"
            try:
                asset_files = list(assets_dir.iterdir())
                file_info_text += f"  包含 {len(asset_files)} 个文件\n"
                for asset_file in asset_files[:5]:  # 只显示前5个
                    file_info_text += f"  - {asset_file.name}\n"
            except Exception as e:
                file_info_text += f"  读取assets目录错误: {e}\n"
        else:
            file_info_text += f"\n✗ assets目录 - 不存在\n"
            
        self.file_info.setPlainText(file_info_text)
        
    def load_excalidraw_page(self):
        """加载Excalidraw页面进行测试"""
        try:
            self.log_message("开始加载Excalidraw页面...")
            
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
                        self.log_message("✗ 未找到excalidraw-simple.js引用")
                        
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
            self.check_resources_btn.setEnabled(True)
            
            # 延迟检查页面内容
            QTimer.singleShot(1000, self.check_page_content)
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
                has_window_handle: typeof window.handleBackendMessage !== 'undefined'
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
        
    def check_resources(self):
        """检查资源加载情况"""
        self.log_message("检查资源加载情况...")
        
        # 执行JavaScript检查资源加载状态
        js_code = """
        (function() {
            var resources = {
                scripts: [],
                styles: [],
                errors: []
            };
            
            // 检查所有script标签
            var scripts = document.getElementsByTagName('script');
            for (var i = 0; i < scripts.length; i++) {
                var script = scripts[i];
                var src = script.src || 'inline';
                var status = script.readyState || (script.src ? 'loaded' : 'inline');
                resources.scripts.push({
                    src: src,
                    status: status
                });
            }
            
            // 检查所有link标签
            var links = document.getElementsByTagName('link');
            for (var i = 0; i < links.length; i++) {
                var link = links[i];
                if (link.rel === 'stylesheet') {
                    resources.styles.push({
                        href: link.href,
                        status: link.sheet ? 'loaded' : 'loading'
                    });
                }
            }
            
            return JSON.stringify(resources);
        })();
        """
        
        def handle_result(result):
            try:
                if result:
                    data = json.loads(result)
                    self.log_message("资源加载情况:")
                    self.log_message(f"Scripts: {len(data['scripts'])} 个")
                    for script in data['scripts']:
                        self.log_message(f"  - {script['src'][:80]} ({script['status']})")
                        
                    self.log_message(f"Styles: {len(data['styles'])} 个")
                    for style in data['styles']:
                        self.log_message(f"  - {style['href'][:80]} ({style['status']})")
                        
                    if data['errors']:
                        self.log_message("加载错误:")
                        for error in data['errors']:
                            self.log_message(f"  - {error}")
                else:
                    self.log_message("无法获取资源加载情况")
            except Exception as e:
                self.log_message(f"解析资源加载结果时出错: {e}")
                
        self.web_view.page().runJavaScript(js_code, handle_result)
        
        self.test_communication_btn.setEnabled(True)
        
    def test_webchannel(self):
        """测试WebChannel通信"""
        self.log_message("测试WebChannel通信...")
        
        # 尝试调用前端就绪方法
        js_code = """
        (function() {
            var result = {
                has_backend_interface: typeof window.backendInterface !== 'undefined',
                has_frontend_ready: typeof window.backendInterface !== 'undefined' && typeof window.backendInterface.frontend_ready !== 'undefined',
                has_dispatch_request: typeof window.backendInterface !== 'undefined' && typeof window.backendInterface.dispatch_request !== 'undefined'
            };
            
            // 尝试调用frontend_ready
            if (result.has_frontend_ready) {
                try {
                    window.backendInterface.frontend_ready();
                    result.frontend_ready_called = true;
                } catch (e) {
                    result.frontend_ready_called = false;
                    result.frontend_ready_error = e.message;
                }
            }
            
            return JSON.stringify(result);
        })();
        """
        
        def handle_result(result):
            try:
                if result:
                    data = json.loads(result)
                    self.log_message("WebChannel通信测试结果:")
                    for key, value in data.items():
                        self.log_message(f"  {key}: {value}")
                else:
                    self.log_message("无法获取WebChannel通信测试结果")
            except Exception as e:
                self.log_message(f"解析WebChannel测试结果时出错: {e}")
                
        self.web_view.page().runJavaScript(js_code, handle_result)


def main():
    """主函数"""
    print("启动Excalidraw白屏问题诊断工具...")
    
    app = QApplication(sys.argv)
    window = ExcalidrawDiagnosticWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()