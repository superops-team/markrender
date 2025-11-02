#!/usr/bin/env python3
"""
测试标签页功能的脚本
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app.editor.tab_manager import TabManager

def test_find_tab_by_item_id():
    """测试根据项目ID查找标签页的功能"""
    print("测试 find_tab_by_item_id 功能...")
    
    # 创建一个模拟的编辑器对象
    class MockEditor:
        def __init__(self, item_id):
            self.item = type('obj', (object,), {'item_id': item_id})()
    
    # 创建标签页管理器
    tab_manager = TabManager()
    
    # 添加一些模拟的编辑器
    tab_manager.editors[0] = MockEditor('item-1')
    tab_manager.editors[1] = MockEditor('item-2')
    tab_manager.editors[2] = MockEditor('item-3')
    
    # 测试查找存在的项目
    index = tab_manager.find_tab_by_item_id('item-2')
    if index == 1:
        print("✓ 正确：找到了item-2，索引为1")
    else:
        print(f"✗ 错误：查找item-2失败，返回索引{index}")
    
    # 测试查找不存在的项目
    index = tab_manager.find_tab_by_item_id('item-4')
    if index == -1:
        print("✓ 正确：未找到item-4，返回-1")
    else:
        print(f"✗ 错误：查找不存在的项目应该返回-1，但返回了{index}")
    
    print("测试完成")

if __name__ == "__main__":
    test_find_tab_by_item_id()