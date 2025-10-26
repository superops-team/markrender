from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base
from enum import Enum


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
    
    # 添加与主数据的关系
    markrender_data = relationship("MarkRenderData", back_populates="change_histories")


class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True)
    key = Column(String, nullable=False, unique=True)  # 
    value = Column(Text)  # 配置value, json格式
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 创建时间
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # 更新时间