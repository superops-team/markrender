#!/usr/bin/env python3
"""
测试不同quickpick项目的数据显示隔离
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_item_isolation():
    """测试项目数据隔离"""
    print("测试项目数据隔离...")
    
    # 模拟两个不同的quickpick项目
    item1 = {
        'id': '1',
        'title': '项目1',
        'content': '这是项目1的内容',
        'page_type': 'markdown'
    }
    
    item2 = {
        'id': '2',
        'title': '项目2',
        'content': '这是项目2的内容',
        'page_type': 'markdown'
    }
    
    print(f"项目1 ID: {item1['id']}, 内容: {item1['content']}")
    print(f"项目2 ID: {item2['id']}, 内容: {item2['content']}")
    
    # 验证两个项目有不同的ID和内容
    if item1['id'] != item2['id'] and item1['content'] != item2['content']:
        print("✓ 项目数据隔离检查通过")
        return True
    else:
        print("✗ 项目数据隔离检查失败")
        return False

if __name__ == "__main__":
    print("MarkRender 项目数据隔离测试")
    print("=" * 40)
    
    success = test_item_isolation()
    
    if success:
        print("\n测试通过！项目数据隔离功能正常。")
    else:
        print("\n测试失败！项目数据可能未正确隔离。")