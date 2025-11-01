from PySide6.QtWidgets import QStatusBar, QLabel, QToolButton, QHBoxLayout, QWidget, QSizePolicy, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, Signal
from app.preference import AppStyle  # 新增导入
from utils.path import get_icon_path
from app.preference.style_constants import (
    NEUTRAL_300, SPACING_XS, PRIMARY_100, PRIMARY_200, PRIMARY_400, PRIMARY_500, PRIMARY_600,
    NEUTRAL_100, NEUTRAL_200, NEUTRAL_700, FONT_SIZE_SM
)

class StatusBar(QStatusBar):
    # 新增信号，用于通知quickpick面板进行标签过滤
    tag_selected = Signal(str)  # 发送选中的标签文本
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent  # 保存主窗口引用
        self.current_page_type = None  # 保存当前页面类型
        self.current_tags = ""  # 保存当前标签
        self.selected_tag = None  # 保存当前选中的标签
        self.tag_buttons = []  # 保存所有标签按钮的引用
        
        # 创建左侧的标签列表
        self.tags_layout = QHBoxLayout()
        self.tags_layout.setContentsMargins(10, 0, 10, 0)
        self.tags_layout.setSpacing(8)
        self.tags_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)  # 垂直居中
        self.tags_container = QWidget()
        self.tags_container.setLayout(self.tags_layout)
        
        # 移除标签标题，只保留标签本身
        
        # 创建右侧容器，包含历史按钮
        self.right_container = QWidget()
        self.right_layout = QHBoxLayout(self.right_container)
        self.right_layout.setContentsMargins(0, 0, 10, 0)
        self.right_layout.setSpacing(5)
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)  # 垂直居中
        
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

    def set_page_type(self, page_type):
        """设置页面类型标签
        
        Args:
            page_type: 页面类型字符串
        """
        self.current_page_type = page_type
        # 重新渲染标签以确保page_type标签正确显示
        self._refresh_display()

    def update_tags(self, tags):
        """更新标签列表
        
        Args:
            tags: 标签字符串，用逗号分隔
        """
        self.current_tags = tags
        # 重新渲染标签以确保page_type标签正确显示
        self._refresh_display()

    def _refresh_display(self):
        """刷新显示内容，包括page_type和tags，所有标签统一使用灰色，支持点击互斥选中"""
        # 清除现有标签
        while self.tags_layout.count() > 0:
            item = self.tags_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # 清空标签按钮列表
        self.tag_buttons = []
        
        # 添加tag标签
        all_tags = []
        
        # 始终将page_type作为第一个标签（如果存在）
        if self.current_page_type and self.current_page_type.strip():
            all_tags.append(self.current_page_type.lower())
        
        # 添加用户自定义的tags
        if self.current_tags:
            user_tags = [tag.strip() for tag in self.current_tags.split(',') if tag.strip()]
            all_tags.extend(user_tags)
        
        # 如果没有任何标签，显示默认的markdown
        if not all_tags:
            all_tags.append("markdown")
        
        # 为所有标签创建按钮，统一使用灰色样式，支持点击
        for tag in all_tags:
            # 创建可点击的标签按钮
            tag_button = self._create_clickable_tag_widget(tag)
            self.tags_layout.addWidget(tag_button)
            self.tag_buttons.append((tag, tag_button))
    
    def _create_clickable_tag_widget(self, tag):
        """创建可点击的标签按钮，支持点击选中/取消选中，互斥关系，选中时显示蓝色"""
        tag_button = QPushButton(tag)
        tag_button.setFlat(True)
        tag_button.setEnabled(True)  # 启用按钮以支持点击
        
        # 连接点击信号
        tag_button.clicked.connect(lambda checked=False, t=tag: self._on_tag_clicked(t))
        
        # 初始样式设置为灰色
        is_selected = (tag == self.selected_tag)
        self._update_tag_button_style(tag_button, is_selected)
        
        # 设置属性以确保样式生效
        tag_button.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        # 设置对象名称以提高样式优先级
        tag_button.setObjectName("status_tag_button")
        return tag_button
    
    def _update_tag_button_style(self, button, is_selected):
        """更新标签按钮样式，选中时显示蓝色，未选中时显示灰色"""
        if is_selected:
            # 选中状态：蓝色背景，白色文字
            bg_color = PRIMARY_500
            border_color = PRIMARY_600
            text_color = "white"
        else:
            # 未选中状态：灰色背景，灰色文字
            bg_color = NEUTRAL_100
            border_color = NEUTRAL_200
            text_color = NEUTRAL_700
        
        button.setStyleSheet(
            "QPushButton {" +
            f"background-color: {bg_color}; " +
            f"border: 1px solid {border_color}; " +
            "border-radius: 14px; " +
            f"color: {text_color}; " +
            "padding: 4px 10px; " +
            f"font-size: {FONT_SIZE_SM}px; " +
            "font-weight: 500; " +
            "text-align: center; " +
            "min-height: 18px; " +
            "}" +
            "QPushButton:hover {" +
            (f"background-color: {PRIMARY_400}; " +
             f"border-color: {PRIMARY_500}; " if is_selected else
             f"background-color: {NEUTRAL_200}; " +
             f"border-color: {NEUTRAL_300}; " ) +
            "}"
        )
    
    def _on_tag_clicked(self, tag):
        """处理标签点击事件，实现互斥选中，发送过滤信号"""
        # 如果点击的是当前选中的标签，则取消选中
        if tag == self.selected_tag:
            self.selected_tag = None
            # 发送空信号表示清除过滤
            self.tag_selected.emit("")
        else:
            # 选中新标签，取消之前的选中状态
            self.selected_tag = tag
            # 发送选中的标签文本作为过滤条件
            self.tag_selected.emit(tag)
        
        # 更新所有标签按钮的样式
        for t, button in self.tag_buttons:
            self._update_tag_button_style(button, t == self.selected_tag)
        
        # 如果主窗口存在quickpick面板，通知它进行过滤
        if self.main_window and hasattr(self.main_window, 'quickpick_panel'):
            try:
                # 调用quickpick面板的过滤方法
                # 这里假设quickpick_panel有一个filter_by_tag方法
                # 如果方法不存在，我们静默失败，因为这是一个优雅降级
                if hasattr(self.main_window.quickpick_panel, 'filter_by_tag'):
                    self.main_window.quickpick_panel.filter_by_tag(self.selected_tag)
            except Exception as e:
                print(f"过滤标签时出错: {e}")

    def toggle_history_panel(self):
        """切换历史记录面板显示状态"""
        try:
            # 直接通过主窗口引用访问历史面板
            if self.main_window and hasattr(self.main_window, 'history_panel'):
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
                    if self.main_window and hasattr(self.main_window, 'current_item') and self.main_window.current_item:
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