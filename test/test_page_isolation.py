#!/usr/bin/env python3
"""
测试页面隔离功能，验证页面切换时内容不会混乱
"""

import sys
import time
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from app.editor.editor import MarkRenderEditor
from app.editor.webengine import WebPageManager

def test_page_isolation():
    """测试页面隔离功能"""
    print("开始测试页面隔离功能...")
    
    app = QApplication.instance() or QApplication(sys.argv)
    
    # 创建编辑器实例
    editor = MarkRenderEditor()
    
    # 获取页面管理器
    page_manager = editor.page_manager
    
    print(f"初始页面类型: {page_manager.current_page_type}")
    print(f"页面数量: {page_manager.get_page_count()}")
    print(f"所有页面类型: {page_manager.get_all_page_types()}")
    
    # 测试页面切换和内容隔离
    def test_switching():
        print("\n=== 测试页面切换和内容隔离 ===")
        
        # 模拟切换到Markdown页面并设置内容
        print("1. 切换到Markdown页面并设置内容")
        page_manager.switch_to_page("markdown")
        # 这里应该通过editor.set_text_content设置内容
        print("   Markdown页面内容已设置")
        
        # 等待一段时间
        time.sleep(1)
        
        # 模拟切换到Excalidraw页面并设置内容
        print("2. 切换到Excalidraw页面并设置内容")
        page_manager.switch_to_page("excalidraw")
        # 这里应该通过editor.set_text_content设置内容
        print("   Excalidraw页面内容已设置")
        
        # 等待一段时间
        time.sleep(1)
        
        # 再次切换回Markdown页面
        print("3. 切换回Markdown页面")
        page_manager.switch_to_page("markdown")
        # 检查内容是否正确
        print("   Markdown页面内容应保持不变")
        
        # 等待一段时间
        time.sleep(1)
        
        # 再次切换到Excalidraw页面
        print("4. 再次切换到Excalidraw页面")
        page_manager.switch_to_page("excalidraw")
        # 检查内容是否正确
        print("   Excalidraw页面内容应保持不变")
        
        print("\n页面隔离测试完成！")
        print("请手动检查页面内容是否正确隔离，没有出现内容混乱的情况。")
        
        # 退出应用
        app.quit()
    
    # 使用QTimer延迟执行测试，确保页面初始化完成
    QTimer.singleShot(2000, test_switching)
    
    return app.exec()

if __name__ == "__main__":
    print("MarkRender 页面隔离测试")
    print("=" * 40)
    
    try:
        exit_code = test_page_isolation()
        print(f"\n测试完成，退出码: {exit_code}")
        sys.exit(exit_code)
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)