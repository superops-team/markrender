# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from .models import Base, MarkRenderData, MarkRenderChangeHistory
from db.db_manager import SingletonEngine, get_user_data_dir
from utils.hash_utils import calculate_md5
from utils.logger_utils import logger  # 添加 logger 导入
from utils import time_utils
import json


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
        """加载所有历史记录，按设置中的排序条件排列"""
        from db.settings_manager import SettingsManager
        
        # 获取搜索排序设置，默认按更新时间排序
        settings_manager = SettingsManager()
        sort_setting = settings_manager.get_setting('general', 'search_sort', 'updated_time')
        
        session = self.Session()
        try:
            query = session.query(MarkRenderData)
            if page_type:
                query = query.filter_by(page_type=page_type)
            
            # 根据设置中的排序条件进行排序
            if sort_setting == 'created_time':
                # 按创建时间降序排列
                query = query.order_by(MarkRenderData.created_at.desc())
            elif sort_setting == 'name':
                # 按名称升序排列
                query = query.order_by(MarkRenderData.title.asc())
            else:
                # 默认按更新时间降序排列
                query = query.order_by(MarkRenderData.updated_at.desc())
            
            # 应用限制
            histories = query.limit(limit).all()
            return [
                {
                    'title': getattr(h, 'title', ''),
                    'id': getattr(h, 'id', 0),
                    'tags': getattr(h, 'tags', ''),
                    'file_path': getattr(h, 'file_path', ''),
                    'theme_id': getattr(h, 'theme_id', 0),
                    'page_type': getattr(h, 'page_type', ''),
                    'converter': getattr(h, 'converter', ''),
                    'converter_start': getattr(h, 'converter_start', None),
                    'converter_end': getattr(h, 'converter_end', None),
                    'status': getattr(h, 'status', ''),
                    'content': getattr(h, 'content', ''),
                    'render_style': getattr(h, 'render_style', ''),
                    'updated_at': getattr(h, 'updated_at', None),
                    'content_md5': getattr(h, 'content_md5', ''),
                    'created_at': getattr(h, 'created_at', None),
                    'page_settings': getattr(h, 'page_settings', ''),
                    'page_engine': getattr(h, 'page_engine', ''),
                    'file_size': len(getattr(h, 'content', '') or ''),
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
        content_str = ''  # 初始化 content_str
        try:
            import json
            
            # 确保content是字符串类型
            if isinstance(content, dict):
                content_str = json.dumps(content, ensure_ascii=False)
            elif not isinstance(content, str):
                content_str = str(content)
            else:
                content_str = content
                
            content_md5 = calculate_md5(content_str)
            now = time_utils.now()  # 获取当前北京时间
            if id:
                # 更新现有记录
                history = session.query(MarkRenderData).filter_by(id=id).first()
                if history:
                    # 保存旧内容用于历史记录
                    old_content = getattr(history, 'content', '')
                    old_theme_id = getattr(history, 'theme_id', 0)
                    old_page_type = getattr(history, 'page_type', '')
                    old_page_engine = getattr(history, 'page_engine', '')
                    old_page_settings = getattr(history, 'page_settings', '')
                    old_file_path = getattr(history, 'file_path', '')
                    
                    if content_md5 and content_md5 != (getattr(history, 'content_md5', '') or ''):
                        setattr(history, 'content_md5', content_md5)
                    if title and title != (getattr(history, 'title', '') or ''):
                        setattr(history, 'title', title)
                    if content_str and content_str != (getattr(history, 'content', '') or ''):
                        setattr(history, 'content', content_str)
                        changed = True
                    if file_path and file_path != (getattr(history, 'file_path', '') or ''):
                        setattr(history, 'file_path', file_path)
                    if theme_id and theme_id != (getattr(history, 'theme_id', 0) or 0):
                        setattr(history, 'theme_id', theme_id)
                    if tags and tags != (getattr(history, 'tags', '') or ''):
                        setattr(history, 'tags', tags)
                    if page_type and page_type != (getattr(history, 'page_type', '') or ''):
                        setattr(history, 'page_type', page_type)
                    if render_style and render_style != (getattr(history, 'render_style', '') or ''):
                        setattr(history, 'render_style', render_style)
                    if page_settings and page_settings != (getattr(history, 'page_settings', '') or ''):
                        setattr(history, 'page_settings', page_settings)
                    if page_engine and page_engine != (getattr(history, 'page_engine', '') or ''):
                        setattr(history, 'page_engine', page_engine)
                    setattr(history, 'updated_at', now)  # 使用北京时间更新
                    if converter_start:
                        setattr(history, 'converter_start', converter_start)
                    if converter_end:
                        setattr(history, 'converter_end', converter_end)
                    if status:
                        setattr(history, 'status', status)
                    if converter:
                        setattr(history, 'converter', converter)
                    session.commit()
                    
                    # 如果内容有变化，记录历史变更
                    if changed:
                        self._save_change_history(
                            session, id, old_content, content_str, 'content_update',
                            'user_edit', 'user', '127.0.0.1', file_path or old_file_path or '',
                            theme_id or old_theme_id or 0, page_type or old_page_type or '',
                            page_engine or old_page_engine or '', page_settings or old_page_settings or ''
                        )
                    return getattr(history, 'id', 0)
                else:
                    raise ValueError(f"未找到 ID 为 {id} 的记录")
            else:
                # 创建新记录
                changed = True
                new_history = MarkRenderData(
                    title=title,
                    content=content_str,
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
                id = getattr(new_history, 'id', 0)
                
                # 记录创建历史
                self._save_change_history(
                    session, id, '', content_str, 'content_create',
                    'user_create', 'user', '127.0.0.1', file_path or '',
                    theme_id or 0, page_type or '', page_engine or '', page_settings or ''
                )
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving markdown: {e}")
            raise e
        finally:
            session.close()
            if id and content_str and changed:
                self.sync_write_localdisk(id, content_str, page_type, page_engine)
        return id

    def _save_change_history(self, session, file_id, old_content, new_content, change_type, 
                           change_reason, change_by, change_ip, change_file_path, 
                           change_theme_id, change_page_type, change_page_engine, 
                           change_page_settings):
        """
        保存变更历史记录
        Args:
            session: 数据库会话
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
        """
        try:
            # 确保new_content是字符串类型
            if isinstance(new_content, dict):
                content_str = json.dumps(new_content, ensure_ascii=False)
            elif not isinstance(new_content, str):
                content_str = str(new_content)
            else:
                content_str = new_content
                
            change_content_md5 = calculate_md5(content_str)
            
            # 确保old_content也是字符串类型
            if isinstance(old_content, dict):
                old_content_str = json.dumps(old_content, ensure_ascii=False)
            elif not isinstance(old_content, str):
                old_content_str = str(old_content)
            else:
                old_content_str = old_content
            
            new_change = MarkRenderChangeHistory(
                file_id=file_id,
                old_content=old_content_str,
                new_content=content_str,
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
                change_page_id=file_id
            )
            session.add(new_change)
            session.commit()
            return new_change
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving change history: {e}")
            raise e

    def sync_write_localdisk(self, id, content, page_type=None, page_engine=None):
        """
        同步将内容写入本地磁盘
        Args:
            id: 记录ID
            content: 内容
        """
        try:
            import json
            
            # 确保content是字符串类型
            if isinstance(content, dict):
                content_str = json.dumps(content, ensure_ascii=False)
            elif not isinstance(content, str):
                content_str = str(content)
            else:
                content_str = content
                
            suffix = 'markrender'
            if page_type == 'markdown':
                suffix = 'md'
            if page_engine == 'excalidraw':
                suffix = 'excalidraw'
            with open(f'{get_user_data_dir()}/output/{id}.{suffix}', 'w') as f:
                f.write(content_str)
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
            import json
            
            # 确保new_content是字符串类型
            if isinstance(new_content, dict):
                content_str = json.dumps(new_content, ensure_ascii=False)
            elif not isinstance(new_content, str):
                content_str = str(new_content)
            else:
                content_str = new_content
                
            change_content_md5 = hashlib.md5(content_str.encode()).hexdigest()
            
            # 确保old_content也是字符串类型
            if isinstance(old_content, dict):
                old_content_str = json.dumps(old_content, ensure_ascii=False)
            elif not isinstance(old_content, str):
                old_content_str = str(old_content)
            else:
                old_content_str = old_content
            
            new_change = MarkRenderChangeHistory(
                file_id=file_id,
                old_content=old_content_str,
                new_content=content_str,
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
                file_id=file_id).order_by(MarkRenderChangeHistory.change_at.desc()).limit(20).all()
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
                'title': getattr(record, 'title', ''),
                'content': getattr(record, 'content', ''),
                'tags': getattr(record, 'tags', ''),
                'file_path': getattr(record, 'file_path', ''),
                'theme_id': getattr(record, 'theme_id', 0),
                'converter': getattr(record, 'converter', ''),
                'converter_start': getattr(record, 'converter_start', None),
                'converter_end': getattr(record, 'converter_end', None),
                'status': getattr(record, 'status', ''),
                'render_style': getattr(record, 'render_style', ''),
                'updated_at': getattr(record, 'updated_at', None),
                'content_md5': getattr(record, 'content_md5', ''),
                'created_at': getattr(record, 'created_at', None),
                'page_type': getattr(record, 'page_type', ''),
                'page_settings': getattr(record, 'page_settings', ''),
                'page_engine': getattr(record, 'page_engine', ''),
                'id': getattr(record, 'id', 0)
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
                # 保存旧标题用于历史记录
                old_title = getattr(record, 'title', '')
                setattr(record, 'title', title)
                session.commit()
                
                # 记录标题变更历史
                self._save_change_history(
                    session, id, old_title or '', title or '', 'title_update',
                    'user_edit', 'user', '127.0.0.1', getattr(record, 'file_path', '') or '',
                    getattr(record, 'theme_id', 0) or 0, getattr(record, 'page_type', '') or '', 
                    getattr(record, 'page_engine', '') or '', getattr(record, 'page_settings', '') or ''
                )
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
                # 保存旧设置用于历史记录
                old_settings = getattr(record, 'page_settings', '')
                setattr(record, 'page_settings', page_settings)
                setattr(record, 'updated_at', time_utils.now())
                session.commit()
                
                # 记录页面设置变更历史
                self._save_change_history(
                    session, id, old_settings or '', page_settings or '', 'page_settings_update',
                    'user_edit', 'user', '127.0.0.1', getattr(record, 'file_path', '') or '',
                    getattr(record, 'theme_id', 0) or 0, getattr(record, 'page_type', '') or '', 
                    getattr(record, 'page_engine', '') or '', page_settings or ''
                )
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
                # 保存旧引擎用于历史记录
                old_engine = getattr(record, 'page_engine', '')
                setattr(record, 'page_engine', page_engine)
                setattr(record, 'updated_at', time_utils.now())
                session.commit()
                
                # 记录页面引擎变更历史
                self._save_change_history(
                    session, id, old_engine or '', page_engine or '', 'page_engine_update',
                    'user_edit', 'user', '127.0.0.1', getattr(record, 'file_path', '') or '',
                    getattr(record, 'theme_id', 0) or 0, getattr(record, 'page_type', '') or '', 
                    page_engine or '', getattr(record, 'page_settings', '') or ''
                )
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
                return getattr(record, 'page_settings', None)
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
                return getattr(record, 'page_engine', None)
            return None
        except Exception as e:
            logger.error(f"Error getting page engine: {e}")
            raise e
        finally:
            session.close()