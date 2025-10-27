#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QuickPick树形结构增删改查测试文件
用于验证和修复树形结构的增删改查bug
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit
from PySide6.QtCore import Qt
from app.quickpick.panel import QuickPickPanel
from db.markrender_manager import MarkRenderManager
from utils.logger_utils import setup_logger

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuickPick树形结构增删改查测试")
        self.setGeometry(100, 100, 800, 600)
        
        # 设置日志
        setup_logger()
        
        # 初始化数据库管理器
        self.markrender_manager = MarkRenderManager()
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        
        # 创建测试按钮
        self.create_test_buttons(layout)
        
        # 创建QuickPick面板
        self.quickpick_panel = QuickPickPanel(self.markrender_manager, self)
        layout.addWidget(self.quickpick_panel)
        
        # 创建日志显示区域
        self.log_display = QTextEdit()
        self.log_display.setMaximumHeight(100)
        self.log_display.setReadOnly(True)
        layout.addWidget(self.log_display)
        
        # 设置当前项属性
        self.current_item = None

    def create_test_buttons(self, layout):
        """创建测试按钮"""
        button_layout = QVBoxLayout()
        
        # 创建测试数据按钮
        create_test_data_btn = QPushButton("创建测试数据")
        create_test_data_btn.clicked.connect(self.create_test_data)
        button_layout.addWidget(create_test_data_btn)
        
        # 验证数据按钮
        validate_data_btn = QPushButton("验证数据")
        validate_data_btn.clicked.connect(self.validate_data)
        button_layout.addWidget(validate_data_btn)
        
        # 清理测试数据按钮
        cleanup_test_data_btn = QPushButton("清理测试数据")
        cleanup_test_data_btn.clicked.connect(self.cleanup_test_data)
        button_layout.addWidget(cleanup_test_data_btn)
        
        layout.addLayout(button_layout)

    def create_test_data(self):
        """创建测试数据"""
        try:
            # 创建根节点
            root_id = self.markrender_manager.save_item(
                title="测试根节点",
                content="这是测试根节点的内容",
                page_type="markdown",
                is_folder=1,
                level=0,
                order=0
            )
            
            # 创建子节点1
            child1_id = self.markrender_manager.save_item(
                title="测试子节点1",
                content="这是测试子节点1的内容",
                page_type="markdown",
                parent_id=root_id,
                level=1,
                order=0
            )
            
            # 创建子节点2
            child2_id = self.markrender_manager.save_item(
                title="测试子节点2",
                content="这是测试子节点2的内容",
                page_type="markdown",
                parent_id=root_id,
                level=1,
                order=1
            )
            
            # 创建子节点2的子节点
            grandchild_id = self.markrender_manager.save_item(
                title="测试孙节点",
                content="这是测试孙节点的内容",
                page_type="markdown",
                parent_id=child2_id,
                level=2,
                order=0
            )
            
            # 刷新QuickPick面板
            self.quickpick_panel.load_quickpick_items()
            
            self.log("测试数据创建成功")
        except Exception as e:
            self.log(f"创建测试数据失败: {e}")

    def validate_data(self):
        """验证数据"""
        try:
            # 获取完整树形结构
            tree_data = self.markrender_manager.get_full_tree()
            
            # 验证树形结构
            self.log(f"树形结构节点总数: {len(tree_data)}")
            
            def validate_tree_node(node, level=0):
                indent = "  " * level
                self.log(f"{indent}节点: {node.get('title', 'Unknown')} (ID: {node.get('id', 'Unknown')})")
                self.log(f"{indent}  层级: {node.get('level', 'Unknown')}")
                self.log(f"{indent}  排序: {node.get('order', 'Unknown')}")
                self.log(f"{indent}  父ID: {node.get('parent_id', 'None')}")
                self.log(f"{indent}  是否文件夹: {node.get('is_folder', 'Unknown')}")
                self.log(f"{indent}  图标类型: {node.get('icon_type', 'None')}")
                self.log(f"{indent}  图标路径: {node.get('icon_path', 'None')}")
                self.log(f"{indent}  图标颜色: {node.get('icon_color', 'None')}")
                self.log(f"{indent}  显示名称: {node.get('display_name', 'None')}")
                self.log(f"{indent}  页面类型: {node.get('page_type', 'None')}")
                
                # 验证必要字段是否存在
                required_fields = ['id', 'title', 'level', 'order', 'parent_id', 'is_folder']
                for field in required_fields:
                    if field not in node:
                        self.log(f"{indent}  缺少必要字段: {field}")
                
                # 递归验证子节点
                if 'children' in node and node['children']:
                    for child in node['children']:
                        validate_tree_node(child, level + 1)
            
            # 验证每个顶层节点
            for node in tree_data:
                validate_tree_node(node)
                
            self.log("数据验证完成")
        except Exception as e:
            self.log(f"验证数据失败: {e}")

    def cleanup_test_data(self):
        """清理测试数据"""
        try:
            # 获取所有包含"测试"的项目
            test_items = self.markrender_manager.search_item("测试")
            
            # 删除测试项目
            for item in test_items:
                self.markrender_manager.delete_item(item.id)
                
            # 刷新QuickPick面板
            self.quickpick_panel.load_quickpick_items()
            
            self.log("测试数据清理完成")
        except Exception as e:
            self.log(f"清理测试数据失败: {e}")

    def log(self, message):
        """记录日志"""
        self.log_display.append(message)
        print(message)

def main():
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()