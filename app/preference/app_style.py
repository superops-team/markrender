# -*- coding: utf-8 -*-
"""
MarkRender 应用样式管理器
统一管理整个应用的样式配置，通过导入设计令牌系统确保样式一致性
"""

from PySide6.QtGui import QColor
from db.settings_manager import SettingsManager
# 导入统一的样式常量
from .style_constants import *

# ========== 向后兼容性设置 ==========

# 以下是向后兼容的颜色别名，逐步迁移到 style_constants.py 中
COLOR_SELECTED = QColor(59, 130, 246, 38)  # PRIMARY_500 with alpha
COLOR_HOVER = QColor(59, 130, 246, 25)     # PRIMARY_500 with alpha
COLOR_DEFAULT_TEXT = QColor(17, 24, 39)    # NEUTRAL_900
COLOR_GRAY_TEXT = QColor(107, 114, 128)    # NEUTRAL_500
COLOR_WHITE = QColor(255, 255, 255)        # NEUTRAL_0
COLOR_LIGHT_GRAY = QColor(229, 231, 235)   # NEUTRAL_200
COLOR_BACKGROUND_LIGHT = NEUTRAL_50
COLOR_BACKGROUND_DARK = '#1f1f1f'
PRIMARY_BUTTON_BACKGROUND = PRIMARY_500
PRIMARY_BUTTON_HOVER = PRIMARY_600
HOVER_COLOR = PRIMARY_50
SIDEBAR_ICON_SELECTED = PRIMARY_500
LINE_COLOR = NEUTRAL_200

# 以下是旧版样式定义，将逐步迁移到 style_constants.py

# Tag 颜色映射表
TAG_COLOR_MAP = {
    'md': QColor(59, 130, 246),      # 蓝色 - Markdown (参考Notion/Apple)
    'pdf': QColor(239, 68, 68),      # 红色 - PDF (参考Adobe Acrobat)
    'png': QColor(139, 92, 246),     # 紫色 - PNG图片 (参考Figma)
    'jpeg': QColor(139, 92, 246),    # 紫色 - JPEG图片 (参考Figma)
    'csv': QColor(34, 197, 94),      # 绿色 - CSV数据 (参考Excel)
    'docx': QColor(59, 130, 246),    # 蓝色 - Word文档 (参考Microsoft)
    'doc': QColor(59, 130, 246),     # 蓝色 - Word文档 (参考Microsoft)
    'xls': QColor(34, 197, 94),      # 绿色 - Excel (参考Microsoft)
    'xlsx': QColor(34, 197, 94),     # 绿色 - Excel (参考Microsoft)
    'ppt': QColor(245, 158, 11),     # 橙色 - PowerPoint (参考Microsoft)
    'pptx': QColor(245, 158, 11),    # 橙色 - PowerPoint (参考Microsoft)
    'epub': QColor(168, 85, 247),    # 紫色 - 电子书 (参考Apple Books)
}
DEFAULT_COLOR = QColor(107, 114, 128)  # 默认灰色 - 默认文件类型颜色

# 通用样式
DIALOG_BORDER_RADIUS = "QDialog { border-radius: 6px; }"  # 更新圆角使设计更现代
WIDGET_BACKGROUND_LIGHT = "QWidget { background-color: #fafafa; }"
WIDGET_BACKGROUND_DARK = "QWidget { background-color: #1f1f1f; }"

# 导入对话框样式 - 使用设计令牌
IMPORT_AREA = f"""
QFrame {{
    border: 1px dashed {PRIMARY_500};
    background-color: {NEUTRAL_100};
    margin: {SPACING_MD}px;
    border-radius: {RADIUS_SM}px;
}}
QFrame:hover {{
    border-color: {PRIMARY_600};
    background-color: {NEUTRAL_200};
}}"""

# 标签样式 - 使用设计令牌
IMPORT_LABEL = f"background-color: {PRIMARY_50}; padding: {SPACING_MD}px; border-radius: {RADIUS_SM}px; color: {NEUTRAL_700};"
INFO_LABEL = f"color: {SUCCESS_500}; font-size: {FONT_SIZE_SM}px;"
FORMAT_LABEL = f"color: {NEUTRAL_500}; font-size: {FONT_SIZE_XS}px;"
LOADING_LABEL = f"font-size: {FONT_SIZE_LG}px; color: {PRIMARY_500};"

OVERLAY_STYLE = """
background-color: rgba(255, 255, 255, 1);
"""

