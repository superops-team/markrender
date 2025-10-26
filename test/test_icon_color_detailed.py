#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细测试图标颜色功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.markrender_manager import MarkRenderManager

def test_icon_color_detailed():
    """详细测试图标颜色功能"""
    print("详细测试图标颜色功能...")
    
    # 创建数据库管理器
    manager = MarkRenderManager()
    
    # 创建带图标颜色的文件
    print("\n1. 创建带图标颜色的文件:")
    file_id = manager.create_file(
        title='详细测试文件-带图标颜色',
        content='# 详细测试文件\n这是一个带图标颜色的详细测试文件',
        page_type='markdown',
        icon_path='icons/palette.svg',
        icon_color='#FF5733'  # 橙色
    )
    print(f"   创建文件ID: {file_id}")
    
    # 立即获取文件详情，检查创建时的图标颜色
    print("\n2. 检查创建时的图标颜色:")
    file_detail = manager.get_detail(file_id)
    print(f"   文件标题: {file_detail['title']}")
    print(f"   图标路径: {file_detail.get('icon_path', 'N/A')}")
    print(f"   图标颜色: {file_detail.get('icon_color', 'N/A')}")
    
    # 更新文件的图标颜色
    print("\n3. 更新文件的图标颜色:")
    manager.save_item(
        id=file_id,
        icon_color='#3357FF'  # 蓝色
    )
    print("   图标颜色已更新为蓝色")
    
    # 再次获取文件详情，验证更新
    print("\n4. 验证文件图标颜色更新:")
    updated_file_detail = manager.get_detail(file_id)
    print(f"   更新后的图标颜色: {updated_file_detail.get('icon_color', 'N/A')}")
    
    print("\n测试完成!")

if __name__ == "__main__":
    test_icon_color_detailed()