from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QColorDialog, QLabel
from PySide6.QtGui import QColor
from PySide6.QtCore import Signal, Qt
from app.preference.style_constants import SPACING_SM
from app.preference.style_utils import create_button_style

class ColorSelectorWidget(QWidget):
    """颜色选择器组件"""
    color_changed = Signal(str)  # 当颜色改变时发出信号，传递颜色值（十六进制字符串）
    
    def __init__(self, current_color=None, parent=None):
        super().__init__(parent)
        self.current_color = current_color
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING_SM)
        
        # 颜色显示按钮 - 增大尺寸并支持点击
        self.color_button = QPushButton()
        self.color_button.setFixedSize(40, 40)
        self.color_button.setCursor(Qt.PointingHandCursor)  # 设置鼠标指针为手型
        self.color_button.clicked.connect(self.open_color_dialog)
        self.update_color_display()
        
        # 添加提示文本
        self.color_label_text = QLabel("点击选择颜色")
        self.color_label_text.setStyleSheet("""
            color: #666666;
            font-size: 12px;
        """)
        
        layout.addWidget(self.color_button)
        layout.addWidget(self.color_label_text)
        
        # 设置整体组件高度
        self.setMinimumHeight(40)
        
        self.setLayout(layout)
        
    def update_color_display(self):
        """更新颜色显示"""
        if self.current_color:
            # 设置按钮背景色
            self.color_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.current_color};
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                }}
                QPushButton:hover {{
                    border-color: #999999;
                }}
                QPushButton:pressed {{
                    opacity: 0.9;
                }}
            """)
        else:
            # 显示默认状态
            self.color_button.setStyleSheet("""
                QPushButton {{
                    background-color: #ffffff;
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                }}
                QPushButton:hover {{
                    border-color: #999999;
                }}
                QPushButton:pressed {{
                    opacity: 0.9;
                }}
            """)
            
    def open_color_dialog(self):
        """打开颜色选择对话框"""
        # 将当前颜色转换为QColor对象
        initial_color = QColor()
        if self.current_color:
            initial_color.setNamedColor(self.current_color)
            
        # 打开颜色选择对话框
        color = QColorDialog.getColor(initial_color, self, "选择图标颜色")
        if color.isValid():
            # 将QColor转换为十六进制字符串
            color_hex = color.name()
            self.current_color = color_hex
            self.update_color_display()
            self.color_changed.emit(color_hex)
            
    def get_selected_color(self):
        """获取选中的颜色"""
        return self.current_color
        
    def set_color(self, color_hex):
        """设置颜色"""
        self.current_color = color_hex
        self.update_color_display()