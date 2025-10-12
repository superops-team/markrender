from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt
from .settings_dialog import SettingsDialog
from utils import get_icon_path
from db.markrender_manager import MarkRenderManager
from app.preference import AppStyle
from app.sidebar.import_dialog import ImportDialog



class SidebarManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.markdown_manager = MarkRenderManager()
        self.parent = parent
        self.app_style = AppStyle()  # 添加样式实例
        self.init_ui()
        # 设置侧边栏背景色和样式
        self.setStyleSheet(self.app_style.get_sidebar())

    def init_ui(self):
        # 创建主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 9, 8)  # 最终精确调整：左8px，右9px，实现精准对齐
        layout.setSpacing(6)  # 按钮间距设置为6px符合设计规范
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # 设置水平居中对齐

        # 创建首页按钮
        self.file_browse_btn = QPushButton()
        self.init_sidebar_button(
            self.file_browse_btn,
            "home",
            self.on_file_browse_toggled
        )

        # 创建导入按钮
        self.import_btn = QPushButton()
        self.init_sidebar_button(
            self.import_btn,
            "plus-square",
            self.on_import_toggled
        )

        # 连接事件
        if hasattr(self.parent, 'quickpick_panel'):
            self.file_browse_btn.clicked.connect(
                self.parent.quickpick_panel.load_quickpick_items)

        # 将顶部按钮添加到布局，使用居中对齐
        layout.addWidget(self.file_browse_btn, 0, Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.import_btn, 0, Qt.AlignmentFlag.AlignHCenter)

        # 添加弹性空间，使设置按钮位于底部
        layout.addSpacerItem(
            QSpacerItem(
                20,
                40,
                QSizePolicy.Policy.Minimum,
                QSizePolicy.Policy.Expanding))

        # 创建设置按钮
        self.settings_btn = QPushButton()
        self.init_sidebar_button(
            self.settings_btn,
            "settings",
            lambda checked, icon_name: self.show_settings_dialog() if checked else None
        )
        layout.addWidget(self.settings_btn, 0, Qt.AlignmentFlag.AlignHCenter)

        # 设置默认选中首页按钮
        self.file_browse_btn.setChecked(True)

    def handle_import(self):
        self.import_btn.setChecked(True)
        import_dialog = ImportDialog(
            self,
            self.markdown_manager,
            self.parent.quickpick_panel if self.parent else None)
        import_dialog.exec_()

    def show_settings_dialog(self):
        """显示设置对话框"""
        self.settings_dialog = SettingsDialog(self)
        self.settings_dialog.exec()

    def init_sidebar_button(self, button: QPushButton, icon_name: str, toggle_slot):
        """初始化侧边栏按钮并设置图标"""
        # 统一使用普通状态的图标，通过CSS控制颜色
        button.setIcon(QIcon(get_icon_path(icon_name, selected=False)))
        button.setIconSize(QSize(20, 20))  # 调整图标尺寸为20x20px
        button.setFixedSize(36, 36)  # 调整按钮尺寸为36x36px符合规范
        button.setStyleSheet(self.app_style.get_sidebar_button_style())
        button.setCheckable(True)
        # 使用lambda包装，确保只传递checked参数给toggle_slot
        button.toggled.connect(lambda checked: self.on_button_toggled(button, checked, icon_name, toggle_slot))

    def on_button_toggled(self, button, checked, icon_name, toggle_slot):
        """统一处理按钮切换事件"""
        if checked:
            # 取消其他按钮的选中状态
            if button != self.file_browse_btn:
                self.file_browse_btn.setChecked(False)
            if button != self.import_btn:
                self.import_btn.setChecked(False)
            if button != self.settings_btn:
                self.settings_btn.setChecked(False)
            
            # 更新图标为选中状态
            button.setIcon(QIcon(get_icon_path(icon_name, selected=True)))
        else:
            # 更新图标为非选中状态
            button.setIcon(QIcon(get_icon_path(icon_name, selected=False)))
        
        # 调用具体的处理函数
        toggle_slot(checked, icon_name)

    def on_file_browse_toggled(self, checked, icon_name="home"):
        """处理首页按钮切换"""
        if checked:
            if hasattr(self.parent, 'quickpick_panel'):
                self.parent.quickpick_panel.load_quickpick_items()

    def on_import_toggled(self, checked, icon_name="plus-square"):
        """处理导入按钮切换"""
        if checked:
            self.handle_import()