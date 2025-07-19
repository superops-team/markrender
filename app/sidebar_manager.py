from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QFileDialog,
    QMessageBox,
    QDialog,
    QLabel,
    QProgressBar,
    QFrame,
)
from PySide6.QtGui import QIcon, QFont, QPixmap
from PySide6 import QtCore, QtGui
from PySide6.QtCore import Qt
from app.settings_dialog import SettingsDialog
from utils import logger, get_icon_path, time_utils, supported_formats
from db import db_manager
from db.markdown_manager import MarkdownManager
from db.settings_manager import SettingsManager
import os
from markitdown import MarkItDown
import time
import re
import urllib.parse
from .app_style import AppStyle


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
        # 监听键盘事件以处理粘贴操作
        self.setFocusPolicy(Qt.StrongFocus)
        self.import_settings = SettingsManager().get_settings_dict('import') # 导入导出设置


    def init_ui(self):
        self.setWindowTitle("文件导入")
        dialog_layout = QVBoxLayout(self)
        dialog_layout.setContentsMargins(10, 10, 10, 10)
        dialog_layout.setSpacing(10)

        # 创建大尺寸导入区域（类似拖拽风格）
        self.import_area = QFrame(self)
        self.import_area.setMinimumSize(400, 200)
        self.import_area.setStyleSheet(AppStyle().get_import_area())
        area_layout = QVBoxLayout(self.import_area)
        area_layout.setAlignment(QtCore.Qt.AlignCenter)

        # 创建遮罩层和加载状态标签，初始状态隐藏
        self.overlay = QFrame(self.import_area)
        # 修改遮罩层样式，将透明度设为 1 使其不透明
        self.overlay.setStyleSheet(AppStyle().get_overlay_style())
        self.overlay.setGeometry(self.import_area.geometry())
        self.overlay.hide()

        self.loading_label = QLabel("任务支持后台处理，可关闭此窗口，后台处理中...", self.overlay)
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet(AppStyle().get_loading_label())
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
        self.import_label.setStyleSheet(AppStyle().get_import_label())

        # 创建布局并将标签居中添加到import_area
        label_layout = QVBoxLayout(self.import_area)
        label_layout.addWidget(self.import_label, alignment=Qt.AlignCenter)
        # 移除单独设置颜色的代码
        # self.import_label.setStyleSheet("color: #343a40;")
        area_layout.addWidget(self.import_label)

        self.format_label = QLabel(f"支持格式: {', '.join(supported_formats)}", self)
        self.format_label.setStyleSheet(AppStyle().get_format_label())
        area_layout.addWidget(self.format_label)

        dialog_layout.addWidget(self.import_area, 0, QtCore.Qt.AlignCenter)

        # 进度条
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.hide()
        self.progress_bar.setStyleSheet(AppStyle().get_progress_bar())
        dialog_layout.addWidget(self.progress_bar)

        # 文件信息标签
        self.info_label = QLabel(self)
        self.info_label.hide()
        self.info_label.setStyleSheet(AppStyle().get_info_label())
        dialog_layout.addWidget(self.info_label)

        # 关闭按钮
        self.close_button = QPushButton("关闭", self)
        self.close_button.hide()
        self.close_button.setStyleSheet(AppStyle().get_close_button_style())
        self.close_button.clicked.connect(self.close)
        dialog_layout.addWidget(self.close_button, 0, QtCore.Qt.AlignCenter)

        # 为导入区域添加点击事件
        self.import_area.mousePressEvent = self.perform_import

    def keyPressEvent(self, event):
        """监听键盘事件，处理粘贴操作"""
        if event.matches(QtGui.QKeySequence.Paste):
            self.handle_paste_image()
        super().keyPressEvent(event)

    def handle_paste_image(self):
        """处理剪贴板中的图片并上传"""
        clipboard = QtGui.QGuiApplication.clipboard()
        mime_data = clipboard.mimeData()

        if mime_data.hasImage():
            image = mime_data.imageData()
            # 这里可根据实际需求实现图片上传逻辑，以下为示例
            # 生成临时文件名
            timestamp = str(int(time.time()))
            temp_file = os.path.join(os.getcwd(), f"pasted_image_{timestamp}.png")
            image.save(temp_file, "PNG")
            
            # 调用上传逻辑，这里假设存在一个 upload_file 方法
            self.do_import(temp_file)
            
            logger.info(f"已粘贴图片到 {temp_file}")
            QMessageBox.information(self, "提示", "图片粘贴成功")
        else:
            QMessageBox.warning(self, "警告", "剪贴板中没有图片")

    def perform_import(self, event=None):  # 显式声明事件参数，设置默认值避免调用冲突
        # 定义支持的文件格式和最大文件大小
        supported_formats = AppStyle().get_supported_formats()
        # max_size = 30 * 1024 * 1024  # 30MB
        import_size = self.import_settings.get('import_size', 30)
        max_size = int(import_size) * 1024 * 1024

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
            QMessageBox.warning(self, f"文件过大", f"文件大小不能超过 {import_size}MB")
            return

        # 验证文件格式
        file_ext = os.path.splitext(file_path)[1][1:]
        if file_ext not in supported_formats:
            QMessageBox.warning(
                self, "格式不支持", f"仅支持 {', '.join(supported_formats)} 格式的文件")
            return
        self.do_import(file_path)
       

    def do_import(self, file_path):
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
        self.import_thread = ImportThread(
            file_path, self.markdown_manager, self.history_panel)
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
        self.import_settings = SettingsManager().get_settings_dict('import') # 导入导出设置
        self.file_size = os.path.getsize(file_path)
        self.file_ext = os.path.splitext(file_path)[1][1:]
        if self.file_ext == 'pdf':
            self.converter = 'marker-pdf'
        else:
            self.converter = 'markitdown'
        self.converter_start = None
        self.converter_end = None

    def run(self):
        try:
            self.converter_start = time_utils.now()
            # 假设转换过程可分步骤，这里简单模拟
            # step1: 获取文件属性
            size_kb = self.file_size / 1024
            size_str = f'{
                size_kb:.2f} KB' if size_kb < 1024 else f'{
                size_kb / 1024:.2f} MB'
            title = os.path.splitext(self.file_name)[0]
            self.progress_updated.emit(25)
            last_id = self.markdown_manager.save_markdown(
                title=title,
                tags=self.file_ext, 
                file_path=self.file_path, 
                converter=self.converter, 
                converter_start=self.converter_start,
                status='processing',
            )
            # step2: 转换格式
            logger.debug(f"开始转换格式！文件格式: {self.file_ext} 文件大小: {size_str}")
            md_content = self.convert()
            self.progress_updated.emit(50)
            self.converter_end = time_utils.now()
            # step3: 写入数据
            self.markdown_manager.save_markdown(
                id=last_id,
                content=md_content, 
                converter=self.converter,
                converter_start=self.converter_start,
                converter_end=self.converter_end,
                status='processed',
            )
            logger.debug(
                f"写入数据！文件格式: {self.file_ext} 文件大小: {size_str} 转换器：{self.converter}")
            self.progress_updated.emit(75)
            # step4: 刷新历史记录
            self.history_panel.load_history_items()
            process_time = time_utils.get_duration(self.converter_start, self.converter_end).total_seconds()
            info_text = f"导入成功！\n处理时长: {
                process_time:.2f} 秒\n文件格式: {
                self.file_ext}\n文件大小: {size_str}"
            self.finished.emit(info_text)
            self.progress_updated.emit(100)
        except Exception as e:
            self.error_occurred.emit(f"导入文件时出错: {str(e)}")

    def convert(self):
        md_content = ''
        if self.file_ext == 'pdf':
            import_method = self.import_settings.get('pdf_import_method', 'marker-pdf')
            if import_method == 'marker-pdf':
                md_content = self.convert_by_markerpdf()
            if import_method == 'markitdown':
                md_content = self.convert_by_markitdown()
        if self.file_ext in ('md', 'docx', 'ppt', 'pptx', 'xls', 'xlsx'):
            md_content = self.convert_by_markitdown()
        if not md_content:
            md_content = self.convert_by_markitdown()
        return md_content
       
    
    def convert_by_markerpdf(self):
        """
        use marker-pdf to parse pdf
        """
        from marker.converters.pdf import PdfConverter
        from marker.models import create_model_dict
        from marker.config.parser import ConfigParser
        from marker.output import save_output
        self.converter = 'marker-pdf'
        base_path = f"{db_manager.get_user_data_dir()}/output"
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
            logger.info(
                f"转换 PDF 成功, 输出路径: {base_path}, 文件名: {
                    self.file_name}")
            save_output(rendered, base_path, self.file_name)
            return replace_image_paths(rendered.markdown, base_path)
        except Exception as e:
            logger.error(f"转换 PDF 时出错, 降级为markitdown: {str(e)}")

    def convert_by_markitdown(self):
        """
        use markitdown to parse pdf or img
        """
        self.converter = 'markitdown'
        md = MarkItDown()
        result = md.convert(self.file_path)
        return result.text_content

class SidebarManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.markdown_manager = MarkdownManager()
        self.parent = parent
        self.app_style = AppStyle()  # 添加样式实例
        self.init_ui()

    def init_ui(self):
        # 创建主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 创建顶部按钮组
        self.file_browse_btn = QPushButton()
        self.init_sidebar_button(
            self.file_browse_btn, 
            "home", 
            self.on_file_browse_toggled
        )
        
        self.import_btn = QPushButton()
        self.init_sidebar_button(
            self.import_btn, 
            "plus-square", 
            self.on_import_toggled
        )
        
        # 假设在类中已经保存了 HistoryPanel 实例
        if hasattr(self.parent, 'history_panel'):
            self.file_browse_btn.clicked.connect(
                lambda: self.file_browse_btn.setChecked(True))
            self.file_browse_btn.clicked.connect(
                self.parent.history_panel.load_history_items)

        self.import_btn = QPushButton()
        self.import_btn.setIcon(
            QIcon(get_icon_path("plus-square")))  # 需替换为实际图标路径
        self.import_btn.setIconSize(QtCore.QSize(25, 25))
        # 应用统一样式并移除flat属性
        self.import_btn.setStyleSheet(AppStyle().get_sidebar_button_style())
        # 设置按钮可选中
        self.import_btn.setCheckable(True)
        self.import_btn.clicked.connect(self.handle_import)

        # 将顶部按钮添加到布局
        layout.addWidget(self.file_browse_btn)
        layout.addWidget(self.import_btn)

        # 添加弹性空间，使设置按钮位于底部
        layout.addSpacerItem(
            QSpacerItem(
                20,
                40,
                QSizePolicy.Minimum,
                QSizePolicy.Expanding))

        # 创建设置按钮
        self.settings_btn = QPushButton()
        self.settings_btn.setIcon(
            QIcon(get_icon_path("settings")))
        self.settings_btn.setIconSize(QtCore.QSize(25, 25))
        # 应用统一样式并移除flat属性
        self.settings_btn.setStyleSheet(AppStyle().get_sidebar_button_style())
        # 设置按钮可选中
        self.settings_btn.setCheckable(True)

        # 绑定点击事件
        self.settings_btn.clicked.connect(self.show_settings_dialog)
        layout.addWidget(self.settings_btn)

        # 设置布局策略
        self.setLayout(layout)

    def handle_import(self):
        self.import_btn.setChecked(True)
        import_dialog = ImportDialog(
            self,
            self.markdown_manager,
            self.parent.history_panel if self.parent else None)
        import_dialog.exec_()

    def show_settings_dialog(self):
        """显示设置对话框"""
        self.settings_dialog = SettingsDialog(self)
        self.settings_dialog.exec()

    def init_sidebar_button(self, button: QPushButton, icon_name: str, toggle_slot):
        """初始化侧边栏按钮并设置图标切换"""
        # 设置初始图标（默认状态）
        button.setIcon(QIcon(get_icon_path(icon_name)))
        button.setIconSize(QtCore.QSize(25, 25))
        button.setStyleSheet(self.app_style.get_sidebar_button_style())
        button.setCheckable(True)
        button.toggled.connect(lambda checked: toggle_slot(checked, icon_name))

    def update_button_icon(self, button: QPushButton, icon_name: str, is_selected: bool):
        """更新按钮图标（直接切换预定义SVG）"""
        button.setIcon(QIcon(get_icon_path(icon_name, selected=is_selected)))

    def on_file_browse_toggled(self, checked, icon_name="home"):
        self.update_button_icon(self.file_browse_btn, icon_name, checked)
        if checked and hasattr(self.parent, 'history_panel'):
            self.parent.history_panel.load_history_items()

    def on_import_toggled(self, checked, icon_name="plus-square"):
        self.update_button_icon(self.import_btn, icon_name, checked)
        if checked:
            self.handle_import()
