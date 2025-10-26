# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
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
                    # 树形结构字段
                    'parent_id': getattr(h, 'parent_id', None),
                    'order': getattr(h, 'order', 0),
                    'level': getattr(h, 'level', 0),
                    'is_folder': getattr(h, 'is_folder', 0),
                    # 图标和显示字段
                    'icon_type': getattr(h, 'icon_type', None),
                    'icon_path': getattr(h, 'icon_path', None),
                    'icon_color': getattr(h, 'icon_color', None),
                    'display_name': getattr(h, 'display_name', None),
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
            # 树形结构参数
            parent_id=None,
            order=None,
            level=None,
            is_folder=None,
            # 图标和显示参数
            icon_type=None,
            icon_path=None,
            icon_color=None,
            display_name=None,
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
                    
                    # 更新字段
                    setattr(history, 'content', content_str)
                    setattr(history, 'content_md5', content_md5)
                    setattr(history, 'updated_at', now)
                    
                    # 更新其他可选字段
                    if title is not None:
                        setattr(history, 'title', title)
                    if tags is not None:
                        setattr(history, 'tags', tags)
                    if render_style is not None:
                        setattr(history, 'render_style', render_style)
                    if file_path is not None:
                        setattr(history, 'file_path', file_path)
                    if converter is not None:
                        setattr(history, 'converter', converter)
                    if theme_id is not None:
                        setattr(history, 'theme_id', theme_id)
                    if status is not None:
                        setattr(history, 'status', status)
                    if converter_start is not None:
                        setattr(history, 'converter_start', converter_start)
                    if converter_end is not None:
                        setattr(history, 'converter_end', converter_end)
                    if page_type is not None:
                        setattr(history, 'page_type', page_type)
                    if page_settings is not None:
                        setattr(history, 'page_settings', page_settings)
                    if page_engine is not None:
                        setattr(history, 'page_engine', page_engine)
                    # 树形结构字段
                    if parent_id is not None:
                        setattr(history, 'parent_id', parent_id)
                    if order is not None:
                        setattr(history, 'order', order)
                    if level is not None:
                        setattr(history, 'level', level)
                    if is_folder is not None:
                        setattr(history, 'is_folder', is_folder)
                    # 图标和显示字段
                    if icon_type is not None:
                        setattr(history, 'icon_type', icon_type)
                    if icon_path is not None:
                        setattr(history, 'icon_path', icon_path)
                    if icon_color is not None:
                        setattr(history, 'icon_color', icon_color)
                    if display_name is not None:
                        setattr(history, 'display_name', display_name)
                    
                    session.commit()
                    changed = True
                else:
                    # 记录不存在，创建新记录
                    new_history = MarkRenderData(
                        title=title or '',
                        content=content_str,
                        content_md5=content_md5,
                        tags=tags or '',
                        render_style=render_style or '',
                        file_path=file_path or '',
                        converter=converter or '',
                        theme_id=theme_id or 0,
                        status=status or 'processed',
                        converter_start=converter_start,
                        converter_end=converter_end,
                        page_type=page_type or 'markdown',
                        page_settings=page_settings or '',
                        page_engine=page_engine or 'markdown',
                        updated_at=now,
                        created_at=now,
                        # 树形结构字段
                        parent_id=parent_id,
                        order=order if order is not None else 0,
                        level=level if level is not None else 0,
                        is_folder=is_folder if is_folder is not None else 0,
                        # 图标和显示字段
                        icon_type=icon_type,
                        icon_path=icon_path,
                        icon_color=icon_color,
                        display_name=display_name,
                    )
                    session.add(new_history)
                    session.commit()
                    id = getattr(new_history, 'id', 0)
                    changed = True
                    
                    # 记录创建历史
                    self._save_change_history(
                        session, id, '', content_str, 'content_create',
                        'user_create', 'user', '127.0.0.1', file_path or '',
                        theme_id or 0, page_type or '', page_engine or '', page_settings or ''
                    )
            else:
                # 创建新记录
                new_history = MarkRenderData(
                    title=title or '',
                    content=content_str,
                    content_md5=content_md5,
                    tags=tags or '',
                    render_style=render_style or '',
                    file_path=file_path or '',
                    converter=converter or '',
                    theme_id=theme_id or 0,
                    status=status or 'processed',
                    converter_start=converter_start,
                    converter_end=converter_end,
                    page_type=page_type or 'markdown',
                    page_settings=page_settings or '',
                    page_engine=page_engine or 'markdown',
                    updated_at=now,
                    created_at=now,
                    # 树形结构字段
                    parent_id=parent_id,
                    order=order if order is not None else 0,
                    level=level if level is not None else 0,
                    is_folder=is_folder if is_folder is not None else 0,
                    # 图标和显示字段
                    icon_type=icon_type,
                    icon_path=icon_path,
                    icon_color=icon_color,
                    display_name=display_name,
                )
                session.add(new_history)
                session.commit()
                id = getattr(new_history, 'id', 0)
                changed = True
                
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
            # 设置文件后缀，默认为markdown
            suffix = 'markdown'  # 默认后缀
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
                'id': getattr(record, 'id', 0),
                # 树形结构字段
                'parent_id': getattr(record, 'parent_id', None),
                'order': getattr(record, 'order', 0),
                'level': getattr(record, 'level', 0),
                'is_folder': getattr(record, 'is_folder', 0),
                # 图标和显示字段
                'icon_type': getattr(record, 'icon_type', None),
                'icon_path': getattr(record, 'icon_path', None),
                'icon_color': getattr(record, 'icon_color', None),
                'display_name': getattr(record, 'display_name', None),
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
                pass
                pass
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
            session.rollback()
            logger.error(f"Error getting page engine: {e}")
            return None
        finally:
            session.close()
            
    def get_children(self, parent_id=None):
        """获取指定父节点的所有子节点"""
        session = self.Session()
        try:
            if parent_id is None:
                # 获取根节点（parent_id为None或空的记录）
                records = session.query(MarkRenderData).filter(
                    or_(MarkRenderData.parent_id == None, MarkRenderData.parent_id == '')
                ).order_by(MarkRenderData.order).all()
            else:
                # 获取指定父节点的子节点
                records = session.query(MarkRenderData).filter_by(
                    parent_id=parent_id
                ).order_by(MarkRenderData.order).all()
            
            # 转换为字典列表
            return [
                {
                    'id': getattr(r, 'id', None),
                    'title': getattr(r, 'title', ''),
                    'content': getattr(r, 'content', ''),
                    'tags': getattr(r, 'tags', ''),
                    'file_path': getattr(r, 'file_path', ''),
                    'theme_id': getattr(r, 'theme_id', 0),
                    'render_style': getattr(r, 'render_style', ''),
                    'page_type': getattr(r, 'page_type', ''),
                    'page_engine': getattr(r, 'page_engine', ''),
                    'updated_at': getattr(r, 'updated_at', None),
                    'created_at': getattr(r, 'created_at', None),
                    # 树形结构字段
                    'parent_id': getattr(r, 'parent_id', None),
                    'order': getattr(r, 'order', 0),
                    'level': getattr(r, 'level', 0),
                    'is_folder': getattr(r, 'is_folder', 0),
                    # 图标和显示字段
                    'icon_type': getattr(r, 'icon_type', None),
                    'icon_path': getattr(r, 'icon_path', None),
                    'icon_color': getattr(r, 'icon_color', None),
                    'display_name': getattr(r, 'display_name', None),
                } for r in records
            ]
        except Exception as e:
            logger.error(f"Error getting children: {e}")
            raise e
        finally:
            session.close()
    
    def move_item(self, item_id, new_parent_id=None):
        """移动节点到新的父节点"""
        session = self.Session()
        try:
            record = session.query(MarkRenderData).filter_by(id=item_id).first()
            if record:
                old_parent_id = getattr(record, 'parent_id', None)
                setattr(record, 'parent_id', new_parent_id)
                
                # 更新层级深度
                if new_parent_id is None:
                    # 移动到根节点
                    setattr(record, 'level', 0)
                else:
                    # 获取新父节点的层级深度
                    parent_record = session.query(MarkRenderData).filter_by(id=new_parent_id).first()
                    if parent_record:
                        new_level = getattr(parent_record, 'level', 0) + 1
                        setattr(record, 'level', new_level)
                
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error moving item: {e}")
            raise e
        finally:
            session.close()
    
    def update_order(self, item_id, new_order):
        """更新节点的排序"""
        session = self.Session()
        try:
            record = session.query(MarkRenderData).filter_by(id=item_id).first()
            if record:
                setattr(record, 'order', new_order)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating order: {e}")
            raise e
        finally:
            session.close()
    
    def get_full_tree(self, parent_id=None):
        """获取完整的树形结构"""
        try:
            def build_tree(parent_id):
                children = self.get_children(parent_id)
                for child in children:
                    child_id = child['id']
                    # 递归获取子节点（所有节点都可能有子节点）
                    child['children'] = build_tree(child_id)
                return children
            
            return build_tree(parent_id)
        except Exception as e:
            logger.error(f"Error getting full tree: {e}")
            raise e
    
    def delete_node(self, item_id, recursive=False):
        """删除节点
        
        Args:
            item_id: 要删除的节点ID
            recursive: 是否递归删除子节点
        """
        session = self.Session()
        try:
            record = session.query(MarkRenderData).filter_by(id=item_id).first()
            if not record:
                return False
                
            if recursive:
                # 递归删除所有子节点
                children = self.get_children(item_id)
                for child in children:
                    self.delete_node(child['id'], recursive=True)
            
            # 删除当前节点
            session.delete(record)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting node: {e}")
            raise e
        finally:
            session.close()
    
    def get_node_path(self, item_id):
        """获取节点的完整路径（从根节点到当前节点）"""
        session = self.Session()
        try:
            path = []
            current_id = item_id
            
            while current_id is not None:
                record = session.query(MarkRenderData).filter_by(id=current_id).first()
                if not record:
                    break
                    
                path.append({
                    'id': getattr(record, 'id', 0),
                    'title': getattr(record, 'title', ''),
                    'is_folder': getattr(record, 'is_folder', 0)
                })
                
                current_id = getattr(record, 'parent_id', None)
            
            # 反转路径，使其从根节点开始
            return list(reversed(path))
        except Exception as e:
            logger.error(f"Error getting node path: {e}")
            raise e
        finally:
            session.close()
    
    def get_subtree(self, item_id):
        """获取指定节点的子树结构"""
        session = self.Session()
        try:
            record = session.query(MarkRenderData).filter_by(id=item_id).first()
            if not record:
                return None
                
            node = {
                'title': getattr(record, 'title', ''),
                'id': getattr(record, 'id', 0),
                'parent_id': getattr(record, 'parent_id', None),
                'order': getattr(record, 'order', 0),
                'level': getattr(record, 'level', 0),
                'is_folder': getattr(record, 'is_folder', 0),
                'page_type': getattr(record, 'page_type', ''),
                'created_at': getattr(record, 'created_at', None),
                'updated_at': getattr(record, 'updated_at', None),
            }
            
            # 获取子节点（所有节点都可能有子节点，不仅仅是is_folder为1的节点）
            children = self.get_children(item_id)
            node['children'] = children
            
            return node
        except Exception as e:
            logger.error(f"Error getting subtree: {e}")
            raise e
        finally:
            session.close()