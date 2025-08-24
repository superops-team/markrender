from datetime import datetime
from PySide6.QtWidgets import (
    QLineEdit, 
    QWidget,
    QHBoxLayout,
    QDialog,
    QPushButton,
    QFormLayout,    
    QLabel,
    QVBoxLayout,
    QTabWidget
)
from PySide6.QtCore import Qt
from app.preference import AppStyle


class EditItemDialog(QDialog):
    def __init__(self, markdown_data, parent=None):
        super().__init__(parent)
        self.markdown_data = markdown_data
        self.tags = []
        # 从数据库读取标签并分割
        tags_text = self.markdown_data.get('tags', '')
        if tags_text:
            self.tags = [tag.strip() for tag in tags_text.split(',') if tag.strip()]
        self.init_ui()
        self.setWindowTitle('编辑信息')
        self.setMinimumSize(600, 400)  # 与settings_dialog.py保持一致
        self.setStyleSheet(AppStyle().get_dialog_border_radius())

    def init_ui(self):
        # 完全复制settings_dialog.py的主布局结构
        layout = QVBoxLayout()
        self.tab_widget = QTabWidget()

        # 添加不同的tab页面
        self.add_editable_tab()
        self.add_readonly_tab()
        # 移除这行代码 - 不要将按钮样式应用到整个对话框
        # self.setStyleSheet(AppStyle().get_primary_button())

        # 添加保存按钮 - 完全复制settings_dialog.py的实现
        save_button = QPushButton("保存设置")
        save_button.clicked.connect(self.accept)
        save_button.setStyleSheet(AppStyle().get_primary_button())

        layout.addWidget(self.tab_widget)
        layout.addWidget(save_button)
        self.setLayout(layout)

    def add_editable_tab(self):
        """添加可编辑区域tab - 完全匹配settings_dialog.py的表单布局"""
        editable_tab = QWidget()
        form_layout = QFormLayout()
        form_layout.setContentsMargins(16, 16, 16, 16)
        form_layout.setSpacing(12)
        # 不设置间距，使用默认值以匹配settings_dialog.py

        # 标题编辑框 - 添加无边框样式
        self.title_edit = QLineEdit(self.markdown_data.get('title', ''))
        self.title_edit.setStyleSheet("background-color: transparent;")
        title_label = self.label_name('标题:')    
        form_layout.addRow(title_label, self.title_edit)

        # 标签区域
        tags_label = self.label_name('标签:')        
        # 标签容器
        tags_container = QWidget()
        tags_layout = QHBoxLayout()
        tags_layout.setSpacing(8)
        tags_layout.setContentsMargins(0, 0, 0, 0)
        
        # 显示现有标签
        self.tag_widgets = []
        for tag in self.tags:
            tag_widget = QLabel(tag)
            tag_widget.setStyleSheet(self._get_tag_style(tag))
            tag_widget.setAlignment(Qt.AlignCenter)
            tag_widget.setMinimumHeight(32)
            tags_layout.addWidget(tag_widget)
            self.tag_widgets.append(tag_widget)
        
        # 添加标签按钮 - 保持功能但使用更匹配的样式
        self.add_tag_button = QPushButton('+')
        self.add_tag_button.setFixedSize(32, 32)
        # 修改样式定义，使用ID选择器而不是类型选择器
        self.add_tag_button.setStyleSheet("""
            #add_tag_button {
                background-color: #0d6efd;
                color: white;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
            }
            #add_tag_button:hover {
                background-color: #0b5ed7;
            }
        """)
        # 为按钮设置对象名称，使ID选择器生效
        self.add_tag_button.setObjectName("add_tag_button")
        self.add_tag_button.clicked.connect(self._add_new_tag)
        tags_layout.addWidget(self.add_tag_button)
        
        tags_layout.addStretch()
        tags_container.setLayout(tags_layout)
        
        form_layout.addRow(tags_label, tags_container)

        editable_tab.setLayout(form_layout)
        self.tab_widget.addTab(editable_tab, "编辑")

    def label_name(self, name):
        label = QLabel(name)
        label.setStyleSheet("border: none; background-color: transparent;")
        return label

    def add_readonly_tab(self):
        """添加只读信息tab - 完全匹配settings_dialog.py的表单布局"""
        readonly_tab = QWidget()
        form_layout = QFormLayout()
        # 不设置间距，使用默认值以匹配settings_dialog.py

        # 文件类型（只读） - 不设置特殊样式，使用默认样式
        file_type = self.markdown_data.get('file_type', 'markdown')
        if not file_type:
            file_type = 'markdown'
        file_type_label = QLabel(file_type)
        # 不设置特殊样式，使用默认样式以匹配settings_dialog.py
        form_layout.addRow(self.label_name('文件类型:'), file_type_label)

        # 创建时间（只读）
        created_time = self.markdown_data.get('created_at', '')
        if created_time:
            if isinstance(created_time, datetime):
                created_time = created_time.strftime('%Y-%m-%d %H:%M:%S')
            created_label = QLabel(str(created_time))
            # 不设置特殊样式，使用默认样式以匹配settings_dialog.py
            form_layout.addRow(self.label_name('创建时间:'), created_label)

        # 修改时间（只读）
        updated_time = self.markdown_data.get('updated_at', '')
        if updated_time:
            if isinstance(updated_time, datetime):
                updated_time = updated_time.strftime('%Y-%m-%d %H:%M:%S')
            updated_label = QLabel(str(updated_time))
            # 不设置特殊样式，使用默认样式以匹配settings_dialog.py
            form_layout.addRow(self.label_name('修改时间:'), updated_label)

        readonly_tab.setLayout(form_layout)
        self.tab_widget.addTab(readonly_tab, "详细信息")

    def _get_tag_style(self, tag):
        """根据标签内容生成不同的样式 - 添加无边框设置"""
        colors = {
            'md': 'background-color: #9FC89C; color: white;',
            'pdf': 'background-color: #91C8E4; color: white;',
            'png': 'background-color: #ADB2D4; color: white;',
            'jpeg': 'background-color: #0F828C; color: white;',
            'csv': 'background-color: #A3DC9A; color: white;',
            'docx': 'background-color: #97B067; color: white;',
            'default': 'background-color: #0078D4; color: white;'  # 使用主按钮颜色
        }
        
        # 使用标签的前几个字符作为key
        tag_key = tag.lower()[:4]
        return f"""
            padding: 6px 16px;
            border-radius: 16px;
            font-size: 14px;
            border: none; /* 明确设置无边框 */
            {colors.get(tag_key, colors['default'])}
        """

    def _add_new_tag(self):
        """直接添加新的可编辑标签"""
        # 创建新的标签输入框 - 不设置特殊样式，使用默认样式
        tag_edit = QLineEdit()
        tag_edit.setPlaceholderText("输入新标签...")
        # 不设置特殊样式，使用默认样式以匹配settings_dialog.py
        tag_edit.returnPressed.connect(lambda: self._finalize_new_tag(tag_edit))
        
        # 获取当前标签布局并插入新标签输入框
        tags_container = self.add_tag_button.parent()
        tags_layout = tags_container.layout()
        tags_layout.insertWidget(len(self.tags), tag_edit)
        
        # 设置焦点到新输入框
        tag_edit.setFocus()
    
    def _finalize_new_tag(self, tag_edit):
        """完成新标签的添加"""
        tag = tag_edit.text().strip()
        if tag:
            if tag not in self.tags:
                self.tags.append(tag)
                # 创建最终的标签显示控件
                tag_widget = QLabel(tag)
                tag_widget.setStyleSheet(self._get_tag_style(tag))
                tag_widget.setAlignment(Qt.AlignCenter)
                tag_widget.setMinimumHeight(32)
                
                # 替换输入框为最终标签
                tags_container = self.add_tag_button.parent()
                tags_layout = tags_container.layout()
                
                # 找到输入框的位置并替换
                for i in range(tags_layout.count()):
                    widget = tags_layout.itemAt(i).widget()
                    if widget == tag_edit:
                        tags_layout.removeWidget(tag_edit)
                        tags_layout.insertWidget(i, tag_widget)
                        self.tag_widgets.append(tag_widget)
                        tag_edit.deleteLater()
                        break
        else:
            # 如果输入为空，移除输入框
            tags_container = self.add_tag_button.parent()
            tags_layout = tags_container.layout()
            tags_layout.removeWidget(tag_edit)
            tag_edit.deleteLater()
    
    def get_new_title(self):
        return self.title_edit.text()

    def get_new_tags(self):
        """获取格式化后的标签字符串"""
        return ', '.join(self.tags)