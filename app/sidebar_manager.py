from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QFileDialog, QMessageBox, QDialog, QLabel, QProgressBar, QFrame)
from PySide6.QtGui import QIcon, QFont, QColor
from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt
from utils import logger
from db import db_manager
from db.markdown_manager import MarkdownManager
import os
from markitdown import MarkItDown 
import time
import sys
import re
import urllib.parse

def replace_image_paths(content, base_url):
    # 匹配 Markdown 图片语法：![alt](path)
    pattern = r'!\[(.*?)\]\((.*?)\)'
    
    # 替换为完整路径
    def replace(match):
        alt = match.group(1)
        path = match.group(2)
        
        # 跳过已为完整路径的图片
        if path.startswith(('http://', 'https://')):
            return f'![{alt}]({path})'
        # 构建完整路径（根据实际需求调整拼接方式）
        full_path = os.path.join(base_url, path)
        # 对路径中的空格进行 URL 编码
        encoded_path = urllib.parse.quote(full_path, safe=':/')
        logger.info(f"full_path: {encoded_path}")
        return f'![{alt}]({encoded_path})'
    
    return re.sub(pattern, replace, content)

class ImportDialog(QDialog):
    def __init__(self, parent, markdown_manager, history_panel):
        super().__init__(parent)
        self.markdown_manager = markdown_manager
        self.parent = parent
        self.history_panel = history_panel
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("文件导入")
        dialog_layout = QVBoxLayout(self)
        dialog_layout.setContentsMargins(10, 10, 10, 10)
        dialog_layout.setSpacing(10)

        # 创建大尺寸导入区域（类似拖拽风格）
        self.import_area = QFrame(self)
        self.import_area.setMinimumSize(400, 200)
        self.import_area.setStyleSheet("""
            QFrame {
                border: 1px dashed #1990ff;
                border-radius: 8px;
                background-color: #f5f5f5;
                margin: 10px;
            }
            QFrame:hover {
                border-color: #0d6efd;
                background-color: #e6e6e6;
            }
        """)
        area_layout = QVBoxLayout(self.import_area)
        area_layout.setAlignment(QtCore.Qt.AlignCenter)

        # 创建遮罩层和加载状态标签，初始状态隐藏
        self.overlay = QFrame(self.import_area)
        # 修改遮罩层样式，将透明度设为 1 使其不透明
        self.overlay.setStyleSheet("background-color: rgba(255, 255, 255, 1);")
        self.overlay.setGeometry(self.import_area.geometry())
        self.overlay.hide()

        self.loading_label = QLabel("任务支持后台处理，可关闭此窗口，后台处理中...", self.overlay)
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("font-size: 16px; color: #0d6efd;")
        self.loading_label.setGeometry(self.overlay.geometry())
        self.loading_label.hide()

        # 导入区域文字提示
        self.import_label = QLabel("点击导入", self)
        font = QFont()
        # 设置字体大小和加粗
        font.setPointSize(12)
        font.setBold(True)
        self.import_label.setFont(font)
        
        # 设置标签居中对齐和背景颜色
        self.import_label.setAlignment(Qt.AlignCenter)
        # 合并样式设置，避免被覆盖
        self.import_label.setStyleSheet("background-color: #F0F3FF; padding: 10px; border-radius: 4px; color: #343a40;")
        
        # 创建布局并将标签居中添加到import_area
        label_layout = QVBoxLayout(self.import_area)
        label_layout.addWidget(self.import_label, alignment=Qt.AlignCenter)
        # 移除单独设置颜色的代码
        # self.import_label.setStyleSheet("color: #343a40;")
        area_layout.addWidget(self.import_label)

        # 支持的导入格式
        supported_formats = ['doc', 'pdf', 'md', 'xlsx', 'xls', 'pptx', 'epub', 'docx']
        self.format_label = QLabel(f"支持格式: {', '.join(supported_formats)}", self)
        self.format_label.setStyleSheet("color: #6c757d; font-size: 12px;")
        area_layout.addWidget(self.format_label)

        dialog_layout.addWidget(self.import_area, 0, QtCore.Qt.AlignCenter)

        # 进度条
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.hide()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border-radius: 4px;
                text-align: center;
                height: 8px;
            }
            QProgressBar::chunk {
                background-color: #0d6efd;
                border-radius: 4px;
            }
        """)
        dialog_layout.addWidget(self.progress_bar)

        # 文件信息标签
        self.info_label = QLabel(self)
        self.info_label.hide()
        self.info_label.setStyleSheet("color: #28a745; font-size: 13px;")
        dialog_layout.addWidget(self.info_label)

        # 关闭按钮
        self.close_button = QPushButton("关闭", self)
        self.close_button.hide()
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
                border-radius: 5px;
            }
        """)
        self.close_button.clicked.connect(self.close)
        dialog_layout.addWidget(self.close_button, 0, QtCore.Qt.AlignCenter)

        # 为导入区域添加点击事件
        self.import_area.mousePressEvent = self.perform_import

    def perform_import(self, event=None):  # 显式声明事件参数，设置默认值避免调用冲突
        # 定义支持的文件格式和最大文件大小
        supported_formats = ['doc', 'pdf', 'md', 'xlsx', 'xls', 'pptx', 'epub', 'docx']
        max_size = 30 * 1024 * 1024  # 30MB

        # 弹出文件选择对话框
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "导入文件",
            "",
            "支持的文件 (*.doc *.pdf *.md *.xlsx *.xls *.pptx *.epub *.docx)"
        )

        if not file_path:
            return

        # 验证文件大小
        file_size = os.path.getsize(file_path)
        if file_size > max_size:
            QMessageBox.warning(self, "文件过大", "文件大小不能超过 30MB")
            return

        # 验证文件格式
        file_ext = os.path.splitext(file_path)[1][1:]
        if file_ext not in supported_formats:
            QMessageBox.warning(self, "格式不支持", "仅支持 md、doc、pdf、md、excel、pptx、epub 格式的文件")
            return

        self.import_area.setEnabled(False)
        self.progress_bar.show()
        self.info_label.show()
        self.progress_bar.setValue(0)
        # 显示遮罩层和加载状态标签
        self.overlay.show()
        self.loading_label.show()
        self.overlay.resize(self.import_area.size())
        # 将遮罩层置于最上层
        self.overlay.raise_()

        # 创建并启动导入线程
        self.import_thread = ImportThread(file_path, self.markdown_manager, self.history_panel)
        self.import_thread.progress_updated.connect(self.update_progress)
        self.import_thread.finished.connect(self.import_finished)
        self.import_thread.error_occurred.connect(self.import_error)
        self.import_thread.start()

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)
        self.repaint()

    def import_finished(self, file_info):
        self.info_label.setText(file_info)
        self.progress_bar.setValue(100)
        self.close_button.show()
        # 隐藏遮罩层和加载状态标签
        self.overlay.hide()
        self.loading_label.hide()
        self.import_area.setEnabled(True)

    def import_error(self, error_msg):
        QMessageBox.warning(self, "导入失败", error_msg)
        # 隐藏遮罩层和加载状态标签
        self.overlay.hide()
        self.loading_label.hide()
        self.import_area.setEnabled(True)
        self.close()

