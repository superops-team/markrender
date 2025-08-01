from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QPainter, QPainterPath, QColor, QPen
from PySide6.QtCore import Qt

class MacOSButton(QPushButton):
    """
    自定义 macOS 风格按钮
    """
    def __init__(self, button_type, parent=None):
        super().__init__(parent)
        self.button_type = button_type
        self.setFixedSize(12, 12)  # 调整按钮尺寸为 12px
        self.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 6px;
                padding: 0px;
                margin-right: 3px;  /* 缩小右侧间距 */
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 20);
            }
        """)
        self.setMouseTracking(True)
        self.hovered = False

    def enterEvent(self, event):
        self.hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hovered = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        path = QPainterPath()
        path.addEllipse(self.rect())
        painter.fillPath(path, self._get_button_color())

        if self.hovered:
            painter.setPen(QPen(QColor(0, 0, 0), 1, Qt.SolidLine))
            if self.button_type == "close":
                # 绘制关闭符号 "×"
                painter.drawLine(4, 4, 8, 8)
                painter.drawLine(4, 8, 8, 4)
            elif self.button_type == "minimize":
                # 绘制最小化符号 "-"
                painter.drawLine(4, 6, 8, 6)
            elif self.button_type == "maximize":
                # 绘制最大化符号 "+"
                painter.drawLine(4, 6, 8, 6)
                painter.drawLine(6, 4, 6, 8)

    def _get_button_color(self):
        colors = {
            "close": QColor(255, 92, 88),
            "minimize": QColor(255, 189, 46),
            "maximize": QColor(39, 201, 63)
        }
        return colors.get(self.button_type, QColor(200, 200, 200))