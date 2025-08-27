# -*- coding: utf-8 -*-
"""
MarkRender 样式工具模块
提供样式生成器函数，简化样式复用和组件样式创建
"""

from .style_constants import *

# ============================================================================
# 🎨 样式生成器函数 (Style Generator Functions)
# ============================================================================

def create_menu_style():
    """创建菜单样式"""
    return f"""
    QMenu {{
        background-color: {NEUTRAL_0};
        border: 1px solid {NEUTRAL_200};
        border-radius: {RADIUS_MD}px;
        padding: {SPACING_SM}px;
    }}
    QMenu::item {{
        color: transparent;
        padding: 0px;
        margin: {SPACING_XS}px;
    }}
    QPushButton {{
        border: none;
        border-radius: {RADIUS_MD}px;
        background-color: transparent;
        padding: {SPACING_MD}px;
        min-width: {BUTTON_HEIGHT_LG}px;
        min-height: {BUTTON_HEIGHT_LG}px;
    }}
    QPushButton:hover {{
        background-color: {PRIMARY_50};
    }}
    QPushButton:pressed {{
        background-color: {PRIMARY_100};
    }}
    QWidget {{
        background-color: transparent;
        border: none;
    }}
    """

def create_button_style(button_type="primary", size="md"):
    """
    创建按钮样式
    
    Args:
        button_type: 按钮类型 ("primary", "secondary", "danger", "ghost")
        size: 按钮大小 ("sm", "md", "lg")
    """
    # 尺寸配置
    size_configs = {
        "sm": {
            "height": BUTTON_HEIGHT_SM,
            "padding": f"{SPACING_XS}px {SPACING_MD}px",
            "font_size": FONT_SIZE_SM,
        },
        "md": {
            "height": BUTTON_HEIGHT_MD,
            "padding": f"{SPACING_SM}px {SPACING_LG}px",
            "font_size": FONT_SIZE_MD,
        },
        "lg": {
            "height": BUTTON_HEIGHT_LG,
            "padding": f"{SPACING_MD}px {SPACING_XL}px",
            "font_size": FONT_SIZE_LG,
        }
    }
    
    # 类型配置
    type_configs = {
        "primary": {
            "bg": PRIMARY_500,
            "color": NEUTRAL_0,
            "border": PRIMARY_600,
            "hover_bg": PRIMARY_600,
            "hover_border": PRIMARY_700,
            "pressed_bg": PRIMARY_700,
        },
        "secondary": {
            "bg": NEUTRAL_0,
            "color": NEUTRAL_700,
            "border": NEUTRAL_300,
            "hover_bg": NEUTRAL_50,
            "hover_border": NEUTRAL_400,
            "pressed_bg": NEUTRAL_100,
        },
        "danger": {
            "bg": ERROR_500,
            "color": NEUTRAL_0,
            "border": ERROR_500,
            "hover_bg": "#dc2626",
            "hover_border": "#dc2626",
            "pressed_bg": "#b91c1c",
        },
        "ghost": {
            "bg": "transparent",
            "color": PRIMARY_500,
            "border": "transparent",
            "hover_bg": PRIMARY_50,
            "hover_border": PRIMARY_100,
            "pressed_bg": PRIMARY_100,
        }
    }
    
    size_config = size_configs.get(size, size_configs["md"])
    type_config = type_configs.get(button_type, type_configs["primary"])
    
    return f"""
    QPushButton {{
        background-color: {type_config["bg"]};
        color: {type_config["color"]};
        border: 1px solid {type_config["border"]};
        border-radius: {RADIUS_SM}px;
        padding: {size_config["padding"]};
        font-size: {size_config["font_size"]}px;
        font-weight: 600;
        min-height: {size_config["height"]}px;
    }}
    QPushButton:hover {{
        background-color: {type_config["hover_bg"]};
        border-color: {type_config["hover_border"]};
    }}
    QPushButton:pressed {{
        background-color: {type_config["pressed_bg"]};
    }}
    QPushButton:disabled {{
        background-color: {NEUTRAL_200};
        color: {NEUTRAL_400};
        border-color: {NEUTRAL_200};
        opacity: 0.6;
    }}
    """

def create_input_style():
    """创建输入框样式"""
    return f"""
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

def create_dialog_style():
    """创建对话框样式"""
    return f"""
    QDialog {{
        background-color: {NEUTRAL_0};
        border-radius: {RADIUS_LG}px;
        border: 1px solid {NEUTRAL_200};
    }}
    QTabWidget::pane {{
        border: 1px solid {NEUTRAL_200};
        border-radius: {RADIUS_MD}px;
        background-color: {NEUTRAL_0};
    }}
    QTabBar::tab {{
        background-color: transparent;
        color: {NEUTRAL_600};
        padding: {SPACING_SM}px {SPACING_LG}px;
        margin-right: {SPACING_XS}px;
        border-top-left-radius: {RADIUS_SM}px;
        border-top-right-radius: {RADIUS_SM}px;
        border: 1px solid transparent;
    }}
    QTabBar::tab:selected {{
        color: {PRIMARY_500};
        background-color: {NEUTRAL_0};
        border: 1px solid {NEUTRAL_200};
        border-bottom: 1px solid {NEUTRAL_0};
        font-weight: 600;
    }}
    QTabBar::tab:hover {{
        background-color: {PRIMARY_50};
        color: {PRIMARY_600};
    }}
    """

def create_tag_color_style(tag_type="default"):
    """
    创建标签颜色样式
    
    Args:
        tag_type: 标签类型，如 "md", "pdf", "png" 等
    """
    color = TAG_COLOR_MAP.get(tag_type.lower(), DEFAULT_TAG_COLOR)
    rgb = f"{color.red()}, {color.green()}, {color.blue()}"
    
    return f"""
    QLabel {{
        background-color: rgba({rgb}, 0.1);
        color: rgb({rgb});
        border: 1px solid rgba({rgb}, 0.3);
        border-radius: {RADIUS_PILL}px;
        padding: {SPACING_XS}px {SPACING_SM}px;
        font-size: {FONT_SIZE_XS}px;
        font-weight: 500;
    }}
    """

def create_hover_effect_style():
    """创建通用悬停效果样式"""
    return f"""
    QWidget:hover {{
        background-color: {PRIMARY_50};
        border-color: {PRIMARY_100};
    }}
    """

def create_card_style():
    """创建卡片样式"""
    return f"""
    QFrame {{
        background-color: {NEUTRAL_0};
        border: 1px solid {NEUTRAL_200};
        border-radius: {RADIUS_MD}px;
        padding: {SPACING_LG}px;
    }}
    QFrame:hover {{
        border-color: {PRIMARY_200};
    }}
    """

# ============================================================================
# 🎯 快捷样式函数 (Quick Style Functions)
# ============================================================================

def danger_button():
    """危险按钮快捷样式"""
    return create_button_style("danger", "md")

def primary_button():
    """主要按钮快捷样式"""
    return create_button_style("primary", "md")

def secondary_button():
    """次要按钮快捷样式"""
    return create_button_style("secondary", "md")

def small_button():
    """小按钮快捷样式"""
    return create_button_style("primary", "sm")

def large_button():
    """大按钮快捷样式"""
    return create_button_style("primary", "lg")

def ghost_button():
    """幽灵按钮快捷样式"""
    return create_button_style("ghost", "md")