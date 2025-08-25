# -*- coding: utf-8 -*-

import os
from platform import system

# 根据 PySide6 提供的参数来判断环境
# 默认使用生产环境名称
app_name = 'MarkRender'


# 删除原来的路径定义
# settings_db = 'settings.db'
# data_db = 'data.db'

def get_user_data_dir():
    """
    获取用户数据目录，根据不同操作系统返回不同路径。
    支持 Windows、macOS 和 Linux。
    """
    app_data_path = os.getenv('MARKDOWN_RENDER_DATA')
    if not app_data_path:
        app_data_path = os.path.join(os.path.expanduser('~'), '.markdown_render')
    if system() == 'Windows':
        user_data_dir = os.path.join(app_data_path, app_name)
    elif system() == 'Darwin':
        user_data_dir = os.path.join(app_data_path, app_name)
    else:
        user_data_dir = os.path.join(app_data_path, app_name)

    os.makedirs(user_data_dir, exist_ok=True)
    os.makedirs(user_data_dir + '/output', exist_ok=True)
    os.makedirs(user_data_dir + '/tmp', exist_ok=True)
    os.makedirs(user_data_dir + '/web_cache', exist_ok=True)
    os.makedirs(user_data_dir + '/web_storage', exist_ok=True)
    
    return user_data_dir

class SingletonEngine:
    _instances = {}

    @staticmethod
    def get_db_path(db_name):
        """统一管理多平台数据库路径"""
        user_data_dir = get_user_data_dir()
        return os.path.join(user_data_dir, db_name)

    @classmethod
    def get_instance(cls, db_path):
        if db_path not in cls._instances:
            from sqlalchemy import create_engine
            print(f"Creating database engine for path: {db_path}")
            cls._instances[db_path] = create_engine(
                "sqlite:///{}".format(db_path),
                connect_args={
                    'check_same_thread': False})
        return cls._instances[db_path]

    @classmethod
    def get_settings_instance(cls):
        return cls.get_instance(cls.get_db_path('settings.db'))

    @classmethod
    def get_data_instance(cls):
        return cls.get_instance(cls.get_db_path('data.db'))
