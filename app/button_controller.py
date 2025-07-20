from PySide6.QtWidgets import QWidget, QHBoxLayout, QToolButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from utils.path import get_icon_path

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

        # 控制 history 面板显示/隐藏的按钮
        self.history_btn = QToolButton()
        self.history_btn.setIcon(QIcon(get_icon_path('sidebar')))
        self.history_btn.setToolTip('显示/隐藏历史面板')
        self.history_btn.clicked.connect(self.toggle_history_panel)
        self.history_btn.setStyleSheet('''
            QToolButton {
                border: none;
                padding: 2px;
                border-radius: 4px;
            }
            QToolButton:hover {
                background-color: #d0d0d0;
            }
        ''')
        self.history_btn.setFixedSize(20, 20)  # 固定按钮大小
        layout.addWidget(self.history_btn)

        # 控制 editor 编辑模式和预览模式的按钮
        self.mode_btn = QToolButton()
        self.mode_btn.setIcon(QIcon(get_icon_path('columns')))
        self.mode_btn.setToolTip('切换编辑/预览模式')
        self.mode_btn.clicked.connect(self.toggle_edit_mode)
        self.mode_btn.setStyleSheet('''
            QToolButton {
                border: none;
                padding: 2px;
                border-radius: 4px;
            }
            QToolButton:hover {
                background-color: #d0d0d0;
            }
        ''')
        self.mode_btn.setFixedSize(20, 20)  # 固定按钮大小
        layout.addWidget(self.mode_btn)

        # 导出控制按钮
        self.export_btn = QToolButton()
        self.export_btn.setIcon(QIcon(get_icon_path('cast')))
        self.export_btn.setToolTip('导出')
        self.export_btn.clicked.connect(self.export_content)
        self.export_btn.setStyleSheet('''
            QToolButton {
                border: none;
                padding: 2px;
                border-radius: 4px;
            }
            QToolButton:hover {
                background-color: #d0d0d0;
            }
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

    def export_content(self):
        self.markdown_editor.export_to_browser()