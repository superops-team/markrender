import os
import json
import tempfile
import subprocess
from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QFileDialog
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from utils import logger

class ExportManager(QDialog):
    def __init__(self, parent=None, content=""):
        super().__init__(parent)
        self.content = content
        self.init_ui()
        self.setWindowTitle('导出预览')
        self.resize(1000, 800)

    def init_ui(self):
        """初始化界面布局"""
        layout = QVBoxLayout(self)

        # 导出选项按钮
        self.export_html_btn = QPushButton('导出 HTML', self)
        self.export_html_btn.clicked.connect(lambda: self.export_file('html'))

        self.export_md_btn = QPushButton('导出 MD', self)
        self.export_md_btn.clicked.connect(lambda: self.export_file('md'))

        self.export_pdf_btn = QPushButton('导出 PDF', self)
        self.export_pdf_btn.clicked.connect(lambda: self.export_file('pdf'))

        self.export_epub_btn = QPushButton('导出 EPUB', self)
        self.export_epub_btn.clicked.connect(lambda: self.export_file('epub'))

        # 预览区域
        self.preview = QWebEngineView(self)
        export_html_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "resources",
                "export_manager.html"
            )
        )
        self.preview.setUrl(QUrl.fromLocalFile(export_html_path))
        self.preview.loadFinished.connect(self.on_page_loaded)

        # 添加按钮到布局
        layout.addWidget(self.export_html_btn)
        layout.addWidget(self.export_md_btn)
        layout.addWidget(self.export_pdf_btn)
        layout.addWidget(self.export_epub_btn)
        layout.addWidget(self.preview)

    def on_page_loaded(self):
        """页面加载完成后设置预览内容"""
        self.preview.page().runJavaScript(f"setPreviewContent('{json.dumps(self.content)}')")

    def export_file(self, format):
        """处理文件导出逻辑"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp:
                tmp.write(self.content)
                tmp_path = tmp.name

            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "保存文件",
                f"untitled.{format}",
                f"{format.upper()} 文件 (*.{format})",
                options=options
            )

            if file_name:
                if format == 'html':
                    subprocess.run(['pandoc', tmp_path, '-o', file_name])
                elif format == 'md':
                    with open(file_name, 'w') as f:
                        f.write(self.content)
                elif format == 'pdf':
                    subprocess.run(['pandoc', tmp_path, '-o', file_name])
                elif format == 'epub':
                    subprocess.run(['pandoc', tmp_path, '-o', file_name])
                logger.info(f"文件已导出到: {file_name}")
        except Exception as e:
            logger.error(f"导出失败: {str(e)}")
        finally:
            if 'tmp_path' in locals():
                os.unlink(tmp_path)