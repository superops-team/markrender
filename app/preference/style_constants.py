# -*- coding: utf-8 -*-
"""
MarkRender 样式常量定义文件
统一管理所有硬编码的样式配置，包括颜色、字体、间距、圆角等
遵循设计令牌系统，确保设计的一致性和可扩展性
"""

from PySide6.QtGui import QColor

# ============================================================================
# 🎨 颜色系统 (Color System)
# ============================================================================

# 主色系 (Primary Colors) - 主要交互色彩
PRIMARY_50 = '#EFF6FF'     # 最浅蓝色 - 用于背景高亮 (更现代的浅蓝)
PRIMARY_100 = '#DBEAFE'    # 浅蓝色 - 用于悬停状态
PRIMARY_200 = '#BFDBFE'    # 中浅蓝色 - 用于按钮悬停
PRIMARY_300 = '#93C5FD'    # 中蓝色 - 用于边框和次要交互
PRIMARY_400 = '#60A5FA'    # 次蓝色 - 用于悬停状态
PRIMARY_500 = '#3B82F6'    # 主蓝色 - 主要交互色和品牌色 (参考Tailwind/现代设计)
PRIMARY_600 = '#2563EB'    # 深蓝色 - 按钮按压状态
PRIMARY_700 = '#1D4ED8'    # 更深蓝色 - 强调状态
PRIMARY_900 = '#1E3A8A'    # 最深蓝色 - 用于深色文本

# 中性色系 (Neutral Colors) - 文本、背景、边框
NEUTRAL_0 = '#FFFFFF'      # 纯白色 - 主要背景
NEUTRAL_50 = '#F9FAFB'     # 背景白 - 卡片背景
NEUTRAL_100 = '#F3F4F6'    # 浅灰背景 - 禁用状态背景
NEUTRAL_200 = '#E5E7EB'    # 边框色 - 主要边框颜色
NEUTRAL_300 = '#D1D5DB'    # 分割线 - 分隔符颜色
NEUTRAL_400 = '#9CA3AF'    # 禁用文本 - 禁用状态文字
NEUTRAL_500 = '#6B7280'    # 次要文本 - 辅助说明文字
NEUTRAL_600 = '#4B5563'    # 辅助文本 - 次级文本
NEUTRAL_700 = '#374151'    # 主要文本 - 正文文本
NEUTRAL_800 = '#1F2937'    # 深色文本 - 深色模式下的文本
NEUTRAL_900 = '#111827'    # 标题文本 - 标题和重要文本

# 语义化颜色 (Semantic Colors) - 状态指示
SUCCESS_50 = '#F0FDF4'     # 成功背景色
SUCCESS_500 = '#22C55E'    # 成功主色
SUCCESS_600 = '#16A34A'    # 成功深色 - 用于边框和悬停状态
WARNING_50 = '#FFFBEB'     # 警告背景色
WARNING_500 = '#F59E0B'    # 警告主色
WARNING_600 = '#D97706'    # 警告深色 - 用于边框和悬停状态
INFO_50 = '#EFF6FF'        # 信息背景色
INFO_500 = '#3B82F6'       # 信息主色 - 蓝色系，用于用户标签
INFO_600 = '#2563EB'       # 信息深色 - 用于边框和悬停状态
ERROR_50 = '#FEF2F2'       # 错误背景色
ERROR_500 = '#EF4444'      # 错误主色
ERROR_600 = '#DC2626'      # 错误深色 - 用于边框和悬停状态
DANGER_50 = '#FEF2F2'      # 危险背景色
DANGER_100 = '#FEE2E2'     # 危险浅色 - 用于悬停状态
DANGER_500 = '#EF4444'     # 危险色 - 用于错误和警告操作 (与ERROR_500保持一致)
DANGER_600 = '#DC2626'     # 危险深色 - 用于边框和悬停状态
PURPLE_500 = '#8B5CF6'     # 紫色 - 用于特殊标签和高亮
PINK_500 = '#EC4899'       # 粉色 - 用于特殊内容和标签
CYAN_500 = '#06B6D4'       # 青色 - 用于信息和提示

