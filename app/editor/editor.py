import os
from utils import logger
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6 import QtWebEngineCore  # Add this import
from PySide6.QtCore import QUrl, QObject, Signal, Property
from PySide6.QtWebChannel import QWebChannel


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

    def load_more(self):
        logger.debug(
            f'load_more, file_id: {
                self.file_id}, _loaded_lines: {
                self._loaded_lines}, _page_size: {
                self._page_size}, _lines: {
                    self._lines}')
        start = self._loaded_lines
        end = start + self._page_size
        page_text = '\n'.join(self._lines[start:end])
        if page_text:
            self._loaded_lines = end
            self.text_changed.emit(page_text)

    def reset(self):
        """重置文档状态"""
        self._text = ""
        self._lines = []
        self._loaded_lines = 0
        self.text_changed.emit("")  # 发射清空内容的信号

    text_changed = Signal(str)
    text = Property(str, get_text, set_text, notify=text_changed)


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

        # 创建布局
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.preview)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(0)
        self.setLayout(layout)

        # 设置圆角样式
        self.setStyleSheet('''
            QWidget {  /* 父容器样式 */
                border: 2px solid #ddd;
                padding: 0;
            }
            QWebEngineView {  /* 预览视图样式 */
                border: none;
                background-color: transparent; /* 设置透明背景 */
                margin: 0; /* 移除抵消布局的 margin */
                padding: 0; /* 移除补充的 padding */
            }
        ''')

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

    def export_to_pdf(self):
        pass
