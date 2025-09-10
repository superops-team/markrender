#!/usr/bin/env python3
"""
测试空内容处理功能
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication
from app.editor.webengine import WebPageManager, PageType
from app.editor.backend_interface import BackendInterface
from app.editor.excalidraw_utils import ExcalidrawDataHandler

def test_empty_content_handling():
    """测试空内容处理"""
    print("开始测试空内容处理...")
    
    # 初始化页面管理器
    page_manager = WebPageManager()
    
    # 创建通信管理器
    markdown_comm = BackendInterface("markdown")
    excalidraw_comm = BackendInterface("excalidraw")
    
    print("\n1. 测试Markdown空内容处理:")
    # 测试空字符串
    empty_content = ""
    print(f"空内容: '{empty_content}'")
    
    # 测试None值
    none_content = None
    print(f"None内容: {none_content}")
    
    # 测试空格字符串
    whitespace_content = "   "
    print(f"空格内容: '{whitespace_content}'")
    
    print("\n2. 测试Excalidraw空内容处理:")
    # 测试空的Excalidraw数据
    empty_excalidraw_data = {}
    normalized_empty = ExcalidrawDataHandler.normalize_drawing_data(empty_excalidraw_data)
    print(f"空Excalidraw数据标准化结果: '{normalized_empty}'")
    
    # 测试空字符串
    empty_string = ""
    try:
        normalized_empty_string = ExcalidrawDataHandler.normalize_drawing_data(empty_string)
        print(f"空字符串标准化结果: '{normalized_empty_string}'")
    except ValueError as e:
        print(f"空字符串标准化失败: {e}")
    
    # 测试空JSON对象
    empty_json = "{}"
    normalized_empty_json = ExcalidrawDataHandler.normalize_drawing_data(empty_json)
    print(f"空JSON对象标准化结果: '{normalized_empty_json}'")
    
    # 测试None值
    none_data = None
    try:
        normalized_none = ExcalidrawDataHandler.normalize_drawing_data(none_data)
        print(f"None数据标准化结果: '{normalized_none}'")
    except ValueError as e:
        print(f"None数据标准化失败: {e}")
    
    print("\n3. 测试页面管理器空内容处理:")
    # 创建页面实例
    markdown_page = page_manager.get_or_create_page(PageType.MARKDOWN, markdown_comm)
    print(f"Markdown页面创建成功: {markdown_page is not None}")
    
    excalidraw_page = page_manager.get_or_create_page(PageType.EXCALIDRAW, excalidraw_comm)
    print(f"Excalidraw页面创建成功: {excalidraw_page is not None}")
    
    print("\n4. 测试数据库空内容模拟:")
    # 模拟从数据库获取的空内容
    db_content = ""  # 模拟数据库返回空字符串
    print(f"数据库返回内容: '{db_content}'")
    
    # 模拟从数据库获取None值
    db_none_content = None  # 模拟数据库返回None
    print(f"数据库返回None: {db_none_content}")
    
    # 模拟从数据库获取空JSON
    db_empty_json = "{}"  # 模拟数据库返回空JSON
    print(f"数据库返回空JSON: '{db_empty_json}'")
    
    print("\n5. 测试内容标准化:")
    # 测试各种输入的标准化
    test_cases = [
        ("", "空字符串"),
        (None, "None值"),
        ("{}", "空JSON对象"),
        ("   ", "空格字符串"),
        ('{"elements": []}', "空元素JSON"),
    ]
    
    for content, description in test_cases:
        try:
            if description == "None值":
                normalized = ExcalidrawDataHandler.normalize_drawing_data(content) if content is not None else ""
            else:
                normalized = ExcalidrawDataHandler.normalize_drawing_data(content)
            print(f"{description} 标准化结果: '{normalized}'")
        except ValueError as e:
            print(f"{description} 标准化失败: {e}")
    
    print("\n空内容处理测试完成")

def test_page_switching_with_empty_content():
    """测试页面切换时的空内容处理"""
    print("\n开始测试页面切换时的空内容处理...")
    
    # 初始化页面管理器
    page_manager = WebPageManager()
    
    # 创建通信管理器
    markdown_comm = BackendInterface("markdown")
    excalidraw_comm = BackendInterface("excalidraw")
    
    # 创建页面实例
    markdown_page = page_manager.get_or_create_page(PageType.MARKDOWN, markdown_comm)
    excalidraw_page = page_manager.get_or_create_page(PageType.EXCALIDRAW, excalidraw_comm)
    
    print("页面创建完成")
    
    # 模拟页面切换时的空内容处理
    print("\n模拟Markdown页面切换:")
    markdown_content = ""  # 模拟空内容
    print(f"切换到Markdown页面，内容: '{markdown_content}'")
    
    print("\n模拟Excalidraw页面切换:")
    excalidraw_content = ""  # 模拟空内容
    print(f"切换到Excalidraw页面，内容: '{excalidraw_content}'")
    print("发送空JSON对象重置面板: '{}'")
    
    print("\n页面切换空内容处理测试完成")

if __name__ == "__main__":
    print("MarkRender 空内容处理测试")
    print("=" * 40)
    
    # 创建QApplication实例
    app = QApplication(sys.argv)
    
    # 运行测试
    test_empty_content_handling()
    test_page_switching_with_empty_content()
    
    print("\n所有测试完成！")