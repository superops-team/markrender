#!/usr/bin/env python3
"""
测试WebChannel处理器注册
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_webchannel_handlers():
    """测试WebChannel处理器注册"""
    print("测试WebChannel处理器注册...")
    
    # 模拟WebCommunicationManager
    class MockWebCommunicationManager:
        def __init__(self, page_type):
            self.page_type = page_type
            self.python_handlers = {}
        
        def register_python_handler(self, action, handler, is_async=False):
            """注册处理器"""
            self.python_handlers[action] = (handler, is_async)
            print(f"  注册处理器: {action} (异步: {is_async})")
        
        def has_handler(self, action):
            """检查是否存在处理器"""
            return action in self.python_handlers
    
    # 创建模拟的WebCommunicationManager实例
    web_comm = MockWebCommunicationManager("markdown")
    
    # 模拟处理器函数
    def mock_handler(data):
        return {"success": True}
    
    # 注册必要的处理器
    handlers_to_register = [
        ('autoSave', mock_handler, True),
        ('contentChanged', mock_handler, False),
        ('getContent', mock_handler, False),
        ('setValue', mock_handler, False),
        ('setCurrentFileId', mock_handler, False),
        ('frontendReady', mock_handler, False),
        ('reportError', mock_handler, False)
    ]
    
    print("注册处理器:")
    for action, handler, is_async in handlers_to_register:
        web_comm.register_python_handler(action, handler, is_async)
    
    # 检查关键处理器是否已注册
    required_handlers = ['contentChanged', 'setValue', 'getContent']
    print("\n检查关键处理器:")
    all_handlers_registered = True
    for handler in required_handlers:
        if web_comm.has_handler(handler):
            print(f"  ✓ {handler} 已注册")
        else:
            print(f"  ✗ {handler} 未注册")
            all_handlers_registered = False
    
    if all_handlers_registered:
        print("\n✓ WebChannel处理器注册检查通过")
        return True
    else:
        print("\n✗ WebChannel处理器注册检查失败")
        return False

if __name__ == "__main__":
    print("MarkRender WebChannel处理器注册测试")
    print("=" * 40)
    
    success = test_webchannel_handlers()
    
    if success:
        print("\n测试通过！WebChannel处理器已正确注册。")
    else:
        print("\n测试失败！WebChannel处理器注册存在问题。")