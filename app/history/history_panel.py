# -*- coding: utf-8 -*-
"""
历史记录面板组件
用于显示文档的编辑历史记录
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QListWidget, QListWidgetItem, QFrame, QLineEdit, QSizePolicy, QAbstractItemView
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QFont, QIcon
from app.preference.style_constants import (
    NEUTRAL_50, NEUTRAL_100, NEUTRAL_200, NEUTRAL_300, NEUTRAL_500, NEUTRAL_700, NEUTRAL_900,
    PRIMARY_50, PRIMARY_500, SPACING_SM, SPACING_MD, SPACING_LG, SPACING_XS, RADIUS_MD, RADIUS_SM,
    FONT_SIZE_MD, FONT_SIZE_SM, FONT_SIZE_LG
)
from utils.logger_utils import logger
from utils.path import get_icon_path
from app.preference import AppStyle
from app.history.history_item import HistoryItemWidget
import datetime


class HistoryPanel(QWidget):
    """历史记录面板"""
    
    # 信号：当用户选择一个历史记录时发出
    history_selected = Signal(object)  # 传递历史记录对象
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.app_style = AppStyle()
        self.current_item_id = None
        self.history_manager = None
        self.selected_item_widget = None  # 当前选中的历史项
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        # 应用Robin Williams设计原则：
        # 1. 亲密性：相关元素组织在一起
        # 2. 对齐：确保元素有清晰的对齐方式
        # 3. 重复：在整个设计中重复视觉元素
        # 4. 对比：使用对比吸引注意力
        main_layout.setContentsMargins(12, 12, 12, 12)  # 增加边距以提供更好的视觉呼吸空间
        main_layout.setSpacing(16)  # 增加间距以增强亲密性原则
        
        # 添加标题标签（应用对比原则：标题使用更大字体和粗体）
        self.title_label = QLabel("编辑历史")
        self.title_label.setStyleSheet(f"""
            color: {NEUTRAL_900};
            font-size: {FONT_SIZE_LG}px;  # 使用更大的字体
            font-weight: 600;  # 半粗体
            padding: {SPACING_SM}px 0;
        """)
        # 应用对齐原则：标题左对齐
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        main_layout.addWidget(self.title_label)
        
        # 历史记录列表（应用亲密性原则：列表与标题紧密组织）
        self.history_list = QListWidget()
        # 设置选择模式
        self.history_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        # 应用重复原则：使用统一的间距
        self.history_list.setSpacing(SPACING_SM)
        # 禁用水平滚动条
        self.history_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # 设置垂直滚动模式
        self.history_list.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        # 设置统一的尺寸策略
        self.history_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # 使用统一的样式系统
        self.history_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {NEUTRAL_50};
                border: 1px solid {NEUTRAL_200};
                border-radius: {RADIUS_MD}px;
                padding: {SPACING_XS}px;
            }}
            QListWidget::item {{
                border: none;
                border-radius: {RADIUS_SM}px;
                padding: {SPACING_XS}px;
                margin-bottom: {SPACING_XS//2}px;
            }}
            QListWidget::item:last {{
                margin-bottom: 0px;
            }}
            QListWidget::item:hover {{
                background-color: {PRIMARY_50};
            }}
            QListWidget::item:selected {{
                background-color: rgba(245, 249, 255, 180);
            }}
        """)
        self.history_list.setUniformItemSizes(True)  # 确保项大小一致
        
        # 连接信号
        self.history_list.itemClicked.connect(self.on_history_item_clicked)
        
        main_layout.addWidget(self.history_list)
        
        # 应用TDesign设计原则优化整体样式
        self.setStyleSheet(f'''
            HistoryPanel {{
                background-color: {NEUTRAL_50};
                border: none;
            }}
        ''')
        
    def set_history_manager(self, history_manager):
        """设置历史记录管理器"""
        self.history_manager = history_manager
        
    def load_history(self, item_id):
        """加载指定项目的歷史記錄"""
        if not self.history_manager or not item_id:
            return
            
        self.current_item_id = item_id
        self.history_list.clear()
        self.selected_item_widget = None  # 清除选中状态
        
        try:
            # 获取当前项目的最新详情
            current_item_detail = self.history_manager.get_detail(item_id)
            
            # 获取历史记录
            history_records = self.history_manager.get_change_history(item_id)
            
            # 创建当前版本的模拟历史记录对象
            if current_item_detail:
                # 创建一个模拟的历史记录对象，包含当前最新内容
                class MockHistoryRecord:
                    def __init__(self, item_detail):
                        self.change_type = 'current_version'  # 特殊的变更类型标识当前版本
                        self.change_at = item_detail.get('updated_at') or datetime.datetime.now()
                        self.new_content = item_detail.get('content', '')
                        self.title = item_detail.get('title', '')
                
                current_version_record = MockHistoryRecord(current_item_detail)
                # 将当前版本插入到历史记录列表的最前面
                history_records.insert(0, current_version_record)
            
            # 按时间倒序排列（最新的在前面）
            history_records.sort(key=lambda x: getattr(x, 'change_at', None) or getattr(x, 'id', 0), reverse=True)
            
            # 添加到列表
            for record in history_records:
                item_widget = HistoryItemWidget(record)
                list_item = QListWidgetItem(self.history_list)
                list_item.setData(Qt.ItemDataRole.UserRole, record)
                # 使用固定高度值，确保所有行对齐一致
                list_item.setSizeHint(QSize(0, 56))  # 与HistoryItemWidget高度保持一致
                self.history_list.setItemWidget(list_item, item_widget)
                
            logger.info(f"加载了 {len(history_records)} 条历史记录（包含当前版本）")
            
        except Exception as e:
            logger.error(f"加载历史记录失败: {e}")
            
    def on_history_item_clicked(self, item):
        """当用户点击历史记录项时"""
        # 获取对应的widget
        item_widget = self.history_list.itemWidget(item)
        
        # 确保无论如何都只有一个选中项
        # 遍历所有项，取消所有选中状态
        for i in range(self.history_list.count()):
            current_item = self.history_list.item(i)
            current_widget = self.history_list.itemWidget(current_item)
            # 类型检查：确保current_widget是HistoryItemWidget类型
            if current_widget and isinstance(current_widget, HistoryItemWidget):
                current_widget.set_selected(False)  # type: ignore
        
        # 设置当前项为选中状态
        if item_widget and isinstance(item_widget, HistoryItemWidget):
            item_widget.set_selected(True)
            self.selected_item_widget = item_widget
            
        # 获取对应的历史记录对象
        row = self.history_list.row(item)
        try:
            if self.history_manager and self.current_item_id:
                # 获取当前项目的最新详情
                current_item_detail = self.history_manager.get_detail(self.current_item_id)
                
                # 获取历史记录
                history_records = self.history_manager.get_change_history(self.current_item_id)
                
                # 创建当前版本的模拟历史记录对象
                if current_item_detail:
                    # 创建一个模拟的历史记录对象，包含当前最新内容
                    class MockHistoryRecord:
                        def __init__(self, item_detail):
                            self.change_type = 'current_version'  # 特殊的变更类型标识当前版本
                            self.change_at = item_detail.get('updated_at') or datetime.datetime.now()
                            self.new_content = item_detail.get('content', '')
                            self.title = item_detail.get('title', '')
                    
                    current_version_record = MockHistoryRecord(current_item_detail)
                    # 将当前版本插入到历史记录列表的最前面
                    history_records.insert(0, current_version_record)
                
                # 按时间倒序排列（最新的在前面）
                history_records.sort(key=lambda x: getattr(x, 'change_at', None) or getattr(x, 'id', 0), reverse=True)
                
                if 0 <= row < len(history_records):
                    selected_record = history_records[row]
                    self.history_selected.emit(selected_record)
        except Exception as e:
            logger.error(f"处理历史记录选择失败: {e}")
            
    def clear_history(self):
        """清空历史记录显示"""
        self.history_list.clear()
        self.current_item_id = None
        self.selected_item_widget = None  # 清除选中状态