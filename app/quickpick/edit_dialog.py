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
    QFrame,
    QMessageBox,
    QGridLayout
)
from PySide6.QtCore import Qt
from app.preference import AppStyle
from app.preference.style_utils import create_dialog_style, create_button_style
from app.preference.style_constants import (
    NEUTRAL_0, NEUTRAL_50, NEUTRAL_100, NEUTRAL_200, NEUTRAL_300, NEUTRAL_500, NEUTRAL_600, NEUTRAL_700, NEUTRAL_800, NEUTRAL_900,
    DANGER_500, DANGER_600,
    PRIMARY_500, PRIMARY_600, PRIMARY_700, PRIMARY_900,
    INFO_500, INFO_600,
    SPACING_SM, SPACING_MD, SPACING_LG, SPACING_XL, SPACING_XS,
    FONT_SIZE_MD, FONT_SIZE_LG, FONT_SIZE_SM,
    RADIUS_SM, RADIUS_MD, RADIUS_LG, RADIUS_PILL,
    BUTTON_HEIGHT_SM, BUTTON_HEIGHT_MD, BUTTON_HEIGHT_LG
)
from utils.logger_utils import logger
# 导入图标选择器组件
from .icon_selector import IconSelectorWidget
# 导入颜色选择器组件
from .color_selector import ColorSelectorWidget

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
        self.setMinimumSize(720, 560)  # 增大对话框尺寸，提供更好的用户体验
        
        # 设置窗口标志，确保对话框行为正确
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        # 使用统一的样式生成器，确保与应用程序风格一致
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {NEUTRAL_0};
            }}
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # 设置为0，让对话框样式控制整个边界
        layout.setSpacing(0)  # 统一间距

        # 创建主内容区域，合并原来的编辑和属性内容
        main_content = QWidget()
        # 确保主内容区域无样式干扰，保持纯净背景，明确设置无圆角
        main_content.setStyleSheet(f"""
            QWidget {{
                background-color: {NEUTRAL_0};
            }}
        """)
        main_layout = QVBoxLayout(main_content)
        main_layout.setContentsMargins(SPACING_MD, SPACING_MD, SPACING_MD, SPACING_MD)  # 统一内边距
        main_layout.setSpacing(SPACING_MD)  # 增大间距，改善元素分组

        # 添加编辑区域（不含标题）
        self.add_edit_content(main_layout)
        
        # 添加属性区域（不含标题）
        self.add_detail_content(main_layout)

        # 按钮区域布局 - 确保按钮右对齐且有足够的间距
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(SPACING_MD, SPACING_MD, SPACING_MD, SPACING_MD)  # 统一内边距
        button_layout.setSpacing(SPACING_SM)
        
        # 添加弹性空间将按钮推到右侧
        button_layout.addStretch()
        
        # 取消按钮
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
        button_layout.addWidget(cancel_button)
        
        # 保存按钮 - 使用TDesign风格的按钮样式
        save_button = QPushButton("保存")
        save_button.setStyleSheet(f"""
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
            QPushButton:hover {{
                background-color: {PRIMARY_600};
                border-color: {PRIMARY_600};
            }}
        """)
        save_button.setAutoDefault(False)  # 防止回车键触发保存，避免tag输入时对话框意外关闭
        save_button.clicked.connect(self.accept)
        
        button_layout.addWidget(save_button)

        layout.addWidget(main_content)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def add_edit_content(self, parent_layout):
        """添加编辑内容区域"""
        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(SPACING_LG)  # 增加间距，改善表单元素布局
        form_layout.setLabelAlignment(Qt.AlignTop)  # 标签顶部对齐
        
        # 设置表单标签和字段的对齐方式
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        
        # 优化标题输入框
        self.title_edit = QLineEdit(self.markdown_data.get('title', ''))
        self.title_edit.setMinimumHeight(40)  # 统一高度
        self.title_edit.setStyleSheet(self.app_style.get_line_edit())
        title_label = self._make_label('标题')
        form_layout.addRow(title_label, self.title_edit)

        parent_layout.addLayout(form_layout)
        
        # 优化标签输入框（移到标签容器之前）
        tags_label = self._make_label('标签')
        self.tag_add_edit = QLineEdit()
        self.tag_add_edit.setMinimumHeight(40)
        self.tag_add_edit.setStyleSheet(self.app_style.get_line_edit())
        self.tag_add_edit.setPlaceholderText("按回车添加标签")
        # 基本焦点设置
        self.tag_add_edit.setFocusPolicy(Qt.StrongFocus)  # 确保可以通过鼠标和键盘获取焦点
        self.tag_add_edit.setAttribute(Qt.WA_InputMethodEnabled, True)  # 确保输入法正常工作
        self.tag_add_edit.setAttribute(Qt.WA_MacShowFocusRect, True)  # 在Mac上显示焦点矩形
        # 确保回车键只用于添加标签，不会触发对话框关闭或其他控件
        # 移除过度的自定义事件处理，使用Qt的默认行为
        
        # 创建一个水平布局来放置标签和输入框
        tag_input_layout = QHBoxLayout()
        tag_input_layout.setContentsMargins(0, 0, 0, 0)
        tag_input_layout.setSpacing(SPACING_SM)
        tag_input_layout.addWidget(tags_label)
        tag_input_layout.addWidget(self.tag_add_edit)
        parent_layout.addLayout(tag_input_layout)

        # 为输入框安装事件过滤器，确保在初始化之后
        self.title_edit.installEventFilter(self)
        self.tag_add_edit.installEventFilter(self)

        # 优化标签容器样式 - 使用柔和的边框和直角（移除圆角）
        self.tags_container = QWidget()
        self.tags_container.setStyleSheet(f'''
            QWidget {{
                border: 1px solid {NEUTRAL_200};
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
        """创建统一风格的标签"""
        label = QLabel(name)
        label.setStyleSheet(f'''
            border: none;
            background-color: transparent;
            font-weight: 600;
            color: {NEUTRAL_700};
            font-size: {FONT_SIZE_MD}px;
            min-width: 80px;
        ''')
        return label

    def _make_info_label(self, text):
        """创建信息显示标签"""
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
        # 创建一个水平布局的容器
        container = QWidget()
        container.setStyleSheet("background-color: transparent; border: none;")
        
        # 使用 QHBoxLayout 来水平排列标签和删除按钮
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        
        # 创建标签按钮，使用 QPushButton 实现圆角效果
        tag_button = QPushButton(tag)
        tag_button.setStyleSheet(f'''
            QPushButton {{
                background-color: {NEUTRAL_100};
                border: 1px solid {NEUTRAL_200};
                border-radius: 16px;
                color: {NEUTRAL_700};
                padding: 6px 12px;
                font-size: {FONT_SIZE_SM}px;
                font-weight: 500;
                text-align: center;
                min-height: 20px;
            }}
            QPushButton:hover {{
                background-color: {NEUTRAL_200};
            }}
        ''')
        tag_button.setCursor(Qt.PointingHandCursor)
        tag_button.setFocusPolicy(Qt.NoFocus)
        
        # 如果不需要删除按钮，直接返回标签按钮
        if not with_delete_button:
            layout.addWidget(tag_button)
            return container

        # 添加删除按钮
        delete_button = QPushButton("×")
        delete_button.setFixedSize(20, 20)
        delete_button.setStyleSheet(f'''
            QPushButton {{
                color: {NEUTRAL_600};
                background-color: transparent;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 10px;
                padding: 0px;
                text-align: center;
            }}
            QPushButton:hover {{
                color: {NEUTRAL_900};
                background-color: {NEUTRAL_200};
            }}
            QPushButton:pressed {{
                background-color: {NEUTRAL_300};
            }}
        ''')
        delete_button.clicked.connect(lambda: self._remove_tag(tag, container))
        delete_button.setCursor(Qt.PointingHandCursor)
        delete_button.setFocusPolicy(Qt.NoFocus)
        
        # 添加到布局中
        layout.addWidget(tag_button)
        layout.addWidget(delete_button)
        
        # 设置容器的最小宽度
        text_width = tag_button.fontMetrics().boundingRect(tag).width() + 60
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
    
    def eventFilter(self, source, event):
        """事件过滤器，拦截标题和标签输入框的回车事件并阻止其传播"""
        # 处理标签输入框的回车事件
        if hasattr(self, 'tag_add_edit') and source == self.tag_add_edit:
            if event.type() == event.Type.KeyPress and (event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter):
                self._add_new_tag()
                return True
        # 处理标题输入框的回车事件，防止触发图标选择对话框
        elif hasattr(self, 'title_edit') and source == self.title_edit:
            if event.type() == event.Type.KeyPress and (event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter):
                # 明确接受此事件，阻止其继续传播
                return True
        # 其他事件让其正常传播
        return super().eventFilter(source, event)
        
    # 移除所有过度的自定义事件处理方法，让Qt使用默认行为

    def add_detail_content(self, parent_layout):
        """添加详细信息区域"""
        # 使用网格布局实现两列显示
        grid_layout = QGridLayout()
        grid_layout.setSpacing(SPACING_LG)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setVerticalSpacing(SPACING_LG)
        grid_layout.setHorizontalSpacing(SPACING_LG)

        # 文件类型编辑 - 设为只读
        page_type = self.markdown_data.get('page_type', 'markdown')
        if not page_type:
            page_type = 'markdown'
        self.page_type_edit = QLineEdit(page_type)
        self.page_type_edit.setReadOnly(True)
        self.page_type_edit.setMinimumHeight(40)
        self.page_type_edit.setStyleSheet(self.app_style.get_line_edit() + "background-color: " + NEUTRAL_100 + ";")
        
        # 文件大小
        file_size = self.markdown_data.get('file_size', '')
        if file_size:
            file_size = f"{file_size:,} bytes"  # 添加千位分隔符
        else:
            file_size = "0 bytes"
        file_size_label = self._make_info_label(file_size)
        
        # 第一行：文件类型和文件大小
        grid_layout.addWidget(self._make_label("文件类型"), 0, 0)
        grid_layout.addWidget(self.page_type_edit, 0, 1)
        grid_layout.addWidget(self._make_label("文件大小"), 0, 2)
        grid_layout.addWidget(file_size_label, 0, 3)

        # 图标和颜色选择器 - 合并为一行
        icon_type = self.markdown_data.get('icon_type', '')
        icon_path = self.markdown_data.get('icon_path', '')
        icon_color = self.markdown_data.get('icon_color', '')
        # 优先使用icon_path中的图标名称
        current_icon = None
        if icon_path and icon_path.startswith('icons/') and icon_path.endswith('.svg'):
            current_icon = icon_path[6:-4]  # 移除 'icons/' 前缀和 '.svg' 后缀
        elif icon_type:
            current_icon = icon_type
            
        # 图标选择器 - 设置为可点击弹出
        self.icon_selector = IconSelectorWidget(current_icon)
        self.icon_selector.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.icon_selector.setMinimumHeight(40)
        self.icon_selector.setCursor(Qt.PointingHandCursor)  # 鼠标悬停显示手型
        
        # 颜色选择器 - 设置为可点击弹出
        self.icon_color_selector = ColorSelectorWidget(icon_color)
        self.icon_color_selector.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.icon_color_selector.setMinimumHeight(40)
        self.icon_color_selector.setCursor(Qt.PointingHandCursor)  # 鼠标悬停显示手型
        
        # 第二行：图标和图标颜色
        grid_layout.addWidget(self._make_label("图标"), 1, 0)
        grid_layout.addWidget(self.icon_selector, 1, 1)
        grid_layout.addWidget(self._make_label("图标颜色"), 1, 2)
        grid_layout.addWidget(self.icon_color_selector, 1, 3)

        # 创建时间和更新时间 - 合并为一行
        create_time = self.markdown_data.get('created_at', '')
        if create_time and not isinstance(create_time, str):
            create_time = create_time.strftime('%Y-%m-%d %H:%M:%S')
        create_time_label = self._make_info_label(str(create_time))
        
        update_time = self.markdown_data.get('updated_at', '')
        if update_time and not isinstance(update_time, str):
            update_time = update_time.strftime('%Y-%m-%d %H:%M:%S')
        update_time_label = self._make_info_label(str(update_time))
        
        # 第三行：创建时间和更新时间
        grid_layout.addWidget(self._make_label("创建时间"), 2, 0)
        grid_layout.addWidget(create_time_label, 2, 1)
        grid_layout.addWidget(self._make_label("更新时间"), 2, 2)
        grid_layout.addWidget(update_time_label, 2, 3)

        # 设置网格布局列的拉伸因子，使布局更均衡
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 2)
        grid_layout.setColumnStretch(2, 1)
        grid_layout.setColumnStretch(3, 2)

        parent_layout.addLayout(grid_layout)
        parent_layout.addStretch()  # 添加弹性空间

    def get_new_title(self):
        # 确保返回非空字符串，避免保存空标题
        title = self.title_edit.text()
        logger.info(f"获取新标题: '{title}'")
        return title

    def get_new_tags(self):
        # 确保返回格式化的标签字符串
        tags_str = ','.join(self.tags)
        logger.info(f"获取新标签: '{tags_str}', 标签列表: {self.tags}")
        return tags_str

    def get_new_page_type(self):
        return self.page_type_edit.text()

    def get_new_icon_type(self):
        # 图标类型现在通过图标选择器设置，返回None表示使用图标路径
        return None

    def get_new_display_name(self):
        # 不再使用显示名称字段，返回None
        return None

    def get_new_icon_path(self):
        # 从图标选择器获取选中的图标，并构造图标路径
        selected_icon = self.icon_selector.get_selected_icon()
        if selected_icon:
            return f"icons/{selected_icon}.svg"
        return None

    def get_new_icon_color(self):
        return self.icon_color_selector.get_selected_color()


class DeleteConfirmDialog(QDialog):
    """
    自定义删除确认对话框
    符合整体设计规范的删除确认弹窗
    """
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.app_style = AppStyle()
        self.setWindowTitle("确认删除")
        # 设置更合适的尺寸，确保内容完整显示
        self.setFixedSize(440, 220)
        
        # 设置窗口标志，确保对话框行为正确
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        # 使用统一的样式生成器，确保与应用程序风格一致
        self.setStyleSheet(create_dialog_style())
        
        self.init_ui(title)
    
    def init_ui(self, title):
        # 主布局
        layout = QVBoxLayout()
        # 调整内边距，确保与设计规范一致
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)
        
        # 标题标签 - 符合TDesign的标题风格
        title_label = QLabel()
        title_label.setStyleSheet(f"""
            font-size: {FONT_SIZE_LG}px;
            color: {NEUTRAL_900};
            font-weight: 600;
            margin-bottom: 8px;
        """)
        title_label.setText("确认删除")
        layout.addWidget(title_label)
        
        # 提示信息 - 符合TDesign的提示文本风格
        message_label = QLabel()
        message_label.setStyleSheet(f"""
            font-size: {FONT_SIZE_MD}px;
            color: {NEUTRAL_700};
            line-height: 20px;
            margin-bottom: 16px;
        """)
        message_label.setText(f"确定要删除文件「{title}」吗？\n此操作不可撤销，删除后数据将无法恢复。")
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(message_label)
        
        # 按钮区域布局 - 更紧凑的按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(SPACING_MD)
        button_layout.addStretch()
        
        # 取消按钮 - 使用TDesign小型按钮样式
        cancel_button = QPushButton("取消")
        # 使用更紧凑的按钮尺寸
        cancel_button.setStyleSheet(create_button_style("secondary", "sm"))
        cancel_button.setFixedWidth(80)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        # 删除按钮（危险操作） - 使用TDesign小型危险按钮样式
        delete_button = QPushButton("删除")
        # 使用更紧凑的按钮尺寸
        delete_button.setStyleSheet(create_button_style("danger", "sm"))
        delete_button.setFixedWidth(80)
        delete_button.clicked.connect(self.accept)
        button_layout.addWidget(delete_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
