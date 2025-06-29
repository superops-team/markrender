from PySide6 import QtWidgets, QtCore
from db.markdown_manager import MarkdownManager
from ui.dayu_widgets.label import MLabel
from ui.dayu_widgets.line_edit import MLineEdit
from ui.dayu_widgets.text_edit import MTextEdit
from ui.dayu_widgets.push_button import MPushButton
from ui.dayu_widgets.message import MMessage


class NewFileDialog(QtWidgets.QDialog):
    save_requested = QtCore.Signal(str, str)

    def __init__(self, markdown_manager=None, parent=None):
        super().__init__(parent)
        self.dialog_title = "新建"
        self.initial_title = ""
        self.markdown_manager = markdown_manager
        self.setWindowTitle(self.dialog_title)
        self.setModal(True)  # 设置为模态对话框
        self.init_ui()
        self.setStyleSheet("QDialog { border-radius: 5px; }")  # 简单样式设置，可按需调整

    def init_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        form_widget = QtWidgets.QWidget()
        form_layout = QtWidgets.QVBoxLayout()

        self.title_label = MLabel('标题:')
        self.title_input = MLineEdit()
        self.title_input.setText(self.initial_title)

        self.content_label = MLabel('内容:')
        self.content_input = MTextEdit()

        form_layout.addWidget(self.title_label)
        form_layout.addWidget(self.title_input)
        form_layout.addWidget(self.content_label)
        form_layout.addWidget(self.content_input, stretch=1)  # 设置拉伸，使内容输入框可自适应
        form_widget.setLayout(form_layout)
        main_layout.addWidget(form_widget, stretch=1)

        # 添加底部按钮布局
        self.bottom_button_layout = QtWidgets.QHBoxLayout()
        self.save_button = MPushButton('保存')
        self.save_button.setProperty('type', 'primary')  # 设置按钮为主要样式，保持风格一致
        self.save_button.clicked.connect(self.on_save_clicked)
        self.bottom_button_layout.addStretch()
        self.bottom_button_layout.addWidget(self.save_button)
        main_layout.addLayout(self.bottom_button_layout)

        self.resize(600, 400)  # 设置初始大小

    def on_save_clicked(self):
        title = self.title_input.text().strip()
        content = self.content_input.toPlainText().strip()

        if not title:
            MMessage.warning('标题不能为空', parent=self, duration=5)
            return

        try:
            # 添加日志记录保存信息
            import logging
            logging.basicConfig(level=logging.INFO)
            logging.info(f'尝试保存 Markdown 文件，标题: {title}, 内容长度: {len(content)}')
            # 发射保存请求信号
            self.save_requested.emit(title, content)
            MMessage.success('保存成功', parent=self, duration=1)
            self.accept()  # 关闭对话框
        except Exception as e:
            logging.error(f'保存失败: {str(e)}')
            MMessage.error(f'保存失败: {str(e)}', parent=self, duration=5)
