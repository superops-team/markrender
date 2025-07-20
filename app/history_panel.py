# 修改导入语句，添加 QEvent 导入
from PySide6.QtWidgets import (
    QVBoxLayout,
    QListWidget,
    QListWidgetItem, 
    QLineEdit, 
    QMenu,
    QHBoxLayout,
    QStyledItemDelegate, QStyleOptionViewItem, QStyle, QPushButton, QMessageBox)
from PySide6.QtGui import QAction, QPainter, QFont, QColor, QIcon
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt, Signal, QSize, QEvent, QRect, QTimer  # 添加 QRect 导入
from PySide6.QtWidgets import QWidget, QInputDialog
from utils.logger_utils import logger
from utils.path import get_icon_path
from sqlalchemy.orm import Session
from db.models import MarkdownFileHistory
from datetime import datetime
from utils.time_utils import get_readable_time, get_duration
from app.app_style import AppStyle
from PySide6.QtGui import QColor, QFont, QPainter, QPen  # 添加 QPen 导入
from PySide6.QtWidgets import QDialog, QFormLayout, QLabel, QLineEdit, QVBoxLayout, QPushButton


class HistoryItemDelegate(QStyledItemDelegate):
    # 定义 tag 到颜色的映射表，方便扩展
    tag_color_map = {
        'md': QColor(159, 200, 156), 
        'pdf': QColor(145, 200, 228),
        'png': QColor(173, 178, 212),  
        'jpeg': QColor(15, 130, 140), 
        'csv': QColor(163, 220, 154), 
        'docx': QColor(151, 176, 103),
        'doc': QColor(151, 176, 103),
        'xls': QColor(67, 112, 87),
        'xlsx': QColor(67, 112, 87),
        'ppt': QColor(255, 166, 115),
        'pptx': QColor(255, 166, 115),
        'epub': QColor(100, 226, 183),
    }
    default_color = QColor(128, 128, 128)    # 默认灰色

    def __init__(self, parent=None):
        super().__init__(parent)
        self.delete_icon = QIcon(get_icon_path('trash-selected'))  # 假设图标文件名为 trash
        #self.delete_selected_icon = QIcon(get_icon_path('trash-selected'))
        self.parent = parent  # 保存父对象引用

    def _format_time(self, modified_time):
        return get_readable_time(modified_time)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index):
        painter.save()

        if option.state & QStyle.State_Selected:
            painter.setBrush(QColor(25, 144, 255, 38))
            painter.setPen(Qt.NoPen)  # 设置无边框
            # 添加绘制背景矩形的代码
            painter.drawRect(option.rect)  # 绘制完整项的背景
        elif option.state & QStyle.State_MouseOver:
            painter.setBrush(QColor(25, 144, 255, 25))
            painter.setPen(Qt.NoPen)  # 设置无边框
            painter.drawRect(option.rect)  # 绘制完整项的背景
        else:
            painter.setPen(Qt.NoPen)  # 设置无边框

        # Get item data
        item_data = index.data(Qt.UserRole)
        if item_data:
            title = item_data.get('title', '')
            modified_time = item_data.get('updated_at', '')
            if item_data.get('status', '') == 'processing':
                preview_suffix = '后台处理中...'
            else:
                preview_suffix = "处理耗时：{}s".format(get_duration(item_data.get('converter_start', ''), item_data.get('converter_end', '')).seconds)
            preview = "{} {}".format(item_data.get('converter', ''), preview_suffix)
            formatted_time = self._format_time(modified_time)
            tag = item_data.get('tags', '')  # 获取 tag 字段

            # 设置边距
            margin = 10
            text_rect = option.rect.adjusted(margin, margin, -margin, -margin)

            # 绘制 tag 角标
            if tag:
                tag_font = QFont()
                tag_font.setPointSize(8)
                painter.setFont(tag_font)
                painter.setPen(QColor(255, 255, 255))

                # 根据 tag 内容获取对应的颜色，如果没有匹配则使用默认颜色
                painter.setBrush(self.tag_color_map.get(tag, self.default_color))

                tag_width = painter.fontMetrics().horizontalAdvance(tag) + 8
                tag_height = 16
                tag_x = text_rect.x()  # 设置 x 坐标为文本区域左侧
                tag_y = text_rect.y() + 5
                painter.drawRoundedRect(tag_x, tag_y, tag_width, tag_height, 4, 4)
                painter.drawText(tag_x + 4, tag_y + 12, tag)

                # 调整标题的起始位置，避免和 tag 角标重叠
                text_rect = text_rect.adjusted(tag_width + 5, 0, 0, 0)

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

            # 鼠标悬停时绘制删除按钮
            if option.state & QStyle.State_MouseOver:
                button_width = 20
                button_height = 20
                button_x = option.rect.right() - button_width - 10
                button_y = option.rect.top() + (option.rect.height() - button_height) // 2
                # 扩大点击区域，四周各增加 5 像素
                padding = 10
                # 修改为局部变量，避免所有项共享同一个删除按钮区域
                delete_button_rect = QRect(
                    button_x - padding,
                    button_y - padding,
                    button_width + padding * 2,
                    button_height + padding * 2
                )
                # 存储删除按钮区域到 index 中，用于 editorEvent 判断
                index.model().setData(index, delete_button_rect, Qt.UserRole + 1)
                painter.drawPixmap(
                    button_x, button_y, self.delete_icon.pixmap(
                        button_width, button_height))
            else:
                # 非悬停状态清除存储的删除按钮区域
                index.model().setData(index, None, Qt.UserRole + 1)

        # 绘制分割线
        if option.state & QStyle.State_Selected:
            painter.setPen(QPen(QColor(25, 144, 255), 1))  # 选中状态使用蓝色
        else:
            painter.setPen(QPen(QColor(220, 220, 220), 1))  # 非选中状态使用浅灰色
        line_y = option.rect.bottom() - 1
        painter.drawLine(option.rect.left() + margin, line_y, option.rect.right() - margin, line_y)

        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index):
        # Bug fix: Call width() method to get the width value
        return QSize(option.rect.width(), 50)

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.MouseButtonDblClick and event.button() == Qt.LeftButton:
            logger.debug("检测到鼠标双击事件")
            item_data = index.data(Qt.UserRole)
            if item_data:
                if isinstance(self.parent, QListWidget):
                    history_panel = self.parent.parent()
                    if hasattr(history_panel, 'edit_item_title'):
                        # 修改为调用新对话框
                        history_panel.edit_item_title(index)
        if event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
            logger.debug("检测到鼠标左键释放事件")
            # 从 index 中获取当前项的删除按钮区域
            delete_button_rect = index.data(Qt.UserRole + 1)
            if delete_button_rect:
                # 直接使用 event.pos()，不进行坐标转换
                if delete_button_rect.contains(event.pos()):
                    logger.debug("点击了删除按钮")
                    item_data = index.data(Qt.UserRole)
                    if item_data and 'id' in item_data:
                        logger.debug(f"尝试删除ID为 {item_data['id']} 的记录")
                        if isinstance(self.parent, QListWidget):
                            history_panel = self.parent.parent()
                            if hasattr(history_panel, 'delete_item'):
                                history_panel.delete_item(item_data['id'])
        return super().editorEvent(event, model, option, index)

