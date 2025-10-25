#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修改后的数据模型功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.markrender_manager import MarkRenderManager

def test_new_features():
    """测试新功能"""
    print("开始测试新功能...")
    
    # 创建MarkRenderManager实例
    manager = MarkRenderManager()
    
    # 创建带图标类型的文件夹
    print("1. 创建带图标类型的文件夹...")
    folder_id = manager.create_folder(
        title="测试文件夹",
        icon_type="folder-icon",
        display_name="我的文件夹"
    )
    print(f"   创建文件夹，ID: {folder_id}")
    
    # 创建带图标类型的文件
    print("2. 创建带图标类型的文件...")
    file_id = manager.create_file(
        title="测试文件.md",
        content="# 测试内容\n\n这是测试文件的内容",
        page_type="markdown",
        icon_type="markdown-icon",
        display_name="我的Markdown文件"
    )
    print(f"   创建文件，ID: {file_id}")
    
    # 更新文件的图标类型和显示名称
    print("3. 更新文件的图标类型和显示名称...")
    manager.save_item(
        id=file_id,
        icon_type="new-markdown-icon",
        display_name="更新后的Markdown文件",
        page_type="markdown"  # 保持内容类型不变
    )
    print("   更新完成")
    
    # 获取树形结构
    print("4. 获取树形结构...")
    tree = manager.get_full_tree()
    print(f"   树形结构: {tree}")
    
    # 验证字段是否正确保存
    print("5. 验证字段保存...")
    children = manager.get_children()
    for child in children:
        print(f"   项目: {child['title']}, 图标类型: {child.get('icon_type')}, 显示名称: {child.get('display_name')}, 内容类型: {child.get('page_type')}")
    
    print("测试完成!")

if __name__ == "__main__":
    test_new_features()