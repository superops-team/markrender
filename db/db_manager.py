# -*- coding: utf-8 -*-
from sqlalchemy import Column, DateTime, Integer, String, create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker
from .base import Base
from .models import Theme


class SingletonEngine:
    _instances = {}

    @classmethod
    def get_instance(cls, db_path):
        if db_path not in cls._instances:
            from sqlalchemy import create_engine
            cls._instances[db_path] = create_engine(
                "sqlite:///{}".format(db_path),
                connect_args={
                    'check_same_thread': False})
        return cls._instances[db_path]


class ThemeManager:
    def __init__(self, db_path):
        self.engine = SingletonEngine.get_instance(db_path)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def create_theme(self, name, css_config):
        session = self.Session()
        try:
            new_theme = Theme(
                name=name,
                css_config=css_config,
                created_at=func.now(),
                updated_at=func.now(),
            )
            session.add(new_theme)
            session.commit()
            return new_theme
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_theme(self, name):
        session = self.Session()
        try:
            return session.query(Theme).filter_by(name=name).first()
        except Exception as e:
            raise e
        finally:
            session.close()

    def get_all_themes(self):
        session = self.Session()
        try:
            return session.query(Theme).all()
        except Exception as e:
            raise e
        finally:
            session.close()

    def update_theme(self, name, new_css_config):
        session = self.Session()
        try:
            theme = session.query(Theme).filter_by(name=name).first()
            if theme:
                theme.css_config = new_css_config
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete_theme(self, name):
        session = self.Session()
        try:
            theme = session.query(Theme).filter_by(name=name).first()
            if theme:
                session.delete(theme)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def theme_exists(self, name):
        session = self.Session()
        try:
            return session.query(Theme).filter_by(
                name=name).first() is not None
        except Exception as e:
            raise e
        finally:
            session.close()
