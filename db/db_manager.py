# -*- coding: utf-8 -*-

import os
from platform import system

# 删除原来的路径定义
# settings_db = 'settings.db'
# data_db = 'data.db'

app_name = 'MarkRender'

def get_user_data_dir():
    """统一管理多平台数据库路径"""
    if system() == 'Windows':
        user_data_dir = os.path.join(os.getenv('APPDATA'), app_name)
    elif system() == 'Darwin':
        user_data_dir = os.path.expanduser(f'~/Library/Application Support/{app_name}')
    else:
        user_data_dir = os.path.join(os.path.expanduser('~'), '.local', 'share', app_name)

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