class MarkdownEditDialog(QDialog):
    def __init__(self, markdown_data, parent=None):
        super().__init__(parent)
        self.markdown_data = markdown_data
        self.init_ui()
        self.setWindowTitle('编辑 Markdown 信息')
        self.resize(450, 350)
        self.setStyleSheet("""
            /* Fluent UI 颜色变量 */
            QDialog {
                background-color: #F3F2F1;
                font-family: 'Segoe UI', 'Segoe UI Web (West European)', 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, 'Helvetica Neue', sans-serif;
            }
            
            QLabel {
                font-size: 14px;
                color: #323130;
                font-weight: 400;
                border: none;
                background: transparent;
            }
            
            QLineEdit {
                font-size: 14px;
                padding: 8px 12px;
                border: 1px solid #D2D0CE;
                border-radius: 2px;
                background-color: #FFFFFF;
                selection-background-color: #0078D4;
                selection-color: #FFFFFF;
            }
            
            QLineEdit:focus {
                border: 1px solid #0078D4;
                outline: 2px solid #71afe5;
            }
            
            QPushButton {
                background-color: #0078D4;
                color: #FFFFFF;
                border: none;
                padding: 8px 16px;
                text-align: center;
                text-decoration: none;
                font-size: 14px;
                border-radius: 2px;
                min-width: 80px;
                font-weight: 600;
            }
            
            QPushButton:hover {
                background-color: #106EBE;
            }
            
            QPushButton:pressed {
                background-color: #005A9E;
            }
            
            QPushButton:disabled {
                background-color: #F3F2F1;
                color: #A19F9D;
            }
        """)

    def init_ui(self):
        # 使用 QFormLayout 作为主布局
        form_layout = QFormLayout()
        form_layout.setVerticalSpacing(16)
        form_layout.setHorizontalSpacing(20)
        form_layout.setContentsMargins(24, 24, 24, 24)

        # 标题编辑框
        self.title_edit = QLineEdit(self.markdown_data.get('title', ''))
        self.title_edit.setStyleSheet("font-weight: 600;")
        form_layout.addRow('<b>标题:</b>', self.title_edit)

        # 其他只读属性
        # 对键进行排序以保证顺序
        for key in sorted(self.markdown_data.keys()):
            if key != 'title':
                value = self.markdown_data[key]
                label = QLabel(str(value))
                # 设置左对齐
                label.setAlignment(Qt.AlignLeft)
                # 仅保留文字颜色和大小设置，移除所有可能产生边框的样式
                label.setStyleSheet('color: #605E5C; font-size: 14px; border: none; background: transparent;')
                form_layout.addRow(f'<b>{key}:</b>', label)

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignRight)
        confirm_button = QPushButton('确认')
        confirm_button.setDefault(True)
        confirm_button.clicked.connect(self.accept)
        button_layout.addWidget(confirm_button)

        # 将按钮布局添加到表单布局下方
        form_layout.addRow(button_layout)

        self.setLayout(form_layout)

    def get_new_title(self):
        return self.title_edit.text()

    def showEvent(self, event):
        super().showEvent(event)
        # 在对话框显示时设置输入框宽度为对话框宽度的 50%
        self.title_edit.setMaximumWidth(int(self.width() * 0.7))

