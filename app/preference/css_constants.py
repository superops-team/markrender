# -*- coding: utf-8 -*-
"""
CSS样式常量定义文件
统一管理HTML/CSS相关的样式配置，用于Markdown渲染和主题系统
"""

from .style_constants import *

# ============================================================================
# 🎨 代码高亮样式 (Code Highlight Styles)
# ============================================================================

# 基础代码样式
BASE_CODE_STYLE = f"""
<style>
    /* 一级标题居中并设置颜色 */
    h1 {{
        text-align: center;
        color: {NEUTRAL_700};
    }}

    /* 代码高亮样式 - 注意: overflow仅用于HTML渲染 */
    pre {{
        background-color: {CODE_HIGHLIGHT_COLORS['background']};
        border-radius: {RADIUS_SM}px;
        font-size: 85%;
        line-height: {LINE_HEIGHT_NORMAL};
        padding: {SPACING_LG}px;
        font-family: {FONT_FAMILY_MONOSPACE};
    }}

    code {{
        background-color: {CODE_HIGHLIGHT_COLORS['inline_background']};
        border-radius: {RADIUS_SM}px;
        font-family: {FONT_FAMILY_MONOSPACE};
        font-size: 85%;
        margin: 0;
        padding: 0.2em 0.4em;
    }}

    /* 代码块高亮 - 注意: overflow-x仅用于HTML渲染 */
    .hljs {{
        display: block;
        padding: 0.5em;
        color: {CODE_HIGHLIGHT_COLORS['text']};
        background: {CODE_HIGHLIGHT_COLORS['background']};
    }}

    /* Python语言高亮样式 */
    .language-python .hljs-keyword {{ color: {CODE_HIGHLIGHT_COLORS['keyword']}; }}
    .language-python .hljs-string {{ color: {CODE_HIGHLIGHT_COLORS['string']}; }}
    .language-python .hljs-number {{ color: {CODE_HIGHLIGHT_COLORS['number']}; }}
    .language-python .hljs-comment {{ color: {CODE_HIGHLIGHT_COLORS['comment']}; }}

    /* JavaScript语言高亮样式 */
    .language-javascript .hljs-keyword {{ color: {CODE_HIGHLIGHT_COLORS['keyword']}; }}
    .language-javascript .hljs-string {{ color: {CODE_HIGHLIGHT_COLORS['string']}; }}
    .language-javascript .hljs-number {{ color: {CODE_HIGHLIGHT_COLORS['number']}; }}
    .language-javascript .hljs-comment {{ color: {CODE_HIGHLIGHT_COLORS['comment']}; }}

    /* HTML语言高亮样式 */
    .language-html .hljs-tag {{ color: {CODE_HIGHLIGHT_COLORS['tag']}; }}
    .language-html .hljs-attr {{ color: {CODE_HIGHLIGHT_COLORS['attribute']}; }}
    .language-html .hljs-string {{ color: {CODE_HIGHLIGHT_COLORS['string']}; }}

    /* CSS语言高亮样式 */
    .language-css .hljs-selector-tag {{ color: {CODE_HIGHLIGHT_COLORS['tag']}; }}
    .language-css .hljs-property {{ color: {CODE_HIGHLIGHT_COLORS['attribute']}; }}
    .language-css .hljs-value {{ color: {CODE_HIGHLIGHT_COLORS['string']}; }}
</style>
"""

# ============================================================================
# 🎭 主题样式模板 (Theme Style Templates)
# ============================================================================

