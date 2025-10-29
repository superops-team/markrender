# -*- coding: utf-8 -*-
"""
历史记录面板组件
用于显示文档的编辑历史记录
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QListWidget, QListWidgetItem, QFrame, QLineEdit, QSizePolicy, QAbstractItemView, QPushButton
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QFont, QIcon
from app.preference.style_constants import (
    NEUTRAL_200, NEUTRAL_300, NEUTRAL_500, NEUTRAL_700, 
    PRIMARY_500, SPACING_SM, SPACING_MD, RADIUS_MD,
    FONT_SIZE_MD, FONT_SIZE_SM
)
from utils.logger_utils import logger
from utils.path import get_icon_path
from app.preference import AppStyle
from app.history.history_item import HistoryItemWidget


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
        self.all_history_records = []  # 存储所有历史记录
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        # 应用Robin Williams设计原则：
        # 1. 亲密性：相关元素组织在一起
        # 2. 对齐：确保元素有清晰的对齐方式
        # 3. 重复：在整个设计中重复视觉元素
        # 4. 对比：使用对比吸引注意力
        main_layout.setContentsMargins(8, 8, 8, 8)  # 统一边距
        main_layout.setSpacing(12)  # 增加间距以增强亲密性原则
        
        
        # 添加搜索框和刷新按钮的容器
        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(SPACING_SM)
        
        # 刷新按钮
        self.refresh_button = QPushButton()
        self.refresh_button.setFixedSize(24, 24)
        self.refresh_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {NEUTRAL_200};
                border: 1px solid {NEUTRAL_300};
                border-radius: {RADIUS_MD}px;
                icon-size: 16px;
                font-weight: bold;
                color: {NEUTRAL_700};
            }}
            QPushButton:hover {{
                background-color: {NEUTRAL_300};
            }}
            QPushButton:pressed {{
                background-color: {NEUTRAL_500};
            }}
        """)
        # 设置刷新图标（使用Unicode字符作为简单图标）
        self.refresh_button.setText("↻")
        self.refresh_button.clicked.connect(self.refresh_history)
        search_layout.addWidget(self.refresh_button)
        
        # 搜索框
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("搜索历史记录...")
        self.search_box.setStyleSheet(f"""
            QLineEdit {{
                padding: {SPACING_SM}px;
                border: 1px solid {NEUTRAL_200};
                border-radius: {RADIUS_MD}px;
                background-color: white;
                font-size: {FONT_SIZE_SM}px;
            }}
            QLineEdit:focus {{
                border-color: {PRIMARY_500};
                outline: none;
            }}
        """)
        self.search_box.textChanged.connect(self.filter_history)
        search_layout.addWidget(self.search_box)
        
        main_layout.addLayout(search_layout)
        
        # 历史记录列表（应用亲密性原则：列表与标题紧密组织）
        self.history_list = QListWidget()
        # 设置选择模式
        self.history_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        # 应用重复原则：使用与quickpick一致的间距
        self.history_list.setSpacing(SPACING_SM)
        # 禁用水平滚动条
        self.history_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # 设置垂直滚动模式
        self.history_list.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        # 设置统一的尺寸策略
        self.history_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # 使用统一的样式系统
        self.history_list.setStyleSheet(self.app_style.get_history_panel())
        self.history_list.setUniformItemSizes(True)  # 确保项大小一致
        
        # 连接信号
        self.history_list.itemClicked.connect(self.on_history_item_clicked)
        
        main_layout.addWidget(self.history_list)
        
        # 简化整体样式，与全局设计保持一致
        self.setStyleSheet('''
            HistoryPanel {
                background-color: white;
                border: none;
            }
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
            # 获取历史记录
            history_records = self.history_manager.get_change_history(item_id)
            
            # 按时间倒序排列（最新的在前面）
            history_records.sort(key=lambda x: getattr(x, 'change_at', None) or getattr(x, 'id', 0), reverse=True)
            
            # 保存所有历史记录用于搜索
            self.all_history_records = history_records
            
            # 添加到列表
            self._populate_history_list(history_records)
                
            logger.info(f"加载了 {len(history_records)} 条历史记录")
            
        except Exception as e:
            logger.error(f"加载历史记录失败: {e}")
            
    def _populate_history_list(self, history_records):
        """填充历史记录列表"""
        self.history_list.clear()
        for record in history_records:
            item_widget = HistoryItemWidget(record)
            list_item = QListWidgetItem(self.history_list)
            list_item.setData(Qt.ItemDataRole.UserRole, record)
            # 使用固定高度值，确保所有行对齐一致
            list_item.setSizeHint(QSize(0, 48))
            self.history_list.setItemWidget(list_item, item_widget)
            
    def filter_history(self, search_text):
        """根据搜索文本筛选历史记录"""
        if not search_text:
            # 如果搜索文本为空，显示所有记录
            self._populate_history_list(self.all_history_records)
            return
            
        # 筛选匹配的记录
        filtered_records = []
        search_text = search_text.lower()
        
        for record in self.all_history_records:
            # 检查变更类型
            change_type = getattr(record, 'change_type', '')
            if change_type and search_text in change_type.lower():
                filtered_records.append(record)
                continue
                
            # 检查变更原因
            change_reason = getattr(record, 'change_reason', '')
            if change_reason and search_text in change_reason.lower():
                filtered_records.append(record)
                continue
                
            # 检查变更人
            change_by = getattr(record, 'change_by', '')
            if change_by and search_text in change_by.lower():
                filtered_records.append(record)
                continue
                
            # 检查内容（仅对内容变更类型）
            if change_type in ['content_create', 'content_update']:
                old_content = getattr(record, 'old_content', '') or ''
                new_content = getattr(record, 'new_content', '') or ''
                if search_text in old_content.lower() or search_text in new_content.lower():
                    filtered_records.append(record)
                    continue
                    
        self._populate_history_list(filtered_records)
            
    def refresh_history(self):
        """刷新历史记录列表"""
        if self.current_item_id:
            self.load_history(self.current_item_id)
            # 清空搜索框
            self.search_box.clear()
            
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
                # 使用当前显示的记录而不是重新获取
                displayed_records = []
                for i in range(self.history_list.count()):
                    list_item = self.history_list.item(i)
                    record = list_item.data(Qt.ItemDataRole.UserRole)
                    if record:
                        displayed_records.append(record)
                        
                # 按时间倒序排列（最新的在前面）
                displayed_records.sort(key=lambda x: getattr(x, 'change_at', None) or getattr(x, 'id', 0), reverse=True)
                
                if 0 <= row < len(displayed_records):
                    selected_record = displayed_records[row]
                    self.history_selected.emit(selected_record)
        except Exception as e:
            logger.error(f"处理历史记录选择失败: {e}")
            
    def clear_history(self):
        """清空历史记录显示"""
        self.history_list.clear()
        self.current_item_id = None
        self.selected_item_widget = None  # 清除选中状态
        self.all_history_records = []  # 清除所有记录
        self.search_box.clear()  # 清空搜索框