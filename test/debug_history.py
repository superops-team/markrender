#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试历史版本数据生成问题
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.markrender_manager import MarkRenderManager

def debug_history():
    """调试历史版本数据生成问题"""
    print("开始调试历史版本数据生成问题...")
    
    # 创建MarkRenderManager实例
    manager = MarkRenderManager()
    
    # 创建测试文件
    print("1. 创建测试文件...")
    file_id = manager.save_item(
        title="调试测试文件",
        content="# 调试测试内容\n\n这是用于调试历史版本的测试文件内容",
        page_type="markdown",
        icon_type="textarea",
        icon_color="#FF0000",  # 红色
        display_name="我的调试测试文件"
    )
    print(f"   创建文件，ID: {file_id}")
    
    # 检查创建历史记录
    print("2. 检查创建历史记录...")
    initial_history = manager.get_change_history(file_id)
    print(f"   创建后历史记录数量: {len(initial_history)}")
    for record in initial_history:
        print(f"     类型: {record.change_type}, 原因: {record.change_reason}")
    
    # 修改标题
    print("3. 修改标题...")
    manager.update_title(file_id, "更新后的调试测试文件")
    
    # 检查标题更新历史记录
    print("4. 检查标题更新历史记录...")
    updated_history = manager.get_change_history(file_id)
    print(f"   标题更新后历史记录数量: {len(updated_history)}")
    for record in updated_history:
        print(f"     类型: {record.change_type}, 原因: {record.change_reason}")
        if record.old_title or record.new_title:
            print(f"     标题变更: '{record.old_title}' -> '{record.new_title}'")
    
    # 清理测试数据
    print("5. 清理测试数据...")
    manager.delete_item(file_id)
    print("   测试数据清理完成")

if __name__ == "__main__":
    debug_history()