# 修改导入语句，移除 dayu_widgets 相关导入，添加 QListWidget 和 QLineEdit 导入
from PySide6.QtWidgets import QVBoxLayout, QListWidget, QListWidgetItem, QLineEdit, QMenu, QStyledItemDelegate, QStyleOptionViewItem, QStyle
from PySide6.QtGui import QAction, QPainter, QFont, QColor
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtWidgets import QWidget, QInputDialog
from utils.logger_utils import logger
from sqlalchemy.orm import Session
from db.models import MarkdownFileHistory
from datetime import datetime, timezone, timedelta
from utils.hash_utils import calculate_md5
from PySide6.QtGui import QColor, QFont, QPainter, QPen  # 添加 QPen 导入

class HistoryItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def _format_time(self, modified_time):
        if isinstance(modified_time, datetime):
            # 确保 now 和 modified_time 时区一致
            if modified_time.tzinfo is None:
                now = datetime.now()
            else:
                now = datetime.now(timezone.utc)
            delta = now - modified_time
            if delta < timedelta(seconds=60):
                return f'{delta.seconds}秒前'
            elif delta < timedelta(minutes=60):
                return f'{delta.seconds // 60}分钟前'
            elif delta < timedelta(hours=24):
                return f'{delta.seconds // 3600}小时前'
            elif delta < timedelta(days=30):
                return f'{delta.days}天前'
            elif delta < timedelta(days=365):
                return f'{delta.days // 30}个月前'
            else:
                return f'{delta.days // 365}年前'
        return str(modified_time)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index):
        painter.save()
        radius = 15
        
        if option.state & QStyle.State_Selected:
            painter.setBrush(QColor(25, 144, 255, 38))   
            painter.setPen(Qt.NoPen)  # 设置无边框
            painter.drawRoundedRect(option.rect, radius, radius)
        elif option.state & QStyle.State_MouseOver:
            painter.setBrush(QColor(25, 144, 255, 25))
            painter.setPen(Qt.NoPen)  # 设置无边框
            painter.drawRoundedRect(option.rect, radius, radius)
        else:
            painter.setPen(Qt.NoPen)  # 设置无边框

        # Get item data
        item_data = index.data(Qt.UserRole)
        if item_data:
            title = item_data.get('title', '')
            modified_time = item_data.get('updated_at', '')
            preview = item_data.get('content', '')[:15] + ('...' if len(item_data.get('content', '')) > 15 else '')
            formatted_time = self._format_time(modified_time)

            # 设置边距
            margin = 10
            text_rect = option.rect.adjusted(margin, margin, -margin, -margin)

            # 绘制标题
            title_font = QFont()
            title_font.setBold(True)
            painter.setFont(title_font)
            if option.state & QStyle.State_Selected:
                painter.setPen(QColor(25, 144, 255))  # #006400 --> 1990ff
            else:
                painter.setPen(QColor(0, 0, 0))
            # Bug fix: 使用 horizontalAdvance 替代 width
            title_width = painter.fontMetrics().horizontalAdvance(title)
            painter.drawText(text_rect.x(), text_rect.y() + 15, title)

            # 绘制修改时间
            time_font = QFont()
            time_font.setPointSize(9)
            painter.setFont(time_font)
            if option.state & QStyle.State_Selected:
                painter.setPen(QColor(25, 144, 255))  # #006400 --> 1990ff
            else:
                painter.setPen(QColor(100, 100, 100))
            time_x = text_rect.x() + title_width + 10
            painter.drawText(time_x, text_rect.y() + 15, formatted_time)

            # 绘制预览
            preview_font = QFont()
            preview_font.setPointSize(9)
            if option.state & QStyle.State_Selected:
                painter.setPen(QColor(25, 144, 255))  # #006400--->1990ff
            else:
                painter.setPen(QColor(100, 100, 100))
            painter.setFont(preview_font)
            preview_rect = text_rect.adjusted(0, 20, 0, 0)
            painter.drawText(preview_rect, Qt.TextSingleLine, preview)

        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index):
        # Bug fix: Call width() method to get the width value
        return QSize(option.rect.width(), 50)

