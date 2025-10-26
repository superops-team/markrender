#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试图标路径修复功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.markrender_manager import MarkRenderManager

def test_icon_path_fix():
    """测试图标路径修复功能"""
    print("测试图标路径修复功能...")
    
    # 创建数据库管理器
    manager = MarkRenderManager()
    
    # 创建一个带自定义图标的文件
    print("\n1. 创建带自定义图标的文件:")
    file_id = manager.create_file(
        title='图标路径测试文件',
        content='# 图标路径测试\n这是一个测试图标路径修复功能的文件',
        page_type='markdown',
        icon_path='icons/palette.svg',  # 使用相对路径
        icon_color='#FF5733'  # 橙色
    )
    print(f"   创建文件ID: {file_id}")
    
    # 获取文件详情
    print("\n2. 获取文件详情:")
    file_detail = manager.get_detail(file_id)
    print(f"   文件标题: {file_detail['title']}")
    print(f"   图标路径: {file_detail.get('icon_path', 'N/A')}")
    print(f"   图标颜色: {file_detail.get('icon_color', 'N/A')}")
    
    # 检查图标文件是否存在
    icon_path = file_detail.get('icon_path')
    if icon_path:
        # 直接使用相对路径检查文件是否存在
        print(f"   图标文件路径: {icon_path}")
        if os.path.exists(icon_path):
            print("   ✅ 图标文件存在")
        else:
            print("   ❌ 图标文件不存在")
    
    print("\n测试完成!")

if __name__ == "__main__":
    test_icon_path_fix()