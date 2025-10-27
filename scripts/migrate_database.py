#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库迁移脚本，用于添加新的字段
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from db.db_manager import SingletonEngine

def migrate_database():
    """迁移数据库以添加新的字段"""
    print("开始数据库迁移...")
    
    # 获取数据库路径
    db_path = SingletonEngine.get_db_path('data.db')
    print(f"数据库路径: {db_path}")
    
    # 创建数据库引擎
    engine = create_engine(f"sqlite:///{db_path}")
    
    # 添加新的字段
    try:
        with engine.connect() as conn:
            # 添加icon_type字段
            try:
                conn.execute(text("ALTER TABLE markrender_data ADD COLUMN icon_type VARCHAR"))
                print("添加icon_type字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("icon_type字段已存在")
                else:
                    print(f"添加icon_type字段时出错: {e}")
            
            # 添加icon_path字段
            try:
                conn.execute(text("ALTER TABLE markrender_data ADD COLUMN icon_path VARCHAR"))
                print("添加icon_path字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("icon_path字段已存在")
                else:
                    print(f"添加icon_path字段时出错: {e}")
            
            # 添加icon_color字段
            try:
                conn.execute(text("ALTER TABLE markrender_data ADD COLUMN icon_color VARCHAR"))
                print("添加icon_color字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("icon_color字段已存在")
                else:
                    print(f"添加icon_color字段时出错: {e}")
            
            # 添加display_name字段
            try:
                conn.execute(text("ALTER TABLE markrender_data ADD COLUMN display_name VARCHAR"))
                print("添加display_name字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("display_name字段已存在")
                else:
                    print(f"添加display_name字段时出错: {e}")
            
            # 为markrender_change_history表添加新字段
            # 标题字段
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN old_title VARCHAR"))
                print("添加old_title字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("old_title字段已存在")
                else:
                    print(f"添加old_title字段时出错: {e}")
            
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN new_title VARCHAR"))
                print("添加new_title字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("new_title字段已存在")
                else:
                    print(f"添加new_title字段时出错: {e}")
            
            # 标签字段
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN old_tags VARCHAR"))
                print("添加old_tags字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("old_tags字段已存在")
                else:
                    print(f"添加old_tags字段时出错: {e}")
            
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN new_tags VARCHAR"))
                print("添加new_tags字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("new_tags字段已存在")
                else:
                    print(f"添加new_tags字段时出错: {e}")
            
            # 渲染样式字段
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN old_render_style VARCHAR"))
                print("添加old_render_style字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("old_render_style字段已存在")
                else:
                    print(f"添加old_render_style字段时出错: {e}")
            
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN new_render_style VARCHAR"))
                print("添加new_render_style字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("new_render_style字段已存在")
                else:
                    print(f"添加new_render_style字段时出错: {e}")
            
            # 转换器字段
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN old_converter VARCHAR"))
                print("添加old_converter字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("old_converter字段已存在")
                else:
                    print(f"添加old_converter字段时出错: {e}")
            
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN new_converter VARCHAR"))
                print("添加new_converter字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("new_converter字段已存在")
                else:
                    print(f"添加new_converter字段时出错: {e}")
            
            # 状态字段
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN old_status VARCHAR"))
                print("添加old_status字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("old_status字段已存在")
                else:
                    print(f"添加old_status字段时出错: {e}")
            
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN new_status VARCHAR"))
                print("添加new_status字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("new_status字段已存在")
                else:
                    print(f"添加new_status字段时出错: {e}")
            
            # 父节点ID字段
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN old_parent_id INTEGER"))
                print("添加old_parent_id字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("old_parent_id字段已存在")
                else:
                    print(f"添加old_parent_id字段时出错: {e}")
            
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN new_parent_id INTEGER"))
                print("添加new_parent_id字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("new_parent_id字段已存在")
                else:
                    print(f"添加new_parent_id字段时出错: {e}")
            
            # 排序字段
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN old_order INTEGER"))
                print("添加old_order字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("old_order字段已存在")
                else:
                    print(f"添加old_order字段时出错: {e}")
            
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN new_order INTEGER"))
                print("添加new_order字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("new_order字段已存在")
                else:
                    print(f"添加new_order字段时出错: {e}")
            
            # 层级字段
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN old_level INTEGER"))
                print("添加old_level字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("old_level字段已存在")
                else:
                    print(f"添加old_level字段时出错: {e}")
            
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN new_level INTEGER"))
                print("添加new_level字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("new_level字段已存在")
                else:
                    print(f"添加new_level字段时出错: {e}")
            
            # 图标类型字段
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN old_icon_type VARCHAR"))
                print("添加old_icon_type字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("old_icon_type字段已存在")
                else:
                    print(f"添加old_icon_type字段时出错: {e}")
            
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN new_icon_type VARCHAR"))
                print("添加new_icon_type字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("new_icon_type字段已存在")
                else:
                    print(f"添加new_icon_type字段时出错: {e}")
            
            # 图标路径字段
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN old_icon_path VARCHAR"))
                print("添加old_icon_path字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("old_icon_path字段已存在")
                else:
                    print(f"添加old_icon_path字段时出错: {e}")
            
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN new_icon_path VARCHAR"))
                print("添加new_icon_path字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("new_icon_path字段已存在")
                else:
                    print(f"添加new_icon_path字段时出错: {e}")
            
            # 图标颜色字段
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN old_icon_color VARCHAR"))
                print("添加old_icon_color字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("old_icon_color字段已存在")
                else:
                    print(f"添加old_icon_color字段时出错: {e}")
            
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN new_icon_color VARCHAR"))
                print("添加new_icon_color字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("new_icon_color字段已存在")
                else:
                    print(f"添加new_icon_color字段时出错: {e}")
            
            # 显示名称字段
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN old_display_name VARCHAR"))
                print("添加old_display_name字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("old_display_name字段已存在")
                else:
                    print(f"添加old_display_name字段时出错: {e}")
            
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN new_display_name VARCHAR"))
                print("添加new_display_name字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("new_display_name字段已存在")
                else:
                    print(f"添加new_display_name字段时出错: {e}")
            
            # 文件夹标识字段
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN old_is_folder INTEGER"))
                print("添加old_is_folder字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("old_is_folder字段已存在")
                else:
                    print(f"添加old_is_folder字段时出错: {e}")
            
            try:
                conn.execute(text("ALTER TABLE markrender_change_history ADD COLUMN new_is_folder INTEGER"))
                print("添加new_is_folder字段成功")
            except Exception as e:
                if "duplicate column name" in str(e).lower():
                    print("new_is_folder字段已存在")
                else:
                    print(f"添加new_is_folder字段时出错: {e}")
            
            conn.commit()
        
        print("数据库迁移完成!")
        return True
        
    except Exception as e:
        print(f"数据库迁移失败: {e}")
        return False

if __name__ == "__main__":
    migrate_database()