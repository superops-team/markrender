# -*- coding: utf-8 -*-

"""
主程序入口
"""

import sys
import os
import traceback

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QMessageBox, 
                              QToolBar, QSizePolicy, QSplitter, QDialog)
from PySide6.QtGui import QFont, QAction, QIcon
from PySide6.QtWidgets import QToolButton

from app.editor import MarkRenderEditor
from app.editor.tab_manager import TabManager  # 添加标签页管理器导入
from app.statusbar import StatusBar
from app.sidebar.sidebar_manager import SidebarManager
from app.quickpick.panel import QuickPickPanel
from app.topbar.button_controller import ButtonController
from app.preference import AppStyle
from db.markrender_manager import MarkRenderManager
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
        # 初始化标签页管理器
        self.tab_manager = TabManager(parent=self)
        self.sidebar = SidebarManager(parent=self)

        # 移除toolbar，quickpick按钮功能已经在侧边栏中实现
        # 创建按钮控制器但不添加到任何工具栏
        self.button_controller = ButtonController(self, self.quickpick_panel, self.tab_manager)

        # 创建中央部件和主布局
        central_widget = QWidget()
        # 为中央部件添加统一背景色
        central_widget.setStyleSheet(AppStyle().get_central_widget())
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 创建主分割器，使用 PySide6 原生的 QSplitter
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
        right_splitter.addWidget(self.tab_manager)  # 使用标签页管理器替代原来的编辑器
        right_splitter.addWidget(self.history_panel)
        # 设置历史面板占比1/5的初始大小比例（20%）
        initial_right_sizes = [int(self.width() * 0.2), int(self.width() * 0.6), int(self.width() * 0.2)]
        right_splitter.setSizes(initial_right_sizes)

        # 将侧边栏和右侧内容添加到主分割器，侧边栏放在左侧
        main_splitter.addWidget(self.sidebar)
        main_splitter.addWidget(right_splitter)

        # 设置sidebar宽度为59px
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
        
        # 连接状态栏的标签选择信号到quickpick面板的过滤方法
        self.status_bar.tag_selected.connect(self.quickpick_panel.filter_by_tag)
        
        # 移除默认的Landing欢迎页面显示
        # 改为加载最后更新的项目
        # 延迟显示，确保所有组件初始化完成
        QTimer.singleShot(100, self.load_last_updated_item)

    def update_theme(self, theme):
        """切换主题"""
        # 检查编辑器是否有update_theme方法
        current_editor = self.tab_manager.get_current_editor()
        if current_editor and hasattr(current_editor, 'update_theme'):
            current_editor.update_theme(theme)

    def load_last_updated_item(self):
        """加载最后更新的项目"""
        try:
            # 核心改进：直接从数据库获取最后更新的项目，而不使用load_items方法
            # 这样可以确保始终按更新时间排序，不受用户设置影响
            session = self.markrender_manager.Session()
            try:
                from db.models import MarkRenderData
                # 直接查询数据库，按更新时间降序排序，获取最新的一条记录
                last_updated_record = session.query(MarkRenderData).order_by(MarkRenderData.updated_at.desc()).first()
                
                if last_updated_record:
                    # 构建项目数据字典
                    last_updated_item = {
                        'title': getattr(last_updated_record, 'title', 'Unknown'),
                        'id': getattr(last_updated_record, 'id', 0),
                        'tags': getattr(last_updated_record, 'tags', ''),
                        'page_type': getattr(last_updated_record, 'page_type', 'markdown'),
                        'updated_at': getattr(last_updated_record, 'updated_at', None),
                        'parent_id': getattr(last_updated_record, 'parent_id', None),
                        'order': getattr(last_updated_record, 'order', 0),
                        'level': getattr(last_updated_record, 'level', 0),
                        'is_folder': getattr(last_updated_record, 'is_folder', 0)
                    }
                    logger.info(f"加载最后更新的项目: {last_updated_item.get('title', 'Unknown')}")
                    # 更新编辑器和预览器
                    self.update_editor_and_previewer(last_updated_item)
                    # 在quickpick面板中选中该项目
                    self.quickpick_panel.select_quickpick_item(last_updated_item)
                else:
                    logger.info("没有找到任何项目，保持空状态")
            except Exception as e:
                logger.error(f"直接查询数据库失败: {e}", exc_info=True)
                # 失败时回退到使用load_items方法
                items = self.markrender_manager.load_items(limit=1)
                if items:
                    last_updated_item = items[0]
                    logger.info(f"回退到使用load_items方法加载项目: {last_updated_item.get('title', 'Unknown')}")
                    self.update_editor_and_previewer(last_updated_item)
                    self.quickpick_panel.select_quickpick_item(last_updated_item)
            finally:
                session.close()
        except Exception as e:
            logger.error(f"加载最后更新的项目失败: {e}", exc_info=True)

    def update_editor_and_previewer(self, quickpick_item):
        """更新编辑区和预览区内容，支持多页面类型路由"""
        try:            
            logger.info(f"开始更新编辑器页面: {quickpick_item.get('title', 'Unknown')}")
            # 核心改进：当用户点击item时，自动取消选中的tag
            # 这确保了用户在查看不同项目时不会被之前的过滤限制
            if hasattr(self, 'status_bar') and hasattr(self.status_bar, 'selected_tag'):
                # 如果有选中的tag，清除它
                if self.status_bar.selected_tag:
                    logger.info(f"清除选中的tag: {self.status_bar.selected_tag}")
                    # 调用_on_tag_clicked方法来清除选中状态并发送信号
                    self.status_bar._on_tag_clicked(self.status_bar.selected_tag)
            # 为项目添加标签页
            self.tab_manager.add_tab_for_item(quickpick_item)
        except Exception as e:
            logger.error(f"更新编辑区和预览区失败: {e}", exc_info=True)
    
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
            
            # 获取当前编辑器并更新内容
            current_editor = self.tab_manager.get_current_editor()
            if current_editor:
                # 使用历史内容更新编辑器
                if history_content is not None:
                    current_editor.set_text_content(history_content)
                
                # 如果有字段变更信息，更新相应的UI元素
                if field_changes:
                    # 这里可以添加字段变更的UI更新逻辑
                    logger.info(f"字段变更信息: {field_changes}")
            
        except Exception as e:
            logger.error(f"处理历史记录选择失败: {e}", exc_info=True)

    def closeEvent(self, event):
        """窗口关闭事件"""
        try:
            # 保存所有标签页的内容
            self.tab_manager.save_all_tabs()
        except Exception as e:
            logger.error(f"保存标签页内容失败: {e}")
        
        # 接受关闭事件
        event.accept()

if __name__ == "__main__":
    logger.info("应用启动")
    app = QApplication(sys.argv)
    # 设置全局字体
    font = QFont("Microsoft YaHei", 9)
    app.setFont(font)
    # 创建主窗口
    window = MainWindow()
    window.show()
    logger.info("QApplication 创建完成")
    # 运行应用
    sys.exit(app.exec())