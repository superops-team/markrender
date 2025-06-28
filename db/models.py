from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func
from .base import Base

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
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    tags = Column(String)
    render_style = Column(String)
    content_md5 = Column(String, nullable=False)

class MarkdownChangeHistory(Base):
    __tablename__ = "markdown_change_history"

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, nullable=False)
    old_content = Column(Text, nullable=False)
    new_content = Column(Text, nullable=False)
    changed_at = Column(DateTime(timezone=True), server_default=func.now())