# 特殊颜色 (Special Colors)
BACKGROUND_LIGHT = NEUTRAL_50   # 浅色主题背景
BACKGROUND_DARK = '#1f1f1f'     # 深色主题背景

# macOS 系统色 (macOS System Colors)
MACOS_RED = '#ff5f56'           # macOS 红色 - 关闭按钮
MACOS_RED_HOVER = '#e2443a'     # macOS 红色悬停
MACOS_RED_BORDER = '#e14239'    # macOS 红色边框
MACOS_YELLOW = '#ffbd2e'        # macOS 黄色 - 最小化按钮
MACOS_YELLOW_HOVER = '#e09e24'  # macOS 黄色悬停
MACOS_YELLOW_BORDER = '#e09e24' # macOS 黄色边框
MACOS_GREEN = '#27c93f'         # macOS 绿色 - 最大化按钮
MACOS_GREEN_HOVER = '#22a535'   # macOS 绿色悬停
MACOS_GREEN_BORDER = '#22a535'  # macOS 绿色边框

# 临时兼容颜色 (Legacy Colors) - 待迁移
LEGACY_BLUE = '#0d6efd'         # 旧版蓝色
LEGACY_BLUE_HOVER = '#0b5ed7'   # 旧版蓝色悬停
LEGACY_GRAY_BORDER = '#ddd'     # 旧版灰色边框
LEGACY_STATUS_BG = '#fafafa'    # 旧版状态栏背景
LEGACY_STATUS_TEXT = '#eaf3ff'  # 旧版状态栏文字
LEGACY_STATUS_LABEL = '#C3C9D3' # 旧版状态栏标签

# 硬编码颜色待迁移
TODO_MIGRATE_COLORS = {
    'dialog_bg': '#f0f0f0',         # 对话框背景
    'dialog_border': '#c0c0c0',     # 对话框边框
    'sidebar_bg': '#fafafa',        # 侧边栏背景
    'import_bg': '#f5f5f5',         # 导入区域背景
    'import_hover': '#e6e6e6',      # 导入区域悬停
    'import_border': '#1990ff',     # 导入区域边框
    'import_label_bg': '#F0F3FF',   # 导入标签背景
    'import_label_text': '#343a40', # 导入标签文字
    'info_text': '#28a745',         # 信息文字
    'format_text': '#6c757d',       # 格式文字
    'splitter_handle': '#c0c0c0',   # 分割器手柄
    'central_border': '#F0F0F0',    # 中央边框
    'tag_md': '#3B82F6',           # MD标签 (更新为现代蓝色)
    'tag_pdf': '#EF4444',          # PDF标签 (更新为现代红色)
    'tag_png': '#8B5CF6',          # PNG标签 (更新为现代紫色)
    'tag_jpeg': '#8B5CF6',         # JPEG标签 (更新为现代紫色)
    'tag_csv': '#22C55E',          # CSV标签 (更新为现代绿色)
    'tag_doc': '#3B82F6',          # DOC标签 (更新为现代蓝色)
    'tag_xls': '#22C55E',          # XLS标签 (更新为现代绿色)
    'tag_ppt': '#F59E0B',          # PPT标签 (更新为现代橙色)
    'tag_epub': '#A855F7',         # EPUB标签 (更新为现代紫色)
    'default_tag': '#6B7280',       # 默认标签 (更新为现代灰色)
}

# ============================================================================
# 📏 间距系统 (Spacing System) - 基于8px网格
# ============================================================================

SPACING_XS = 4      # 0.25rem - 最小间距
SPACING_SM = 8      # 0.5rem - 小间距
SPACING_MD = 12     # 0.75rem - 中等间距
SPACING_LG = 16     # 1rem - 大间距
SPACING_XL = 24     # 1.5rem - 特大间距
SPACING_2XL = 32    # 2rem - 超大间距
SPACING_3XL = 48    # 3rem - 巨大间距

# ============================================================================
# 🔘 圆角系统 (Border Radius System)
# ============================================================================

