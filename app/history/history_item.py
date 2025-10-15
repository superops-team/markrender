# -*- coding: utf-8 -*-
"""
历史记录项组件
用于显示单个历史记录的信息
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPen, QPainter, QColor, QPixmap
from app.preference.style_constants import (
    NEUTRAL_200, NEUTRAL_500, NEUTRAL_600, NEUTRAL_700, NEUTRAL_900,
    PRIMARY_50, PRIMARY_100, PRIMARY_300, PRIMARY_500, PRIMARY_600, PRIMARY_700, 
    SPACING_SM, SPACING_MD, SPACING_LG, RADIUS_SM, RADIUS_MD, 
    FONT_SIZE_SM, FONT_SIZE_XS
)
from utils.time_utils import get_readable_time


class HistoryItemWidget(QWidget):
    """历史记录项控件"""
    
    def __init__(self, history_record, parent=None):
        super().__init__(parent)
        self.history_record = history_record
        self.is_selected = False  # 添加选中状态标志
        self.is_hovered = False  # 添加悬停状态标志
        self.setup_ui()
        
    def setup_ui(self):
        # 设置对象名以便调试
        self.setObjectName("HistoryItemWidget")
        
        # 创建隐藏的标签用于存储文本内容，但不显示
        # 变更类型标签
        change_type = getattr(self.history_record, 'change_type', '')
        # 统一变更类型显示
        type_text = self._get_readable_change_type(change_type)
        self.type_label = QLabel(type_text)
        self.type_label.hide()  # 隐藏标签，我们手动绘制
        
        # 变更时间
        change_at = getattr(self.history_record, 'change_at', None)
        time_text = get_readable_time(change_at) if change_at else "未知时间"
        self.time_label = QLabel(time_text)
        self.time_label.hide()  # 隐藏标签，我们手动绘制
        
        # 设置固定高度和背景透明
        self.setFixedHeight(40)
        self.setAttribute(Qt.WA_TranslucentBackground)  # 背景透明，让我们手动绘制背景
        
        # 更新样式
        self.update_style()
    
    def _get_readable_change_type(self, change_type):
        """将变更类型转换为可读的文本"""
        type_map = {
            'content_create': '创建',
            'content_update': '内容更新',
            'title_update': '重命名',
            'setting_update': '设置更新'
        }
        return type_map.get(change_type.lower(), change_type)
    
    def paintEvent(self, event):
        """重写绘制事件，添加分割线并优化居中显示"""
        # 不调用super().paintEvent(event)，避免双重绘制背景
        
        # 创建画家对象
        painter = QPainter(self)
        painter.save()
        
        # 绘制选中状态的背景
        if self.is_selected:
            painter.setBrush(QColor(PRIMARY_100))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(self.rect().adjusted(2, 1, -2, -1), RADIUS_MD, RADIUS_MD)
        elif self.is_hovered:
            painter.setBrush(QColor(PRIMARY_50))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(self.rect().adjusted(2, 1, -2, -1), RADIUS_MD, RADIUS_MD)
        
        # 获取文本内容
        type_text = self.type_label.text()
        time_text = self.time_label.text()
        
        # 设置边距
        margin = 12  # 左右边距
        text_height = 20  # 文本高度
        
        # 计算垂直居中位置
        center_y = self.height() // 2
        text_y = center_y + 5  # 微调基线位置
        
        # 绘制变更类型文本
        type_font = QFont()
        type_font.setBold(True)
        type_font.setPointSize(FONT_SIZE_XS)
        painter.setFont(type_font)
        
        if self.is_selected:
            painter.setPen(QColor(PRIMARY_600))
        else:
            painter.setPen(QColor(PRIMARY_500))
        
        # 绘制文本（左侧对齐）
        painter.drawText(margin, text_y, type_text)
        
        # 绘制时间文本（右侧对齐）
        time_font = QFont()
        time_font.setPointSize(FONT_SIZE_SM)
        painter.setFont(time_font)
        
        if self.is_selected:
            painter.setPen(QColor(PRIMARY_700))
        else:
            painter.setPen(QColor(NEUTRAL_500))
        
        # 计算文本宽度用于右对齐
        time_metrics = painter.fontMetrics()
        time_width = time_metrics.horizontalAdvance(time_text)
        time_x = self.width() - margin - time_width
        
        painter.drawText(time_x, text_y, time_text)
        
        # 移除底部分割线绘制，避免横线贯穿内容区域
        # 分割线由QListWidget的样式统一管理
        
        painter.restore()
        
    def update_style(self):
        """更新样式，现在通过重绘实现"""
        # 触发重绘以更新手动绘制的内容
        self.update()
            
    def set_selected(self, selected):
        """设置选中状态"""
        self.is_selected = selected
        self.update_style()
        
    def enterEvent(self, event):
        """处理鼠标进入事件"""
        super().enterEvent(event)
        self.is_hovered = True
        if not self.is_selected:  # 只有在未选中状态下才更新悬停样式
            self.update_style()
            
    def leaveEvent(self, event):
        """处理鼠标离开事件"""
        super().leaveEvent(event)
        self.is_hovered = False
        if not self.is_selected:  # 只有在未选中状态下才更新样式
            self.update_style()
            
    def mousePressEvent(self, event):
        """处理鼠标点击事件"""
        super().mousePressEvent(event)
        # 不在这里处理选中状态切换，让HistoryPanel统一管理互斥选中