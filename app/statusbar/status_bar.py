from PySide6.QtWidgets import QStatusBar, QLabel, QToolButton, QHBoxLayout, QWidget  # 修改导入语句
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from app.preference import AppStyle  # 新增导入
from utils.path import get_icon_path
from app.preference.style_constants import NEUTRAL_300, SPACING_XS

class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent  # 保存主窗口引用
        
        # 创建左侧的标签列表
        self.tags_layout = QHBoxLayout()
        self.tags_layout.setContentsMargins(10, 0, 10, 0)
        self.tags_layout.setSpacing(8)
        self.tags_container = QWidget()
        self.tags_container.setLayout(self.tags_layout)
        
        # 移除标签标题，只保留标签本身
        
        # 创建右侧容器，包含历史按钮
        self.right_container = QWidget()
        self.right_layout = QHBoxLayout(self.right_container)
        self.right_layout.setContentsMargins(0, 0, 10, 0)
        self.right_layout.setSpacing(5)
        
        # 创建历史记录按钮
        self.history_btn = QToolButton()
        self.history_btn.setIcon(QIcon(get_icon_path('history', False)))
        self.history_btn.setToolTip('显示/隐藏编辑历史')
        self.history_btn.clicked.connect(self.toggle_history_panel)
        self.history_btn.setStyleSheet(f'''
            QToolButton {{
                border: none;
                padding: {SPACING_XS}px;
            }}
            QToolButton:hover {{
                background-color: {NEUTRAL_300};
            }}
        ''')
        self.history_btn.setFixedSize(20, 20)  # 固定按钮大小
        
        # 添加历史按钮到右侧布局
        self.right_layout.addWidget(self.history_btn)
        
        # 添加组件到状态栏
        self.addWidget(self.tags_container)  # 左侧标签列表
        self.addPermanentWidget(self.right_container)  # 右侧历史按钮
        
        # 设置样式表
        self.setStyleSheet(AppStyle().get_status_bar())  # 新增样式表设置
        
        # 初始化历史状态
        self.is_history_selected = False

    def update_tags(self, tags):
        """更新标签列表
        
        Args:
            tags: 标签字符串，用逗号分隔
        """
        # 清除现有标签
        while self.tags_layout.count() > 0:  # 清除所有标签
            item = self.tags_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # 添加新标签
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            for tag in tag_list:
                tag_label = QLabel(f"{tag}")
                tag_label.setStyleSheet('''
                    background-color: #e8f3ff;
                    color: #1976d2;
                    padding: 2px 8px;
                    border-radius: 10px;
                    font-size: 11px;
                    border: 1px solid #b3d9ff;
                ''')
                self.tags_layout.addWidget(tag_label)
        else:
            # 如果没有标签，显示"无"消息
            no_tags_label = QLabel("无")
            no_tags_label.setStyleSheet("color: #999; font-size: 11px; font-style: italic;")
            self.tags_layout.addWidget(no_tags_label)
            
    def toggle_history_panel(self):
        """切换历史记录面板显示状态"""
        try:
            # 直接通过主窗口引用访问历史面板
            if hasattr(self.main_window, 'history_panel'):
                history_panel = self.main_window.history_panel
                if history_panel.isVisible():
                    history_panel.hide()
                    # 未选中状态，使用普通图标
                    self.history_btn.setIcon(QIcon(get_icon_path('history', False)))
                    self.is_history_selected = False
                else:
                    history_panel.show()
                    # 选中状态，使用选中图标
                    self.history_btn.setIcon(QIcon(get_icon_path('history', True)))
                    self.is_history_selected = True
                    # 如果当前有选中的项目，加载其历史记录
                    if hasattr(self.main_window, 'current_item') and self.main_window.current_item:
                        item_id = self.main_window.current_item.get('id')
                        if item_id:
                            history_panel.load_history(item_id)
            else:
                print("错误：未找到历史面板组件")
        except Exception as e:
            print(f"切换历史面板时出错: {e}")

    def show_message(self, message):
        self.showMessage(message, 3000)  # 显示消息 3 秒
        
    def set_main_window(self, main_window):
        """设置主窗口引用"""
        self.main_window = main_window