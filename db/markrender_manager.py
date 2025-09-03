# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from .models import Base, MarkRenderData, MarkRenderChangeHistory
from db.db_manager import SingletonEngine, get_user_data_dir
from utils.hash_utils import calculate_md5
from utils.logger_utils import logger  # 添加 logger 导入
from utils import time_utils


class MarkRenderManager:
    def __init__(self, db_path=None):
        if db_path is None:
            self.db_path = SingletonEngine.get_db_path('data.db')
        else:
            self.db_path = db_path
        self.engine = SingletonEngine.get_instance(self.db_path)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_item(self, new_file):
        try:
            with self.Session() as session:
                session.add(new_file)
                session.commit()
                return True
        except Exception as e:
            logger.error(f"Error adding history item: {e}")
            return False

    def delete_item(self, item_id):
        try:
            with self.Session() as session:
                history_item = session.query(MarkRenderData).filter_by(id=item_id).first()
                if history_item:
                    session.delete(history_item)
                    session.commit()
                    return True
                return False
        except Exception as e:
            logger.error(f"Error deleting history item: {e}")
            return False

    def load_items(self, limit=20, page_type=''):
        """加载所有历史记录"""
        session = self.Session()
        try:
            query = session.query(MarkRenderData)
            if page_type:
                query = query.filter_by(page_type=page_type)
            histories = query.order_by(MarkRenderData.created_at.desc()).limit(limit).all()
            return [
                {
                    'title': h.title,
                    'id': h.id,
                    'tags': h.tags,
                    'file_path': h.file_path,
                    'theme_id': h.theme_id,
                    'page_type': h.page_type,
                    'converter': h.converter,
                    'converter_start': h.converter_start,
                    'converter_end': h.converter_end,
                    'status': h.status,
                    'content': h.content,
                    'render_style': h.render_style,
                    'updated_at': h.updated_at,
                    'content_md5': h.content_md5,
                    'created_at': h.created_at,
                    'page_settings': h.page_settings,
                    'page_engine': h.page_engine,
                    'file_size': len(h.content),
                } for h in histories]
        except Exception as e:
            raise e
        finally:
            session.close()
    
    def save_item(
            self,
            id=None,
            title='',
            content='',
            tags='',
            render_style=None,
            file_path='',
            converter='',
            theme_id=None,
            status='',
            converter_start=None,
            converter_end=None,
            page_type=None,
            page_settings=None,
            page_engine=None,
        ):
        session = self.Session()
        changed = False
        try:
            content_md5 = calculate_md5(content)
            now = time_utils.now()  # 获取当前北京时间
            if id:
                # 更新现有记录
                history = session.query(MarkRenderData).filter_by(id=id).first()
                if history:
                    if content_md5 and content_md5 != history.content_md5:
                        history.content_md5 = content_md5
                    if title and title != history.title:
                        history.title = title
                    if content and content != history.content:
                        history.content = content
                        changed = True
                    if file_path and file_path != history.file_path:
                        history.file_path = file_path
                    if theme_id and theme_id != history.theme_id:
                        history.theme_id = theme_id
                    if tags and tags != history.tags:
                        history.tags = tags
                    if page_type and page_type != history.page_type:
                        history.page_type = page_type
                    if render_style and render_style != history.render_style:
                        history.render_style = render_style
                    if page_settings and page_settings != history.page_settings:
                        history.page_settings = page_settings
                    if page_engine and page_engine != history.page_engine:
                        history.page_engine = page_engine
                    history.updated_at = now  # 使用北京时间更新
                    if converter_start:
                        history.converter_start = converter_start
                    if converter_end:
                        history.converter_end = converter_end
                    if status:
                        history.status = status
                    if converter:
                        history.converter = converter
                    session.commit()
                    return history.id
                else:
                    raise ValueError(f"未找到 ID 为 {id} 的记录")
            else:
                # 创建新记录
                changed = True
                new_history = MarkRenderData(
                    title=title,
                    content=content,
                    tags=tags,
                    render_style=render_style,
                    content_md5=content_md5,
                    created_at=now,  # 使用北京时间创建
                    updated_at=now,  # 使用北京时间更新
                    file_path=file_path,
                    theme_id=theme_id,
                    converter=converter,
                    converter_start=converter_start,
                    converter_end=converter_end,
                    status=status,
                    page_type=page_type,
                    page_settings=page_settings,
                    page_engine=page_engine,
                )
                session.add(new_history)
                session.commit()
                id = new_history.id
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving markdown: {e}")
            raise e
        finally:
            session.close()
            if id and content and changed:
                self.sync_write_localdisk(id, content)
        return id


    def sync_write_localdisk(self, id, content, page_type=None, page_engine=None):
        """
        同步将内容写入本地磁盘
        Args:
            id: 记录ID
            content: 内容
        """
        try:
            suffix = 'markrender'
            if page_type == 'markdown':
                suffix = 'md'
            if page_engine == 'excalidraw':
                suffix = 'excalidraw'
            with open(f'{get_user_data_dir()}/output/{id}.{suffix}', 'w') as f:
                f.write(content)
        except Exception as e:
            logger.error(f"Error writing to local disk: {e}")


    def search_item(self, keyword=None, page_type=None):
        session = self.Session()
        try:
            if keyword:
                query = session.query(MarkRenderData).filter(
                    MarkRenderData.title.ilike(f'%{keyword}%'))
                if page_type:
                    query = query.filter_by(page_type=page_type)
                return query.all()
            else:
                query = session.query(MarkRenderData)
                if page_type:
                    query = query.filter_by(page_type=page_type)
                return query.all()
        except Exception as e:
            logger.error(f"Error searching markdown: {e}")
            raise e
        finally:
            session.close()

    def get_file_history(self, title, page_type=None):
        session = self.Session()
        try:
            query = session.query(MarkRenderData).filter_by(
                title=title)
            if page_type:
                query = query.filter_by(page_type=page_type)
            return query.all()
        except Exception as e:
            logger.error(f"Error getting file history: {e}")
            raise e
        finally:
            session.close()

    def save_change_history(self, file_id, old_content, new_content, change_type='content_update', 
                           change_reason='user_edit', change_by='user', change_ip='127.0.0.1', 
                           change_file_path='', change_theme_id=1, change_page_type='markdown', 
                           change_page_engine='markdown', change_page_settings='{}', change_page_id=None):
        """
        保存变更历史记录
        Args:
            file_id: 文件ID
            old_content: 旧内容
            new_content: 新内容
            change_type: 变更类型
            change_reason: 变更原因
            change_by: 变更人
            change_ip: 变更IP
            change_file_path: 变更文件路径
            change_theme_id: 变更主题ID
            change_page_type: 变更页面类型
            change_page_engine: 变更页面引擎
            change_page_settings: 变更页面设置
            change_page_id: 变更页面ID
        """
        session = self.Session()
        try:
            # 计算内容MD5
            import hashlib
            change_content_md5 = hashlib.md5(new_content.encode()).hexdigest()
            
            new_change = MarkRenderChangeHistory(
                file_id=file_id,
                old_content=old_content,
                new_content=new_content,
                change_type=change_type,
                change_reason=change_reason,
                change_by=change_by,
                change_ip=change_ip,
                change_content_md5=change_content_md5,
                change_file_path=change_file_path,
                change_theme_id=change_theme_id,
                change_page_type=change_page_type,
                change_page_engine=change_page_engine,
                change_page_settings=change_page_settings,
                change_page_id=change_page_id or file_id
            )
            session.add(new_change)
            session.commit()
            return new_change
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving change history: {e}")
            raise e
        finally:
            session.close()

    def get_change_history(self, file_id):
        session = self.Session()
        try:
            return session.query(MarkRenderChangeHistory).filter_by(
                file_id=file_id).all()
        except Exception as e:
            logger.error(f"Error getting change history: {e}")
            raise e
        finally:
            session.close()
    
    def get_detail(self, id):
        session = self.Session()
        try:
            record = session.query(MarkRenderData).filter_by(
                id=id).first()
            return {
                'title': record.title,
                'content': record.content,
                'tags': record.tags,
                'file_path': record.file_path,
                'theme_id': record.theme_id,
                'converter': record.converter,
                'converter_start': record.converter_start,
                'converter_end': record.converter_end,
                'status': record.status,
                'render_style': record.render_style,
                'updated_at': record.updated_at,
                'content_md5': record.content_md5,
                'created_at': record.created_at,
                'page_type': record.page_type,
                'page_settings': record.page_settings,
                'page_engine': record.page_engine,
                'id': record.id
            }
        except Exception as e:
            logger.error(f"Error getting detail: {e}")
            raise e
        finally:
            session.close()
        
    def update_title(self, id, title):
        if not id:
            return
        if not title:
            return
        session = self.Session()
        try:
            record = session.query(MarkRenderData).filter_by(
                id=id).first()
            if record:
                record.title = title
                session.commit()
            else:
                raise ValueError(f"未找到 ID 为 {id} 的记录")
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating title: {e}")
            raise e
        finally:
            session.close()
    
    def update_page_settings(self, id, page_settings):
        """更新页面定制化配置"""
        if not id:
            return
        if page_settings is None:
            return
        session = self.Session()
        try:
            record = session.query(MarkRenderData).filter_by(
                id=id).first()
            if record:
                record.page_settings = page_settings
                record.updated_at = time_utils.now()
                session.commit()
            else:
                raise ValueError(f"未找到 ID 为 {id} 的记录")
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating page settings: {e}")
            raise e
        finally:
            session.close()
    
    def update_page_engine(self, id, page_engine):
        """更新页面核心处理引擎"""
        if not id:
            return
        if not page_engine:
            return
        session = self.Session()
        try:
            record = session.query(MarkRenderData).filter_by(
                id=id).first()
            if record:
                record.page_engine = page_engine
                record.updated_at = time_utils.now()
                session.commit()
            else:
                raise ValueError(f"未找到 ID 为 {id} 的记录")
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating page engine: {e}")
            raise e
        finally:
            session.close()
    
    def get_page_settings(self, id):
        """获取页面定制化配置"""
        if not id:
            return None
        session = self.Session()
        try:
            record = session.query(MarkRenderData).filter_by(
                id=id).first()
            if record:
                return record.page_settings
            return None
        except Exception as e:
            logger.error(f"Error getting page settings: {e}")
            raise e
        finally:
            session.close()
    
    def get_page_engine(self, id):
        """获取页面核心处理引擎"""
        if not id:
            return None
        session = self.Session()
        try:
            record = session.query(MarkRenderData).filter_by(
                id=id).first()
            if record:
                return record.page_engine
            return None
        except Exception as e:
            logger.error(f"Error getting page engine: {e}")
            raise e
        finally:
            session.close()