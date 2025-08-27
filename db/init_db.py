# -*- coding: utf-8 -*-
import os
import logging
import sys

# 尝试导入统一的CSS样式常量
try:
    from app.preference.css_constants import THEME_STYLES, BASE_CODE_STYLE
except ImportError:
    # 如果无法导入，使用简化样式
    BASE_CODE_STYLE = """
<style>
    h1 { text-align: center; color: #333; }
    pre { background: #f6f8fa; padding: 16px; border-radius: 3px; }
    code { background: rgba(27,31,35,.05); padding: 0.2em 0.4em; border-radius: 3px; }
</style>
"""

# 主题样式 - 使用统一的样式系统
try:
    from app.preference.css_constants import THEME_STYLES
    themes = THEME_STYLES
except ImportError:
    # 备用主题样式
    themes = {
        "默认样式": BASE_CODE_STYLE + "<style>body { font-family: system-ui; }</style>",
        "GitHub风格": BASE_CODE_STYLE + "<style>body { font-family: system-ui; } h2 { border-bottom: 1px solid #eee; }</style>",
        "浅色主题": BASE_CODE_STYLE + "<style>body { background: #f9f9f9; color: #333; }</style>",
        "深色主题": BASE_CODE_STYLE + "<style>body { background: #2d2d2d; color: #e9e9e9; }</style>",
        "文档风格": BASE_CODE_STYLE + "<style>body { font-family: serif; max-width: 800px; margin: 0 auto; }</style>",
    }

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


def init_db(db_path):
    # 确保主题表已创建
    from db.base import Base
    from db.db_manager import SingletonEngine
    from db.theme_manager import ThemeManager
    engine = SingletonEngine.get_settings_instance()
    Base.metadata.create_all(engine)
    manager = ThemeManager()
    manager.Session.configure(bind=manager.engine)
    for name, theme_style in themes.items():
        if manager.theme_exists(name):
            continue
        full_style = base_style + theme_style
        manager.create_theme(name, full_style)
