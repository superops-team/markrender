#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
验证搜索设置功能
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.settings_manager import SettingsManager

def verify_search_settings():
    """验证搜索设置功能"""
    # 创建设置管理器
    settings_manager = SettingsManager()
    
    # 获取当前的通用设置
    general_settings = settings_manager.get_settings_dict('general')
    print("当前通用设置:", general_settings)
    
    # 检查是否存在搜索排序设置
    if 'search_sort' in general_settings:
        print(f"搜索排序设置: {general_settings['search_sort']}")
    else:
        print("未找到搜索排序设置，默认值将为 'name'")
    
    # 模拟设置搜索排序为按创建时间
    general_settings['search_sort'] = 'created_time'
    settings_manager.create_settings('general', general_settings)
    
    # 再次获取并验证
    updated_settings = settings_manager.get_settings_dict('general')
    print("更新后的通用设置:", updated_settings)
    print(f"搜索排序设置: {updated_settings.get('search_sort', 'name')}")

if __name__ == "__main__":
    verify_search_settings()