# 进度条样式 - 使用设计令牌
PROGRESS_BAR = f"""
QProgressBar {{
    border-radius: {RADIUS_SM}px;
    text-align: center;
    height: {PROGRESS_BAR_HEIGHT}px;
    background-color: {NEUTRAL_200};
}}
QProgressBar::chunk {{
    background-color: {PRIMARY_500};
    border-radius: {RADIUS_SM}px;
}}"""

CONFIRM_BUTTON = f"""
QPushButton {{
    background-color: {PRIMARY_500};
    color: {NEUTRAL_0};
    border: 1px solid {PRIMARY_600};
    border-radius: {RADIUS_SM}px;
    padding: {SPACING_SM}px {SPACING_LG}px;
    font-size: {FONT_SIZE_MD}px;
    font-weight: 600;
    min-width: 80px;
    min-height: 32px;
}}
QPushButton:hover {{
    background-color: {PRIMARY_600};
    border-color: {PRIMARY_700};
}}
QPushButton:pressed {{
    background-color: {PRIMARY_700};
    border-color: {PRIMARY_900};
}}
QPushButton:disabled {{
    background-color: {NEUTRAL_200};
    color: {NEUTRAL_400};
    border-color: {NEUTRAL_200};
}}
"""

# 按钮样式
MAIN_CLOSE_BUTTON = """
QPushButton {
    background-color: #ff5f56;
    border-radius: 10px;
    border: 1px solid #e14239;
    qproperty-flat: true;
}
QPushButton:hover {
    background-color: #e2443a;
    border: 1px solid #c03a2f;
}
QPushButton:hover::after {
    font-size: 12px;
    font-weight: 500;
    position: absolute;
}
"""

# 状态栏样式 - 使用设计令牌
STATUS_STYLE = f'''
QStatusBar {{
    border: {EDITOR_BORDER_WIDTH}px solid {NEUTRAL_300};
    background-color: {NEUTRAL_50};
    color: {NEUTRAL_500};
    font-size: {FONT_SIZE_XS}px;
    padding: {SPACING_XS}px {SPACING_XL}px {SPACING_XS}px {SPACING_XL}px;
    height: {STATUSBAR_HEIGHT}px;
}}
QLabel {{
    margin-left: {SPACING_LG}px;
    color: {NEUTRAL_400};
}}
'''

LINE_EDIT = f"""
QLineEdit {{
    border: 1px solid {NEUTRAL_300};
    border-radius: {RADIUS_SM}px;
    padding: {SPACING_SM}px {SPACING_MD}px;
    font-size: {FONT_SIZE_MD}px;
    color: {NEUTRAL_700};
    background-color: {NEUTRAL_0};
    min-height: 20px;
    line-height: {LINE_HEIGHT_NORMAL};
}}
QLineEdit:hover {{
    border-color: {PRIMARY_300};
    background-color: {PRIMARY_50};
}}
QLineEdit:focus {{
    border-color: {PRIMARY_500};
    background-color: {NEUTRAL_0};
    outline: 2px solid {PRIMARY_100};
    outline-offset: -2px;
}}
QLineEdit:disabled {{
    background-color: {NEUTRAL_100};
    color: {NEUTRAL_400};
    border-color: {NEUTRAL_200};
}}
"""

# macOS 最小化按钮样式 - 使用设计令牌
MINIMIZE_BUTTON_LEGACY = f"""
QPushButton {{
    background-color: {MACOS_YELLOW};
    border-radius: {MACOS_BUTTON_RADIUS}px;
    border: 1px solid {MACOS_YELLOW_BORDER};
    qproperty-flat: true;
}}
QPushButton:hover {{
    background-color: {MACOS_YELLOW_HOVER};
    border: 1px solid {MACOS_YELLOW_BORDER};
}}
QPushButton:hover::after {{
    content: "-";
    color: rgba(0, 0, 0, 0.8);
    position: absolute;
}}"""

# macOS 最大化按钮样式 - 使用设计令牌
MAXIMIZE_BUTTON = f"""
QPushButton {{
    background-color: {MACOS_GREEN};
    border-radius: {MACOS_BUTTON_RADIUS}px;
    border: 1px solid {MACOS_GREEN_BORDER};
    qproperty-flat: true;
}}
QPushButton:hover {{
    background-color: {MACOS_GREEN_HOVER};
    border: 1px solid {MACOS_GREEN_BORDER};
}}
QPushButton:hover::after {{
    content: "+";
    color: rgba(0, 0, 0, 0.8);
    font-family: "{FONT_FAMILY_SYSTEM}";
    font-size: {FONT_SIZE_XS}px;
    font-weight: 500;
    position: absolute;
    top: 50%;
    left: 50%;
}}"""

