from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func

# 创建基础类
Base = declarative_base()


class SingletonEngine:
    _instance = None
    _db_path = None

    @classmethod
    def get_instance(cls, db_path):
        if cls._instance is None:
            cls._db_path = db_path
            from sqlalchemy import create_engine
            cls._instance = create_engine("sqlite:///{}".format(db_path))
        elif cls._db_path != db_path:
            import logging
            logging.warning(
                '尝试使用不同的数据库路径，当前路径: %s, 尝试路径: %s',
                cls._db_path,
                db_path)
            raise ValueError(
                'Database path cannot be changed once the engine is initialized.')
        return cls._instance


class Theme(Base):
    __tablename__ = "themes"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    css_config = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ThemeManager:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = SingletonEngine._db_path
        engine = SingletonEngine.get_instance(db_path)
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

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
