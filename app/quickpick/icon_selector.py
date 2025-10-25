from PySide6.QtWidgets import (
    QWidget, QComboBox, QHBoxLayout, QLabel, QPushButton,
    QGridLayout, QScrollArea, QVBoxLayout, QDialog, QFrame,
    QSizePolicy, QApplication, QLineEdit
)
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtCore import Qt, QSize, Signal
import os
from utils.path import get_icon_path

class IconSelectorDialog(QDialog):
    """图标选择对话框"""
    icon_selected = Signal(str)  # 发送选中的图标名称
    
    def __init__(self, current_icon=None, parent=None):
        super().__init__(parent)
        self.current_icon = current_icon
        self.selected_icon = current_icon
        self.setWindowTitle("选择图标")
        self.setMinimumSize(600, 400)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # 搜索框
        search_layout = QHBoxLayout()
        search_label = QLabel("搜索图标:")
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("输入图标名称...")
        self.search_edit.textChanged.connect(self.filter_icons)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_edit)
        layout.addLayout(search_layout)
        
        # 图标网格
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.icon_container = QWidget()
        self.icon_layout = QGridLayout(self.icon_container)
        self.icon_layout.setSpacing(10)
        self.icon_layout.setContentsMargins(10, 10, 10, 10)
        
        self.scroll_area.setWidget(self.icon_container)
        layout.addWidget(self.scroll_area)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("取消")
        self.ok_button = QPushButton("确定")
        self.ok_button.setDefault(True)
        self.ok_button.setEnabled(False)
        
        self.cancel_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.accept)
        
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.ok_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # 加载图标
        self.load_icons()
        
    def load_icons(self):
        """加载所有可用图标"""
        # 清空现有图标
        for i in reversed(range(self.icon_layout.count())):
            item = self.icon_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                widget.setParent(None)
                
        # 获取图标目录
        icons_dir = os.path.join(os.getcwd(), "icons")
        if not os.path.exists(icons_dir):
            return
            
        # 获取所有SVG图标文件
        icon_files = [f for f in os.listdir(icons_dir) if f.endswith(".svg")]
        self.all_icons = []
        
        for i, icon_file in enumerate(icon_files):
            icon_name = os.path.splitext(icon_file)[0]
            self.all_icons.append(icon_name)
            
            # 创建图标按钮
            icon_button = QPushButton()
            icon_button.setFixedSize(60, 60)
            icon_button.setIconSize(QSize(32, 32))
            
            # 尝试加载图标
            icon_path = os.path.join(icons_dir, icon_file)
            if os.path.exists(icon_path):
                icon = QIcon(icon_path)
                icon_button.setIcon(icon)
            
            icon_button.setToolTip(icon_name)
            icon_button.setCheckable(True)
            
            # 如果是当前图标，选中它
            if icon_name == self.current_icon:
                icon_button.setChecked(True)
                self.selected_icon = icon_name
                self.ok_button.setEnabled(True)
                
            # 连接点击事件
            # 使用lambda的默认参数来捕获当前值
            icon_button.clicked.connect(
                lambda checked, name=icon_name, btn=icon_button: 
                self.on_icon_selected(name, btn)
            )
            
            # 添加到网格布局
            row = i // 8
            col = i % 8
            self.icon_layout.addWidget(icon_button, row, col)
            
        # 收集所有图标按钮
        self.all_icon_buttons = []
        for i in range(self.icon_layout.count()):
            item = self.icon_layout.itemAt(i)
            if item and item.widget():
                self.all_icon_buttons.append(item.widget())
        
    def filter_icons(self, text):
        """根据搜索文本过滤图标"""
        text = text.lower()
        for button in self.all_icon_buttons:
            icon_name = button.toolTip().lower()
            button.setVisible(text in icon_name)
            
    def on_icon_selected(self, icon_name, button):
        """处理图标选择"""
        # 取消其他按钮的选中状态
        for btn in self.all_icon_buttons:
            if btn != button:
                btn.setChecked(False)
                
        # 设置选中状态
        self.selected_icon = icon_name if button.isChecked() else None
        self.ok_button.setEnabled(button.isChecked())
        
    def get_selected_icon(self):
        """获取选中的图标名称"""
        return self.selected_icon

class IconSelectorWidget(QWidget):
    """图标选择器组件"""
    icon_changed = Signal(str)  # 当图标改变时发出信号
    
    def __init__(self, current_icon=None, parent=None):
        super().__init__(parent)
        self.current_icon = current_icon
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 图标显示标签
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(32, 32)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_icon_display()
        
        # 选择按钮
        self.select_button = QPushButton("选择图标")
        self.select_button.clicked.connect(self.open_icon_selector)
        
        layout.addWidget(self.icon_label)
        layout.addWidget(self.select_button)
        layout.addStretch()
        
        self.setLayout(layout)
        
    def update_icon_display(self):
        """更新图标显示"""
        if self.current_icon:
            icon_path = os.path.join(os.getcwd(), "icons", f"{self.current_icon}.svg")
            if os.path.exists(icon_path):
                icon = QIcon(icon_path)
                self.icon_label.setPixmap(icon.pixmap(32, 32))
            else:
                self.icon_label.setText("❓")
        else:
            self.icon_label.setText("无")
            
    def open_icon_selector(self):
        """打开图标选择对话框"""
        dialog = IconSelectorDialog(self.current_icon, self)
        if dialog.exec():
            selected_icon = dialog.get_selected_icon()
            if selected_icon != self.current_icon:
                self.current_icon = selected_icon
                self.update_icon_display()
                self.icon_changed.emit(selected_icon)
                
    def get_selected_icon(self):
        """获取选中的图标"""
        return self.current_icon
        
    def set_icon(self, icon_name):
        """设置图标"""
        self.current_icon = icon_name
        self.update_icon_display()