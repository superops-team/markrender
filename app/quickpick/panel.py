from PySide6.QtWidgets import (
    QVBoxLayout,
    QTreeWidget,
    QTreeWidgetItem,
    QLineEdit,
    QWidget,
    QInputDialog,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QSizePolicy,
    QAbstractItemView,
    QMenu,
    QWidgetAction,
    QLabel
)
from PySide6.QtGui import QAction
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal, QSize, Qt, QTimer
from app.quickpick.edit_dialog import DeleteConfirmDialog

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
        super().__init__(parent)
        self._parent = parent
        self.app_style = AppStyle()
        self.markrender_manager = markrender_manager
        # 替换 QListWidget 为 QTreeWidget
        self.quickpick_list = QTreeWidget()
        # 设置 sizePolicy 为 Expanding
        self.quickpick_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # 禁用水平滚动条
        self.quickpick_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # 设置自定义委托
        self.quickpick_list.setItemDelegate(QuickPickItemDelegate(self.quickpick_list))
        # 禁用双击编辑
        self.quickpick_list.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        # 配置树形控件
        self.quickpick_list.setHeaderHidden(True)  # 隐藏表头
        self.quickpick_list.setIndentation(16)  # TDesign风格的缩进
        # 启用右键菜单
        self.quickpick_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.quickpick_list.customContextMenuRequested.connect(self.show_tree_context_menu)
        # 设置单击item即可展开/折叠子节点
        self.quickpick_list.setExpandsOnDoubleClick(False)  # 禁用双击展开
        self.quickpick_list.setAllColumnsShowFocus(True)  # 确保所有列都能响应焦点
        self.quickpick_list.setRootIsDecorated(True)  # 确保根节点有装饰（展开/折叠图标）
        # 连接事件
        self.quickpick_list.itemClicked.connect(self.on_item_clicked_with_expand)  # 连接单击事件
        # 处理鼠标悬停以显示操作按钮
        self.quickpick_list.setMouseTracking(True)
        self.quickpick_list.viewport().setMouseTracking(True)
        
        # 初始化UI
        self.init_ui()
        self.load_quickpick_items()
        self.switch_pending = None  # 存储待切换的项数据
        self.save_complete.connect(self._complete_item_switch)

    def init_ui(self):
        main_layout = QVBoxLayout()
        # TDesign风格的边距
        main_layout.setContentsMargins(6, 6, 6, 6)
        # 创建搜索和新建按钮的水平布局
        search_layout = QHBoxLayout()
        search_layout.setSpacing(8)  # TDesign间距规范
        search_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)  # 垂直居中对齐

        # 创建TDesign风格的搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索历史记录...")
        # 使用统一的样式系统
        self.search_input.setStyleSheet(self.app_style.get_line_edit())
        self.search_input.setMinimumHeight(36)  # TDesign标准高度
        self.search_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.search_input.textChanged.connect(self.filter_quickpick)
        self.search_input.returnPressed.connect(self.filter_quickpick)

        # 创建新建按钮
        self.new_btn = QPushButton()
        # 初始图标
        self.new_btn.setIcon(QIcon(get_icon_path("folder", selected=False)))
        self.new_btn.setIconSize(QSize(18, 18))  # TDesign标准图标尺寸
        # 设置固定尺寸，与搜索框对齐
        self.new_btn.setFixedSize(36, 36)  # TDesign标准按钮尺寸
        # 应用TDesign风格的按钮样式
        self.new_btn.setStyleSheet("""
            QPushButton {
                background-color: #f5f5f5;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #e8f3ff;
                border-color: #b3d9ff;
            }
            QPushButton:pressed {
                background-color: #d0e1ff;
                border-color: #80bfff;
            }
        """)
        # 连接点击事件到创建子目录方法
        self.new_btn.clicked.connect(self.create_new_folder_item)
        # 添加ToolTip
        self.new_btn.setToolTip("新建文件夹")

        # 添加到水平布局
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.new_btn)

        # 添加到主布局
        main_layout.addLayout(search_layout)

        # 设置搜索框和历史列表之间的间距
        main_layout.setSpacing(8)

        # 应用TDesign风格的树形导航面板样式
        self.quickpick_list.viewport().setMouseTracking(True)
        self.quickpick_list.setStyleSheet(self.app_style.get_quickpick_panel())
        # 确保整个控件区域都能响应鼠标事件
        self.quickpick_list.setMouseTracking(True)
        main_layout.addWidget(self.quickpick_list)
        # 设置布局
        self.setLayout(main_layout)

        # TDesign风格的整体面板样式
        self.setStyleSheet('''
            QuickPickPanel {
                background-color: white;
                border: none;
            }
        ''')

    def edit_item(self, index):
        """处理双击编辑标题逻辑"""
        logger.info("edit_item方法被调用")
        logger.info(f"索引有效: {index.isValid()}")
        item = self.quickpick_list.itemFromIndex(index)
        if not item:
            logger.info("未找到对应的项")
            return
        item_data = item.data(0, Qt.ItemDataRole.UserRole)
        logger.info(f"项数据: {item_data}")
        if not item_data:
            logger.info("项数据为空")
            return
        dialog = EditItemDialog(item_data, self)
        logger.info("创建编辑对话框")
        if dialog.exec():  # 显示对话框并等待用户操作
            logger.info("编辑对话框已关闭，开始处理保存操作")
            new_title = dialog.get_new_title()
            logger.info(f"从对话框获取的新标题: {new_title}")
            # 获取并更新标签
            new_tags = dialog.get_new_tags()
            logger.info(f"从对话框获取的新标签: '{new_tags}'")
            
            # 更新item_data
            item_data['title'] = new_title
            item_data['tags'] = new_tags
            logger.info(f"更新后的item_data标题: {item_data['title']}")
            logger.info(f"更新后的item_data标签: '{item_data['tags']}'")
            
            # 获取可能更新的字段
            new_icon_type = dialog.get_new_icon_type()
            new_icon_path = dialog.get_new_icon_path()
            new_display_name = dialog.get_new_display_name()
            new_page_type = dialog.get_new_page_type()
            new_icon_color = dialog.get_new_icon_color()
            
            # 更新item_data中的字段，只更新非None的值
            if new_icon_type is not None:
                item_data['icon_type'] = new_icon_type
            if new_icon_path is not None:
                item_data['icon_path'] = new_icon_path
            if new_display_name is not None:
                item_data['display_name'] = new_display_name
            if new_page_type is not None:
                item_data['page_type'] = new_page_type
            if new_icon_color is not None:
                item_data['icon_color'] = new_icon_color
            
            # 调用数据库更新逻辑
            if 'id' in item_data:
                try:
                    # 构建更新参数字典，只包含需要更新的字段
                    update_params = {
                        'id': item_data['id'],
                        'title': item_data['title'],  # 使用更新后的标题
                        'tags': item_data['tags']  # 确保标签正确传递
                    }
                    logger.info(f"构建的更新参数字典: {update_params}")
                    
                    # 只添加非None的字段到更新参数中
                    if new_icon_type is not None:
                        update_params['icon_type'] = new_icon_type
                    if new_icon_path is not None:
                        update_params['icon_path'] = new_icon_path
                    if new_display_name is not None:
                        update_params['display_name'] = new_display_name
                    if new_page_type is not None:
                        update_params['page_type'] = new_page_type
                    if new_icon_color is not None:
                        update_params['icon_color'] = new_icon_color
                    
                    # 添加必要的额外字段，确保树形结构不被破坏
                    update_params['parent_id'] = item_data.get('parent_id')
                    update_params['order'] = item_data.get('order')
                    update_params['level'] = item_data.get('level')
                    update_params['is_folder'] = item_data.get('is_folder')
                    
                    logger.info(f"准备保存更新参数: {update_params}")
                    
                    # 执行数据库更新
                    self.markrender_manager.save_item(**update_params)
                    logger.info("数据库更新完成")
                    
                    # 更新树中的节点数据，而不是刷新整个树
                    self.find_and_update_item_in_tree(item_data['id'], item_data)
                    logger.info("树节点更新完成")
                    
                except Exception as e:
                    logger.error(f"保存项目属性失败: {e}")
                    QMessageBox.warning(self, "保存失败", f"无法保存属性更改: {str(e)}")
        logger.info("edit_item方法执行完成")

    def on_item_clicked(self, index):
        # 获取点击的项目数据
        item = self.quickpick_list.itemFromIndex(index)
        if not item:
            return
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if data and 'id' in data:
            # 确保 parent 和 current_item 属性存在
            if self._parent is not None and hasattr(self._parent, 'current_item'):
                current_item = getattr(self._parent, 'current_item', None)
                if current_item and 'id' in current_item:
                    current_id = current_item.get('id')
                    # 检查当前点击项是否和 current_item 是同一项目
                    if current_id == data['id']:
                        return  # 如果是同一项目，不执行切换
            
            # 发射选中信号
            self.quickpick_item_selected.emit(data)

    def on_item_clicked_with_expand(self, item, column):
        """处理item单击事件，如果是文件夹则展开/折叠子节点"""
        # 获取项数据
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if data:
            # 检查是否为文件夹或是否有子节点
            is_folder = data.get('is_folder', 0)
            has_children = 'children' in data and len(data['children']) > 0
            
            # 如果是文件夹或有子节点，则切换展开状态
            if is_folder or has_children:
                # 切换展开状态
                item.setExpanded(not item.isExpanded())
                logger.debug(f"切换节点展开状态: {data.get('title', 'Unknown')} -> {item.isExpanded()}")
            
            # 如果有ID，则处理项选择逻辑
            if 'id' in data:
                # 确保 parent 和 current_item 属性存在
                if self._parent is not None and hasattr(self._parent, 'current_item'):
                    current_item = getattr(self._parent, 'current_item', None)
                    if current_item:
                        current_id = current_item.get('id')
                        # 检查当前点击项是否和 current_item 是同一项目
                        if current_id == data['id']:
                            logger.debug(f"点击的是当前正在查看的历史记录项: {data['id']}，跳过处理")
                            return

                # 存储待切换的项数据
                self.switch_pending = data
                # 在切换前保存当前 markdown 内容
                self.save_current_item()
        else:
            logger.warning("点击的列表项数据为空")

    def load_quickpick_items(self):
        """加载所有历史记录"""
        try:
            # 获取完整的树形结构数据
            self.all_quickpick_items = self.markrender_manager.get_full_tree()
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
            
            # 获取搜索文本
            search_text = self.search_input.text().strip().lower()
            logger.debug(f"搜索关键字: {search_text}")
            
            def add_tree_items(parent_item, items):
                """递归添加树节点"""
                for item in items:
                    # 创建节点
                    if parent_item is None:
                        tree_item = QTreeWidgetItem()
                    else:
                        tree_item = QTreeWidgetItem(parent_item)
                    
                    # 设置节点数据
                    tree_item.setData(0, Qt.ItemDataRole.UserRole, item)
                    
                    # 设置节点文本，确保项可见
                    tree_item.setText(0, item.get('title', ''))
                    
                    # 确保所有层级的节点都正确设置数据和标志
                    tree_item.setFlags(
                        Qt.ItemFlag.ItemIsSelectable | 
                        Qt.ItemFlag.ItemIsEnabled | 
                        Qt.ItemFlag.ItemIsEditable
                    )
                    
                    # 如果有子节点，递归添加
                    if 'children' in item and item['children']:
                        add_tree_items(tree_item, item['children'])
                    
                    # 根据搜索条件决定是否添加到显示列表
                    # 确保即使title为空也能正确处理
                    title_lower = item.get('title', '').lower()
                    if not search_text or search_text in title_lower:
                        if parent_item is None:
                            # 如果没有父节点，则添加到顶层
                            self.quickpick_list.addTopLevelItem(tree_item)
                    elif parent_item is None:
                        # 如果不匹配搜索条件且没有父节点，检查子节点是否有匹配的
                        has_matching_children = False
                        if 'children' in item and item['children']:
                            def check_children(children):
                                for child in children:
                                    child_title_lower = child.get('title', '').lower()
                                    if search_text in child_title_lower:
                                        return True
                                    if 'children' in child and child['children']:
                                        if check_children(child['children']):
                                            return True
                                return False
                            has_matching_children = check_children(item['children'])
                        
                        # 如果有匹配的子节点，也添加到显示列表
                        if has_matching_children:
                            self.quickpick_list.addTopLevelItem(tree_item)
            
            # 添加树形结构数据
            add_tree_items(None, self.all_quickpick_items)
            
            logger.debug(f"过滤后匹配项数量: {self.quickpick_list.topLevelItemCount()}")
            logger.debug("快速选择记录过滤完成。")
        except Exception as e:
            logger.error(f"过滤快速选择记录时发生错误: {e}", exc_info=True)
        finally:
            # 确保在任何情况下都能保持UI响应性
            self.quickpick_list.viewport().update()
    
    def save_current_item(self):
        """保存当前文件并执行页面切换 - 修复版本"""
        try:
            # 保存当前编辑内容
            if self._parent is not None and hasattr(self._parent, 'editor') and hasattr(self._parent.editor, 'save_current_item'):
                # 检查是否有当前项需要保存
                if self._parent is not None and hasattr(self._parent, 'current_item'):
                    current_item = getattr(self._parent, 'current_item', None)
                    if current_item:
                        # 检查编辑器是否有文件ID，如果没有则使用current_item的ID
                        editor_item_id = ''
                        if hasattr(self._parent, 'editor'):
                            editor = getattr(self._parent, 'editor', None)
                            if editor and hasattr(editor, 'item'):
                                editor_item_id = getattr(editor, 'item', '')
                        
                        current_item_id = current_item.get('id', '')
                        
                        # 如果编辑器没有ID但current_item有ID，则使用current_item的ID
                        if not editor_item_id and current_item_id:
                            logger.info(f"编辑器缺少文件ID，使用current_item ID: {current_item_id}")
                            editor_item_id = current_item_id
                            # 同时更新编辑器的item_id
                            if hasattr(self._parent, 'editor'):
                                editor = getattr(self._parent, 'editor', None)
                                if editor and hasattr(editor, 'set_item_id'):
                                    editor.set_item_id(current_item_id)
                        
                        can_save = bool(editor_item_id)
                        
                        if can_save:
                            logger.info(msg=f"切换页面触发保存动作，文件->{current_item.get('title')}")
                            
                            # 使用回调方式保存，确保获取到内容后再切换页面
                            self._save_with_callback()
                            return  # 等待回调完成后再执行页面切换
                        else:
                            logger.info(f"当前文档未关联文件ID，跳过保存: {current_item.get('title')}")
                    else:
                        logger.info("没有当前项需要保存")
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
        if self._parent is not None and hasattr(self._parent, 'editor'):
            editor = getattr(self._parent, 'editor', None)
            if editor:
                success = editor.save_current_item()
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
        
        if self._parent is not None and hasattr(self._parent, 'editor'):
            editor = getattr(self._parent, 'editor', None)
            if editor:
                editor.save_current_item(callback=internal_callback)
    
    def _execute_switch(self):
        """执行页面切换"""
        if self.switch_pending:
            logger.debug(f"执行页面切换: {self.switch_pending.get('title')}")
            # 调用父窗口的update_editor_and_previewer方法
            if self._parent is not None and hasattr(self._parent, 'update_editor_and_previewer'):
                self._parent.update_editor_and_previewer(self.switch_pending)
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
            if self._parent is not None and hasattr(self._parent, 'current_item'):
                self._parent.current_item = selected_item
            if selected_item:
                logger.debug(f"找到匹配的快速选择记录项: {selected_item}")
                self.quickpick_item_selected.emit(selected_item)
            else:
                logger.warning(f"未找到ID为 {data['id']} 的快速选择记录项")
            self.switch_pending = None
    
    def rename_selected_file(self):
        """重命名选中的文件"""
        current_item = None
        if self._parent is not None and hasattr(self._parent, 'current_item'):
            current_item = getattr(self._parent, 'current_item', None)
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
        current_item = self.quickpick_list.currentItem()
        if not current_item:
            return
        data = current_item.data(0, Qt.ItemDataRole.UserRole)
        if not data:
            return
        if 'id' not in data:
            return
        # 显示自定义确认对话框
        title = data.get('title', '未命名文件')
        dialog = DeleteConfirmDialog(title, self)
        if not dialog.exec():
            return
        self._delete_item_and_select_next(data['id'], current_item)

    def _delete_item_and_select_next(self, item_id, current_item):
        """删除项目并选中下一个同级项目"""
        try:
            if self.markrender_manager.delete_item(item_id):
                # 获取下一个同级节点
                next_item_data = self._get_next_sibling_item(current_item)
                
                # 重新加载数据
                self.load_quickpick_items()
                
                # 如果有下一个同级节点，则选中它
                if next_item_data:
                    self._select_item_by_id(next_item_data['id'])
                else:
                    # 如果没有下一个同级节点，尝试选中父节点或第一个节点
                    parent_item_data = self._get_parent_item(current_item)
                    if parent_item_data:
                        self._select_item_by_id(parent_item_data['id'])
                    elif self.quickpick_list.topLevelItemCount() > 0:
                        # 选中第一个顶层节点
                        first_item = self.quickpick_list.topLevelItem(0)
                        if first_item:
                            first_data = first_item.data(0, Qt.ItemDataRole.UserRole)
                            if first_data:
                                self._select_item_by_id(first_data['id'])
                
                # 清空编辑区
                if self._parent is not None and hasattr(self._parent, 'editor'):
                    editor = getattr(self._parent, 'editor', None)
                    if editor:
                        editor.reset()
                # 设置 current_item 为空
                if self._parent is not None and hasattr(self._parent, 'current_item'):
                    self._parent.current_item = None
            else:
                # 获取当前项的数据用于日志记录
                data = current_item.data(0, Qt.ItemDataRole.UserRole)
                logger.warning(f'无法删除历史记录: {data}')
        except Exception as e:
            logger.error(f"删除历史记录失败: {e}")

    def _get_next_sibling_item(self, item):
        """获取同级的下一个节点"""
        # 获取父节点
        parent = item.parent()
        
        # 获取当前节点在父节点中的索引
        if parent:
            current_index = parent.indexOfChild(item)
            # 如果不是最后一个子节点，则返回下一个子节点
            if current_index < parent.childCount() - 1:
                next_item = parent.child(current_index + 1)
                if next_item:
                    return next_item.data(0, Qt.ItemDataRole.UserRole)
        else:
            # 如果是顶层节点，获取在顶层节点中的索引
            current_index = self.quickpick_list.indexOfTopLevelItem(item)
            # 如果不是最后一个顶层节点，则返回下一个顶层节点
            if current_index < self.quickpick_list.topLevelItemCount() - 1:
                next_item = self.quickpick_list.topLevelItem(current_index + 1)
                if next_item:
                    return next_item.data(0, Qt.ItemDataRole.UserRole)
        
        # 没有下一个同级节点
        return None

    def _get_parent_item(self, item):
        """获取父节点"""
        parent = item.parent()
        if parent:
            return parent.data(0, Qt.ItemDataRole.UserRole)
        return None

    def _select_item_by_id(self, item_id):
        """根据ID选中节点"""
        def find_and_select(parent_item):
            if parent_item is None:
                # 搜索顶层节点
                for i in range(self.quickpick_list.topLevelItemCount()):
                    item = self.quickpick_list.topLevelItem(i)
                    if item:
                        data = item.data(0, Qt.ItemDataRole.UserRole)
                        if data and data.get('id') == item_id:
                            self.quickpick_list.setCurrentItem(item)
                            # 发射选中信号
                            self.quickpick_item_selected.emit(data)
                            return True
                        # 递归搜索子节点
                        if find_and_select(item):
                            return True
            else:
                # 搜索子节点
                for i in range(parent_item.childCount()):
                    item = parent_item.child(i)
                    if item:
                        data = item.data(0, Qt.ItemDataRole.UserRole)
                        if data and data.get('id') == item_id:
                            self.quickpick_list.setCurrentItem(item)
                            # 发射选中信号
                            self.quickpick_item_selected.emit(data)
                            return True
                        # 递归搜索子节点的子节点
                        if find_and_select(item):
                            return True
            return False
        
        # 开始搜索
        find_and_select(None)

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
        content_container.setFixedSize(32, 40)  # 减小尺寸使布局更紧凑
        content_layout = QVBoxLayout(content_container)
        content_layout.setSpacing(2)  # 最小间距
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        content_btn = QPushButton()
        content_btn.setIcon(QIcon(get_icon_path("textarea")))
        content_btn.setIconSize(QSize(16, 16))  # 减小图标尺寸
        content_btn.setFixedSize(28, 28)  # 减小按钮尺寸
        content_btn.setToolTip("创建笔记")
        content_btn.clicked.connect(self.create_new_markdown_item)
        
        # 创建紧凑的 内容 标签
        content_label = QLabel("笔记")
        content_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_label.setFixedHeight(10)  # 减小标签高度
        # 应用样式，使用Qt兼容的格式
        content_label.setStyleSheet("color: #6B7280; font-size: 10px;")
        
        content_layout.addWidget(content_btn, 0, Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(content_label, 0, Qt.AlignmentFlag.AlignCenter)

        # 创建 Board 按钮组合（紧凑设计）
        board_container = QWidget()
        board_container.setFixedSize(32, 40)  # 减小尺寸使布局更紧凑
        board_layout = QVBoxLayout(board_container)
        board_layout.setSpacing(2)  # 最小间距
        board_layout.setContentsMargins(0, 0, 0, 0)
        
        board_btn = QPushButton()
        board_btn.setIcon(QIcon(get_icon_path("excalidraw")))
        board_btn.setIconSize(QSize(16, 16))  # 减小图标尺寸
        board_btn.setFixedSize(28, 28)  # 减小按钮尺寸
        board_btn.setToolTip("创建画布")
        board_btn.clicked.connect(self.create_new_board_item)
        
        # 创建紧凑的 Board 标签
        board_label = QLabel("画布")
        board_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        board_label.setFixedHeight(10)  # 减小标签高度
        # 应用样式，使用Qt兼容的格式
        board_label.setStyleSheet("color: #6B7280; font-size: 10px;")
        
        board_layout.addWidget(board_btn, 0, Qt.AlignmentFlag.AlignCenter)
        board_layout.addWidget(board_label, 0, Qt.AlignmentFlag.AlignCenter)

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

    def create_new_folder_item(self):
        """创建新的根目录文件夹"""
        from utils import time_utils
        
        timestamp = time_utils.now().strftime('%Y%m%d%H%M%S')
        folder_title = '文件夹-{}'.format(timestamp)
        
        # 创建根目录文件夹，默认使用markdown类型
        folder_id = self.markrender_manager.save_item(
            title=folder_title, 
            content='',  # 文件夹通常不需要内容
            parent_id=None,  # 根目录文件夹
            page_type='markdown',  # 默认markdown类型
            is_folder=1,  # 标记为文件夹
            icon_type='folder',  # 使用folder图标类型
            icon_path=None  # 暂时不设置自定义图标路径
        )
        
        # 重新加载数据以显示新文件夹
        self.load_quickpick_items()

    def add_node_to_tree(self, parent_index, item_id, title, is_folder=False):
        """在树中添加新节点而不进行全局刷新"""
        # 获取父项
        parent_item = self.quickpick_list.itemFromIndex(parent_index)
        if not parent_item:
            # 如果找不到父项，回退到全局刷新
            self.load_quickpick_items()
            return
        
        # 获取新创建项的详细信息
        item_data = self.markrender_manager.get_detail(item_id)
        if not item_data:
            # 如果获取不到详细信息，回退到全局刷新
            self.load_quickpick_items()
            return
        
        # 创建新的树节点
        new_item = QTreeWidgetItem(parent_item)
        new_item.setData(0, Qt.ItemDataRole.UserRole, item_data)
        new_item.setText(0, title)
        
        # 确保节点标志正确设置
        new_item.setFlags(
            Qt.ItemFlag.ItemIsSelectable | 
            Qt.ItemFlag.ItemIsEnabled | 
            Qt.ItemFlag.ItemIsEditable
        )
        
        # 更新父节点的数据，确保父节点知道自己有子节点
        parent_data = parent_item.data(0, Qt.ItemDataRole.UserRole)
        if parent_data:
            # 如果父节点原来没有children字段或者children为空，需要更新它
            if 'children' not in parent_data or not parent_data['children']:
                parent_data['children'] = []
            
            # 将新节点添加到父节点的children列表中
            parent_data['children'].append(item_data)
            
            # 更新父节点的数据
            parent_item.setData(0, Qt.ItemDataRole.UserRole, parent_data)
            
            # 确保父节点的标志位正确设置
            parent_item.setFlags(
                Qt.ItemFlag.ItemIsSelectable | 
                Qt.ItemFlag.ItemIsEnabled | 
                Qt.ItemFlag.ItemIsEditable
            )
        
        # 展开父节点以显示新添加的子节点
        parent_item.setExpanded(True)

    def create_new_child_item(self, parent_index, item_type):
        """创建新的子项"""
        from utils import time_utils
        
        # 获取父项数据
        parent_data = parent_index.data(Qt.ItemDataRole.UserRole)
        parent_id = parent_data.get('id') if parent_data else None
        
        timestamp = time_utils.now().strftime('%Y%m%d%H%M%S')
        
        if item_type == 'markdown':
            # 保存到数据库，指定父ID
            item_id = self.markrender_manager.save_item(
                title='MD-{}'.format(timestamp),
                content='',
                parent_id=parent_id,
                page_type='markdown',
                page_engine=None,
                icon_type='textarea',  # 使用textarea图标类型
                icon_path=None  # 暂时不设置自定义图标路径
            )
            # 不进行全局刷新，而是直接在树中添加新节点
            self.add_node_to_tree(parent_index, item_id, 'MD-{}'.format(timestamp), is_folder=False)
        elif item_type == 'excalidraw':
            # 保存到数据库，指定父ID
            item_id = self.markrender_manager.save_item(
                title='Board-{}'.format(timestamp),
                content='',
                parent_id=parent_id,
                page_type='excalidraw',
                page_engine='excalidraw',
                icon_type='excalidraw',  # 使用excalidraw图标类型
                icon_path=None  # 暂时不设置自定义图标路径
            )
            # 不进行全局刷新，而是直接在树中添加新节点
            self.add_node_to_tree(parent_index, item_id, 'Board-{}'.format(timestamp), is_folder=False)
        else:
            return

    def create_new_child_folder(self, parent_index):
        """创建新的子文件夹"""
        from utils import time_utils
        
        # 获取父项数据
        parent_data = parent_index.data(Qt.ItemDataRole.UserRole)
        parent_id = parent_data.get('id') if parent_data else None
        
        timestamp = time_utils.now().strftime('%Y%m%d%H%M%S')
        folder_title = '文件夹-{}'.format(timestamp)
        
        # 根据父节点的page_type设置子文件夹的page_type和图标
        page_type = 'markdown'  # 默认page_type
        icon_type = 'folder'    # 默认图标类型为文件夹
        
        if parent_data and 'page_type' in parent_data:
            parent_page_type = parent_data.get('page_type')
            if parent_page_type in ['markdown', 'excalidraw']:
                page_type = parent_page_type
                # 为不同类型的文件夹设置不同的图标
                if parent_page_type == 'markdown':
                    icon_type = 'filetype-md'  # 使用markdown文件类型图标
                elif parent_page_type == 'excalidraw':
                    icon_type = 'excalidraw'  # 使用excalidraw图标
            else:
                page_type = 'markdown'  # 其他情况默认为markdown
        
        # 创建文件夹
        folder_id = self.markrender_manager.save_item(
            title=folder_title, 
            content='',  # 文件夹通常不需要内容
            parent_id=parent_id,
            page_type=page_type,  # 根据父节点设置page_type
            is_folder=1,  # 标记为文件夹
            icon_type=icon_type,  # 根据page_type设置图标类型
            icon_path=None  # 暂时不设置自定义图标路径
        )
        
        # 不进行全局刷新，而是直接在树中添加新节点
        self.add_node_to_tree(parent_index, folder_id, folder_title, is_folder=True)

    def find_and_update_item_in_tree(self, item_id, updated_data):
        """在树中查找并更新特定节点的数据"""
        def find_item_recursive(parent_item):
            """递归查找节点"""
            if parent_item is None:
                # 搜索顶层节点
                for i in range(self.quickpick_list.topLevelItemCount()):
                    item = self.quickpick_list.topLevelItem(i)
                    if item:
                        data = item.data(0, Qt.ItemDataRole.UserRole)
                        if data and data.get('id') == item_id:
                            return item
                        # 递归搜索子节点
                        found = find_item_recursive(item)
                        if found:
                            return found
            else:
                # 搜索子节点
                for i in range(parent_item.childCount()):
                    item = parent_item.child(i)
                    if item:
                        data = item.data(0, Qt.ItemDataRole.UserRole)
                        if data and data.get('id') == item_id:
                            return item
                        # 递归搜索子节点的子节点
                        found = find_item_recursive(item)
                        if found:
                            return found
            return None
        
        # 查找并更新树节点
        tree_item = find_item_recursive(None)
        if tree_item:
            # 更新节点数据
            tree_item.setData(0, Qt.ItemDataRole.UserRole, updated_data)
            tree_item.setText(0, updated_data.get('title', ''))
            
            # 确保节点标志正确设置
            tree_item.setFlags(
                Qt.ItemFlag.ItemIsSelectable | 
                Qt.ItemFlag.ItemIsEnabled | 
                Qt.ItemFlag.ItemIsEditable
            )
            
            # 同时更新内部数据结构 all_quickpick_items
            def update_internal_data(items):
                """递归更新内部数据结构"""
                for item in items:
                    if item.get('id') == item_id:
                        # 更新匹配项的所有字段
                        for key, value in updated_data.items():
                            item[key] = value
                        return True
                    # 递归更新子节点
                    if 'children' in item and item['children']:
                        if update_internal_data(item['children']):
                            return True
                return False
            
            # 更新内部数据结构
            update_internal_data(self.all_quickpick_items)
            
            return True
        return False

    def show_tree_context_menu(self, position):
        """显示树形控件的上下文菜单"""
        # 获取右键点击的项
        item = self.quickpick_list.itemAt(position)
        if not item:
            return
            
        # 创建菜单并应用统一的样式
        menu = QMenu(self)
        
        # 导入样式工具并应用统一的菜单样式
        from app.preference.style_utils import create_menu_style
        menu.setStyleSheet(create_menu_style())
        
        # 获取项数据
        item_data = item.data(0, Qt.ItemDataRole.UserRole)
        is_folder = item_data.get('is_folder', 0) if item_data else 0
        
        # 添加"添加子项"菜单项（所有节点都支持添加子项）
        add_submenu = menu.addMenu("添加子项")
        # 为子菜单也应用相同的样式
        add_submenu.setStyleSheet(create_menu_style())
        
        # 添加 Markdown 文件
        add_markdown_action = QAction("Markdown 文件", self)
        add_markdown_action.triggered.connect(lambda: self.create_new_child_item(self.quickpick_list.indexFromItem(item), 'markdown'))
        add_submenu.addAction(add_markdown_action)
        
        # 添加 Excalidraw 文件
        add_excalidraw_action = QAction("Excalidraw 文件", self)
        add_excalidraw_action.triggered.connect(lambda: self.create_new_child_item(self.quickpick_list.indexFromItem(item), 'excalidraw'))
        add_submenu.addAction(add_excalidraw_action)
        
        menu.addSeparator()
        
        # 添加编辑和删除操作
        edit_action = QAction("编辑", self)
        edit_action.triggered.connect(lambda: self.edit_item(self.quickpick_list.indexFromItem(item)))
        menu.addAction(edit_action)
        
        delete_action = QAction("删除", self)
        delete_action.triggered.connect(lambda: self.delete_selected_file())
        menu.addAction(delete_action)
        
        # 显示菜单
        menu.exec(self.quickpick_list.viewport().mapToGlobal(position))

    def select_quickpick_item(self, current_item):
        """根据文件路径选择快速选择项"""
        if not current_item or 'id' not in current_item:
            logger.warning("传入的 current_item 为空或缺少 id 字段")
            return
        for i in range(self.quickpick_list.topLevelItemCount()):
            item = self.quickpick_list.topLevelItem(i)
            if item:
                data = item.data(0, Qt.ItemDataRole.UserRole)
                if data and data.get('id') == current_item['id']:
                    self.quickpick_list.setCurrentItem(item)
                    break
