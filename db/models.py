from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base
from enum import Enum
from sqlalchemy import event
from utils.hash_utils import calculate_md5
from utils import time_utils
import json


class Theme(Base):
    __tablename__ = "themes"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    css_config = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class MarkRenderData(Base):
    __tablename__ = "markrender_data"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)  # 标题
    content = Column(Text)  # 内容
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 创建时间
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # 更新时间
    tags = Column(String)  # 标签
    render_style = Column(String)  # 渲染样式
    content_md5 = Column(String)  # 内容md5
    file_path = Column(String, nullable=True)  # 文件路径
    theme_id = Column(Integer)  # 主题id
    converter = Column(String)  # 渲染器
    page_type = Column(String, nullable=True)  # 页面内容类型，如markdown、excalidraw等，仅表示内容格式
    converter_start = Column(DateTime(timezone=True), server_default=func.now())  # 转换开始时间
    converter_end = Column(DateTime(timezone=True), server_default=func.now())  # 转换结束时间
    page_settings = Column(Text)  # 页面定制化配置，JSON格式
    page_engine = Column(String)  # 页面核心处理引擎，如cherry-markdown、excalidraw等

    status = Column(String)  # 渲染状态
    
    # 树形结构字段
    parent_id = Column(Integer, ForeignKey('markrender_data.id'), nullable=True)  # 父节点ID
    order = Column(Integer, default=0)  # 同级排序
    level = Column(Integer, default=0)  # 层级深度
    # 图标和显示相关字段
    icon_type = Column(String, nullable=True)  # 图标类型，用于区分显示图标
    icon_path = Column(String, nullable=True)  # 图标路径，支持自定义图标
    icon_color = Column(String, nullable=True)  # 图标颜色，支持自定义图标颜色
    display_name = Column(String, nullable=True)  # 显示名称，可与title不同
    is_folder = Column(Integer, default=0)  # 是否为文件夹，0表示文件，1表示文件夹
    
    # 自引用关系
    children = relationship("MarkRenderData", backref="parent", remote_side=[id])
    
    # 添加与历史记录的关系
    change_histories = relationship("MarkRenderChangeHistory", back_populates="markrender_data")


class MarkRenderChangeHistory(Base):
    __tablename__ = "markrender_change_history"

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('markrender_data.id'), nullable=True)  # 文件id，外键关联
    old_content = Column(Text, nullable=True)  # 旧内容
    new_content = Column(Text, nullable=True)  # 新内容
    change_type = Column(String, nullable=True)  # 变更类型
    change_reason = Column(String, nullable=True)  # 变更原因
    change_by = Column(String, nullable=True)  # 变更人
    change_at = Column(DateTime(timezone=True), server_default=func.now())  # 变更时间
    change_ip = Column(String, nullable=True)  # 变更ip
    change_content_md5 = Column(String, nullable=True)  # 变更内容md5
    change_file_path = Column(String, nullable=True)  # 变更文件路径
    change_theme_id = Column(Integer, nullable=True)  # 变更主题id
    change_page_type = Column(String, nullable=True)  # 变更页面类型
    change_page_engine = Column(String, nullable=True)  # 变更页面引擎
    change_page_settings = Column(Text, nullable=True)  # 变更页面定制化配置，JSON格式
    change_page_id = Column(Integer, nullable=True)  # 变更页面id
    
    # 新增：记录所有字段的变更历史
    old_title = Column(String, nullable=True)  # 旧标题
    new_title = Column(String, nullable=True)  # 新标题
    old_tags = Column(String, nullable=True)  # 旧标签
    new_tags = Column(String, nullable=True)  # 新标签
    old_render_style = Column(String, nullable=True)  # 旧渲染样式
    new_render_style = Column(String, nullable=True)  # 新渲染样式
    old_converter = Column(String, nullable=True)  # 旧转换器
    new_converter = Column(String, nullable=True)  # 新转换器
    old_status = Column(String, nullable=True)  # 旧状态
    new_status = Column(String, nullable=True)  # 新状态
    old_parent_id = Column(Integer, nullable=True)  # 旧父节点ID
    new_parent_id = Column(Integer, nullable=True)  # 新父节点ID
    old_order = Column(Integer, nullable=True)  # 旧排序
    new_order = Column(Integer, nullable=True)  # 新排序
    old_level = Column(Integer, nullable=True)  # 旧层级
    new_level = Column(Integer, nullable=True)  # 新层级
    old_icon_type = Column(String, nullable=True)  # 旧图标类型
    new_icon_type = Column(String, nullable=True)  # 新图标类型
    old_icon_path = Column(String, nullable=True)  # 旧图标路径
    new_icon_path = Column(String, nullable=True)  # 新图标路径
    old_icon_color = Column(String, nullable=True)  # 旧图标颜色
    new_icon_color = Column(String, nullable=True)  # 新图标颜色
    old_display_name = Column(String, nullable=True)  # 旧显示名称
    new_display_name = Column(String, nullable=True)  # 新显示名称
    old_is_folder = Column(Integer, nullable=True)  # 旧文件夹标识
    new_is_folder = Column(Integer, nullable=True)  # 新文件夹标识
    
    # 添加与主数据的关系
    markrender_data = relationship("MarkRenderData", back_populates="change_histories")


