#!/usr/bin/env python3
"""
测试主窗口圆角效果
"""

import sys
import os
from PySide6.QtCore import Qt, QRectF
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QRegion, QPainterPath

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.preference import AppStyle

class TestMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("主窗口圆角测试")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # 设置无边框窗口
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        label = QLabel("这是一个测试主窗口，用于验证圆角效果")
        layout.addWidget(label)
        
        # 设置基础样式
        self.setStyleSheet(AppStyle().get_main_style())
        
        # 应用圆角效果
        self.apply_rounded_corners()

    def apply_rounded_corners(self):
        """应用圆角效果到主窗口"""
        # 创建圆角矩形路径
        path = QPainterPath()
        radius = 10  # 圆角半径
        rect = self.rect()
        path.addRoundedRect(QRectF(rect), radius, radius)
        
        # 创建区域并应用到窗口
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    def resizeEvent(self, event):
        """窗口大小改变时重新应用圆角效果"""
        super().resizeEvent(event)
        self.apply_rounded_corners()

def main():
    app = QApplication(sys.argv)
    
    window = TestMainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()