from PySide6.QtWidgets import QWidget, QHBoxLayout, QToolButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from utils.path import get_icon_path

from PySide6.QtWidgets import QMenu  # 新增导入

class ButtonController(QWidget):
    def __init__(self, parent, history_panel, markdown_editor):
        super().__init__(parent)
        self.history_panel = history_panel
        self.markdown_editor = markdown_editor
        self.setup_buttons()

    def setup_buttons(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignRight)

        # 控制 history 面板显示/隐藏的按钮 - 使用样式常量
        from app.preference.style_constants import NEUTRAL_300, SPACING_XS
        self.history_btn = QToolButton()
        self.history_btn.setIcon(QIcon(get_icon_path('sidebar')))
        self.history_btn.setToolTip('显示/隐藏历史面板')
        self.history_btn.clicked.connect(self.toggle_history_panel)
        self.history_btn.setStyleSheet(f'''
            QToolButton {{
                border: none;
                padding: {SPACING_XS}px;
            }}
            QToolButton:hover {{
                background-color: {NEUTRAL_300};
            }}
        ''')
        self.history_btn.setFixedSize(20, 20)  # 固定按钮大小
        layout.addWidget(self.history_btn)

        # 控制 editor 编辑模式和预览模式的按钮 - 使用样式常量
        self.mode_btn = QToolButton()
        self.mode_btn.setIcon(QIcon(get_icon_path('columns')))
        self.mode_btn.setToolTip('切换编辑/预览模式')
        self.mode_btn.clicked.connect(self.toggle_edit_mode)
        self.mode_btn.setStyleSheet(f'''
            QToolButton {{
                border: none;
                padding: {SPACING_XS}px;
            }}
            QToolButton:hover {{
                background-color: {NEUTRAL_300};
            }}
        ''')
        self.mode_btn.setFixedSize(20, 20)  # 固定按钮大小
        layout.addWidget(self.mode_btn)

        # 导出控制按钮，改为支持下拉菜单
        self.export_btn = QToolButton()
        self.export_btn.setIcon(QIcon(get_icon_path('download')))
        self.export_btn.setToolTip('导出')
        # 修改为 InstantPopup 模式，点击整个按钮都会触发下拉菜单
        self.export_btn.setPopupMode(QToolButton.InstantPopup)
        
        # 创建下拉菜单 - 使用样式常量
        from app.preference.style_constants import NEUTRAL_0, NEUTRAL_200, SPACING_XS, SPACING_XL
        export_menu = QMenu(self.export_btn)
        export_menu.setStyleSheet(f'''
            QMenu {{
                border: 1px solid {NEUTRAL_200};
                background-color: {NEUTRAL_0};
                padding: {SPACING_XS}px;
                margin: {SPACING_XS}px;
            }}
            QMenu::item {{
                padding: {SPACING_XS}px {SPACING_XL}px {SPACING_XS}px {SPACING_XL}px;
                margin: 0px;
            }}
            QMenu::item:selected {{
                background-color: {NEUTRAL_200};
            }}
        ''')
        formats = ['html', 'md', 'pdf', 'epub']
        for format in formats:
            action = export_menu.addAction(f'导出 {format.upper()}')
            action.triggered.connect(lambda _, fmt=format: self.export_content(fmt))
        
        self.export_btn.setMenu(export_menu)
        self.export_btn.setStyleSheet(f'''
            QToolButton {{
                border: none;
                padding: {SPACING_XS}px;
                background: transparent;
                selection-background-color: transparent;
            }}
            QToolButton:hover {{
                background-color: {NEUTRAL_300};
            }}
            QToolButton::menu-indicator {{
                image: none;
            }}
        ''')
        self.export_btn.setFixedSize(20, 20)  # 固定按钮大小
        layout.addWidget(self.export_btn)

    def toggle_history_panel(self):
        if self.history_panel.isVisible():
            self.history_panel.hide()
        else:
            self.history_panel.show()

    def toggle_edit_mode(self):
        # 这里需要根据实际的编辑模式切换逻辑修改，当前为示例代码
        print('切换编辑/预览模式')

    def export_content(self, format):
        # 调用 markdown_editor 的导出方法，直接导出指定类型文件
        self.markdown_editor.export_file(format)