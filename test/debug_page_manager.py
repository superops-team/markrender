#!/usr/bin/env python3
"""
调试页面管理器，查看页面创建和复用过程
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication
from app.editor.webengine import WebPageManager, PageType
from app.editor.backend_interface import BackendInterface

def debug_page_manager():
    """调试页面管理器"""
    print("开始调试页面管理器...")
    
    # 初始化页面管理器
    page_manager = WebPageManager()
    
    # 创建通信管理器
    markdown_comm = BackendInterface("markdown")
    excalidraw_comm = BackendInterface("excalidraw")
    landing_comm = BackendInterface("landing")
    
    print("\n1. 创建Markdown页面:")
    markdown_page = page_manager.get_or_create_page(PageType.MARKDOWN, markdown_comm)
    print(f"Markdown页面创建成功: {markdown_page is not None}")
    if markdown_page:
        page_obj = markdown_page.page()
        if hasattr(page_obj, 'page_type'):
            print(f"Markdown页面类型: {page_obj.page_type}")
    
    print("\n2. 创建Excalidraw页面:")
    excalidraw_page = page_manager.get_or_create_page(PageType.EXCALIDRAW, excalidraw_comm)
    print(f"Excalidraw页面创建成功: {excalidraw_page is not None}")
    if excalidraw_page:
        page_obj = excalidraw_page.page()
        if hasattr(page_obj, 'page_type'):
            print(f"Excalidraw页面类型: {page_obj.page_type}")
    
    print("\n3. 创建Landing页面:")
    landing_page = page_manager.get_or_create_page(PageType.LANDING, landing_comm)
    print(f"Landing页面创建成功: {landing_page is not None}")
    if landing_page:
        page_obj = landing_page.page()
        if hasattr(page_obj, 'page_type'):
            print(f"Landing页面类型: {page_obj.page_type}")
    
    print("\n4. 再次获取Markdown页面:")
    markdown_page2 = page_manager.get_or_create_page(PageType.MARKDOWN, markdown_comm)
    print(f"Markdown页面获取成功: {markdown_page2 is not None}")
    print(f"是否复用了同一个页面: {markdown_page is markdown_page2}")
    if markdown_page2:
        page_obj = markdown_page2.page()
        if hasattr(page_obj, 'page_type'):
            print(f"复用的Markdown页面类型: {page_obj.page_type}")
    
    print("\n5. 再次获取Excalidraw页面:")
    excalidraw_page2 = page_manager.get_or_create_page(PageType.EXCALIDRAW, excalidraw_comm)
    print(f"Excalidraw页面获取成功: {excalidraw_page2 is not None}")
    print(f"是否复用了同一个页面: {excalidraw_page is excalidraw_page2}")
    if excalidraw_page2:
        page_obj = excalidraw_page2.page()
        if hasattr(page_obj, 'page_type'):
            print(f"复用的Excalidraw页面类型: {page_obj.page_type}")
    
    print("\n6. 再次获取Landing页面:")
    landing_page2 = page_manager.get_or_create_page(PageType.LANDING, landing_comm)
    print(f"Landing页面获取成功: {landing_page2 is not None}")
    print(f"是否复用了同一个页面: {landing_page is landing_page2}")
    if landing_page2:
        page_obj = landing_page2.page()
        if hasattr(page_obj, 'page_type'):
            print(f"复用的Landing页面类型: {page_obj.page_type}")
    
    print("\n7. 检查页面配置:")
    for page_type, config in page_manager.page_configs.items():
        print(f"页面类型 {page_type}: 配置类型 {config.page_type}")
    
    print("\n8. 检查预加载页面:")
    for page_type, view in page_manager.preloaded_pages.items():
        page_obj = view.page()
        if hasattr(page_obj, 'page_type'):
            print(f"预加载页面 {page_type}: 页面对象类型 {page_obj.page_type}")
    
    print("\n页面管理器调试完成")

if __name__ == "__main__":
    print("MarkRender 页面管理器调试")
    print("=" * 40)
    
    # 创建QApplication实例
    app = QApplication(sys.argv)
    
    # 运行调试
    debug_page_manager()
    
    print("\n调试完成！")