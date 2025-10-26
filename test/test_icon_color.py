#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试图标颜色功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.markrender_manager import MarkRenderManager

def test_icon_color():
    """测试图标颜色功能"""
    print("测试图标颜色功能...")
    
    # 创建数据库管理器
    manager = MarkRenderManager()
    
    # 创建带图标颜色的文件
    print("\n1. 创建带图标颜色的文件:")
    file_id = manager.create_file(
        title='测试文件-带图标颜色',
        content='# 测试文件\n这是一个带图标颜色的测试文件',
        page_type='markdown',
        icon_path='icons/palette.svg',
        icon_color='#FF5733'  # 橙色
    )
    print(f"   创建文件ID: {file_id}")
    
    # 创建带图标颜色的文件夹
    print("\n2. 创建带图标颜色的文件夹:")
    folder_id = manager.create_folder(
        title='测试文件夹-带图标颜色',
        icon_path='icons/folder.svg',
        icon_color='#33FF57'  # 绿色
    )
    print(f"   创建文件夹ID: {folder_id}")
    
    # 获取文件详情
    print("\n3. 获取文件详情:")
    file_detail = manager.get_detail(file_id)
    print(f"   文件标题: {file_detail['title']}")
    print(f"   图标路径: {file_detail.get('icon_path', 'N/A')}")
    print(f"   图标颜色: {file_detail.get('icon_color', 'N/A')}")
    
    # 获取文件夹详情
    print("\n4. 获取文件夹详情:")
    folder_detail = manager.get_detail(folder_id)
    print(f"   文件夹标题: {folder_detail['title']}")
    print(f"   图标路径: {folder_detail.get('icon_path', 'N/A')}")
    print(f"   图标颜色: {folder_detail.get('icon_color', 'N/A')}")
    
    # 更新文件的图标颜色
    print("\n5. 更新文件的图标颜色:")
    manager.save_item(
        id=file_id,
        icon_color='#3357FF'  # 蓝色
    )
    print("   图标颜色已更新为蓝色")
    
    # 再次获取文件详情，验证更新
    print("\n6. 验证文件图标颜色更新:")
    updated_file_detail = manager.get_detail(file_id)
    print(f"   更新后的图标颜色: {updated_file_detail.get('icon_color', 'N/A')}")
    
    # 获取根节点
    print("\n7. 获取根节点:")
    root_items = manager.get_children(None)
    print(f"   根节点数量: {len(root_items)}")
    for item in root_items:
        print(f"   - {item['title']}: 图标路径={item.get('icon_path', 'N/A')}, 图标颜色={item.get('icon_color', 'N/A')}")
    
    print("\n测试完成!")

if __name__ == "__main__":
    test_icon_color()