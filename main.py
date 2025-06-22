import sys
import logging
import os

# 主窗口必要的导入
from PySide6.QtWidgets import QApplication, QMainWindow

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
ThemeManager = None
ThemeManagerGUI = None
init_db = None

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)

logger = logging.getLogger(__name__)


def init_resources():
    # 检测 markrender.db 文件是否存在
    db_path = 'markrender.db'
    try:
        home_dir = os.path.expanduser('~')
        markrender_dir = os.path.join(home_dir, '.markrender')
        os.makedirs(markrender_dir, exist_ok=True)
        db_path = os.path.join(markrender_dir, db_path)
        init_db.run(db_path)  # 假设 init_db.py 中有 main 函数用于初始化
    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}", exc_info=True)
        raise
    return db_path


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        global markdown, Qt, QTimer, QWebEngineView, QComboBox, QFileDialog, QHBoxLayout, QInputDialog, QLabel, QMessageBox, QSplitter, QTextEdit, QToolBar, QVBoxLayout, QWidget, ThemeManager, ThemeManagerGUI, init_db, logging
        if markdown is None:
            import markdown
        if Qt is None:
            from PySide6.QtCore import Qt, QTimer
        if QWebEngineView is None:
            from PySide6.QtWebEngineWidgets import QWebEngineView
        if QComboBox is None:
            from PySide6.QtWidgets import QComboBox, QFileDialog, QHBoxLayout, QInputDialog, QLabel, QMessageBox, QSplitter, QTextEdit, QToolBar, QVBoxLayout, QWidget
        if ThemeManager is None:
            from db_manager import ThemeManager
        if ThemeManagerGUI is None:
            from theme_manager_gui import ThemeManagerGUI
        if init_db is None:
            import init_db
        db_path = init_resources()
        self.theme_manager = ThemeManager(db_path)
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
        style_label = QLabel("Markdown样式:")
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
        theme_management_button.triggered.connect(
            self.theme_manager_gui.show_theme_management_dialog
        )

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

    def delete_theme(self, theme_name=None):
        if not theme_name:
            theme_name = self.style_combobox.currentText()
        if theme_name:
            reply = QMessageBox.question(
                self,
                "确认删除",
                f"确定要删除主题 '{theme_name}' 吗？",
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                self.theme_manager.delete_theme(theme_name)
                self.style_combobox.removeItem(
                    self.style_combobox.findText(theme_name))
                # 重新加载主题管理对话框
                if hasattr(self, "show_theme_management_dialog"):
                    self.show_theme_management_dialog()

    def edit_theme(self, theme_name):
        from PySide6.QtWidgets import (
            QDialog,
            QHBoxLayout,
            QLineEdit,
            QPushButton,
            QTextEdit,
            QVBoxLayout,
        )

        theme = self.theme_manager.get_theme(theme_name)
        if theme:
            dialog = QDialog(self)
            dialog.setWindowTitle("编辑主题")
            layout = QVBoxLayout()

            # 主题标题输入框，使用单个输入框
            title_input = QLineEdit(theme_name)
            title_input.setPlaceholderText("请输入新主题名称")
            title_input.setReadOnly(True)  # 设置为只读
            layout.addWidget(title_input)

            # 主题配置输入框
            config_input = QTextEdit()
            config_input.setPlainText(theme.css_config)
            config_input.setPlaceholderText("输入主题配置")
            layout.addWidget(config_input)

            # 保存和取消按钮
            button_layout = QHBoxLayout()
            save_button = QPushButton("保存")
            save_button.clicked.connect(
                lambda: self.update_existing_theme(
                    title_input.text(),
                    config_input.toPlainText(),
                    theme_name,
                    dialog))
            cancel_button = QPushButton("取消")
            cancel_button.clicked.connect(dialog.close)
            button_layout.addWidget(save_button)
            button_layout.addWidget(cancel_button)
            layout.addLayout(button_layout)

            dialog.setLayout(layout)
            dialog.exec()

    def update_existing_theme(self, new_title, new_config, old_name, dialog):
        if new_config:
            self.theme_manager.update_theme(old_name, new_config)
            dialog.close()
            if hasattr(self, "theme_management_dialog") and hasattr(
                self.theme_management_dialog, "table"
            ):
                table = self.theme_management_dialog.table
                themes = self.theme_manager.get_all_themes()
                table.setRowCount(len(themes))
                for row in range(table.rowCount()):
                    if table.cellWidget(row, 3):
                        table.cellWidget(row, 3).disconnect()
                    if table.cellWidget(row, 4):
                        table.cellWidget(row, 4).disconnect()
                for row, theme in enumerate(themes):
                    # 主题名称
                    item_name = QTableWidgetItem(theme.name)
                    table.setItem(row, 0, item_name)

                    # 创建时间
                    item_create_time = QTableWidgetItem(str(theme.created_at))
                    table.setItem(row, 1, item_create_time)

                    # 修改时间
                    item_update_time = QTableWidgetItem(str(theme.updated_at))
                    table.setItem(row, 2, item_update_time)

                    # 编辑按钮，解决闭包问题
                    edit_button = QPushButton("编辑")
                    edit_button.clicked.connect(
                        lambda _, t=theme.name: self.edit_theme(t)
                    )
                    table.setCellWidget(row, 3, edit_button)

                    # 删除按钮，解决闭包问题
                    delete_button = QPushButton("删除")
                    delete_button.clicked.connect(
                        lambda _, t=theme.name: self.delete_theme(t)
                    )
                    table.setCellWidget(row, 4, delete_button)

    def show_theme_management_dialog(self):
        from PySide6.QtWidgets import (
            QDialog,
            QHeaderView,
            QPushButton,
            QTableWidget,
            QTableWidgetItem,
            QVBoxLayout,
        )

        self.theme_management_dialog = QDialog(self)
        self.theme_management_dialog.setWindowTitle("主题管理")
        self.theme_management_dialog.resize(800, 600)  # 放大对话框
        layout = QVBoxLayout()

        # 创建表格
        self.theme_management_dialog.table = QTableWidget()
        themes = self.theme_manager.get_all_themes()
        self.theme_management_dialog.table.setRowCount(len(themes))
        self.theme_management_dialog.table.setColumnCount(5)
        self.theme_management_dialog.table.setHorizontalHeaderLabels(
            ["主题名称", "创建时间", "修改时间", "编辑", "删除"]
        )

        for row, theme in enumerate(themes):
            # 主题名称
            item_name = QTableWidgetItem(theme.name)
            self.theme_management_dialog.table.setItem(row, 0, item_name)

            # 创建时间
            item_create_time = QTableWidgetItem(str(theme.created_at))
            self.theme_management_dialog.table.setItem(
                row, 1, item_create_time)

            # 修改时间
            item_update_time = QTableWidgetItem(str(theme.updated_at))
            self.theme_management_dialog.table.setItem(
                row, 2, item_update_time)

            # 编辑按钮，解决闭包问题
            edit_button = QPushButton("编辑")
            edit_button.clicked.connect(
                lambda _, t=theme.name: self.edit_theme(t))
            self.theme_management_dialog.table.setCellWidget(
                row, 3, edit_button)

            # 删除按钮，解决闭包问题
            delete_button = QPushButton("删除")
            delete_button.clicked.connect(
                lambda _, t=theme.name: self.delete_theme(t))
            self.theme_management_dialog.table.setCellWidget(
                row, 4, delete_button)

        self.theme_management_dialog.table.horizontalHeader(
        ).setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.theme_management_dialog.table)

        # 新增主题按钮
        add_button = QPushButton("新增主题")
        add_button.clicked.connect(self.show_add_theme_dialog)

        self.theme_management_dialog.setLayout(layout)
        self.theme_management_dialog.exec()

    def rename_theme(self):
        current_theme_name = self.style_combobox.currentText()
        if current_theme_name:
            new_name, ok = QInputDialog.getText(
                self, "重命名主题", "请输入新主题名称:", text=current_theme_name
            )
            if ok and new_name:
                current_style = self.get_current_style()
                self.theme_manager.delete_theme(current_theme_name)
                self.theme_manager.create_theme(new_name, current_style)
                self.style_combobox.removeItem(
                    self.style_combobox.currentIndex())
                self.style_combobox.addItem(new_name)
                self.style_combobox.setCurrentText(new_name)

    def show_theme_management_dialog(self):
        from PySide6.QtWidgets import (
            QDialog,
            QHeaderView,
            QPushButton,
            QTableWidget,
            QTableWidgetItem,
            QVBoxLayout,
        )

        dialog = QDialog(self)
        dialog.setWindowTitle("主题管理")
        dialog.resize(800, 600)  # 放大对话框
        layout = QVBoxLayout()

        # 创建表格
        table = QTableWidget()
        themes = self.theme_manager.get_all_themes()
        table.setRowCount(len(themes))
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(
            ["主题名称", "创建时间", "修改时间", "编辑", "删除"]
        )

        for row, theme in enumerate(themes):
            # 主题名称
            item_name = QTableWidgetItem(theme.name)
            table.setItem(row, 0, item_name)

            # 创建时间
            item_create_time = QTableWidgetItem(str(theme.created_at))
            table.setItem(row, 1, item_create_time)

            # 修改时间
            item_update_time = QTableWidgetItem(str(theme.updated_at))
            table.setItem(row, 2, item_update_time)

            # 编辑按钮
            edit_button = QPushButton("编辑")
            edit_button.clicked.connect(
                lambda _, r=row: self.edit_theme(
                    theme.name))
            table.setCellWidget(row, 3, edit_button)

            # 删除按钮
            delete_button = QPushButton("删除")
            delete_button.clicked.connect(
                lambda _, r=row: self.delete_theme(theme.name)
            )
            table.setCellWidget(row, 4, delete_button)

        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(table)

        # 新增主题按钮
        add_button = QPushButton("新增主题")
        add_button.clicked.connect(self.show_add_theme_dialog)
        layout.addWidget(add_button)

        dialog.setLayout(layout)
        dialog.exec()

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
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
