#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试父子节点关系，确保添加按钮只能添加子节点
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db.markrender_manager import MarkRenderManager

def test_parent_child_relationship():
    """测试父子节点关系"""
    print("开始测试父子节点关系...")
    
    # 创建MarkRenderManager实例
    manager = MarkRenderManager()
    
    # 1. 创建测试用的文件夹层次结构
    print("1. 创建测试用的文件夹层次结构...")
    
    # 创建根文件夹A
    root_a_id = manager.create_folder(
        title="根文件夹A",
        icon_type="folder",
        icon_path="icons/folder.svg"
    )
    print(f"   创建根文件夹A，ID: {root_a_id}")
    
    # 创建根文件夹B
    root_b_id = manager.create_folder(
        title="根文件夹B",
        icon_type="folder",
        icon_path="icons/folder.svg"
    )
    print(f"   创建根文件夹B，ID: {root_b_id}")
    
    # 在根文件夹A下创建子文件夹
    sub_a_id = manager.create_folder(
        title="子文件夹A",
        parent_id=root_a_id,
        icon_type="folder",
        icon_path="icons/folder.svg"
    )
    print(f"   在根文件夹A下创建子文件夹A，ID: {sub_a_id}")
    
    # 在根文件夹B下创建子文件夹
    sub_b_id = manager.create_folder(
        title="子文件夹B",
        parent_id=root_b_id,
        icon_type="folder",
        icon_path="icons/folder.svg"
    )
    print(f"   在根文件夹B下创建子文件夹B，ID: {sub_b_id}")
    
    # 2. 验证父子关系
    print("2. 验证父子关系...")
    
    # 获取根文件夹A的子项
    children_a = manager.get_children(root_a_id)
    print(f"   根文件夹A的子项数量: {len(children_a)}")
    for child in children_a:
        print(f"     子项: {child['title']}, ID: {child['id']}, 父ID: {child['parent_id']}")
        # 验证父ID正确
        assert child['parent_id'] == root_a_id, f"子项 {child['title']} 的父ID不正确"
    
    # 获取根文件夹B的子项
    children_b = manager.get_children(root_b_id)
    print(f"   根文件夹B的子项数量: {len(children_b)}")
    for child in children_b:
        print(f"     子项: {child['title']}, ID: {child['id']}, 父ID: {child['parent_id']}")
        # 验证父ID正确
        assert child['parent_id'] == root_b_id, f"子项 {child['title']} 的父ID不正确"
    
    # 3. 测试在不同父节点下添加子项
    print("3. 测试在不同父节点下添加子项...")
    
    # 在根文件夹A下添加文件
    file_a_id = manager.create_file(
        title="文件A.md",
        content="# 文件A\n\n这是根文件夹A中的文件",
        parent_id=root_a_id,
        page_type="markdown",
        icon_type="textarea",
        icon_path="icons/file-earmark-text.svg"
    )
    print(f"   在根文件夹A下添加文件A，ID: {file_a_id}")
    
    # 在子文件夹A下添加文件
    file_sub_a_id = manager.create_file(
        title="子文件A.md",
        content="# 子文件A\n\n这是子文件夹A中的文件",
        parent_id=sub_a_id,
        page_type="markdown",
        icon_type="textarea",
        icon_path="icons/file-earmark-text.svg"
    )
    print(f"   在子文件夹A下添加子文件A，ID: {file_sub_a_id}")
    
    # 4. 验证添加后的父子关系
    print("4. 验证添加后的父子关系...")
    
    # 验证根文件夹A现在有2个子项
    children_a = manager.get_children(root_a_id)
    print(f"   根文件夹A的子项数量: {len(children_a)}")
    assert len(children_a) == 2, f"根文件夹A应该有2个子项，实际有{len(children_a)}个"
    
    # 验证子文件夹A有1个子项
    children_sub_a = manager.get_children(sub_a_id)
    print(f"   子文件夹A的子项数量: {len(children_sub_a)}")
    assert len(children_sub_a) == 1, f"子文件夹A应该有1个子项，实际有{len(children_sub_a)}个"
    
    # 5. 验证完整的树形结构
    print("5. 验证完整的树形结构...")
    tree = manager.get_full_tree()
    
    # 查找根文件夹A
    root_a = None
    for item in tree:
        if item['id'] == root_a_id:
            root_a = item
            break
    
    if root_a:
        print(f"   根文件夹A: {root_a['title']}")
        print(f"   根文件夹A的子项数量: {len(root_a.get('children', []))}")
        
        # 验证子项
        children = root_a.get('children', [])
        child_titles = [child['title'] for child in children]
        expected_children = ['子文件夹A', '文件A.md']
        for expected in expected_children:
            assert expected in child_titles, f"根文件夹A应该包含子项{expected}"
        
        # 查找子文件夹A并验证其子项
        sub_a = None
        for child in children:
            if child['id'] == sub_a_id:
                sub_a = child
                break
        
        if sub_a:
            print(f"   子文件夹A的子项数量: {len(sub_a.get('children', []))}")
            sub_children = sub_a.get('children', [])
            assert len(sub_children) == 1, f"子文件夹A应该有1个子项，实际有{len(sub_children)}个"
            assert sub_children[0]['title'] == '子文件A.md', f"子文件夹A的子项应该是'子文件A.md'，实际是'{sub_children[0]['title']}'"
    
    print("父子节点关系测试通过!")

if __name__ == "__main__":
    test_parent_child_relationship()