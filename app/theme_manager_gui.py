# -*- coding: utf-8 -*-
from dayu_widgets import dayu_theme
from dayu_widgets.message import MMessage
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QColorDialog, QDialog, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QTableView
from PySide6.QtCore import QAbstractTableModel, Qt


class ThemeManagerGUI:
    def __init__(self, main_window, theme_manager):
        self.main_window = main_window
        self.theme_manager = theme_manager
        self.table_model = None  # 新增 table_model 属性
        self.table_view = None  # 新增 table_view 属性

    def get_theme_names(self):
        themes = self.theme_manager.get_all_themes()
        return [theme.name for theme in themes]

    def select_title_color(self, event):
        """打开颜色选择对话框"""
        color = QColorDialog.getColor(
            QColor(
                self.main_window.title_color),
            self.main_window,
            "选择标题颜色")
        if color.isValid():
            self.main_window.title_color = color.name()
            self.main_window.color_button.setStyleSheet(
                f"color: {self.main_window.title_color}; font-size: 18px;"
            )
            self.main_window.update_preview()
            # 更新数据库中的主题样式
            current_theme_name = self.main_window.style_combobox.currentText()
            current_style = self.main_window.get_current_style()
            self.theme_manager.update_theme(current_theme_name, current_style)

    def add_theme(self):
        dialog = QDialog(parent=self.main_window)
        dialog.setWindowTitle("新增主题")
        layout = QVBoxLayout()

        # 主题标题输入框
        title_input = QLineEdit()
        title_input.setPlaceholderText("请输入新主题名称")
        layout.addWidget(title_input)

        # 主题配置输入框
        config_input = QTextEdit()
        config_input.setPlaceholderText("输入主题配置")
        layout.addWidget(config_input)

        # 保存和取消按钮
        button_layout = QVBoxLayout()
        save_button = QPushButton("保存")
        cancel_button = QPushButton("取消")
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        dialog.setLayout(layout)
        dayu_theme.apply(dialog)

        def save_theme():
            theme_name = title_input.text()
            theme_config = config_input.toPlainText()
            if theme_name and theme_config:
                self.theme_manager.create_theme(theme_name, theme_config)
                dialog.close()
                # 刷新主题管理对话框表格
                self.refresh_theme_table()

        save_button.clicked.connect(save_theme)
        cancel_button.clicked.connect(dialog.close)

        dialog.exec()

    def delete_theme(self, theme_name=None):
        if not theme_name:
            theme_name = self.main_window.style_combobox.currentText()
        if theme_name:
            reply = MMessage.confirm(
                f"确定要删除主题 '{theme_name}' 吗？",
                parent=self.main_window,
                title="确认删除",
            )
            if reply:
                self.theme_manager.delete_theme(theme_name)
                self.main_window.style_combobox.removeItem(
                    self.main_window.style_combobox.findText(theme_name)
                )
                # 刷新主题管理对话框表格
                self.refresh_theme_table()

    def refresh_theme_table(self):
        themes = self.theme_manager.get_all_themes()
        headers = ["主题名称", "创建时间", "修改时间", "编辑", "删除"]
        data = []
        for theme in themes:
            data.append([
                theme.name,
                str(theme.created_at),
                str(theme.updated_at),
                "编辑",
                "删除"
            ])
        self.table_model = ThemeTableModel(data, headers)
        self.table_view.setModel(self.table_model)

    def get_current_style(self):
        current_theme_name = self.main_window.style_combobox.currentText()
        theme = self.theme_manager.get_theme(current_theme_name)
        if theme:
            return theme.css_config
        return self.main_window.get_base_style()

    def show_theme_management_dialog(self):
        dialog = QDialog(parent=self.main_window)
        dialog.setWindowTitle("主题管理")
        # 调整对话框大小
        dialog.resize(550, 550)
        layout = QVBoxLayout()

        self.table_model = QAbstractTableModel()
        self.table_view = QTableView()
        self.refresh_theme_table()

        # 添加新增主题按钮到对话框底部
        add_theme_button = QPushButton("新增主题")
        add_theme_button.clicked.connect(self.add_theme)
        layout.addWidget(add_theme_button)
        layout.addWidget(self.table_view)
        dialog.setLayout(layout)
        dayu_theme.apply(dialog)
        dialog.exec()


class ThemeTableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self._data[index.row()][index.column()])
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        return None
