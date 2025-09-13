# -*- coding: utf-8 -*-
import sys
import os
import traceback

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QMessageBox)
from PySide6.QtWidgets import QSplitter

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
        self.setWindowFlags(Qt.FramelessWindowHint)  # 设置无边框窗口
        self.setWindowTitle("MarkRender")
        self.showMaximized()  # 恢复启动最大化
        self.setup_ui()
        self.current_item = None
        self.backend_interface = None
        # 设置基础样式表
        self.setStyleSheet(AppStyle().get_main_style())

    def showEvent(self, event):
        """窗口显示时根据窗口状态设置样式"""
        super().showEvent(event)
        if not self.isMaximized():
            self.setStyleSheet(AppStyle().get_main_style())
        else:
            self.setStyleSheet(AppStyle().get_main_style_color())

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
        # 调用 showEvent 更新样式
        self.showEvent(None)

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

        # 将顶部组件添加到主窗口
        central_widget = QWidget()
        # 为中央部件添加圆角样式和统一背景色
        central_widget.setStyleSheet(AppStyle().get_central_widget())
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        # 初始化quickpick面板
        self.markrender_manager = MarkRenderManager(db_path)
        self.quickpick_panel = QuickPickPanel(self.markrender_manager, self)
        self.sidebar_manager = SidebarManager(parent=self)
        # 初始化  编辑器
        self.editor = MarkRenderEditor(parent=self)
        self.sidebar = SidebarManager(parent=self)

        # 创建自定义标题栏
        title_bar = QWidget()
        title_bar.setFixedHeight(30)  # 固定标题栏高度
        title_bar.setStyleSheet(AppStyle().get_title_bar())
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(10, 5, 10, 5)  # 调整上下边距


        # 添加最小化、最大化、关闭按钮
        self.minimize_btn = MacOSButton("minimize", self)
        self.maximize_btn = MacOSButton("maximize", self)
        self.close_btn =  MacOSButton("close", self)

        self.minimize_btn.clicked.connect(self.showMinimized)
        self.maximize_btn.clicked.connect(self.toggle_maximize)
        self.close_btn.clicked.connect(self.close)

        # 将按钮添加到标题栏左侧
        title_bar_layout.addWidget(self.close_btn)
        title_bar_layout.addWidget(self.minimize_btn)
        title_bar_layout.addWidget(self.maximize_btn)
        title_bar_layout.addStretch()

        # 添加按钮控制区域
        self.button_controller = ButtonController(self, self.quickpick_panel, self.editor)
        self.button_controller.setFixedHeight(20)  # 固定按钮区域高度
        title_bar_layout.addWidget(self.button_controller)

        # 添加边框容器
        border_frame = QFrame()
        border_frame.setFixedHeight(1)
        border_frame.setFixedWidth(59)  # 最终精准调整：8+42+9=59px
        border_frame.setStyleSheet("background-color: {};".format(AppStyle().get_line_color()))
        self.main_layout.addWidget(border_frame)

        self.main_layout.addWidget(title_bar)

        # 修改为创建主分割器，使用 PySide6 原生的 QSplitter
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.setStyleSheet(AppStyle().get_main_splitter())
        # 创建右侧内容分割器，同样使用 QSplitter
        right_splitter = QSplitter(Qt.Horizontal)
        # 设置分割器样式，统一边距和圆角
        right_splitter.setStyleSheet(AppStyle().get_right_splitter())
        # 隐藏分割条并禁用拖拽功能
        right_splitter.setHandleWidth(0)

        right_splitter.addWidget(self.quickpick_panel)
        right_splitter.addWidget(self.editor)
        initial_right_sizes = [int(self.width() * 0.2), int(self.width() * 0.8)]
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

        # 设置状态栏
        self.status_bar = StatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.setStyleSheet(AppStyle().get_status_bar())
        
        # 移除默认的Landing欢迎页面显示
        # 改为加载最后更新的项目
        from PySide6.QtCore import QTimer
        # 延迟显示，确保所有组件初始化完成
        QTimer.singleShot(100, self.load_last_updated_item)

    def update_theme(self, theme):
        """切换主题"""
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
            # 根据页面类型路由到不同的处理逻辑
            if page_type == "markdown":
                self._handle_page(quickpick_item)
            elif page_type == "excalidraw":
                self._handle_page(quickpick_item)
            # 更新状态栏
            content = self.markrender_manager.get_detail(quickpick_item.get('id', ''))['content']
            self.status_bar.update_file_size(len(content))
            self.status_bar.update_word_count(len(content))
            logger.info(f"页面更新完成: {quickpick_item.get('title', 'Unknown')}")
        except Exception as e:
            logger.error(f"更新编辑区和预览区失败: {e}", exc_info=True)
    
    def _handle_page(self, quickpick_item):
        """处理页面"""
        logger.debug(f"处理页面: {quickpick_item.get('title')}")
        
        try:
            # 使用Markdown页面类型
            page_type = quickpick_item.get('page_type')
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
                        content = item_detail.get('content')
                        logger.info(f"从数据库获取到最新内容，长度: {len(content)}")
                    else:
                        logger.info(f"数据库中未找到内容，使用空内容初始化")
                except Exception as e:
                    logger.error(f"从数据库获取内容失败: {e}")
                # 更新Markdown编辑器内容（但不重新创建页面）
                self.editor.set_current_item(item_id, page_type, content)                
                # 确保Markdown编辑器可见
                self.editor.show()
                
                logger.debug(f"页面内容更新完成: {quickpick_item.get('title')}")
                
            else:
                logger.error(f"创建页面失败: {page_type}")
                QMessageBox.warning(self, "页面创建失败", f"无法创建{page_type}页面，请稍后再试。")
                
        except Exception as e:
            logger.error(f"页面处理失败: {e}", exc_info=True)
            QMessageBox.warning(self, "页面处理失败", f"处理{page_type}页面时发生错误: {str(e)}")
        
        logger.debug(f"页面处理完成")
    
    
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
            # 快速检查编辑器状态
            if self.editor:
                logger.debug("主窗口关闭: 检查编辑器状态")
                # 直接调用编辑器的保存方法，不再通过事件传递
                if not self.editor._close_ready:
                    logger.debug("执行编辑器保存操作")
                    self.editor._perform_save_on_close()  
                    # 标记编辑器已准备好关闭
                    self.editor._close_ready = True
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

    # 移除on_editor_close_ready方法，不再需要这个回调
    
    # 实现窗口拖动功能
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'drag_start_position'):
            if event.buttons() & Qt.LeftButton:
                self.move(event.globalPosition().toPoint() - self.drag_start_position)
                event.accept()

    # 添加双击事件处理方法
    def mouseDoubleClickEvent(self, event):
        # 当双击主窗口时切换最大化状态
        self.toggle_maximize()
        event.accept()

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
        from PySide6.QtWidgets import QMessageBox
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(f"应用遇到致命错误: {str(e)}")
        msg_box.setDetailedText(error_msg)
        msg_box.setWindowTitle("错误")
        msg_box.exec()
        sys.exit(1)
