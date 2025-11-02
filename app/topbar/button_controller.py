from PySide6.QtWidgets import QWidget, QHBoxLayout, QToolButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from utils.path import get_icon_path

from PySide6.QtWidgets import QMenu  # 新增导入

class ButtonController(QWidget):
    def __init__(self, parent, quickpick_panel, editor_component):
        super().__init__(parent)
        self.main_window = parent  # 保存主窗口引用
        self.quickpick_panel = quickpick_panel
        self.editor_component = editor_component  # 可能是单个编辑器或标签页管理器
        # 添加选中状态标志，默认进入页面后为选中状态
        self.is_quickpick_selected = True
        self.is_history_selected = False  # 历史面板选中状态
        self.setup_buttons()

    def setup_buttons(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        # 控制 quickpick 面板显示/隐藏的按钮 - 使用样式常量
        from app.preference.style_constants import NEUTRAL_300, SPACING_XS
        self.quickpick_btn = QToolButton()
        # 初始设置为选中状态的图标
        self.quickpick_btn.setIcon(QIcon(get_icon_path('sidebar', True)))
        self.quickpick_btn.setToolTip('显示/隐藏快速选择面板')
        self.quickpick_btn.clicked.connect(self.toggle_quickpick_panel)
        self.quickpick_btn.setStyleSheet(f'''
            QToolButton {{
                border: none;
                padding: {SPACING_XS}px;
            }}
            QToolButton:hover {{
                background-color: {NEUTRAL_300};
            }}
        ''')
        self.quickpick_btn.setFixedSize(20, 20)  # 固定按钮大小
        layout.addWidget(self.quickpick_btn)

        # 历史记录按钮
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
        layout.addWidget(self.history_btn)

        # 确保进入页面后默认展示quickpick页面
        if not self.quickpick_panel.isVisible():
            self.quickpick_panel.show()

    def toggle_quickpick_panel(self):
        if self.quickpick_panel.isVisible():
            self.quickpick_panel.hide()
            # 未选中状态，使用普通图标
            self.quickpick_btn.setIcon(QIcon(get_icon_path('sidebar', False)))
            self.is_quickpick_selected = False
        else:
            self.quickpick_panel.show()
            # 选中状态，使用选中图标
            self.quickpick_btn.setIcon(QIcon(get_icon_path('sidebar', True)))
            self.is_quickpick_selected = True

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

    def get_current_editor(self):
        """获取当前编辑器实例"""
        # 如果是标签页管理器，返回当前标签页的编辑器
        if hasattr(self.editor_component, 'get_current_editor'):
            return self.editor_component.get_current_editor()
        # 如果是单个编辑器，直接返回
        return self.editor_component