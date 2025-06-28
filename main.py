# -*- coding: utf-8 -*-
import sys
import os
import traceback
import markdown
from PySide6 import QtCore
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QMainWindow, QComboBox, QFileDialog, 
                               QHBoxLayout, QInputDialog, QLabel, QMessageBox, 
                               QSplitter, QToolBar, QVBoxLayout, QWidget)
from PySide6.QtWebEngineWidgets import QWebEngineView
from ui.history_panel import HistoryPanel
from ui.editor_panel import EditorPanel
from ui.theme_manager_gui import ThemeManagerGUI
from db.db_manager import ThemeManager
from db.markdown_history_manager import MarkdownHistoryManager
from db import init_db
from utils.logger_utils import logger

DB_NAME = "markrender.db"

def init_themes():
    # 检测 markrender.db 文件是否存在
    db_path = init_db.get_db_path(DB_NAME)
    theme_manager = ThemeManager(db_path=db_path)
    init_db.init_themes(theme_manager)  # 假设 init_db.py 中有 main 函数用于初始化
    return theme_manager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        db_path = init_db.get_db_path(DB_NAME)
        self.theme_manager = init_themes()
        self.markdown_history_manager = MarkdownHistoryManager(db_path)
        self.theme_manager_gui = ThemeManagerGUI(self, self.theme_manager)
        self.setWindowTitle("MarkRender")
        self.showMaximized()
        self.setup_ui()

    def setup_ui(self):
        """设置UI界面"""
        # 创建工具栏
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

       

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
            logger.warning('Failed to load icon: format-justify-fill.svg')
            self.toggle_history_button = self.toolbar.addAction(
                "展开/折叠", None)
        # 左侧历史记录面板
        self.history_panel = HistoryPanel(self.markdown_history_manager, parent=self)
        self.toggle_history_button.triggered.connect(self.history_panel.toggle_panel)
        self.toolbar.insertAction(
            self.toolbar.actions()[0],
            self.toggle_history_button)
        self.toolbar.setIconSize(QtCore.QSize(24, 24))

        self.toolbar.addWidget(style_widget)
        self.toolbar.addSeparator()
        
        # 初始化编辑器面板
        self.editor_panel = EditorPanel(self.theme_manager_gui)
        self.editor_panel.editor.textChanged.connect(self.history_panel.save_history)
        # 新建文件按钮
        new_file_button = self.toolbar.addAction("新建")
        new_file_button.triggered.connect(self.history_panel.create_new_markdown)

        # 导出按钮
        export_image_button = self.toolbar.addAction("导出图片")
        export_image_button.triggered.connect(self.editor_panel.export_image_dialog)

        export_pdf_button = self.toolbar.addAction("导出PDF")
        export_pdf_button.triggered.connect(self.editor_panel.export_pdf_dialog)

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
        splitter.addWidget(self.history_panel)
        self.history_panel.history_item_selected.connect(self.show_history_content)

        # 添加编辑器面板
        splitter.addWidget(self.editor_panel)
        # 设置三栏默认比例，参考VSCode布局
        splitter.setSizes([200, 800])

        # 设置主布局
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(splitter)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 初始化历史列表
        self.history_panel.load_history_items()

        # 初始化预览
        self.update_preview()

    def show_history_content(self, item):
        # Handle case where item is an index (int) instead of QListWidgetItem
        if isinstance(item, int):
            item = self.history_panel.history_list.item(item)
        if item:
            file_name = item.text()
            histories = self.markdown_history_manager.get_file_history(file_name)
            if histories:
                self.editor_panel.set_text_content(histories[0].content)
                self.update_preview()
            else:
                logger.warning(f"No history found for file: {file_name}")
        else:
            logger.warning("No valid item selected in history panel")

    def update_preview(self):
        """更新预览区内容"""
        logger.info('开始更新预览区内容')
        self.editor_panel.update_preview()
        logger.info('预览区内容更新完成')

   


if __name__ == "__main__":
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
