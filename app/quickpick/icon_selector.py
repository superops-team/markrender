from PySide6.QtWidgets import (
    QWidget, QComboBox, QHBoxLayout, QLabel, QPushButton,
    QGridLayout, QScrollArea, QVBoxLayout, QDialog, QFrame,
    QSizePolicy, QApplication, QLineEdit, QGroupBox
)
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor
from PySide6.QtCore import Qt, QSize, Signal
import os
import sys
from utils.path import get_icon_path
from app.preference.style_constants import (
    NEUTRAL_0, NEUTRAL_50, NEUTRAL_100, NEUTRAL_200, NEUTRAL_300, NEUTRAL_400, NEUTRAL_500, NEUTRAL_600, NEUTRAL_700, NEUTRAL_900,
    PRIMARY_50, PRIMARY_100, PRIMARY_200, PRIMARY_500, PRIMARY_600, PRIMARY_700,
    SPACING_SM, SPACING_MD, SPACING_LG, SPACING_XL,
    FONT_SIZE_SM, FONT_SIZE_MD, FONT_SIZE_LG,
    RADIUS_SM, RADIUS_MD, RADIUS_LG,
    BUTTON_HEIGHT_SM, BUTTON_HEIGHT_MD
)
from app.preference.style_utils import create_dialog_style, create_button_style

