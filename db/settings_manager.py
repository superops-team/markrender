import json
from .models import Settings, Base
from utils.logger_utils import logger
from db.db_manager import SingletonEngine
from sqlalchemy.orm import sessionmaker

class SettingsManager:
    def __init__(self, db_path: str = None):
        if db_path is None:
            self.db_path = SingletonEngine.get_db_path('settings.db')
        else:
            self.db_path = db_path
        self.engine = SingletonEngine.get_settings_instance()
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def create_settings(self, key: str, value: dict) -> Settings:
        """
        创建或更新 Settings，如果 key 存在则更新，不存在则创建
        :param key: Settings 的 key
        :param value: Settings 的 value，应为字典类型
        :return: 创建或更新后的 Settings 实例
        """
        value_str = json.dumps(value)  # 将字典转换为 JSON 字符串
        try:
            with self.Session() as session:
                existing_settings = session.query(Settings).filter(Settings.key == key).first()
                if existing_settings:
                    existing_settings.value = value_str
                    session.commit()
                    session.refresh(existing_settings)
                    return existing_settings
                else:
                    new_settings = Settings(key=key, value=value_str)
                    session.add(new_settings)
                    session.commit()
                    session.refresh(new_settings)
                    return new_settings
        except Exception as e:
            logger.error(f"Error creating settings: {e}")
            return None
        finally:
            session.close()

    def get_settings_by_key(self, key: str) -> Settings:
        """
        根据 key 获取 Settings
        :param key: Settings 的 key
        :return: Settings 的 settings 字典，如果未找到则返回 None
        """
        session = self.Session()
        try:
            settings_obj = session.query(Settings).filter(Settings.key == key).first()
            return settings_obj
        except Exception as e:
            logger.error(f"Error getting settings: {e}")
            return None
        finally:
            session.close()

    
    def get_settings_dict(self, key: str) -> dict:
        """
        根据 key 获取 Settings
        :param key: Settings 的 key
        :return: Settings 的 settings 字典，如果未找到则返回 None
        """
        session = self.Session()
        try:
            settings_obj = session.query(Settings).filter(Settings.key == key).first()
            if settings_obj:
                try:
                    return json.loads(settings_obj.value)
                except json.JSONDecodeError:
                    logger.error(f"Error parsing JSON settings for key {key}")
                    return None
            return None
        except Exception as e:
            logger.error(f"Error getting settings: {e}")
            return None
        finally:
            session.close()

    def update_settings(self, key: str, **kwargs) -> dict:
        """
        根据 key 更新 Settings   
        :param key: Settings 的 key
        :param kwargs: 要更新的字段和值，如果包含 settings 则应为字典类型
        :return: 更新成功返回 True未找到则返回 False
        """
        settings_obj = self.get_settings_by_key(key)
        if settings_obj:
            settings = json.loads(settings_obj.value)
            for k, value in kwargs.items():
                settings[k] = value
            settings_str = json.dumps(settings)
            settings_obj.value = settings_str
            return True
        return False


    def delete_settings(self, key: str,) -> bool:
        """
        根据 key 删除 Settings
        :param key: Settings 的 key
        :return: 删除成功返回 True，未找到则返回 False
        """
        settings_obj = self.get_settings_by_key(key)
        if settings_obj:
            session = self.Session()
            try:
                session.delete(settings_obj)
                session.commit()
                return True
            except Exception as e:
                logger.error(f"Error deleting settings: {e}")
                return False
            finally:
                session.close()
        return False
    
    def get_setting(self, ns: str, key: str, default=None):
        '''
        获取设置
        :param ns: 命名空间
        :param key: 键
        :param default: 默认值
        :return: 设置值
        '''
        settings = self.get_settings_dict(ns)
        if settings is None:
            return default
        return settings.get(key, default)
    
    def set_setting(self, ns: str, key: str, value):
        settings = self.get_settings_dict(ns)
        if settings is None:
            settings = {}
        settings[key] = value
        self.create_settings(ns, settings)
