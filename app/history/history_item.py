# -*- coding: utf-8 -*-
"""
历史记录项组件
用于显示单个历史记录的信息
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QFont, QPen, QPainter, QColor, QFontMetrics
from app.preference.style_constants import (
    NEUTRAL_50, NEUTRAL_100, NEUTRAL_200, NEUTRAL_300, NEUTRAL_500, NEUTRAL_600, NEUTRAL_700, NEUTRAL_900,
    PRIMARY_50, PRIMARY_100, PRIMARY_200, PRIMARY_300, PRIMARY_500, PRIMARY_600, PRIMARY_700, 
    SPACING_XS, SPACING_SM, SPACING_MD, SPACING_LG, RADIUS_SM, RADIUS_MD, 
    FONT_SIZE_SM, FONT_SIZE_XS, FONT_SIZE_MD,
    LINE_HEIGHT_NORMAL
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
        
        # 设置固定高度
        self.setFixedHeight(56)  # 增加高度以提供更好的视觉效果
        
        # 更新样式
        self.update_style()
    
    def _get_readable_change_type(self, change_type):
        """将变更类型转换为可读的文本"""
        # 检查是否为当前版本的特殊标识
        if change_type == 'current_version':
            return '当前版本'
            
        type_map = {
            'content_create': '创建',
            'content_update': '内容更新',
            'title_update': '重命名',
            'setting_update': '设置更新',
            'page_engine_update': '引擎更新'
        }
        return type_map.get(change_type.lower(), change_type)
    
    def paintEvent(self, event):
        """重写绘制事件，按照设计原则优化布局和样式"""
        # 创建画家对象
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)  # 抗锯齿
        painter.save()
        
        # 绘制背景 - 应用TDesign设计原则
        if self.is_selected:
            # 选中状态：使用更明显的蓝色背景，增强对比度
            painter.setBrush(QColor(PRIMARY_100))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().adjusted(4, 2, -4, -2), RADIUS_MD, RADIUS_MD)
        elif self.is_hovered:
            # 悬停状态：使用浅蓝色背景
            painter.setBrush(QColor(PRIMARY_50))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().adjusted(4, 2, -4, -2), RADIUS_MD, RADIUS_MD)
        else:
            # 默认状态：使用白色背景
            painter.setBrush(QColor(NEUTRAL_50))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(self.rect().adjusted(4, 2, -4, -2), RADIUS_MD, RADIUS_MD)
        
        # 获取文本内容
        type_text = self.type_label.text()
        time_text = self.time_label.text()
        
        # 设置字体 - 应用TDesign字体系统
        # 变更类型字体（中等粗体）
        type_font = QFont()
        type_font.setWeight(QFont.Weight.Medium)  # 中等粗体
        type_font.setPointSize(FONT_SIZE_SM)
        
        # 时间字体（常规）
        time_font = QFont()
        time_font.setPointSize(FONT_SIZE_XS)
        
        # 设置边距和间距 - 应用Robin Williams设计原则
        horizontal_margin = 16  # 水平边距
        vertical_margin = 12     # 垂直边距
        text_spacing = 16       # 文本间距
        
        # 计算文本位置（应用Robin Williams设计原则）
        # 1. 亲密性：将相关元素组织在一起
        # 2. 对齐：确保元素有清晰的对齐方式
        # 3. 重复：在整个设计中重复视觉元素
        # 4. 对比：使用对比吸引注意力
        
        # 垂直居中计算
        center_y = self.height() // 2
        
        # 绘制变更类型文本（左侧）
        painter.setFont(type_font)
        if self.is_selected:
            painter.setPen(QColor(PRIMARY_700))  # 选中时使用更深的蓝色
        else:
            painter.setPen(QColor(NEUTRAL_900))  # 默认使用深色文本
        
        # 应用对比原则：变更类型使用深色强调
        type_metrics = QFontMetrics(type_font)
        type_width = type_metrics.horizontalAdvance(type_text)
        type_y = center_y + (type_metrics.ascent() - type_metrics.descent()) // 2
        painter.drawText(horizontal_margin, type_y, type_text)
        
        # 绘制时间文本（右侧）
        painter.setFont(time_font)
        if self.is_selected:
            painter.setPen(QColor(PRIMARY_600))  # 选中时使用深蓝色
        else:
            painter.setPen(QColor(NEUTRAL_500))  # 默认使用灰色
        
        # 应用对比原则：时间使用灰色，与变更类型形成对比
        time_metrics = QFontMetrics(time_font)
        time_width = time_metrics.horizontalAdvance(time_text)
        time_x = self.width() - horizontal_margin - time_width
        time_y = center_y + (time_metrics.ascent() - time_metrics.descent()) // 2
        painter.drawText(time_x, time_y, time_text)
        
        # 绘制底部分割线（应用亲密性原则：分割线将不同项分组）
        painter.setPen(QPen(QColor(NEUTRAL_200), 1))
        line_y = self.height() - 1
        painter.drawLine(horizontal_margin, line_y, self.width() - horizontal_margin, line_y)
        
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