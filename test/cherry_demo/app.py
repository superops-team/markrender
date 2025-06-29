import sys
import os
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QToolBar, QComboBox, QPushButton
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtCore import QObject

class MarkdownDocument(QObject):
    def __init__(self):
        super().__init__()
        self._text = ""

    def get_text(self):
        return self._text

    def set_text(self, text):
        self._text = text
        self.text_changed.emit(text)

    from PySide6.QtCore import Signal, Property
    text_changed = Signal(str)
    text = Property(str, get_text, set_text, notify=text_changed)

class MarkdownEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cherry Markdown Editor")
        self.resize(1000, 600)

        # Initialize document for WebChannel
        self.document = MarkdownDocument()

        # Setup GUI
        self.setup_ui()

    def setup_ui(self):
        # Toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Toolbar buttons
        open_btn = QPushButton("Open")
        save_btn = QPushButton("Save")
        toolbar.addWidget(open_btn)
        toolbar.addWidget(save_btn)
        open_btn.clicked.connect(self.open_file)
        save_btn.clicked.connect(self.save_file)

        # Theme selection
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["default", "dark", "light"])
        self.theme_combo.currentTextChanged.connect(self.update_theme)
        toolbar.addWidget(self.theme_combo)

        # Web view for Cherry Markdown
        self.preview = QWebEngineView()

        # 创建一个中央部件和布局
        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.preview)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Setup WebChannel
        self.channel = QWebChannel(self)
        self.channel.registerObject("content", self.document)
        self.preview.page().setWebChannel(self.channel)

        # Load HTML file
        html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources", "index.html"))
        self.preview.setUrl(QUrl.fromLocalFile(html_path))

        # 注入 JavaScript 禁止页面滚动
        disable_scroll_js = """
        document.addEventListener('DOMContentLoaded', function() {
            document.body.style.overflow = 'hidden';
            const editorElement = document.getElementById('editor');
            if (editorElement) {
                editorElement.style.overflow = 'hidden';
            }
        });
        """
        self.preview.page().runJavaScript(disable_scroll_js)

    def update_theme(self, theme):
        """Switch the Cherry Markdown theme."""
        js_code = f"""
            if (window.editor) {{
                window.editor.setTheme('{theme}');
            }}
        """
        self.preview.page().runJavaScript(js_code)

    def open_file(self):
        """Open a Markdown file and set it in Cherry Markdown."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Markdown Files (*.md)")
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
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
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Markdown Files (*.md)")
        if file_path:
            # Retrieve raw Markdown content from Cherry Markdown
            def handle_markdown_content(content):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = MarkdownEditor()
    editor.show()
    sys.exit(app.exec())