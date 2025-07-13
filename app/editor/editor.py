import os
from utils import logger
from PySide6 import QtWidgets
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6 import QtWebEngineCore  # Add this import
from PySide6.QtCore import QUrl, QObject, Signal, Property
from PySide6.QtWebChannel import QWebChannel
from ..app_style import AppStyle
from PySide6.QtWebEngineCore import QWebEnginePage


class MarkdownDocument(QObject):
    def __init__(self, file_id, file_name):
        super().__init__()
        self._file_id = file_id
        self.file_name = file_name
        self._text = ""
        self._lines = []  # 存储按行分割后的文本
        self._page_size = 500  # 每页行数
        self._loaded_lines = 0  # 已加载的行数

    @property
    def file_id(self):
        return self._file_id

    @file_id.setter
    def file_id(self, value):
        if value != self._file_id:
            self.reset()
            self._file_id = value

    def get_text(self):
        return self._text

    def set_text(self, text):
        # 仅在文件 ID 变化时才 reset，这里调用 set_text 时应先设置正确的 file_id
        self._text = text
        self._lines = text.split('\n')
        self.text_changed.emit(text)

    def reset(self):
        """重置文档状态"""
        self._text = ""
        self._lines = []
        self._loaded_lines = 0
        self.text_changed.emit("")  # 发射清空内容的信号

    text_changed = Signal(str)
    text = Property(str, get_text, set_text, notify=text_changed)


# 自定义 QWebEnginePage 类，拦截控制台日志
class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)

    def javaScriptConsoleMessage(self, level, message, line_number, source_id):
        # 调用原有的处理方法，可根据需求修改处理逻辑
        super().javaScriptConsoleMessage(level, message, line_number, source_id)
        # 可以在这里添加自定义的日志记录逻辑
        print(f"JS Console: {message} (Line {line_number} in {source_id})", level)

class MarkdownEditor(QtWidgets.QWidget):
    def __init__(self, parent=None, file_id="", file_name=""):
        super().__init__(parent)
        # Initialize document for WebChannel
        self.document = MarkdownDocument(file_id, file_name)
        # Setup GUI
        self.setup_ui()

    def setup_ui(self):
        # Web view for Cherry Markdown
        self.preview = QWebEngineView()
        # 创建自定义的 Page 实例
        page = CustomWebEnginePage(self.preview)
        self.preview.setPage(page)

        # 创建布局
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.preview)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(0)
        self.setLayout(layout)

        # 设置圆角样式
        self.setStyleSheet(AppStyle().get_editor_parent() + AppStyle().get_editor_preview())

        # Setup WebChannel
        self.channel = QWebChannel(self)
        self.channel.registerObject("document", self.document)
        self.preview.page().setWebChannel(self.channel)

        # Load HTML file
        html_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "resources",
                "index.html"))
        self.preview.setUrl(QUrl.fromLocalFile(html_path))
        # Add these settings with corrected import
        self.preview.page().settings().setAttribute(
            QtWebEngineCore.QWebEngineSettings.ErrorPageEnabled, True)
        # 禁用不必要的功能
        self.preview.page().settings().setAttribute(
            QtWebEngineCore.QWebEngineSettings.PluginsEnabled, False)
        self.preview.page().settings().setAttribute(
            QtWebEngineCore.QWebEngineSettings.JavascriptCanOpenWindows, False)
        self.preview.page().settings().setAttribute(
            QtWebEngineCore.QWebEngineSettings.LocalStorageEnabled, True)

    def update_theme(self, theme):
        """Switch the Cherry Markdown theme."""
        js_code = f"""
            if (window.editor) {{
                window.editor.setTheme('{theme}');
            }}
        """
        self.preview.page().runJavaScript(js_code)

    def reset(self):
        self.document.file_id = ""
        self.document.file_name = ""
        self.document.reset()  # 调用文档的 reset 方法
        # 执行 JavaScript 清空编辑区内容
        js_code = """
            if (window.editor) {
                window.editor.setValue('');
            }
        """
        self.preview.page().runJavaScript(js_code)

    def set_file_id(self, file_id):
        self.document.file_id = file_id

    def set_file_name(self, file_name):
        self.document.file_name = file_name

    def set_text_content(self, text_content):
        self.document.set_text(text_content)

    def resizeEvent(self, event):
        """窗口大小改变时触发，确保编辑区高度自适应"""
        super().resizeEvent(event)
        # 可以在这里添加额外的调整逻辑
        # 布局管理器会自动处理子部件的大小

    def handle_js_console_message(self, level, message, line_number, source_id):
        """处理 JavaScript 控制台消息"""
        level_map = {
            QWebEnginePage.InfoMessageLevel: "INFO",
            QWebEnginePage.WarningMessageLevel: "WARNING",
            QWebEnginePage.ErrorMessageLevel: "ERROR"
        }
        log_level = level_map.get(level, "UNKNOWN")
        logger.info(f"JS {log_level}: {message} at {source_id}:{line_number}")
