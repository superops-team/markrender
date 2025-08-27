from PySide6.QtWidgets import QWidget, QHBoxLayout, QToolButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from utils.path import get_icon_path

from PySide6.QtWidgets import QMenu  # 新增导入

class ButtonController(QWidget):
    def __init__(self, parent, quickpick_panel, markdown_editor):
        super().__init__(parent)
        self.quickpick_panel = quickpick_panel
        self.markdown_editor = markdown_editor
        # 添加选中状态标志，默认进入页面后为选中状态
        self.is_quickpick_selected = True
        self.setup_buttons()

    def setup_buttons(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignRight)

        # 控制 quickpick 面板显示/隐藏的按钮 - 使用样式常量
        from app.preference.style_constants import NEUTRAL_300, SPACING_XS
        self.quickpick_btn = QToolButton()
        # 初始设置为选中状态的图标
        self.quickpick_btn.setIcon(QIcon(get_icon_path('sidebar', True)))
        self.quickpick_btn.setToolTip('显示/隐藏快速选择面板')
        self.quickpick_btn.clicked.connect(self.toggle_quickpick_panel)
        self.quickpick_btn.setStyleSheet(f'''
            QToolButton {{
                border: none;
                padding: {SPACING_XS}px;
            }}
            QToolButton:hover {{
                background-color: {NEUTRAL_300};
            }}
        ''')
        self.quickpick_btn.setFixedSize(20, 20)  # 固定按钮大小
        layout.addWidget(self.quickpick_btn)

        # 确保进入页面后默认展示quickpick页面
        if not self.quickpick_panel.isVisible():
            self.quickpick_panel.show()

    def toggle_quickpick_panel(self):
        if self.quickpick_panel.isVisible():
            self.quickpick_panel.hide()
            # 未选中状态，使用普通图标
            self.quickpick_btn.setIcon(QIcon(get_icon_path('sidebar', False)))
            self.is_quickpick_selected = False
        else:
            self.quickpick_panel.show()
            # 选中状态，使用选中图标
            self.quickpick_btn.setIcon(QIcon(get_icon_path('sidebar', True)))
            self.is_quickpick_selected = True