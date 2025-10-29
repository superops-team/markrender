# -*- coding: utf-8 -*-
"""
历史记录差异对比对话框
使用diff-match-patch显示当前版本与历史版本的差异
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, 
    QLabel, QWidget, QSizePolicy, QApplication, QFrame, QScrollArea, QTabWidget, QFormLayout
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QTextCharFormat, QColor, QFont
from diff_match_patch import diff_match_patch

from app.preference.style_constants import (
    NEUTRAL_0, NEUTRAL_50, NEUTRAL_100, NEUTRAL_200, NEUTRAL_700,
    SUCCESS_500, DANGER_500, SPACING_SM, SPACING_MD, RADIUS_MD,
    FONT_SIZE_MD, FONT_SIZE_SM
)


class HistoryDiffDialog(QDialog):
    """历史记录差异对比对话框"""
    
    def __init__(self, current_content, history_content, change_type, field_changes=None, parent=None):
        super().__init__(parent)
        self.current_content = current_content or ""
        self.history_content = history_content or ""
        self.change_type = change_type or "content_update"
        self.field_changes = field_changes or {}  # 字段变更信息，格式：{'field_name': {'old': 'old_value', 'new': 'new_value'}}
        self.dmp = diff_match_patch()
        self.setup_ui()
        self.compare_contents()
        
    def setup_ui(self):
        """设置UI界面"""
        self.setWindowTitle("版本差异对比")
        self.setMinimumSize(QSize(900, 700))
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {NEUTRAL_0};
            }}
        """)
        
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(SPACING_MD, SPACING_MD, SPACING_MD, SPACING_MD)
        main_layout.setSpacing(SPACING_MD)
        
        # 标题
        title_label = QLabel("版本差异对比")
        title_label.setStyleSheet(f"""
            color: {NEUTRAL_700};
            font-size: {FONT_SIZE_MD}px;
            font-weight: 600;
            margin-bottom: {SPACING_SM}px;
        """)
        main_layout.addWidget(title_label)
        
        # 说明文本
        info_label = QLabel("红色背景表示已删除的内容，绿色背景表示新增的内容")
        info_label.setStyleSheet(f"""
            color: {NEUTRAL_700};
            font-size: {FONT_SIZE_SM}px;
            margin-bottom: {SPACING_MD}px;
        """)
        main_layout.addWidget(info_label)
        
        # 创建Tab控件
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {NEUTRAL_200};
                border-radius: {RADIUS_MD}px;
                padding: {SPACING_SM}px;
                background-color: {NEUTRAL_0};
            }}
            QTabBar::tab {{
                background: {NEUTRAL_50};
                color: {NEUTRAL_700};
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: {RADIUS_MD}px;
                border-top-right-radius: {RADIUS_MD}px;
                border: 1px solid {NEUTRAL_200};
                font-weight: 500;
            }}
            QTabBar::tab:selected {{
                background: {NEUTRAL_0};
                border-bottom-color: {NEUTRAL_0};
            }}
            QTabBar::tab:hover {{
                background: {NEUTRAL_100};
            }}
        """)
        
        # 固定两个Tab项：内容差异和字段变更
        # 内容差异Tab
        content_tab = QWidget()
        content_layout = QVBoxLayout(content_tab)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(SPACING_MD)
        self.setup_content_diff_section(content_layout)
        self.tab_widget.addTab(content_tab, "内容差异")
        
        # 字段变更Tab
        field_tab = QWidget()
        field_layout = QVBoxLayout(field_tab)
        field_layout.setContentsMargins(0, 0, 0, 0)
        field_layout.setSpacing(SPACING_MD)
        self.setup_field_changes_section(field_layout)
        self.tab_widget.addTab(field_tab, "字段变更")
        
        # 默认展示内容差异Tab
        self.tab_widget.setCurrentIndex(0)
        
        main_layout.addWidget(self.tab_widget)
        
        # 按钮区域 - 右对齐
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(SPACING_SM)
        
        # 添加弹性空间将按钮推到右侧
        button_layout.addStretch()
        
        # 取消按钮
        self.cancel_button = QPushButton("取消")
        self.cancel_button.setStyleSheet(f"""
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
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        # 使用历史版本按钮
        self.use_history_button = QPushButton("使用历史版本")
        self.use_history_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {SUCCESS_500};
                color: {NEUTRAL_0};
                border: 1px solid {SUCCESS_500};
                border-radius: {RADIUS_MD}px;
                padding: {SPACING_SM}px {SPACING_MD}px;
                font-size: {FONT_SIZE_MD}px;
                font-weight: 500;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: #218838;
                border-color: #1e7e34;
            }}
        """)
        self.use_history_button.clicked.connect(self.accept)
        button_layout.addWidget(self.use_history_button)
        
        main_layout.addLayout(button_layout)
        
    def setup_field_changes_section(self, main_layout):
        """设置字段变更区域"""
        # 创建滚动区域以容纳所有字段变更
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(SPACING_SM)
        
        # 使用表单布局组织字段变更
        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(SPACING_SM)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # 显示每个字段的变更
        for field_name, change_info in self.field_changes.items():
            old_value = change_info.get('old', '')
            new_value = change_info.get('new', '')
            
            # 创建变更展示容器
            change_container = QWidget()
            change_layout = QHBoxLayout(change_container)
            change_layout.setContentsMargins(0, 0, 0, 0)
            change_layout.setSpacing(SPACING_SM)
            
            # 旧值
            old_label = QLabel(str(old_value) if old_value is not None else "无")
            old_label.setStyleSheet(f"""
                color: {DANGER_500};
                font-size: {FONT_SIZE_SM}px;
                background-color: rgba(220, 53, 69, 0.1);
                padding: 4px 8px;
                border-radius: {RADIUS_MD}px;
                min-width: 120px;
            """)
            old_label.setWordWrap(True)
            old_label.setMinimumHeight(28)
            change_layout.addWidget(old_label)
            
            # 箭头
            arrow_label = QLabel("→")
            arrow_label.setStyleSheet(f"""
                color: {NEUTRAL_700};
                font-size: {FONT_SIZE_SM}px;
                font-weight: bold;
                margin: 0 8px;
            """)
            change_layout.addWidget(arrow_label)
            
            # 新值
            new_label = QLabel(str(new_value) if new_value is not None else "无")
            new_label.setStyleSheet(f"""
                color: {SUCCESS_500};
                font-size: {FONT_SIZE_SM}px;
                background-color: rgba(40, 167, 69, 0.1);
                padding: 4px 8px;
                border-radius: {RADIUS_MD}px;
                min-width: 120px;
            """)
            new_label.setWordWrap(True)
            new_label.setMinimumHeight(28)
            change_layout.addWidget(new_label)
            
            # 添加弹性空间
            change_layout.addStretch()
            
            # 添加到表单布局
            field_display_name = self.get_field_display_name(field_name)
            form_layout.addRow(QLabel(f"{field_display_name}:"), change_container)
        
        # 如果没有字段变更，显示提示信息
        if not self.field_changes:
            no_changes_label = QLabel("没有字段变更")
            no_changes_label.setStyleSheet(f"""
                color: {NEUTRAL_700};
                font-size: {FONT_SIZE_SM}px;
                font-style: italic;
                padding: {SPACING_SM}px;
                text-align: center;
            """)
            no_changes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            form_layout.addRow(no_changes_label)
        
        scroll_layout.addLayout(form_layout)
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
    def setup_content_diff_section(self, main_layout):
        """设置内容差异区域"""
        # 创建滚动区域以容纳内容差异
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; }")
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(SPACING_SM)
        
        # 创建文本显示区域
        self.diff_text_edit = QTextEdit()
        self.diff_text_edit.setReadOnly(True)
        self.diff_text_edit.setStyleSheet(f"""
            QTextEdit {{
                border: 1px solid {NEUTRAL_200};
                border-radius: {RADIUS_MD}px;
                padding: {SPACING_MD}px;
                background-color: {NEUTRAL_50};
                font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
                font-size: {FONT_SIZE_SM}px;
                selection-background-color: {NEUTRAL_200};
            }}
        """)
        self.diff_text_edit.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.diff_text_edit.setMinimumHeight(450)  # 增加最小高度
        scroll_layout.addWidget(self.diff_text_edit)
        
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
    def get_field_display_name(self, field_name):
        """获取字段显示名称"""
        field_names = {
            'title': '标题',
            'display_name': '显示名称',
            'icon_type': '图标类型',
            'icon_path': '图标路径',
            'icon_color': '图标颜色'
        }
        return field_names.get(field_name, field_name)
        
    def compare_contents(self):
        """比较内容并显示差异"""
        # 只有内容变更类型才显示内容差异
        if self.change_type in ['content_create', 'content_update']:
            # 使用diff-match-patch计算差异
            diffs = self.dmp.diff_main(self.current_content, self.history_content)
            self.dmp.diff_cleanupSemantic(diffs)
            
            # 创建文本格式
            cursor = self.diff_text_edit.textCursor()
            self.diff_text_edit.clear()
            
            # 定义格式
            normal_format = QTextCharFormat()
            normal_format.setForeground(QColor(NEUTRAL_700))
            normal_format.setFont(QFont("Menlo", 12))
            
            delete_format = QTextCharFormat()
            delete_format.setBackground(QColor(DANGER_500))
            delete_format.setForeground(QColor(NEUTRAL_0))
            delete_format.setFont(QFont("Menlo", 12))
            
            insert_format = QTextCharFormat()
            insert_format.setBackground(QColor(SUCCESS_500))
            insert_format.setForeground(QColor(NEUTRAL_0))
            insert_format.setFont(QFont("Menlo", 12))
            
            # 应用格式到文本
            for op, text in diffs:
                if op == self.dmp.DIFF_EQUAL:
                    cursor.insertText(text, normal_format)
                elif op == self.dmp.DIFF_DELETE:
                    cursor.insertText(text, delete_format)
                elif op == self.dmp.DIFF_INSERT:
                    cursor.insertText(text, insert_format)