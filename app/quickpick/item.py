import os
import sys
from PySide6.QtWidgets import (
    QTreeWidget,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QStyle,
)
from PySide6.QtGui import QPainter, QFont, QColor, QIcon, QPen, QFontMetrics
from PySide6.QtCore import QSize, QEvent, QRect, Qt

from utils.logger_utils import logger
from utils.path import get_icon_path
from utils.time_utils import get_readable_time, format_datetime


# 首先添加必要的导入
from app.preference.style_constants import (
    NEUTRAL_900, NEUTRAL_600, NEUTRAL_500, NEUTRAL_400, NEUTRAL_300, NEUTRAL_100, NEUTRAL_0,
    PRIMARY_700, PRIMARY_600, PRIMARY_300, PRIMARY_100, PRIMARY_50,
    SPACING_XS, SPACING_SM, SPACING_MD, SPACING_LG, SPACING_XL,
    RADIUS_SM, RADIUS_MD, RADIUS_LG,
    FONT_SIZE_XS, FONT_SIZE_SM, FONT_SIZE_MD, FONT_SIZE_LG
)


class QuickPickItemDelegate(QStyledItemDelegate):
    # 使用统一的设计令牌系统定义tag颜色映射表 - 优化颜色搭配，参考现代软件设计
    # 遵循TDesign色彩设计原则，使用更和谐的颜色搭配
    tag_color_map = {
        'md': QColor(59, 130, 246),        # 蓝色系 - Markdown文档 (参考TDesign/现代设计)
        'markdown': QColor(59, 130, 246),
        'pdf': QColor(239, 68, 68),        # 红色系 - PDF文档 (参考TDesign/现代设计)
        'png': QColor(139, 92, 246),       # 紫色系 - 图片文件 (参考TDesign/现代设计)
        'jpeg': QColor(139, 92, 246),
        'csv': QColor(34, 197, 94),        # 绿色系 - 数据文件 (参考TDesign/现代设计)
        'docx': QColor(59, 130, 246),
        'doc': QColor(59, 130, 246),
        'xls': QColor(34, 197, 94),
        'xlsx': QColor(34, 197, 94),
        'ppt': QColor(245, 158, 11),       # 橙色系 - 演示文稿 (参考TDesign/现代设计)
        'pptx': QColor(245, 158, 11),
        'epub': QColor(168, 85, 247),      # 紫色系 - 电子书 (参考TDesign/现代设计)
        'board': QColor(171, 71, 188),     # 创意紫色 - 画布文件
        'excalidraw': QColor(171, 71, 188), # 创意紫色 - Excalidraw文件
    }
    default_color = QColor(107, 114, 128)  # 中性灰色 - 默认文件类型颜色

    # 定义文件类型到图标名称的映射
    file_type_to_icon = {
        'md': 'textarea',
        'markdown': 'textarea',
        'pdf': 'book',
        'png': 'card-checklist',
        'jpeg': 'card-checklist',
        'csv': 'textarea',
        'docx': 'book',
        'doc': 'book',
        'xls': 'card-checklist',
        'xlsx': 'card-checklist',
        'ppt': 'card-checklist',
        'pptx': 'card-checklist',
        'epub': 'book',
        'board': 'diagram',
        'excalidraw': 'excalidraw',
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.delete_icon = QIcon(get_icon_path('trash-selected'))  # 假设图标文件名为 trash
        self.more_icon = QIcon(get_icon_path('gear'))  # 使用齿轮图标作为三个点图标
        self.add_icon = QIcon(get_icon_path('plus-square'))  # 使用正确的加号图标
        # 初始化图标缓存
        self.icon_cache = {}
        self._parent = parent  # 保存父对象引用
        # 添加鼠标位置跟踪
        self._hovered_index = None

    def _format_time(self, modified_time):
        # 如果 modified_time 是字符串，直接返回它
        if isinstance(modified_time, str):
            return modified_time
        # 否则使用 get_readable_time 处理
        return get_readable_time(modified_time)

    def _get_icon_for_file_type(self, file_type, icon_type=None, icon_path=None):
        """根据文件类型、图标类型或图标路径获取对应的图标"""
        # 优先使用icon_path字段
        if icon_path:
            # 检查缓存中是否已有该图标
            if icon_path in self.icon_cache:
                return self.icon_cache[icon_path]
            
            # 处理相对路径和绝对路径
            if os.path.isabs(icon_path):
                # 绝对路径直接使用
                icon_file_path = icon_path
            else:
                # 相对路径，需要根据应用根目录解析
                if hasattr(sys, '_MEIPASS'):
                    # 打包环境
                    icon_file_path = os.path.join(sys._MEIPASS, icon_path)  # type: ignore
                else:
                    # 开发环境 - 修复路径解析逻辑
                    # 直接使用相对路径，因为图标目录就在项目根目录下
                    icon_file_path = icon_path
            
            # 检查文件是否存在
            if os.path.exists(icon_file_path):
                # 直接使用图标路径创建图标对象
                icon = QIcon(icon_file_path)
                # 缓存图标
                self.icon_cache[icon_path] = icon
                return icon
            else:
                # 文件不存在，回退到默认处理
                # 不打印错误信息，避免日志污染
                pass
        
        # 其次使用icon_type字段
        if icon_type:
            # 检查缓存中是否已有该图标
            if icon_type in self.icon_cache:
                return self.icon_cache[icon_type]
            # 获取图标路径并创建图标对象
            icon_path_result = get_icon_path(icon_type)
            icon = QIcon(icon_path_result)
            # 缓存图标
            self.icon_cache[icon_type] = icon
            return icon
        
        # 检查缓存中是否已有该图标
        if file_type in self.icon_cache:
            return self.icon_cache[file_type]
        # 根据文件类型获取图标名称
        icon_name = self.file_type_to_icon.get(file_type.lower(), 'file-earmark-plus')
        # 获取图标路径并创建图标对象
        icon_path_result = get_icon_path(icon_name)
        icon = QIcon(icon_path_result)
        # 缓存图标
        self.icon_cache[file_type] = icon
        return icon

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index):
        painter.save()

        # 获取选项矩形区域 - 忽略类型检查错误
        option_rect = option.rect  # type: ignore

        # 改善选中和悬停状态的对比度 - 对齐和对比度优化
        # type: ignore 注释用于忽略类型检查错误
        if option.state & QStyle.StateFlag.State_Selected:  # type: ignore
            # 增强选中状态的对比度 - 使用更深的背景色
            painter.setBrush(QColor(PRIMARY_100))  # 更明显的选中背景，增强对比度
            painter.setPen(Qt.PenStyle.NoPen)
            # 减少圆角半径，使选中状态更紧凑
            painter.drawRoundedRect(option_rect, RADIUS_SM, RADIUS_SM)  # type: ignore
        elif option.state & QStyle.StateFlag.State_MouseOver:  # type: ignore
            # 增强悬停状态的对比度
            painter.setBrush(QColor(PRIMARY_50))  # 浅蓝色悬停背景
            painter.setPen(Qt.PenStyle.NoPen)
            # 减少圆角半径，使悬停状态更紧凑
            painter.drawRoundedRect(option_rect, RADIUS_SM, RADIUS_SM)  # type: ignore
        else:
            # 默认状态使用浅色背景，增强整体对比度
            painter.setBrush(QColor(NEUTRAL_0))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(option_rect)  # type: ignore

        # 绘制一个透明的占位符，确保整个item区域都能响应事件
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(option_rect)

        # Get item data
        item_data = index.data(Qt.ItemDataRole.UserRole)
        if item_data:
            title = item_data.get('title', '')
            modified_time = item_data.get('updated_at', '')
            formatted_time = self._format_time(modified_time)
            page_type = item_data.get('page_type', '')
            if not page_type:
                page_type = 'markdown'
            item_created_at = item_data.get('created_at', '')
            # 只显示时间，不显示"创建时间："前缀
            # 确保preview始终是字符串类型
            if isinstance(item_created_at, str):
                preview = item_created_at
            elif item_created_at:
                preview = format_datetime(item_created_at)
            else:
                preview = ""

            # 优化边距和布局 - 使用统一间距 - 增强对齐性 - 减少间距使布局更紧凑
            margin_top = SPACING_XS
            margin_bottom = SPACING_XS
            margin_left = SPACING_SM  # 为图标留出空间
            margin_right = SPACING_SM
            text_rect = option_rect.adjusted(margin_left, margin_top, -margin_right, -margin_bottom)  # type: ignore

            # 获取文件类型对应的颜色
            tag_color = self.tag_color_map.get(page_type.lower(), self.default_color)

            # 优化图标尺寸和位置 - 对齐优化 - 减小图标尺寸使布局更紧凑
            icon_size = 16  # 减小图标尺寸，提高紧凑性
            tag_width = icon_size + 8
            tag_height = icon_size + 8
            tag_x = option_rect.x() + SPACING_SM  # 固定图标位置，确保对齐
            tag_y = text_rect.y() + (text_rect.height() - tag_height) // 2  # 垂直居中对齐

            # 绘制更美观的标签背景 - 重复原则（使用统一圆角）- 减小圆角使布局更紧凑
            painter.setBrush(tag_color)
            painter.setPen(Qt.PenStyle.NoPen)
            # 减少圆角半径，使标签更紧凑
            painter.drawRoundedRect(tag_x, tag_y, tag_width, tag_height, RADIUS_SM//2, RADIUS_SM//2)  # 统一圆角半径

            # 获取并绘制图标
            icon_type = item_data.get('icon_type')
            icon_path = item_data.get('icon_path')
            icon_color = item_data.get('icon_color')  # 获取图标颜色
            icon = self._get_icon_for_file_type(page_type, icon_type, icon_path)
            # 图标在圆角矩形中的位置，居中显示 - 对齐优化
            icon_x = tag_x + (tag_width - icon_size) // 2
            icon_y = tag_y + (tag_height - icon_size) // 2
            
            # 如果有图标颜色设置，则应用颜色
            if icon_color:
                # 创建带颜色的图标
                pixmap = icon.pixmap(icon_size, icon_size)
                # 创建一个彩色的pixmap
                colored_pixmap = pixmap.copy()
                # 使用QPainter在图标上绘制颜色
                painter2 = QPainter(colored_pixmap)
                painter2.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
                painter2.fillRect(colored_pixmap.rect(), QColor(icon_color))
                painter2.end()
                painter.drawPixmap(icon_x, icon_y, colored_pixmap)
            else:
                # 使用默认绘制方式
                painter.drawPixmap(icon_x, icon_y, icon.pixmap(icon_size, icon_size))

            # 调整标题的起始位置，避免和标签重叠 - 亲密性优化
            content_rect = text_rect.adjusted(tag_width + SPACING_SM, 0, 0, 0)  # 使用统一间距

            # 绘制标题 - 优化字体和颜色 - 对比度优化
            title_font = QFont()
            title_font.setBold(True)
            title_font.setPointSize(FONT_SIZE_MD)  # 使用中等字体大小，增强可读性
            painter.setFont(title_font)
            if option.state & QStyle.StateFlag.State_Selected:  # type: ignore
                painter.setPen(QColor(PRIMARY_700))  # 更深的蓝色，增强对比度
            else:
                painter.setPen(QColor(NEUTRAL_900))  # 深灰色文本，增强对比度

            # 计算标题可用宽度，保留时间显示空间
            available_width = content_rect.width() - 100  # 保留空间给时间显示
            title_metrics = painter.fontMetrics()
            elided_title = title_metrics.elidedText(title, Qt.TextElideMode.ElideRight, available_width)
            title_width = title_metrics.horizontalAdvance(elided_title)
            
            # 垂直居中对齐标题
            title_y = content_rect.y() + title_metrics.ascent() + (content_rect.height() - title_metrics.height()) // 3

            # 绘制标题
            painter.drawText(content_rect.x(), title_y, elided_title)

            # 绘制修改时间 - 优化亲密性
            time_font = QFont()
            time_font.setPointSize(FONT_SIZE_XS)  # 使用小字体大小
            painter.setFont(time_font)
            if option.state & QStyle.StateFlag.State_Selected:  # type: ignore
                painter.setPen(QColor(PRIMARY_600))  # 选中状态蓝色，增强对比度
            else:
                painter.setPen(QColor(NEUTRAL_500))  # 中性灰色
            time_x = content_rect.x() + title_width + SPACING_XS  # 使用小间距
            time_y = title_y  # 与标题在同一行
            painter.drawText(time_x, time_y, formatted_time)

            # 绘制预览 - 优化布局和颜色，确保文本完整显示
            preview_font = QFont()
            preview_font.setPointSize(FONT_SIZE_XS)  # 使用小字体大小
            painter.setFont(preview_font)
            if option.state & QStyle.StateFlag.State_Selected:  # type: ignore
                painter.setPen(QColor(NEUTRAL_600))  # 选中状态的辅助文本，增强对比度
            else:
                painter.setPen(QColor(NEUTRAL_500))  # 辅助文本颜色

            # 计算预览文本可用宽度
            preview_available_width = content_rect.width() - 20  # 保留一些边距
            preview_metrics = painter.fontMetrics()
            # 确保preview是字符串类型
            preview_str = str(preview) if preview else ""
            elided_preview = preview_metrics.elidedText(preview_str, Qt.TextElideMode.ElideRight, preview_available_width)

            # 修正预览文本的Y坐标位置，确保完整显示 - 对齐优化
            preview_y = content_rect.y() + content_rect.height() - preview_metrics.height() // 2

            # 在标题下方添加page_type标签 - 增强亲密性
            type_label_font = QFont()
            type_label_font.setPointSize(FONT_SIZE_XS-1)  # 使用更小的字体大小
            type_label_font.setBold(True)
            painter.setFont(type_label_font)
            if option.state & QStyle.StateFlag.State_Selected:  # type: ignore
                painter.setPen(QColor(NEUTRAL_600))  # 选中状态的辅助文本颜色
            else:
                painter.setPen(tag_color)  # 使用与图标相同的颜色

            # 计算page_type标签宽度
            type_metrics = QFontMetrics(type_label_font)
            type_text_width = type_metrics.horizontalAdvance(page_type.upper())

            # 绘制page_type标签
            type_x = content_rect.x()
            type_y = preview_y
            painter.drawText(type_x, type_y, page_type.upper())

            # 调整时间显示位置，在page_type标签右侧 - 亲密性优化
            time_x_offset = type_text_width + SPACING_XS  # page_type标签宽度 + 小间距
            painter.setFont(preview_font)  # 恢复预览文本字体
            if option.state & QStyle.StateFlag.State_Selected:  # type: ignore
                painter.setPen(QColor(NEUTRAL_600))  # 选中状态的辅助文本
            else:
                painter.setPen(QColor(NEUTRAL_500))  # 辅助文本颜色

            preview_x = content_rect.x() + time_x_offset + SPACING_XS
            painter.drawText(preview_x, type_y, elided_preview)

        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index):
        # 减小项高度，提升紧凑性
        return QSize(option.rect.width(), 56)  # 从80px减少到56px，使布局更紧凑  # type: ignore

    def editorEvent(self, event, model, option, index):
        # 移除双击和按钮点击事件处理，改为右键菜单触发
        return super().editorEvent(event, model, option, index)