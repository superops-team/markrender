from PySide6.QtGui import QColor
from db.settings_manager import SettingsManager

# ========== 设计令牌系统 (Design Tokens) ==========
# 按照Robin Williams四大设计原则建立统一的设计系统

# 主色调系统 - 蓝色系 (统一品牌色彩)
PRIMARY_50 = '#E8F4FD'    # 最浅蓝色 - 用于背景高亮
PRIMARY_100 = '#C3E2FB'   # 浅蓝色 - 用于悬停状态
PRIMARY_200 = '#A1D2F8'   # 中浅蓝色
PRIMARY_300 = '#7EC0F5'   # 中蓝色 - 用于边框
PRIMARY_500 = '#2591FF'   # 主蓝色 - 主要交互色
PRIMARY_600 = '#1E7CE8'   # 深蓝色 - 按压状态
PRIMARY_700 = '#1A6BD1'   # 更深蓝色
PRIMARY_900 = '#0F3A5F'   # 最深蓝色 - 用于文本

# 中性色系统 (灰度色阶)
NEUTRAL_0 = '#FFFFFF'     # 纯白色
NEUTRAL_50 = '#FAFBFC'    # 背景白
NEUTRAL_100 = '#F5F6F7'   # 浅灰背景
NEUTRAL_200 = '#EBEEF2'   # 边框色
NEUTRAL_300 = '#DDE1E6'   # 分割线
NEUTRAL_400 = '#C1C7CD'   # 禁用文本
NEUTRAL_500 = '#8D9499'   # 次要文本
NEUTRAL_600 = '#697077'   # 辅助文本
NEUTRAL_700 = '#4D5358'   # 主要文本
NEUTRAL_900 = '#1C1E21'   # 标题文本

# 语义化颜色 (状态色彩)
SUCCESS_50 = '#F0F9F4'
SUCCESS_500 = '#22C55E'
WARNING_50 = '#FFFBEB'
WARNING_500 = '#F59E0B'
ERROR_50 = '#FEF2F2'
ERROR_500 = '#EF4444'

# 兼容性别名 (保持向后兼容)
COLOR_SELECTED = QColor(37, 145, 255, 38)  # PRIMARY_500 with alpha
COLOR_HOVER = QColor(37, 145, 255, 25)     # PRIMARY_500 with alpha
COLOR_DEFAULT_TEXT = QColor(28, 30, 33)    # NEUTRAL_900
COLOR_GRAY_TEXT = QColor(141, 148, 153)    # NEUTRAL_500
COLOR_WHITE = QColor(255, 255, 255)        # NEUTRAL_0
COLOR_LIGHT_GRAY = QColor(235, 238, 242)   # NEUTRAL_200
COLOR_BACKGROUND_LIGHT = NEUTRAL_50
COLOR_BACKGROUND_DARK = '#1f1f1f'
PRIMARY_BUTTON_BACKGROUND = PRIMARY_500
PRIMARY_BUTTON_HOVER = PRIMARY_600
HOVER_COLOR = PRIMARY_50
SIDEBAR_ICON_SELECTED = PRIMARY_500
LINE_COLOR = NEUTRAL_200

# 间距系统 (基于8px网格)
SPACING_XS = 4   # 0.25rem
SPACING_SM = 8   # 0.5rem
SPACING_MD = 12  # 0.75rem
SPACING_LG = 16  # 1rem
SPACING_XL = 24  # 1.5rem
SPACING_2XL = 32 # 2rem
SPACING_3XL = 48 # 3rem

# 圆角系统
RADIUS_SM = 4   # 小圆角
RADIUS_MD = 8   # 中等圆角
RADIUS_LG = 12  # 大圆角
RADIUS_XL = 16  # 特大圆角
RADIUS_PILL = 9999 # 胶囊形

# 字体系统
FONT_SIZE_XS = 11
FONT_SIZE_SM = 12
FONT_SIZE_MD = 14
FONT_SIZE_LG = 16
FONT_SIZE_XL = 18
FONT_SIZE_2XL = 24

