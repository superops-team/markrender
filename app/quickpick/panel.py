from PySide6.QtWidgets import (
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
    QWidget,
    QInputDialog,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QLineEdit,
    QVBoxLayout,
    QPushButton,
    QSizePolicy,
    QAbstractItemView,
    QMenu,
    QWidgetAction
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal, QSize, Qt

from utils.logger_utils import logger
from utils.path import get_icon_path
from app.preference import AppStyle
from .item import QuickPickItemDelegate
from .edit_dialog import EditItemDialog


class QuickPickPanel(QWidget):
    # 定义保存完成信号
    save_complete = Signal()
    file_created = Signal(str)
    file_renamed = Signal(str, str)
    # 修改信号，传递完整的历史记录项
    quickpick_item_selected = Signal(dict)

    def __init__(self, markdown_manager, parent=None):
        self.parent = parent
        super().__init__(parent)
        self.app_style = AppStyle()
        self.markdown_manager = markdown_manager
        # 替换 MListView 为 QListWidget
        self.quickpick_list = QListWidget()
        # 设置 sizePolicy 为 Expanding
        self.quickpick_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 禁用水平滚动条
        self.quickpick_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.quickpick_list.setItemDelegate(
            QuickPickItemDelegate(self.quickpick_list))
        # 设置列表项可编辑
        self.quickpick_list.setEditTriggers(
            QAbstractItemView.DoubleClicked
        )
        self.init_ui()
        self.load_quickpick_items()
        self.switch_pending = None  # 存储待切换的项数据
        self.save_complete.connect(self._complete_item_switch)
        self.quickpick_list.clicked.connect(self.on_item_clicked)

    def init_ui(self):
        main_layout = QVBoxLayout()
        # 统一Editor区域的边距，确保高度对齐
        main_layout.setContentsMargins(5, 5, 5, 5)
        # 创建搜索和新建按钮的水平布局
        search_layout = QHBoxLayout()
        search_layout.setSpacing(8)  # 使用统一的小间距
        search_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)  # 垂直居中对齐

        # 创建美观的搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索历史记录...")
        # 使用统一的样式系统
        self.search_input.setStyleSheet(self.app_style.get_line_edit())
        self.search_input.setMinimumHeight(40)  # 统一高度，改善对齐
        self.search_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.search_input.textChanged.connect(self.filter_quickpick)
        self.search_input.returnPressed.connect(self.filter_quickpick)

        # 创建新建按钮
        self.new_btn = QPushButton()
        # 初始图标
        self.new_btn.setIcon(QIcon(get_icon_path("pencil-square", selected=False)))
        self.new_btn.setIconSize(QSize(20, 20))
        # 设置固定尺寸，与搜索框对齐
        self.new_btn.setFixedSize(40, 40)
        # 应用统一侧边栏按钮样式
        self.new_btn.setStyleSheet(self.app_style.get_sidebar_button_style())
        # 连接点击事件到显示菜单方法
        self.new_btn.clicked.connect(self.show_create_menu)

        # 添加到水平布局
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.new_btn)

        # 添加到主布局
        main_layout.addLayout(search_layout)

        # 设置搜索框和历史列表之间的间距为8px
        main_layout.setSpacing(8)

        # 优化列表项选中样式，与全局风格保持一致
        self.quickpick_list.viewport().setMouseTracking(True)
        self.quickpick_list.setStyleSheet(self.app_style.get_quickpick_panel())
        main_layout.addWidget(self.quickpick_list)
        # 设置布局后，设置统一的背景色
        self.setLayout(main_layout)

        # 简化整体样式，与全局设计保持一致
        self.setStyleSheet('''
            QuickPickPanel {
                background-color: white;
                border: none;
            }
        ''')

    def edit_item(self, index):
        """处理双击编辑标题逻辑"""
        item_data = index.data(Qt.UserRole)
        if not item_data:
            return
        dialog = EditItemDialog(item_data, self)
        if dialog.exec():  # 显示对话框并等待用户操作
            new_title = dialog.get_new_title()
            if new_title:
                item_data['title'] = new_title
                item_data['tags'] = dialog.get_new_tags()
                # 更新 index 数据
                self.quickpick_list.model().setData(index, item_data, Qt.UserRole)
                # 调用数据库更新逻辑，需根据实际情况实现
                if 'id' in item_data:
                    self.markdown_manager.save_markdown(
                        id=item_data['id'],
                        title=new_title,
                        tags=item_data['tags'],
                    )

    def on_item_clicked(self, index):
        # 修改获取数据的方式
        item = self.quickpick_list.itemFromIndex(index)
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

    def load_quickpick_items(self):
        """加载所有历史记录"""
        try:
            self.all_quickpick_items = self.markdown_manager.load_items()
            if self.all_quickpick_items:
                logger.info(f"成功加载 {len(self.all_quickpick_items)} 条记录")
            else:
                logger.info("未找到记录")
            self.filter_quickpick()
        except Exception as e:
            logger.error(f"加载记录失败: {e}", exc_info=True)

    def filter_quickpick(self):
        """根据搜索框过滤记录"""
        try:
            logger.debug("开始过滤记录...")
            # 清除当前列表中的数据
            self.quickpick_list.clear()
            search_text = self.search_input.text().lower()
            logger.debug(f"搜索关键字: {search_text}")

            logger.debug(f"当前所有记录数量: {len(self.all_quickpick_items)}")
            for item in self.all_quickpick_items:
                if search_text in item['title'].lower():
                    logger.debug(f"找到匹配项: {item}")
                    # 创建自定义列表项
                    list_item = QListWidgetItem()
                    list_item.setData(Qt.UserRole, item)
                    # 设置列表项文本，确保项可见
                    list_item.setText(item.get('title', ''))
                    self.quickpick_list.addItem(list_item)
            logger.debug(f"过滤后匹配项数量: {self.quickpick_list.count()}")
            logger.debug(
                f"快速选择列表模型是否设置成功: {
                    self.quickpick_list.model() is not None}")
            logger.debug("快速选择记录过滤完成。")
        except Exception as e:
            logger.error(f"过滤快速选择记录时发生错误: {e}", exc_info=True)

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

            # 通过Web通信方式获取编辑器内容
            if hasattr(self.parent.markdown_editor, 'web_comm') and hasattr(self.parent.markdown_editor.web_comm, 'send_message'):
                def handle_web_response(response):
                    logger.debug(f"切换item前收到Web通信响应: {response}")
                    # 处理Web通信返回的响应
                    content = response.get('content', '') if response else ''
                    handle_content(content)

                # 发送消息请求获取Markdown内容
                self.parent.markdown_editor.web_comm.send_message('getMarkdown', {}, handle_web_response)
                logger.debug("已发送获取Markdown内容的Web通信请求")
            else:
                # 回退方案：使用原有的直接执行JS方式
                js_code = """
                    if (window.appState.editor) {
                        window.appStat.editor.getMarkdown();
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
                (x for x in self.all_quickpick_items if x['id'] == data['id']), None)
            self.parent.current_file = selected_item
            if selected_item:
                logger.debug(f"找到匹配的快速选择记录项: {selected_item}")
                self.quickpick_item_selected.emit(selected_item)
            else:
                logger.warning(f"未找到ID为 {data['id']} 的快速选择记录项")
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
                self.load_quickpick_items()
                logger.debug(f"重命名后快速选择记录数量: {len(self.all_quickpick_items)}")
                # 新增刷新搜索结果逻辑
                self.filter_quickpick()
                self.file_renamed.emit(old_title, new_title)
            except Exception as e:
                logger.error(f"重命名文件失败: {e}")

    def delete_selected_file(self):
        """删除选中的快速选择记录"""
        index = self.quickpick_list.currentIndex()
        if not index.isValid():
            return
        # 修改获取项的方式
        item = self.quickpick_list.itemFromIndex(index)
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
            if self.markdown_manager.delete_item(data['id']):
                self.load_quickpick_items()
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

    def show_create_menu(self):
        """显示创建菜单"""
        menu = QMenu(self)

        # 使用统一的菜单样式生成器
        from app.preference.style_utils import create_menu_style
        menu.setStyleSheet(create_menu_style())

        # 创建一个容器widget用于放置按钮
        container = QWidget()
        h_layout = QHBoxLayout(container)
        h_layout.setSpacing(6)  # 提升亲密性，减少间距
        h_layout.setContentsMargins(8, 8, 8, 8)  # 统一内边距

        # 创建Markdown按钮
        markdown_btn = QPushButton()
        markdown_btn.setIcon(QIcon(get_icon_path("textarea")))
        markdown_btn.setIconSize(QSize(24, 24))  # 统一图标尺寸
        markdown_btn.setToolTip("创建笔记")  # 设置悬停提示
        markdown_btn.clicked.connect(self.create_new_markdown_item)

        # 创建Board按钮
        board_btn = QPushButton()
        board_btn.setIcon(QIcon(get_icon_path("diagram")))
        board_btn.setIconSize(QSize(24, 24))  # 统一图标尺寸
        board_btn.setToolTip("创建画布")  # 设置悬停提示
        board_btn.clicked.connect(self.create_new_board_item)

        # 将按钮添加到水平布局
        h_layout.addWidget(markdown_btn)
        h_layout.addWidget(board_btn)

        # 将容器添加到菜单中
        menu_action = QWidgetAction(menu)
        menu_action.setDefaultWidget(container)
        menu.addAction(menu_action)

        # 在按钮下方显示菜单
        menu.exec(self.new_btn.mapToGlobal(self.new_btn.rect().bottomLeft()))

    def create_new_markdown_item(self):
        """创建新的Markdown记录"""
        from utils import time_utils
        timestamp = time_utils.now().strftime('%Y%m%d%H%M%S')
        new_item = {
            'title': 'MD-{}'.format(timestamp),
            'content': '',
            'tags': '',
            'status': 'processed',
            'page_type': 'markdown',
            'converter': 'manual',
        }
        # 保存到数据库
        self.markdown_manager.save_markdown(**new_item)
        # 刷新快速选择列表
        self.load_quickpick_items()
        # 选择新创建的项目
        if self.quickpick_list.count() > 0:
            self.quickpick_list.setCurrentRow(0)
            self.on_item_clicked(self.quickpick_list.model().index(0, 0))

    def create_new_board_item(self):
        """创建新的Board记录"""
        from utils import time_utils
        timestamp = time_utils.now().strftime('%Y%m%d%H%M%S')
        new_item = {
            'title': 'Board-{}'.format(timestamp),
            'content': '',
            'tags': '',
            'status': 'processed',
            'page_type': 'board',
            'converter': 'manual',
        }
        # 保存到数据库
        self.markdown_manager.save_markdown(**new_item)
        # 刷新快速选择列表
        self.load_quickpick_items()
        # 选择新创建的项目
        if self.quickpick_list.count() > 0:
            self.quickpick_list.setCurrentRow(0)
            self.on_item_clicked(self.quickpick_list.model().index(0, 0))

    def toggle_visibility(self):
        """切换面板可见性"""
        if self.isVisible():
            self.hide()
        else:
            self.show()

    def select_quickpick_item(self, current_file):
        """根据文件路径选择快速选择项"""
        if not current_file or 'id' not in current_file:
            logger.warning("传入的 current_file 为空或缺少 id 字段")
            return
        for i in range(self.quickpick_list.count()):
            item = self.quickpick_list.item(i)
            data = item.data(Qt.UserRole)
            if data and data.get('id') == current_file['id']:
                self.quickpick_list.setCurrentItem(item)
                break

    def delete_item(self, item_id):
        """删除指定ID的快速选择记录"""
        logger.debug(f"准备删除ID为 {item_id} 的快速选择记录，显示确认对话框")
        # 获取当前要删除的快速选择记录项
        item = next(
            (x for x in self.all_quickpick_items if x['id'] == item_id),
            None)
        if not item:
            logger.warning(f'未找到ID为 {item_id} 的快速选择记录')
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

        # 设置删除按钮样式 - 使用统一的样式生成器
        from app.preference.style_utils import danger_button
        delete_btn.setStyleSheet(danger_button())

        msg_box.exec_()

        if msg_box.clickedButton() != delete_btn:
            return
        logger.debug(f"用户确认删除ID为 {item_id} 的历史记录")
        try:
            if self.markdown_manager.delete_item(item_id):
                logger.info(f"成功删除ID为 {item_id} 的快速选择记录，刷新列表")
                self.load_quickpick_items()
                # 清空编辑区
                self.parent.markdown_editor.reset()
                # 设置 current_file 为空
                self.parent.current_file = None
            else:
                logger.warning(f'无法删除快速选择记录: ID为 {item_id} 的记录')
        except Exception as e:
            logger.error(f"删除快速选择记录失败: {e}")
