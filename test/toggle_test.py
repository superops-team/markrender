import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFrame
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("展开折叠按钮示例")
        self.setGeometry(100, 100, 800, 600)

        # 创建侧边栏
        self.sidebar = QFrame(self)
        self.sidebar.setFrameShape(QFrame.StyledPanel)
        self.sidebar.setFixedWidth(200)
        self.sidebar.setStyleSheet("background-color: lightgray;")

        # 创建按钮
        self.toggle_button = QPushButton("折叠", self)
        self.toggle_button.setFixedSize(100, 30)
        self.toggle_button.setStyleSheet(
            "background-color: red; color: white;")

        # 设置布局
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.toggle_button)
        layout.addWidget(self.sidebar)
        self.setCentralWidget(central_widget)

        # 连接信号槽
        self.toggle_button.clicked.connect(self.toggle_sidebar)

        # 初始状态：侧边栏展开
        self.sidebar_visible = True

    def toggle_sidebar(self):
        """切换侧边栏的显示状态并更新按钮样式"""
        if self.sidebar_visible:
            # 折叠侧边栏
            self.sidebar.hide()
            self.toggle_button.setText("展开")
            self.toggle_button.setStyleSheet(
                "background-color: green; color: white;")
        else:
            # 展开侧边栏
            self.sidebar.show()
            self.toggle_button.setText("折叠")
            self.toggle_button.setStyleSheet(
                "background-color: red; color: white;")
        self.sidebar_visible = not self.sidebar_visible


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
