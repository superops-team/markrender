import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QVBoxLayout,
                             QWidget, QSplitter, QToolBar, QFileDialog,
                             QComboBox, QLabel, QHBoxLayout, QColorDialog)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor
import markdown

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Markdown 编辑器与预览器")
        self.setGeometry(100, 100, 800, 600)

        # 初始化标题颜色
        self.title_color = "#333333"

        # 创建工具栏
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # 添加样式选择器
        style_layout = QHBoxLayout()
        style_label = QLabel("Markdown样式:")
        self.style_combobox = QComboBox()
        self.style_combobox.addItems([
            "默认样式",
            "GitHub风格",
            "浅色主题",
            "深色主题",
            "文档风格"
        ])
        self.style_combobox.currentIndexChanged.connect(self.update_preview)

        # 添加标题颜色选择器
        color_layout = QHBoxLayout()
        color_label = QLabel("标题颜色:")
        self.color_button = QLabel("■")
        self.color_button.setStyleSheet(f"color: {self.title_color}; font-size: 18px;")
        self.color_button.setToolTip("点击选择标题颜色")
        self.color_button.mousePressEvent = self.select_title_color

        style_widget = QWidget()
        style_layout.addWidget(style_label)
        style_layout.addWidget(self.style_combobox)
        style_layout.addLayout(color_layout)
        style_layout.addWidget(color_label)
        style_layout.addWidget(self.color_button)
        style_widget.setLayout(style_layout)

        toolbar.addWidget(style_widget)
        toolbar.addSeparator()

        # 导出按钮
        export_image_button = toolbar.addAction("导出图片")
        export_image_button.triggered.connect(self.export_image)
        
        export_pdf_button = toolbar.addAction("导出PDF")
        export_pdf_button.triggered.connect(self.export_pdf)

        # 创建左右布局
        splitter = QSplitter(Qt.Horizontal)

        # 左侧 Markdown 编辑区
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("在此输入 Markdown 文本...")
        self.text_edit.textChanged.connect(self.update_preview)
        splitter.addWidget(self.text_edit)

        # 右侧预览区
        self.webview = QWebEngineView()
        splitter.addWidget(self.webview)

        # 设置主布局
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(splitter)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 初始化预览
        self.update_preview()

    def select_title_color(self, event):
        """打开颜色选择对话框"""
        color = QColorDialog.getColor(QColor(self.title_color), self, "选择标题颜色")
        if color.isValid():
            self.title_color = color.name()
            self.color_button.setStyleSheet(f"color: {self.title_color}; font-size: 18px;")
            self.update_preview()

    def get_current_style(self):
        """根据当前选择返回对应的CSS样式"""
        # 基础样式：代码高亮和一级标题样式
        base_style = f"""
            <style>
                /* 一级标题居中并设置颜色 */
                h1 {{
                    text-align: center;
                    color: {self.title_color};
                }}

                /* 代码高亮样式 */
                pre {{
                    background-color: #f6f8fa;
                    border-radius: 3px;
                    font-size: 85%;
                    line-height: 1.45;
                    overflow: auto;
                    padding: 16px;
                }}

                code {{
                    background-color: rgba(27,31,35,.05);
                    border-radius: 3px;
                    font-family: SFMono-Regular,Consolas,Liberation Mono,Menlo,monospace;
                    font-size: 85%;
                    margin: 0;
                    padding: 0.2em 0.4em;
                }}

                /* 代码块高亮 */
                .hljs {{
                    display: block;
                    overflow-x: auto;
                    padding: 0.5em;
                    color: #333;
                    background: #f8f8f8;
                }}

                /* 不同语言高亮样式 */
                .language-python .hljs-keyword {{ color: #0000FF; }}
                .language-python .hljs-string {{ color: #008000; }}
                .language-python .hljs-number {{ color: #0000CD; }}
                .language-python .hljs-comment {{ color: #808080; }}

                .language-javascript .hljs-keyword {{ color: #0000FF; }}
                .language-javascript .hljs-string {{ color: #008000; }}
                .language-javascript .hljs-number {{ color: #0000CD; }}
                .language-javascript .hljs-comment {{ color: #808080; }}

                .language-html .hljs-tag {{ color: #000080; }}
                .language-html .hljs-attr {{ color: #FF0000; }}
                .language-html .hljs-string {{ color: #008000; }}

                .language-css .hljs-selector-tag {{ color: #000080; }}
                .language-css .hljs-property {{ color: #FF0000; }}
                .language-css .hljs-value {{ color: #008000; }}
            </style>
        """

        # 主题样式
        themes = {
            "默认样式": """
                <style>
                    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif; }
                    h2 { border-bottom: 1px solid #eaecef; }
                    blockquote { border-left: 0.25em solid #dfe2e5; padding: 0 1em; color: #6a737d; }
                    table { border-collapse: collapse; }
                    th, td { border: 1px solid #dfe2e5; padding: 6px 13px; }
                </style>
            """,
            "GitHub风格": """
                <style>
                    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif; }
                    h2 { font-size: 1.5em; border-bottom: 1px solid #eaecef; }
                    blockquote { border-left: 0.25em solid #dfe2e5; padding: 0 1em; color: #6a737d; }
                    table { border-collapse: collapse; }
                    th, td { border: 1px solid #dfe2e5; padding: 6px 13px; }
                </style>
            """,
            "浅色主题": """
                <style>
                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #f9f9f9;
                        color: #333;
                    }
                    h2 { color: #1a1a1a; border-bottom: 1px solid #ddd; }
                    blockquote { border-left: 3px solid #666; color: #555; }
                    table { border-collapse: collapse; }
                    th, td { border: 1px solid #ddd; padding: 6px 13px; }
                </style>
            """,
            "深色主题": """
                <style>
                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #2d2d2d;
                        color: #e9e9e9;
                    }
                    h2 { color: #fff; border-bottom: 1px solid #444; }
                    blockquote { border-left: 3px solid #777; color: #bbb; }
                    a { color: #61afef; }
                    table { border-collapse: collapse; }
                    th, td { border: 1px solid #444; padding: 6px 13px; }
                </style>
            """,
            "文档风格": """
                <style>
                    body {
                        font-family: 'Times New Roman', Times, serif;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                    }
                    h2 { font-family: Arial, sans-serif; font-size: 22px; }
                    blockquote { font-style: italic; }
                    table { border-collapse: collapse; }
                    th, td { border: 1px solid #ccc; padding: 6px 13px; }
                </style>
            """
        }

        return base_style + themes[self.style_combobox.currentText()]

    def update_preview(self):
        """将 Markdown 转换为 HTML 并更新预览区"""
        markdown_text = self.text_edit.toPlainText()

        # 使用fenced_code和codehilite扩展
        html = markdown.markdown(
            markdown_text,
            extensions=['tables', 'fenced_code', 'codehilite'],
            extension_configs={
                'codehilite': {
                    'linenums': False,
                    'guess_lang': True,
                    'css_class': 'hljs',
                    'pygments_style': 'default',
                }
            }
        )

        # 添加选中的样式和代码高亮库
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            {self.get_current_style()}
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/default.min.css">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
            <script>
                document.addEventListener('DOMContentLoaded', (event) => {{
                    if (window.hljs) {{
                        hljs.highlightAll();
                    }}
                }});
            </script>
        </head>
        <body>
            {html}
        </body>
        </html>
        """

        self.webview.setHtml(full_html)

    def export_image(self):
        """导出图片"""
        file_name, _ = QFileDialog.getSaveFileName(self, "保存图片", "", "PNG 文件 (*.png);;JPEG 文件 (*.jpg)")
        if file_name:
            # 等待页面加载
            QTimer.singleShot(500, lambda: self.save_image(file_name))

    def save_image(self, file_name):
        """保存图片"""
        image = self.webview.grab().toImage()
        if not image.save(file_name):
            print(f"保存图片失败: {file_name}")

    def export_pdf(self):
        """导出PDF"""
        file_name, _ = QFileDialog.getSaveFileName(self, "保存PDF", "", "PDF 文件 (*.pdf)")
        if file_name:
            if not file_name.endswith('.pdf'):
                file_name += '.pdf'
            # 等待页面加载
            QTimer.singleShot(500, lambda: self.save_pdf(file_name))

    def save_pdf(self, file_name):
        """保存PDF"""
        self.webview.page().printToPdf(file_name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())