# -*- coding: utf-8 -*-
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QWidget, QMenuBar, QVBoxLayout
from ui.dayu_widgets import MPushButton, dayu_theme, MMessage
from utils.logger_utils import logger
from app.new_file_dialog import NewFileDialog
from sqlalchemy.orm import Session
from db.models import MarkdownFileHistory
from datetime import datetime, timezone
from utils.hash_utils import calculate_md5


class TopMenu(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.setup_menu_bar()
        self.setup_tool_buttons()
        self.setStyleSheet("background: #f0f0f0;")
        from PySide6.QtWidgets import QSizePolicy
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.menu_bar)
        layout.addWidget(self.tool_buttons_widget)

    def setup_menu_bar(self):
        """设置菜单栏"""
        self.menu_bar = QMenuBar()

        # 文件菜单
        file_menu = self.menu_bar.addMenu('文件')

        new_action = file_menu.addAction('新建文件')
        new_action.triggered.connect(self.new_file)

        export_action = file_menu.addAction('导出PDF')
        export_action.triggered.connect(self.export_pdf)

    def setup_tool_buttons(self):
        """设置工具按钮栏"""
        self.tool_buttons_widget = QWidget()
        layout = QHBoxLayout(self.tool_buttons_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(1)

        # 新建文件按钮
        new_file_button = MPushButton('新建文件')
        new_file_button.clicked.connect(self.new_file)
        dayu_theme.apply(new_file_button)
        layout.addWidget(new_file_button)

        # 导出PDF按钮
        export_pdf_button = MPushButton('导出PDF')
        export_pdf_button.clicked.connect(self.export_pdf)
        dayu_theme.apply(export_pdf_button)
        layout.addWidget(export_pdf_button)

    def new_file(self):
        """新建文件功能，弹出对话框交互式设置文件名和内容"""
        logger.info('触发新建文件功能')
        dialog = NewFileDialog(
            self.main_window.markdown_manager,
            self.main_window)
        dialog.save_requested.connect(self.handle_new_file)
        dialog.show()

    def handle_new_file(self, title, content):
        """处理新建文件保存请求"""
        logger.info(f'新建文件: {title}')
        try:
            # 创建新的 MarkdownFileHistory 实例
            new_file = MarkdownFileHistory(
                title=title,
                content=content,
                tags='',
                render_style='',  # 可根据实际情况修改
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                content_md5=calculate_md5(content)
            )

            # 保存新文件到数据库
            with Session(self.main_window.markdown_manager.engine) as session:
                session.add(new_file)
                session.commit()
                session.refresh(new_file)
                new_file_id = new_file.id

            # 刷新历史记录列表
            self.main_window.history_panel.load_history_items()

            # 设置编辑区内容
            self.main_window.markdown_editor.set_text_content(content)

            # 更新预览
            self.main_window.update_preview()

            # 选中新建的文件
            all_history = self.main_window.history_panel.all_history_items
            for item in all_history:
                if item['id'] == new_file_id:
                    # 查找对应列表项并选中
                    model = self.main_window.history_panel.history_list.model()
                    for row in range(model.rowCount()):
                        list_item = model.item(row)
                        if list_item.data(Qt.UserRole) == new_file_id:
                            index = model.index(row, 0)
                            self.main_window.history_panel.history_list.setCurrentIndex(
                                index)
                            self.main_window.history_panel.on_item_clicked(
                                index)
                            break
                    break

        except Exception as e:
            logger.error(f'保存新建文件失败: {e}')
            MMessage.error(f'保存失败: {str(e)}', parent=self, duration=3)

    def export_pdf(self):
        """导出PDF功能，弹出对话框设置导出位置，调用webview的逻辑导出"""
        logger.info('触发导出PDF功能')
        try:
            from PySide6.QtWidgets import QFileDialog
            # 弹出文件保存对话框
            file_path, _ = QFileDialog.getSaveFileName(
                self.main_window, '保存PDF文件', '', 'PDF文件 (*.pdf)')

            if file_path:
                # 假设 self.main_window.webview 有导出PDF的方法
                self.main_window.markdown_previewer.export_pdf(file_path)
                logger.info(f'PDF成功导出至 {file_path}')
            else:
                logger.info('用户取消了PDF导出操作')
        except Exception as e:
            logger.error(f'PDF导出失败: {str(e)}')
