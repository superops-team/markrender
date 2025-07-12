from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func
from .base import Base
from enum import Enum


class Theme(Base):
    __tablename__ = "themes"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    css_config = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class MarkdownFileHistory(Base):
    __tablename__ = "markdown_file_history"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)  # 标题
    content = Column(Text)  # 内容
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 创建时间
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # 更新时间
    tags = Column(String)  # 标签
    render_style = Column(String)  # 渲染样式
    content_md5 = Column(String)  # 内容md5
    file_path = Column(String)  # 文件路径
    theme_id = Column(Integer)  # 主题id
    converter = Column(String)  # 渲染器
    converter_start = Column(DateTime(timezone=True), server_default=func.now())  # 转换开始时间
    converter_end = Column(DateTime(timezone=True), server_default=func.now())  # 转换结束时间

    status = Column(String)  # 渲染状态


class MarkdownChangeHistory(Base):
    __tablename__ = "markdown_change_history"

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, nullable=False)  # 文件id
    old_content = Column(Text, nullable=False)  # 旧内容
    new_content = Column(Text, nullable=False)  # 新内容
    changed_at = Column(DateTime(timezone=True), server_default=func.now())  # 变更时间


class MarkdownConverterSettings(Base):
    __tablename__ = "markdown_converter_settings"

    id = Column(Integer, primary_key=True)
    converter = Column(String, nullable=False)  # 渲染器
    settings = Column(String, nullable=False)  # 配置, json fmt


class Status(Enum):
    PROCESSING = 'processing'
    COMPLETED = 'completed'