class HistoryPanel(QWidget):
    file_created = Signal(str)
    file_renamed = Signal(str, str)
    # 修改信号，传递完整的历史记录项
    history_item_selected = Signal(dict)

    def __init__(self, markdown_manager, parent=None):
        self.parent = parent
        super().__init__(parent)
        self.markdown_manager = markdown_manager
        # 替换 MListView 为 QListWidget
        self.history_list = QListWidget()
        # 设置 sizePolicy 为 Expanding
        from PySide6.QtWidgets import QSizePolicy
        self.history_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 禁用水平滚动条
        from PySide6.QtCore import Qt
        self.history_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.history_list.setItemDelegate(HistoryItemDelegate(self.history_list))
        # 设置列表项可编辑
        self.history_list.setEditTriggers(
            QtWidgets.QAbstractItemView.DoubleClicked
        )
        self.init_ui()
        # 删除初始化模型及设置模型的代码
        # self.model = QStandardItemModel()
        # self.history_list.setModel(self.model)
        # 将 load_history_items 调用移到 init_ui 之后，确保 search_input 已初始化
        self.load_history_items()
        self.history_list.clicked.connect(self.on_item_clicked)
        # 删除编辑完成信号连接代码
        # self.model.itemChanged.connect(self.save_title_edit)

    def init_ui(self):
        main_layout = QVBoxLayout()
        # 设置上下左右边距均为 5px
        main_layout.setContentsMargins(1, 1, 1, 1)
        # 创建美观的搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索...")
        self.search_input.setStyleSheet('''
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 15px;
                padding: 5px 15px;
                font-size: 16px;
            }
            QLineEdit:hover {
                border: 2px solid #E6F6FF;
                background-color: #EAF3FF;
            }
            QLineEdit:focus {
                border: 2px solid #e1e1e1; 
                outline: none;
            }
        ''')
        # #E6F6FF
        self.search_input.textChanged.connect(self.filter_history)
        self.search_input.returnPressed.connect(self.filter_history)
        main_layout.addWidget(self.search_input)

        # 优化列表项选中样式，与全局风格保持一致
        self.history_list.setStyleSheet('''
            QListWidget { 
                border: 2px solid #ddd; 
                border-radius: 15px; 
                padding: 0; 
            } 
            QListWidget::item { 
                border: 2px solid transparent; 
                border-radius: 15px; 
                padding: 5px 10px; 
                background-color: #f0f0f0; 
            } 
            QListWidget::item:hover { 
                border: 2px solid rgb(25, 144, 255, 0.1); 
                background-color: rgb(234, 243, 255, 0.1); 
            } 
            QListWidget::item:selected { 
                border: 2px solid rgb(25, 144, 255, 0.1); 
                background-color: rgb(234, 243, 255, 0.1); 
            } 
        ''')
        main_layout.addWidget(self.history_list)
        # 设置布局后，添加样式表修改底色，这里以浅灰色为例
        self.setLayout(main_layout)
        
        # 设置控件边角样式，与搜索框保持一致，并设置白色背景
        self.setStyleSheet('''
            QWidget { 
                border: 2px solid #ddd;
                border-radius: 15px;
                background-color: white;
            }
        ''')

    def on_item_clicked(self, index):
        # 修改获取数据的方式
        item = self.history_list.itemFromIndex(index)
        if item:
            data = item.data(Qt.UserRole)
            if data and 'id' in data:
                logger.debug(f"点击的列表项ID: {data['id']}")
                # 找到对应的完整历史记录项
                selected_item = next(
                    (x for x in self.all_history_items if x['id'] == data['id']), None)
                if selected_item:
                    logger.debug(f"找到匹配的历史记录项: {selected_item}")
                    self.history_item_selected.emit(selected_item)
                else:
                    logger.warning(f"未找到ID为 {data['id']} 的历史记录项")
            else:
                logger.warning("点击的列表项数据为空或缺少ID字段")
        else:
            logger.warning("未找到点击的列表项")

    def load_history_items(self):
        """加载所有历史记录"""
        try:
            logger.debug("开始加载历史记录...")
            self.all_history_items = self.markdown_manager.load_history()
            if self.all_history_items:
                logger.info(f"成功加载 {len(self.all_history_items)} 条历史记录")
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
            # 清除当前列表中的数据
            self.history_list.clear()
            search_text = self.search_input.text().lower()
            logger.debug(f"搜索关键字: {search_text}")

            from PySide6.QtCore import Qt

            logger.debug(f"当前所有历史项数量: {len(self.all_history_items)}")
            for item in self.all_history_items:
                if search_text in item['title'].lower():
                    logger.debug(f"找到匹配项: {item}")
                    # 创建自定义列表项
                    list_item = QListWidgetItem()
                    list_item.setData(Qt.UserRole, item)
                    # 设置列表项文本，确保项可见
                    list_item.setText(item.get('title', ''))
                    self.history_list.addItem(list_item)
            logger.debug(f"过滤后匹配项数量: {self.history_list.count()}")
            logger.debug(f"历史列表模型是否设置成功: {self.history_list.model() is not None}")
            logger.debug("历史记录过滤完成。")
        except Exception as e:
            logger.error(f"过滤历史记录时发生错误: {e}", exc_info=True)

    def show_context_menu(self, position):
        """显示上下文菜单"""
        index = self.history_list.currentIndex()
        if not index.isValid():
            return

        # 替换 MMenu 为 QMenu
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
        index = self.history_list.currentIndex()
        # 修改获取当前标题的方式
        current_title = self.history_list.item(index.row()).text() if index.isValid() else "Untitled"
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
            # 修改获取项的方式
            item = self.history_list.item(index.row())
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
            # 修改获取项的方式
            item = self.history_list.item(index.row())
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

    def select_history_item(self, current_file):
        """根据文件路径选择历史记录项"""
        if not current_file or 'id' not in current_file:
            logger.warning("传入的 current_file 为空或缺少 id 字段")
            return
        for i in range(self.history_list.count()):
            item = self.history_list.item(i)
            data = item.data(Qt.UserRole)
            if data and data.get('id') == current_file['id']:
                self.history_list.setCurrentItem(item)
                break

    def save_title_edit(self, item):
        # 此方法暂时不需要，可删除
        pass
