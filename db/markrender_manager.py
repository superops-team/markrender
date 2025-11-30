# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_, text
from .models import Base, MarkRenderData, MarkRenderChangeHistory
from db.db_manager import SingletonEngine, get_user_data_dir
from utils.hash_utils import calculate_md5
from utils.logger_utils import logger  # 添加 logger 导入
from utils import time_utils
import json
import sqlite3


class MarkRenderManager:
    def __init__(self, db_path=None):
        if db_path is None:
            self.db_path = SingletonEngine.get_db_path('data.db')
        else:
            self.db_path = db_path
        self.engine = SingletonEngine.get_instance(self.db_path)
        # 先创建所有表（如果不存在）
        Base.metadata.create_all(self.engine)
        # 执行数据库迁移，为现有表添加缺失的字段
        self._migrate_database()
        self.Session = sessionmaker(bind=self.engine)
    
    def _migrate_database(self):
        """数据库迁移，安全地为现有表添加缺失的字段"""
        try:
            # 使用原生SQLite连接来检查和添加字段
            with sqlite3.connect(self.db_path.replace('sqlite:///', '')) as conn:
                cursor = conn.cursor()
                
                # 检查并添加 deleted_at 字段
                cursor.execute("PRAGMA table_info(markrender_data)")
                columns = [col[1] for col in cursor.fetchall()]
                
                if 'deleted_at' not in columns:
                    logger.info("添加缺失的 deleted_at 字段")
                    cursor.execute("ALTER TABLE markrender_data ADD COLUMN deleted_at DATETIME")
                
                if 'is_deleted' not in columns:
                    logger.info("添加缺失的 is_deleted 字段")
                    cursor.execute("ALTER TABLE markrender_data ADD COLUMN is_deleted INTEGER DEFAULT 0")
                
                conn.commit()
                logger.info("数据库迁移完成")
        except Exception as e:
            logger.error(f"数据库迁移失败: {e}")
            # 迁移失败不应该阻止程序运行，继续使用现有结构

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
                    # 安全地执行逻辑删除，处理字段可能不存在的情况
                    try:
                        # 检查字段是否存在
                        if hasattr(history_item, 'is_deleted'):
                            history_item.is_deleted = 1
                        if hasattr(history_item, 'deleted_at'):
                            history_item.deleted_at = time_utils.now()
                        session.commit()
                        logger.info(f"项目 {item_id} 逻辑删除成功")
                        return True
                    except Exception as update_error:
                        logger.error(f"更新删除状态时出错: {update_error}")
                        session.rollback()
                        return False
                return False
        except Exception as e:
            logger.error(f"删除项目失败: {e}")
            return False

    def load_items(self, limit=20, page_type='', include_deleted=False):
        """加载所有历史记录，按设置中的排序条件排列
        
        Args:
            limit: 返回记录的最大数量
            page_type: 页面类型过滤
            include_deleted: 是否包含已删除的记录，默认为False
        """
        from db.settings_manager import SettingsManager
        
        # 获取搜索排序设置，默认按更新时间排序
        settings_manager = SettingsManager()
        sort_setting = settings_manager.get_setting('general', 'search_sort', 'updated_time')
        
        session = self.Session()
        try:
            query = session.query(MarkRenderData)
            # 安全地过滤已删除项，处理字段可能不存在的情况
            if not include_deleted:
                try:
                    # 检查模型是否有is_deleted字段
                    if hasattr(MarkRenderData, 'is_deleted'):
                        query = query.filter_by(is_deleted=0)
                except Exception as filter_error:
                    logger.warning(f"过滤已删除项时出错: {filter_error}，将返回所有记录")
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
            logger.info(f"准备保存项目，ID: {id}, 标题: {title}")
            if id:
                # 更新现有记录
                history = session.query(MarkRenderData).filter_by(id=id).first()
                if history:
                    logger.info(f"找到现有记录，开始更新字段")
                    
                    # 更新字段
                    setattr(history, 'content', content_str)
                    setattr(history, 'content_md5', content_md5)
                    setattr(history, 'updated_at', now)
                    
                    # 更新其他可选字段
                    if title is not None and title != '':
                        logger.info(f"更新标题: '{title}'")
                        setattr(history, 'title', title)
                    elif title is None:
                        logger.info("标题参数为None，保持原有标题不变")
                    if tags is not None and tags != '':
                        logger.info(f"更新标签: {tags}")
                        setattr(history, 'tags', tags)
                    elif tags is None:
                        logger.info("标签参数为None，保持原有标签不变")
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
                    logger.info(f"记录更新完成，ID: {id}")
                else:
                    # 记录不存在，创建新记录
                    logger.info(f"记录不存在，创建新记录")
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
                    session.flush()  # 确保获取到ID
                    id = getattr(new_history, 'id', 0)
                    changed = True
                    session.commit()
            else:
                # 创建新记录
                logger.info(f"创建新记录")
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
                session.flush()  # 确保获取到ID
                id = getattr(new_history, 'id', 0)
                changed = True
                session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Error saving markdown: {e}")
            raise e
        finally:
            session.close()
            if id and content_str and changed:
                self.sync_write_localdisk(id, content_str, page_type, page_engine)
        logger.info(f"保存项目完成，返回ID: {id}")
        return id

    def _save_change_history(self, session, file_id, old_content, new_content, change_type, 
                           change_reason, change_by, change_ip, change_file_path, 
                           change_theme_id, change_page_type, change_page_engine, 
                           change_page_settings, old_values=None, new_values=None):
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
            old_values: 旧字段值字典
            new_values: 新字段值字典
        """
        try:
            logger.info(f"准备保存变更历史记录: file_id={file_id}, change_type={change_type}, change_reason={change_reason}")
            
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
            
            # 创建变更历史记录
            new_change = MarkRenderChangeHistory(
                change_content_md5=change_content_md5,
                change_file_path=change_file_path,
                change_theme_id=change_theme_id,
                change_page_type=change_page_type,
                change_page_engine=change_page_engine,
                change_page_settings=change_page_settings,
                change_page_id=file_id,
                old_content=old_content_str,
                new_content=content_str,
                change_type=change_type,
                change_reason=change_reason,
                change_by=change_by,
                change_ip=change_ip
            )
            
            # 如果提供了字段变更信息，则记录所有字段的变更
            if old_values and new_values:
                logger.info(f"记录字段变更: old_values={old_values}, new_values={new_values}")
                # 标题变更
                if 'title' in old_values or 'title' in new_values:
                    new_change.old_title = old_values.get('title')
                    new_change.new_title = new_values.get('title')
                
                # 标签变更
                if 'tags' in old_values or 'tags' in new_values:
                    new_change.old_tags = old_values.get('tags')
                    new_change.new_tags = new_values.get('tags')
                
                # 渲染样式变更
                if 'render_style' in old_values or 'render_style' in new_values:
                    new_change.old_render_style = old_values.get('render_style')
                    new_change.new_render_style = new_values.get('render_style')
                
                # 转换器变更
                if 'converter' in old_values or 'converter' in new_values:
                    new_change.old_converter = old_values.get('converter')
                    new_change.new_converter = new_values.get('converter')
                
                # 状态变更
                if 'status' in old_values or 'status' in new_values:
                    new_change.old_status = old_values.get('status')
                    new_change.new_status = new_values.get('status')
                
                # 父节点ID变更
                if 'parent_id' in old_values or 'parent_id' in new_values:
                    new_change.old_parent_id = old_values.get('parent_id')
                    new_change.new_parent_id = new_values.get('parent_id')
                
                # 排序变更
                if 'order' in old_values or 'order' in new_values:
                    new_change.old_order = old_values.get('order')
                    new_change.new_order = new_values.get('order')
                
                # 层级变更
                if 'level' in old_values or 'level' in new_values:
                    new_change.old_level = old_values.get('level')
                    new_change.new_level = new_values.get('level')
                
                # 图标类型变更
                if 'icon_type' in old_values or 'icon_type' in new_values:
                    new_change.old_icon_type = old_values.get('icon_type')
                    new_change.new_icon_type = new_values.get('icon_type')
                
                # 图标路径变更
                if 'icon_path' in old_values or 'icon_path' in new_values:
                    new_change.old_icon_path = old_values.get('icon_path')
                    new_change.new_icon_path = new_values.get('icon_path')
                
                # 图标颜色变更
                if 'icon_color' in old_values or 'icon_color' in new_values:
                    new_change.old_icon_color = old_values.get('icon_color')
                    new_change.new_icon_color = new_values.get('icon_color')
                
                # 显示名称变更
                if 'display_name' in old_values or 'display_name' in new_values:
                    new_change.old_display_name = old_values.get('display_name')
                    new_change.new_display_name = new_values.get('display_name')
                
                # 文件夹标识变更
                if 'is_folder' in old_values or 'is_folder' in new_values:
                    new_change.old_is_folder = old_values.get('is_folder')
                    new_change.new_is_folder = new_values.get('is_folder')
            
            session.add(new_change)
            logger.info(f"变更历史记录已添加到session: change_id={new_change.id if new_change.id is not None else '未分配'}")
            # 注意：不在此处commit，由调用方负责commit
            return new_change
        except Exception as e:
            # 注意：不在此处rollback，由调用方负责rollback
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
            suffix = 'md'  # 默认后缀
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
                           change_page_engine='markdown', change_page_settings='{}', change_page_id=None,
                           old_values=None, new_values=None):
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
            old_values: 旧字段值字典
            new_values: 新字段值字典
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
            
            # 创建变更历史记录
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
            
            # 如果提供了字段变更信息，则记录所有字段的变更
            if old_values and new_values:
                # 标题变更
                if 'title' in old_values or 'title' in new_values:
                    new_change.old_title = old_values.get('title')
                    new_change.new_title = new_values.get('title')
                
                # 标签变更
                if 'tags' in old_values or 'tags' in new_values:
                    new_change.old_tags = old_values.get('tags')
                    new_change.new_tags = new_values.get('tags')
                
                # 渲染样式变更
                if 'render_style' in old_values or 'render_style' in new_values:
                    new_change.old_render_style = old_values.get('render_style')
                    new_change.new_render_style = new_values.get('render_style')
                
                # 转换器变更
                if 'converter' in old_values or 'converter' in new_values:
                    new_change.old_converter = old_values.get('converter')
                    new_change.new_converter = new_values.get('converter')
                
                # 状态变更
                if 'status' in old_values or 'status' in new_values:
                    new_change.old_status = old_values.get('status')
                    new_change.new_status = new_values.get('status')
                
                # 父节点ID变更
                if 'parent_id' in old_values or 'parent_id' in new_values:
                    new_change.old_parent_id = old_values.get('parent_id')
                    new_change.new_parent_id = new_values.get('parent_id')
                
                # 排序变更
                if 'order' in old_values or 'order' in new_values:
                    new_change.old_order = old_values.get('order')
                    new_change.new_order = new_values.get('order')
                
                # 层级变更
                if 'level' in old_values or 'level' in new_values:
                    new_change.old_level = old_values.get('level')
                    new_change.new_level = new_values.get('level')
                
                # 图标类型变更
                if 'icon_type' in old_values or 'icon_type' in new_values:
                    new_change.old_icon_type = old_values.get('icon_type')
                    new_change.new_icon_type = new_values.get('icon_type')
                
                # 图标路径变更
                if 'icon_path' in old_values or 'icon_path' in new_values:
                    new_change.old_icon_path = old_values.get('icon_path')
                    new_change.new_icon_path = new_values.get('icon_path')
                
                # 图标颜色变更
                if 'icon_color' in old_values or 'icon_color' in new_values:
                    new_change.old_icon_color = old_values.get('icon_color')
                    new_change.new_icon_color = new_values.get('icon_color')
                
                # 显示名称变更
                if 'display_name' in old_values or 'display_name' in new_values:
                    new_change.old_display_name = old_values.get('display_name')
                    new_change.new_display_name = new_values.get('display_name')
                
                # 文件夹标识变更
                if 'is_folder' in old_values or 'is_folder' in new_values:
                    new_change.old_is_folder = old_values.get('is_folder')
                    new_change.new_is_folder = new_values.get('is_folder')
            
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
                change_page_id=file_id).order_by(MarkRenderChangeHistory.change_at.desc()).limit(20).all()
        except Exception as e:
            logger.error(f"Error getting change history: {e}")
            raise e
        finally:
            session.close()
    
    def get_detail(self, id, include_deleted=False):
        """获取详情
        
        Args:
            id: 记录ID
            include_deleted: 是否包含已删除的记录，默认为False
        """
        session = self.Session()
        try:
            # 安全地查询记录，处理is_deleted字段可能不存在的情况
            record = session.query(MarkRenderData).filter_by(id=id).first()
            
            # 如果记录存在且不包含已删除记录，则检查is_deleted状态
            if record and not include_deleted:
                try:
                    # 只有当is_deleted字段存在且值不为0时才过滤
                    if hasattr(record, 'is_deleted') and getattr(record, 'is_deleted', 0) != 0:
                        record = None
                except Exception as e:
                    logger.warning(f"检查记录删除状态时出错: {e}")
                    # 出错时不过滤，返回记录
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
                'deleted_at': getattr(record, 'deleted_at', None),
                'is_deleted': getattr(record, 'is_deleted', 0),
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
                # 保存旧标题用于历史记录
                old_title = getattr(record, 'title', '')
                if old_title != title:
                    setattr(record, 'title', title)
                    logger.info(f"更新标题: {old_title} -> {title}")
                    
                    # 记录标题变更历史
                    old_values = {'title': old_title}
                    new_values = {'title': title}
                    logger.info(f"准备记录标题变更历史: old_values={old_values}, new_values={new_values}")
                    self._save_change_history(
                        session, id, 
                        getattr(record, 'content', ''), 
                        getattr(record, 'content', ''),
                        'title_update',
                        'user_edit', 
                        'user', 
                        '127.0.0.1', 
                        getattr(record, 'file_path', '') or '',
                        getattr(record, 'theme_id', 0) or 0, 
                        getattr(record, 'page_type', '') or '', 
                        getattr(record, 'page_engine', '') or '', 
                        getattr(record, 'page_settings', '') or '',
                        old_values,
                        new_values
                    )
                    logger.info("标题变更历史记录已保存")
                    
                    session.commit()
                    logger.info("标题更新已提交")
            else:
                raise ValueError(f"未找到 ID 为 {id} 的记录")
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating title: {e}")
            raise e
        finally:
            session.close()
    
    def update_icon(self, id, icon_type=None, icon_path=None, icon_color=None):
        """更新图标信息"""
        if not id:
            return
        session = self.Session()
        try:
            record = session.query(MarkRenderData).filter_by(id=id).first()
            if record:
                old_values = {}
                new_values = {}
                changed = False
                
                # 更新图标类型
                if icon_type is not None:
                    old_icon_type = getattr(record, 'icon_type', None)
                    if old_icon_type != icon_type:
                        old_values['icon_type'] = old_icon_type
                        new_values['icon_type'] = icon_type
                        setattr(record, 'icon_type', icon_type)
                        changed = True
                
                # 更新图标路径
                if icon_path is not None:
                    old_icon_path = getattr(record, 'icon_path', None)
                    if old_icon_path != icon_path:
                        old_values['icon_path'] = old_icon_path
                        new_values['icon_path'] = icon_path
                        setattr(record, 'icon_path', icon_path)
                        changed = True
                
                # 更新图标颜色
                if icon_color is not None:
                    old_icon_color = getattr(record, 'icon_color', None)
                    if old_icon_color != icon_color:
                        old_values['icon_color'] = old_icon_color
                        new_values['icon_color'] = icon_color
                        setattr(record, 'icon_color', icon_color)
                        changed = True
                
                # 只有在有变更时才提交和记录历史
                if changed:
                    # 记录图标变更历史
                    self._save_change_history(
                        session, id, 
                        getattr(record, 'content', ''), 
                        getattr(record, 'content', ''),
                        'icon_update',
                        'user_edit', 
                        'user', 
                        '127.0.0.1', 
                        getattr(record, 'file_path', '') or '',
                        getattr(record, 'theme_id', 0) or 0, 
                        getattr(record, 'page_type', '') or '', 
                        getattr(record, 'page_engine', '') or '', 
                        getattr(record, 'page_settings', '') or '',
                        old_values,
                        new_values
                    )
                    
                    session.commit()
            else:
                raise ValueError(f"未找到 ID 为 {id} 的记录")
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating icon: {e}")
            raise e
        finally:
            session.close()
    
    def update_display_name(self, id, display_name):
        """更新显示名称"""
        if not id:
            return
        session = self.Session()
        try:
            record = session.query(MarkRenderData).filter_by(id=id).first()
            if record:
                old_display_name = getattr(record, 'display_name', None)
                if old_display_name != display_name:
                    setattr(record, 'display_name', display_name)
                    
                    # 记录显示名称变更历史
                    old_values = {'display_name': old_display_name}
                    new_values = {'display_name': display_name}
                    self._save_change_history(
                        session, id, 
                        getattr(record, 'content', ''), 
                        getattr(record, 'content', ''),
                        'display_name_update',
                        'user_edit', 
                        'user', 
                        '127.0.0.1', 
                        getattr(record, 'file_path', '') or '',
                        getattr(record, 'theme_id', 0) or 0, 
                        getattr(record, 'page_type', '') or '', 
                        getattr(record, 'page_engine', '') or '', 
                        getattr(record, 'page_settings', '') or '',
                        old_values,
                        new_values
                    )
                    
                    session.commit()
            else:
                raise ValueError(f"未找到 ID 为 {id} 的记录")
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating display name: {e}")
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
            
    def get_children(self, parent_id=None, include_deleted=False):
        """获取指定父节点的所有子节点
        
        Args:
            parent_id: 父节点ID，为None时获取顶级节点
            include_deleted: 是否包含已删除的记录，默认为False
        """
        session = self.Session()
        try:
            # 构建查询
            query = session.query(MarkRenderData)
            # 安全地过滤已删除项，处理字段可能不存在的情况
            if not include_deleted:
                try:
                    if hasattr(MarkRenderData, 'is_deleted'):
                        query = query.filter_by(is_deleted=0)
                except Exception as filter_error:
                    logger.warning(f"过滤已删除项时出错: {filter_error}")
                
            if parent_id is None:
                # 获取根节点（parent_id为None或空的记录）
                records = query.filter(
                    or_(MarkRenderData.parent_id == None, MarkRenderData.parent_id == '')
                ).order_by(MarkRenderData.created_at.desc()).all()  # 按创建时间倒序排列（最新的在前）
            else:
                # 获取指定父节点的子节点
                records = query.filter_by(
                    parent_id=parent_id
                ).order_by(MarkRenderData.created_at.desc()).all()  # 按创建时间倒序排列（最新的在前）
            
            # 转换为字典列表
            results = []
            for r in records:
                try:
                    # 安全地构建返回字典
                    item_dict = {
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
                    }
                    
                    # 安全地添加可能不存在的字段
                    try:
                        if hasattr(r, 'deleted_at'):
                            item_dict['deleted_at'] = getattr(r, 'deleted_at', None)
                        else:
                            item_dict['deleted_at'] = None
                        
                        if hasattr(r, 'is_deleted'):
                            item_dict['is_deleted'] = getattr(r, 'is_deleted', 0)
                        else:
                            item_dict['is_deleted'] = 0
                    except Exception as field_error:
                        logger.warning(f"添加字段时出错: {field_error}")
                    
                    results.append(item_dict)
                except Exception as item_error:
                    logger.error(f"处理记录时出错: {item_error}")
                    # 继续处理其他记录
                    continue
            
            return results
        except Exception as e:
            logger.error(f"Error getting children: {e}")
            raise e
        finally:
            session.close()
    
    def move_item(self, item_id, new_parent_id=None):
        """移动节点到新的父节点"""
        # 防止节点移动到自身
        if item_id == new_parent_id:
            return True
        
        session = self.Session()
        try:
            record = session.query(MarkRenderData).filter_by(id=item_id).first()
            if record:
                # 更新层级深度
                if new_parent_id is None:
                    # 移动到根节点
                    setattr(record, 'parent_id', None)
                    setattr(record, 'level', 0)
                    # 更新所有子节点的层级
                    self._update_children_levels(session, item_id, 0)
                else:
                    # 获取新父节点的层级深度
                    parent_record = session.query(MarkRenderData).filter_by(id=new_parent_id).first()
                    if parent_record:
                        setattr(record, 'parent_id', new_parent_id)
                        new_level = getattr(parent_record, 'level', 0) + 1
                        setattr(record, 'level', new_level)
                        # 更新所有子节点的层级
                        self._update_children_levels(session, item_id, new_level)
                    else:
                        # 父节点不存在，将节点移动到根节点
                        setattr(record, 'parent_id', None)
                        setattr(record, 'level', 0)
                        # 更新所有子节点的层级
                        self._update_children_levels(session, item_id, 0)
                
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error moving item: {e}")
            raise e
        finally:
            session.close()
    
    def _update_children_levels(self, session, parent_id, parent_level, visited=None):
        """递归更新子节点的层级深度"""
        if visited is None:
            visited = set()
        
        # 防止循环引用导致的无限递归
        if parent_id in visited:
            return
        
        visited.add(parent_id)
        
        # 获取所有直接子节点
        children = session.query(MarkRenderData).filter_by(parent_id=parent_id).all()
        for child in children:
            new_level = parent_level + 1
            logger.info(f"更新子节点 {child.id} 的层级从 {getattr(child, 'level', 'unknown')} 到 {new_level}")
            setattr(child, 'level', new_level)
            # 递归更新子节点的子节点
            self._update_children_levels(session, child.id, new_level, visited)
    
    def update_item_level(self, item_id, new_level):
        """更新节点的层级深度"""
        session = self.Session()
        try:
            record = session.query(MarkRenderData).filter_by(id=item_id).first()
            if record:
                setattr(record, 'level', new_level)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating item level: {e}")
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
        """删除节点（逻辑删除）
        
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
                # 递归逻辑删除所有子节点
                children = self.get_children(item_id)
                for child in children:
                    self.delete_node(child['id'], recursive=True)
            
            # 安全地执行逻辑删除，处理字段可能不存在的情况
            try:
                if hasattr(record, 'is_deleted'):
                    record.is_deleted = 1
                if hasattr(record, 'deleted_at'):
                    record.deleted_at = time_utils.now()
                session.commit()
                logger.info(f"节点 {item_id} 逻辑删除成功")
                return True
            except Exception as update_error:
                logger.error(f"更新节点删除状态时出错: {update_error}")
                session.rollback()
                return False
        except Exception as e:
            session.rollback()
            logger.error(f"删除节点失败: {e}")
            # 返回False而不是抛出异常，避免中断程序
            return False
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
                
            # 安全地构建节点信息，处理字段可能不存在的情况
            node = {}
            try:
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
            except Exception as field_error:
                logger.warning(f"构建节点信息时出错: {field_error}")
                # 使用基本的安全信息
                node = {
                    'title': getattr(record, 'title', 'Unknown Title'),
                    'id': getattr(record, 'id', 0),
                }
            
            # 获取子节点（所有节点都可能有子节点，不仅仅是is_folder为1的节点）
            try:
                children = self.get_children(item_id)
                node['children'] = children
            except Exception as children_error:
                logger.error(f"获取子节点时出错: {children_error}")
                node['children'] = []
            
            return node
        except Exception as e:
            logger.error(f"获取子树结构失败: {e}")
            # 返回None而不是抛出异常，避免中断程序
            return None
        finally:
            session.close()