class IconSelectorDialog(QDialog):
    """图标选择对话框"""
    icon_selected = Signal(str)  # 发送选中的图标名称
    
    def __init__(self, current_icon=None, parent=None):
        super().__init__(parent)
        self.current_icon = current_icon
        self.selected_icon = current_icon
        self.setWindowTitle("选择图标")
        self.setMinimumSize(700, 500)  # 增大对话框尺寸，提供更好的用户体验
        # 设置窗口标志，确保对话框行为正确
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        # 使用统一的样式生成器
        self.setStyleSheet(create_dialog_style())
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)  # 统一内边距
        layout.setSpacing(SPACING_LG)  # 统一间距
        
        # 标题标签
        title_label = QLabel("选择图标")
        title_label.setStyleSheet(f"""
            color: {NEUTRAL_900};
            font-size: {FONT_SIZE_LG}px;
            font-weight: 600;
            margin-bottom: {SPACING_SM}px;
        """)
        layout.addWidget(title_label)
        
        # 搜索框
        search_group = QGroupBox()
        search_group.setStyleSheet(f"""
            QGroupBox {{
                border: none;
                background-color: transparent;
                margin: 0px;
                padding: 0px;
            }}
        """)
        search_layout = QHBoxLayout(search_group)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(SPACING_SM)
        
        search_label = QLabel("搜索图标:")
        search_label.setStyleSheet(f"""
            color: {NEUTRAL_700};
            font-size: {FONT_SIZE_MD}px;
            font-weight: 500;
            min-width: 80px;
        """)
        
        self.search_edit = QLineEdit()
        self.search_edit.setMinimumHeight(BUTTON_HEIGHT_MD)
        self.search_edit.setPlaceholderText("输入图标名称...")
        self.search_edit.setStyleSheet(f"""
            QLineEdit {{
                background-color: {NEUTRAL_50};
                border: 1px solid {NEUTRAL_200};
                border-radius: {RADIUS_MD}px;
                padding: 0px {SPACING_MD}px;
                font-size: {FONT_SIZE_MD}px;
                color: {NEUTRAL_700};
            }}
            QLineEdit:hover {{
                border-color: {NEUTRAL_300};
            }}
            QLineEdit:focus {{
                border-color: {PRIMARY_500};
                outline: none;
                background-color: {NEUTRAL_0};
            }}
        """)
        
        self.search_edit.textChanged.connect(self.filter_icons)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_edit)
        layout.addWidget(search_group)
        
        # 图标网格容器
        icon_container = QWidget()
        icon_container.setStyleSheet(f"""
            QWidget {{
                background-color: {NEUTRAL_50};
                border: 1px solid {NEUTRAL_200};
                border-radius: {RADIUS_MD}px;
            }}
        """)
        icon_container_layout = QVBoxLayout(icon_container)
        icon_container_layout.setContentsMargins(16, 16, 16, 16)
        
        # 图标网格说明
        icon_count_label = QLabel(f"共 {len(os.listdir(os.path.join(os.getcwd(), 'icons'))) if os.path.exists(os.path.join(os.getcwd(), 'icons')) else 0} 个图标")
        icon_count_label.setStyleSheet(f"""
            color: {NEUTRAL_600};
            font-size: {FONT_SIZE_SM}px;
            margin-bottom: {SPACING_SM}px;
        """)
        icon_container_layout.addWidget(icon_count_label)
        
        # 图标网格
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: transparent;
                border: none;
            }}
            QScrollArea > QWidget > QWidget {{
                background-color: transparent;
            }}
            QScrollBar:vertical {{
                width: 8px;
                background-color: {NEUTRAL_100};
                margin: 0px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {NEUTRAL_300};
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {NEUTRAL_400};
            }}
            QScrollBar::sub-line:vertical,
            QScrollBar::add-line:vertical {{
                height: 0px;
                subcontrol-origin: margin;
            }}
        """)
        
        self.icon_container = QWidget()
        self.icon_layout = QGridLayout(self.icon_container)
        self.icon_layout.setSpacing(SPACING_MD)  # 增加图标间距
        self.icon_layout.setContentsMargins(0, 0, 0, 0)
        
        self.scroll_area.setWidget(self.icon_container)
        icon_container_layout.addWidget(self.scroll_area)
        
        layout.addWidget(icon_container, 1)  # 让图标区域占据更多空间
        
        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(SPACING_MD)
        button_layout.addStretch()
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.setStyleSheet(create_button_style("secondary", "md"))
        self.cancel_button.setFixedWidth(100)
        
        self.ok_button = QPushButton("确定")
        self.ok_button.setStyleSheet(create_button_style("primary", "md"))
        self.ok_button.setFixedWidth(100)
        self.ok_button.setDefault(True)
        self.ok_button.setEnabled(False)
        
        self.cancel_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.accept)
        
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
                
        # 获取图标目录 - 修复打包环境中的路径问题
        if hasattr(sys, '_MEIPASS'):
            # 在打包环境中，从_MEIPASS路径获取icons目录
            icons_dir = os.path.join(getattr(sys, '_MEIPASS'), "icons")
        else:
            # 在开发环境中，从当前工作目录获取icons目录
            icons_dir = os.path.join(os.getcwd(), "icons")
            
        if not os.path.exists(icons_dir):
            # 如果上述路径不存在，尝试从脚本所在目录获取icons目录
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icons_dir = os.path.join(os.path.dirname(script_dir), "icons")
            # 如果仍然不存在，尝试从项目根目录获取
            if not os.path.exists(icons_dir):
                icons_dir = os.path.join(os.path.dirname(os.path.dirname(script_dir)), "icons")
            
        if not os.path.exists(icons_dir):
            return
            
        # 获取所有SVG图标文件并排序
        icon_files = sorted([f for f in os.listdir(icons_dir) if f.endswith(".svg")])
        self.all_icons = []
        self.all_icon_buttons = []
        
        for i, icon_file in enumerate(icon_files):
            icon_name = os.path.splitext(icon_file)[0]
            self.all_icons.append(icon_name)
            
            # 创建图标按钮 - 使用更现代的样式
            icon_button = QPushButton()
            icon_button.setFixedSize(60, 60)  # 减小按钮尺寸
            icon_button.setIconSize(QSize(28, 28))  # 减小图标尺寸
            
            # 设置按钮样式
            icon_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {NEUTRAL_0};
                    border: 1px solid {NEUTRAL_200};
                    border-radius: {RADIUS_SM}px;
                    padding: {SPACING_SM}px;
                }}
                QPushButton:hover {{
                    background-color: {PRIMARY_50};
                    border-color: {PRIMARY_200};
                }}
                QPushButton:checked {{
                    background-color: {PRIMARY_100};
                    border-color: {PRIMARY_500};
                }}
            """)
            
            # 尝试加载图标
            icon_path = os.path.join(icons_dir, icon_file)
            if os.path.exists(icon_path):
                icon = QIcon(icon_path)
                icon_button.setIcon(icon)
            else:
                # 在打包环境中，尝试从_MEIPASS路径加载图标
                if hasattr(sys, '_MEIPASS'):
                    packed_icon_path = os.path.join(getattr(sys, '_MEIPASS'), 'icons', icon_file)
                    if os.path.exists(packed_icon_path):
                        icon = QIcon(packed_icon_path)
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
            
            self.all_icon_buttons.append(icon_button)
            
            # 添加到网格布局 - 每行9个图标
            row = i // 9
            col = i % 9
            self.icon_layout.addWidget(icon_button, row, col)
            
        # 更新图标数量显示
        icon_count_label = self.findChild(QLabel)
        if icon_count_label and "共" in icon_count_label.text():
            icon_count_label.setText(f"共 {len(icon_files)} 个图标")
        
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
        layout.setSpacing(SPACING_SM)
        
        # 图标显示区域 - 增大尺寸以完整显示图标
        # 使用QPushButton代替QWidget，使其可点击
        self.icon_display_button = QPushButton()
        self.icon_display_button.setFixedSize(40, 40)
        self.icon_display_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {NEUTRAL_0};
                border: 1px solid {NEUTRAL_200};
                border-radius: {RADIUS_SM}px;
                padding: 0px;
            }}
            QPushButton:hover {{
                background-color: {PRIMARY_50};
                border-color: {PRIMARY_200};
            }}
            QPushButton:pressed {{
                background-color: {PRIMARY_100};
            }}
        """)
        # 设置鼠标指针为手型
        self.icon_display_button.setCursor(Qt.PointingHandCursor)
        # 连接点击事件
        self.icon_display_button.clicked.connect(self.open_icon_selector)
        
        # 图标显示布局
        icon_display_layout = QHBoxLayout(self.icon_display_button)
        icon_display_layout.setContentsMargins(2, 2, 2, 2)  # 减小内边距，给图标更多空间
        
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(36, 36)  # 增大图标标签尺寸
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_display_layout.addWidget(self.icon_label)
        
        self.update_icon_display()
        
        # 只添加图标显示按钮
        layout.addWidget(self.icon_display_button)
        # 添加提示文本
        self.icon_label_text = QLabel("点击选择图标")
        self.icon_label_text.setStyleSheet(f"""
            color: {NEUTRAL_600};
            font-size: {FONT_SIZE_SM}px;
        """)
        layout.addWidget(self.icon_label_text)
        
        # 设置整体组件的最小高度
        self.setMinimumHeight(40)
        
        self.setLayout(layout)
        
    def update_icon_display(self):
        """更新图标显示"""
        if self.current_icon:
            icon_path = get_icon_path(self.current_icon)
            if os.path.exists(icon_path):
                icon = QIcon(icon_path)
                # 使用scaled方法确保图标完整显示，不被裁剪
                pixmap = icon.pixmap(QSize(36, 36))
                self.icon_label.setPixmap(pixmap)
            else:
                self.icon_label.clear()
        else:
            self.icon_label.clear()
            
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