# 顶部菜单样式 - 使用设计令牌
TOP_MENU_BACKGROUND = f"background: {NEUTRAL_100};"

# 编辑器样式 - 使用设计令牌
EDITOR_PARENT = f"""
QWidget {{  /* 父容器样式 */
    border: {EDITOR_BORDER_WIDTH}px solid {NEUTRAL_300};
    padding: {EDITOR_PADDING}px;
}}"""

EDITOR_PREVIEW = f"""
QWebEngineView {{  /* 预览视图样式 */
    border: none;
    background-color: transparent;
    margin: 0;
    padding: 0;
}}"""

# 主要按钮样式 - 使用设计令牌 (将会被新的CONFIRM_BUTTON替代)
PRIMARY_BUTTON_LEGACY = f"""
QPushButton {{
    background-color: {PRIMARY_500};
    color: {NEUTRAL_0};
    border-radius: {RADIUS_SM}px;
    padding: {SPACING_SM}px {SPACING_LG}px;
    font-size: {FONT_SIZE_MD}px;
}}
QPushButton:hover {{
    background-color: {PRIMARY_600};
}}"""

MAIN_WINDOW = """
QMainWindow {{
    background-color: {};
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}}
"""

MAIN_WINDOW_COLOR = """
QMainWindow {{
    background-color: {};
}}
"""

# 侧边栏按钮样式 - 使用设计令牌系统
SIDEBAR_BUTTON = f"""
QPushButton {{
    color: {NEUTRAL_600};
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: {RADIUS_SM}px;
    padding: {SPACING_XS}px;
    font-size: {FONT_SIZE_SM}px;
    font-weight: 500;
    min-width: 28px;
    min-height: 28px;
    max-width: 32px;
    max-height: 32px;
}}
QPushButton:hover {{
    background-color: {PRIMARY_50};
    border-color: {PRIMARY_100};
    color: {PRIMARY_600};
}}
QPushButton:pressed {{
    background-color: {PRIMARY_100};
    border-color: {PRIMARY_200};
    color: {PRIMARY_700};
}}
QPushButton:checked {{
    background-color: {NEUTRAL_0};
    border: 1px solid {PRIMARY_300};
    color: {PRIMARY_500};
    font-weight: 600;
    padding: 2px;
}}
QPushButton:checked:hover {{
    background-color: {PRIMARY_50};
    border: 1px solid {PRIMARY_300};
    color: {PRIMARY_600};
    padding: 2px;
}}
"""



# 标题栏样式 - 使用设计令牌
TITLE_BAR = f"""
QWidget {{
    background-color: {NEUTRAL_100};
    font-size: {FONT_SIZE_MD}px;
    font-weight: bold;
    border-bottom: 1px solid {NEUTRAL_300};
    height: {TITLEBAR_HEIGHT}px;
}}"""

# 侧边栏样式 - 使用设计令牌
SIDEBAR = f"""
QWidget {{
    background-color: {NEUTRAL_50};
    border-right: 1px solid {NEUTRAL_300};
    width: {SIDEBAR_WIDTH}px;
}}"""



MAXIMIZE_BUTTON = """
QPushButton {
    background-color: #34c84a;
    border-radius: 10px;
    min-width: 12px;
    min-height: 12px;
    max-width: 12px;
    max-height: 12px;
    border: 1px solid #2da03f;
    margin-right: 6px;
}
QPushButton:hover {
    background-color: #2da03f;
}
"""

CLOSE_BUTTON = """
QPushButton {
    background-color: #0d6efd;
    color: white;
    border-radius: 5px;
    padding: 8px 16px;
    font-size: 14px;
    margin-right: 5px;  # 添加右侧间距
}
QPushButton:hover {
    background-color: #0b5ed7;
    border-radius: 5px;
}
# 添加选中状态样式
QPushButton:checked {
    background-color: #2591FF;
}
"""

NEW_FILE_DIALOG = "QDialog { border-radius: 5px; }"

EDITOR = """
QWidget {  /* 父容器样式 */
    border: 2px solid #ddd;
    padding: 0;
}
QWebEngineView {  /* 预览视图样式 */
    border: none;
    background-color: transparent; /* 设置透明背景 */
    margin: 0; /* 移除抵消布局的 margin */
    padding: 0; /* 移除补充的 padding */
}
"""