class HistoryPanel(QWidget):
    # 定义保存完成信号
    save_complete = Signal()
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
        self.history_list.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 禁用水平滚动条
        from PySide6.QtCore import Qt
        self.history_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.history_list.setItemDelegate(
            HistoryItemDelegate(self.history_list))
        # 设置列表项可编辑
        self.history_list.setEditTriggers(
            QtWidgets.QAbstractItemView.DoubleClicked
        )
        self.init_ui()
        self.load_history_items()
        self.switch_pending = None  # 存储待切换的项数据
        self.save_complete.connect(self._complete_item_switch)
        self.history_list.clicked.connect(self.on_item_clicked)

    def init_ui(self):
        main_layout = QVBoxLayout()
        # 设置主布局内容边距，上右下左均为5px
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # 创建搜索和新建按钮的水平布局
        search_layout = QHBoxLayout()
        search_layout.setSpacing(5)
        
        # 创建美观的搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索历史记录...")
        self.search_input.setStyleSheet('''
            QLineEdit {
                border: 2px solid #ddd;
                border-radius: 15px;
                padding: 8px 15px;
                font-size: 14px;
            }
            QLineEdit:hover {
                border-color: #E6F6FF;
                background-color: #F5F9FF;
            }
            QLineEdit:focus {
                border-color: #2591FF;
                background-color: white;
                outline: none;
            }
        ''')
        self.search_input.textChanged.connect(self.filter_history)
        self.search_input.returnPressed.connect(self.filter_history)
        
        # 创建新建按钮
        self.new_btn = QPushButton()
        # 设置可选中状态
        self.new_btn.setCheckable(True)
        # 初始图标（默认状态）
        self.new_btn.setIcon(QIcon(get_icon_path("pencil-square", selected=False)))
        self.new_btn.setIconSize(QtCore.QSize(20, 20))
        # 应用统一侧边栏按钮样式
        self.new_btn.setStyleSheet(AppStyle().get_sidebar_button_style())
        # 连接状态切换信号
        self.new_btn.clicked.connect(self.create_new_markdown)
        
        # 添加到水平布局
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.new_btn)
        
        # 添加到主布局
        main_layout.addLayout(search_layout)
        
        # 设置搜索框和历史列表之间的间距为5px
        main_layout.setSpacing(5)
        
        # 优化列表项选中样式，与全局风格保持一致
        self.history_list.viewport().setMouseTracking(True)
        self.history_list.setStyleSheet('''
            QListWidget {
                border: 2px solid #ddd;
                border-radius: 8px;
                padding: 0;
                margin-top: 0px; /* 移除原有的margin-top设置 */
            }
            QListWidget::item {
                border: 2px solid transparent;
                padding: 5px 10px;
                background-color: #f0f0f0;
                border-bottom: 1px solid #ddd !important;
            }
            QListWidget::item:last {
                border-bottom: none !important;
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
                background-color: white;
            }
        ''')

    def edit_item_title(self, index):
        """处理双击编辑标题逻辑"""
        item_data = index.data(Qt.UserRole)
        if not item_data:
            return
        dialog = MarkdownEditDialog(item_data, self)
        if dialog.exec():  # 显示对话框并等待用户操作
            new_title = dialog.get_new_title()
            if new_title:
                item_data['title'] = new_title
                # 更新 index 数据
                self.history_list.model().setData(index, item_data, Qt.UserRole)
                # 调用数据库更新逻辑，需根据实际情况实现
                if 'id' in item_data:
                    self.markdown_manager.update_title(item_data['id'], new_title)

    def on_item_clicked(self, index):
        # 修改获取数据的方式
        item = self.history_list.itemFromIndex(index)
        if not item:
            logger.warning("未找到点击的列表项")
            return
        data = item.data(Qt.UserRole)
        if data and 'id' in data:
            # 确保 parent 和 current_file 属性存在
            if hasattr(self.parent, 'current_file'):
                current_id = self.parent.current_file.get('id') if self.parent.current_file else None
                # 检查当前点击项是否和 current_file 是同一项目
                if current_id == data['id']:
                    logger.debug(f"点击的是当前正在查看的历史记录项: {data['id']}，跳过处理")
                    return
            
            # 存储待切换的项数据
            self.switch_pending = data
            # 在切换前保存当前 markdown 内容
            self.save_current_file()
        else:
            logger.warning("点击的列表项数据为空或缺少ID字段")

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
            logger.debug(
                f"历史列表模型是否设置成功: {
                    self.history_list.model() is not None}")
            logger.debug("历史记录过滤完成。")
        except Exception as e:
            logger.error(f"过滤历史记录时发生错误: {e}", exc_info=True)

    def save_current_file(self):
        """保存选中的文件"""
        try:
            # 在调用异步方法前保存当前文件的 ID
            current_file_id = None
            if self.parent.current_file and self.parent.current_file.get('id'):
                current_file_id = self.parent.current_file['id']

            # 获取当前内容，使用异步回调确保获取到最新内容
            def handle_content(content):
                if current_file_id:
                    self.markdown_manager.save_markdown(
                        id=current_file_id,
                        content=content
                    )
                    logger.info(f"成功保存 ID 为 {current_file_id} 的内容")
                # 添加保存完成信号发射
                self.save_complete.emit()

            js_code = """
                    if (window.editor) {
                        window.editor.getMarkdown();
                    } else {
                        '';
                    }
            """
            self.parent.markdown_editor.preview.page().runJavaScript(js_code, handle_content)
        except Exception as e:
            logger.error(f"保存内容失败: {str(e)}")
            self.save_complete.emit()  # 出错时也发射信号，避免阻塞

    def _complete_item_switch(self):
        """完成历史项切换"""
        if self.switch_pending:
            data = self.switch_pending
            logger.debug(f"点击的列表项ID: {data['id']}")
            # 找到对应的完整历史记录项
            selected_item = next(
                (x for x in self.all_history_items if x['id'] == data['id']), None)
            self.parent.current_file = selected_item
            if selected_item:
                logger.debug(f"找到匹配的历史记录项: {selected_item}")
                self.history_item_selected.emit(selected_item)
            else:
                logger.warning(f"未找到ID为 {data['id']} 的历史记录项")
            self.switch_pending = None

    def rename_selected_file(self):
        """重命名选中的文件"""
        current_file = self.parent.current_file
        if not current_file:
            return
        # 修改获取项的方式
        old_title = current_file['title']
        new_title, ok = QInputDialog.getText(self, '重命名标题', '请输入新标题:', text=old_title)
        if ok and new_title and new_title != old_title:
            try:
                # 使用 save_markdown 方法更新标题
                self.markdown_manager.save_markdown(
                    id=current_file['id'],
                    title=new_title
                )
                self.load_history_items()
                logger.debug(f"重命名后历史记录数量: {len(self.all_history_items)}")
                # 新增刷新搜索结果逻辑
                self.filter_history()
                self.file_renamed.emit(old_title, new_title)
            except Exception as e:
                logger.error(f"重命名文件失败: {e}")

    def delete_selected_file(self):
        """删除选中的历史记录"""
        index = self.history_list.currentIndex()
        if not index.isValid():
            return
        # 修改获取项的方式
        item = self.history_list.itemFromIndex(index)
        if not item:
            return
        data = item.data(Qt.UserRole)
        if not data:
            return
        if 'id' not in data:
            return
        # 显示确认对话框
        reply = QMessageBox.question(
            self, '确认删除', '确定要删除该文件吗？',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return
        try:
            if self.markdown_manager.delete_history_item(data['id']):
                self.load_history_items()
                # 清空编辑区
                if hasattr(self.parent, 'markdown_editor'):
                    self.parent.markdown_editor.reset()
                # 设置 current_file 为空
                if hasattr(self.parent, 'current_file'):
                    self.parent.current_file = None
            else:
                logger.warning(f'无法删除历史记录: {data}')
        except Exception as e:
            logger.error(f"删除历史记录失败: {e}")
            
    def create_new_markdown(self):
        """创建新的markdown文档"""
        from utils import time_utils
        timestamp = time_utils.now().strftime('%Y%m%d%H%M%S')
        new_item = {
            'title': 'manual-{}'.format(timestamp),
            'content': '',
            'tags': 'md',
            'status': 'processed',
            'converter': 'manual',
        }
        # 保存到数据库
        self.markdown_manager.save_markdown(**new_item)
        # 刷新历史列表
        self.load_history_items()
        # 选择新创建的项目
        if self.history_list.count() > 0:
            self.history_list.setCurrentRow(0)
            self.on_item_clicked(self.history_list.model().index(0, 0))

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

    def delete_item(self, item_id):
        """删除指定ID的历史记录"""
        logger.debug(f"准备删除ID为 {item_id} 的历史记录，显示确认对话框")
        # 获取当前要删除的历史记录项
        item = next(
            (x for x in self.all_history_items if x['id'] == item_id),
            None)
        if not item:
            logger.warning(f'未找到ID为 {item_id} 的历史记录')
            return

        title = item.get('title', '')
        preview = item.get('content', '')[
            :50] + ('...' if len(item.get('content', '')) > 50 else '')

        # 显示确认对话框
        msg_box = QMessageBox()
        msg_box.setWindowTitle('确认删除')
        msg_box.setText('确定要删除该文件吗？')
        msg_box.setInformativeText(f'文件名: {title}\n文件预览: {preview}')

        # 设置按钮
        delete_btn = msg_box.addButton('删除', QMessageBox.AcceptRole)

        # 设置删除按钮为红色
        delete_btn.setStyleSheet(
            'QPushButton { color: white; background-color: #ff4444; border-radius: 4px; padding: 5px 15px; } QPushButton:hover { background-color: #cc0000; }')

        msg_box.exec_()

        if msg_box.clickedButton() != delete_btn:
            return
        logger.debug(f"用户确认删除ID为 {item_id} 的历史记录")
        try:
            if self.markdown_manager.delete_history_item(item_id):
                logger.info(f"成功删除ID为 {item_id} 的历史记录，刷新列表")
                self.load_history_items()
                # 清空编辑区
                self.parent.markdown_editor.reset()
                # 设置 current_file 为空
                self.parent.current_file = None
            else:
                logger.warning(f'无法删除历史记录: ID为 {item_id} 的记录')
        except Exception as e:
            logger.error(f"删除历史记录失败: {e}")