class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=False, unique=True)  # 
    value = Column(Text)  # 配置value, json格式
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 创建时间
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # 更新时间


# 添加ORM事件监听器，自动创建历史记录
@event.listens_for(MarkRenderData, 'before_update')
def before_update_listener(mapper, connection, target):
    """在更新MarkRenderData记录之前，创建历史记录"""
    # 获取旧记录的值
    old_record = connection.execute(
        mapper.local_table.select().where(mapper.local_table.c.id == target.id)
    ).fetchone()
    
    if old_record:
        # 创建变更历史记录
        change_type = 'content_update'
        change_reason = 'auto_save'
        change_by = 'system'
        change_ip = '127.0.0.1'
        
        # 检查内容是否发生变化
        old_content = old_record.content or ''
        new_content = target.content or ''
        
        # 特别检查空白字符差异
        old_stripped = old_content.strip()
        new_stripped = new_content.strip()
        content_changed = (old_content != new_content) or (old_stripped != new_stripped)
        
        # 如果内容发生变化，创建历史记录
        if content_changed:
            # 计算新内容的MD5
            content_md5 = calculate_md5(new_content)
            
            # 构造历史记录数据
            history_data = {
                'file_id': target.id,
                'old_content': old_content,
                'new_content': new_content,
                'change_type': change_type,
                'change_reason': change_reason,
                'change_by': change_by,
                'change_ip': change_ip,
                'change_content_md5': content_md5,
                'change_file_path': target.file_path or '',
                'change_theme_id': target.theme_id or 0,
                'change_page_type': target.page_type or '',
                'change_page_engine': target.page_engine or '',
                'change_page_settings': target.page_settings or '',
                'change_page_id': target.id
            }
            
            # 插入历史记录
            connection.execute(
                MarkRenderChangeHistory.__table__.insert().values(**history_data)
            )


@event.listens_for(MarkRenderData, 'after_insert')
def after_insert_listener(mapper, connection, target):
    """在插入MarkRenderData记录之后，创建历史记录"""
    # 创建变更历史记录
    change_type = 'content_create'
    change_reason = 'auto_save'
    change_by = 'system'
    change_ip = '127.0.0.1'
    
    # 获取新内容
    new_content = target.content or ''
    
    # 计算新内容的MD5
    content_md5 = calculate_md5(new_content)
    
    # 构造历史记录数据
    history_data = {
        'file_id': target.id,
        'old_content': '',  # 新创建的记录没有旧内容
        'new_content': new_content,
        'change_type': change_type,
        'change_reason': change_reason,
        'change_by': change_by,
        'change_ip': change_ip,
        'change_content_md5': content_md5,
        'change_file_path': target.file_path or '',
        'change_theme_id': target.theme_id or 0,
        'change_page_type': target.page_type or '',
        'change_page_engine': target.page_engine or '',
        'change_page_settings': target.page_settings or '',
        'change_page_id': target.id
    }
    
    # 插入历史记录
    connection.execute(
        MarkRenderChangeHistory.__table__.insert().values(**history_data)
    )