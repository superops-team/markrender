import time
import os

from markitdown import MarkItDown
from PySide6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QDialog,
    QLabel,
    QProgressBar,
    QFrame,
    QHBoxLayout,
)
from PySide6.QtGui import QFont, QKeySequence, QGuiApplication
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtSvgWidgets import QSvgWidget
from utils import logger, time_utils, supported_formats
from db.settings_manager import SettingsManager
from app.preference import AppStyle
from app.preference.style_utils import (
    create_dialog_style,
    create_button_style,
    primary_button,
    secondary_button,
)
from app.preference.style_constants import (
    PRIMARY_500,
    NEUTRAL_100,
    NEUTRAL_200,
    NEUTRAL_500,
    NEUTRAL_700,
    SPACING_MD,
    SPACING_LG,
    SPACING_XL,
    RADIUS_SM,
    FONT_SIZE_LG,
    FONT_SIZE_MD,
    FONT_SIZE_SM,
)


class ImportDialog(QDialog):
    def __init__(self, parent, markrender_manager, quickpick_panel):
        super().__init__(parent)
        self.markrender_manager = markrender_manager
        self.parent = parent
        self.quickpick_panel = quickpick_panel
        self.init_ui()
        # 监听键盘事件以处理粘贴操作
        self.setFocusPolicy(Qt.StrongFocus)
        self.import_settings = SettingsManager().get_settings_dict('import') # 导入导出设置


    def init_ui(self):
        # 应用统一的对话框样式
        self.setStyleSheet(create_dialog_style())
        self.setWindowTitle("文件导入")
        self.setFixedSize(500, 300)  # 调整高度以保持宽高比一致性
        
        dialog_layout = QVBoxLayout(self)
        dialog_layout.setContentsMargins(24, 24, 24, 24)  # 优化边距
        dialog_layout.setSpacing(16)

        # 创建导入区域（不带虚线框的纯内容区域）
        content_widget = QFrame(self)
        content_widget.setFixedSize(452, 120)  # 调整尺寸
        content_widget.setStyleSheet(f"""
            QFrame {{
                background-color: transparent;
                border: none;
            }}
        """)
        
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignCenter)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(12)

        # 创建遮罩层和加载状态标签，初始状态隐藏
        self.overlay = QFrame(content_widget)
        self.overlay.setStyleSheet(self.get_overlay_style())
        self.overlay.setGeometry(0, 0, 452, 120)
        self.overlay.hide()

        self.loading_label = QLabel("任务支持后台处理，可关闭此窗口，后台处理中...", self.overlay)
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet(self.get_loading_label_style())
        self.loading_label.setGeometry(0, 0, 452, 120)
        self.loading_label.hide()

        # 创建垂直布局用于容纳图标和文字
        text_content_layout = QVBoxLayout()
        text_content_layout.setAlignment(Qt.AlignCenter)
        text_content_layout.setSpacing(8)

        # 上传图标（使用SVG图标）
        self.icon_label = QSvgWidget()
        self.icon_label.load(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "icons", "upload.svg"))
        self.icon_label.setFixedSize(48, 48)
        text_content_layout.addWidget(self.icon_label, 0, Qt.AlignCenter)

        # 导入区域文字提示（不带虚线框）
        self.import_label = QLabel("点击导入文件", self)
        font = QFont()
        font.setPointSize(16)  # 增大字体以提高可读性
        font.setBold(True)
        self.import_label.setFont(font)
        self.import_label.setAlignment(Qt.AlignCenter)
        self.import_label.setStyleSheet(f"""
            QLabel {{
                color: {NEUTRAL_700};
                font-weight: 600;
                background-color: transparent;
                border: none;
                padding: 10px;
            }}
        """)
        text_content_layout.addWidget(self.import_label)

        content_layout.addLayout(text_content_layout)

        self.format_label = QLabel(f"支持格式: {', '.join(supported_formats)}", self)
        self.format_label.setAlignment(Qt.AlignCenter)
        self.format_label.setStyleSheet(f"""
            QLabel {{
                color: {NEUTRAL_500};
                font-size: {FONT_SIZE_SM}px;
                background-color: transparent;
                border: none;
            }}
        """)
        content_layout.addWidget(self.format_label)

        dialog_layout.addWidget(content_widget, 0, Qt.AlignCenter)

        # 进度条
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.hide()
        self.progress_bar.setStyleSheet(self.get_progress_bar_style())
        dialog_layout.addWidget(self.progress_bar)

        # 文件信息标签
        self.info_label = QLabel(self)
        self.info_label.hide()
        self.info_label.setStyleSheet(self.get_info_label_style())
        dialog_layout.addWidget(self.info_label)

        # 按钮区域 - 使用水平布局保持对齐
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(12)
        
        # 关闭按钮 - 使用统一的次要按钮样式
        self.close_button = QPushButton("关闭", self)
        self.close_button.hide()
        self.close_button.setStyleSheet(secondary_button())  # 使用统一的次要按钮样式
        self.close_button.clicked.connect(self.close)
        self.close_button.setMinimumWidth(80)
        
        # 添加弹性空间实现右对齐
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)
        
        dialog_layout.addLayout(button_layout)

        # 为内容区域添加点击事件
        content_widget.mousePressEvent = self.perform_import

    def get_import_area_style(self):
        """获取导入区域样式"""
        return f"""
        QFrame {{
            border: 2px dashed {PRIMARY_500};
            background-color: {NEUTRAL_100};
            border-radius: {RADIUS_SM}px;
        }}
        QFrame:hover {{
            border-color: {PRIMARY_500};
            background-color: {NEUTRAL_200};
        }}
        """

    def get_overlay_style(self):
        """获取遮罩层样式"""
        return """
        QFrame {
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 4px;
        }
        """

    def get_loading_label_style(self):
        """获取加载标签样式"""
        return f"""
        QLabel {{
            font-size: {FONT_SIZE_MD}px;
            color: {PRIMARY_500};
            font-weight: 500;
        }}
        """

    def get_progress_bar_style(self):
        """获取进度条样式"""
        return f"""
        QProgressBar {{
            border-radius: {RADIUS_SM}px;
            text-align: center;
            height: 12px;
            background-color: {NEUTRAL_200};
        }}
        QProgressBar::chunk {{
            background-color: {PRIMARY_500};
            border-radius: {RADIUS_SM}px;
        }}
        """

    def get_info_label_style(self):
        """获取信息标签样式"""
        return f"""
        QLabel {{
            color: {PRIMARY_500};
            font-size: {FONT_SIZE_SM}px;
            font-weight: 500;
            text-align: center;
        }}
        """

    def keyPressEvent(self, event):
        """监听键盘事件，处理粘贴操作"""
        if event.matches(QKeySequence.Paste):
            self.handle_paste_image()
        super().keyPressEvent(event)

    def handle_paste_image(self):
        """处理剪贴板中的图片并上传"""
        clipboard = QGuiApplication.clipboard()
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
        # 禁用内容区域而不是导入区域
        content_widget = self.layout().itemAt(0).widget()  # 获取内容区域
        if content_widget:
            content_widget.setEnabled(False)
        self.progress_bar.show()
        self.info_label.show()
        self.progress_bar.setValue(0)
        # 显示遮罩层和加载状态标签
        self.overlay.show()
        self.loading_label.show()
        # 将遮罩层置于最上层
        self.overlay.raise_()
         # 创建并启动导入线程
        self.import_thread = ImportThread(
            file_path, self.markrender_manager, self.quickpick_panel)
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
        # 重新启用内容区域
        content_widget = self.layout().itemAt(0).widget()
        if content_widget:
            content_widget.setEnabled(True)

    def import_error(self, error_msg):
        QMessageBox.warning(self, "导入失败", error_msg)
        # 隐藏遮罩层和加载状态标签
        self.overlay.hide()
        self.loading_label.hide()
        # 重新启用内容区域
        content_widget = self.layout().itemAt(0).widget()
        if content_widget:
            content_widget.setEnabled(True)
        self.close()


