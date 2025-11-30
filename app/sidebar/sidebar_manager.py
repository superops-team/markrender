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
        # 初始化按钮组
        self.button_group = []
        self.init_ui()
        # 设置侧边栏背景色和样式
        self.setStyleSheet(self.app_style.get_sidebar())

    def init_ui(self):
        # 创建主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)  # 进一步减小内边距使布局更紧凑
        layout.setSpacing(4)  # 进一步减小间距使按钮布局更密集
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # 设置水平居中对齐

        # 创建展开折叠quickpick的按钮
        self.toggle_quickpick_btn = QPushButton()
        self.init_sidebar_button(
            self.toggle_quickpick_btn,
            "sidebar",
            self.on_toggle_quickpick_toggled
        )
        # 初始为选中状态（显示quickpick面板）
        self.toggle_quickpick_btn.setChecked(True)

        # 将顶部按钮添加到布局，使用居中对齐
        layout.addWidget(self.toggle_quickpick_btn, 0, Qt.AlignmentFlag.AlignHCenter)

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
            self.on_settings_toggled
        )
        layout.addWidget(self.settings_btn, 0, Qt.AlignmentFlag.AlignHCenter)

        # 创建按钮组，实现互斥效果
        self.button_group = [self.toggle_quickpick_btn, self.settings_btn]

    def handle_import(self):
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
        button.setIconSize(QSize(16, 16))  # 减小图标尺寸使布局更紧凑
        button.setFixedSize(28, 28)  # 减小按钮尺寸使布局更紧凑
        button.setStyleSheet(self.app_style.get_sidebar_button_style() + "QPushButton { margin-left: 2px; margin-right: 2px; }")  # 进一步减小边距使布局更紧凑
        button.setCheckable(True)
        # 使用lambda包装，确保只传递checked参数给toggle_slot
        button.toggled.connect(lambda checked: self.on_button_toggled(button, checked, icon_name, toggle_slot))

    def on_button_toggled(self, button, checked, icon_name, toggle_slot):
        """统一处理按钮切换事件"""
        # 核心改进：设置按钮不参与互斥逻辑，避免影响quickpick的展开折叠状态
        # 使用icon_name来识别特殊按钮，因为它在button初始化时就已经知道，而对应的属性可能还未初始化
        is_settings_button = (icon_name == "settings")
        is_special_button = is_settings_button
        
        # 确保button_group已初始化
        if hasattr(self, 'button_group') and self.button_group:
            if checked:
                # 只有非特殊按钮才执行互斥逻辑
                if not is_special_button:
                    # 实现按钮互斥效果，但只影响其他非特殊按钮
                    for other_button in self.button_group:
                        # 同样使用icon_name来识别其他按钮，而不是直接比较对象
                        other_icon_name = None
                        # 通过遍历按钮和对应的图标名称来找到当前按钮的图标
                        if hasattr(self, 'toggle_quickpick_btn') and other_button == self.toggle_quickpick_btn:
                            other_icon_name = "sidebar"
                        elif hasattr(self, 'settings_btn') and other_button == self.settings_btn:
                            other_icon_name = "settings"
                        
                        # 如果不是特殊按钮且已选中，则取消选中
                        if other_button != button and other_icon_name not in ["settings"] and other_button.isChecked():
                            other_button.setChecked(False)
                
                # 更新图标为选中状态
                button.setIcon(QIcon(get_icon_path(icon_name, selected=True)))
            else:
                # 更新图标为非选中状态
                button.setIcon(QIcon(get_icon_path(icon_name, selected=False)))
        else:
            # 如果button_group未初始化，直接更新图标
            if checked:
                button.setIcon(QIcon(get_icon_path(icon_name, selected=True)))
            else:
                button.setIcon(QIcon(get_icon_path(icon_name, selected=False)))
        
        # 调用具体的处理函数
        toggle_slot(checked, icon_name)

    def on_toggle_quickpick_toggled(self, checked, icon_name="sidebar"):
        """处理展开折叠quickpick按钮切换"""
        if hasattr(self.parent, 'quickpick_panel'):
            if checked:
                self.parent.quickpick_panel.show()
            else:
                self.parent.quickpick_panel.hide()



    def on_settings_toggled(self, checked, icon_name="settings"):
        """处理设置按钮切换，确保不影响quickpick的展开折叠状态"""
        if checked:
            # 显示设置对话框
            self.show_settings_dialog()
            
            # 取消设置按钮的选中状态，因为它不是一个持久的选中状态
            # 这样用户再次点击时还能正常显示设置对话框
            # 注意：由于设置按钮不再参与互斥逻辑，这里不会影响quickpick按钮的状态
            self.settings_btn.setChecked(False)