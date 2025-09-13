#!/usr/bin/env python3
"""
测试页面复用功能，验证不同页面类型是否正确复用
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication
from app.editor.webengine import WebPageManager, PageType

def test_page_reuse():
    """测试页面复用功能"""
    print("开始测试页面复用功能...")
    
    # 初始化页面管理器
    page_manager = WebPageManager()
    
    # 测试创建不同类型的页面
    print("\n1. 测试创建不同类型的页面:")
    
    # 创建Markdown页面
    markdown_page1 = page_manager.get_or_create_page(PageType.MARKDOWN)
    print(f"创建Markdown页面1: {markdown_page1 is not None}")
    
    # 再次创建Markdown页面（应该复用）
    markdown_page2 = page_manager.get_or_create_page(PageType.MARKDOWN)
    print(f"创建Markdown页面2: {markdown_page2 is not None}")
    print(f"Markdown页面是否复用: {markdown_page1 is markdown_page2}")
    
    # 创建Excalidraw页面
    excalidraw_page1 = page_manager.get_or_create_page(PageType.EXCALIDRAW)
    print(f"创建Excalidraw页面1: {excalidraw_page1 is not None}")
    
    # 再次创建Excalidraw页面（应该复用）
    excalidraw_page2 = page_manager.get_or_create_page(PageType.EXCALIDRAW)
    print(f"创建Excalidraw页面2: {excalidraw_page2 is not None}")
    print(f"Excalidraw页面是否复用: {excalidraw_page1 is excalidraw_page2}")
    
    # 验证不同类型页面不互相干扰
    print("\n2. 验证不同类型页面隔离:")
    print(f"Markdown页面 != Excalidraw页面: {markdown_page1 is not excalidraw_page1}")
    
    # 测试页面数量
    print("\n3. 测试页面数量:")
    page_count = page_manager.get_page_count()
    print(f"当前页面数量: {page_count}")
    
    # 测试获取所有页面类型
    all_page_types = page_manager.get_all_page_types()
    print(f"所有页面类型: {[pt for pt in all_page_types]}")
    
    print("\n页面复用功能测试完成")

if __name__ == "__main__":
    print("MarkRender 页面复用功能测试")
    print("=" * 40)
    
    # 创建QApplication实例
    app = QApplication(sys.argv)
    
    # 运行测试
    test_page_reuse()
    
    print("\n所有测试完成！")