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

from utils.path import get_icon_path
from utils.time_utils import get_readable_time, format_datetime


# 导入TDesign风格的设计令牌
from app.preference.style_constants import (
    NEUTRAL_900, NEUTRAL_800, NEUTRAL_700, NEUTRAL_600, NEUTRAL_500, NEUTRAL_400, NEUTRAL_300, NEUTRAL_200, NEUTRAL_100, NEUTRAL_50, NEUTRAL_0,
    PRIMARY_700, PRIMARY_600, PRIMARY_500, PRIMARY_400, PRIMARY_300, PRIMARY_200, PRIMARY_100, PRIMARY_50,
    SUCCESS_500, WARNING_500, DANGER_500, PURPLE_500, PINK_500, CYAN_500,
    SPACING_XS, SPACING_SM, SPACING_MD, SPACING_LG, SPACING_XL,
    RADIUS_SM, RADIUS_MD, RADIUS_LG, RADIUS_PILL,
    FONT_SIZE_XS, FONT_SIZE_SM, FONT_SIZE_MD, FONT_SIZE_LG,
    LINE_HEIGHT_NORMAL
)


class QuickPickItemDelegate(QStyledItemDelegate):
    # TDesign风格的标签颜色映射 - 基于腾讯蓝系统色，优化色彩搭配以符合Robin Williams设计原则
    # 遵循60-30-10色彩法则：60%主色(PRIMARY)，30%辅助色(SECONDARY)，10%强调色(ACCENT)
    # 同时确保颜色之间的和谐搭配和良好的视觉层次
    tag_color_map = {
        # 主色系列 - 腾讯蓝 (60%主色调，用于主要文档类型)
        'md': PRIMARY_500,        # 腾讯蓝 - Markdown文档
        'markdown': PRIMARY_500,
        'docx': PRIMARY_400,      # 稍浅的蓝色 - Word文档
        'doc': PRIMARY_400,       # 稍浅的蓝色 - Word文档
        
        # 辅助色系列 - 成功绿 (30%辅助色，用于数据类文件)
        'csv': SUCCESS_500,       # TDesign成功色 - CSV数据文件
        'xls': SUCCESS_500,       # TDesign成功色 - Excel文件
        'xlsx': SUCCESS_500,      # TDesign成功色 - Excel文件
        
        # 辅助色系列 - 警告橙 (30%辅助色，用于演示类文件)
        'ppt': WARNING_500,       # TDesign警告色 - PowerPoint演示文稿
        'pptx': WARNING_500,      # TDesign警告色 - PowerPoint演示文稿
        
        # 强调色系列 - 危险红 (10%强调色，用于PDF等特殊文件)
        'pdf': DANGER_500,        # TDesign错误色 - PDF文档
        
        # 强调色系列 - 紫色 (10%强调色，用于媒体类文件)
        'png': PURPLE_500,        # TDesign紫色 - PNG图片文件
        'jpeg': PURPLE_500,       # TDesign紫色 - JPEG图片文件
        'jpg': PURPLE_500,        # TDesign紫色 - JPG图片文件
        'epub': PURPLE_500,       # TDesign紫色 - 电子书文件
        
        # 强调色系列 - 粉色 (10%强调色，用于创意类文件)
        'board': PINK_500,        # TDesign粉色 - 画布文件
        'excalidraw': PINK_500,   # TDesign粉色 - Excalidraw文件
        
        # 特殊色系列 - 青色 (用于文件夹)
        'folder': CYAN_500,       # TDesign天蓝色 - 文件夹
    }
    default_color = NEUTRAL_500  # TDesign中性灰 - 默认文件类型颜色

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
        # 根据文件类型获取图标名称，处理None值情况
        file_type_str = file_type.lower() if file_type is not None else 'markdown'
        icon_name = self.file_type_to_icon.get(file_type_str, 'file-earmark-plus')
        # 获取图标路径并创建图标对象
        icon_path_result = get_icon_path(icon_name)
        icon = QIcon(icon_path_result)
        # 缓存图标
        self.icon_cache[file_type] = icon
        return icon

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index):
        painter.save()
        
        # 启用抗锯齿，使绘制更平滑
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        # 获取选项矩形区域
        option_rect = option.rect
        
        # TDesign风格的状态颜色处理 - 优化点击区域和视觉效果
        if option.state & QStyle.StateFlag.State_Selected:
            # TDesign选中状态 - 使用更轻量的选中背景色，符合自然、务实的设计原则
            painter.setBrush(QColor(245, 249, 255, 180))  # 更轻量的腾讯蓝浅色背景，带透明度
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(option_rect, 6, 6)  # TDesign风格圆角优化
        elif option.state & QStyle.StateFlag.State_MouseOver:
            # TDesign悬停状态 - 使用统一的悬停背景色
            painter.setBrush(NEUTRAL_100)  # TDesign hover background
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(option_rect, 6, 6)

        # Get item data
        item_data = index.data(Qt.ItemDataRole.UserRole)
        if item_data:
            title = item_data.get('title', '')
            modified_time = item_data.get('updated_at', '')
            formatted_time = self._format_time(modified_time)
            page_type = item_data.get('page_type', 'markdown')
            
            # 判断是否为文件夹
            is_folder = item_data.get('is_folder', False)
            
            # 根据层级调整缩进 - TDesign风格的层级展示
            level = item_data.get('level', 0)
            indent = 24 + (level * 16)  # 基础缩进 + 层级缩进
            
            # 获取文件类型对应的颜色 - 使用TDesign色彩系统
            page_type_str = page_type.lower() if page_type is not None else 'markdown'
            tag_color = self.tag_color_map.get(page_type_str, self.default_color) \
                       if not is_folder else self.tag_color_map['folder']
            
            # 图标尺寸和位置 - TDesign规范
            icon_size = 16
            icon_bg_width = 32
            icon_bg_height = 32
            icon_x = option_rect.x() + SPACING_SM + indent
            icon_y = option_rect.y() + (option_rect.height() - icon_bg_height) // 2
            
            # 绘制图标背景 - TDesign风格的圆角矩形，优化颜色对比度和视觉层次
            # 使用更柔和的颜色处理方式，确保整体协调性
            bg_color = QColor(tag_color)
            
            # 根据TDesign设计原则优化颜色：
            # 1. 对比度：确保图标背景与整体背景有足够的对比度
            # 2. 重复：使用一致的颜色处理方式
            # 3. 亲密性：相关文件类型使用相近的颜色
            # 4. 对齐：保持视觉层次的一致性
            
            # 调整颜色饱和度和亮度以获得更好的视觉效果
            h = bg_color.hsvHue()
            s = bg_color.hsvSaturation()
            v = bg_color.value()
            a = bg_color.alpha()
            
            # TDesign推荐的图标背景色优化策略：
            # 1. 对于饱和度较高的颜色，适当降低饱和度以获得更柔和的效果
            # 2. 对于过亮或过暗的颜色，调整亮度以增强可读性
            # 3. 保持颜色的一致性和和谐性
            if s > 150:  # 对于高饱和度颜色
                s = int(s * 0.7)  # 适度降低饱和度
            if v < 180:  # 对于较暗的颜色
                v = min(255, int(v * 1.3))  # 提高亮度
            elif v > 220:  # 对于过亮的颜色
                v = int(v * 0.85)  # 降低亮度
            
            bg_color.setHsv(h, s, v, a)
            
            painter.setBrush(bg_color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(icon_x, icon_y, icon_bg_width, icon_bg_height, 8, 8)  # TDesign圆角8px
            
            # 获取并绘制图标
            icon_type = item_data.get('icon_type')
            icon_path = item_data.get('icon_path')
            icon_color = item_data.get('icon_color', '#FFFFFF')  # 默认白色图标在彩色背景上
            
            # 文件夹使用特殊图标
            if is_folder:
                icon = self._get_icon_for_file_type('folder', icon_type, icon_path)
            else:
                icon = self._get_icon_for_file_type(page_type, icon_type, icon_path)
            
            # 图标在背景中的位置
            icon_draw_x = icon_x + (icon_bg_width - icon_size) // 2
            icon_draw_y = icon_y + (icon_bg_height - icon_size) // 2
            
            # 如果有图标颜色设置，则应用颜色
            if icon_color:
                # 创建带颜色的图标
                pixmap = icon.pixmap(icon_size, icon_size)
                colored_pixmap = pixmap.copy()
                painter2 = QPainter(colored_pixmap)
                painter2.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
                painter2.fillRect(colored_pixmap.rect(), QColor(icon_color))
                painter2.end()
                painter.drawPixmap(icon_draw_x, icon_draw_y, colored_pixmap)
            else:
                painter.drawPixmap(icon_draw_x, icon_draw_y, icon.pixmap(icon_size, icon_size))
            
            # 内容区域 - 调整为TDesign风格
            content_x = icon_x + icon_bg_width + SPACING_MD
            content_y = option_rect.y() + SPACING_MD
            content_width = option_rect.width() - content_x - 90  # 保留操作按钮空间
            
            # 绘制标题 - TDesign文本样式
            title_font = QFont()
            title_font.setPointSize(FONT_SIZE_MD)
            title_font.setWeight(QFont.Weight.Medium)
            painter.setFont(title_font)
            
            if option.state & QStyle.StateFlag.State_Selected:
                painter.setPen(PRIMARY_700)  # TDesign selected text color
            else:
                painter.setPen(NEUTRAL_900)  # TDesign primary text
            
            # 计算标题可用宽度
            title_metrics = painter.fontMetrics()
            elided_title = title_metrics.elidedText(title, Qt.TextElideMode.ElideRight, content_width)
            
            # 绘制标题
            painter.drawText(content_x, content_y + title_metrics.ascent(), elided_title)
            
            # 绘制次要信息（修改时间）
            if formatted_time:
                time_font = QFont()
                time_font.setPointSize(FONT_SIZE_XS)
                painter.setFont(time_font)
                
                if option.state & QStyle.StateFlag.State_Selected:
                    painter.setPen(PRIMARY_600)  # TDesign selected secondary text
                else:
                    painter.setPen(NEUTRAL_500)  # TDesign secondary text
                
                time_y = content_y + title_metrics.height() + SPACING_XS + painter.fontMetrics().ascent()
                painter.drawText(content_x, time_y, formatted_time)
            
            # 注释掉标签绘制代码，不再显示标签
            # 标签只在编辑对话框中管理，不在列表项中显示
            
            # 绘制底部边框分隔线 - TDesign风格
            painter.setPen(NEUTRAL_200)  # TDesign border color
            painter.drawLine(option_rect.left() + SPACING_MD + indent, option_rect.bottom() - 1, 
                           option_rect.right() - SPACING_MD, option_rect.bottom() - 1)
            
            # 移除多余的操作按钮绘制
        
        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index):
        # 减小项高度，提升紧凑性
        return QSize(option.rect.width(), 56)  # 从80px减少到56px，使布局更紧凑  # type: ignore

    def editorEvent(self, event, model, option, index):
        # 移除双击和按钮点击事件处理，改为右键菜单触发
        return super().editorEvent(event, model, option, index)