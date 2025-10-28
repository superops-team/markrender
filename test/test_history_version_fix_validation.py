#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证历史版本数据生成修复效果
测试修改标题、图标、颜色等操作是否能正确产生新历史版本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.markrender_manager import MarkRenderManager

def test_history_version_fix_validation():
    """验证历史版本数据生成修复效果"""
    print("开始验证历史版本数据生成修复效果...")
    
    # 创建MarkRenderManager实例
    manager = MarkRenderManager()
    
    # 创建测试文件
    print("1. 创建测试文件...")
    file_id = manager.save_item(
        title="验证测试文件",
        content="# 验证测试内容\n\n这是用于验证历史版本修复的测试文件内容",
        page_type="markdown",
        icon_type="textarea",
        icon_color="#FF0000",  # 红色
        display_name="我的验证测试文件"
    )
    print(f"   创建文件，ID: {file_id}")
    
    # 获取初始历史记录
    print("2. 获取初始历史记录...")
    initial_history = manager.get_change_history(file_id)
    print(f"   初始历史记录数量: {len(initial_history)}")
    
    # 修改标题
    print("3. 修改标题...")
    manager.update_title(file_id, "更新后的验证测试文件")
    
    # 修改图标类型
    print("4. 修改图标类型...")
    manager.update_icon(file_id, icon_type="file")
    
    # 修改图标颜色
    print("5. 修改图标颜色...")
    manager.update_icon(file_id, icon_color="#00FF00")  # 绿色
    
    # 修改显示名称
    print("6. 修改显示名称...")
    manager.update_display_name(file_id, "我的更新后的验证测试文件")
    
    # 再次获取历史记录
    print("7. 获取更新后的历史记录...")
    updated_history = manager.get_change_history(file_id)
    print(f"   更新后历史记录数量: {len(updated_history)}")
    
    # 验证历史记录是否正确增加
    expected_new_records = 4  # 标题更新、图标类型更新、图标颜色更新、显示名称更新
    actual_new_records = len(updated_history) - len(initial_history)
    
    print(f"8. 验证历史记录...")
    print(f"   期望新增记录数: {expected_new_records}")
    print(f"   实际新增记录数: {actual_new_records}")
    
    if actual_new_records >= expected_new_records:
        print("   ✓ 验证通过：修改标题、图标、颜色等操作能正确产生新历史版本")
    else:
        print("   ✗ 验证失败：修改标题、图标、颜色等操作未能正确产生新历史版本")
    
    # 打印详细的历史记录信息
    print("9. 详细历史记录信息:")
    for i, record in enumerate(updated_history):
        print(f"   记录 {i+1}:")
        print(f"     类型: {record.change_type}")
        print(f"     原因: {record.change_reason}")
        print(f"     时间: {record.change_at}")
        if record.old_title or record.new_title:
            print(f"     标题变更: '{record.old_title}' -> '{record.new_title}'")
        if record.old_icon_type or record.new_icon_type:
            print(f"     图标类型变更: '{record.old_icon_type}' -> '{record.new_icon_type}'")
        if record.old_icon_color or record.new_icon_color:
            print(f"     图标颜色变更: '{record.old_icon_color}' -> '{record.new_icon_color}'")
        if record.old_display_name or record.new_display_name:
            print(f"     显示名称变更: '{record.old_display_name}' -> '{record.new_display_name}'")
        print()
    
    # 清理测试数据
    print("10. 清理测试数据...")
    manager.delete_item(file_id)
    print("   测试数据清理完成")
    
    return actual_new_records >= expected_new_records

if __name__ == "__main__":
    success = test_history_version_fix_validation()
    if success:
        print("\n🎉 所有测试通过！历史版本数据生成修复成功！")
        sys.exit(0)
    else:
        print("\n❌ 测试失败！请检查历史版本数据生成逻辑。")
        sys.exit(1)