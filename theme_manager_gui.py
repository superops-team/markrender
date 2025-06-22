# -*- coding: utf-8 -*-
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QColorDialog,
    QDialog,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)


class ThemeManagerGUI:
    def __init__(self, main_window, theme_manager):
        self.main_window = main_window
        self.theme_manager = theme_manager
        self.table = None  # 将 table 对象作为属性

    def get_theme_names(self):
        themes = self.theme_manager.get_all_themes()
        return [theme.name for theme in themes]

    def select_title_color(self, event):
        """打开颜色选择对话框"""
        color = QColorDialog.getColor(
            QColor(self.main_window.title_color), self.main_window, "选择标题颜色"
        )
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
        from PySide6.QtWidgets import (
            QDialog,
            QHBoxLayout,
            QLineEdit,
            QPushButton,
            QTextEdit,
            QVBoxLayout,
        )

        dialog = QDialog(self.main_window)
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
        button_layout = QHBoxLayout()
        save_button = QPushButton("保存")
        cancel_button = QPushButton("取消")
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        dialog.setLayout(layout)

        def save_theme():
            theme_name = title_input.text()
            theme_config = config_input.toPlainText()
            if theme_name and theme_config:
                self.theme_manager.create_theme(theme_name, theme_config)
                dialog.close()
                # 刷新主题管理对话框表格
                if self.table:
                    self.refresh_theme_table()

        save_button.clicked.connect(save_theme)
        cancel_button.clicked.connect(dialog.close)

        dialog.exec()

    def delete_theme(self, theme_name=None):
        if not theme_name:
            theme_name = self.main_window.style_combobox.currentText()
        if theme_name:
            reply = QMessageBox.question(
                self.main_window,
                "确认删除",
                f"确定要删除主题 '{theme_name}' 吗？",
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                self.theme_manager.delete_theme(theme_name)
                self.main_window.style_combobox.removeItem(
                    self.main_window.style_combobox.findText(theme_name)
                )
                # 刷新主题管理对话框表格
                if self.table:
                    self.refresh_theme_table()

    def refresh_theme_table(self):
        themes = self.theme_manager.get_all_themes()
        self.table.setRowCount(len(themes))
        for row, theme in enumerate(themes):
            # 主题名称
            item_name = QTableWidgetItem(theme.name)
            self.table.setItem(row, 0, item_name)
            # 创建时间
            item_create_time = QTableWidgetItem(str(theme.created_at))
            self.table.setItem(row, 1, item_create_time)
            # 修改时间
            item_update_time = QTableWidgetItem(str(theme.updated_at))
            self.table.setItem(row, 2, item_update_time)

            # 编辑按钮
            edit_button = QPushButton("编辑")
            edit_button.clicked.connect(
                lambda _, tn=theme.name: self.edit_theme(tn))
            self.table.setCellWidget(row, 3, edit_button)

            # 删除按钮
            delete_button = QPushButton("删除")
            delete_button.clicked.connect(
                lambda _, tn=theme.name: self.delete_theme(tn)
            )
            self.table.setCellWidget(row, 4, delete_button)

    def get_current_style(self):
        current_theme_name = self.main_window.style_combobox.currentText()
        theme = self.theme_manager.get_theme(current_theme_name)
        if theme:
            return theme.css_config
        return self.main_window.get_base_style()

    def show_theme_management_dialog(self):
        # 这里实现主题管理对话框的创建和显示逻辑
        dialog = QDialog(self.main_window)
        dialog.setWindowTitle("主题管理")
        # 调整对话框大小
        dialog.resize(550, 550)
        layout = QVBoxLayout()

        self.table = QTableWidget()
        themes = self.theme_manager.get_all_themes()
        self.table.setRowCount(len(themes))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["主题名称", "创建时间", "修改时间", "编辑", "删除"]
        )

        for row, theme in enumerate(themes):
            # 主题名称
            item_name = QTableWidgetItem(theme.name)
            self.table.setItem(row, 0, item_name)
            # 创建时间
            item_create_time = QTableWidgetItem(str(theme.created_at))
            self.table.setItem(row, 1, item_create_time)
            # 修改时间
            item_update_time = QTableWidgetItem(str(theme.updated_at))
            self.table.setItem(row, 2, item_update_time)
            # 编辑按钮
            edit_button = QPushButton("编辑")
            edit_button.clicked.connect(
                lambda _, theme_name=theme.name: self.edit_theme(theme_name)
            )
            self.table.setCellWidget(row, 3, edit_button)
            # 删除按钮
            delete_button = QPushButton("删除")
            delete_button.clicked.connect(
                lambda _, theme_name=theme.name: self.delete_theme(theme_name)
            )
            self.table.setCellWidget(row, 4, delete_button)
        # 添加新增主题按钮到对话框底部
        add_theme_button = QPushButton("新增主题")
        add_theme_button.clicked.connect(self.add_theme)
        layout.addWidget(add_theme_button)

        # Bug 修复：将 table 替换为 self.table
        layout.addWidget(self.table)
        dialog.setLayout(layout)
        dialog.exec()

    def edit_theme(self, theme_name):
        from PySide6.QtWidgets import (
            QDialog,
            QHBoxLayout,
            QLineEdit,
            QPushButton,
            QTextEdit,
            QVBoxLayout,
        )

        theme = self.theme_manager.get_theme(theme_name)
        if theme:
            dialog = QDialog(self.main_window)
            dialog.setWindowTitle("编辑主题")
            layout = QVBoxLayout()

            # 主题标题输入框，使用单个输入框
            title_input = QLineEdit(theme_name)
            title_input.setPlaceholderText("请输入新主题名称")
            title_input.setReadOnly(True)  # 设置为只读
            layout.addWidget(title_input)

            # 主题配置输入框
            config_input = QTextEdit()
            config_input.setPlainText(theme.css_config)
            config_input.setPlaceholderText("输入主题配置")
            layout.addWidget(config_input)

            # 保存和取消按钮
            button_layout = QHBoxLayout()
            save_button = QPushButton("保存")
            save_button.clicked.connect(
                lambda: self.main_window.update_existing_theme(
                    title_input.text(), config_input.toPlainText(), theme_name, dialog
                )
            )
            cancel_button = QPushButton("取消")
            cancel_button.clicked.connect(dialog.close)
            button_layout.addWidget(save_button)
            button_layout.addWidget(cancel_button)
            layout.addLayout(button_layout)

            dialog.setLayout(layout)
            dialog.exec()