MAIN_SPLITTER = """
QSplitter {{
    background-color: {};
}}
QSplitter::handle {{
    background: #c0c0c0;
    width: 2px;
}}
"""

RIGHT_SPLITTER = """
QSplitter::handle {{
    background: transparent;
    width: 2px;
}}
QSplitter {{
    padding: 2px;
    background-color: {};
}}
QSplitter > QWidget {{
    margin: 2 2px;
}}
"""

CENTRAL_WIDGET = """
QWidget {{
    background-color: {};
    border: 1px solid #F0F0F0;  /* 添加边框 */
}}
"""

QUICKPICK_PANEL = f"""
QTreeWidget {{
    border: 1px solid {NEUTRAL_200};
    border-radius: {RADIUS_MD}px;
    background-color: {NEUTRAL_0};
    padding: {SPACING_XS}px;
    margin-top: 0px;
}}
QTreeWidget::item {{
    border: none;
    border-radius: {RADIUS_SM}px;
    padding: {SPACING_XS}px;
    margin-bottom: {SPACING_XS//2}px;
    background-color: {NEUTRAL_0};
    min-height: 48px;
    margin-left: {SPACING_SM}px;
    margin-right: {SPACING_SM}px;
}}
QTreeWidget::item:last {{
    margin-bottom: 0px;
}}
QTreeWidget::item:hover {{
    background-color: {PRIMARY_50};
}}
QTreeWidget::item:selected {{
    background-color: {PRIMARY_100};
}}
QTreeWidget::branch:has-children:!has-siblings:closed,
QTreeWidget::branch:closed:has-children:has-siblings {{
    border-image: none;
    image: url(icons/chevron-right.svg);
}}
QTreeWidget::branch:open:has-children:!has-siblings,
QTreeWidget::branch:open:has-children:has-siblings {{
    border-image: none;
    image: url(icons/chevron-down.svg);
}}
/* 确保所有层级的item都能正确响应点击事件 */
QTreeWidget::item {{
    padding-top: {SPACING_XS//2}px;
    padding-bottom: {SPACING_XS//2}px;
}}
/* 优化树形结构的视觉层次，遵循TDesign设计原则 */
QTreeWidget::branch {{
    width: 16px;
    height: 16px;
    background-color: transparent;
}}
/* 确保选中状态的一致性，移除可能导致冲突的分支样式 */
QTreeWidget::branch:selected {{
    background-color: transparent;
}}
QTreeWidget::branch:hover {{
    background-color: transparent;
}}
/* 确保选中状态覆盖整个item区域 */
QTreeWidget::item:selected:active {{
    background-color: {PRIMARY_100};
}}
QTreeWidget::item:selected:!active {{
    background-color: {PRIMARY_100};
}}
/* 移除折叠区域缩进的特殊颜色渲染 */
QTreeWidget::branch:has-children {{
    background-color: transparent;
    border: none;
}}
"""
TAB_STYLE = """
/* 去掉 tab 页边框 */
QTabWidget::pane {
    border: none;
}
/* 标签栏文字 + 指示器 */
QTabBar::tab {
    border: none;
    padding: 6px 12px;
    margin: 0px 1px;
}
QTabBar::tab:selected {
    color: white;
    background-color: #0d6efd;
    border-radius: 4px;
}

/* 对话框统一圆角 */
EditItemDialog {
    border-radius: 4px;
}
QPushButton {
    background-color: #0d6efd;
    color: white;
    border-radius: 4px;
    padding: 8px 16px;
    font-size: 14px;
}
QPushButton:hover {
    background-color: #0b5ed7;
    border-radius: 4px;
}
QTabWidget::tab-bar {
    background: transparent;
    border: none;
}
"""

