from PySide6.QtWidgets import QStatusBar, QLabel, QToolButton, QHBoxLayout, QWidget, QSizePolicy, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from app.preference import AppStyle  # 新增导入
from utils.path import get_icon_path
from app.preference.style_constants import (
    NEUTRAL_300, SPACING_XS, PRIMARY_100, PRIMARY_200, PRIMARY_600,
    NEUTRAL_100, NEUTRAL_200, NEUTRAL_700, FONT_SIZE_SM
)

class StatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent  # 保存主窗口引用
        self.current_page_type = None  # 保存当前页面类型
        self.current_tags = ""  # 保存当前标签
        
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
        """刷新显示内容，包括page_type和tags"""
        # 清除现有标签
        while self.tags_layout.count() > 0:
            item = self.tags_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # 添加tag标签
        if self.current_tags:
            # 如果有tags，先添加page_type作为首个标签（如果存在）
            if self.current_page_type:
                page_type_widget = self._create_page_type_widget(self.current_page_type)
                self.tags_layout.addWidget(page_type_widget)
            
            # 然后添加tag标签
            tag_list = [tag.strip() for tag in self.current_tags.split(',') if tag.strip()]
            for tag in tag_list:
                tag_button = self._create_tag_widget(tag)
                self.tags_layout.addWidget(tag_button)
        elif self.current_page_type and self.current_page_type.strip():
            # 如果有page_type但没有tags，显示page_type的默认值作为标签
            display_text = self._get_page_type_display_text(self.current_page_type)
            page_type_widget = self._create_tag_widget(display_text)
            self.tags_layout.addWidget(page_type_widget)
        else:
            # 如果既没有page_type也没有tags，显示默认的md
            md_widget = self._create_tag_widget("md")
            self.tags_layout.addWidget(md_widget)

    def _get_page_type_display_text(self, page_type):
        """获取页面类型显示文本，根据默认值映射规则"""
        # 默认值映射规则
        default_mappings = {
            'markdown': 'md',
            'excalidraw': 'board'
        }
        return default_mappings.get(page_type.lower(), page_type.lower())

    def _create_page_type_widget(self, page_type):
        """创建页面类型标签，使用与edit_dialog一致的颜色映射但适应statusbar"""
        # 导入颜色映射
        from app.quickpick.item import QuickPickItemDelegate
        from PySide6.QtGui import QColor
        
        delegate = QuickPickItemDelegate()
        type_color = delegate.tag_color_map.get(page_type.lower(), delegate.default_color)
        
        # 确保type_color是QColor对象
        if isinstance(type_color, QColor):
            # 将QColor转换为CSS颜色字符串
            bg_color = f'rgb({type_color.red()}, {type_color.green()}, {type_color.blue()})'
            # 创建稍深的边框颜色（降低亮度）
            border_color = f'rgb({max(0, type_color.red()-20)}, {max(0, type_color.green()-20)}, {max(0, type_color.blue()-20)})'
        else:
            # 如果不是QColor对象，使用默认颜色
            bg_color = "#6B7280"  # NEUTRAL_500
            border_color = "#4B5563"  # NEUTRAL_600
        
        # 创建标签按钮
        type_button = QPushButton(page_type.upper())
        type_button.setFlat(True)
        type_button.setEnabled(False)
        type_button.setStyleSheet(
            f"QPushButton {{"
            f"background-color: {bg_color};"
            f"border: 1px solid {border_color};"
            f"border-radius: 14px;"  # 与tag标签保持一致的圆角
            f"color: white;"
            f"padding: 4px 10px;"  # 与tag标签保持一致的内边距
            f"font-size: {FONT_SIZE_SM}px;"
            f"font-weight: 500;"
            f"text-align: center;"
            f"min-height: 18px;"  # 与tag标签保持一致的高度
            f"}}"
            f"QPushButton:disabled {{"
            f"background-color: {bg_color};"
            f"color: white;"
            f"border: 1px solid {border_color};"
            f"}}"
        )
        # 设置属性以确保样式生效
        type_button.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        # 设置对象名称以提高样式优先级
        type_button.setObjectName("status_page_type_button")
        return type_button

    def _create_tag_widget(self, tag):
        """创建标签按钮，样式与edit_dialog保持一致但适应statusbar"""
        tag_button = QPushButton(tag)
        tag_button.setFlat(True)
        tag_button.setEnabled(False)
        # 保持与edit_dialog一致的圆角样式，但调整尺寸以适应statusbar
        tag_button.setStyleSheet(
            f"QPushButton {{"
            f"background-color: {NEUTRAL_100};"
            f"border: 1px solid {NEUTRAL_200};"
            f"border-radius: 14px;"  # 保持明显的圆角效果
            f"color: {NEUTRAL_700};"
            f"padding: 4px 10px;"  # 适当调整内边距
            f"font-size: {FONT_SIZE_SM}px;"
            f"font-weight: 500;"
            f"text-align: center;"
            f"min-height: 18px;"  # 适当调整最小高度
            f"}}"
            f"QPushButton:disabled {{"
            f"background-color: {NEUTRAL_100};"
            f"color: {NEUTRAL_700};"
            f"border: 1px solid {NEUTRAL_200};"
            f"}}"
        )
        # 设置属性以确保样式生效
        tag_button.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        # 设置对象名称以提高样式优先级
        tag_button.setObjectName("status_tag_button")
        return tag_button

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