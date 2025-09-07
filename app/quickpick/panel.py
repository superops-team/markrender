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
    QWidgetAction,
    QLabel
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal, QSize, Qt, QTimer

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

    def __init__(self, markrender_manager, parent=None):
        self.parent = parent
        super().__init__(parent)
        self.app_style = AppStyle()
        self.markrender_manager = markrender_manager
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
                    self.markrender_manager.save_item(
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
            # 确保 parent 和 current_item 属性存在
            if hasattr(self.parent, 'current_item'):
                current_id = self.parent.current_item.get('id') if self.parent.current_item else None
                # 检查当前点击项是否和 current_item 是同一项目
                if current_id == data['id']:
                    logger.debug(f"点击的是当前正在查看的历史记录项: {data['id']}，跳过处理")
                    return

            # 存储待切换的项数据
            self.switch_pending = data
            # 在切换前保存当前 markdown 内容
            self.save_current_item()
        else:
            logger.warning("点击的列表项数据为空或缺少ID字段")

    def load_quickpick_items(self):
        """加载所有历史记录"""
        try:
            self.all_quickpick_items = self.markrender_manager.load_items()
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

    def save_current_item(self):
        """保存当前文件并执行页面切换 - 修复版本"""
        try:
            # 保存当前编辑内容
            if hasattr(self.parent, 'editor') and hasattr(self.parent.editor, 'save_current_item'):
                # 检查是否有当前项需要保存
                if self.parent.current_item:
                    # 检查编辑器是否有文件ID，如果没有则使用current_item的ID
                    editor_item_id = getattr(self.parent.editor.item, 'item_id', '') if hasattr(self.parent.editor, 'item') else ''
                    current_item_id = self.parent.current_item.get('id', '')
                    
                    # 如果编辑器没有ID但current_item有ID，则使用current_item的ID
                    if not editor_item_id and current_item_id:
                        logger.info(f"编辑器缺少文件ID，使用current_item ID: {current_item_id}")
                        editor_item_id = current_item_id
                        # 同时更新编辑器的item_id
                        self.parent.editor.set_item_id(current_item_id)
                    
                    can_save = bool(editor_item_id)
                    
                    if can_save:
                        logger.info(msg=f"切换页面触发保存动作，文件->{self.parent.current_item.get('title')}")
                        
                        # 使用回调方式保存，确保获取到内容后再切换页面
                        self._save_with_callback()
                        return  # 等待回调完成后再执行页面切换
                    else:
                        logger.info(f"当前文档未关联文件ID，跳过保存: {self.parent.current_item.get('title')}")
                else:
                    logger.info("没有当前项需要保存")
            else:
                logger.warning("编辑器或保存方法不可用")
            
            # 如果不需要保存或保存方法不可用，直接执行页面切换
            self._execute_switch()
            
        except Exception as e:
            import traceback
            logger.error(f"保存当前文件并切换页面失败: {e}")
            logger.error(traceback.format_exc())
            # 弹窗报错
            QMessageBox.warning(self, "切换失败", f"页面切换过程中发生错误: {str(e)}")
            # 清除待切换状态
            self.switch_pending = None
    
    def _save_with_callback(self):
        """使用回调方式保存，确保获取到内容后再切换页面"""
        success = self.parent.editor.save_current_item()
        if not success:
            logger.error("保存当前文件失败，取消页面切换")
            # 弹窗报错
            QMessageBox.warning(self, "保存失败", "无法保存当前文件，请稍后再试。")
            # 清除待切换状态
            self.switch_pending = None
            return
        # 保存成功，执行页面切换
        logger.info("保存成功，执行页面切换")
        self._execute_switch()

    
    def _save_with_retry(self, callback, retry_count=3):
        """带重试机制的保存方法"""
        def internal_callback(success):
            if not success and retry_count > 0:
                logger.warning(f"保存失败，剩余重试次数: {retry_count}")
                # 等待一段时间后重试
                from PySide6.QtCore import QTimer
                retry_timer = QTimer()
                retry_timer.setSingleShot(True)
                retry_timer.timeout.connect(lambda: self._save_with_retry(callback, retry_count-1))
                retry_timer.start(1000)  # 等待1秒后重试
            else:
                callback(success)
        
        self.parent.editor.save_current_item(callback=internal_callback)


    def _execute_switch(self):
        """执行页面切换"""
        if self.switch_pending:
            logger.debug(f"执行页面切换: {self.switch_pending.get('title')}")
            # 调用父窗口的update_editor_and_previewer方法
            if hasattr(self.parent, 'update_editor_and_previewer'):
                self.parent.update_editor_and_previewer(self.switch_pending)
            else:
                logger.error("父窗口没有update_editor_and_previewer方法")
                # 弹窗报错
                QMessageBox.warning(self, "切换失败", "无法执行页面切换，请稍后再试。")
            
            # 清除待切换状态
            self.switch_pending = None
        else:
            logger.debug("没有待切换的项目")
        
    def _complete_item_switch(self):
        """完成历史项切换"""
        if self.switch_pending:
            data = self.switch_pending
            logger.debug(f"点击的列表项ID: {data['id']}")
            # 找到对应的完整历史记录项
            selected_item = next(
                (x for x in self.all_quickpick_items if x['id'] == data['id']), None)
            self.parent.current_item = selected_item
            if selected_item:
                logger.debug(f"找到匹配的快速选择记录项: {selected_item}")
                self.quickpick_item_selected.emit(selected_item)
            else:
                logger.warning(f"未找到ID为 {data['id']} 的快速选择记录项")
            self.switch_pending = None

    def rename_selected_file(self):
        """重命名选中的文件"""
        current_item = self.parent.current_item
        if not current_item:
            return
        # 修改获取项的方式
        old_title = current_item['title']
        new_title, ok = QInputDialog.getText(self, '重命名标题', '请输入新标题:', text=old_title)
        if ok and new_title and new_title != old_title:
            try:
                # 使用 save_item 方法更新标题
                self.markrender_manager.save_item(
                    id=current_item['id'],
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
            if self.markrender_manager.delete_item(data['id']):
                self.load_quickpick_items()
                # 清空编辑区
                if hasattr(self.parent, 'editor'):
                    self.parent.editor.reset()
                # 设置 current_item 为空
                if hasattr(self.parent, 'current_item'):
                    self.parent.current_item = None
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
        h_layout.setSpacing(4)  # 紧密间距
        h_layout.setContentsMargins(6, 4, 6, 4)  # 精简内边距

        # 导入需要的样式常量
        from app.preference.style_constants import NEUTRAL_600, FONT_SIZE_XS

        # 创建 内容 按钮组合（紧凑设计）
        content_container = QWidget()
        content_container.setFixedSize(36, 48)  # 固定小尺寸
        content_layout = QVBoxLayout(content_container)
        content_layout.setSpacing(2)  # 最小间距
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        content_btn = QPushButton()
        content_btn.setIcon(QIcon(get_icon_path("textarea")))
        content_btn.setIconSize(QSize(20, 20))  # 紧凑图标尺寸
        content_btn.setFixedSize(32, 32)  # 固定按钮尺寸
        content_btn.setToolTip("创建笔记")
        content_btn.clicked.connect(self.create_new_markdown_item)
        
        # 创建紧凑的 内容 标签
        content_label = QLabel("笔记")
        content_label.setAlignment(Qt.AlignCenter)
        content_label.setFixedHeight(12)  # 固定标签高度    
        
        content_layout.addWidget(content_btn, 0, Qt.AlignCenter)
        content_layout.addWidget(content_label, 0, Qt.AlignCenter)

        # 创建 Board 按钮组合（紧凑设计）
        board_container = QWidget()
        board_container.setFixedSize(36, 48)  # 固定小尺寸
        board_layout = QVBoxLayout(board_container)
        board_layout.setSpacing(2)  # 最小间距
        board_layout.setContentsMargins(0, 0, 0, 0)
        
        board_btn = QPushButton()
        board_btn.setIcon(QIcon(get_icon_path("excalidraw")))
        board_btn.setIconSize(QSize(20, 20))  # 紧凑图标尺寸
        board_btn.setFixedSize(32, 32)  # 固定按钮尺寸
        board_btn.setToolTip("创建画布")
        board_btn.clicked.connect(self.create_new_board_item)
        
        # 创建紧凑的 Board 标签
        board_label = QLabel("画布")
        board_label.setAlignment(Qt.AlignCenter)
        board_label.setFixedHeight(12)  # 固定标签高度
        
        board_layout.addWidget(board_btn, 0, Qt.AlignCenter)
        board_layout.addWidget(board_label, 0, Qt.AlignCenter)

        # 将按钮组合添加到水平布局
        h_layout.addWidget(content_container)
        h_layout.addWidget(board_container)

        # 将容器添加到菜单中
        menu_action = QWidgetAction(menu)
        menu_action.setDefaultWidget(container)
        menu.addAction(menu_action)

        # 在按钮下方显示菜单
        menu.exec(self.new_btn.mapToGlobal(self.new_btn.rect().bottomLeft()))

    def create_new_markdown_item(self):
        """创建新的笔记"""
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
        self.markrender_manager.save_item(**new_item)
        # 刷新快速选择列表
        self.load_quickpick_items()
        # 选择新创建的项目
        if self.quickpick_list.count() > 0:
            self.quickpick_list.setCurrentRow(0)
            self.on_item_clicked(self.quickpick_list.model().index(0, 0))

    def create_new_board_item(self):
        """创建新的Excalidraw记录"""
        from utils import time_utils
        timestamp = time_utils.now().strftime('%Y%m%d%H%M%S')
        new_item = {
            'title': 'Board-{}'.format(timestamp),
            'content': '',
            'tags': '',
            'status': 'processed',
            'page_type': 'excalidraw',
            'page_engine': 'excalidraw',
            'converter': 'manual',
        }
        # 保存到数据库
        self.markrender_manager.save_item(**new_item)
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

    def select_quickpick_item(self, current_item):
        """根据文件路径选择快速选择项"""
        if not current_item or 'id' not in current_item:
            logger.warning("传入的 current_item 为空或缺少 id 字段")
            return
        for i in range(self.quickpick_list.count()):
            item = self.quickpick_list.item(i)
            data = item.data(Qt.UserRole)
            if data and data.get('id') == current_item['id']:
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
            if self.markrender_manager.delete_item(item_id):
                logger.info(f"成功删除ID为 {item_id} 的快速选择记录，刷新列表")
                self.load_quickpick_items()
                # 清空编辑区
                self.parent.editor.reset()
                # 设置 current_item 为空
                self.parent.current_item = None
            else:
                logger.warning(f'无法删除快速选择记录: ID为 {item_id} 的记录')
        except Exception as e:
            logger.error(f"删除快速选择记录失败: {e}")
