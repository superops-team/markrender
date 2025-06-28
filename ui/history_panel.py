from PySide6.QtWidgets import QWidget, QListWidget, QListWidgetItem, QMenu, QVBoxLayout, QLineEdit, QHBoxLayout, QInputDialog, QMessageBox
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QListWidgetItem
from utils.logger_utils import logger
from utils.time_utils import get_current_timestamp
from sqlalchemy.orm import Session
from db.models import MarkdownFileHistory


class HistoryPanel(QWidget):
    file_created = Signal(str)
    file_renamed = Signal(str, str)
    history_item_selected = Signal(QListWidgetItem)
    
    def __init__(self, markdown_history_manager, parent=None):
        self.parent = parent
        super().__init__(parent)
        self.markdown_history_manager = markdown_history_manager
        self.history_list = QListWidget()
        self.init_ui()
        self.load_history_items()
        self.history_list.itemClicked.connect(self.on_item_clicked)
        
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        
        # 创建搜索框
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索历史...")
        self.search_input.textChanged.connect(self.filter_history)
        search_layout.addWidget(self.search_input)
        
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.history_list)
        self.setLayout(main_layout)
        
        # 设置上下文菜单
        self.history_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.history_list.customContextMenuRequested.connect(self.show_context_menu)
        
        # 存储所有历史项
        self.all_history_items = []
        
    def on_item_clicked(self, item):
        self.history_item_selected.emit(item)

    def toggle_panel(self):
        if self.isVisible():
            self.hide()
            from PySide6.QtWidgets import QStyle
            icon = self.parent.style().standardIcon(QStyle.SP_TitleBarShadeButton)
            if not icon.isNull():
                self.parent.toggle_history_button.setIcon(icon)
            else:
                logger.warning('Failed to load icon: format-justify-fill.svg')
        else:
            self.show()
            self.load_history_items()
            from PySide6.QtWidgets import QStyle
            icon = self.parent.style().standardIcon(QStyle.SP_TitleBarUnshadeButton)
            if not icon.isNull():
                self.parent.toggle_history_button.setIcon(icon)
            else:
                logger.warning('Failed to load icon: format-justify.svg')

    def load_history_items(self):
        """加载所有历史记录"""
        self.all_history_items = self.markdown_history_manager.load_history()
        self.filter_history()
        
    def filter_history(self):
        """根据搜索框过滤历史记录"""
        self.history_list.clear()
        search_text = self.search_input.text().lower()
        
        for item in self.all_history_items:
            if search_text in item['title'].lower():
                list_item = QListWidgetItem(item['title'])
                list_item.setData(Qt.UserRole, item['id'])
                self.history_list.addItem(list_item)
            
    def show_context_menu(self, position):
        """显示上下文菜单"""
        if not self.history_list.selectedItems():
            return
            
        menu = QMenu()
        rename_action = QAction('重命名', self.history_list)
        rename_action.triggered.connect(self.rename_selected_file)
        delete_action = QAction('删除', self.history_list)
        delete_action.triggered.connect(self.delete_selected_history)
        menu.addAction(rename_action)
        menu.addAction(delete_action)
        menu.exec_(self.history_list.mapToGlobal(position))
        
    def save_history(self):
        """保存 Markdown 变更历史"""
        current_title = self.history_list.currentItem().text() if self.history_list.currentItem() else "Untitled"
        histories = self.markdown_history_manager.get_file_history(current_title)
        if histories:
            old_content = histories[0].content
            new_content = self.parent.editor_panel.get_text_content()
            if old_content != new_content:
                self.markdown_history_manager.save_change_history(histories[0].id, old_content, new_content)
                histories[0].content = new_content

    def rename_selected_file(self):
        """重命名选中的文件"""
        selected_items = self.history_list.selectedItems()
        if selected_items:
            item = selected_items[0]
            old_title = item.text()
            new_title, ok = QInputDialog.getText(
                self, '重命名标题', '请输入新标题:', text=old_title)
            if ok and new_title and new_title != old_title:
                with Session(self.markdown_history_manager.engine) as session:
                    history = session.query(MarkdownFileHistory).filter(
                        MarkdownFileHistory.title == old_title).first()
                    if history:
                        history.title = new_title
                        history.updated_at = get_current_timestamp()
                        session.commit()
                        self.load_history_items()
                        self.file_renamed.emit(old_title, new_title)

    def delete_selected_history(self):
        """删除选中的历史记录"""
        selected_item = self.history_list.currentItem()
        if selected_item:
            title = selected_item.text()
            if self.markdown_history_manager.delete_history_item(title):
                self.load_history_items()
            else:
                logger.warning(f'无法删除历史记录: {title}')

    def create_new_markdown(self):
        """创建新的markdown文件"""
        from ui.new_file_dialog import NewFileDialog
        dialog = NewFileDialog(self)
        dialog.save_requested.connect(self.save_new_markdown)
        dialog.exec()

    def save_new_markdown(self, title, content):
        """保存新的markdown文件"""
        theme_names = self.parent().theme_manager_gui.get_theme_names()
        first_theme_style = self.parent().theme_manager_gui.get_theme_css(
            theme_names[0]) if theme_names else ''
        new_file = MarkdownFileHistory(
            title=title,
            content=content,
            tags='',
            render_style=first_theme_style,
            created_at=get_current_timestamp(),
            updated_at=get_current_timestamp()
        )

        with Session(self.markdown_history_manager.engine) as session:
            session.add(new_file)
            session.commit()
        self.load_history_items()
        self.file_created.emit(title)
                
    def toggle_visibility(self):
        """切换面板可见性"""
        if self.isVisible():
            self.hide()
        else:
            self.show()