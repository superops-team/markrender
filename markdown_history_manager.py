# -*- coding: utf-8 -*-
from sqlalchemy import Column, DateTime, Integer, String, Text
from db_manager import SingletonEngine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func

# 创建基础类
Base = declarative_base()


class MarkdownFileHistory(Base):
    __tablename__ = "markdown_file_history"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    tags = Column(String)
    render_style = Column(String)


class MarkdownChangeHistory(Base):
    __tablename__ = "markdown_change_history"

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, nullable=False)
    old_content = Column(Text, nullable=False)
    new_content = Column(Text, nullable=False)
    changed_at = Column(DateTime(timezone=True), server_default=func.now())


class MarkdownHistoryManager:
    def __init__(self, db_path):
        if db_path is None:
            db_path = SingletonEngine._db_path
        self.engine = SingletonEngine.get_instance(db_path)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def save_file_history(
            self,
            title,
            content,
            tags=None,
            render_style=None):
        session = self.Session()
        try:
            new_history = MarkdownFileHistory(
                title=title,
                content=content,
                tags=tags,
                render_style=render_style
            )
            session.add(new_history)
            session.commit()
            return new_history
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def search_file_history(self, keyword=None):
        session = self.Session()
        try:
            if keyword:
                return session.query(MarkdownFileHistory).filter(
                    MarkdownFileHistory.title.ilike(f'%{keyword}%')).all()
            else:
                return session.query(MarkdownFileHistory).all()
        except Exception as e:
            raise e
        finally:
            session.close()

    def get_file_history(self, title):
        session = self.Session()
        try:
            return session.query(MarkdownFileHistory).filter_by(
                title=title).all()
        except Exception as e:
            raise e
        finally:
            session.close()

    def save_change_history(self, file_id, old_content, new_content):
        session = self.Session()
        try:
            new_change = MarkdownChangeHistory(
                file_id=file_id,
                old_content=old_content,
                new_content=new_content
            )
            session.add(new_change)
            session.commit()
            return new_change
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_change_history(self, file_id):
        session = self.Session()
        try:
            return session.query(MarkdownChangeHistory).filter_by(
                file_id=file_id).all()
        except Exception as e:
            raise e
        finally:
            session.close()
