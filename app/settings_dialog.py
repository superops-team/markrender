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
    QPushButton,  # 新增导入
)
from PySide6.QtCore import Qt
from db.settings_manager import SettingsManager
from app.app_style import AppStyle

from PySide6.QtWidgets import ( 
    QRadioButton, 
    QButtonGroup 
) 

class SettingsDialog(QDialog):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("软件设置")
        self.setMinimumSize(600, 400)
        self.theme_settings = SettingsManager().get_settings_dict('theme') # 主题设置
        self.editor_settings = SettingsManager().get_settings_dict('editor') # 编辑器设置
        self.general_settings = SettingsManager().get_settings_dict('general') # 通用设置
        self.import_settings = SettingsManager().get_settings_dict('import') # 导入导出设置
        # 保存控件引用
        self.auto_save_checkbox = None
        self.auto_save_interval = None
        self.font_size_spin = None
        self.font_family_edit = None
        self.dark_mode_checkbox = None
        self.theme_edit = None
        self.import_dir_edit = None  # 修改控件引用名
        self.import_size = None  # 新增该行
        self.init_ui()

    def init_ui(self):
        # 创建主布局和 tab 控件
        layout = QVBoxLayout()
        self.tab_widget = QTabWidget()

        # 添加不同的设置 tab 页面
        self.add_general_tab()
        self.add_editor_tab()
        self.add_appearance_tab()
        self.add_import_export_tab()
        self.setStyleSheet(AppStyle().get_confirm_button_style())

        # 添加保存按钮
        save_button = QPushButton("保存设置")
        save_button.clicked.connect(self.save_settings)

        layout.addWidget(self.tab_widget)
        layout.addWidget(save_button)
        self.setLayout(layout)

    def add_general_tab(self):
        """添加通用设置 tab"""
        general_tab = QWidget()
        form_layout = QFormLayout()

        # 添加设置项示例
        self.auto_save_checkbox = QCheckBox("自动保存")
        self.auto_save_checkbox.setChecked(self.general_settings.get('auto_save', False))
        self.auto_save_interval = QSpinBox()
        self.auto_save_interval.setRange(1, 60)
        self.auto_save_interval.setValue(self.general_settings.get('auto_save_interval', 5))
        self.auto_save_interval.setSuffix(" 分钟")

        form_layout.addRow("自动保存频率:", self.auto_save_interval)
        form_layout.addRow("", self.auto_save_checkbox)

        general_tab.setLayout(form_layout)
        self.tab_widget.addTab(general_tab, "通用设置")

    def add_editor_tab(self):
        """添加编辑器设置 tab"""
        editor_tab = QWidget()
        form_layout = QFormLayout()

        # 添加设置项示例
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 24)
        self.font_size_spin.setValue(self.editor_settings.get('font_size', 12))
        self.font_family_edit = QLineEdit(self.editor_settings.get('font_family', "Consolas"))

        form_layout.addRow("字体大小:", self.font_size_spin)
        form_layout.addRow("字体:", self.font_family_edit)

        editor_tab.setLayout(form_layout)
        self.tab_widget.addTab(editor_tab, "编辑器设置")

    def add_appearance_tab(self):
        """添加外观设置 tab"""
        appearance_tab = QWidget()
        form_layout = QFormLayout()

        # 添加设置项示例
        self.dark_mode_checkbox = QCheckBox("启用深色模式")
        self.dark_mode_checkbox.setChecked(self.theme_settings.get('dark_mode', False))
        self.theme_edit = QLineEdit(self.theme_settings.get('theme', "默认主题"))

        form_layout.addRow("主题:", self.theme_edit)
        form_layout.addRow("", self.dark_mode_checkbox)

        appearance_tab.setLayout(form_layout)
        self.tab_widget.addTab(appearance_tab, "外观设置")

    def add_import_export_tab(self):
        """添加导入导出设置 tab"""
        import_export_tab = QWidget()
        form_layout = QFormLayout()

        # 修改导入设置项
        # self.import_dir_edit = QLineEdit("默认导入目录")  # 删除该行
        self.import_size = QSpinBox()  # 新增该行
        self.import_size.setRange(1, 1024)  # 设置范围为 1 - 1024 MB
        self.import_size.setValue(self.import_settings.get('import_size', 100))  # 从设置读取或使用默认值 100 MB
        self.import_size.setSuffix(" MB")  # 设置后缀

        form_layout.addRow("最大导入大小:", self.import_size)  # 修改标签

        # 添加 PDF 导入方式选择
        pdf_label = QLabel("PDF 导入方式:")
        self.pdf_import_group = QButtonGroup()
        markitdown_radio = QRadioButton("markitdown")
        marker_pdf_radio = QRadioButton("marker-pdf")
        docling_radio = QRadioButton("docling")

        # 从设置中获取并设置默认选中项
        pdf_method = self.import_settings.get('pdf_import_method', "markitdown")
        if pdf_method == "markitdown":
            markitdown_radio.setChecked(True)
        elif pdf_method == "marker-pdf":
            marker_pdf_radio.setChecked(True)
        elif pdf_method == "docling":
            docling_radio.setChecked(True)

        self.pdf_import_group.addButton(markitdown_radio)
        self.pdf_import_group.addButton(marker_pdf_radio)
        self.pdf_import_group.addButton(docling_radio)

        pdf_buttons_layout = QVBoxLayout()
        pdf_buttons_layout.addWidget(markitdown_radio)
        pdf_buttons_layout.addWidget(marker_pdf_radio)
        pdf_buttons_layout.addWidget(docling_radio)

        form_layout.addRow(pdf_label, pdf_buttons_layout)

        # 添加 MD 导入方式选择
        md_label = QLabel("MD 导入方式:")
        self.md_import_group = QButtonGroup()
        markitdown_md_radio = QRadioButton("markitdown")
        marker_pdf_md_radio = QRadioButton("marker-pdf")
        docling_md_radio = QRadioButton("docling")

        # 从设置中获取并设置默认选中项
        md_method = self.import_settings.get('md_import_method', "markitdown")
        if md_method == "markitdown":
            markitdown_md_radio.setChecked(True)
        elif md_method == "marker-pdf":
            marker_pdf_md_radio.setChecked(True)
        elif md_method == "docling":
            docling_md_radio.setChecked(True)

        self.md_import_group.addButton(markitdown_md_radio)
        self.md_import_group.addButton(marker_pdf_md_radio)
        self.md_import_group.addButton(docling_md_radio)

        md_buttons_layout = QVBoxLayout()
        md_buttons_layout.addWidget(markitdown_md_radio)
        md_buttons_layout.addWidget(marker_pdf_md_radio)
        md_buttons_layout.addWidget(docling_md_radio)

        form_layout.addRow(md_label, md_buttons_layout)

        import_export_tab.setLayout(form_layout)
        self.tab_widget.addTab(import_export_tab, "导入导出设置")

    def save_settings(self):
        """保存所有设置项"""
        settings_manager = SettingsManager()

        # 保存通用设置
        general_settings = {
            'auto_save': self.auto_save_checkbox.isChecked(),
            'auto_save_interval': self.auto_save_interval.value()
        }
        settings_manager.create_settings('general', general_settings)

        # 保存编辑器设置
        editor_settings = {
            'font_size': self.font_size_spin.value(),
            'font_family': self.font_family_edit.text()
        }
        settings_manager.create_settings('editor', editor_settings)

        # 保存外观设置
        appearance_settings = {
            'dark_mode': self.dark_mode_checkbox.isChecked(),
            'theme': self.theme_edit.text()
        }
        settings_manager.create_settings('theme', appearance_settings)

        # 修改保存的导入导出设置
        import_export_settings = {
            'import_size': self.import_size.value(),  # 新增该行
            'pdf_import_method': self.pdf_import_group.checkedButton().text(),
            'md_import_method': self.md_import_group.checkedButton().text()
        }
        settings_manager.create_settings('import', import_export_settings)

        self.accept()