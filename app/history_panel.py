from ui.dayu_widgets import MListView, MLineEdit, MMenu
from db.markdown_manager import MarkdownManager
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtGui import QAction
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QInputDialog
from PySide6.QtGui import QStandardItemModel, QStandardItem
from utils.logger_utils import logger
from utils.time_utils import get_current_timestamp
from sqlalchemy.orm import Session
from db.models import MarkdownFileHistory
from datetime import datetime, timezone
from utils.hash_utils import calculate_md5


class HistoryPanel(QWidget):
    file_created = Signal(str)
    file_renamed = Signal(str, str)
    # 修改信号，传递完整的历史记录项
    history_item_selected = Signal(dict)

    def __init__(self, markdown_manager, parent=None):
        self.parent = parent
        super().__init__(parent)
        self.markdown_manager = markdown_manager
        self.history_list = MListView()
        # 设置列表项可编辑
        self.history_list.setEditTriggers(
            QtWidgets.QAbstractItemView.DoubleClicked)
        self.init_ui()
        # 初始化模型并保存为实例属性
        self.model = QStandardItemModel()
        self.history_list.setModel(self.model)
        # 将 load_history_items 调用移到 init_ui 之后，确保 search_input 已初始化
        self.load_history_items()
        self.history_list.clicked.connect(self.on_item_clicked)
        # 连接编辑完成信号到保存标题的方法
        self.model.itemChanged.connect(self.save_title_edit)

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)  # 设置布局的 margin

        # 创建搜索框
        self.search_input = MLineEdit()
        self.search_input.setPlaceholderText("搜索历史...")
        self.search_input.textChanged.connect(self.filter_history)
        self.search_input.returnPressed.connect(self.filter_history)
        main_layout.addWidget(self.search_input)
        main_layout.addWidget(self.history_list)
        self.setLayout(main_layout)

        # 设置上下文菜单
        self.history_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.history_list.customContextMenuRequested.connect(
            self.show_context_menu)

        # 存储所有历史项
        self.all_history_items = []

    def on_item_clicked(self, index):
        model = self.history_list.model()
        item = model.itemFromIndex(index)
        item_id = item.data(Qt.UserRole)
        logger.debug(f"点击的列表项ID: {item_id}")
        # 找到对应的完整历史记录项
        selected_item = next(
            (x for x in self.all_history_items if x['id'] == item_id), None)
        if selected_item:
            logger.debug(f"找到匹配的历史记录项: {selected_item}")
            self.history_item_selected.emit(selected_item)
        else:
            logger.warning(f"未找到ID为 {item_id} 的历史记录项")

    def load_history_items(self):
        """加载所有历史记录"""
        try:
            logger.debug("开始加载历史记录...")
            self.all_history_items = self.markdown_manager.load_history()
            if self.all_history_items:
                logger.info(
                    f"成功加载 {len(self.all_history_items)} 条历史记录，内容: {self.all_history_items}")
            else:
                logger.info("未找到历史记录")
            logger.debug("调用 filter_history 方法过滤历史记录...")
            self.filter_history()
        except Exception as e:
            logger.error(f"加载历史记录失败: {e}", exc_info=True)

    def filter_history(self):
        """根据搜索框过滤历史记录"""
        try:
            logger.debug("开始过滤历史记录...")
            # MListView may not have clear method, use model().clear() instead
            if self.history_list.model() is not None:
                logger.debug("清除当前列表模型中的数据...")
                self.model.clear()
            search_text = self.search_input.text().lower()
            logger.debug(f"搜索关键字: {search_text}")

            from PySide6.QtCore import Qt

            logger.debug(f"当前所有历史项数量: {len(self.all_history_items)}")
            for item in self.all_history_items:
                if search_text in item['title'].lower():
                    logger.debug(f"找到匹配项: {item}")
                    list_item = QStandardItem(item['title'])
                    list_item.setData(item['id'], Qt.UserRole)
                    self.model.appendRow(list_item)
            logger.debug(f"过滤后匹配项数量: {self.model.rowCount()}")
            logger.debug(
                f"历史列表模型是否设置成功: {
                    self.history_list.model() is not None}")
            logger.debug("历史记录过滤完成。")
        except Exception as e:
            logger.error(f"过滤历史记录时发生错误: {e}", exc_info=True)

    def show_context_menu(self, position):
        """显示上下文菜单"""
        index = self.history_list.currentIndex()
        if not index.isValid():
            return

        menu = MMenu()
        rename_action = QAction('重命名', self.history_list)
        rename_action.triggered.connect(self.rename_selected_file)
        delete_action = QAction('删除', self.history_list)
        delete_action.triggered.connect(self.delete_selected_history)
        menu.addAction(rename_action)
        menu.addAction(delete_action)
        menu.exec_(self.history_list.mapToGlobal(position))

    def save_history(self):
        """保存 Markdown 变更历史"""
        index = self.history_list.currentIndex()
        current_title = self.history_list.model().itemFromIndex(
            index).text() if index.isValid() else "Untitled"
        try:
            histories = self.markdown_manager.get_file_history(current_title)
            if histories:
                old_content = histories[0].content
                new_content = self.parent.editor_panel.get_text_content()
                if old_content != new_content:
                    self.markdown_manager.save_change_history(
                        histories[0].id, old_content, new_content)
                    histories[0].content = new_content
        except Exception as e:
            logger.error(f"保存历史记录失败: {e}")

    def rename_selected_file(self):
        """重命名选中的文件"""
        index = self.history_list.currentIndex()
        if index.isValid():
            model = self.history_list.model()
            item = model.itemFromIndex(index)
            old_title = item.text()
            new_title, ok = QInputDialog.getText(
                self, '重命名标题', '请输入新标题:', text=old_title)
            if ok and new_title and new_title != old_title:
                try:
                    with Session(self.markdown_manager.engine) as session:
                        item_id = item.data(Qt.UserRole)
                        history = session.query(MarkdownFileHistory).filter(
                            MarkdownFileHistory.id == item_id).first()
                        if history:
                            history.title = new_title
                            history.updated_at = datetime.now()
                            session.commit()
                            self.load_history_items()
                            self.file_renamed.emit(old_title, new_title)
                except Exception as e:
                    logger.error(f"重命名文件失败: {e}")

    def delete_selected_history(self):
        """删除选中的历史记录"""
        index = self.history_list.currentIndex()
        if index.isValid():
            model = self.history_list.model()
            item = model.itemFromIndex(index)
            title = item.text()
            try:
                # 获取 id 而非 title 进行删除
                item_id = item.data(Qt.UserRole)
                if self.markdown_manager.delete_history_item(item_id):
                    self.load_history_items()
                else:
                    logger.warning(f'无法删除历史记录: {title}')
            except Exception as e:
                logger.error(f"删除历史记录失败: {e}")

    def save_new_markdown(self, title, content):
        try:
            logger.debug(f"开始保存新的 Markdown 文件，标题: {title}")
            theme_names = self.parent.theme_manager_gui.get_theme_names()
            logger.debug(f"获取到的主题名称列表: {theme_names}")
            first_theme_style = self.parent.theme_manager_gui.get_current_style() if theme_names else ''
            logger.debug(f"当前使用的主题样式: {first_theme_style}")
            new_file = MarkdownFileHistory(
                title=title,
                content=content,
                tags='',
                render_style=first_theme_style,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                content_md5=calculate_md5(content)
            )
            logger.debug(f"创建的新文件对象: {new_file}")

            logger.debug("尝试将新文件添加到数据库...")
            save_result = self.markdown_manager.add_history_item(new_file)
            if save_result:
                logger.info(f"成功保存Markdown文件到数据库，标题: {title}，内容: {content}")
                logger.debug("调用 load_history_items 方法刷新历史记录...")
                self.load_history_items()
                logger.debug("发射 file_created 信号...")
                self.file_created.emit(title)
            else:
                logger.warning(f"将文件添加到数据库失败，标题: {title}")
        except Exception as e:
            logger.error(f"保存新文件失败: {e}", exc_info=True)

    def toggle_visibility(self):
        """切换面板可见性"""
        if self.isVisible():
            self.hide()
        else:
            self.show()

    def select_history_item(self, file_path):
        """根据文件路径选择历史记录项"""
        for item in self.all_history_items:
            if item.get('UserRole') == file_path:
                self.list_widget.setCurrentItem(item)
                break

    def save_title_edit(self, item):
        """保存标题编辑内容"""
        item_id = item.data(Qt.UserRole)
        old_title = None
        # 从 all_history_items 中找到原标题
        for history_item in self.all_history_items:
            if history_item['id'] == item_id:
                old_title = history_item['title']
                break

        if old_title:
            new_title = item.text()
            if new_title and new_title != old_title:
                try:
                    with Session(self.markdown_manager.engine) as session:
                        # 通过 ID 搜索文件
                        history = session.query(MarkdownFileHistory).filter(
                            MarkdownFileHistory.id == item_id).first()
                        if history:
                            history.title = new_title
                            history.updated_at = datetime.now()
                            session.commit()
                            self.load_history_items()
                            self.file_renamed.emit(old_title, new_title)
                except Exception as e:
                    logger.error(f"重命名文件失败: {e}")
                    # 恢复原标题
                    item.setText(old_title)