class AppStyle:
    '''
    应用程序样式
    '''
    def __init__(self) -> None:
        self.settings_manager = SettingsManager()
        self.dark_mode = self.settings_manager.get_setting('theme', 'dark_mode', False)

    def get_background_color(self):
        return COLOR_BACKGROUND_LIGHT if not self.dark_mode else COLOR_BACKGROUND_DARK

    def get_border_color(self):
        return QColor(59, 130, 246, 76)  # 修复 alpha 值为整数

    def get_hover_color(self):
        return HOVER_COLOR

    def get_editor_preview_background_color(self):
        return COLOR_BACKGROUND_LIGHT if not self.dark_mode else COLOR_BACKGROUND_DARK

    def get_tab_style(self):
        return TAB_STYLE

    def get_confirm_button_style(self):
        return CONFIRM_BUTTON if not self.dark_mode else CONFIRM_BUTTON.replace('#0078D4', '#005A9E')

    def get_close_button_style(self):
        return CLOSE_BUTTON if not self.dark_mode else CLOSE_BUTTON.replace('#0d6efd', '#005A9E')

    def get_sidebar_button_style(self):
        return SIDEBAR_BUTTON

    def get_dialog_border_radius(self):
        return DIALOG_BORDER_RADIUS

    def get_import_area(self):
        return IMPORT_AREA

    def get_import_label(self):
        return IMPORT_LABEL

    def get_progress_bar(self):
        return PROGRESS_BAR

    def get_top_menu_background(self):
        return TOP_MENU_BACKGROUND

    def get_editor_parent(self):
        return EDITOR_PARENT

    def get_editor_preview(self):
        return EDITOR_PREVIEW

    def get_quickpick_panel(self):
        return QUICKPICK_PANEL

    def get_format_label(self):
        return FORMAT_LABEL

    def get_info_label(self):
        return INFO_LABEL

    def get_loading_label(self):
        return LOADING_LABEL

    def get_primary_button(self):
        return PRIMARY_BUTTON_LEGACY

    def get_overlay_style(self):
        return OVERLAY_STYLE

    def get_supported_formats(self):
        return TAG_COLOR_MAP.keys()

    def get_sidebar_icon_selected(self):
        return SIDEBAR_ICON_SELECTED

    def get_main_style(self):
        return MAIN_WINDOW.format(self.get_background_color())

    def get_main_style_color(self):
        return MAIN_WINDOW_COLOR.format(self.get_background_color())

    def get_title_bar(self):
        return TITLE_BAR

    def get_line_edit(self):
        return LINE_EDIT

    def get_sidebar(self):
        bg_color = COLOR_BACKGROUND_LIGHT if not self.dark_mode else COLOR_BACKGROUND_DARK
        return f"""
QWidget {{
    background-color: {bg_color};
    border-right: 1px solid {LINE_COLOR};  /* 右侧内侧边框 */
}}
"""

    def get_status_bar(self):
        return STATUS_STYLE

    def get_minimize_button(self):
        return MINIMIZE_BUTTON_LEGACY

    def get_maximize_button(self):
        return MAXIMIZE_BUTTON

    def get_main_close_button(self):
        return MAIN_CLOSE_BUTTON

    def get_line_color(self):
        return LINE_COLOR

    def get_main_splitter(self):
        return MAIN_SPLITTER.format(self.get_line_color())

    def get_right_splitter(self):
        return RIGHT_SPLITTER.format(self.get_line_color())

    def get_central_widget(self):
        return CENTRAL_WIDGET.format(self.get_line_color())

    def get_tag_style(self, tag):
        """根据标签内容生成不同的样式 - 添加无边框设置"""
        colors = {
            'md': 'background-color: #9FC89C; color: white;',
            'pdf': 'background-color: #91C8E4; color: white;',
            'png': 'background-color: #ADB2D4; color: white;',
            'jpeg': 'background-color: #0F828C; color: white;',
            'csv': 'background-color: #A3DC9A; color: white;',
            'docx': 'background-color: #97B067; color: white;',
            'default': 'background-color: #0F828C; color: white;'
        }

        # 使用标签的前几个字符作为key
        tag_key = tag.lower()[:4]
        return f"""
            padding: 6px 16px;
            border-radius: 16px;
            font-size: 14px;
            border: none; /* 明确设置无边框 */
            {colors.get(tag_key, colors['default'])}
        """

    def get_menu_style(self):
        bg_color = '#ffffff' if not self.dark_mode else '#2d2d2d'
        hover_color = '#E6F6FF' if not self.dark_mode else '#3a3a3a'
        text_color = '#000000' if not self.dark_mode else '#ffffff'
        border_color = '#ddd' if not self.dark_mode else '#444'

        return f"""
        QMenu {{
            background-color: {bg_color};
            border: 1px solid {border_color};
            border-radius: 4px;
            padding: 4px;
        }}

        QMenu::item {{
            color: {text_color};
            padding: 6px 32px 6px 28px;  /* Adjusted left padding for larger icons */
            margin: 2px;
            border-radius: 2px;
        }}

        QMenu::item:selected {{
            background-color: {hover_color};
        }}

        QMenu::item:hover {{
            background-color: {hover_color};
        }}

        QMenu::separator {{
            height: 1px;
            background: {border_color};
            margin: 4px 8px;
        }}
        """