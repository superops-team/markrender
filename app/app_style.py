from PySide6.QtGui import QColor
from db.settings_manager import SettingsManager

# 颜色常量
COLOR_SELECTED = QColor(25, 144, 255, 38)
COLOR_HOVER = QColor(25, 144, 255, 25)
COLOR_DEFAULT_TEXT = QColor(0, 0, 0)
COLOR_GRAY_TEXT = QColor(100, 100, 100)
COLOR_WHITE = QColor(255, 255, 255)
COLOR_LIGHT_GRAY = QColor(220, 220, 220)
COLOR_BACKGROUND_LIGHT = '#fafafa'
COLOR_BACKGROUND_DARK = '#1f1f1f'
PRIMARY_BUTTON_BACKGROUND = '#0d6efd'
PRIMARY_BUTTON_HOVER = '#0b5ed7'
# 添加选中状态图标颜色
SIDEBAR_ICON_SELECTED = '#2591FF'
LINE_COLOR = '#F2F2F2'

# Tag 颜色映射表
TAG_COLOR_MAP = {
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
DEFAULT_COLOR = QColor(128, 128, 128)

# 通用样式
DIALOG_BORDER_RADIUS = "QDialog { border-radius: 5px; }"
WIDGET_BACKGROUND_LIGHT = "QWidget { background-color: #fafafa; }"
WIDGET_BACKGROUND_DARK = "QWidget { background-color: #1f1f1f; }"

# 导入对话框样式
IMPORT_AREA = """
QFrame {
    border: 1px dashed #1990ff;
    border-radius: 5px;
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

CONFIRM_BUTTON = """
QPushButton {
    background-color: #0078D4;
    color: #FFFFFF;
    border: none;
    padding: 8px 16px;
    text-align: center;
    text-decoration: none;
    font-size: 14px;
    border-radius: 2px;
    min-width: 80px;
    font-weight: 600;
}
QPushButton:hover {
    background-color: #106EBE;
}
        
QPushButton:pressed {
    background-color: #005A9E;
}

QPushButton:disabled {
    background-color: #F3F2F1;
    color: #A19F9D;
}
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
    border-radius: 2px; /* 边框圆角 */
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

# 添加侧边栏按钮样式
SIDEBAR_BUTTON = """
QPushButton {
    color: white;
    background-color: transparent;
    border-radius: 5px;
    padding: 8px;
    font-size: 14px;
    border: none;
}
QPushButton:hover {
    background-color: #E6F6FF;
}
QPushButton:pressed {
    background-color: #F7F7F7;
}
// 添加选中状态样式
QPushButton:checked {
    background-color: #2591FF;
}
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
QWidget {{
    background-color: #f0f0f0;
    font-size: 14px;
    font-weight: bold;
    border-bottom: 1px solid {};  /* 底部内侧边框 */
}}
"""

SIDEBAR = """
QWidget {{
    background-color: #fafafa;
    border-right: 1px solid {};  /* 右侧内侧边框 */
}}
"""

STATUS_BAR = f"""
QStatusBar {{
    background-color: #fafafa;
    border-top: 1px solid {LINE_COLOR};  /* 顶部内侧边框 */
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
    border-radius: 10px;
    background-color: {};
    border: 1px solid #F0F0F0;  /* 添加边框 */
}}
"""

HISTORY_PANEL = """
QListWidget {
    border: 2px solid #ddd;
    border-radius: 8px;
    padding: 0;
    margin-top: 0px; /* 移除原有的margin-top设置 */
}
QListWidget::item {
    border: 2px solid transparent;
    padding: 5px 10px;
    background-color: #f0f0f0;
    border-bottom: 1px solid #ddd !important;
}
QListWidget::item:last {
    border-bottom: none !important;
}
QListWidget::item:hover {
    border: 2px solid rgb(25, 144, 255, 0.1);
    background-color: rgb(234, 243, 255, 0.1);
}
QListWidget::item:selected {
    border: 2px solid rgb(25, 144, 255, 0.1);
    background-color: rgb(234, 243, 255, 0.1);
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
        return WIDGET_BACKGROUND_LIGHT if not self.dark_mode else self.WIDGET_BACKGROUND_DARK
    
    def get_editor_preview_background_color(self):
        return WIDGET_BACKGROUND_LIGHT if not self.dark_mode else self.WIDGET_BACKGROUND_DARK
    
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
    
    def get_history_panel(self):
        return HISTORY_PANEL

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
        return TITLE_BAR.format('#c0c0c0')
    
    def get_sidebar(self):
        bg_color = COLOR_BACKGROUND_LIGHT if not self.dark_mode else COLOR_BACKGROUND_DARK
        return f"""
QWidget {{
    background-color: {bg_color};
    border-right: 1px solid {LINE_COLOR};  /* 右侧内侧边框 */
}}
"""

    def get_status_bar(self):
        bg_color = COLOR_BACKGROUND_LIGHT if not self.dark_mode else COLOR_BACKGROUND_DARK
        return f"""
QStatusBar {{
    background-color: {bg_color};
    border-top: 1px solid {LINE_COLOR};  /* 顶部内侧边框 */
}}
"""
    
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