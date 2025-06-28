from PySide6.QtWidgets import QWidget, QSplitter, QVBoxLayout, QFileDialog, QSizePolicy
from PySide6.QtCore import Qt, QTimer
from PySide6.QtCore import Qt
from ui.markdown_editor import MarkdownEditor
from ui.markdown_renderer import MarkdownRenderer

class EditorPanel(QWidget):
    def __init__(self, theme_manager_gui, parent=None):
        super().__init__(parent)
        self.theme_manager_gui = theme_manager_gui
        self.editor = MarkdownEditor()
        self.renderer = MarkdownRenderer(theme_manager_gui)
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        """初始化编辑器和预览区布局"""
        layout = QVBoxLayout(self)
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.renderer)
        self.editor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.renderer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        splitter.setSizes([int(self.width()/2), int(self.width()/2)])
        layout.addWidget(splitter)
        self.setLayout(layout)
        
    def setup_connections(self):
        """设置信号与槽连接"""
        self.editor.textChanged.connect(self.update_preview)
        self.editor.textChanged.connect(self.mark_file_modified)
        
    def export_image_dialog(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "保存图片", "", "PNG 文件 (*.png);;JPEG 文件 (*.jpg)"
        )
        if file_name:
            QTimer.singleShot(500, lambda: self.export_image(file_name))

    def export_pdf_dialog(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "保存PDF", "", "PDF 文件 (*.pdf)"
        )
        if file_name:
            QTimer.singleShot(500, lambda: self.export_pdf(file_name))

    def update_preview(self):
        """更新预览区内容"""
        markdown_text = self.editor.get_text_content()
        self.renderer.render_markdown(markdown_text)
        

        
    def get_text_content(self):
        """获取编辑器内容"""
        return self.editor.get_text_content()

    def set_text_content(self, content):
        """设置编辑器内容"""
        self.editor.set_text_content(content)

    def update_initial_md5(self):
        """更新初始MD5值"""
        self.editor.update_initial_md5()

    def mark_file_modified(self):
        """检查文件是否修改"""
        return self.editor.mark_file_modified()

    def export_image(self, file_name):
        """导出图片"""
        image = self.renderer.webview.grab().toImage()
        return image.save(file_name)

    def export_pdf(self, file_name):
        """导出PDF"""
        if not file_name.endswith(".pdf"):
            file_name += ".pdf"
        self.renderer.webview.page().printToPdf(file_name)