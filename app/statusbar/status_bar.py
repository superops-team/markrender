from PySide6.QtWidgets import QStatusBar, QLabel  # 修改导入语句
from PySide6.QtCore import Qt
from app.preference import AppStyle  # 新增导入

class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_size_label = QLabel("大小: 0 KB")  # 修改为 QLabel
        self.word_count_label = QLabel("字数: 0")  # 修改为 QLabel

        # 设置标签对齐方式为右对齐
        self.file_size_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.word_count_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.addPermanentWidget(self.file_size_label)
        self.addPermanentWidget(self.word_count_label)

        # 设置样式表
        self.setStyleSheet(AppStyle().get_status_bar())  # 新增样式表设置

    def update_file_size(self, size_in_bytes):
        size_in_kb = size_in_bytes / 1024
        self.file_size_label.setText(f"文件大小: {size_in_kb:.2f} KB")

    def update_word_count(self, count):
        self.word_count_label.setText(f"字数: {count}")

    def show_message(self, message):
        self.showMessage(message, 3000)  # 显示消息 3 秒