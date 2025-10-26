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
            
            conn.commit()
        
        print("数据库迁移完成!")
        return True
        
    except Exception as e:
        print(f"数据库迁移失败: {e}")
        return False

if __name__ == "__main__":
    migrate_database()