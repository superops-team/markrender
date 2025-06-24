# -*- coding: utf-8 -*-
import sys
import logging
import os
import sys
import traceback
from logging import StreamHandler


# 主窗口必要的导入
from PySide6.QtWidgets import QApplication, QMainWindow
from db_manager import ThemeManager
import init_db

# 其他包懒加载
markdown = None
Qt = None
QTimer = None
QWebEngineView = None
QComboBox = None
QFileDialog = None
QHBoxLayout = None
QInputDialog = None
QLabel = None
QMessageBox = None
QSplitter = None
QTextEdit = None
QToolBar = None
QVBoxLayout = None
QWidget = None
ThemeManagerGUI = None


def setup_logging():
    # 创建日志器
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 创建文件处理器
    log_file = os.path.join(init_db.get_user_data_dir(), 'app.log')

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # 创建控制台处理器
    console_handler = StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # 将处理器添加到日志器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger = logging.getLogger(__name__)
    return logger


def init_themes():
    # 检测 markrender.db 文件是否存在
    db_path = init_db.get_db_path('markrender.db')
    theme_manager = ThemeManager(db_path=db_path)
    init_db.init_themes(theme_manager)  # 假设 init_db.py 中有 main 函数用于初始化
    return theme_manager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        global markdown, Qt, QTimer, QWebEngineView, QComboBox, QFileDialog, QHBoxLayout, QInputDialog, QLabel, QMessageBox, QSplitter, QTextEdit, QToolBar, QVBoxLayout, QWidget, ThemeManagerGUI
        if markdown is None:
            import markdown
        if Qt is None:
            from PySide6.QtCore import Qt, QTimer
        if QWebEngineView is None:
            from PySide6.QtWebEngineWidgets import QWebEngineView
        if QComboBox is None:
            from PySide6.QtWidgets import QComboBox, QFileDialog, QHBoxLayout, QInputDialog, QLabel, QMessageBox, QSplitter, QTextEdit, QToolBar, QVBoxLayout, QWidget
        if ThemeManagerGUI is None:
            from theme_manager_gui import ThemeManagerGUI
        self.theme_manager = init_themes()
        self.theme_manager_gui = ThemeManagerGUI(self, self.theme_manager)
        self.setWindowTitle("MarkRender")
        self.setGeometry(100, 100, 800, 600)

        # 创建工具栏
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        # 初始化 text_edit
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("在此输入 Markdown 文本...")
        self.text_edit.textChanged.connect(self.update_preview)

        # 初始化 webview
        self.webview = QWebEngineView()

        # 添加样式选择器
        style_layout = QHBoxLayout()
        style_label = QLabel("样式:")
        self.style_combobox = QComboBox()
        self.style_combobox.addItems(self.theme_manager_gui.get_theme_names())
        self.style_combobox.currentIndexChanged.connect(self.update_preview)

        # 添加标题颜色选择器
        color_layout = QHBoxLayout()
        color_label = QLabel("标题颜色:")
        self.color_button = QLabel("■")
        self.color_button.setToolTip("点击选择标题颜色")
        self.color_button.mousePressEvent = self.theme_manager_gui.select_title_color

        style_widget = QWidget()
        style_layout.addWidget(style_label)
        style_layout.addWidget(self.style_combobox)
        style_layout.addLayout(color_layout)
        style_layout.addWidget(color_label)
        style_layout.addWidget(self.color_button)
        style_widget.setLayout(style_layout)

        self.toolbar.addWidget(style_widget)
        self.toolbar.addSeparator()

        # 导出按钮
        export_image_button = self.toolbar.addAction("导出图片")
        export_image_button.triggered.connect(self.export_image)
        self.text_edit.setPlaceholderText("在此输入 Markdown 文本...")
        self.text_edit.textChanged.connect(self.update_preview)
        export_pdf_button = self.toolbar.addAction("导出PDF")
        export_pdf_button.triggered.connect(self.export_pdf)

        # 添加新的主题管理按钮
        theme_management_button = self.toolbar.addAction("主题管理")

        def refresh_style_combobox():
            self.theme_manager_gui.show_theme_management_dialog()
            self.style_combobox.clear()
            self.style_combobox.addItems(
                self.theme_manager_gui.get_theme_names())

        theme_management_button.triggered.connect(refresh_style_combobox)

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

    def get_current_style(self):
        return self.theme_manager_gui.get_current_style()

    def update_preview(self):
        """将 Markdown 转换为 HTML 并更新预览区"""
        markdown_text = self.text_edit.toPlainText()

        # 使用fenced_code和codehilite扩展
        html = markdown.markdown(
            markdown_text,
            extensions=["tables", "fenced_code", "codehilite"],
            extension_configs={
                "codehilite": {
                    "linenums": False,
                    "guess_lang": True,
                    "css_class": "hljs",
                    "pygments_style": "default",
                }
            },
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
        file_name, _ = QFileDialog.getSaveFileName(
            self, "保存图片", "", "PNG 文件 (*.png);;JPEG 文件 (*.jpg)"
        )
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
        file_name, _ = QFileDialog.getSaveFileName(
            self, "保存PDF", "", "PDF 文件 (*.pdf)"
        )
        if file_name:
            if not file_name.endswith(".pdf"):
                file_name += ".pdf"
            # 等待页面加载
            QTimer.singleShot(500, lambda: self.save_pdf(file_name))

    def save_pdf(self, file_name):
        """保存PDF"""
        self.webview.page().printToPdf(file_name)

    def get_base_style(self):
        return """<style>
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
        </style>"""


if __name__ == "__main__":
    logger = setup_logging()
    logger.info("应用启动")
    try:
        logger.info(f"工作目录: {os.getcwd()}")
        logger.info(f"应用路径: {init_db.get_app_path()}")
        logger.info(f"数据库路径: {init_db.get_db_path('markrender.db')}")
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        error_msg = traceback.format_exc()
        logger.critical(f"致命错误: {e}\n{error_msg}")
        # 可以显示一个错误对话框
        from PySide6.QtWidgets import QMessageBox
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(f"应用遇到致命错误: {str(e)}")
        msg_box.setDetailedText(error_msg)
        msg_box.setWindowTitle("错误")
        msg_box.exec()
        sys.exit(1)
