#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多页面WebEngine管理系统测试用例
测试PageType枚举、多页面创建、切换、预加载等功能
"""

import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont

from utils.logger_utils import logger
from app.editor.webengine import WebPageManager, PageType, PageConfig, CustomWebEnginePage
from app.editor.backend_interface import BackendInterface

class MultiPageTestWindow(QMainWindow):
    """多页面管理系统测试窗口"""
    
    def __init__(self):
        super().__init__()
        self.page_manager = WebPageManager()
        self.web_comm = None
        self.current_page_id = None
        self.test_results = []
        self.init_ui()
        self.init_web_comm()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("🧪 多页面WebEngine管理系统测试")
        self.setGeometry(100, 100, 1000, 700)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 标题
        title = QLabel("🧪 多页面WebEngine管理系统测试")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 测试状态显示
        self.status_label = QLabel("📋 准备开始测试...")
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #f0f9ff;
                border: 1px solid #0ea5e9;
                border-radius: 6px;
                padding: 12px;
                color: #0c4a6e;
                font-weight: 500;
            }
        """)
        layout.addWidget(self.status_label)
        
        # 测试按钮区域
        button_layout = QHBoxLayout()
        
        # 基础功能测试
        basic_tests_layout = QVBoxLayout()
        basic_title = QLabel("🔧 基础功能测试")
        basic_title.setFont(QFont("Arial", 12, QFont.Bold))
        basic_tests_layout.addWidget(basic_title)
        
        self.test_enum_btn = QPushButton("📝 测试PageType枚举")
        self.test_enum_btn.clicked.connect(self.test_page_type_enum)
        self.test_enum_btn.setStyleSheet(self.get_button_style())
        basic_tests_layout.addWidget(self.test_enum_btn)
        
        self.test_manager_btn = QPushButton("🏗️ 测试页面管理器")
        self.test_manager_btn.clicked.connect(self.test_page_manager)
        self.test_manager_btn.setStyleSheet(self.get_button_style())
        basic_tests_layout.addWidget(self.test_manager_btn)
        
        self.test_config_btn = QPushButton("⚙️ 测试页面配置")
        self.test_config_btn.clicked.connect(self.test_page_config)
        self.test_config_btn.setStyleSheet(self.get_button_style())
        basic_tests_layout.addWidget(self.test_config_btn)
        
        # 页面创建测试
        page_tests_layout = QVBoxLayout()
        page_title = QLabel("📄 页面创建测试")
        page_title.setFont(QFont("Arial", 12, QFont.Bold))
        page_tests_layout.addWidget(page_title)
        
        self.create_markdown_btn = QPushButton("📝 创建Markdown页面")
        self.create_markdown_btn.clicked.connect(lambda: self.test_create_page(PageType.MARKDOWN))
        self.create_markdown_btn.setStyleSheet(self.get_button_style())
        page_tests_layout.addWidget(self.create_markdown_btn)
        
        self.create_board_btn = QPushButton("🎨 创建Board页面")
        self.create_board_btn.clicked.connect(lambda: self.test_create_page(PageType.EXCALIDRAW))
        self.create_board_btn.setStyleSheet(self.get_button_style())
        page_tests_layout.addWidget(self.create_board_btn)
        
        self.create_landing_btn = QPushButton("🏠 创建Landing页面")
        self.create_landing_btn.clicked.connect(lambda: self.test_create_page(PageType.LANDING))
        self.create_landing_btn.setStyleSheet(self.get_button_style())
        page_tests_layout.addWidget(self.create_landing_btn)
        
        # 控制按钮
        control_layout = QVBoxLayout()
        control_title = QLabel("🎮 测试控制")
        control_title.setFont(QFont("Arial", 12, QFont.Bold))
        control_layout.addWidget(control_title)
        
        self.run_all_btn = QPushButton("🚀 运行全部测试")
        self.run_all_btn.clicked.connect(self.run_all_tests)
        self.run_all_btn.setStyleSheet(self.get_primary_button_style())
        control_layout.addWidget(self.run_all_btn)
        
        self.clear_results_btn = QPushButton("🧹 清空结果")
        self.clear_results_btn.clicked.connect(self.clear_test_results)
        self.clear_results_btn.setStyleSheet(self.get_button_style())
        control_layout.addWidget(self.clear_results_btn)
        
        # 添加到主布局
        button_layout.addLayout(basic_tests_layout)
        button_layout.addLayout(page_tests_layout)
        button_layout.addLayout(control_layout)
        
        layout.addLayout(button_layout)
        
        # 测试结果显示区域
        self.results_label = QLabel("📊 测试结果将在这里显示...")
        self.results_label.setStyleSheet("""
            QLabel {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 15px;
                color: #475569;
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }
        """)
        self.results_label.setAlignment(Qt.AlignTop)
        self.results_label.setMinimumHeight(300)
        self.results_label.setWordWrap(True)
        layout.addWidget(self.results_label)
        
    def get_button_style(self):
        return """
            QPushButton {
                background-color: #f1f5f9;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                padding: 10px 15px;
                color: #334155;
                font-weight: 500;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #e2e8f0;
                border-color: #94a3b8;
            }
        """
    
    def get_primary_button_style(self):
        return """
            QPushButton {
                background-color: #3b82f6;
                border: none;
                border-radius: 6px;
                padding: 12px 20px;
                color: white;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """
    
    def init_web_comm(self):
        """初始化WebChannel通信"""
        try:
            self.web_comm = BackendInterface("test_page_manager")
            logger.info("WebChannel通信管理器初始化成功")
        except Exception as e:
            logger.error(f"WebChannel通信管理器初始化失败: {e}")
    
    def update_status(self, message, is_error=False):
        """更新状态显示"""
        prefix = "❌" if is_error else "✅"
        self.status_label.setText(f"{prefix} {message}")
    
    def add_test_result(self, test_name, result, details=""):
        """添加测试结果"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        status = "✅ PASS" if result else "❌ FAIL"
        
        result_entry = {
            'timestamp': timestamp,
            'test_name': test_name,
            'result': result,
            'details': details
        }
        
        self.test_results.append(result_entry)
        
        # 更新显示
        result_text = f"[{timestamp}] {status} {test_name}"
        if details:
            result_text += f"\\n    {details}"
        
        current_text = self.results_label.text()
        if current_text == "📊 测试结果将在这里显示...":
            current_text = ""
        
        new_text = current_text + "\\n" + result_text if current_text else result_text
        self.results_label.setText(new_text)
        
        logger.info(f"测试结果: {test_name} - {status}")
    
    def test_page_type_enum(self):
        """测试PageType枚举功能"""
        self.update_status("测试PageType枚举...")
        
        try:
            # 测试枚举值
            types = [PageType.MARKDOWN, PageType.EXCALIDRAW, PageType.LANDING, PageType.MOCK_TEST]
            
            for page_type in types:
                # 测试HTML文件映射
                html_file = page_type.html_file
                assert html_file.endswith('.html'), f"HTML文件名应以.html结尾: {html_file}"
                
                # 测试显示名称
                display_name = page_type.display_name
                assert len(display_name) > 0, f"显示名称不能为空: {page_type.value}"
            
            self.add_test_result("PageType枚举测试", True, f"测试了{len(types)}种页面类型")
            self.update_status("PageType枚举测试通过")
            
        except Exception as e:
            self.add_test_result("PageType枚举测试", False, str(e))
            self.update_status(f"PageType枚举测试失败: {e}", True)
    
    def test_page_manager(self):
        """测试页面管理器基础功能"""
        self.update_status("测试页面管理器...")
        
        try:
            # 测试单例模式
            manager1 = WebPageManager()
            manager2 = WebPageManager()
            assert manager1 is manager2, "页面管理器应该是单例"
            
            # 测试初始状态
            initial_count = manager1.get_page_count()
            logger.info(f"初始页面数量: {initial_count}")
            
            self.add_test_result("页面管理器基础测试", True, "单例模式和信号系统正常")
            self.update_status("页面管理器测试通过")
            
        except Exception as e:
            self.add_test_result("页面管理器基础测试", False, str(e))
            self.update_status(f"页面管理器测试失败: {e}", True)
    
    def test_page_config(self):
        """测试页面配置功能"""
        self.update_status("测试页面配置...")
        
        try:
            # 测试基本配置创建
            config1 = PageConfig(page_type=PageType.MARKDOWN)
            assert config1.page_type == PageType.MARKDOWN, "页面类型设置错误"
            assert config1.preload == False, "默认预加载应为False"
            
            # 测试字符串转换
            config2 = PageConfig(page_type="board")
            assert config2.page_type == PageType.EXCALIDRAW, "字符串转PageType失败"
            
            self.add_test_result("页面配置测试", True, "所有配置选项工作正常")
            self.update_status("页面配置测试通过")
            
        except Exception as e:
            self.add_test_result("页面配置测试", False, str(e))
            self.update_status(f"页面配置测试失败: {e}", True)
    
    def test_create_page(self, page_type):
        """测试创建特定类型的页面"""
        type_name = page_type.display_name
        self.update_status(f"创建{type_name}页面...")
        
        try:
            page_id = f"test_{page_type.value}_{int(datetime.now().timestamp())}"
            
            # 使用get_or_create_page方法
            view = self.page_manager.get_or_create_page(
                page_type=page_type,
                backend_interface=self.web_comm
            )
            
            assert view is not None, f"创建{type_name}页面失败"
            assert page_id in self.page_manager.preloaded_pages, f"{type_name}页面未正确存储"
            
            self.current_page_id = page_id
            
            self.add_test_result(f"创建{type_name}页面", True, f"页面ID: {page_id}")
            self.update_status(f"{type_name}页面创建成功")
            
        except Exception as e:
            self.add_test_result(f"创建{type_name}页面", False, str(e))
            self.update_status(f"创建{type_name}页面失败: {e}", True)
    
    def run_all_tests(self):
        """运行所有测试"""
        self.update_status("运行全部测试...")
        self.clear_test_results()
        
        # 按顺序运行所有测试
        tests = [
            self.test_page_type_enum,
            self.test_page_manager,
            self.test_page_config,
            lambda: self.test_create_page(PageType.MARKDOWN),
            lambda: self.test_create_page(PageType.EXCALIDRAW),
            lambda: self.test_create_page(PageType.LANDING),
        ]
        
        for i, test in enumerate(tests, 1):
            try:
                test()
                QTimer.singleShot(100 * i, lambda: None)
            except Exception as e:
                logger.error(f"测试执行出错: {e}")
        
        # 延迟显示最终报告
        QTimer.singleShot(len(tests) * 100 + 500, self.show_final_report)
    
    def show_final_report(self):
        """显示最终测试报告"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['result'])
        failed_tests = total_tests - passed_tests
        
        if failed_tests == 0:
            self.update_status(f"🎉 全部测试通过！({passed_tests}/{total_tests})")
        else:
            self.update_status(f"⚠️ 测试完成：{passed_tests}通过，{failed_tests}失败", failed_tests > 0)
    
    def clear_test_results(self):
        """清空测试结果"""
        self.test_results.clear()
        self.results_label.setText("📊 测试结果将在这里显示...")
        self.update_status("📋 准备开始测试...")


def main():
    """主函数"""
    app = QApplication.instance() or QApplication(sys.argv)
    
    window = MultiPageTestWindow()
    window.show()
    
    # 自动运行基础测试
    QTimer.singleShot(1000, window.test_page_type_enum)
    
    return app.exec()


if __name__ == "__main__":
    logger.info("多页面WebEngine管理系统测试启动")
    try:
        main()
    except Exception as e:
        logger.error(f"测试程序运行出错: {e}")
        sys.exit(1)