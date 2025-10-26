from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QColorDialog
from PySide6.QtGui import QColor
from PySide6.QtCore import Signal

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
        
        # 颜色显示按钮
        self.color_button = QPushButton()
        self.color_button.setFixedSize(32, 32)
        self.update_color_display()
        
        # 选择颜色按钮
        self.select_button = QPushButton("选择颜色")
        self.select_button.clicked.connect(self.open_color_dialog)
        
        layout.addWidget(self.color_button)
        layout.addWidget(self.select_button)
        layout.addStretch()
        
        self.setLayout(layout)
        
    def update_color_display(self):
        """更新颜色显示"""
        if self.current_color:
            # 设置按钮背景色
            self.color_button.setStyleSheet(f"""
                background-color: {self.current_color};
                border: 1px solid #cccccc;
                border-radius: 4px;
            """)
        else:
            # 显示默认状态
            self.color_button.setStyleSheet("""
                background-color: #ffffff;
                border: 1px solid #cccccc;
                border-radius: 4px;
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