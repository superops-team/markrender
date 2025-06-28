from PySide6.QtWidgets import QStatusBar, QLabel
from PySide6.QtCore import Qt

class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_changed_label = QLabel("文件状态: 未变更")
        self.file_size_label = QLabel("文件大小: 0 KB")
        self.word_count_label = QLabel("字数: 0")

        self.addWidget(self.file_changed_label, 1)
        self.addWidget(self.file_size_label, 1)
        self.addWidget(self.word_count_label, 1)

    def update_file_status(self, is_changed):
        self.file_changed_label.setText(f"文件状态: {'已变更' if is_changed else '未变更'}")

    def update_file_size(self, size_in_bytes):
        size_in_kb = size_in_bytes / 1024
        self.file_size_label.setText(f"文件大小: {size_in_kb:.2f} KB")

    def update_word_count(self, count):
        self.word_count_label.setText(f"字数: {count}")