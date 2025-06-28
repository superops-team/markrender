from PySide6.QtWidgets import QTextEdit
from utils.hash_utils import calculate_md5


class MarkdownEditor(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initial_md5 = calculate_md5(self.toPlainText())
        self.setup_editor()

    def setup_editor(self):
        """配置编辑器基本属性"""
        self.setAcceptRichText(False)
        self.setLineWrapMode(QTextEdit.WidgetWidth)



    def mark_file_modified(self):
        """通过MD5值比较判断文件是否修改"""
        current_md5 = calculate_md5(self.toPlainText())
        return current_md5 != self.initial_md5

    def update_initial_md5(self):
        """更新初始MD5值"""
        self.initial_md5 = calculate_md5(self.toPlainText())

    def get_text_content(self):
        """获取编辑器内容"""
        return self.toPlainText()

    def set_text_content(self, content):
        """设置编辑器内容"""
        self.setPlainText(content)
        self.update_initial_md5()