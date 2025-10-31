# -*- coding: utf-8 -*-
import sys
import os
import traceback

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QMessageBox, 
                              QToolBar, QSizePolicy)  # 添加QToolBar和QSizePolicy导入
from PySide6.QtWidgets import QSplitter, QDialog  # 添加QDialog导入
from PySide6.QtGui import QFont, QAction, QIcon  # 添加QIcon导入
from PySide6.QtWidgets import QToolButton

from app.editor import MarkRenderEditor
from app.statusbar import StatusBar
from app.quickpick import QuickPickPanel
from app.sidebar import SidebarManager
from app.editor.backend_interface import BackendInterface

from db.markrender_manager import MarkRenderManager

from app.topbar import ButtonController
from app.preference import MacOSButton, AppStyle  # 新增导入
from utils.logger_utils import logger

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 移除无边框窗口设置，使用系统原生窗口
        self.setWindowTitle("MarkRender")
        # 设置窗口初始大小，但不固定
        self.resize(1200, 800)
        self.setup_ui()
        self.current_item = None
        self.backend_interface = None
        # 设置基础样式表
        self.setStyleSheet(AppStyle().get_main_style())

    def setup_ui(self):
        """设置UI界面"""
        # 初始化数据库路径，使用用户数据路径
        from db.db_manager import get_user_data_dir
        user_data_dir = get_user_data_dir()
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

        # 初始化quickpick面板
        self.markrender_manager = MarkRenderManager(db_path)
        self.quickpick_panel = QuickPickPanel(self.markrender_manager, self)
        # 初始化编辑器
        self.editor = MarkRenderEditor(parent=self)
        self.sidebar = SidebarManager(parent=self)

        # 移除toolbar，quickpick按钮功能已经在侧边栏中实现
        # 创建按钮控制器但不添加到任何工具栏
        self.button_controller = ButtonController(self, self.quickpick_panel, self.editor)

        # 创建中央部件和主布局
        central_widget = QWidget()
        # 为中央部件添加统一背景色
        central_widget.setStyleSheet(AppStyle().get_central_widget())
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 修改为创建主分割器，使用 PySide6 原生的 QSplitter
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.setStyleSheet(AppStyle().get_main_splitter())
        # 创建右侧内容分割器，同样使用 QSplitter
        right_splitter = QSplitter(Qt.Orientation.Horizontal)
        # 设置分割器样式，统一边距和圆角
        right_splitter.setStyleSheet(AppStyle().get_right_splitter())
        # 恢复设置，隐藏分割条并禁用拖拽功能
        right_splitter.setHandleWidth(1)  # 设置分割条宽度为1像素

        # 创建历史记录面板
        from app.history.history_panel import HistoryPanel
        self.history_panel = HistoryPanel()
        self.history_panel.set_history_manager(self.markrender_manager)
        self.history_panel.hide()  # 默认隐藏

        right_splitter.addWidget(self.quickpick_panel)
        right_splitter.addWidget(self.editor)
        right_splitter.addWidget(self.history_panel)
        # 设置历史面板占比1/4的初始大小比例
        initial_right_sizes = [int(self.width() * 0.2), int(self.width() * 0.55), int(self.width() * 0.25)]
        right_splitter.setSizes(initial_right_sizes)

        # 将侧边栏和右侧内容添加到主分割器，侧边栏放在左侧
        main_splitter.addWidget(self.sidebar)
        main_splitter.addWidget(right_splitter)

        # 设置sidebar宽度为52，适配对称边距配置（7+36+2边框+7=52px）
        main_splitter.setSizes([59, int(self.width() - 59)])
        self.sidebar.setFixedWidth(59)

        # 修改为使用 self.main_layout 添加组件
        self.main_layout.addWidget(main_splitter)

        self.setCentralWidget(central_widget)

        # 连接历史列表项选中信号
        self.quickpick_panel.quickpick_item_selected.connect(
            self.update_editor_and_previewer)

        # 连接历史面板选择信号
        self.history_panel.history_selected.connect(
            self.on_history_selected)

        # 设置状态栏，并传递主窗口引用
        self.status_bar = StatusBar(self)
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet(AppStyle().get_status_bar())
        
        # 移除默认的Landing欢迎页面显示
        # 改为加载最后更新的项目
        # 延迟显示，确保所有组件初始化完成
        QTimer.singleShot(100, self.load_last_updated_item)

    def update_theme(self, theme):
        """切换主题"""
        # 检查编辑器是否有update_theme方法
        if hasattr(self.editor, 'update_theme'):
            self.editor.update_theme(theme)

    def load_last_updated_item(self):
        """加载最后更新的项目"""
        try:
            # 从数据库加载项目，按更新时间排序
            items = self.markrender_manager.load_items(limit=1)
            if items:
                # 获取最后更新的项目
                last_updated_item = items[0]
                logger.info(f"加载最后更新的项目: {last_updated_item.get('title', 'Unknown')}")
                # 更新编辑器和预览器
                self.update_editor_and_previewer(last_updated_item)
                # 在quickpick面板中选中该项目
                self.quickpick_panel.select_quickpick_item(last_updated_item)
            else:
                logger.info("没有找到任何项目，保持空状态")
        except Exception as e:
            logger.error(f"加载最后更新的项目失败: {e}", exc_info=True)

    def update_editor_and_previewer(self, quickpick_item):
        """更新编辑区和预览区内容，支持多页面类型路由"""
        try:            
            logger.info(f"开始更新编辑器页面: {quickpick_item.get('title', 'Unknown')}")
            # 没有修改或没有当前项，直接切换
            self._continue_update_editor_and_previewer(quickpick_item)
        except Exception as e:
            logger.error(f"更新编辑区和预览区失败: {e}", exc_info=True)
    
    def _continue_update_editor_and_previewer(self, quickpick_item):
        """继续执行更新编辑区和预览区内容的逻辑"""
        try:            
            logger.info(f"继续更新编辑器页面: {quickpick_item.get('title', 'Unknown')}")
            self.current_item = quickpick_item
            # 获取页面类型，默认为markdown
            page_type = quickpick_item.get('page_type', 'markdown')
            logger.info(f"页面类型: {page_type}")
            
            # 获取页面类型，默认为markdown
            page_type = quickpick_item.get('page_type', 'markdown')
            logger.info(f"页面类型: {page_type}")
            # 根据页面类型路由到不同的处理逻辑
            if page_type == "markdown":
                self._handle_page(quickpick_item)
            elif page_type == "excalidraw":
                self._handle_page(quickpick_item)
            
            # 在处理完页面后再加载历史记录，避免干扰编辑器显示
            # 加载历史记录
            item_id = quickpick_item.get('id')
            if item_id and hasattr(self, 'history_panel'):
                self.history_panel.load_history(item_id)
            
            # 更新状态栏的标签显示
            item_detail = self.markrender_manager.get_detail(quickpick_item.get('id', ''))
            tags = item_detail.get('tags', '') if item_detail else ''
            self.status_bar.update_tags(tags)
            logger.info(f"页面更新完成: {quickpick_item.get('title', 'Unknown')}")
        except Exception as e:
            logger.error(f"更新编辑区和预览区失败: {e}", exc_info=True)
    
    def _handle_page(self, quickpick_item):
        """处理页面"""
        logger.debug(f"处理页面: {quickpick_item.get('title')}")
        
        try:
            # 使用Markdown页面类型
            page_type = quickpick_item.get('page_type', 'markdown')
            page_manager = self.editor.page_manager
            # 获取或创建markdown页面
            markdown_view = page_manager.get_or_create_page(
                page_type=page_type,
                backend_interface=self.editor.backend_interface
            )
            
            # 确保 BackendInterface 和页面对象正确关联
            if markdown_view:
                self.editor.backend_interface.set_page(markdown_view.page())
                # 切换到Markdown页面， Switch后需要重新设置页面内容，否则页面会被reset后显示空
                page_manager.switch_to_page(page_type)
                # 获取内容 - 对于不同的item，必须从对应的item获取内容
                item_id = quickpick_item.get('id')
                content = ''
                try:
                    item_detail = self.markrender_manager.get_detail(item_id)
                    if item_detail and item_detail.get('content'):
                        content = item_detail.get('content', '')
                        logger.info(f"从数据库获取到最新内容，长度: {len(content)}")
                    else:
                        logger.info(f"数据库中未找到内容，使用空内容初始化")
                except Exception as e:
                    logger.error(f"从数据库获取内容失败: {e}")
                # 更新Markdown编辑器内容（但不重新创建页面）
                self.editor.set_current_item(item_id, page_type, content)                
                # 确保Markdown编辑器可见
                self.editor.show()
                
                # 确保内容被正确设置到编辑器中
                # 在页面切换后延迟设置内容，确保页面已完全加载
                QTimer.singleShot(100, lambda: self.editor.set_text_content(content))
                
                logger.debug(f"页面内容更新完成: {quickpick_item.get('title')}")
                
            else:
                logger.error(f"创建页面失败: {page_type}")
                QMessageBox.warning(self, "页面创建失败", f"无法创建{page_type}页面，请稍后再试。")
                
        except Exception as e:
            page_type = quickpick_item.get('page_type', 'markdown')
            logger.error(f"页面处理失败: {e}", exc_info=True)
            QMessageBox.warning(self, "页面处理失败", f"处理{page_type}页面时发生错误: {str(e)}")
        
        logger.debug(f"页面处理完成")
    
    def on_history_selected(self, history_record):
        """当用户选择历史记录时的处理"""
        try:
            logger.info(f"选择了历史记录: {getattr(history_record, 'change_type', '')}")
            
            # 根据变更类型获取历史内容和字段变更信息
            change_type = getattr(history_record, 'change_type', '')
            history_content = None
            field_changes = {}  # 字段变更信息
            
            # 对于不同类型的变更，获取相应的内容和字段变更信息
            if change_type in ['content_create', 'content_update']:
                # 内容变更，使用new_content字段
                history_content = getattr(history_record, 'new_content', '')
            elif change_type == 'title_update':
                # 标题变更，使用new_title字段
                history_content = getattr(history_record, 'new_title', '')
                # 添加字段变更信息
                old_title = getattr(history_record, 'old_title', '')
                new_title = getattr(history_record, 'new_title', '')
                if old_title != new_title:
                    field_changes['title'] = {'old': old_title, 'new': new_title}
            elif change_type == 'display_name_update':
                # 显示名称变更，使用new_display_name字段
                history_content = getattr(history_record, 'new_display_name', '')
                # 添加字段变更信息
                old_display_name = getattr(history_record, 'old_display_name', '')
                new_display_name = getattr(history_record, 'new_display_name', '')
                if old_display_name != new_display_name:
                    field_changes['display_name'] = {'old': old_display_name, 'new': new_display_name}
            elif change_type == 'icon_update':
                # 图标变更，这里可能需要特殊处理
                # 暂时使用new_content字段（文档内容）
                history_content = getattr(history_record, 'new_content', '')
                # 添加字段变更信息
                old_icon_type = getattr(history_record, 'old_icon_type', '')
                new_icon_type = getattr(history_record, 'new_icon_type', '')
                if old_icon_type != new_icon_type:
                    field_changes['icon_type'] = {'old': old_icon_type, 'new': new_icon_type}
                
                old_icon_path = getattr(history_record, 'old_icon_path', '')
                new_icon_path = getattr(history_record, 'new_icon_path', '')
                if old_icon_path != new_icon_path:
                    field_changes['icon_path'] = {'old': old_icon_path, 'new': new_icon_path}
                
                old_icon_color = getattr(history_record, 'old_icon_color', '')
                new_icon_color = getattr(history_record, 'new_icon_color', '')
                if old_icon_color != new_icon_color:
                    field_changes['icon_color'] = {'old': old_icon_color, 'new': new_icon_color}
            else:
                # 其他类型的变更，尝试使用new_content字段
                history_content = getattr(history_record, 'new_content', '')
            
            if history_content is not None and self.current_item:
                # 获取当前版本内容
                current_item_id = self.current_item.get('id', '')
                current_record = self.markrender_manager.get_detail(current_item_id)
                
                # 根据变更类型获取当前内容
                current_content = None
                if change_type in ['content_create', 'content_update']:
                    # 内容变更，使用文档内容
                    current_content = current_record.get('content', '') if current_record else ''
                elif change_type == 'title_update':
                    # 标题变更，使用当前标题
                    current_content = current_record.get('title', '') if current_record else ''
                elif change_type == 'display_name_update':
                    # 显示名称变更，使用当前显示名称
                    current_content = current_record.get('display_name', '') if current_record else ''
                elif change_type == 'icon_update':
                    # 图标变更，这里可能需要特殊处理
                    # 暂时使用文档内容
                    current_content = current_record.get('content', '') if current_record else ''
                else:
                    # 其他类型的变更，使用文档内容
                    current_content = current_record.get('content', '') if current_record else ''
                
                # 显示差异对比对话框，传递字段变更信息
                from app.history.history_diff_dialog import HistoryDiffDialog
                from PySide6.QtWidgets import QDialog
                dialog = HistoryDiffDialog(current_content, history_content, change_type, field_changes, self)
                result = dialog.exec()
                
                # 如果用户选择使用历史版本
                if result == QDialog.Accepted:
                    # 在应用历史版本之前，先将当前编辑区的内容保存为一个新的历史版本
                    self._save_current_content_as_history(current_item_id)
                    
                    # 根据变更类型应用不同的更新逻辑
                    if change_type in ['content_create', 'content_update']:
                        # 内容变更，更新编辑器内容
                        self.editor.set_current_item(
                            current_item_id,
                            self.current_item.get('page_type', 'markdown'),
                            history_content
                        )
                        # 更新编辑器显示
                        self.editor.set_text_content(history_content)
                    elif change_type == 'title_update':
                        # 标题变更，更新标题
                        self.markrender_manager.update_title(current_item_id, history_content)
                        # 更新当前项的标题
                        if self.current_item:
                            self.current_item['title'] = history_content
                        # 更新快速选择面板
                        self.update_quickpick_list()
                    elif change_type == 'display_name_update':
                        # 显示名称变更，更新显示名称
                        self.markrender_manager.update_display_name(current_item_id, history_content)
                        # 更新当前项的显示名称
                        if self.current_item:
                            self.current_item['display_name'] = history_content
                        # 更新快速选择面板
                        self.update_quickpick_list()
                    
                    # 应用完历史版本后刷新历史列表
                    self._refresh_history_list(current_item_id)
        except Exception as e:
            logger.error(f"处理历史记录选择失败: {e}")
    
    def _save_current_content_as_history(self, item_id):
        """将当前编辑区的内容保存为一个新的历史版本"""
        try:
            logger.info(f"保存当前编辑区内容为历史版本: {item_id}")
            
            # 获取当前编辑器的内容
            if hasattr(self, 'editor') and self.editor and hasattr(self.editor, 'item') and self.editor.item.item_id:
                result = self.editor.backend_interface.send_message_sync("getContent", {}, item_id=self.editor.item.item_id, timeout=10000)
                if result and result.get('success', False): 
                    content = result.get('content', '') if result else ''
                    
                    # 获取当前记录的详细信息
                    current_record = self.markrender_manager.get_detail(item_id)
                    if current_record:
                        # 检查内容是否发生变化
                        old_content = current_record.get('content', '') if current_record else ''
                        
                        # 只有当内容真正发生变化时才保存历史记录
                        if content != old_content:
                            logger.info(f"内容发生变化，保存新的历史记录")
                            
                            # 保存项目，这会自动创建历史记录
                            self.markrender_manager.save_item(
                                id=item_id,
                                content=content,
                                title=current_record.get('title', ''),
                                tags=current_record.get('tags', ''),
                                render_style=current_record.get('render_style', ''),
                                file_path=current_record.get('file_path', ''),
                                converter=current_record.get('converter', ''),
                                theme_id=current_record.get('theme_id', 0),
                                status=current_record.get('status', ''),
                                page_type=current_record.get('page_type', ''),
                                page_settings=current_record.get('page_settings', ''),
                                page_engine=current_record.get('page_engine', ''),
                                # 树形结构字段
                                parent_id=current_record.get('parent_id', None),
                                order=current_record.get('order', 0),
                                level=current_record.get('level', 0),
                                is_folder=current_record.get('is_folder', 0),
                                # 图标和显示字段
                                icon_type=current_record.get('icon_type', None),
                                icon_path=current_record.get('icon_path', None),
                                icon_color=current_record.get('icon_color', None),
                                display_name=current_record.get('display_name', None),
                            )
                            logger.info(f"新的历史记录已保存: {item_id}")
                        else:
                            logger.info(f"内容未发生变化，跳过保存历史记录: {item_id}")
                else:
                    logger.warning(f"获取编辑器内容失败，使用空内容")
                    # 即使获取内容失败，也要尝试保存（可能是空内容）
                    current_record = self.markrender_manager.get_detail(item_id)
                    if current_record:
                        content = ""
                        old_content = current_record.get('content', '') if current_record else ''
                        
                        # 只有当内容真正发生变化时才保存历史记录
                        if content != old_content:
                            self.markrender_manager.save_item(
                                id=item_id,
                                content=content,
                                title=current_record.get('title', ''),
                                tags=current_record.get('tags', ''),
                                render_style=current_record.get('render_style', ''),
                                file_path=current_record.get('file_path', ''),
                                converter=current_record.get('converter', ''),
                                theme_id=current_record.get('theme_id', 0),
                                status=current_record.get('status', ''),
                                page_type=current_record.get('page_type', ''),
                                page_settings=current_record.get('page_settings', ''),
                                page_engine=current_record.get('page_engine', ''),
                                # 树形结构字段
                                parent_id=current_record.get('parent_id', None),
                                order=current_record.get('order', 0),
                                level=current_record.get('level', 0),
                                is_folder=current_record.get('is_folder', 0),
                                # 图标和显示字段
                                icon_type=current_record.get('icon_type', None),
                                icon_path=current_record.get('icon_path', None),
                                icon_color=current_record.get('icon_color', None),
                                display_name=current_record.get('display_name', None),
                            )
                            logger.info(f"新的历史记录已保存（空内容）: {item_id}")
                        else:
                            logger.info(f"内容未发生变化，跳过保存历史记录: {item_id}")
        except Exception as e:
            logger.error(f"保存当前内容为历史版本时出错: {e}")
    
    def _refresh_history_list(self, item_id):
        """刷新历史列表"""
        try:
            logger.info(f"刷新历史列表: {item_id}")
            if hasattr(self, 'history_panel') and self.history_panel:
                self.history_panel.load_history(item_id)
                logger.info(f"历史列表已刷新: {item_id}")
        except Exception as e:
            logger.error(f"刷新历史列表时出错: {e}")

    def update_quickpick_list(self):
        """更新快速选择列表"""
        self.quickpick_panel.load_quickpick_items()
        if self.current_item:
            self.quickpick_panel.select_quickpick_item(self.current_item)
    
    def on_editor_close_ready(self):
        """当编辑器准备好关闭时的处理"""
        logger.info("接收到编辑器关闭准备信号，开始关闭主窗口")
        # 由主窗口统一控制关闭流程，确保原子性
        self.close()

    def closeEvent(self, event):
        """在窗口关闭前保存未保存的笔记并清理线程"""
        try:
            # 先最小化窗口
            self.showMinimized()
            
            # 保存当前操作的item数据
            if self.editor and hasattr(self.editor, 'item') and self.editor.item:
                logger.debug("主窗口关闭: 保存当前编辑器内容")
                self._perform_save_on_close()
            
            logger.debug("主窗口正常关闭")
            # 所有准备工作完成，接受关闭事件
            event.accept()
            
        except Exception as e:
            import traceback
            logger.error(f"主窗口关闭时出错: {e} {traceback.format_exc()}")
            # 出错时也接受关闭事件，避免无法退出
            event.accept()
            
        # 调用父类的关闭事件处理
        super().closeEvent(event)

    def _perform_save_on_close(self):
        """在关闭时执行保存操作，不涉及事件处理"""
        try:
            # 退出前同步拉取数据并保存
            if hasattr(self, 'editor') and self.editor and hasattr(self.editor, 'item') and self.editor.item.item_id:
                result = self.editor.backend_interface.send_message_sync("getContent", {}, item_id=self.editor.item.item_id, timeout=10000)
                if result and result.get('success', False): 
                    content = result.get('content', '') if result else ''
                    item_id = self.editor.item.item_id
                    
                    # 在保存前检查内容是否发生变化
                    old_record = self.markrender_manager.get_detail(item_id)
                    old_content = old_record.get('content', '') if old_record else ''
                    
                    # 只有当内容真正发生变化时才保存
                    if content != old_content:
                        self.markrender_manager.save_item(id=item_id, content=content)
                        logger.debug(f"文档已保存: {item_id}")
                    else:
                        logger.debug(f"内容未发生变化，跳过保存: {item_id}")
                else:
                    # 即使获取内容失败，也要尝试保存（可能是空内容）
                    item_id = self.editor.item.item_id
                    content = ""
                    
                    # 在保存前检查内容是否发生变化
                    old_record = self.markrender_manager.get_detail(item_id)
                    old_content = old_record.get('content', '') if old_record else ''
                    
                    # 只有当内容真正发生变化时才保存
                    if content != old_content:
                        self.markrender_manager.save_item(id=item_id, content=content)
                        logger.debug(f"文档已保存（空内容）: {item_id}")
                    else:
                        logger.debug(f"内容未发生变化，跳过保存: {item_id}")
            self.editor._close_ready = True
        except Exception as e:
            logger.error(f"发送getContent消息时出错: {e}")
            self.editor._close_ready = True

    # 移除自定义的窗口拖动功能，使用系统原生的窗口管理
    # 移除双击事件处理，使用系统原生的最大化/还原功能

    def handle_close_button(self):
        """处理关闭按钮点击事件"""
        # 使用closeEvent处理关闭逻辑，不再单独实现
        self.close()

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
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setText(f"应用遇到致命错误: {str(e)}")
        msg_box.setDetailedText(error_msg)
        msg_box.setWindowTitle("错误")
        msg_box.exec()
        sys.exit(1)