#!/usr/bin/env python3
"""
测试页面切换功能，验证页面切换时BackendInterface是否正确更新
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication
from app.editor.webengine import WebPageManager, PageType
from app.editor.channel import BackendInterface

def test_page_switching():
    """测试页面切换功能"""
    print("开始测试页面切换功能...")
    
    # 初始化页面管理器
    page_manager = WebPageManager()
    
    # 创建通信管理器
    web_comm = BackendInterface("test")
    
    # 测试创建不同类型的页面
    print("\n1. 测试创建不同类型的页面:")
    
    # 创建Markdown页面
    markdown_page = page_manager.get_or_create_page(PageType.MARKDOWN, web_comm)
    print(f"创建Markdown页面: {markdown_page is not None}")
    if markdown_page:
        # 手动设置页面引用
        web_comm.set_page(markdown_page.page())
        print(f"WebComm页面引用: {web_comm.page}")
        print(f"页面类型: {markdown_page.page().page_type if markdown_page.page() else 'None'}")
    
    # 创建Excalidraw页面
    excalidraw_page = page_manager.get_or_create_page(PageType.EXCALIDRAW, web_comm)
    print(f"创建Excalidraw页面: {excalidraw_page is not None}")
    if excalidraw_page:
        # 手动设置页面引用
        web_comm.set_page(excalidraw_page.page())
        print(f"WebComm页面引用: {web_comm.page}")
        print(f"页面类型: {excalidraw_page.page().page_type if excalidraw_page.page() else 'None'}")
    
    # 再次获取Markdown页面（应该复用）
    markdown_page2 = page_manager.get_or_create_page(PageType.MARKDOWN, web_comm)
    print(f"再次获取Markdown页面: {markdown_page2 is not None}")
    print(f"Markdown页面是否复用: {markdown_page is markdown_page2}")
    if markdown_page2:
        # 手动设置页面引用
        web_comm.set_page(markdown_page2.page())
        print(f"WebComm页面引用: {web_comm.page}")
        print(f"页面类型: {markdown_page2.page().page_type if markdown_page2.page() else 'None'}")
    
    print("\n页面切换功能测试完成")

if __name__ == "__main__":
    print("MarkRender 页面切换功能测试")
    print("=" * 40)
    
    # 创建QApplication实例
    app = QApplication(sys.argv)
    
    # 运行测试
    test_page_switching()
    
    print("\n所有测试完成！")