class ImportThread(QThread):
    progress_updated = Signal(int)
    finished = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, file_path, markrender_manager, quickpick_panel):
        super().__init__()
        self.file_path = file_path
        self.file_name = os.path.basename(self.file_path)
        self.markrender_manager = markrender_manager
        self.quickpick_panel = quickpick_panel
        self.import_settings = SettingsManager().get_settings_dict('import') # 导入导出设置
        self.file_size = os.path.getsize(file_path)
        self.file_ext = os.path.splitext(file_path)[1][1:]
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
            last_id = self.markrender_manager.save_item(
                title=title,
                tags=self.file_ext, 
                file_path=self.file_path, 
                converter=self.converter, 
                converter_start=self.converter_start,
                status='processing',
                page_type='markdown',
            )
            # step2: 转换格式
            logger.debug(f"开始转换格式！文件格式: {self.file_ext} 文件大小: {size_str}")
            md_content = self.convert()
            self.progress_updated.emit(50)
            self.converter_end = time_utils.now()
            # step3: 写入数据
            self.markrender_manager.save_item(
                id=last_id,
                content=md_content, 
                converter=self.converter,
                converter_start=self.converter_start,
                converter_end=self.converter_end,
                status='processed',
                page_type='markdown',
            )
            logger.debug(
                f"写入数据！文件格式: {self.file_ext} 文件大小: {size_str} 转换器：{self.converter}")
            self.progress_updated.emit(75)
            # step4: 刷新quickpick记录
            self.quickpick_panel.load_quickpick_items()
            process_time = time_utils.get_duration(self.converter_start, self.converter_end).total_seconds()
            info_text = f"导入成功！\n处理时长: {
                process_time:.2f} 秒\n文件格式: {
                self.file_ext}\n文件大小: {size_str}"
            self.finished.emit(info_text)
            self.progress_updated.emit(100)
        except Exception as e:
            self.error_occurred.emit(f"导入文件时出错: {str(e)}")

    def convert(self):
        return self.convert_by_markitdown()

    def convert_by_markitdown(self):
        """
        use markitdown to parse pdf or img
        """
        self.converter = 'markitdown'
        md = MarkItDown()
        result = md.convert(self.file_path)
        return result.text_content