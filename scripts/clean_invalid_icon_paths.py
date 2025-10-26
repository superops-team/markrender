#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理数据库中的无效图标路径
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.markrender_manager import MarkRenderManager

def clean_invalid_icon_paths():
    """清理数据库中的无效图标路径"""
    print("清理数据库中的无效图标路径...")
    
    # 创建数据库管理器
    manager = MarkRenderManager()
    
    # 查找所有带有无效图标路径的记录
    session = manager.Session()
    try:
        from db.models import MarkRenderData
        # 查找icon_path不以icons/开头或者文件不存在的记录
        records = session.query(MarkRenderData).filter(
            MarkRenderData.icon_path.isnot(None)
        ).all()
        
        cleaned_count = 0
        for record in records:
            icon_path = getattr(record, 'icon_path', None)
            # 检查是否为有效的图标路径
            if icon_path and not str(icon_path).startswith('icons/'):
                print(f"  发现无效图标路径: ID {record.id}, 标题: {record.title}, 图路径: {icon_path}")
                # 清理无效的图标路径
                setattr(record, 'icon_path', None)
                cleaned_count += 1
        
        if cleaned_count > 0:
            session.commit()
            print(f"  已清理 {cleaned_count} 条无效图标路径记录")
        else:
            print("  未发现无效图标路径记录")
            
    except Exception as e:
        print(f"清理过程中发生错误: {e}")
        session.rollback()
    finally:
        session.close()
    
    print("清理完成!")

if __name__ == "__main__":
    clean_invalid_icon_paths()