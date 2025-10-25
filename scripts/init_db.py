# -*- coding: utf-8 -*-
import os
import logging
import sys

# 修复导入路径问题
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.db_manager import SingletonEngine
from db.theme_manager import ThemeManager
# 导入统一的CSS样式常量
try:
    from app.preference.css_constants import THEME_STYLES, get_theme_style
except ImportError:
    # 如果无法导入，使用简化的样式定义
    THEME_STYLES = {}

_db_path = ""


def get_app_path():
    """获取应用程序的根路径，兼容打包后的环境"""
    if getattr(sys, 'frozen', False):
        # 如果是打包后的可执行文件
        return os.path.dirname(sys.executable)
    else:
        # 如果是直接运行的Python脚本
        return os.path.dirname(os.path.abspath(__file__))


def get_user_data_dir():
    """获取用户数据目录"""
    app_name = "MarkRender"
    user_data_dir = os.path.expanduser(
        f'~/Library/Application Support/{app_name}')
    os.makedirs(user_data_dir, exist_ok=True)
    return user_data_dir


def get_db_path(db_name):
    """获取SQLite数据库文件的绝对路径"""
    return os.path.join(get_user_data_dir(), db_name)


def get_db_path_v1(db_name):
    global _db_path
    if _db_path:
        return _db_path
    home_dir = os.path.expanduser('~')
    markrender_dir = os.path.join(home_dir, '.markrender')
    os.makedirs(markrender_dir, exist_ok=True)
    _db_path = os.path.join(markrender_dir, db_name)
    logging.info("use db_path=%s as config", _db_path)
    return _db_path


def init_themes(manager):
    """初始化主题数据 - 使用统一的样式常量"""
    # 尝试使用新的样式系统
    try:
        from app.preference.css_constants import THEME_STYLES
        themes_to_use = THEME_STYLES
    except ImportError:
        # 如果无法导入，使用备用样式
        themes_to_use = {
            "默认样式": "<style>body { font-family: system-ui; }</style>"
        }
    
    for name, theme_style in themes_to_use.items():
        if manager.theme_exists(name):
            continue
        manager.create_theme(name, theme_style)