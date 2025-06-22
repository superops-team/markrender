from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func

# 创建基础类
Base = declarative_base()


class Theme(Base):
    __tablename__ = "themes"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    css_config = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ThemeManager:
    def __init__(self):
        self.engine = create_engine("sqlite:///config.db")
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
            return session.query(Theme).filter_by(name=name).first() is not None
        except Exception as e:
            raise e
        finally:
            session.close()


if __name__ == "__main__":
    manager = ThemeManager()
    # 示例用法
    # new_theme = manager.create_theme('new_theme', 'body { color: red; }')
    # print(manager.get_theme('new_theme'))
    # print(manager.get_all_themes())
    # print(manager.update_theme('new_theme', 'body { color: blue; }'))
    # print(manager.delete_theme('new_theme'))
