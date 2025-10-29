#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试diff-match-patch差异对比
验证diff-match-patch的参数顺序和差异显示效果
"""

from diff_match_patch import diff_match_patch

def test_diff_match_patch():
    """测试diff-match-patch参数顺序和差异显示效果"""
    print("🚀 启动diff-match-patch调试...")
    
    # 测试数据
    current_content = """# 当前版本标题

这是当前版本的内容，包含一些文本。

## 当前章节

这里有一些当前版本特有的内容。"""
    
    history_content = """# 历史版本标题

这是历史版本的内容，包含一些文本。

## 历史章节

这里有一些历史版本特有的内容。"""
    
    print("当前内容:")
    print(repr(current_content))
    print("\n历史内容:")
    print(repr(history_content))
    
    # 创建diff-match-patch实例
    dmp = diff_match_patch()
    
    # 测试参数顺序1：current_content, history_content (当前->历史)
    print("\n=== 参数顺序1：current_content, history_content ===")
    diffs1 = dmp.diff_main(current_content, history_content)
    dmp.diff_cleanupSemantic(diffs1)
    
    print("差异结果:")
    for op, text in diffs1:
        if op == dmp.DIFF_EQUAL:
            print(f"  等同: {repr(text[:50])}")
        elif op == dmp.DIFF_DELETE:
            print(f"  删除: {repr(text[:50])}")
        elif op == dmp.DIFF_INSERT:
            print(f"  插入: {repr(text[:50])}")
    
    # 测试参数顺序2：history_content, current_content (历史->当前)
    print("\n=== 参数顺序2：history_content, current_content ===")
    diffs2 = dmp.diff_main(history_content, current_content)
    dmp.diff_cleanupSemantic(diffs2)
    
    print("差异结果:")
    for op, text in diffs2:
        if op == dmp.DIFF_EQUAL:
            print(f"  等同: {repr(text[:50])}")
        elif op == dmp.DIFF_DELETE:
            print(f"  删除: {repr(text[:50])}")
        elif op == dmp.DIFF_INSERT:
            print(f"  插入: {repr(text[:50])}")
    
    print("\n✅ 调试完成")

if __name__ == "__main__":
    test_diff_match_patch()