def create_theme_style(theme_name="default"):
    """
    创建主题样式
    
    Args:
        theme_name: 主题名称 ("default", "github", "light", "dark", "document")
    """
    
    # 获取主题配置
    if theme_name == "light":
        config = THEME_COLORS['light']
    elif theme_name == "dark":
        config = THEME_COLORS['dark']
    else:
        # 默认主题配置
        config = {
            'body_bg': NEUTRAL_0,
            'body_text': NEUTRAL_700,
            'h2_color': NEUTRAL_900,
            'border': NEUTRAL_200,
            'blockquote_border': NEUTRAL_400,
            'blockquote_text': NEUTRAL_600,
        }
    
    # GitHub风格特殊处理
    if theme_name == "github":
        return f"""<style>
        body {{ 
            font-family: {FONT_FAMILY_SYSTEM};
            background-color: {config.get('body_bg', NEUTRAL_0)};
            color: {config.get('body_text', NEUTRAL_700)};
        }}
        h2 {{ 
            font-size: {FONT_SIZE_XL}px; 
            border-bottom: 1px solid {config.get('border', NEUTRAL_200)}; 
        }}
        blockquote {{ 
            border-left: 0.25em solid {config.get('blockquote_border', NEUTRAL_300)}; 
            padding: 0 1em; 
            color: {config.get('blockquote_text', NEUTRAL_600)}; 
        }}
        table {{ border-collapse: collapse; }}
        th, td {{ 
            border: 1px solid {config.get('border', NEUTRAL_200)}; 
            padding: {SPACING_XS}px {SPACING_SM}px; 
        }}
    </style>"""
    
    # 文档风格特殊处理
    if theme_name == "document":
        return f"""<style>
        body {{
            font-family: {FONT_FAMILY_SERIF};
            max-width: 800px;
            margin: 0 auto;
            padding: {SPACING_XL}px;
        }}
        h2 {{ 
            font-family: {FONT_FAMILY_SYSTEM}; 
            font-size: {FONT_SIZE_2XL}px; 
        }}
        blockquote {{ font-style: italic; }}
        table {{ border-collapse: collapse; }}
        th, td {{ 
            border: 1px solid {NEUTRAL_300}; 
            padding: {SPACING_XS}px {SPACING_SM}px; 
        }}
    </style>"""
    
    # 通用主题样式
    return f"""<style>
        body {{
            font-family: {FONT_FAMILY_SYSTEM};
            background-color: {config.get('body_bg', NEUTRAL_0)};
            color: {config.get('body_text', NEUTRAL_700)};
        }}
        h2 {{ 
            color: {config.get('h2_color', NEUTRAL_900)}; 
            border-bottom: 1px solid {config.get('border', NEUTRAL_200)}; 
        }}
        blockquote {{ 
            border-left: 3px solid {config.get('blockquote_border', NEUTRAL_400)}; 
            color: {config.get('blockquote_text', NEUTRAL_600)}; 
        }}
        a {{ color: {config.get('link', PRIMARY_500)}; }}
        table {{ border-collapse: collapse; }}
        th, td {{ 
            border: 1px solid {config.get('border', NEUTRAL_200)}; 
            padding: {SPACING_XS}px {SPACING_SM}px; 
        }}
    </style>"""

# ============================================================================
# 🎨 预定义主题样式 (Predefined Theme Styles)  
# ============================================================================

# 所有主题样式字典
THEME_STYLES = {
    "默认样式": BASE_CODE_STYLE + create_theme_style("default"),
    "GitHub风格": BASE_CODE_STYLE + create_theme_style("github"), 
    "浅色主题": BASE_CODE_STYLE + create_theme_style("light"),
    "深色主题": BASE_CODE_STYLE + create_theme_style("dark"),
    "文档风格": BASE_CODE_STYLE + create_theme_style("document"),
}

# ============================================================================
# 🔧 样式工具函数 (Style Utility Functions)
# ============================================================================

def get_theme_style(theme_name):
    """
    获取指定主题的完整样式
    
    Args:
        theme_name: 主题名称
        
    Returns:
        str: 完整的CSS样式字符串
    """
    return THEME_STYLES.get(theme_name, THEME_STYLES["默认样式"])

def get_all_theme_names():
    """
    获取所有可用的主题名称
    
    Returns:
        list: 主题名称列表
    """
    return list(THEME_STYLES.keys())

def add_custom_theme(name, style):
    """
    添加自定义主题
    
    Args:
        name: 主题名称
        style: CSS样式字符串
    """
    full_style = BASE_CODE_STYLE + style if not style.startswith('<style>') else style
    THEME_STYLES[name] = full_style

def create_inline_style(**kwargs):
    """
    创建内联样式
    
    Args:
        **kwargs: CSS属性键值对
        
    Returns:
        str: 内联样式字符串
    """
    styles = []
    for key, value in kwargs.items():
        # 将下划线转换为连字符
        css_key = key.replace('_', '-')
        styles.append(f"{css_key}: {value}")
    
    return "; ".join(styles)

# ============================================================================
# 🎯 快捷样式函数 (Quick Style Functions)
# ============================================================================

def primary_text_style():
    """主要文本样式"""
    return create_inline_style(
        color=NEUTRAL_700,
        font_size=f"{FONT_SIZE_MD}px",
        line_height=LINE_HEIGHT_NORMAL
    )

def secondary_text_style():
    """次要文本样式"""
    return create_inline_style(
        color=NEUTRAL_500,
        font_size=f"{FONT_SIZE_SM}px"
    )

def code_inline_style():
    """行内代码样式"""
    return create_inline_style(
        background_color=CODE_HIGHLIGHT_COLORS['inline_background'],
        padding="0.2em 0.4em",
        border_radius=f"{RADIUS_SM}px",
        font_family=FONT_FAMILY_MONOSPACE,
        font_size="85%"
    )

def highlight_background_style():
    """高亮背景样式"""
    return create_inline_style(
        background_color=PRIMARY_50,
        border_left=f"3px solid {PRIMARY_500}",
        padding=f"{SPACING_SM}px {SPACING_MD}px"
    )