from PySide6.QtWidgets import (
    QDialog, 
    QTabWidget, 
    QVBoxLayout, 
    QWidget, 
    QLabel, 
    QLineEdit, 
    QFormLayout, 
    QPushButton,
    QHBoxLayout,
    QSizePolicy,
    QComboBox
) 
from PySide6.QtCore import Qt
from app.preference import AppStyle

class EditItemDialog(QDialog):
    
    def __init__(self, markdown_data, parent=None):
        super().__init__(parent)
        self.app_style = AppStyle()
        self.markdown_data = markdown_data
        self.tags = []
        tags_text = self.markdown_data.get('tags', '')
        if tags_text:
            self.tags = [tag.strip() for tag in tags_text.split(',') if tag.strip()]
        self.setWindowTitle(self.markdown_data.get('title', '查看详情'))
        self.setMinimumSize(600, 400)
        self.setStyleSheet(self.app_style.get_tab_style())
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.tab_widget = QTabWidget()
        self.add_edit_tab()
        self.add_detail_tab()
        save_button = QPushButton("保存设置")
        save_button.clicked.connect(self.accept)
        layout.addWidget(self.tab_widget)
        layout.addWidget(save_button)
        self.setLayout(layout)

    def add_edit_tab(self):
        edit_tab = QWidget()
        main_layout = QVBoxLayout(edit_tab)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(8)
        
        self.title_edit = QLineEdit(self.markdown_data.get('title', ''))
        self.title_edit.setMinimumHeight(32)
        self.title_edit.setMinimumWidth(450)
        self.title_edit.setStyleSheet(self.app_style.get_line_edit())
        title_label = self._make_label('标题:')
        form_layout.addRow(title_label, self.title_edit)
        
        tags_label = self._make_label('标签:')
        self.tag_add_edit = QLineEdit()
        self.tag_add_edit.setMinimumHeight(32)
        self.tag_add_edit.setMinimumWidth(450)
        self.tag_add_edit.setStyleSheet(self.app_style.get_line_edit())
        self.tag_add_edit.setPlaceholderText("添加标签")
        self.tag_add_edit.returnPressed.connect(self._add_new_tag)
        form_layout.addRow(tags_label, self.tag_add_edit)
        
        main_layout.addLayout(form_layout)
        
        self.tags_container = QWidget()
        self.tags_container.setStyleSheet("border: none; background: transparent;")
        self.tags_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        self.tags_vertical_layout = QVBoxLayout(self.tags_container)
        self.tags_vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.tags_vertical_layout.setSpacing(6)
        
        self.tag_layouts = []
        self.tag_widgets = []
        
        self._create_new_row()
        self._refresh_tags()  # Initialize tags display
        
        self.tags_vertical_layout.addStretch(1)
        main_layout.addWidget(self.tags_container)
        self.tab_widget.addTab(edit_tab, "编辑")
    
    def _create_new_row(self):
        new_layout = QHBoxLayout()
        new_layout.setContentsMargins(0, 0, 0, 0)
        new_layout.setSpacing(8)
        self.tags_vertical_layout.insertLayout(self.tags_vertical_layout.count() - 1, new_layout)
        self.tag_layouts.append(new_layout)
        return new_layout
        
    def _make_label(self, name):
        label = QLabel(name)
        label.setStyleSheet("border: none; background-color: transparent;")
        return label
        
    def _make_tag_widget(self, tag, with_delete_button=True):
        container = QWidget()
        container.setMinimumHeight(32)
        container.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        container.setStyleSheet("""
            QWidget {
                background-color: #E7F0FD;
                border: 1px solid #0078D4;
                border-radius: 16px;
            }
        """)
        
        layout = QHBoxLayout(container)
        layout.setContentsMargins(12, 6, 8, 6)
        layout.setSpacing(8)
        
        tag_label = QLabel(tag)
        tag_label.setStyleSheet("""
            color: #0078D4;
            background-color: transparent;
            border: none;
            padding: 0px;
        """)
        tag_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(tag_label, 1)
        
        if not with_delete_button:
            return container
        
        delete_button = QPushButton("x")
        delete_button.setFixedSize(20, 20)
        delete_button.setStyleSheet("""
            QPushButton {
                color: #0078D4;
                background-color: transparent;
                font-size: 14px;
                font-weight: bold;
                border: none;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(0, 120, 212, 0.2);
                border-radius: 10px;
            }
        """)
        delete_button.clicked.connect(lambda: self._remove_tag(tag, container))
        layout.addWidget(delete_button)
        
        text_width = tag_label.fontMetrics().boundingRect(tag).width() + 40
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
        """Handle adding a new tag"""
        tag_text = self.tag_add_edit.text().strip()
        if tag_text and tag_text not in self.tags:
            self.tags.append(tag_text)
            self._refresh_tags()  # Re-render all tags
            self.tag_add_edit.clear()

    def add_detail_tab(self):
        editor_tab = QWidget()
        form_layout = QFormLayout()
        page_type = self.markdown_data.get('page_type', 'markdown')
        if not page_type:
            page_type = 'markdown'
        page_type_label = self._make_tag_widget(page_type, False)
        page_type_layout = QHBoxLayout()
        page_type_layout.addWidget(page_type_label)
        form_layout.addRow(self._make_label("文件类型："), page_type_layout)
        create_time = self.markdown_data.get('created_at', '')
        if create_time:
            create_time = create_time.strftime('%Y-%m-%d %H:%M:%S')
        create_time_label = self._make_label(create_time)
        form_layout.addRow(self._make_label("创建时间："), create_time_label)
        update_time = self.markdown_data.get('updated_at', '')
        if update_time:
            update_time = update_time.strftime('%Y-%m-%d %H:%M:%S')
        update_time_label = self._make_label(update_time)
        form_layout.addRow(self._make_label("更新时间："), update_time_label)
        file_size = self.markdown_data.get('file_size', '')
        if file_size:
            file_size = f"{file_size} bytes"
        else:
            file_size = "0 bytes"
        file_size_label = self._make_label(file_size)
        form_layout.addRow(self._make_label("文件大小："), file_size_label)
        content_md5 = self.markdown_data.get('content_md5', '')
        if content_md5:
            content_md5 = f"{content_md5}"
        else:
            content_md5 = ""
        content_md5_label = self._make_label(content_md5)
        form_layout.addRow(self._make_label("MD5值："), content_md5_label)
        editor_tab.setLayout(form_layout)
        self.tab_widget.addTab(editor_tab, "属性")

    def get_new_title(self):
        return self.title_edit.text()

    def get_new_tags(self):
        return ','.join(self.tags)