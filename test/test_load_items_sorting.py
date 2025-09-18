#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试 load_items 方法的排序功能
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.markrender_manager import MarkRenderManager
from db.settings_manager import SettingsManager

def test_load_items_sorting():
    """测试 load_items 方法的排序功能"""
    # 创建设置管理器和数据管理器
    settings_manager = SettingsManager()
    data_manager = MarkRenderManager()
    
    # 获取当前排序设置
    current_sort = settings_manager.get_setting('general', 'search_sort', 'updated_time')
    print(f"当前排序设置: {current_sort}")
    
    # 测试不同的排序设置
    sort_options = ['created_time', 'updated_time', 'name']
    
    for sort_option in sort_options:
        print(f"\n=== 测试排序选项: {sort_option} ===")
        
        # 设置排序条件
        settings_manager.set_setting('general', 'search_sort', sort_option)
        
        # 加载数据
        try:
            items = data_manager.load_items(limit=5)  # 限制为5个以便查看
            print(f"加载了 {len(items)} 个项目")
            
            # 显示排序结果
            if sort_option == 'created_time':
                for item in items:
                    print(f"  标题: {item['title']}, 创建时间: {item['created_at']}")
            elif sort_option == 'name':
                for item in items:
                    print(f"  标题: {item['title']}")
            else:  # updated_time
                for item in items:
                    print(f"  标题: {item['title']}, 更新时间: {item['updated_at']}")
        except Exception as e:
            print(f"加载数据时出错: {e}")
    
    # 恢复原始设置
    settings_manager.set_setting('general', 'search_sort', current_sort)
    print(f"\n已恢复原始排序设置: {current_sort}")

if __name__ == "__main__":
    test_load_items_sorting()