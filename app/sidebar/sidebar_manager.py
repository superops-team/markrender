from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize
from .settings_dialog import SettingsDialog
from utils import get_icon_path
from db.markdown_manager import MarkdownManager
from app.preference import AppStyle
from app.sidebar.import_dialog import ImportDialog



class SidebarManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.markdown_manager = MarkdownManager()
        self.parent = parent
        self.app_style = AppStyle()  # 添加样式实例
        self.init_ui()
        # 设置侧边栏背景色
        self.setStyleSheet('''
            QWidget {
                background-color: #fafafa;
            }
        ''')

    def init_ui(self):
        # 创建主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 创建顶部按钮组
        self.file_browse_btn = QPushButton()
        self.init_sidebar_button(
            self.file_browse_btn, 
            "home", 
            self.on_file_browse_toggled
        )
        
        self.import_btn = QPushButton()
        self.init_sidebar_button(
            self.import_btn, 
            "plus-square", 
            self.on_import_toggled
        )
        
        # 假设在类中已经保存了 HistoryPanel 实例
        if hasattr(self.parent, 'history_panel'):
            self.file_browse_btn.clicked.connect(
                lambda: self.file_browse_btn.setChecked(True))
            self.file_browse_btn.clicked.connect(
                self.parent.history_panel.load_history_items)

        self.import_btn = QPushButton()
        self.import_btn.setIcon(
            QIcon(get_icon_path("plus-square")))  # 需替换为实际图标路径
        self.import_btn.setIconSize(QSize(25, 25))
        # 应用统一样式并移除flat属性
        self.import_btn.setStyleSheet(AppStyle().get_sidebar_button_style())
        # 设置按钮可选中
        self.import_btn.setCheckable(True)
        self.import_btn.clicked.connect(self.handle_import)

        # 将顶部按钮添加到布局
        layout.addWidget(self.file_browse_btn)
        layout.addWidget(self.import_btn)

        # 添加弹性空间，使设置按钮位于底部
        layout.addSpacerItem(
            QSpacerItem(
                20,
                40,
                QSizePolicy.Minimum,
                QSizePolicy.Expanding))

        # 创建设置按钮
        self.settings_btn = QPushButton()
        self.settings_btn.setIcon(
            QIcon(get_icon_path("settings")))
        self.settings_btn.setIconSize(QSize(25, 25))
        # 应用统一样式并移除flat属性
        self.settings_btn.setStyleSheet(AppStyle().get_sidebar_button_style())
        # 设置按钮可选中
        self.settings_btn.setCheckable(True)

        # 绑定点击事件
        self.settings_btn.clicked.connect(self.show_settings_dialog)
        layout.addWidget(self.settings_btn)

        # 设置布局策略
        self.setLayout(layout)

    def handle_import(self):
        self.import_btn.setChecked(True)
        import_dialog = ImportDialog(
            self,
            self.markdown_manager,
            self.parent.history_panel if self.parent else None)
        import_dialog.exec_()

    def show_settings_dialog(self):
        """显示设置对话框"""
        self.settings_dialog = SettingsDialog(self)
        self.settings_dialog.exec()

    def init_sidebar_button(self, button: QPushButton, icon_name: str, toggle_slot):
        """初始化侧边栏按钮并设置图标切换"""
        # 设置初始图标（默认状态）
        button.setIcon(QIcon(get_icon_path(icon_name)))
        button.setIconSize(QSize(25, 25))
        button.setStyleSheet(self.app_style.get_sidebar_button_style())
        button.setCheckable(True)
        button.toggled.connect(lambda checked: toggle_slot(checked, icon_name))

    def update_button_icon(self, button: QPushButton, icon_name: str, is_selected: bool):
        """更新按钮图标（直接切换预定义SVG）"""
        button.setIcon(QIcon(get_icon_path(icon_name, selected=is_selected)))

    def on_file_browse_toggled(self, checked, icon_name="home"):
        self.update_button_icon(self.file_browse_btn, icon_name, checked)
        if checked and hasattr(self.parent, 'history_panel'):
            self.parent.history_panel.load_history_items()

    def on_import_toggled(self, checked, icon_name="plus-square"):
        self.update_button_icon(self.import_btn, icon_name, checked)
        if checked:
            self.handle_import()
