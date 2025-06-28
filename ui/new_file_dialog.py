from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLineEdit, QLabel, QTextEdit, QMessageBox
from PySide6.QtCore import Signal

class NewFileDialog(QDialog):
    save_requested = Signal(str, str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('新建')
        layout = QVBoxLayout()
        
        self.title_label = QLabel('标题:')
        self.title_input = QLineEdit()
        
        self.content_label = QLabel('Markdown 内容:')
        self.content_edit = QTextEdit()
        
        self.save_button = QPushButton('保存')
        self.save_button.clicked.connect(self.on_save_clicked)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.title_input)
        layout.addWidget(self.content_label)
        layout.addWidget(self.content_edit)
        layout.addWidget(self.save_button)
        
        self.setLayout(layout)
        
    def on_save_clicked(self):
        title = self.title_input.text()
        content = self.content_edit.text()
        if title and content:
            self.save_requested.emit(title, content)
            self.accept()
        else:
            QMessageBox.warning(self, '错误', '标题和内容不能为空')