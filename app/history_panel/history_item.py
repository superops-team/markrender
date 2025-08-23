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
from utils.time_utils import get_readable_time, get_duration


class HistoryItemDelegate(QStyledItemDelegate):
    # 定义 tag 到颜色的映射表，方便扩展
    tag_color_map = {
        'md': QColor(159, 200, 156), 
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
    }
    default_color = QColor(128, 128, 128)    # 默认灰色

    def __init__(self, parent=None):
        super().__init__(parent)
        self.delete_icon = QIcon(get_icon_path('trash-selected'))  # 假设图标文件名为 trash
        #self.delete_selected_icon = QIcon(get_icon_path('trash-selected'))
        self.parent = parent  # 保存父对象引用

    def _format_time(self, modified_time):
        return get_readable_time(modified_time)

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
            tag = item_data.get('tags', '')  # 获取 tag 字段
            if tag != 'md':
                if item_data.get('status', '') == 'processing':
                    preview_suffix = '后台处理中...'
                else:
                    preview_suffix = "处理耗时：{}s".format(get_duration(item_data.get('converter_start', ''), item_data.get('converter_end', '')).seconds)
            else:
                item_created_at = item_data.get('created_at', '')
                preview_suffix = f'创建时间：{item_created_at}'
            preview = "{} {}".format(item_data.get('converter', ''), preview_suffix)

            # 设置边距
            margin = 10
            text_rect = option.rect.adjusted(margin, margin, -margin, -margin)

            # 绘制 tag 角标
            if tag:
                tag_font = QFont()
                tag_font.setPointSize(8)
                painter.setFont(tag_font)
                painter.setPen(QColor(255, 255, 255))

                # 根据 tag 内容获取对应的颜色，如果没有匹配则使用默认颜色
                painter.setBrush(self.tag_color_map.get(tag, self.default_color))

                tag_width = painter.fontMetrics().horizontalAdvance(tag) + 8
                tag_height = 16
                tag_x = text_rect.x()  # 设置 x 坐标为文本区域左侧
                tag_y = text_rect.y() + 5
                painter.drawRoundedRect(tag_x, tag_y, tag_width, tag_height, 4, 4)
                painter.drawText(tag_x + 4, tag_y + 12, tag)

                # 调整标题的起始位置，避免和 tag 角标重叠
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
            if item_data:
                if isinstance(self.parent, QListWidget):
                    history_panel = self.parent.parent()
                    if hasattr(history_panel, 'edit_item_title'):
                        # 修改为调用新对话框
                        history_panel.edit_item_title(index)
        if event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
            logger.debug("检测到鼠标左键释放事件")
            # 从 index 中获取当前项的删除按钮区域
            delete_button_rect = index.data(Qt.UserRole + 1)
            if delete_button_rect:
                # 直接使用 event.pos()，不进行坐标转换
                if delete_button_rect.contains(event.pos()):
                    logger.debug("点击了删除按钮")
                    item_data = index.data(Qt.UserRole)
                    if item_data and 'id' in item_data:
                        logger.debug(f"尝试删除ID为 {item_data['id']} 的记录")
                        if isinstance(self.parent, QListWidget):
                            history_panel = self.parent.parent()
                            if hasattr(history_panel, 'delete_item'):
                                history_panel.delete_item(item_data['id'])
        return super().editorEvent(event, model, option, index)