from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QWidget,
    QLabel,
    QLineEdit,
    QFormLayout,
    QPushButton,
    QHBoxLayout,
    QSizePolicy,
    QComboBox,
    QFrame
)
from PySide6.QtCore import Qt
from app.preference import AppStyle

class EditItemDialog(QDialog):
    """
    编辑项目对话框
    """
    def __init__(self, markdown_data, parent=None):
        super().__init__(parent)
        self.app_style = AppStyle()
        self.markdown_data = markdown_data
        self.tags = []
        tags_text = self.markdown_data.get('tags', '')
        if tags_text:
            self.tags = [tag.strip() for tag in tags_text.split(',') if tag.strip()]
        self.setWindowTitle(self.markdown_data.get('title', '查看详情'))
        self.setMinimumSize(640, 480)  # 稍微增大对话框尺寸
        
        # 设置窗口标志，尝试解决macOS上的圆角显示问题
        from PySide6.QtCore import Qt
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        # 使用统一的样式生成器
        from app.preference.style_utils import create_dialog_style
        self.setStyleSheet(create_dialog_style())
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)  # 减少内边距，避免影响圆角显示
        layout.setSpacing(16)  # 统一间距

        # 创建主内容区域，合并原来的编辑和属性内容
        main_content = QWidget()
        # 确保主内容区域无样式干扰，保持纯净背景
        main_content.setStyleSheet("""
            QWidget {
                background-color: transparent;
                border: none;
                border-radius: 0px;
            }
        """)
        main_layout = QVBoxLayout(main_content)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # 添加编辑区域
        self.add_edit_content(main_layout)
        
        # 添加分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        from app.preference.style_constants import NEUTRAL_200
        separator.setStyleSheet(f"border: 1px solid {NEUTRAL_200};")
        main_layout.addWidget(separator)
        
        # 添加属性区域
        self.add_detail_content(main_layout)

        # 优化保存按钮样式 - 使用紧凑设计符合对话框设计规范
        save_button = QPushButton("保存设置")
        # 使用自定义样式覆盖默认的确认按钮样式，减少padding和高度
        from app.preference.style_constants import (
            PRIMARY_500, PRIMARY_600, PRIMARY_700, PRIMARY_900,
            NEUTRAL_0, NEUTRAL_200, NEUTRAL_400,
            RADIUS_SM, FONT_SIZE_MD, SPACING_SM, SPACING_MD
        )
        save_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY_500};
                color: {NEUTRAL_0};
                border: 1px solid {PRIMARY_600};
                border-radius: {RADIUS_SM}px;
                padding: {SPACING_SM}px {SPACING_MD}px;  /* 更紧凑的padding: 8px 12px */
                font-size: {FONT_SIZE_MD}px;
                font-weight: 600;
                min-width: 80px;
                min-height: 24px;  /* 更小的最小高度 */
                max-height: 24px;  /* 限制最大高度 */
                margin-bottom: 8px;  /* 增加底部边距，避免影响对话框圆角 */
            }}
            QPushButton:hover {{
                background-color: {PRIMARY_600};
                border-color: {PRIMARY_700};
            }}
            QPushButton:pressed {{
                background-color: {PRIMARY_700};
                border-color: {PRIMARY_900};
            }}
            QPushButton:disabled {{
                background-color: {NEUTRAL_200};
                color: {NEUTRAL_400};
                border-color: {NEUTRAL_200};
            }}
        """)
        save_button.setAutoDefault(False)  # 防止回车键触发保存，避免tag输入时对话框意外关闭
        save_button.clicked.connect(self.accept)

        layout.addWidget(main_content)
        layout.addWidget(save_button)
        self.setLayout(layout)

    def add_edit_content(self, parent_layout):
        """添加编辑内容区域"""
        # 添加标题
        title_label = QLabel("编辑信息")
        from app.preference.style_constants import NEUTRAL_900, FONT_SIZE_LG
        title_label.setStyleSheet(f"""
            color: {NEUTRAL_900};
            font-size: {FONT_SIZE_LG}px;
            font-weight: 600;
            margin-bottom: 8px;
        """)
        parent_layout.addWidget(title_label)
        
        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(16)  # 统一间距
        form_layout.setLabelAlignment(Qt.AlignTop)  # 标签顶部对齐
        # 优化标题输入框
        self.title_edit = QLineEdit(self.markdown_data.get('title', ''))
        self.title_edit.setMinimumHeight(44)  # 统一高度
        self.title_edit.setMinimumWidth(500)  # 增加宽度
        self.title_edit.setStyleSheet(self.app_style.get_line_edit())
        title_label = self._make_label('标题:')
        form_layout.addRow(title_label, self.title_edit)
        # 优化标签输入框
        tags_label = self._make_label('标签:')
        self.tag_add_edit = QLineEdit()
        self.tag_add_edit.setMinimumHeight(44)
        self.tag_add_edit.setMinimumWidth(500)
        self.tag_add_edit.setStyleSheet(self.app_style.get_line_edit())
        self.tag_add_edit.setPlaceholderText("按回车添加标签")
        # 确保回车键只用于添加标签，不会触发对话框关闭
        self.tag_add_edit.returnPressed.connect(self._add_new_tag)
        form_layout.addRow(tags_label, self.tag_add_edit)

        parent_layout.addLayout(form_layout)

        # 优化标签容器样式 - 移除圆角，保持视觉层次统一
        from app.preference.style_constants import NEUTRAL_200, NEUTRAL_50, SPACING_MD
        self.tags_container = QWidget()
        self.tags_container.setStyleSheet(f'''
            QWidget {{
                border: 1px solid {NEUTRAL_200};
                border-radius: 0px;  /* 移除圆角，与对话框整体设计保持一致 */
                background-color: {NEUTRAL_50};
                padding: {SPACING_MD}px;
            }}
        ''')
        self.tags_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.tags_vertical_layout = QVBoxLayout(self.tags_container)
        self.tags_vertical_layout.setContentsMargins(8, 8, 8, 8)  # 统一内边距
        self.tags_vertical_layout.setSpacing(8)  # 统一间距

        self.tag_layouts = []
        self.tag_widgets = []

        self._create_new_row()
        self._refresh_tags()  # Initialize tags display

        self.tags_vertical_layout.addStretch(1)
        parent_layout.addWidget(self.tags_container)

    def _create_new_row(self):
        new_layout = QHBoxLayout()
        new_layout.setContentsMargins(0, 0, 0, 0)
        new_layout.setSpacing(12)  # 增加标签间间距
        self.tags_vertical_layout.insertLayout(self.tags_vertical_layout.count() - 1, new_layout)
        self.tag_layouts.append(new_layout)
        return new_layout

    def _make_label(self, name):
        from app.preference.style_constants import NEUTRAL_700, FONT_SIZE_MD
        label = QLabel(name)
        label.setStyleSheet(f'''
            border: none;
            background-color: transparent;
            font-weight: 600;
            color: {NEUTRAL_700};
            font-size: {FONT_SIZE_MD}px;
        ''')
        return label

    def _make_info_label(self, text):
        """创建信息显示标签"""
        from app.preference.style_constants import NEUTRAL_600, FONT_SIZE_MD, SPACING_XS
        label = QLabel(text)
        label.setStyleSheet(f'''
            border: none;
            background-color: transparent;
            color: {NEUTRAL_600};
            font-size: {FONT_SIZE_MD}px;
            padding: {SPACING_XS}px 0px;
        ''')
        return label

    def _make_tag_widget(self, tag, with_delete_button=True):
        container = QWidget()
        container.setMinimumHeight(36)  # 统一高度
        container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        # 使用青色系作为用户添加的标签，与列表页面markdown的绿色区分
        from app.preference.style_constants import INFO_500, INFO_600, SPACING_LG, SPACING_SM
        container.setStyleSheet(f'''
            QWidget {{
                background-color: {INFO_500};
                border: 1px solid {INFO_600};
                border-radius: 18px;
            }}
        ''')

        layout = QHBoxLayout(container)
        layout.setContentsMargins(16, 8, 12, 8)  # 增加内边距
        layout.setSpacing(8)

        tag_label = QLabel(tag)
        tag_label.setStyleSheet('''
            color: white;
            background-color: transparent;
            border: none;
            padding: 0px;
            font-weight: 500;
        ''')
        tag_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(tag_label, 1)

        if not with_delete_button:
            return container

        delete_button = QPushButton("×")  # 使用更好的删除符号
        delete_button.setFixedSize(24, 24)
        delete_button.setStyleSheet('''
            QPushButton {
                color: white;
                background-color: rgba(255, 255, 255, 0.2);
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 12px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.4);
            }
        ''')
        delete_button.clicked.connect(lambda: self._remove_tag(tag, container))
        layout.addWidget(delete_button)

        # 计算容器宽度
        text_width = tag_label.fontMetrics().boundingRect(tag).width() + 60  # 增加宽度
        container.setMinimumWidth(text_width)

        return container

    def _make_page_type_widget(self, page_type):
        """创建文件类型标签，使用与列表页面一致的颜色映射"""
        container = QWidget()
        container.setMinimumHeight(36)  # 统一高度
        container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        
        # 导入列表页面的颜色映射，确保一致性
        from app.quickpick.item import QuickPickItemDelegate
        delegate = QuickPickItemDelegate()
        type_color = delegate.tag_color_map.get(page_type.lower(), delegate.default_color)
        
        # 将QColor转换为CSS颜色字符串
        bg_color = f'rgb({type_color.red()}, {type_color.green()}, {type_color.blue()})'
        # 创建稍深的边框颜色（降低亮度）
        border_color = f'rgb({max(0, type_color.red()-20)}, {max(0, type_color.green()-20)}, {max(0, type_color.blue()-20)})'
        
        container.setStyleSheet(f'''
            QWidget {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 18px;
            }}
        ''')

        layout = QHBoxLayout(container)
        layout.setContentsMargins(16, 8, 16, 8)  # 对称内边距，无删除按钮
        layout.setSpacing(8)

        type_label = QLabel(page_type.upper())  # 大写显示文件类型
        type_label.setStyleSheet('''
            color: white;
            background-color: transparent;
            border: none;
            padding: 0px;
            font-weight: 600;
            font-size: 12px;
        ''')
        type_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(type_label, 1)

        # 计算容器宽度
        text_width = type_label.fontMetrics().boundingRect(page_type.upper()).width() + 32
        container.setMinimumWidth(text_width)

        return container

    def _refresh_tags(self):
        """Re-render all tags to ensure consistency"""
        # Clear all existing tag widgets and layouts
        for widget in self.tag_widgets:
            widget.deleteLater()
        for layout in self.tag_layouts:
            while layout.count() > 0:
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            self.tags_vertical_layout.removeItem(layout)
        self.tag_widgets.clear()
        self.tag_layouts.clear()

        # Recreate initial row
        self._create_new_row()

        # Re-add all tags
        for tag in self.tags:
            self._add_tag_to_layout(tag)

        self.tags_container.updateGeometry()
        self.tags_container.repaint()

    def _add_tag_to_layout(self, tag):
        """Add a tag to the layout with proper width management"""
        tag_widget = self._make_tag_widget(tag)
        self.tag_widgets.append(tag_widget)

        if not self.tag_layouts:
            self._create_new_row()

        last_layout = self.tag_layouts[-1]
        total_width = tag_widget.sizeHint().width()
        for i in range(last_layout.count()):
            item = last_layout.itemAt(i)
            widget = item.widget()
            if widget:
                total_width += widget.sizeHint().width() + last_layout.spacing()

        container_width = self.tags_container.width() or (self.width() - 40)

        if total_width <= container_width:
            last_layout.addWidget(tag_widget)
        else:
            new_layout = self._create_new_row()
            new_layout.addWidget(tag_widget)

        self.tags_container.updateGeometry()
        self.tags_container.repaint()

    def _remove_tag(self, tag, widget):
        """Remove a tag and re-render all tags"""
        if tag in self.tags and widget in self.tag_widgets:
            tag_index = self.tags.index(tag)
            self.tags.pop(tag_index)
            self.tag_widgets.pop(tag_index)
            widget.deleteLater()
            self._refresh_tags()  # Re-render all tags to ensure consistency

    def _add_new_tag(self):
        """处理添加新标签，确保不会意外关闭对话框"""
        try:
            tag_text = self.tag_add_edit.text().strip()
            if tag_text and tag_text not in self.tags:
                self.tags.append(tag_text)
                self._refresh_tags()  # Re-render all tags
                self.tag_add_edit.clear()
                # 确保焦点保持在输入框上，方便继续添加标签
                self.tag_add_edit.setFocus()
            elif tag_text in self.tags:
                # 如果标签已存在，清空输入框并显示提示
                self.tag_add_edit.clear()
                self.tag_add_edit.setPlaceholderText("标签已存在，请输入其他标签")
                # 2秒后恢复原始提示
                from PySide6.QtCore import QTimer
                QTimer.singleShot(2000, lambda: self.tag_add_edit.setPlaceholderText("按回车添加标签"))
        except Exception as e:
            # 在发生错误时不应该关闭对话框
            print(f"添加标签时发生错误: {e}")
            self.tag_add_edit.clear()

    def add_detail_content(self, parent_layout):
        """添加详细信息区域"""
        # 添加标题
        detail_title = QLabel("文件属性")
        from app.preference.style_constants import NEUTRAL_900, FONT_SIZE_LG
        detail_title.setStyleSheet(f"""
            color: {NEUTRAL_900};
            font-size: {FONT_SIZE_LG}px;
            font-weight: 600;
            margin-bottom: 8px;
        """)
        parent_layout.addWidget(detail_title)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(16)
        form_layout.setLabelAlignment(Qt.AlignTop)

        # 文件类型显示
        page_type = self.markdown_data.get('page_type', 'markdown')
        if not page_type:
            page_type = 'markdown'
        page_type_label = self._make_page_type_widget(page_type)  # 使用专门的橙色样式
        page_type_layout = QHBoxLayout()
        page_type_layout.addWidget(page_type_label)
        page_type_layout.addStretch()  # 添加弹性空间
        form_layout.addRow(self._make_label("文件类型："), page_type_layout)

        # 创建时间
        create_time = self.markdown_data.get('created_at', '')
        if create_time:
            create_time = create_time.strftime('%Y-%m-%d %H:%M:%S')
        create_time_label = self._make_info_label(create_time)
        form_layout.addRow(self._make_label("创建时间："), create_time_label)

        # 更新时间
        update_time = self.markdown_data.get('updated_at', '')
        if update_time:
            update_time = update_time.strftime('%Y-%m-%d %H:%M:%S')
        update_time_label = self._make_info_label(update_time)
        form_layout.addRow(self._make_label("更新时间："), update_time_label)

        # 文件大小
        file_size = self.markdown_data.get('file_size', '')
        if file_size:
            file_size = f"{file_size:,} bytes"  # 添加千位分隔符
        else:
            file_size = "0 bytes"
        file_size_label = self._make_info_label(file_size)
        form_layout.addRow(self._make_label("文件大小："), file_size_label)

        # MD5值
        content_md5 = self.markdown_data.get('content_md5', '')
        if content_md5:
            content_md5 = f"{content_md5}"
        else:
            content_md5 = "未计算"
        content_md5_label = self._make_info_label(content_md5)
        form_layout.addRow(self._make_label("MD5值："), content_md5_label)

        parent_layout.addLayout(form_layout)
        parent_layout.addStretch()  # 添加弹性空间

    def get_new_title(self):
        return self.title_edit.text()

    def get_new_tags(self):
        return ','.join(self.tags)


