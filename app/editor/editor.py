import os
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6 import QtWebEngineCore  # Add this import
from PySide6.QtCore import QUrl
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QObject, Signal, Property

class MarkdownDocument(QObject):
    def __init__(self):
        super().__init__()
        self._text = ""

    def get_text(self):
        return self._text

    def set_text(self, text):
        self._text = text
        self.text_changed.emit(text)
    
    text_changed = Signal(str)
    text = Property(str, get_text, set_text, notify=text_changed)

class MarkdownEditor(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Initialize document for WebChannel
        self.document = MarkdownDocument()
        # Setup GUI
        self.setup_ui()

    def setup_ui(self):
        # Web view for Cherry Markdown
        self.preview = QWebEngineView()

        # 创建布局
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.preview)
        layout.setContentsMargins(0, 0, 0, 0)
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
        self.channel.registerObject("content", self.document)
        self.preview.page().setWebChannel(self.channel)

        # Load HTML file
        html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources", "index.html"))
        self.preview.setUrl(QUrl.fromLocalFile(html_path))
        # Add these settings with corrected import
        self.preview.page().settings().setAttribute(QtWebEngineCore.QWebEngineSettings.JavascriptEnabled, True)
        self.preview.page().settings().setAttribute(QtWebEngineCore.QWebEngineSettings.LocalStorageEnabled, True)
        self.preview.page().settings().setAttribute(QtWebEngineCore.QWebEngineSettings.ErrorPageEnabled, True)

    def update_theme(self, theme):
        """Switch the Cherry Markdown theme."""
        js_code = f"""
            if (window.editor) {{
                window.editor.setTheme('{theme}');
            }}
        """
        self.preview.page().runJavaScript(js_code)
    
    def set_text_content(self, text_content):
        self.document.set_text(text_content)

    def open_file(self):
        """Open a Markdown file and set it in Cherry Markdown."""
        self.current_file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Markdown Files (*.md)")
        if self.current_file_path:
            with open(self.current_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.document.set_text(content)
                js_code = f"""
                    if (window.editor) {{
                        window.editor.setValue('{content.replace("'", "\\'").replace("\n", "\\n")}');
                    }}
                """
                self.preview.page().runJavaScript(js_code)

    def save_file(self):
        """Save the raw Markdown content from Cherry Markdown."""
        # Retrieve raw Markdown content from Cherry Markdown
        def handle_markdown_content(content):
            if content:
                self.parent.markdown_manager.save_markdown('test', content)
            else:
                logger.error("Failed to get Markdown content from editor")

        js_code = """
            if (window.editor) {
                window.editor.getMarkdown();
            } else {
                '';
            }
        """
        self.preview.page().runJavaScript(js_code, handle_markdown_content)

    def resizeEvent(self, event):
        """窗口大小改变时触发，确保编辑区高度自适应"""
        super().resizeEvent(event)
        # 可以在这里添加额外的调整逻辑
        # 布局管理器会自动处理子部件的大小
    
    def export_to_pdf(self):
        pass
    
  