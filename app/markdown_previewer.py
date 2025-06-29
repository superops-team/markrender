from ui.dayu_widgets import MLoadingWrapper, MMessage, MTextEdit
from utils.logger_utils import logger

from PySide6.QtWebEngineWidgets import QWebEngineView
import markdown
import os
from PySide6.QtWidgets import QWidget, QVBoxLayout


class MarkdownPreviewer(QWidget):
    def __init__(self, theme_manager_gui, parent=None):
        super().__init__(parent)
        self.webview = QWebEngineView()
        self.theme_manager_gui = theme_manager_gui
        self.loading_wrapper = MLoadingWrapper(self.webview)
        self.loading_wrapper.set_dayu_loading(False)
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.loading_wrapper)
        self.setLayout(self.main_layout)
        self.setup_webview()
        self.init_ui()
        self.init_theme()

    def setup_webview(self):
        self.webview.loadFinished.connect(self.handle_load_finished)

    def handle_load_finished(self, ok):
        try:
            self.loading_wrapper.set_dayu_loading(False)
        except AttributeError:
            pass

    def init_ui(self):
        """初始化预览器布局，使用 dayu_widgets 风格优化"""
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        self.main_layout.setSpacing(12)
        self.setStyleSheet('QWidget { background-color: #fafafa; }')

    def init_theme(self):
        """初始化主题配置，适配 dayu_widgets 主题"""
        if self.theme_manager_gui:
            self.theme_manager_gui.theme_changed.connect(self.update_theme)
            self.update_theme()

    def update_theme(self):
        """更新主题样式"""
        if self.theme_manager_gui:
            theme_style = self.theme_manager_gui.get_current_style()
            # 可根据主题类型动态设置不同的样式
            if self.theme_manager_gui.is_dark_theme():
                self.setStyleSheet('QWidget { background-color: #1f1f1f; }')
            else:
                self.setStyleSheet('QWidget { background-color: #fafafa; }')

    def mermaid_format(self, source, language, class_name):
        """格式化Mermaid图表代码"""
        return f'<div class="{class_name}">{source}</div>'

    def export_pdf(self, file_path):
        """导出PDF功能，使用 dayu_widgets 消息提示"""
        logger.info('触发导出PDF功能')
        try:
            def save_pdf(pdf_data):
                if pdf_data:
                    with open(file_path, 'wb') as f:
                        f.write(pdf_data)
                    logger.info(f'PDF成功导出至 {file_path}')
                    # 检查 parent 控件是否有效
                    MMessage.success(
                        f'PDF成功导出至 {file_path}',
                        parent=self.parent,
                        duration=5)
                else:
                    logger.error('未获取到PDF数据，导出失败')
                    # 检查 parent 控件是否有效
                    MMessage.error(
                        '未获取到PDF数据，导出失败',
                        parent=self.parent,
                        duration=3)

            self.webview.page().printToPdf(save_pdf)
        except Exception as e:
            logger.error(f'PDF导出失败: {str(e)}')
            # 检查 parent 控件是否有效
            MMessage.error(
                f'PDF导出失败: {
                    str(e)}',
                parent=self.parent,
                duration=3)

    def render_markdown(self, markdown_text):
        """将Markdown文本渲染为HTML并显示，优化主题适配"""
        try:
            self.loading_wrapper.set_dayu_loading(True)
        except AttributeError:
            pass
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

        # 获取当前主题状态
        is_dark = self.theme_manager_gui.is_dark_theme() if self.theme_manager_gui else False
        theme = 'dark' if is_dark else 'default'

        # 添加选中的样式、代码高亮库和 dayu_widgets 主题样式
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            {self.theme_manager_gui.get_current_style() if self.theme_manager_gui else ''}
            <link rel="stylesheet" href="file://{os.path.join(os.path.dirname(__file__), '../../ui/assets/highlight.min.css')}">
            <link rel="stylesheet" href="file://{os.path.join(os.path.dirname(__file__), '../../ui/assets/mermaid.min.css')}">
            <link rel="stylesheet" href="file://{os.path.join(os.path.dirname(__file__), '../../ui/dayu_widgets/static/theme.css')}">
            <style>body {{ --theme: {theme}; }}</style>
            <script src="file://{os.path.join(os.path.dirname(__file__), '../../ui/assets/highlight.min.js')}"></script>
            <script src="file://{os.path.join(os.path.dirname(__file__), '../../ui/assets/mermaid.min.js')}"></script>
            <script>
                document.addEventListener('DOMContentLoaded', (event) => {{
                    if (window.hljs) {{
                        hljs.highlightAll();
                    }}
                    if (window.mermaid) {{
                        mermaid.initialize({{
                            theme: '{theme}',
                            fontFamily: '"Microsoft YaHei", "SimSun", Arial, sans-serif',
                            flowchart: {{
                                useMaxWidth: true,
                                htmlLabels: true,
                                curve: 'basis'
                            }},
                            themeVariables: {{
                                fontSize: '14px',
                                primaryColor: '#1890ff',
                                secondaryColor: '#fafafa',
                                background: '{"#1f1f1f" if is_dark else "#fafafa"}'
                            }}
                        }});
                    }}
                    // 应用 dayu_widgets 主题样式
                    const style = document.createElement('style');
                    style.textContent = `
                        body {{
                            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                            color: {'#fff' if is_dark else '#333'};
                            background-color: {'#1f1f1f' if is_dark else '#fafafa'};
                            line-height: 1.5;
                        }}
                        a {{
                            color: #40a9ff;
                            text-decoration: none;
                        }}
                        a:hover {{
                            text-decoration: underline;
                        }}
                        .hljs {{
                            background-color: {'#2d2d2d' if is_dark else '#f8f9fa'};
                        }}
                    `;
                    document.head.appendChild(style);
                }});
            </script>
        </head>
        <body>
            {html}
        </body>
        </html>
        """

        self.webview.setHtml(full_html)
