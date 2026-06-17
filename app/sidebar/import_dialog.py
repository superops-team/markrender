import time
import os

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
    secondary_button,
    primary_button,
    create_button_style,
)
from app.preference.style_constants import (
    PRIMARY_50,
    PRIMARY_300,
    PRIMARY_500,
    PRIMARY_600,
    NEUTRAL_0,
    NEUTRAL_50,
    NEUTRAL_100,
    NEUTRAL_200,
    NEUTRAL_300,
    NEUTRAL_400,
    NEUTRAL_500,
    NEUTRAL_700,
    SUCCESS_500,
    RADIUS_SM,
    RADIUS_MD,
    FONT_SIZE_MD,
    FONT_SIZE_SM,
    SPACING_SM,
    SPACING_MD,
    SPACING_LG,
    SPACING_XL,
)


class ImportDialog(QDialog):
    def __init__(self, parent, markrender_manager, quickpick_panel):
        super().__init__(parent)
        self.markrender_manager = markrender_manager
        self.parent = parent
        self.quickpick_panel = quickpick_panel
        self.init_ui()
        # 监听键盘事件以处理粘贴操作

        self.import_settings = SettingsManager().get_settings_dict('import') # 导入导出设置


    def init_ui(self):
        # 应用与EditItemDialog一致的对话框样式
        self.setWindowTitle("文件导入")
        self.setMinimumSize(520, 400)  # 适当调整最小尺寸
        
        # 对话框样式与EditItemDialog保持一致
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {NEUTRAL_0};
            }}
        """)
        
        # 主布局 - 与EditItemDialog保持一致的边距和间距
        dialog_layout = QVBoxLayout(self)
        dialog_layout.setContentsMargins(SPACING_MD, SPACING_MD, SPACING_MD, SPACING_MD)  # 与EditItemDialog一致
        dialog_layout.setSpacing(SPACING_MD)  # 与EditItemDialog一致

        # 创建导入区域 - 优化样式使其更现代
        content_widget = QFrame(self)
        content_widget.setMinimumHeight(200)  # 使用最小高度而不是固定尺寸
        content_widget.setStyleSheet(f"""
            QFrame {{
                background-color: {NEUTRAL_50};
                border: 2px dashed {PRIMARY_300};
                border-radius: {RADIUS_MD}px;
            }}
            QFrame:hover {{
                background-color: {PRIMARY_50};
                border-color: {PRIMARY_500};
            }}
            QFrame:disabled {{
                border-color: {NEUTRAL_300};
                background-color: {NEUTRAL_50};
            }}
        """)
        
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(SPACING_MD)

        # 创建遮罩层和加载状态标签，初始状态隐藏
        self.overlay = QFrame(content_widget)
        # 移除遮罩层的圆角
        self.overlay.setStyleSheet(f"""
        QFrame {{
            background-color: {NEUTRAL_0};
        }}
        """)
        self.overlay.setGeometry(0, 0, 472, 160)
        self.overlay.hide()

        self.loading_label = QLabel("任务支持后台处理，可关闭此窗口，后台处理中...", self.overlay)
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_label.setStyleSheet(self.get_loading_label_style())
        self.loading_label.setGeometry(0, 0, 472, 160)
        self.loading_label.hide()

        # 创建垂直布局用于容纳图标和文字
        text_content_layout = QVBoxLayout()
        text_content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_content_layout.setSpacing(SPACING_SM)

        # 上传图标（使用SVG图标）
        self.icon_label = QSvgWidget()
        self.icon_label.load(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "icons", "upload.svg"))
        self.icon_label.setFixedSize(56, 56)
        text_content_layout.addWidget(self.icon_label, 0, Qt.AlignmentFlag.AlignCenter)

        # 导入区域文字提示（参考history面板样式）
        self.import_label = QLabel("点击导入文件", self)
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.import_label.setFont(font)
        self.import_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.import_label.setStyleSheet(f"""
            QLabel {{
                color: {NEUTRAL_700};
                font-weight: 600;
                background-color: transparent;
                border: none;
                padding: {SPACING_SM}px;
            }}
        """)
        text_content_layout.addWidget(self.import_label)

        content_layout.addLayout(text_content_layout)

        self.format_label = QLabel(f"支持格式: {', '.join(supported_formats)}", self)
        self.format_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.format_label.setStyleSheet(f"""
            QLabel {{
                color: {NEUTRAL_500};
                font-size: {FONT_SIZE_SM}px;
                background-color: transparent;
                border: none;
            }}
        """)
        content_layout.addWidget(self.format_label)

        dialog_layout.addWidget(content_widget, 0, Qt.AlignmentFlag.AlignCenter)

        # 文件信息标签
        self.info_label = QLabel(self)
        self.info_label.hide()
        self.info_label.setStyleSheet(self.get_info_label_style())
        dialog_layout.addWidget(self.info_label)

        # 进度条 - 移到按钮上方，符合TDesign设计规范
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.hide()
        # 隐藏进度条文本，使用更现代的样式
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(self.get_progress_bar_style())
        self.progress_bar.setFixedHeight(6)
        # 添加适当的边距
        progress_layout = QHBoxLayout()
        progress_layout.setContentsMargins(SPACING_MD, SPACING_SM, SPACING_MD, 0)
        progress_layout.addWidget(self.progress_bar)
        dialog_layout.addLayout(progress_layout)

        # 为内容区域添加点击事件
        content_widget.mousePressEvent = self.perform_import
        # 监听键盘事件以处理粘贴操作
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        
        # 添加标准的底部按钮区域，与EditItemDialog保持一致
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(SPACING_MD, SPACING_MD, SPACING_MD, SPACING_MD)
        button_layout.setSpacing(SPACING_SM)
        
        # 添加弹性空间将按钮推到右侧
        button_layout.addStretch()
        
        # 取消按钮 - 与EditItemDialog完全一致的样式
        cancel_button = QPushButton("取消")
        cancel_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {NEUTRAL_50};
                color: {NEUTRAL_700};
                border: 1px solid {NEUTRAL_100};
                border-radius: {RADIUS_MD}px;
                padding: {SPACING_SM}px {SPACING_MD}px;
                font-size: {FONT_SIZE_MD}px;
                font-weight: 500;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {NEUTRAL_100};
            }}
        """)
        cancel_button.clicked.connect(self.reject)
        
        # 导入按钮 - 与EditItemDialog的保存按钮样式一致
        self.import_button = QPushButton("导入文件")
        self.import_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY_500};
                color: {NEUTRAL_0};
                border: 1px solid {PRIMARY_500};
                border-radius: {RADIUS_MD}px;
                padding: {SPACING_SM}px {SPACING_MD}px;
                font-size: {FONT_SIZE_MD}px;
                font-weight: 500;
                min-width: 80px;
            }}
            QPushButton:hover:enabled {{
                background-color: {PRIMARY_600};
                border-color: {PRIMARY_600};
            }}
            QPushButton:disabled {{
                background-color: {NEUTRAL_200};
                color: {NEUTRAL_400};
                border-color: {NEUTRAL_300};
                font-weight: normal;
            }}
        """)
        self.import_button.setAutoDefault(False)
        self.import_button.setDefault(True)
        self.import_button.clicked.connect(self.perform_import)
        
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(self.import_button)
        
        dialog_layout.addLayout(button_layout)

    def get_import_area_style(self):
        """获取导入区域样式"""
        return f"""
        QFrame {{
            border: 2px dashed {PRIMARY_500};
            background-color: {NEUTRAL_100};
            # 移除 border-radius 属性以避免内部圆角
        }}
        QFrame:hover {{
            border-color: {PRIMARY_500};
            background-color: {NEUTRAL_200};
        }}
        """

    def get_overlay_style(self):
        """获取遮罩层样式"""
        return f"""
        QFrame {{
            background-color: {NEUTRAL_0};
            # 移除 border-radius 属性以避免内部圆角
        }}
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
        """获取进度条样式 - 符合TDesign设计规范"""
        return f"""
        QProgressBar {{
            border-radius: {RADIUS_SM}px;
            background-color: {NEUTRAL_200};
            border: none;
            padding: 0px;
        }}
        QProgressBar::chunk {{
            background-color: {PRIMARY_500};
            border-radius: {RADIUS_SM}px;
            transition: width 0.2s ease-in-out;
        }}
        """

    def get_info_label_style(self):
        """获取信息标签样式 - 优化为更现代的设计"""
        return f"""
        QLabel {{
            color: {NEUTRAL_700};
            font-size: {FONT_SIZE_MD}px;
            font-weight: 500;
            text-align: center;
            padding: {SPACING_SM}px;
            background-color: {NEUTRAL_50};
            border-radius: {RADIUS_SM}px;
        }}
        """

    def keyPressEvent(self, event):
        """监听键盘事件，处理粘贴操作"""
        if event.matches(QKeySequence.StandardKey.Paste):
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
        # 禁用内容区域和导入按钮
        layout = self.layout()
        if layout is not None:
            content_item = layout.itemAt(0)
            if content_item is not None:
                content_widget = content_item.widget()
                if content_widget is not None:
                    content_widget.setEnabled(False)
        
        # 禁用导入按钮防止重复点击
        if hasattr(self, 'import_button'):
            self.import_button.setEnabled(False)
            self.import_button.setText("导入中...")
        
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
        
        # 更新导入按钮状态为成功
        if hasattr(self, 'import_button'):
            self.import_button.setEnabled(False)
            self.import_button.setText("导入成功")
            # 添加成功状态样式
            self.import_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {SUCCESS_500};
                    color: {NEUTRAL_0};
                    border: 1px solid {SUCCESS_500};
                    border-radius: {RADIUS_MD}px;
                    padding: {SPACING_SM}px {SPACING_MD}px;
                    font-size: {FONT_SIZE_MD}px;
                    font-weight: 500;
                    min-width: 80px;
                }}
                QPushButton:disabled {{
                    background-color: {SUCCESS_500};
                    color: {NEUTRAL_0};
                    border-color: {SUCCESS_500};
                    opacity: 0.9;
                }}
            """)
        
        # 使用 QTimer 延迟关闭对话框，给用户查看结果的时间
        from PySide6.QtCore import QTimer
        QTimer.singleShot(2000, self.close)  # 2秒后自动关闭对话框
        # 隐藏遮罩层和加载状态标签
        self.overlay.hide()
        self.loading_label.hide()
        # 重新启用内容区域
        layout = self.layout()
        if layout is not None:
            content_item = layout.itemAt(0)
            if content_item is not None:
                content_widget = content_item.widget()
                if content_widget is not None:
                    content_widget.setEnabled(True)

    def import_error(self, error_msg):
        # 恢复导入按钮状态
        if hasattr(self, 'import_button'):
            self.import_button.setEnabled(True)
            self.import_button.setText("导入文件")
            # 恢复原始样式
            self.import_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {PRIMARY_500};
                    color: {NEUTRAL_0};
                    border: 1px solid {PRIMARY_500};
                    border-radius: {RADIUS_MD}px;
                    padding: {SPACING_SM}px {SPACING_MD}px;
                    font-size: {FONT_SIZE_MD}px;
                    font-weight: 500;
                    min-width: 80px;
                }}
                QPushButton:hover:enabled {{
                    background-color: {PRIMARY_600};
                    border-color: {PRIMARY_600};
                }}
                QPushButton:disabled {{
                    background-color: {NEUTRAL_200};
                    color: {NEUTRAL_400};
                    border-color: {NEUTRAL_300};
                    font-weight: normal;
                }}
            """)
        
        QMessageBox.warning(self, "导入失败", error_msg)
        # 隐藏遮罩层和加载状态标签
        self.overlay.hide()
        self.loading_label.hide()
        # 重新启用内容区域
        layout = self.layout()
        if layout is not None:
            content_item = layout.itemAt(0)
            if content_item is not None:
                content_widget = content_item.widget()
                if content_widget is not None:
                    content_widget.setEnabled(True)


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
            size_str = f'{size_kb:.2f} KB' if size_kb < 1024 else f'{size_kb / 1024:.2f} MB'
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
            info_text = f"导入成功！\n处理时长: {process_time:.2f} 秒\n文件格式: {self.file_ext}\n文件大小: {size_str}"
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
        from markitdown import MarkItDown

        self.converter = 'markitdown'
        md = MarkItDown()
        result = md.convert(self.file_path)
        return result.text_content
