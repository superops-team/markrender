#!/usr/bin/env python3
"""
完整测试页面切换功能，包括HTML加载和WebChannel初始化
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from app.editor.webengine import WebPageManager, PageType
from app.editor.backend_interface import BackendInterface

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("页面切换测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 初始化页面管理器
        self.page_manager = WebPageManager()
        
        # 创建通信管理器
        self.markdown_comm = BackendInterface("markdown")
        self.excalidraw_comm = BackendInterface("excalidraw")
        self.landing_comm = BackendInterface("landing")
        
        # 连接信号
        self.page_manager.page_loaded.connect(self.on_page_loaded)
        self.page_manager.page_switched.connect(self.on_page_switched)
        
        # 创建UI
        self.setup_ui()
        
        # 预加载页面
        self.preload_pages()
    
    def setup_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # 创建按钮
        self.markdown_btn = QPushButton("切换到Markdown页面")
        self.excalidraw_btn = QPushButton("切换到Excalidraw页面")
        self.landing_btn = QPushButton("切换到Landing页面")
        
        # 连接按钮信号
        self.markdown_btn.clicked.connect(lambda: self.switch_to_page(PageType.MARKDOWN))
        self.excalidraw_btn.clicked.connect(lambda: self.switch_to_page(PageType.EXCALIDRAW))
        self.landing_btn.clicked.connect(lambda: self.switch_to_page(PageType.LANDING))
        
        # 添加到布局
        layout.addWidget(self.markdown_btn)
        layout.addWidget(self.excalidraw_btn)
        layout.addWidget(self.landing_btn)
        
        # 创建预览区域
        self.preview = None
        
        self.setCentralWidget(central_widget)
    
    def preload_pages(self):
        print("预加载页面...")
        self.page_manager.preload_page_type(PageType.MARKDOWN, self.markdown_comm)
        self.page_manager.preload_page_type(PageType.EXCALIDRAW, self.excalidraw_comm)
        self.page_manager.preload_page_type(PageType.LANDING, self.landing_comm)
    
    def switch_to_page(self, page_type):
        print(f"切换到页面: {page_type.value}")
        
        # 根据页面类型选择通信管理器
        if page_type == PageType.MARKDOWN:
            backend_interface = self.markdown_comm
        elif page_type == PageType.EXCALIDRAW:
            backend_interface = self.excalidraw_comm
        else:
            backend_interface = self.landing_comm
        
        # 获取或创建页面
        view = self.page_manager.get_or_create_page(page_type, backend_interface)
        
        if view:
            # 更新通信管理器的页面引用
            if page_type == PageType.MARKDOWN:
                self.markdown_comm.set_page(view.page())
            elif page_type == PageType.EXCALIDRAW:
                self.excalidraw_comm.set_page(view.page())
            else:
                self.landing_comm.set_page(view.page())
            
            # 显示页面
            if self.preview:
                self.centralWidget().layout().removeWidget(self.preview)
                self.preview.setParent(None)
            
            self.preview = view
            self.centralWidget().layout().addWidget(view)
            view.show()
    
    def on_page_loaded(self, page_type, success):
        print(f"页面加载完成: {page_type}, 成功: {success}")
    
    def on_page_switched(self, from_type, to_type):
        print(f"页面切换: {from_type} -> {to_type}")

def test_full_page_switching():
    """完整测试页面切换功能"""
    print("开始完整页面切换测试...")
    
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    
    print("测试窗口已显示，请手动点击按钮测试页面切换")
    print("关闭窗口以结束测试")
    
    return app.exec()

if __name__ == "__main__":
    print("MarkRender 完整页面切换测试")
    print("=" * 40)
    
    # 运行测试
    exit_code = test_full_page_switching()
    
    print("\n测试完成！")
    sys.exit(exit_code)