class ImportThread(QtCore.QThread):
    progress_updated = QtCore.Signal(int)
    finished = QtCore.Signal(str)
    error_occurred = QtCore.Signal(str)

    def __init__(self, file_path, markdown_manager, history_panel):
        super().__init__()
        self.file_path = file_path
        self.file_name = os.path.basename(self.file_path)
        self.markdown_manager = markdown_manager
        self.history_panel = history_panel
        self.file_size = os.path.getsize(file_path)
        self.file_ext = os.path.splitext(file_path)[1][1:]

    def run(self):
        try:
            start_time = time.time()
            # 假设转换过程可分步骤，这里简单模拟
            # step1: 获取文件属性
            size_kb = self.file_size / 1024
            size_str = f'{size_kb:.2f} KB' if size_kb < 1024 else f'{size_kb / 1024:.2f} MB'
            title = os.path.splitext(self.file_name)[0]
            tag = self.file_ext
            self.progress_updated.emit(25)
            # step2: 转换格式
            logger.debug(f"开始转换格式！文件格式: {self.file_ext} 文件大小: {size_str}")
            md_content = self.convert()
            self.progress_updated.emit(50)
            # step3: 写入数据
            self.markdown_manager.save_markdown(title=title, content=md_content, tags=tag)
            logger.debug(f"写入数据！文件格式: {self.file_ext} 文件大小: {size_str}, tags: {tag}")
            self.progress_updated.emit(75)  
            # step4: 刷新历史记录
            self.history_panel.load_history_items()
            process_time = time.time() - start_time
            info_text = f"导入成功！\n处理时长: {process_time:.2f} 秒\n文件格式: {self.file_ext}\n文件大小: {size_str}"
            self.finished.emit(info_text)
            self.progress_updated.emit(100)
        except Exception as e:
            self.error_occurred.emit(f"导入文件时出错: {str(e)}")
    
    def convert(self):
        # 初始化 MarkItDown
        if self.file_ext == 'pdf':
            from marker.converters.pdf import PdfConverter
            from marker.models import create_model_dict
            from marker.config.parser import ConfigParser
            from marker.output import save_output
            base_path =  f"{db_manager.get_user_data_dir()}/output"
            # base_path = urllib.parse.quote(base_path, safe=':/')
            config = {
                "output_format": "markdown",
                "output_dir": base_path,
            }
            config_parser = ConfigParser(config)
            try:
                converter = PdfConverter(
                    config=config_parser.generate_config_dict(),
                    artifact_dict=create_model_dict(),
                    processor_list=config_parser.get_processors(),
                    renderer=config_parser.get_renderer(),
                    llm_service=config_parser.get_llm_service()
                )
                rendered = converter(self.file_path)
                logger.info(f"转换 PDF 成功, 输出路径: {base_path}, 文件名: {self.file_name}")
                save_output(rendered, base_path, self.file_name)
                return replace_image_paths(rendered.markdown, base_path)
            except Exception as e:
                logger.error(f"转换 PDF 时出错, 降级为markitdown: {str(e)}")
        md = MarkItDown()
        result = md.convert(self.file_path)
        return result.text_content
        

class SidebarManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.markdown_manager = MarkdownManager()
        self.parent = parent
        self.init_ui()

    def get_icon_path(self, icon_name):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, 'icons', icon_name)
        return os.path.join('icons', icon_name)
        
    def init_ui(self):
        # 创建主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 创建顶部按钮组
        self.file_browse_btn = QPushButton()
        self.file_browse_btn.setIcon(QIcon(self.get_icon_path("folder.svg")))  # 需替换为实际图标路径
        self.file_browse_btn.setIconSize(QtCore.QSize(22, 22))
        self.file_browse_btn.setFlat(True)

        self.search_btn = QPushButton()
        self.search_btn.setIcon(QIcon(self.get_icon_path("search.svg")))  # 需替换为实际图标路径
        self.search_btn.setIconSize(QtCore.QSize(22, 22))
        self.search_btn.setFlat(True)

        self.import_btn = QPushButton()
        self.import_btn.setIcon(QIcon(self.get_icon_path("plus-square.svg")))  # 需替换为实际图标路径
        self.import_btn.setIconSize(QtCore.QSize(22, 22))
        self.import_btn.setFlat(True)
        self.import_btn.clicked.connect(self.handle_import)

        # 将顶部按钮添加到布局
        layout.addWidget(self.file_browse_btn)
        layout.addWidget(self.search_btn)
        layout.addWidget(self.import_btn)

        # 添加弹性空间，使设置按钮位于底部
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # 创建设置按钮
        self.settings_btn = QPushButton()
        self.settings_btn.setIcon(QIcon(self.get_icon_path("settings.svg")))  # 需替换为实际图标路径
        self.settings_btn.setIconSize(QtCore.QSize(22, 22))
        self.settings_btn.setFlat(True)
        layout.addWidget(self.settings_btn)

        # 设置布局策略
        self.setLayout(layout)

    def handle_import(self):
        import_dialog = ImportDialog(self, self.markdown_manager, self.parent.history_panel if self.parent else None)
        import_dialog.exec_()