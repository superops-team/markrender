# -*- coding: utf-8 -*-
import sys
import logging
import os
import sys
import traceback
import logging

from logging import StreamHandler


# 主窗口必要的导入
from PySide6.QtWidgets import QApplication, QMainWindow, QLineEdit, QListWidget, QPushButton
from PySide6.QtGui import QAction
from PySide6 import QtCore
from db_manager import ThemeManager
import pymdownx
from pymdownx import superfences
from markdown_history_manager import MarkdownHistoryManager
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
    def toggle_history_panel(self):
        from PySide6.QtGui import QIcon
        if self.history_widget.isVisible():
            self.history_widget.hide()
            from PySide6.QtWidgets import QStyle
            icon = self.style().standardIcon(QStyle.SP_TitleBarShadeButton)
            if not icon.isNull():
                self.toggle_history_button.setIcon(icon)
            else:
                logging.warning('Failed to load icon: format-justify-fill.svg')
        else:
            self.history_widget.show()
            from PySide6.QtWidgets import QStyle
            icon = self.style().standardIcon(QStyle.SP_TitleBarUnshadeButton)
            if not icon.isNull():
                self.toggle_history_button.setIcon(icon)
            else:
                logging.warning('Failed to load icon: format-justify.svg')

    def rename_selected_file(self):
        from PySide6.QtWidgets import QInputDialog
        selected_items = self.history_list.selectedItems()
        if selected_items:
            item = selected_items[0]
            old_title = item.text()
            new_title, ok = QInputDialog.getText(
                self, '重命名标题', '请输入新标题:', text=old_title)
            if ok and new_title:
                from sqlalchemy.orm import Session
                from markdown_history_manager import MarkdownFileHistory
                with Session(self.markdown_history_manager.engine) as session:
                    history = session.query(MarkdownFileHistory).filter(
                        MarkdownFileHistory.title == old_title).first()
                    if history:
                        history.title = new_title
                        session.commit()
                self.load_history()

    def create_new_markdown(self):
        from PySide6.QtWidgets import QTextEdit, QDialog, QVBoxLayout, QPushButton, QLineEdit, QLabel
        dialog = QDialog(self)
        dialog.setWindowTitle('新建')
        layout = QVBoxLayout()
        title_label = QLabel('标题:')
        title_input = QLineEdit()
        content_label = QLabel('Markdown 内容:')
        text_edit = QTextEdit()
        save_button = QPushButton('保存')
        save_button.clicked.connect(
            lambda: self.save_new_markdown(
                title_input.text(),
                text_edit.toPlainText(),
                dialog))
        layout.addWidget(title_label)
        layout.addWidget(title_input)
        layout.addWidget(content_label)
        layout.addWidget(text_edit)
        layout.addWidget(save_button)
        dialog.setLayout(layout)
        dialog.exec()

    def save_new_markdown(self, title, content, dialog):
        from datetime import datetime
        from sqlalchemy.orm import Session
        from markdown_history_manager import MarkdownFileHistory
        theme_names = self.theme_manager_gui.get_theme_names()
        first_theme_style = self.theme_manager_gui.get_theme_css(
            theme_names[0]) if theme_names else ''
        new_file = MarkdownFileHistory(
            title=title,
            content=content,
            tags='',
            render_style=first_theme_style,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        dialog.close()
        with Session(self.markdown_history_manager.engine) as session:
            session.add(new_file)
            session.commit()
        self.load_history()

    def save_markdown_history(self):
        """保存 Markdown 变更历史"""
        current_title = self.history_list.currentItem().text(
        ) if self.history_list.currentItem() else "Untitled"
        histories = self.markdown_history_manager.get_file_history(
            current_title)
        if histories:
            old_content = histories[0].content
            new_content = self.text_edit.toPlainText()
            if old_content != new_content:
                self.markdown_history_manager.save_change_history(
                    histories[0].id, old_content, new_content)
                # 更新文件内容
                histories = self.markdown_history_manager.get_file_history(
                    current_title)
                if histories:
                    histories[0].content = new_content
                    with self.markdown_history_manager.Session() as session:
                        session.merge(histories[0])
                        session.commit()

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
        db_path = init_db.get_db_path('markrender.db')
        self.theme_manager = init_themes()
        self.markdown_history_manager = MarkdownHistoryManager(db_path)
        self.theme_manager_gui = ThemeManagerGUI(self, self.theme_manager)
        self.setWindowTitle("MarkRender")
        self.showMaximized()

        # 创建工具栏
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        # 初始化 text_edit
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("在此输入 Markdown 文本...")
        self.text_edit.textChanged.connect(self.save_markdown_history)
        self.text_edit.textChanged.connect(self.update_preview)

        # 初始化 webview
        self.webview = QWebEngineView()

        # 添加样式选择器
        style_layout = QHBoxLayout()
        style_label = QLabel("样式:")
        self.style_combobox = QComboBox()
        self.style_combobox.addItems(self.theme_manager_gui.get_theme_names())
        self.style_combobox.currentIndexChanged.connect(self.update_preview)

        style_widget = QWidget()
        style_layout.addWidget(style_label)
        style_layout.addWidget(self.style_combobox)
        style_widget.setLayout(style_layout)

        # 设置展开折叠按钮图标
        from PySide6.QtGui import QIcon
        from PySide6.QtWidgets import QStyle
        icon = self.style().standardIcon(QStyle.SP_TitleBarShadeButton)
        if not icon.isNull():
            self.toggle_history_button = self.toolbar.addAction(icon, "")
        else:
            logging.warning('Failed to load icon: format-justify-fill.svg')
            self.toggle_history_button = self.toolbar.addAction(
                "展开/折叠左侧目录", None)
        self.toggle_history_button.triggered.connect(self.toggle_history_panel)
        self.toolbar.insertAction(
            self.toolbar.actions()[0],
            self.toggle_history_button)
        self.toolbar.setIconSize(QtCore.QSize(24, 24))

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

        # 创建三栏布局
        splitter = QSplitter(Qt.Horizontal)

        # 左侧 Markdown 历史栏
        self.history_widget = QWidget()
        history_layout = QVBoxLayout()

        # 搜索输入框和按钮
        self.new_markdown_button = QPushButton('新建 Markdown')
        from PySide6.QtWidgets import QStyle
        self.new_markdown_button.setIcon(
            self.style().standardIcon(
                QStyle.SP_FileIcon))
        self.new_markdown_button.clicked.connect(self.create_new_markdown)
        self.search_input = QLineEdit()
        self.search_button = QPushButton("搜索")
        self.search_button.clicked.connect(self.search_history)

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)

        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.show_history_content)
        self.history_list.setContextMenuPolicy(Qt.ActionsContextMenu)
        delete_action = QAction('删除', self.history_list)
        delete_action.triggered.connect(self.delete_selected_file)
        rename_action = QAction('重命名', self.history_list)
        rename_action.triggered.connect(self.rename_selected_file)
        self.history_list.addAction(delete_action)
        self.history_list.addAction(rename_action)

        self.new_markdown_button = QPushButton('新建 Markdown')
        from PySide6.QtWidgets import QStyle
        self.new_markdown_button.setIcon(
            self.style().standardIcon(
                QStyle.SP_FileIcon))
        self.new_markdown_button.clicked.connect(self.create_new_markdown)
        history_layout.addWidget(self.new_markdown_button)
        history_layout.addLayout(search_layout)
        history_layout.addWidget(self.history_list)
        self.history_widget.setLayout(history_layout)
        splitter.addWidget(self.history_widget)
        self.history_widget.show()

        # 中间 Markdown 编辑区
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

        # 初始化历史列表
        self.load_history()

        # 初始化预览
        self.update_preview()

    def load_history(self):
        # Assume we want to get all files, so we can iterate through all possible paths
        # This is a workaround, better to implement a proper
        # get_all_file_history method in the future
        from sqlalchemy.orm import Session
        from markdown_history_manager import MarkdownFileHistory

        with Session(self.markdown_history_manager.engine) as session:
            histories = session.query(MarkdownFileHistory).all()
        self.history_list.clear()
        for history in histories:
            self.history_list.addItem(history.title)

    def search_history(self):
        keyword = self.search_input.text()
        if not keyword:
            # 当关键词为空时，加载所有历史记录
            self.load_history()
        else:
            histories = self.markdown_history_manager.search_file_history(
                keyword)
            self.history_list.clear()
            for history in histories:
                self.history_list.addItem(history.title)

    def delete_selected_file(self):
        from sqlalchemy.orm import Session
        from markdown_history_manager import MarkdownFileHistory
        selected_items = self.history_list.selectedItems()
        if selected_items:
            item = selected_items[0]
            title = item.text()
            with Session(self.markdown_history_manager.engine) as session:
                history = session.query(MarkdownFileHistory).filter(
                    MarkdownFileHistory.title == title).first()
                if history:
                    session.delete(history)
                    session.commit()
            self.load_history()

    def show_history_content(self, item):
        file_path = item.text()
        history = self.markdown_history_manager.get_file_history(file_path)[0]
        self.text_edit.setPlainText(history.content)
        self.update_preview()

    def get_current_style(self):
        return self.theme_manager_gui.get_current_style()
        # 定义 Mermaid 格式化函数，将代码包装在带有 "mermaid" 类的 div 中

    def mermaid_format(
            self,
            source,
            language,
            css_class,
            options,
            md,
            **kwargs):
        return f'<div class="{css_class}">{source}</div>'

    def update_preview(self):
        """将 Markdown 转换为 HTML 并更新预览区"""
        markdown_text = self.text_edit.toPlainText()

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
            {self.get_current_style() if self.get_current_style() else self.get_base_style()}
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/default.min.css">    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.css">
            <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
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
            font-family: 'Times New Roman', Times, 'Microsoft YaHei', 'SimSun', serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h2 { font-family: Arial, 'Microsoft YaHei', 'SimSun', sans-serif; font-size: 22px; }
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
