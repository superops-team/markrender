from PySide6.QtWidgets import (
    QListWidget,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QStyle,
)
from PySide6.QtGui import QPainter, QFont, QColor, QIcon, QPen
from PySide6.QtCore import QSize, QEvent, QRect, Qt

from utils.logger_utils import logger
from utils.path import get_icon_path
from utils.time_utils import get_readable_time, format_datetime


class QuickPickItemDelegate(QStyledItemDelegate):
    # 定义 tag 到颜色的映射表，方便扩展
    tag_color_map = {
        'md': QColor(159, 200, 156), 
        'markdown': QColor(159, 200, 156), 
        'pdf': QColor(145, 200, 228),
        'png': QColor(173, 178, 212),  
        'jpeg': QColor(15, 130, 140), 
        'csv': QColor(163, 220, 154), 
        'docx': QColor(151, 176, 103),
        'doc': QColor(151, 176, 103),
        'xls': QColor(67, 112, 87),
        'xlsx': QColor(67, 112, 87),
        'ppt': QColor(255, 166, 115),
        'pptx': QColor(255, 166, 115),
        'epub': QColor(100, 226, 183),
        'board': QColor(100, 226, 183),
    }
    default_color = QColor(211, 218, 217, 100)    # 默认灰色

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

        if option.state & QStyle.State_Selected:
            painter.setBrush(QColor(25, 144, 255, 38))
            painter.setPen(Qt.NoPen)  # 设置无边框
            # 添加绘制背景矩形的代码
            painter.drawRect(option.rect)  # 绘制完整项的背景
        elif option.state & QStyle.State_MouseOver:
            painter.setBrush(QColor(25, 144, 255, 25))
            painter.setPen(Qt.NoPen)  # 设置无边框
            painter.drawRect(option.rect)  # 绘制完整项的背景
        else:
            painter.setPen(Qt.NoPen)  # 设置无边框

        # Get item data
        item_data = index.data(Qt.UserRole)
        if item_data:
            title = item_data.get('title', '')
            modified_time = item_data.get('updated_at', '')
            formatted_time = self._format_time(modified_time)
            page_type = item_data.get('page_type', '')  # 获取文件类型字段
            if not page_type:
                page_type = 'markdown'
            item_created_at = format_datetime(item_data.get('created_at', ''))
            preview_suffix = f'创建时间：{item_created_at}'
            preview = "{} {}".format(page_type, preview_suffix)

            # 设置边距
            margin = 10
            text_rect = option.rect.adjusted(margin, margin, -margin, -margin)

            # 获取文件类型对应的颜色
            background_color = self.default_color
            
            # 图标尺寸设置
            icon_size = 16
            tag_width = icon_size + 8  # 图标宽度 + 边距
            tag_height = icon_size + 8  # 图标高度 + 边距
            tag_x = text_rect.x()
            tag_y = text_rect.y() + 5
            
            # 绘制标签背景
            painter.setBrush(background_color)
            painter.drawRoundedRect(tag_x, tag_y, tag_width, tag_height, 4, 4)
            
            # 获取并绘制图标
            icon = self._get_icon_for_file_type(page_type)
            # 图标在圆角矩形中的位置，居中显示
            icon_x = tag_x + (tag_width - icon_size) // 2
            icon_y = tag_y + (tag_height - icon_size) // 2
            painter.drawPixmap(icon_x, icon_y, icon.pixmap(icon_size, icon_size))

            # 调整标题的起始位置，避免和标签重叠
            text_rect = text_rect.adjusted(tag_width + 5, 0, 0, 0)

            # 绘制标题
            title_font = QFont()
            title_font.setBold(True)
            painter.setFont(title_font)
            if option.state & QStyle.State_Selected:
                painter.setPen(QColor(25, 144, 255))  # #006400 --> 1990ff
            else:
                painter.setPen(QColor(0, 0, 0))
            # Bug fix: 使用 horizontalAdvance 替代 width
            title_width = painter.fontMetrics().horizontalAdvance(title)
            painter.drawText(text_rect.x(), text_rect.y() + 15, title)

            # 绘制修改时间
            time_font = QFont()
            time_font.setPointSize(9)
            painter.setFont(time_font)
            if option.state & QStyle.State_Selected:
                painter.setPen(QColor(25, 144, 255))  # #006400 --> 1990ff
            else:
                painter.setPen(QColor(100, 100, 100))
            time_x = text_rect.x() + title_width + 10
            painter.drawText(time_x, text_rect.y() + 15, formatted_time)

            # 绘制预览
            preview_font = QFont()
            preview_font.setPointSize(9)
            if option.state & QStyle.State_Selected:
                painter.setPen(QColor(25, 144, 255))  # #006400--->1990ff
            else:
                painter.setPen(QColor(100, 100, 100))
            painter.setFont(preview_font)
            preview_rect = text_rect.adjusted(0, 20, 0, 0)
            painter.drawText(preview_rect, Qt.TextSingleLine, preview)

            # 鼠标悬停时绘制删除按钮
            if option.state & QStyle.State_MouseOver:
                button_width = 20
                button_height = 20
                button_x = option.rect.right() - button_width - 10
                button_y = option.rect.top() + (option.rect.height() - button_height) // 2
                # 扩大点击区域，四周各增加 5 像素
                padding = 10
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

        # 绘制分割线
        if option.state & QStyle.State_Selected:
            painter.setPen(QPen(QColor(25, 144, 255), 1))  # 选中状态使用蓝色
        else:
            painter.setPen(QPen(QColor(220, 220, 220), 1))  # 非选中状态使用浅灰色
        line_y = option.rect.bottom() - 1
        painter.drawLine(option.rect.left() + margin, line_y, option.rect.right() - margin, line_y)

        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index):
        # Bug fix: Call width() method to get the width value
        return QSize(option.rect.width(), 50)

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.MouseButtonDblClick and event.button() == Qt.LeftButton:
            logger.debug("检测到鼠标双击事件")
            item_data = index.data(Qt.UserRole)
            if not item_data:
                return
            if isinstance(self.parent, QListWidget):
                quick_pick_panel = self.parent.parent()
                quick_pick_panel.edit_item(index)
        if event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
            # 从 index 中获取当前项的删除按钮区域
            delete_button_rect = index.data(Qt.UserRole + 1)
            if not delete_button_rect:
                return
            if not delete_button_rect.contains(event.pos()):
                return
            item_data = index.data(Qt.UserRole)
            if item_data and 'id' in item_data:
                logger.debug(f"尝试删除ID为 {item_data['id']} 的记录")
                if isinstance(self.parent, QListWidget):
                    quick_pick_panel = self.parent.parent()
                    if hasattr(quick_pick_panel, 'delete_item'):
                        quick_pick_panel.delete_item(item_data['id'])
        return super().editorEvent(event, model, option, index)