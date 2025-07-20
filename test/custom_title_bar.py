import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QHBoxLayout,QVBoxLayout,
                               QPushButton, QLabel, QStyle)
from PySide6.QtCore import Qt, QPoint, QSize
from PySide6.QtGui import QIcon, QAction, QPainter, QPainterPath, QColor

class MacOSButton(QPushButton):
    def __init__(self, button_type, parent=None):
        super().__init__(parent)
        self.button_type = button_type
        self.setFixedSize(12, 12)  # 缩小按钮尺寸
        self.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 6px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 10);
            }
        """)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        path = QPainterPath()
        path.addEllipse(self.rect())
        painter.fillPath(path, self._get_button_color())

    def _get_button_color(self):
        colors = {
            "close": QColor(255, 92, 88),
            "minimize": QColor(255, 189, 46),
            "maximize": QColor(39, 201, 63)
        }
        return colors.get(self.button_type, QColor(200, 200, 200))

class CustomTitleBar(QWidget):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.setFixedHeight(28)  # 更紧凑的标题栏高度
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
        """)
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(12, 0, 12, 0)
        self.layout.setSpacing(8)

        # macOS 风格按钮组
        self.btn_close = MacOSButton("close", self)
        self.btn_min = MacOSButton("minimize", self)
        self.btn_max = MacOSButton("maximize", self)

        # 按钮点击功能
        self.btn_close.clicked.connect(self.window.close)
        self.btn_min.clicked.connect(self.window.showMinimized)
        self.btn_max.clicked.connect(self.window.showFullScreen)  # macOS 全屏模式

        # 标题标签
        self.title = QLabel("Custom Title Bar")
        self.title.setStyleSheet("""
            QLabel {
                color: #333;
                font-family: -apple-system;
                font-size: 13px;
            }
        """)

        # 右侧自定义按钮
        self.btn_custom = QPushButton("⚙️", self)
        self.btn_custom.setFixedSize(24, 24)
        self.btn_custom.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 4px;
                background: rgba(0, 0, 0, 0);
            }
            QPushButton:hover {
                background: rgba(0, 0, 0, 10);
            }
        """)

        # 布局
        self.layout.addWidget(self.btn_close)
        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_max)
        self.layout.addStretch()
        self.layout.addWidget(self.title)
        self.layout.addStretch()
        self.layout.addWidget(self.btn_custom)

        # 窗口拖动处理
        self.drag_pos = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.window.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.window.move(event.globalPosition().toPoint() - self.drag_pos)
            event.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("macOS Style Window")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(600, 400)
        self.setStyleSheet("""
            QMainWindow {
                background: white;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            }
        """)

        # 添加自定义标题栏
        self.title_bar = CustomTitleBar(self)
        self.setMenuWidget(self.title_bar)

        # 窗口内容
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 10, 20, 20)
        layout.addWidget(QLabel("Main Content Area"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # 确保样式一致性
    window = MainWindow()
    window.show()
    sys.exit(app.exec())