# 行高系统
LINE_HEIGHT_TIGHT = 1.2
LINE_HEIGHT_NORMAL = 1.4
LINE_HEIGHT_RELAXED = 1.6

# 阴影系统
SHADOW_SM = '0 1px 2px rgba(0, 0, 0, 0.05)'
SHADOW_MD = '0 4px 6px rgba(0, 0, 0, 0.07)'
SHADOW_LG = '0 10px 15px rgba(0, 0, 0, 0.1)'
SHADOW_XL = '0 20px 25px rgba(0, 0, 0, 0.15)'

# Tag 颜色映射表
TAG_COLOR_MAP = {
    'md': QColor(0, 171, 179),
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
DEFAULT_COLOR = QColor(128, 128, 128)

# 通用样式
DIALOG_BORDER_RADIUS = "QDialog { border-radius: 4px; }"
WIDGET_BACKGROUND_LIGHT = "QWidget { background-color: #fafafa; }"
WIDGET_BACKGROUND_DARK = "QWidget { background-color: #1f1f1f; }"

# 导入对话框样式
IMPORT_AREA = """
QFrame {
    border: 1px dashed #1990ff;
    background-color: #f5f5f5;
    margin: 10px;
}
QFrame:hover {
    border-color: #0d6efd;
    background-color: #e6e6e6;
}"""

IMPORT_LABEL = "background-color: #F0F3FF; padding: 10px; border-radius: 4px; color: #343a40;"
INFO_LABEL = "color: #28a745; font-size: 13px;"
FORMAT_LABEL = "color: #6c757d; font-size: 12px;"
LOADING_LABEL = "font-size: 16px; color: #0d6efd;"

OVERLAY_STYLE = """
background-color: rgba(255, 255, 255, 1);
"""

# 进度条样式
PROGRESS_BAR = """
QProgressBar {
    border-radius: 4px;
    text-align: center;
    height: 8px;
}
QProgressBar::chunk {
    background-color: #0d6efd;
    border-radius: 4px;
}"""

CONFIRM_BUTTON = f"""
QPushButton {{
    background-color: {PRIMARY_500};
    color: {NEUTRAL_0};
    border: 1px solid {PRIMARY_600};
    border-radius: {RADIUS_SM}px;
    padding: {SPACING_MD}px {SPACING_XL}px;
    font-size: {FONT_SIZE_MD}px;
    font-weight: 600;
    min-width: 80px;
    min-height: 36px;
}}
QPushButton:hover {{
    background-color: {PRIMARY_600};
    border-color: {PRIMARY_700};
    transform: translateY(-1px);
    box-shadow: {SHADOW_SM};
}}
QPushButton:pressed {{
    background-color: {PRIMARY_700};
    border-color: {PRIMARY_900};
    transform: translateY(0px);
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

STATUS_STYLE = '''
QStatusBar {
    border: 2px solid #ddd; /* 边框样式 */
    background-color: #fafafa; /* 使用统一背景色 */
    color: #eaf3ff; /* 字体颜色 */
    font-size: 12px; /* 字体大小 */
    padding: 2px 20px 2px 32px; /* 上、右、下、左内边距，左侧设置为 32px */
}
QLabel {
    margin-left: 15px; /* 标签间距 */
    color: #C3C9D3; /* 新增标签字体颜色 */
}
'''

LINE_EDIT = f"""
QLineEdit {{
    border: 1px solid {NEUTRAL_300};
    border-radius: {RADIUS_SM}px;
    padding: {SPACING_MD}px {SPACING_LG}px;
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

MINIMIZE_BUTTON = """
QPushButton {
    background-color: #ffbd2e;
    border-radius: 10px;
    border: 1px solid #e09e24;
    qproperty-flat: true;
}
QPushButton:hover {
    background-color: #e09e24;
    border: 1px solid #c28a20;
}
QPushButton:hover::after {
    content: "-";
    color: rgba(0, 0, 0, 0.8);
    position: absolute;
}
"""

MAXIMIZE_BUTTON = """
QPushButton {
    background-color: #27c93f;
    border-radius: 10px;
    border: 1px solid #22a535;
    qproperty-flat: true;
}
QPushButton:hover {
    background-color: #22a535;
    border: 1px solid #1e8f2f;
}
QPushButton:hover::after {
    content: "+";
    color: rgba(0, 0, 0, 0.8);
    font-family: "SF Pro Text", "Helvetica Neue", sans-serif;
    font-size: 12px;
    font-weight: 500;
    position: absolute;
    top: 50%;
    left: 50%;
}
"""

# 顶部菜单样式
TOP_MENU_BACKGROUND = "background: #f0f0f0;"

# 编辑器样式
EDITOR_PARENT = """
QWidget {  /* 父容器样式 */
    border: 2px solid #ddd;
    padding: 0;
}"""

EDITOR_PREVIEW = """
QWebEngineView {  /* 预览视图样式 */
    border: none;
    background-color: transparent;
    margin: 0;
    padding: 0;
}"""

PRIMARY_BUTTON = """
QPushButton {
    background-color: #0d6efd;
    color: white;
    border-radius: 5px;
    padding: 8px 16px;
    font-size: 14px;
}
QPushButton:hover {
    background-color: #0b5ed7;
    border-radius: 5px;
}
"""

MAIN_WINDOW = """
QMainWindow {{
    background-color: {};
    overflow: hidden;
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
    min-width: 32px;
    min-height: 32px;
    max-width: 36px;
    max-height: 36px;
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
    border-color: {PRIMARY_500};
    color: {PRIMARY_500};
    font-weight: 600;
}}
QPushButton:checked:hover {{
    background-color: {PRIMARY_50};
    border-color: {PRIMARY_600};
    color: {PRIMARY_600};
}}
"""

PROGRESS_BAR = """
QProgressBar {
    border-radius: 4px;
    text-align: center;
    height: 8px;
}
QProgressBar::chunk {
    background-color: #0d6efd;
    border-radius: 4px;
}
"""

# 新增样式定义
TITLE_BAR = """
QWidget {
    background-color: #f0f0f0;
    font-size: 14px;
    font-weight: bold;
    border-bottom: 1px solid #c0c0c0;  /* 底部内侧边框 */
}
"""

SIDEBAR = """
QWidget {{
    background-color: #fafafa;
    border-right: 1px solid {};  /* 右侧内侧边框 */
}}
"""

MINIMIZE_BUTTON = """
QPushButton {
    background-color: #fdbc40;
    border-radius: 10px;
    min-width: 12px;
    min-height: 12px;
    max-width: 12px;
    max-height: 12px;
    border: 1px solid #e2a137;
    margin-right: 6px;
}
QPushButton:hover {
    background-color: #e2a137;
}
"""

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
QListWidget {{
    border: 1px solid {NEUTRAL_200};
    border-radius: {RADIUS_MD}px;
    background-color: {NEUTRAL_0};
    padding: {SPACING_XS}px;
    margin-top: 0px;
    selection-background-color: transparent;
}}
QListWidget::item {{
    border: none;
    border-radius: {RADIUS_SM}px;
    padding: {SPACING_MD}px;
    margin-bottom: {SPACING_XS}px;
    background-color: {NEUTRAL_0};
    border-bottom: 1px solid {NEUTRAL_200};
    min-height: 48px;
}}
QListWidget::item:last {{
    border-bottom: none;
    margin-bottom: 0px;
}}
QListWidget::item:hover {{
    background-color: {PRIMARY_50};
    border-color: {PRIMARY_100};
    transform: translateY(-1px);
    box-shadow: {SHADOW_SM};
}}
QListWidget::item:selected {{
    background-color: {PRIMARY_100};
    border-color: {PRIMARY_200};
    color: {PRIMARY_700};
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
        return QColor(34, 184, 207, 76)  # 修复 alpha 值为整数

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
        return PRIMARY_BUTTON

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
        return MINIMIZE_BUTTON

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