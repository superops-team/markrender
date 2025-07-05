from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy)
from PySide6.QtGui import QIcon
from PySide6 import QtCore

class SidebarManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # 创建主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 创建顶部按钮组
        self.file_browse_btn = QPushButton()
        self.file_browse_btn.setIcon(QIcon("icons/folder.svg"))  # 需替换为实际图标路径
        self.file_browse_btn.setIconSize(QtCore.QSize(22, 22))
        self.file_browse_btn.setFlat(True)

        self.search_btn = QPushButton()
        self.search_btn.setIcon(QIcon("icons/search.svg"))  # 需替换为实际图标路径
        self.search_btn.setIconSize(QtCore.QSize(22, 22))
        self.search_btn.setFlat(True)

        self.import_btn = QPushButton()
        self.import_btn.setIcon(QIcon("icons/plus-square.svg"))  # 需替换为实际图标路径
        self.import_btn.setIconSize(QtCore.QSize(22, 22))
        self.import_btn.setFlat(True)

        # 将顶部按钮添加到布局
        layout.addWidget(self.file_browse_btn)
        layout.addWidget(self.search_btn)
        layout.addWidget(self.import_btn)

        # 添加弹性空间，使设置按钮位于底部
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # 创建设置按钮
        self.settings_btn = QPushButton()
        self.settings_btn.setIcon(QIcon("icons/settings.svg"))  # 需替换为实际图标路径
        self.settings_btn.setIconSize(QtCore.QSize(22, 22))
        self.settings_btn.setFlat(True)
        layout.addWidget(self.settings_btn)

        # 设置布局策略
        self.setLayout(layout)

if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    sidebar = SidebarManager()
    sidebar.show()
    sys.exit(app.exec_())