import sys
import os
import json
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QTextEdit, QLabel, QSplitter
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QPalette

class WebEnginePage(QWebEnginePage):
    """自定义WebEnginePage以捕获控制台消息"""
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"JS Console [{level}]: {message} (line {lineNumber})")

class ExcalidrawTester(QMainWindow):
    def __init__(self):
        super().__init__()
        self.left_view = None
        self.right_view = None
        self.left_content = None
        self.right_content = None
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Excalidraw接口测试工具')
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        
        # 创建水平分割器
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # 左侧Excalidraw画布
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        
        left_label = QLabel("左侧Excalidraw画布")
        left_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(left_label)
        
        self.left_view = QWebEngineView()
        left_page = WebEnginePage(self.left_view)
        self.left_view.setPage(left_page)
        left_layout.addWidget(self.left_view)
        
        splitter.addWidget(left_widget)
        
        # 右侧Excalidraw画布
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)
        
        right_label = QLabel("右侧Excalidraw画布")
        right_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(right_label)
        
        self.right_view = QWebEngineView()
        right_page = WebEnginePage(self.right_view)
        self.right_view.setPage(right_page)
        right_layout.addWidget(self.right_view)
        
        splitter.addWidget(right_widget)
        
        # 控制面板
        control_widget = QWidget()
        control_layout = QHBoxLayout()
        control_widget.setLayout(control_layout)
        main_layout.addWidget(control_widget)
        
        # 左侧控制按钮
        left_control_group = QWidget()
        left_control_layout = QVBoxLayout()
        left_control_group.setLayout(left_control_layout)
        left_control_layout.addWidget(QLabel("左侧画布控制:"))
        
        self.get_left_btn = QPushButton("获取左侧内容")
        self.get_left_btn.clicked.connect(lambda: self.get_content(self.left_view, "左侧"))
        left_control_layout.addWidget(self.get_left_btn)
        
        self.reset_left_btn = QPushButton("重置左侧画布")
        self.reset_left_btn.clicked.connect(lambda: self.reset_canvas(self.left_view, "左侧"))
        left_control_layout.addWidget(self.reset_left_btn)
        
        control_layout.addWidget(left_control_group)
        
        # 中间控制按钮
        middle_control_group = QWidget()
        middle_control_layout = QVBoxLayout()
        middle_control_group.setLayout(middle_control_layout)
        middle_control_layout.addWidget(QLabel("操作:"))
        
        self.copy_btn = QPushButton("复制左侧内容到右侧")
        self.copy_btn.clicked.connect(self.copy_content)
        middle_control_layout.addWidget(self.copy_btn)
        
        control_layout.addWidget(middle_control_group)
        
        # 右侧控制按钮
        right_control_group = QWidget()
        right_control_layout = QVBoxLayout()
        right_control_group.setLayout(right_control_layout)
        right_control_layout.addWidget(QLabel("右侧画布控制:"))
        
        self.get_right_btn = QPushButton("获取右侧内容")
        self.get_right_btn.clicked.connect(lambda: self.get_content(self.right_view, "右侧"))
        right_control_layout.addWidget(self.get_right_btn)
        
        self.reset_right_btn = QPushButton("重置右侧画布")
        self.reset_right_btn.clicked.connect(lambda: self.reset_canvas(self.right_view, "右侧"))
        right_control_layout.addWidget(self.reset_right_btn)
        
        control_layout.addWidget(right_control_group)
        
        # 结果显示区域
        self.result_display = QTextEdit()
        self.result_display.setMaximumHeight(150)
        self.result_display.setReadOnly(True)
        main_layout.addWidget(QLabel("结果输出:"))
        main_layout.addWidget(self.result_display)
        
        # 加载Excalidraw页面
        self.load_excalidraw_pages()
        
    def load_excalidraw_pages(self):
        """加载Excalidraw页面到两个视图"""
        # 使用本地部署的文件
        react_build_path = os.path.abspath("./app/editor/plugins/excalidraw/index.html")
        url = QUrl.fromLocalFile(react_build_path)
        
        self.left_view.load(url)
        self.right_view.load(url)
        
        # 等待页面加载完成后执行初始化
        self.left_view.loadFinished.connect(lambda: self.on_page_loaded("左侧"))
        self.right_view.loadFinished.connect(lambda: self.on_page_loaded("右侧"))
        
    def on_page_loaded(self, side):
        """页面加载完成后的回调"""
        self.log_message(f"{side}页面加载完成")
        # 检查window对象上是否有我们需要的函数
        js_code = """
        (function() {
            const functions = ['getContent', 'setValue', 'reset', 'getCurrentItemId', 'setCurrentItemId'];
            const available = {};
            functions.forEach(func => {
                available[func] = typeof window[func] === 'function';
            });
            console.log("Available functions:", available);
            return JSON.stringify(available);
        })();
        """
        
        def handle_result(result):
            try:
                available = json.loads(result)
                self.log_message(f"{side}页面可用函数: {available}")
            except Exception as e:
                self.log_message(f"{side}页面函数检查失败: {str(e)}")
                
        if side == "左侧":
            self.left_view.page().runJavaScript(js_code, handle_result)
        else:
            self.right_view.page().runJavaScript(js_code, handle_result)
        
    def get_content(self, view, side):
        """获取Excalidraw内容"""
        self.log_message(f"正在获取{side}内容...")
        
        js_code = """
        (function() {
            if (typeof window.getContent === 'function') {
                try {
                    const content = window.getContent();
                    console.log("getContent result:", content);
                    return JSON.stringify({success: true, content: content});
                } catch (e) {
                    console.error("getContent error:", e);
                    return JSON.stringify({success: false, error: e.message});
                }
            } else {
                console.error("getContent function not found");
                return JSON.stringify({success: false, error: 'getContent function not found'});
            }
        })();
        """
        
        def handle_result(result):
            try:
                data = json.loads(result)
                if data.get('success'):
                    content = data.get('content', {})
                    self.log_message(f"{side}内容获取成功")
                    self.result_display.append(f"{side}内容: {json.dumps(content, indent=2, ensure_ascii=False)}")
                    
                    # 保存内容用于复制
                    if side == "左侧":
                        self.left_content = content
                    else:
                        self.right_content = content
                else:
                    self.log_message(f"{side}内容获取失败: {data.get('error')}")
            except Exception as e:
                self.log_message(f"{side}内容解析失败: {str(e)}")
                
        view.page().runJavaScript(js_code, handle_result)
        
    def set_content(self, view, side, content):
        """设置Excalidraw内容"""
        self.log_message(f"正在设置{side}内容...")
        
        # 转换内容为JSON字符串
        content_json = json.dumps(content, ensure_ascii=False)
        
        js_code = f"""
        (function() {{
            if (typeof window.setValue === 'function') {{
                try {{
                    const content = JSON.parse('{content_json}');
                    console.log("setValue called with:", content);
                    window.setValue(content);
                    return JSON.stringify({{success: true}});
                }} catch (e) {{
                    console.error("setValue error:", e);
                    return JSON.stringify({{success: false, error: e.message}});
                }}
            }} else {{
                console.error("setValue function not found");
                return JSON.stringify({{success: false, error: 'setValue function not found'}});
            }}
        }})();
        """
        
        def handle_result(result):
            try:
                data = json.loads(result)
                if data.get('success'):
                    self.log_message(f"{side}内容设置成功")
                else:
                    self.log_message(f"{side}内容设置失败: {data.get('error')}")
            except Exception as e:
                self.log_message(f"{side}内容设置结果解析失败: {str(e)}")
                
        view.page().runJavaScript(js_code, handle_result)
        
    def reset_canvas(self, view, side):
        """重置Excalidraw画布"""
        self.log_message(f"正在重置{side}画布...")
        
        js_code = """
        (function() {
            if (typeof window.reset === 'function') {
                try {
                    console.log("reset called");
                    window.reset();
                    return JSON.stringify({success: true});
                } catch (e) {
                    console.error("reset error:", e);
                    return JSON.stringify({success: false, error: e.message});
                }
            } else {
                console.error("reset function not found");
                return JSON.stringify({success: false, error: 'reset function not found'});
            }
        })();
        """
        
        def handle_result(result):
            try:
                data = json.loads(result)
                if data.get('success'):
                    self.log_message(f"{side}画布重置成功")
                    # 清空保存的内容
                    if side == "左侧":
                        self.left_content = None
                    else:
                        self.right_content = None
                else:
                    self.log_message(f"{side}画布重置失败: {data.get('error')}")
            except Exception as e:
                self.log_message(f"{side}画布重置结果解析失败: {str(e)}")
                
        view.page().runJavaScript(js_code, handle_result)
        
    def copy_content(self):
        """复制左侧内容到右侧"""
        self.log_message("正在复制左侧内容到右侧...")
        
        if self.left_content is None:
            self.log_message("错误: 左侧内容为空，请先获取左侧内容")
            return
            
        self.set_content(self.right_view, "右侧", self.left_content)
        
    def log_message(self, message):
        """在结果区域显示消息"""
        self.result_display.append(message)
        print(message)  # 同时打印到控制台

def main():
    app = QApplication(sys.argv)
    
    # 设置应用程序样式
    app.setStyle('Fusion')
    
    tester = ExcalidrawTester()
    tester.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()