RADIUS_XS = 2       # 超小圆角 - 微小元素
RADIUS_SM = 4       # 小圆角 - 按钮、输入框
RADIUS_MD = 6       # 中等圆角 - 卡片、面板 (减小圆角使设计更现代)
RADIUS_LG = 8       # 大圆角 - 对话框 (减小圆角使设计更现代)
RADIUS_XL = 12      # 特大圆角 - 特殊容器
RADIUS_PILL = 9999  # 胶囊形 - 标签、徽章
RADIUS_FULL = 9999  # 全圆角 - 等同于胶囊形

# ============================================================================
# 📝 字体系统 (Typography System)
# ============================================================================

# 字体大小 (Font Sizes)
FONT_SIZE_XS = 11   # 超小字体 - 标签、注释
FONT_SIZE_SM = 12   # 小字体 - 辅助文字
FONT_SIZE_MD = 13   # 中等字体 - 正文 (减小字体大小使布局更紧凑)
FONT_SIZE_LG = 14   # 大字体 - 标题 (减小字体大小使布局更紧凑)
FONT_SIZE_XL = 16   # 特大字体 - 大标题
FONT_SIZE_2XL = 20  # 超大字体 - 主标题 (减小字体大小使布局更紧凑)

# 行高 (Line Heights)
LINE_HEIGHT_TIGHT = 1.2    # 紧密行高 - 标题
LINE_HEIGHT_NORMAL = 1.4   # 正常行高 - 正文
LINE_HEIGHT_RELAXED = 1.6  # 宽松行高 - 长文本

# 字体族 (Font Families)
FONT_FAMILY_SYSTEM = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
FONT_FAMILY_MONOSPACE = "SFMono-Regular, Consolas, Liberation Mono, Menlo, monospace"
FONT_FAMILY_SERIF = "'Times New Roman', Times, serif"

# ============================================================================
# 🎭 阴影系统 (Shadow System) - 注意: Qt不支持CSS3 box-shadow
# 以下常量主要用于HTML/CSS渲染，在Qt样式表中不可用
# ============================================================================

SHADOW_SM = '0 1px 2px rgba(0, 0, 0, 0.05)'      # 小阴影 - 仅用于CSS
SHADOW_MD = '0 4px 6px rgba(0, 0, 0, 0.07)'      # 中等阴影 - 仅用于CSS
SHADOW_LG = '0 10px 15px rgba(0, 0, 0, 0.1)'     # 大阴影 - 仅用于CSS
SHADOW_XL = '0 20px 25px rgba(0, 0, 0, 0.15)'    # 特大阴影 - 仅用于CSS

# ============================================================================
# 🏷️ 文件类型标签颜色映射 (File Type Tag Colors) - 更新为现代软件设计颜色
# ============================================================================

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
DEFAULT_TAG_COLOR = QColor(107, 114, 128)  # 默认灰色 - 默认文件类型颜色

# ============================================================================
# 📐 布局系统 (Layout System)
# ============================================================================

# 组件尺寸 (Component Sizes)
BUTTON_HEIGHT_SM = 24       # 小按钮高度 (减小高度使布局更紧凑)
BUTTON_HEIGHT_MD = 32       # 中等按钮高度 (减小高度使布局更紧凑)
BUTTON_HEIGHT_LG = 40       # 大按钮高度 (减小高度使布局更紧凑)

INPUT_HEIGHT_SM = 24        # 小输入框高度 (减小高度使布局更紧凑)
INPUT_HEIGHT_MD = 32        # 中等输入框高度 (减小高度使布局更紧凑)
INPUT_HEIGHT_LG = 40        # 大输入框高度 (减小高度使布局更紧凑)

SIDEBAR_WIDTH = 56          # 侧边栏宽度 (数据驱动优化后，减小宽度使布局更紧凑)
TITLEBAR_HEIGHT = 32        # 标题栏高度 (增加高度使布局更平衡)
STATUSBAR_HEIGHT = 20       # 状态栏高度 (减小高度使布局更紧凑)

# ============================================================================
# 🎯 特殊配置 (Special Configurations)
# ============================================================================

