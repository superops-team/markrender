#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试历史记录内容修复
验证不同类型的历史记录是否能正确显示差异
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from diff_match_patch import diff_match_patch

def test_diff_logic():
    """测试差异逻辑"""
    print("🚀 启动差异逻辑测试...")
    
    # 创建diff-match-patch实例
    dmp = diff_match_patch()
    
    # 测试内容变更
    print("\n=== 测试内容变更 ===")
    current_content = "# 当前文档\n\n这是当前的文档内容。"
    history_content = "# 历史文档\n\n这是历史的文档内容。"
    
    diffs = dmp.diff_main(current_content, history_content)
    dmp.diff_cleanupSemantic(diffs)
    
    print("当前内容:", repr(current_content))
    print("历史内容:", repr(history_content))
    print("差异结果:")
    for op, text in diffs:
        if op == dmp.DIFF_EQUAL:
            print(f"  等同: {repr(text[:30])}")
        elif op == dmp.DIFF_DELETE:
            print(f"  删除: {repr(text[:30])}")
        elif op == dmp.DIFF_INSERT:
            print(f"  插入: {repr(text[:30])}")
    
    # 测试标题变更
    print("\n=== 测试标题变更 ===")
    current_title = "当前标题"
    history_title = "历史标题"
    
    diffs = dmp.diff_main(current_title, history_title)
    dmp.diff_cleanupSemantic(diffs)
    
    print("当前标题:", repr(current_title))
    print("历史标题:", repr(history_title))
    print("差异结果:")
    for op, text in diffs:
        if op == dmp.DIFF_EQUAL:
            print(f"  等同: {repr(text[:30])}")
        elif op == dmp.DIFF_DELETE:
            print(f"  删除: {repr(text[:30])}")
        elif op == dmp.DIFF_INSERT:
            print(f"  插入: {repr(text[:30])}")
    
    # 测试显示名称变更
    print("\n=== 测试显示名称变更 ===")
    current_display_name = "当前显示名称"
    history_display_name = "历史显示名称"
    
    diffs = dmp.diff_main(current_display_name, history_display_name)
    dmp.diff_cleanupSemantic(diffs)
    
    print("当前显示名称:", repr(current_display_name))
    print("历史显示名称:", repr(history_display_name))
    print("差异结果:")
    for op, text in diffs:
        if op == dmp.DIFF_EQUAL:
            print(f"  等同: {repr(text[:30])}")
        elif op == dmp.DIFF_DELETE:
            print(f"  删除: {repr(text[:30])}")
        elif op == dmp.DIFF_INSERT:
            print(f"  插入: {repr(text[:30])}")
    
    print("\n✅ 差异逻辑测试完成")

if __name__ == "__main__":
    test_diff_logic()
