from PySide6.QtWidgets import QStatusBar, QLabel  # 修改导入语句
from PySide6.QtCore import Qt


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
        self.setStyleSheet('''
            QStatusBar {
                border: 2px solid #ddd; /* 边框样式 */
                border-radius: 10px; /* 边框圆角 */
                background-color: #f5f5f5; /* 背景颜色 */
                color: #eaf3ff; /* 字体颜色 */
                font-size: 12px; /* 字体大小 */
                padding: 5px 20px 5px 32px; /* 上、右、下、左内边距，左侧设置为 32px */
            }
            QLabel {
                margin-left: 15px; /* 标签间距 */
                color: #C3C9D3; /* 新增标签字体颜色 */
            }
        ''')

    def update_file_size(self, size_in_bytes):
        size_in_kb = size_in_bytes / 1024
        self.file_size_label.setText(f"文件大小: {size_in_kb:.2f} KB")

    def update_word_count(self, count):
        self.word_count_label.setText(f"字数: {count}")