# Sidebar 按钮精确配置 (数据驱动优化)
SIDEBAR_BUTTON_SIZE = 32            # 按钮尺寸 (减小尺寸使布局更紧凑)
SIDEBAR_BUTTON_ICON_SIZE = 16       # 图标尺寸 (减小尺寸使布局更紧凑)
SIDEBAR_MARGIN_LEFT = 6             # 左边距 (非对称补偿)
SIDEBAR_MARGIN_RIGHT = 7            # 右边距 (数据驱动优化)
SIDEBAR_PADDING_NORMAL = 3          # 正常状态内边距
SIDEBAR_PADDING_CHECKED = 2         # 选中状态内边距

# macOS 按钮配置
MACOS_BUTTON_SIZE = 12              # macOS 按钮尺寸
MACOS_BUTTON_RADIUS = 6             # macOS 按钮圆角

# 编辑器配置
EDITOR_BORDER_WIDTH = 1             # 编辑器边框宽度 (减小边框宽度使布局更紧凑)
EDITOR_PADDING = 0                  # 编辑器内边距
EDITOR_RADIUS = RADIUS_MD           # 编辑器圆角半径 (保持与整体设计一致)

# 进度条配置
PROGRESS_BAR_HEIGHT = 6             # 进度条高度 (减小高度使布局更紧凑)
PROGRESS_BAR_RADIUS = 3             # 进度条圆角

# ============================================================================
# 🔧 兼容性别名 (Legacy Compatibility)
# ============================================================================

# 保持向后兼容的QColor对象
COLOR_SELECTED = QColor(59, 130, 246, 38)   # PRIMARY_500 with alpha
COLOR_HOVER = QColor(59, 130, 246, 25)      # PRIMARY_500 with alpha
COLOR_DEFAULT_TEXT = QColor(17, 24, 39)     # NEUTRAL_900
COLOR_GRAY_TEXT = QColor(107, 114, 128)     # NEUTRAL_500
COLOR_WHITE = QColor(255, 255, 255)         # NEUTRAL_0
COLOR_LIGHT_GRAY = QColor(229, 231, 235)    # NEUTRAL_200
COLOR_BACKGROUND_LIGHT = NEUTRAL_50
COLOR_BACKGROUND_DARK = BACKGROUND_DARK
PRIMARY_BUTTON_BACKGROUND = PRIMARY_500
PRIMARY_BUTTON_HOVER = PRIMARY_600
HOVER_COLOR = PRIMARY_50
SIDEBAR_ICON_SELECTED = PRIMARY_500
LINE_COLOR = NEUTRAL_200

# ============================================================================
# 🎨 CSS/HTML 样式常量 (CSS/HTML Style Constants)
# ============================================================================

# 代码高亮色彩
CODE_HIGHLIGHT_COLORS = {
    'background': '#f6f8fa',                    # 代码块背景
    'inline_background': 'rgba(27,31,35,.05)', # 行内代码背景
    'text': '#333',                             # 代码文字
    'keyword': '#0000FF',                       # 关键字
    'string': '#008000',                        # 字符串
    'number': '#0000CD',                        # 数字
    'comment': '#808080',                       # 注释
    'tag': '#000080',                           # HTML标签
    'attribute': '#FF0000',                     # HTML属性
}

# 主题样式
THEME_COLORS = {
    'light': {
        'body_bg': '#f9f9f9',                   # 浅色主题背景
        'body_text': '#333',                    # 浅色主题文字
        'h2_color': '#1a1a1a',                  # 浅色主题标题
        'border': '#ddd',                       # 浅色主题边框
        'blockquote_border': '#666',            # 浅色主题引用边框
        'blockquote_text': '#555',              # 浅色主题引用文字
    },
    'dark': {
        'body_bg': '#2d2d2d',                   # 深色主题背景
        'body_text': '#e9e9e9',                 # 深色主题文字
        'h2_color': '#fff',                     # 深色主题标题
        'border': '#444',                       # 深色主题边框
        'blockquote_border': '#777',            # 深色主题引用边框
        'blockquote_text': '#bbb',              # 深色主题引用文字
        'link': '#61afef',                      # 深色主题链接
    }
}