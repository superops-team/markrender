#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QuickPick树形结构增删改查测试文件（修复版）
用于验证和修复树形结构的增删改查bug
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QSplitter
from PySide6.QtCore import Qt
from app.quickpick.panel import QuickPickPanel
from db.markrender_manager import MarkRenderManager
from utils.logger_utils import setup_logger

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuickPick树形结构增删改查测试（修复版）")
        self.setGeometry(100, 100, 1000, 700)
        
        # 设置日志
        setup_logger()
        
        # 初始化数据库管理器
        self.markrender_manager = MarkRenderManager()
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 创建测试面板
        test_panel = QWidget()
        test_layout = QVBoxLayout(test_panel)
        
        # 创建测试按钮
        self.create_test_buttons(test_layout)
        
        # 创建日志显示区域
        self.log_display = QTextEdit()
        self.log_display.setMaximumHeight(200)
        self.log_display.setReadOnly(True)
        test_layout.addWidget(self.log_display)
        
        # 创建QuickPick面板
        self.quickpick_panel = QuickPickPanel(self.markrender_manager, self)
        
        # 添加到分割器
        splitter.addWidget(test_panel)
        splitter.addWidget(self.quickpick_panel)
        splitter.setSizes([300, 700])  # 设置初始大小
        
        # 设置主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(splitter)

    def create_test_buttons(self, layout):
        """创建测试按钮"""
        # 创建测试数据按钮
        create_test_data_btn = QPushButton("1. 创建测试数据")
        create_test_data_btn.clicked.connect(self.create_test_data)
        layout.addWidget(create_test_data_btn)
        
        # 验证数据按钮
        validate_data_btn = QPushButton("2. 验证数据")
        validate_data_btn.clicked.connect(self.validate_data)
        layout.addWidget(validate_data_btn)
        
        # 测试编辑功能按钮
        test_edit_btn = QPushButton("3. 测试编辑功能")
        test_edit_btn.clicked.connect(self.test_edit_function)
        layout.addWidget(test_edit_btn)
        
        # 验证编辑后数据按钮
        validate_after_edit_btn = QPushButton("4. 验证编辑后数据")
        validate_after_edit_btn.clicked.connect(self.validate_after_edit)
        layout.addWidget(validate_after_edit_btn)
        
        # 清理测试数据按钮
        cleanup_test_data_btn = QPushButton("5. 清理测试数据")
        cleanup_test_data_btn.clicked.connect(self.cleanup_test_data)
        layout.addWidget(cleanup_test_data_btn)
        
        # 刷新面板按钮
        refresh_panel_btn = QPushButton("刷新面板")
        refresh_panel_btn.clicked.connect(self.refresh_panel)
        layout.addWidget(refresh_panel_btn)

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
                order=0,
                icon_type="folder",
                icon_color="#FF0000",
                display_name="测试根节点显示名"
            )
            self.log(f"创建根节点，ID: {root_id}")
            
            # 创建子节点1
            child1_id = self.markrender_manager.save_item(
                title="测试子节点1",
                content="这是测试子节点1的内容",
                page_type="markdown",
                parent_id=root_id,
                level=1,
                order=0,
                icon_type="textarea",
                icon_color="#00FF00",
                display_name="测试子节点1显示名"
            )
            self.log(f"创建子节点1，ID: {child1_id}")
            
            # 创建子节点2
            child2_id = self.markrender_manager.save_item(
                title="测试子节点2",
                content="这是测试子节点2的内容",
                page_type="excalidraw",
                parent_id=root_id,
                level=1,
                order=1,
                icon_type="excalidraw",
                icon_color="#0000FF",
                display_name="测试子节点2显示名"
            )
            self.log(f"创建子节点2，ID: {child2_id}")
            
            # 创建子节点2的子节点
            grandchild_id = self.markrender_manager.save_item(
                title="测试孙节点",
                content="这是测试孙节点的内容",
                page_type="markdown",
                parent_id=child2_id,
                level=2,
                order=0,
                icon_type="book",
                icon_color="#FFFF00",
                display_name="测试孙节点显示名"
            )
            self.log(f"创建孙节点，ID: {grandchild_id}")
            
            # 刷新QuickPick面板
            self.refresh_panel()
            
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

    def test_edit_function(self):
        """测试编辑功能"""
        self.log("请在QuickPick面板中右键点击'测试子节点1'，选择'编辑'选项，然后：")
        self.log("1. 修改标题为'已修改的测试子节点1'")
        self.log("2. 添加标签'test,modified'")
        self.log("3. 修改图标类型为'gear'")
        self.log("4. 修改图标颜色为'#FF00FF'")
        self.log("5. 修改显示名称为'已修改的显示名'")
        self.log("6. 修改页面类型为'excalidraw'")
        self.log("7. 点击'保存设置'按钮")
        self.log("完成后点击'验证编辑后数据'按钮")

    def validate_after_edit(self):
        """验证编辑后数据"""
        try:
            # 获取完整树形结构
            tree_data = self.markrender_manager.get_full_tree()
            
            # 查找测试子节点1
            def find_test_node(nodes):
                for node in nodes:
                    if node.get('title') == '已修改的测试子节点1':
                        return node
                    if 'children' in node and node['children']:
                        result = find_test_node(node['children'])
                        if result:
                            return result
                return None
            
            test_node = find_test_node(tree_data)
            
            if test_node:
                self.log("找到已修改的测试节点:")
                self.log(f"  标题: {test_node.get('title')}")
                self.log(f"  标签: {test_node.get('tags')}")
                self.log(f"  图标类型: {test_node.get('icon_type')}")
                self.log(f"  图标颜色: {test_node.get('icon_color')}")
                self.log(f"  显示名称: {test_node.get('display_name')}")
                self.log(f"  页面类型: {test_node.get('page_type')}")
                
                # 验证字段是否正确更新
                expected_values = {
                    'title': '已修改的测试子节点1',
                    'tags': 'test,modified',
                    'icon_type': 'gear',
                    'icon_color': '#FF00FF',
                    'display_name': '已修改的显示名',
                    'page_type': 'excalidraw'
                }
                
                all_correct = True
                for field, expected_value in expected_values.items():
                    actual_value = test_node.get(field)
                    if actual_value != expected_value:
                        self.log(f"  字段 {field} 不匹配: 期望 '{expected_value}', 实际 '{actual_value}'")
                        all_correct = False
                
                if all_correct:
                    self.log("所有字段都正确更新！")
                else:
                    self.log("部分字段未正确更新，请检查编辑功能。")
            else:
                self.log("未找到已修改的测试节点，请确保已完成编辑操作。")
                
            # 刷新面板以显示更新
            self.refresh_panel()
            
        except Exception as e:
            self.log(f"验证编辑后数据失败: {e}")

    def cleanup_test_data(self):
        """清理测试数据"""
        try:
            # 获取所有包含"测试"的项目
            test_items = self.markrender_manager.search_item("测试")
            
            # 删除测试项目
            deleted_count = 0
            for item in test_items:
                if self.markrender_manager.delete_item(item.id):
                    deleted_count += 1
                    
            self.log(f"已删除 {deleted_count} 个测试项目")
            
            # 刷新QuickPick面板
            self.refresh_panel()
            
            self.log("测试数据清理完成")
        except Exception as e:
            self.log(f"清理测试数据失败: {e}")

    def refresh_panel(self):
        """刷新面板"""
        try:
            self.quickpick_panel.load_quickpick_items()
            self.log("面板已刷新")
        except Exception as e:
            self.log(f"刷新面板失败: {e}")

    def log(self, message):
        """记录日志"""
        self.log_display.append(message)
        print(message)
        
        # 自动滚动到底部
        self.log_display.verticalScrollBar().setValue(self.log_display.verticalScrollBar().maximum())

def main():
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()