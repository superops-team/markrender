import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 关键：获取 React 打包后的 index.html 绝对路径
    #react_build_path = os.path.abspath("./frontend/excalidraw/dist/index.html")  # 替换为你的 build 目录路径
    react_build_path = os.path.abspath("./app/editor/plugins/excalidraw/index.html")  # 替换为你的 build 目录路径
    url = QUrl.fromLocalFile(react_build_path)

    view = QWebEngineView()
    view.load(url)
    view.show()

    sys.exit(app.exec())
