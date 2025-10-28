#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试历史版本数据生成
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.markrender_manager import MarkRenderManager

def simple_test():
    """简单测试历史版本数据生成"""
    print("开始简单测试历史版本数据生成...")
    
    # 创建MarkRenderManager实例
    manager = MarkRenderManager()
    
    # 创建测试文件
    print("1. 创建测试文件...")
    file_id = manager.save_item(
        title="简单测试文件",
        content="# 简单测试内容\n\n这是用于简单测试历史版本的测试文件内容",
        page_type="markdown"
    )
    print(f"   创建文件，ID: {file_id}")
    
    # 获取初始历史记录
    print("2. 获取初始历史记录...")
    initial_history = manager.get_change_history(file_id)
    print(f"   初始历史记录数量: {len(initial_history)}")
    
    # 修改标题
    print("3. 修改标题...")
    manager.update_title(file_id, "更新后的简单测试文件")
    
    # 再次获取历史记录
    print("4. 获取更新后的历史记录...")
    updated_history = manager.get_change_history(file_id)
    print(f"   更新后历史记录数量: {len(updated_history)}")
    
    # 打印详细的历史记录信息
    print("5. 详细历史记录信息:")
    for i, record in enumerate(updated_history):
        print(f"   记录 {i+1}:")
        print(f"     类型: {record.change_type}")
        print(f"     原因: {record.change_reason}")
        print(f"     时间: {record.change_at}")
        if record.old_title or record.new_title:
            print(f"     标题变更: '{record.old_title}' -> '{record.new_title}'")
        print()

if __name__ == "__main__":
    simple_test()