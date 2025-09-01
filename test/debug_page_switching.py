#!/usr/bin/env python3
"""
调试页面切换和HTML加载
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication
from app.editor.webengine import WebPageManager, PageType
from app.editor.channel import WebCommunicationManager

def debug_page_switching():
    """调试页面切换和HTML加载"""
    print("开始调试页面切换和HTML加载...")
    
    # 初始化页面管理器
    page_manager = WebPageManager()
    
    # 创建通信管理器
    markdown_comm = WebCommunicationManager("markdown")
    excalidraw_comm = WebCommunicationManager("excalidraw")
    landing_comm = WebCommunicationManager("landing")
    
    # 连接信号
    def on_page_loaded(page_type, success):
        print(f"页面加载完成: {page_type}, 成功: {success}")
    
    def on_page_switched(from_type, to_type):
        print(f"页面切换: {from_type} -> {to_type}")
    
    page_manager.page_loaded.connect(on_page_loaded)
    page_manager.page_switched.connect(on_page_switched)
    
    print("\n1. 创建Markdown页面:")
    markdown_page = page_manager.get_or_create_page(PageType.MARKDOWN, markdown_comm)
    print(f"Markdown页面创建成功: {markdown_page is not None}")
    
    print("\n2. 创建Excalidraw页面:")
    excalidraw_page = page_manager.get_or_create_page(PageType.EXCALIDRAW, excalidraw_comm)
    print(f"Excalidraw页面创建成功: {excalidraw_page is not None}")
    
    print("\n3. 创建Landing页面:")
    landing_page = page_manager.get_or_create_page(PageType.LANDING, landing_comm)
    print(f"Landing页面创建成功: {landing_page is not None}")
    
    print("\n4. 切换到Markdown页面:")
    markdown_page2 = page_manager.get_or_create_page(PageType.MARKDOWN, markdown_comm)
    print(f"Markdown页面获取成功: {markdown_page2 is not None}")
    
    print("\n5. 切换到Excalidraw页面:")
    excalidraw_page2 = page_manager.get_or_create_page(PageType.EXCALIDRAW, excalidraw_comm)
    print(f"Excalidraw页面获取成功: {excalidraw_page2 is not None}")
    
    print("\n6. 切换到Landing页面:")
    landing_page2 = page_manager.get_or_create_page(PageType.LANDING, landing_comm)
    print(f"Landing页面获取成功: {landing_page2 is not None}")
    
    print("\n页面切换调试完成")

if __name__ == "__main__":
    print("MarkRender 页面切换调试")
    print("=" * 40)
    
    # 创建QApplication实例
    app = QApplication(sys.argv)
    
    # 运行调试
    debug_page_switching()
    
    print("\n调试完成！")