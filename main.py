# -*- coding: utf-8 -*-
import sys
import traceback
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout)
from utils.logger_utils import logger
from PySide6.QtWidgets import QSplitter
from app.editor import MarkdownEditor
from app.status_bar import StatusBar
from app.history_panel import HistoryPanel
from app.sidebar_manager import SidebarManager
from db.markdown_manager import MarkdownManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MarkRender")
        self.showMaximized()
        self.setup_ui()
        self.current_file = None

    def setup_ui(self):
        """设置UI界面"""
        # 初始化数据库路径，使用用户数据路径
        import os
        from platform import system
        if system() == 'Windows':
            user_data_dir = os.path.join(os.getenv('APPDATA'), 'markrender')
        elif system() == 'Darwin':
            user_data_dir = os.path.join(
                os.path.expanduser('~'),
                'Library',
                'Application Support',
                'markrender')
        else:
            user_data_dir = os.path.join(
                os.path.expanduser('~'), '.local', 'share', 'markrender')
        os.makedirs(user_data_dir, exist_ok=True)
        db_path = os.path.join(user_data_dir, 'data.db')
        logger.info(f'数据库路径初始化完成，路径为: {db_path}')

        # 添加数据库初始化逻辑
        from db.init_db import init_db
        try:
            init_db(db_path)
            logger.info('数据库初始化完成')
        except Exception as e:
            logger.error(f'数据库初始化失败: {e}')
            sys.exit(1)

        # 将顶部组件添加到主窗口
        central_widget = QWidget()
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        # 初始化历史面板
        self.markdown_manager = MarkdownManager(db_path)
        logger.info("MarkdownManager 初始化完成")
        self.history_panel = HistoryPanel(self.markdown_manager, self)
        self.sidebar_manager = SidebarManager(parent=self)
        logger.info("HistoryPanel 初始化完成")
        # 初始化 Markdown 编辑器
        self.markdown_editor = MarkdownEditor(self, '', '')
        self.sidebar = SidebarManager(self)

        # 修改为创建主分割器，使用 PySide6 原生的 QSplitter
        main_splitter = QSplitter(Qt.Horizontal)
        # 禁止分割条调整大小
        main_splitter.setOpaqueResize(False)
        main_splitter.setHandleWidth(0)

        # 创建右侧内容分割器，同样使用 QSplitter
        right_splitter = QSplitter(Qt.Horizontal)
        # 设置分割器样式，统一边距和圆角
        right_splitter.setStyleSheet('''
            QSplitter::handle {
                background: transparent;
                width: 2px;
            }
            QSplitter {
                padding: 3px;
            }
            QSplitter > QWidget {
                margin: 2 2px;
            }
        ''')
        right_splitter.addWidget(self.history_panel)
        right_splitter.addWidget(self.markdown_editor)
        initial_right_sizes = [
            int(self.width() * 0.2), int(self.width() * 0.8)]
        right_splitter.setSizes(initial_right_sizes)

        # 将侧边栏和右侧内容添加到主分割器，侧边栏放在左侧
        main_splitter.addWidget(self.sidebar)
        main_splitter.addWidget(right_splitter)

        # 设置侧边栏宽度为 30，并禁止调整大小
        main_splitter.setSizes([32, int(self.width() - 32)])
        self.sidebar.setFixedWidth(32)

        self.main_layout.addWidget(main_splitter)

        self.setCentralWidget(central_widget)

        # 连接历史列表项选中信号
        self.history_panel.history_item_selected.connect(
            self.update_editor_and_previewer)

        # 设置状态栏
        self.status_bar = StatusBar()
        self.setStatusBar(self.status_bar)

    def update_theme(self, theme):
        """切换主题"""
        self.markdown_editor.update_theme(theme)

    def update_editor_and_previewer(self, history_item):
        """更新编辑区和预览区内容"""
        try:
            self.current_file = history_item
            # 获取选中历史项的内容
            content = history_item.get('content', '')
            # 更新编辑区内容
            self.markdown_editor.set_file_id(history_item.get('id', ''))
            self.markdown_editor.set_file_name(history_item.get('title', ''))
            self.markdown_editor.set_text_content(content)
            self.status_bar.update_file_size(len(content))
            self.status_bar.update_word_count(len(content))
        except Exception as e:
            logger.error(f"更新编辑区和预览区失败: {e}")

    def update_history_list(self):
        """更新历史列表"""
        self.history_panel.load_history_items()
        if self.current_file:
            self.history_panel.select_history_item(self.current_file)

    def export_pdf(self):
        """导出PDF功能"""
        logger.info('触发导出PDF功能')
        try:
            # 假设 self.markdown_editor 是 Markdown 编辑器实例
            self.markdown_editor.export_to_pdf()
            logger.info('PDF导出成功')
        except Exception as e:
            logger.error(f'PDF导出失败: {str(e)}')


if __name__ == "__main__":
    logger.info("应用启动")
    try:
        app = QApplication(sys.argv)
        # 设置全局字体
        font = app.font()
        font.setFamily('Arial')  # 可替换为系统存在的字体
        app.setFont(font)
        logger.info("QApplication 创建完成")
        window = MainWindow()
        logger.info("MainWindow 创建完成")
        window.show()
        logger.info("MainWindow 显示完成")
        sys.exit(app.exec())
    except Exception as e:
        error_msg = traceback.format_exc()
        logger.critical(f"致命错误: {e} {error_msg}")
        from PySide6.QtWidgets import QMessageBox
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(f"应用遇到致命错误: {str(e)}")
        msg_box.setDetailedText(error_msg)
        msg_box.setWindowTitle("错误")
        msg_box.exec()
        sys.exit(1)
