from PySide6.QtWidgets import (
    QDialog, 
    QTabWidget, 
    QVBoxLayout, 
    QWidget, 
    QLabel, 
    QCheckBox, 
    QSpinBox, 
    QLineEdit, 
    QFormLayout, 
    QPushButton,
    QRadioButton, 
    QButtonGroup,
    QHBoxLayout,
    QFrame,
    QGroupBox,
    QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from typing import Optional
from db.settings_manager import SettingsManager
from app.preference import AppStyle
from app.preference.style_utils import (
    create_dialog_style, 
    create_input_style, 
    create_button_style,
    primary_button
)
from app.preference.style_constants import (
    NEUTRAL_0, NEUTRAL_50, NEUTRAL_100, NEUTRAL_200, NEUTRAL_300, NEUTRAL_400, NEUTRAL_500, NEUTRAL_600, NEUTRAL_700, NEUTRAL_900,
    PRIMARY_50, PRIMARY_100, PRIMARY_200, PRIMARY_300, PRIMARY_500, PRIMARY_600,
    SPACING_XS, SPACING_SM, SPACING_MD, SPACING_LG, SPACING_XL, SPACING_2XL,
    RADIUS_SM, RADIUS_MD, RADIUS_LG,
    FONT_SIZE_SM, FONT_SIZE_MD, FONT_SIZE_LG, FONT_SIZE_XL,
    LINE_HEIGHT_NORMAL
) 

class SettingsDialog(QDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("软件设置")
        self.setMinimumSize(680, 520)  # 优化尺寸以适应新的布局
        self.setMaximumSize(800, 600)  # 限制最大尺寸保持紧凑
        
        # 设置窗口属性和样式
        from PySide6.QtCore import Qt
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)
        self.setStyleSheet(create_dialog_style())
        
        # 加载设置数据
        self.theme_settings = SettingsManager().get_settings_dict('theme')
        self.editor_settings = SettingsManager().get_settings_dict('editor')
        self.general_settings = SettingsManager().get_settings_dict('general')
        self.import_settings = SettingsManager().get_settings_dict('import')
        
        # 控件引用 - 添加类型注解
        self.auto_save_checkbox: Optional[QCheckBox] = None
        self.auto_save_interval: Optional[QSpinBox] = None
        self.font_size_spin: Optional[QSpinBox] = None
        self.font_family_edit: Optional[QLineEdit] = None
        self.dark_mode_checkbox: Optional[QCheckBox] = None
        self.theme_edit: Optional[QLineEdit] = None
        self.import_size: Optional[QSpinBox] = None
        self.pdf_import_group: Optional[QButtonGroup] = None
        # 搜索设置控件引用
        self.search_sort_group: Optional[QButtonGroup] = None
        
        self.init_ui()

    def init_ui(self):
        """初始化UI - 基于Robin Williams四大设计原则优化"""
        # 主布局 - 使用合理的边距（对齐原则）
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(SPACING_2XL, SPACING_LG, SPACING_2XL, SPACING_XL)  # 减少顶部边距
        main_layout.setSpacing(SPACING_LG)
        
        # 创建和配置Tab控件（重复原则）
        self.tab_widget = QTabWidget()
        self._configure_tab_widget()
        
        # 添加各个设置页面（亲密性原则）
        self.add_general_tab()
        self.add_editor_tab()
        self.add_appearance_tab()
        self.add_import_export_tab()
        
        main_layout.addWidget(self.tab_widget)
        
        # 按钮区域（对齐原则）
        self._add_button_area(main_layout)
        
        self.setLayout(main_layout)

    def add_general_tab(self):
        """添加通用设置 tab - 应用亲密性和对齐原则"""
        general_tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(SPACING_XL, SPACING_LG, SPACING_XL, SPACING_LG)
        layout.setSpacing(SPACING_LG)
        
        # 自动保存设置组（亲密性原则）
        auto_save_group = self._create_group_box("自动保存设置")
        auto_save_layout = QVBoxLayout()
        auto_save_layout.setSpacing(SPACING_MD)
        
        # 自动保存复选框
        self.auto_save_checkbox = QCheckBox("启用自动保存")
        self.auto_save_checkbox.setChecked(self.general_settings.get('auto_save', False))
        self.auto_save_checkbox.setStyleSheet(self._get_checkbox_style())
        auto_save_layout.addWidget(self.auto_save_checkbox)
        
        # 自动保存间隔设置（对齐原则）
        interval_container = QHBoxLayout()
        interval_label = QLabel("保存间隔：")
        interval_label.setStyleSheet(self._get_label_style())
        
        self.auto_save_interval = QSpinBox()
        self.auto_save_interval.setRange(1, 60)
        self.auto_save_interval.setValue(self.general_settings.get('auto_save_interval', 5))
        self.auto_save_interval.setSuffix(" 秒")
        self.auto_save_interval.setStyleSheet(self._get_spinbox_style())
        self.auto_save_interval.setEnabled(self.auto_save_checkbox.isChecked())
        
        # 连接信号以启用/禁用间隔控件
        self.auto_save_checkbox.toggled.connect(self.auto_save_interval.setEnabled)
        
        interval_container.addWidget(interval_label)
        interval_container.addWidget(self.auto_save_interval)
        interval_container.addStretch()
        
        auto_save_layout.addLayout(interval_container)
        auto_save_group.setLayout(auto_save_layout)
        layout.addWidget(auto_save_group)
        
        # 搜索设置组（亲密性原则）
        search_group = self._create_group_box("搜索设置")
        search_layout = QVBoxLayout()
        search_layout.setSpacing(SPACING_MD)
        
        search_label = QLabel("搜索结果排序条件：")
        search_label.setStyleSheet(self._get_label_style())
        search_layout.addWidget(search_label)
        
        # 搜索排序选项（单选按钮组）
        self.search_sort_group = QButtonGroup()
        sort_options = [
            ("按创建时间", "created_time"),
            ("按更新时间", "updated_time"),
            ("按名称排序", "name")
        ]
        
        # 获取当前设置的排序条件，默认为按名称排序
        current_sort = self.general_settings.get('search_sort', 'name')
        
        for text, value in sort_options:
            radio = QRadioButton(text)
            radio.setStyleSheet(self._get_radio_style())
            radio.setProperty("value", value)
            if value == current_sort:
                radio.setChecked(True)
            self.search_sort_group.addButton(radio)
            search_layout.addWidget(radio)
        
        search_group.setLayout(search_layout)
        layout.addWidget(search_group)
        
        layout.addStretch()
        general_tab.setLayout(layout)
        self.tab_widget.addTab(general_tab, "🔧 通用设置")

    def add_editor_tab(self):
        """添加编辑器设置 tab - 应用对比和重复原则"""
        editor_tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(SPACING_XL, SPACING_LG, SPACING_XL, SPACING_LG)
        layout.setSpacing(SPACING_LG)
        
        # 字体设置组（亲密性原则）
        font_group = self._create_group_box("字体设置")
        font_layout = QVBoxLayout()
        font_layout.setSpacing(SPACING_MD)
        
        # 字体大小设置（对齐原则）
        font_size_container = QHBoxLayout()
        font_size_label = QLabel("字体大小：")
        font_size_label.setStyleSheet(self._get_label_style())
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 32)
        self.font_size_spin.setValue(self.editor_settings.get('font_size', 14))
        self.font_size_spin.setSuffix(" px")
        self.font_size_spin.setStyleSheet(self._get_spinbox_style())
        self.font_size_spin.setFixedWidth(120)
        
        font_size_container.addWidget(font_size_label)
        font_size_container.addWidget(self.font_size_spin)
        font_size_container.addStretch()
        font_layout.addLayout(font_size_container)
        
        # 字体族设置（对齐原则）
        font_family_container = QVBoxLayout()
        font_family_label = QLabel("字体族：")
        font_family_label.setStyleSheet(self._get_label_style())
        
        self.font_family_edit = QLineEdit(self.editor_settings.get('font_family', "'Segoe UI', Consolas, monospace"))
        self.font_family_edit.setStyleSheet(create_input_style())
        self.font_family_edit.setPlaceholderText("例如：Consolas, 'Courier New', monospace")
        
        font_family_container.addWidget(font_family_label)
        font_family_container.addWidget(self.font_family_edit)
        font_layout.addLayout(font_family_container)
        
        font_group.setLayout(font_layout)
        layout.addWidget(font_group)
        
        layout.addStretch()
        editor_tab.setLayout(layout)
        self.tab_widget.addTab(editor_tab, "📝 编辑器设置")

    def add_appearance_tab(self):
        """添加外观设置 tab - 重点应用对比原则"""
        appearance_tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(SPACING_XL, SPACING_LG, SPACING_XL, SPACING_LG)
        layout.setSpacing(SPACING_LG)
        
        # 主题设置组（亲密性原则）
        theme_group = self._create_group_box("主题设置")
        theme_layout = QVBoxLayout()
        theme_layout.setSpacing(SPACING_MD)
        
        # 深色模式切换（对比原则 - 突出重要功能）
        self.dark_mode_checkbox = QCheckBox("启用深色模式")
        self.dark_mode_checkbox.setChecked(self.theme_settings.get('dark_mode', False))
        self.dark_mode_checkbox.setStyleSheet(self._get_checkbox_style(highlighted=True))
        theme_layout.addWidget(self.dark_mode_checkbox)
        
        # 主题名称设置
        theme_name_container = QVBoxLayout()
        theme_label = QLabel("主题名称：")
        theme_label.setStyleSheet(self._get_label_style())
        
        self.theme_edit = QLineEdit(self.theme_settings.get('theme', "默认主题"))
        self.theme_edit.setStyleSheet(create_input_style())
        self.theme_edit.setPlaceholderText("输入自定义主题名称")
        
        theme_name_container.addWidget(theme_label)
        theme_name_container.addWidget(self.theme_edit)
        theme_layout.addLayout(theme_name_container)
        
        # 添加主题说明（提供更好的用户体验）
        theme_hint = QLabel("💡 提示：深色模式可以减少眼部疲劳，适合长时间编辑使用")
        theme_hint.setStyleSheet(f"""
            QLabel {{
                color: {NEUTRAL_500};
                font-size: {FONT_SIZE_SM}px;
                background-color: {NEUTRAL_50};
                padding: {SPACING_SM}px {SPACING_MD}px;
                border-radius: {RADIUS_SM}px;
                border-left: 3px solid {PRIMARY_500};
                margin-top: {SPACING_SM}px;
            }}
        """)
        theme_hint.setWordWrap(True)
        theme_layout.addWidget(theme_hint)
        
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        
        layout.addStretch()
        appearance_tab.setLayout(layout)
        self.tab_widget.addTab(appearance_tab, "🎨 外观设置")

    def add_import_export_tab(self):
        """添加导入导出设置 tab - 强调功能性分组"""
        import_export_tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(SPACING_XL, SPACING_LG, SPACING_XL, SPACING_LG)
        layout.setSpacing(SPACING_LG)
        
        # 导入限制设置组（亲密性原则）
        import_group = self._create_group_box("导入限制设置")
        import_layout = QVBoxLayout()
        import_layout.setSpacing(SPACING_MD)
        
        # 最大导入大小设置（对齐原则）
        size_container = QHBoxLayout()
        size_label = QLabel("最大导入文件大小：")
        size_label.setStyleSheet(self._get_label_style())
        
        self.import_size = QSpinBox()
        self.import_size.setRange(1, 1024)
        self.import_size.setValue(self.import_settings.get('import_size', 30))
        self.import_size.setSuffix(" MB")
        self.import_size.setStyleSheet(self._get_spinbox_style())
        self.import_size.setFixedWidth(120)
        
        size_container.addWidget(size_label)
        size_container.addWidget(self.import_size)
        size_container.addStretch()
        import_layout.addLayout(size_container)
        
        import_group.setLayout(import_layout)
        layout.addWidget(import_group)
        
        # PDF处理设置组（亲密性原则）
        pdf_group = self._create_group_box("PDF处理设置")
        pdf_layout = QVBoxLayout()
        pdf_layout.setSpacing(SPACING_MD)
        
        pdf_label = QLabel("PDF导入解析方式：")
        pdf_label.setStyleSheet(self._get_label_style())
        pdf_layout.addWidget(pdf_label)
        
        # PDF导入方式选择（重复原则 - 统一的单选按钮样式）
        self.pdf_import_group = QButtonGroup()
        markitdown_radio = QRadioButton("使用 MarkItDown 解析器")
        markitdown_radio.setChecked(True)
        markitdown_radio.setStyleSheet(self._get_radio_style())
        
        self.pdf_import_group.addButton(markitdown_radio)
        pdf_layout.addWidget(markitdown_radio)
        
        # 添加说明文字
        pdf_hint = QLabel("📄 MarkItDown提供高质量的PDF文本提取和格式保留")
        pdf_hint.setStyleSheet(f"""
            QLabel {{
                color: {NEUTRAL_500};
                font-size: {FONT_SIZE_SM}px;
                background-color: {NEUTRAL_50};
                padding: {SPACING_SM}px {SPACING_MD}px;
                border-radius: {RADIUS_SM}px;
                border-left: 3px solid {PRIMARY_500};
                margin-top: {SPACING_XS}px;
            }}
        """)
        pdf_layout.addWidget(pdf_hint)
        
        pdf_group.setLayout(pdf_layout)
        layout.addWidget(pdf_group)
        
        layout.addStretch()
        import_export_tab.setLayout(layout)
        self.tab_widget.addTab(import_export_tab, "📁 导入导出设置")

    def save_settings(self):
        """保存所有设置项并触发主题更新"""
        settings_manager = SettingsManager()
        
        try:
            # 确保所有控件都已初始化
            if not all([
                self.auto_save_checkbox, self.auto_save_interval,
                self.font_size_spin, self.font_family_edit,
                self.dark_mode_checkbox, self.theme_edit,
                self.import_size, self.pdf_import_group,
                self.search_sort_group
            ]):
                raise ValueError("控件未正确初始化")
                
            # 保存通用设置 - 添加类型断言
            assert self.auto_save_checkbox is not None
            assert self.auto_save_interval is not None
            # 获取选中的搜索排序选项
            assert self.search_sort_group is not None
            checked_button = self.search_sort_group.checkedButton()
            search_sort_value = checked_button.property("value") if checked_button else "name"
            
            general_settings = {
                'auto_save': self.auto_save_checkbox.isChecked(),
                'auto_save_interval': self.auto_save_interval.value(),
                'search_sort': search_sort_value  # 保存搜索排序设置
            }
            settings_manager.create_settings('general', general_settings)
            
            # 保存编辑器设置 - 添加类型断言
            assert self.font_size_spin is not None
            assert self.font_family_edit is not None
            editor_settings = {
                'font_size': self.font_size_spin.value(),
                'font_family': self.font_family_edit.text().strip()
            }
            settings_manager.create_settings('editor', editor_settings)
            
            # 保存外观设置 - 添加类型断言
            assert self.dark_mode_checkbox is not None
            assert self.theme_edit is not None
            old_dark_mode = self.theme_settings.get('dark_mode', False)
            new_dark_mode = self.dark_mode_checkbox.isChecked()
            
            appearance_settings = {
                'dark_mode': new_dark_mode,
                'theme': self.theme_edit.text().strip()
            }
            settings_manager.create_settings('theme', appearance_settings)
            
            # 保存导入导出设置 - 添加类型断言
            assert self.pdf_import_group is not None
            assert self.import_size is not None
            checked_button = self.pdf_import_group.checkedButton()
            import_export_settings = {
                'import_size': self.import_size.value(),
                'pdf_import_method': checked_button.text() if checked_button else 'markitdown',
            }
            settings_manager.create_settings('import', import_export_settings)
            
            # 如果主题模式发生变化，通知父窗口更新主题
            if old_dark_mode != new_dark_mode and self.parent():
                parent = self.parent()
                if hasattr(parent, 'update_theme'):
                    parent.update_theme()  # type: ignore
            
            self.accept()
            
        except Exception as e:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "保存失败", f"设置保存失败：{str(e)}")
    
    # ========== 私有辅助方法 - 实现Robin Williams设计原则 ==========
    
    def _configure_tab_widget(self):
        """配置Tab控件样式（重复和对齐原则）"""
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {NEUTRAL_200};
                background-color: {NEUTRAL_0};
                border-radius: {RADIUS_MD}px;
                margin-top: {SPACING_XS}px;
            }}
            QTabBar::tab {{
                background-color: {NEUTRAL_100};
                color: {NEUTRAL_600};
                border: 1px solid {NEUTRAL_200};
                border-bottom: none;
                padding: {SPACING_MD}px {SPACING_XL}px;
                margin-right: 2px;
                border-top-left-radius: {RADIUS_SM}px;
                border-top-right-radius: {RADIUS_SM}px;
                font-size: {FONT_SIZE_MD}px;
                font-weight: 500;
                min-width: 120px;
            }}
            QTabBar::tab:selected {{
                background-color: {NEUTRAL_0};
                color: {PRIMARY_600};
                border-color: {NEUTRAL_200};
                border-bottom: 1px solid {NEUTRAL_0};
                font-weight: 600;
            }}
            QTabBar::tab:hover:!selected {{
                background-color: {PRIMARY_50};
                color: {PRIMARY_500};
                border-color: {PRIMARY_200};
            }}
        """)
    
    def _add_button_area(self, layout):
        """添加按钮区域（对齐原则）- 使用小尺寸按钮保持协调"""
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, SPACING_LG, 0, 0)
        
        # 添加弹性空间实现右对齐
        button_layout.addStretch()
        
        # 取消按钮（重复原则 - 统一按钮样式）- 使用小尺寸
        cancel_button = QPushButton("取消")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet(create_button_style("secondary", "sm"))  # 改为小尺寸
        cancel_button.setMinimumWidth(60)  # 减小最小宽度
        
        # 保存按钮（对比原则 - 突出主要操作）- 使用小尺寸
        save_button = QPushButton("保存")
        save_button.clicked.connect(self.save_settings)
        save_button.setStyleSheet(create_button_style("primary", "sm"))  # 改为小尺寸
        save_button.setMinimumWidth(60)  # 减小最小宽度
        save_button.setDefault(True)  # 设为默认按钮
        
        button_layout.addWidget(cancel_button)
        button_layout.addSpacing(SPACING_SM)  # 减小按钮间距
        button_layout.addWidget(save_button)
        
        layout.addLayout(button_layout)
    
    def _create_group_box(self, title):
        """创建统一样式的分组框（亲密性原则）"""
        group_box = QGroupBox(title)
        group_box.setStyleSheet(f"""
            QGroupBox {{
                font-size: {FONT_SIZE_MD}px;
                font-weight: 600;
                color: {NEUTRAL_700};
                border: 1px solid {NEUTRAL_200};
                border-radius: {RADIUS_SM}px;
                margin-top: {SPACING_MD}px;
                padding-top: {SPACING_MD}px;
                background-color: {NEUTRAL_0};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: {SPACING_MD}px;
                padding: 0 {SPACING_SM}px;
                background-color: {NEUTRAL_0};
                color: {NEUTRAL_700};
            }}
        """)
        return group_box
    
    def _get_label_style(self):
        """获取标签样式（重复原则）"""
        return f"""
            QLabel {{
                color: {NEUTRAL_700};
                font-size: {FONT_SIZE_MD}px;
                font-weight: 500;
                margin-bottom: {SPACING_XS}px;
                line-height: {LINE_HEIGHT_NORMAL};
            }}
        """
    
    def _get_checkbox_style(self, highlighted=False):
        """获取复选框样式（对比原则）"""
        base_color = PRIMARY_500 if highlighted else NEUTRAL_600
        return f"""
            QCheckBox {{
                color: {NEUTRAL_700};
                font-size: {FONT_SIZE_MD}px;
                font-weight: {600 if highlighted else 500};
                spacing: {SPACING_SM}px;
                padding: {SPACING_XS}px 0;
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 2px solid {NEUTRAL_300};
                border-radius: 3px;
                background-color: {NEUTRAL_0};
            }}
            QCheckBox::indicator:hover {{
                border-color: {base_color};
                background-color: {PRIMARY_50 if highlighted else NEUTRAL_50};
            }}
            QCheckBox::indicator:checked {{
                background-color: {base_color};
                border-color: {base_color};
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDQuNUw0LjUgOEwxMSAxIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
            }}
            QCheckBox::indicator:checked:hover {{
                background-color: {PRIMARY_600 if highlighted else PRIMARY_500};
            }}
        """
    
    def _get_spinbox_style(self):
        """获取数字输入框样式（重复原则）"""
        return f"""
            QSpinBox {{
                border: 1px solid {NEUTRAL_300};
                border-radius: {RADIUS_SM}px;
                padding: {SPACING_SM}px {SPACING_MD}px;
                font-size: {FONT_SIZE_MD}px;
                color: {NEUTRAL_700};
                background-color: {NEUTRAL_0};
                min-height: 20px;
                selection-background-color: {PRIMARY_100};
            }}
            QSpinBox:hover {{
                border-color: {PRIMARY_300};
                background-color: {PRIMARY_50};
            }}
            QSpinBox:focus {{
                border-color: {PRIMARY_500};
                background-color: {NEUTRAL_0};
                outline: 2px solid {PRIMARY_100};
                outline-offset: -2px;
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                width: 16px;
                background-color: {NEUTRAL_100};
                border: 1px solid {NEUTRAL_300};
                border-radius: 2px;
            }}
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
                background-color: {PRIMARY_50};
                border-color: {PRIMARY_300};
            }}
            QSpinBox::up-arrow, QSpinBox::down-arrow {{
                width: 8px;
                height: 8px;
            }}
        """
    
    def _get_radio_style(self):
        """获取单选按钮样式（重复原则）"""
        return f"""
            QRadioButton {{
                color: {NEUTRAL_700};
                font-size: {FONT_SIZE_MD}px;
                font-weight: 500;
                spacing: {SPACING_SM}px;
                padding: {SPACING_XS}px 0;
            }}
            QRadioButton::indicator {{
                width: 16px;
                height: 16px;
                border: 2px solid {NEUTRAL_300};
                border-radius: 8px;
                background-color: {NEUTRAL_0};
            }}
            QRadioButton::indicator:hover {{
                border-color: {PRIMARY_500};
                background-color: {PRIMARY_50};
            }}
            QRadioButton::indicator:checked {{
                background-color: {PRIMARY_500};
                border-color: {PRIMARY_500};
            }}
            QRadioButton::indicator:checked:hover {{
                background-color: {PRIMARY_600};
                border-color: {PRIMARY_600};
            }}
        """