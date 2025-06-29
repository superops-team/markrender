# -*- coding: utf-8 -*-
from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from .models import Base, MarkdownFileHistory, MarkdownChangeHistory
from db.db_manager import SingletonEngine
from utils.hash_utils import calculate_md5
from utils.logger_utils import logger  # 添加 logger 导入


class MarkdownManager:
    def __init__(self, db_path=None):
        if db_path is None:
            self.db_path = SingletonEngine.get_db_path('data.db')
        else:
            self.db_path = db_path
        self.engine = SingletonEngine.get_instance(self.db_path)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_history_item(self, new_file):
        try:
            with self.Session() as session:
                session.add(new_file)
                session.commit()
                return True
        except Exception as e:
            logger.error(f"Error adding history item: {e}")
            return False

    def delete_history_item(self, item_id):
        try:
            with self.Session() as session:
                history_item = session.query(MarkdownFileHistory).filter_by(id=item_id).first()
                if history_item:
                    session.delete(history_item)
                    session.commit()
                    return True
                return False
        except Exception as e:
            logger.error(f"Error deleting history item: {e}")
            return False

    def load_history(self):
        """加载所有历史记录"""
        session = self.Session()
        try:
            histories = session.query(MarkdownFileHistory).all()
            return [{'title': h.title, 'id': h.id, 'content': h.content, 'tags': h.tags, 'render_style': h.render_style} for h in histories]
        except Exception as e:
            raise e
        finally:
            session.close()

    def save_markdown(
            self,
            title,
            content,
            tags=None,
            render_style=None,
            id=None):
        session = self.Session()
        try:
            content_md5 = calculate_md5(content)
            if id:
                # 更新现有记录
                history = session.query(MarkdownFileHistory).filter_by(id=id).first()
                if history:
                    history.title = title
                    history.content = content
                    history.tags = tags
                    history.render_style = render_style
                    history.content_md5 = content_md5
                    session.commit()
                    return history
                else:
                    raise ValueError(f"未找到 ID 为 {id} 的记录")
            else:
                # 创建新记录
                new_history = MarkdownFileHistory(
                    title=title,
                    content=content,
                    tags=tags,
                    render_style=render_style,
                    content_md5=content_md5
                )
                session.add(new_history)
                session.commit()
                return new_history
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def search_markdown(self, keyword=None):
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