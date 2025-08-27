from PySide6.QtWidgets import (
    QListWidget,
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
    NEUTRAL_600, NEUTRAL_500, NEUTRAL_900, 
    NEUTRAL_200,  # 确保单独列出NEUTRAL_200
    PRIMARY_50, PRIMARY_100, PRIMARY_300, PRIMARY_700, PRIMARY_600,
    SPACING_XS, SPACING_SM, SPACING_MD, SPACING_LG,
    RADIUS_SM, RADIUS_MD,
    FONT_SIZE_XS, FONT_SIZE_SM, FONT_SIZE_MD
)


class QuickPickItemDelegate(QStyledItemDelegate):
    # 使用统一的设计令牌系统定义tag颜色映射表
    tag_color_map = {
        'md': QColor(34, 197, 94),        # 绿色系 - 成功色
        'markdown': QColor(34, 197, 94),
        'pdf': QColor(59, 130, 246),      # 蓝色系 - 文档色
        'png': QColor(139, 92, 246),      # 紫色系 - 图片色
        'jpeg': QColor(139, 92, 246),
        'csv': QColor(245, 158, 11),      # 橙色系 - 数据色
        'docx': QColor(59, 130, 246),
        'doc': QColor(59, 130, 246),
        'xls': QColor(245, 158, 11),
        'xlsx': QColor(245, 158, 11),
        'ppt': QColor(239, 68, 68),       # 红色系 - 演示色
        'pptx': QColor(239, 68, 68),
        'epub': QColor(34, 197, 94),
        'board': QColor(168, 85, 247),    # 创意紫色
    }
    default_color = QColor(156, 163, 175)  # 中性灰色

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
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.delete_icon = QIcon(get_icon_path('trash-selected'))  # 假设图标文件名为 trash
        # 初始化图标缓存
        self.icon_cache = {}
        self.parent = parent  # 保存父对象引用

    def _format_time(self, modified_time):
        return get_readable_time(modified_time)

    def _get_icon_for_file_type(self, file_type):
        """根据文件类型获取对应的图标"""
        # 检查缓存中是否已有该图标
        if file_type in self.icon_cache:
            return self.icon_cache[file_type]
        # 根据文件类型获取图标名称
        icon_name = self.file_type_to_icon.get(file_type.lower(), 'file-earmark-plus')
        # 获取图标路径并创建图标对象
        icon_path = get_icon_path(icon_name)
        icon = QIcon(icon_path)
        # 缓存图标
        self.icon_cache[file_type] = icon
        return icon

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index):
        painter.save()

        # 改善选中和悬停状态的对比度 - 对齐和对比度优化
        if option.state & QStyle.State_Selected:
            painter.setBrush(QColor(PRIMARY_100))  # 更明显的选中背景，增强对比度
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(option.rect.adjusted(SPACING_SM, SPACING_XS, -SPACING_SM, -SPACING_XS), RADIUS_MD, RADIUS_MD)  # 使用统一圆角
        elif option.state & QStyle.State_MouseOver:
            painter.setBrush(QColor(PRIMARY_50))  # 浅蓝色悬停背景
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(option.rect.adjusted(SPACING_SM, SPACING_XS, -SPACING_SM, -SPACING_XS), RADIUS_MD, RADIUS_MD)
        else:
            painter.setPen(Qt.NoPen)

        # Get item data
        item_data = index.data(Qt.UserRole)
        if item_data:
            title = item_data.get('title', '')
            modified_time = item_data.get('updated_at', '')
            formatted_time = self._format_time(modified_time)
            page_type = item_data.get('page_type', '')
            if not page_type:
                page_type = 'markdown'
            item_created_at = format_datetime(item_data.get('created_at', ''))
            # 只显示时间，不显示"创建时间："前缀
            preview = item_created_at

            # 优化边距和布局 - 使用统一间距
            margin = SPACING_LG  # 增加边距提升可读性
            text_rect = option.rect.adjusted(margin, margin, -margin, -margin)

            # 获取文件类型对应的颜色
            tag_color = self.tag_color_map.get(page_type.lower(), self.default_color)

            # 优化图标尺寸和位置 - 对齐优化
            icon_size = 18  # 稍微增大图标
            tag_width = icon_size + 10
            tag_height = icon_size + 10
            tag_x = text_rect.x()
            tag_y = text_rect.y() + 2

            # 绘制更美观的标签背景 - 重复原则（使用统一圆角）
            painter.setBrush(tag_color)
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(tag_x, tag_y, tag_width, tag_height, RADIUS_SM, RADIUS_SM)  # 统一圆角半径
            # 获取并绘制图标
            icon = self._get_icon_for_file_type(page_type)
            # 图标在圆角矩形中的位置，居中显示 - 对齐优化
            icon_x = tag_x + (tag_width - icon_size) // 2
            icon_y = tag_y + (tag_height - icon_size) // 2
            painter.drawPixmap(icon_x, icon_y, icon.pixmap(icon_size, icon_size))

            # 调整标题的起始位置，避免和标签重叠 - 亲密性优化
            text_rect = text_rect.adjusted(tag_width + SPACING_MD, 0, 0, 0)  # 使用统一间距

            # 绘制标题 - 优化字体和颜色 - 对比度优化
            title_font = QFont()
            title_font.setBold(True)
            title_font.setPointSize(FONT_SIZE_MD)  # 使用统一字体大小
            painter.setFont(title_font)
            if option.state & QStyle.State_Selected:
                painter.setPen(QColor(PRIMARY_700))  # 更深的蓝色，增强对比度
            else:
                painter.setPen(QColor(NEUTRAL_900))  # 深灰色文本，增强对比度

            # 计算标题可用宽度，保留时间显示空间
            available_width = text_rect.width() - 120  # 保留120px给时间显示
            title_metrics = painter.fontMetrics()
            elided_title = title_metrics.elidedText(title, Qt.TextElideMode.ElideRight, available_width)
            title_width = title_metrics.horizontalAdvance(elided_title)
            title_y = text_rect.y() + 16  # 调整基线位置
            painter.drawText(text_rect.x(), title_y, elided_title)

            # 绘制修改时间 - 优化亲密性
            time_font = QFont()
            time_font.setPointSize(FONT_SIZE_XS)  # 使用统一字体大小
            painter.setFont(time_font)
            if option.state & QStyle.State_Selected:
                painter.setPen(QColor(PRIMARY_600))  # 选中状态蓝色，增强对比度
            else:
                painter.setPen(QColor(NEUTRAL_500))  # 中性灰色
            time_x = text_rect.x() + title_width + SPACING_SM  # 使用统一间距
            painter.drawText(time_x, title_y, formatted_time)

            # 绘制预览 - 优化布局和颜色，确保文本完整显示
            preview_font = QFont()
            preview_font.setPointSize(FONT_SIZE_SM)  # 使用统一字体大小
            if option.state & QStyle.State_Selected:
                painter.setPen(QColor(NEUTRAL_600))  # 选中状态的辅助文本，增强对比度
            else:
                painter.setPen(QColor(NEUTRAL_500))  # 辅助文本颜色
            painter.setFont(preview_font)

            # 计算预览文本可用宽度，避免被删除按钮遮挡
            preview_available_width = text_rect.width() - 60  # 保留空间给删除按钮
            preview_metrics = painter.fontMetrics()
            elided_preview = preview_metrics.elidedText(preview, Qt.TextElideMode.ElideRight, preview_available_width)

            # 修正预览文本的Y坐标位置，确保完整显示 - 对齐优化
            preview_y = text_rect.y() + 38  # 增加Y偏移量，从标题下方留出足够空间

            # 在标题下方、时间左侧添加page_type标签
            type_label_font = QFont()
            type_label_font.setPointSize(FONT_SIZE_XS)  # 使用统一字体大小
            type_label_font.setBold(True)
            painter.setFont(type_label_font)
            if option.state & QStyle.State_Selected:
                painter.setPen(QColor(NEUTRAL_600))  # 选中状态的辅助文本颜色
            else:
                painter.setPen(tag_color)  # 使用与图标相同的颜色

            # 计算page_type标签宽度
            type_metrics = QFontMetrics(type_label_font)
            type_text_width = type_metrics.horizontalAdvance(page_type.upper())

            # 绘制page_type标签
            painter.drawText(text_rect.x(), preview_y, page_type.upper())

            # 调整时间显示位置，在page_type标签右侧 - 亲密性优化
            time_x_offset = type_text_width + SPACING_SM  # page_type标签宽度 + 统一间距
            painter.setFont(preview_font)  # 恢复预览文本字体
            if option.state & QStyle.State_Selected:
                painter.setPen(QColor(NEUTRAL_600))  # 选中状态的辅助文本
            else:
                painter.setPen(QColor(NEUTRAL_500))  # 辅助文本颜色

            painter.drawText(text_rect.x() + time_x_offset, preview_y, preview)

            # 鼠标悬停时绘制删除按钮 - 优化样式
            if option.state & QStyle.State_MouseOver:
                button_width = 24  # 稍微增大按钮
                button_height = 24
                button_x = option.rect.right() - button_width - SPACING_LG  # 使用统一间距
                button_y = option.rect.top() + (option.rect.height() - button_height) // 2
                # 扩大点击区域，四周各增加 8 像素
                padding = 8
                # 修改为局部变量，避免所有项共享同一个删除按钮区域
                delete_button_rect = QRect(
                    button_x - padding,
                    button_y - padding,
                    button_width + padding * 2,
                    button_height + padding * 2
                )
                # 存储删除按钮区域到 index 中，用于 editorEvent 判断
                index.model().setData(index, delete_button_rect, Qt.UserRole + 1)
                painter.drawPixmap(
                    button_x, button_y, self.delete_icon.pixmap(
                        button_width, button_height))
            else:
                # 非悬停状态清除存储的删除按钮区域
                index.model().setData(index, None, Qt.UserRole + 1)

        # 在paint方法中使用时也确保正确引用
        # 绘制分割线 - 优化样式 - 对齐优化
        if option.state & QStyle.State_Selected:
            painter.setPen(QPen(QColor(PRIMARY_300), 1))  # 选中状态使用浅蓝色，增强对比度
        else:
            painter.setPen(QPen(QColor(NEUTRAL_200), 1))  # 非选中状态使用浅灰色
        line_y = option.rect.bottom() - 1
        margin = SPACING_LG  # 使用统一的边距
        painter.drawLine(option.rect.left() + margin, line_y, option.rect.right() - margin, line_y)

        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index):
        # 增加项高度，提升视觉舒适度并确保文本完整显示
        return QSize(option.rect.width(), 72)  # 从64px增加到72px，为预览文本提供更多空间

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.MouseButtonDblClick and event.button() == Qt.LeftButton:
            logger.debug("检测到鼠标双击事件")
            item_data = index.data(Qt.UserRole)
            if not item_data:
                return False  # 明确返回False表示事件未处理
            if isinstance(self.parent, QListWidget):
                quick_pick_panel = self.parent.parent()
                quick_pick_panel.edit_item(index)
                return True  # 明确返回True表示事件已处理
        if event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
            # 从 index 中获取当前项的删除按钮区域
            delete_button_rect = index.data(Qt.UserRole + 1)
            if not delete_button_rect:
                return False  # 明确返回False表示事件未处理
            if not delete_button_rect.contains(event.pos()):
                return False  # 明确返回False表示事件未处理
            item_data = index.data(Qt.UserRole)
            if item_data and 'id' in item_data:
                logger.debug(f"尝试删除ID为 {item_data['id']} 的记录")
                if isinstance(self.parent, QListWidget):
                    quick_pick_panel = self.parent.parent()
                    if hasattr(quick_pick_panel, 'delete_item'):
                        quick_pick_panel.delete_item(item_data['id'])
                        return True  # 明确返回True表示事件已处理
        return super().editorEvent(event, model, option, index)