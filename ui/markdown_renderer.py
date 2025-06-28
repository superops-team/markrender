from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
import markdown

class MarkdownRenderer(QWidget):
    def __init__(self, theme_manager_gui, parent=None):
        super().__init__(parent)
        self.webview = QWebEngineView()
        self.theme_manager_gui = theme_manager_gui
        self.init_ui()

    def init_ui(self):
        """初始化渲染器布局"""
        layout = QVBoxLayout(self)
        layout.addWidget(self.webview)
        self.setLayout(layout)

    def mermaid_format(self, source, language, class_name):
        """格式化Mermaid图表代码"""
        return f'<div class="{class_name}">{source}</div>'

    def render_markdown(self, markdown_text):
        """将Markdown文本渲染为HTML并显示"""
        # 使用fenced_code和codehilite扩展
        html = markdown.markdown(
            markdown_text,
            extensions=[
                "tables",
                "fenced_code",
                "codehilite",
                "attr_list",
                "pymdownx.highlight",
                "pymdownx.tasklist",
                "pymdownx.b64",
                "pymdownx.superfences"],
            extension_configs={
                "codehilite": {
                    "linenums": False,
                    "guess_lang": True,
                    "css_class": "hljs",
                    "pygments_style": "default",
                },
                'pymdownx.superfences': {
                    'custom_fences': [
                        {
                            'name': 'mermaid',         # 识别 ```mermaid 代码块
                            'class': 'mermaid',        # 添加 "mermaid" 类
                            'format': self.mermaid_format   # 使用自定义格式化函数
                        }
                    ]
                }
            },
        )

        # 添加选中的样式和代码高亮库
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            {self.theme_manager_gui.get_current_style() if self.theme_manager_gui.get_current_style() else self.theme_manager_gui.get_base_style()}
            <link rel="stylesheet" href="assets/highlight.min.css">    <link rel="stylesheet" href="assets/mermaid.min.css">
            <script src="assets/highlight.min.js"></script>
            <script src="assets/mermaid.min.js"></script>
            <script>
                document.addEventListener('DOMContentLoaded', (event) => {{
                    if (window.hljs) {{
                        hljs.highlightAll();
                    }}
                    if (window.mermaid) {{{{
                        mermaid.initialize({{
                            theme: 'default',
                            fontFamily: '"Microsoft YaHei", "SimSun", Arial, sans-serif',
                            flowchart: {{
                                useMaxWidth: true,
                                htmlLabels: true,
                                curve: 'basis'
                            }}
                        }});
                    }}}}
                }});
            </script>
        </head>
        <body>
            {html}
        </body>
        </html>
        """

        self.webview.setHtml(full_html)