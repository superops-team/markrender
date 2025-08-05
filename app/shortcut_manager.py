"""
快捷键管理模块
用于捕获和处理各种快捷键操作
支持全局快捷键和局部快捷键管理
支持Windows和Mac平台差异化快捷键
"""
import json
import sys
from PySide6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QHBoxLayout, QPushButton, QFileDialog
from PySide6.QtCore import Signal, QObject, QSettings, Qt, QEvent
from PySide6.QtGui import QKeySequence, QShortcut
from utils import logger



class ShortcutManager(QObject):
    """全局快捷键管理器"""
    
    # 定义全局快捷键信号
    save_requested = Signal()
    save_all_requested = Signal()
    copy_requested = Signal()
    paste_requested = Signal()
    cut_requested = Signal()
    undo_requested = Signal()
    redo_requested = Signal()
    find_requested = Signal()
    replace_requested = Signal()
    new_file_requested = Signal()
    open_file_requested = Signal()
    export_requested = Signal()
    print_requested = Signal()
    close_tab_requested = Signal()
    next_tab_requested = Signal()
    prev_tab_requested = Signal()
    bold_requested = Signal()
    italic_requested = Signal()
    underline_requested = Signal()
    strikethrough_requested = Signal()
    insert_link_requested = Signal()
    insert_image_requested = Signal()
    insert_table_requested = Signal()
    insert_code_requested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.shortcuts = {}
        self.global_shortcuts = {}
        self.enabled = True
        self.settings = QSettings("MarkRender", "Shortcuts")
        self.setup_default_shortcuts()
        self.load_custom_shortcuts()
        
    def setup_default_shortcuts(self):
        """设置默认快捷键映射，根据平台自动调整"""
        # 检测当前平台
        is_mac = sys.platform == "darwin"
        
        # 根据平台选择修饰键
        ctrl_key = "Meta+" if is_mac else "Ctrl+"
        shift_key = "Shift+"
        
        self.default_shortcuts = {
            'save': f'{ctrl_key}S',
            'save_all': f'{ctrl_key}{shift_key}S',
            'copy': f'{ctrl_key}C',
            'paste': f'{ctrl_key}V',
            'cut': f'{ctrl_key}X',
            'undo': f'{ctrl_key}Z',
            'redo': f'{ctrl_key}Y',
            'find': f'{ctrl_key}F',
            'replace': f'{ctrl_key}H',
            'new_file': f'{ctrl_key}N',
            'open_file': f'{ctrl_key}O',
            'export': f'{ctrl_key}E',
            'print': f'{ctrl_key}P',
            'close_tab': f'{ctrl_key}W',
            'next_tab': f'{ctrl_key}Tab',
            'prev_tab': f'{ctrl_key}{shift_key}Tab',
            'bold': f'{ctrl_key}B',
            'italic': f'{ctrl_key}I',
            'underline': f'{ctrl_key}U',
            'strikethrough': f'{ctrl_key}{shift_key}S',
            'insert_link': f'{ctrl_key}K',
            'insert_image': f'{ctrl_key}{shift_key}I',
            'insert_table': f'{ctrl_key}T',
            'insert_code': f'{ctrl_key}{shift_key}C',
        }
        
    def get_platform_modifier(self):
        """获取当前平台的修饰键"""
        if sys.platform == "darwin":
            return Qt.MetaModifier
        else:
            return Qt.ControlModifier
            
    def handle_key_event(self, event, target_widget=None):
        """处理键盘事件，支持平台差异"""
        if not self.enabled:
            return False
            
        # 获取当前平台的修饰键
        platform_modifier = self.get_platform_modifier()
        
        # 定义快捷键映射
        key_combinations = {
            'copy': (platform_modifier, Qt.Key_C),
            'paste': (platform_modifier, Qt.Key_V),
            'cut': (platform_modifier, Qt.Key_X),
            'undo': (platform_modifier, Qt.Key_Z),
            'redo': (platform_modifier, Qt.Key_Y),
            'find': (platform_modifier, Qt.Key_F),
            'replace': (platform_modifier, Qt.Key_H),
            'bold': (platform_modifier, Qt.Key_B),
            'italic': (platform_modifier, Qt.Key_I),
            'underline': (platform_modifier, Qt.Key_U),
            'insert_link': (platform_modifier, Qt.Key_K),
            'insert_image': (platform_modifier | Qt.ShiftModifier, Qt.Key_I),
            'insert_table': (platform_modifier, Qt.Key_T),
            'insert_code': (platform_modifier | Qt.ShiftModifier, Qt.Key_C),
        }
        
        # Mac平台特殊处理strikethrough快捷键
        if sys.platform == "darwin":
            key_combinations['strikethrough'] = (platform_modifier | Qt.ShiftModifier, Qt.Key_S)
        else:
            key_combinations['strikethrough'] = (platform_modifier | Qt.ShiftModifier, Qt.Key_S)
            
        modifiers = event.modifiers()
        key = event.key()
        
        for action, (mod, k) in key_combinations.items():
            if modifiers == mod and key == k:
                self._emit_action_signal(action)
                return True
                
        return False
        
    def get_shortcut_display_name(self, action_name):
        """获取快捷键的显示名称，根据平台格式化"""
        shortcut = self.get_shortcut(action_name)
        if isinstance(shortcut, str):
            formatted = shortcut
        else:
            formatted = shortcut.toString()
            
        # 根据平台调整显示格式
        if sys.platform == "darwin":
            formatted = formatted.replace("Ctrl", "⌘")
            formatted = formatted.replace("Meta", "⌘")
            formatted = formatted.replace("Shift", "⇧")
            formatted = formatted.replace("Alt", "⌥")
        
        return formatted
        
    def register_shortcut(self, action_name, key_sequence, is_global=False):
        """注册快捷键
        
        Args:
            action_name: 操作名称
            key_sequence: 快捷键序列（字符串或QKeySequence）
            is_global: 是否为全局快捷键
        """
        if isinstance(key_sequence, str):
            key_sequence = QKeySequence(key_sequence)
            
        if is_global and self.parent():
            # 注册全局快捷键
            shortcut = QShortcut(key_sequence, self.parent())
            shortcut.setContext(Qt.ApplicationShortcut)
            self.global_shortcuts[action_name] = shortcut
            
            # 连接信号
            self._connect_global_shortcut(action_name, shortcut)
        else:
            # 注册局部快捷键
            self.shortcuts[action_name] = key_sequence
            
        logger.info(f"注册{'全局' if is_global else '局部'}快捷键: {action_name} -> {key_sequence.toString()}")
        
    def _connect_global_shortcut(self, action_name, shortcut):
        """连接全局快捷键信号"""
        signal_map = {
            'save': self.save_requested,
            'save_all': self.save_all_requested,
            'new_file': self.new_file_requested,
            'open_file': self.open_file_requested,
            'find': self.find_requested,
            'replace': self.replace_requested,
            'export': self.export_requested,
            'print': self.print_requested,
            'close_tab': self.close_tab_requested,
            'next_tab': self.next_tab_requested,
            'prev_tab': self.prev_tab_requested,
        }
        
        if action_name in signal_map:
            shortcut.activated.connect(signal_map[action_name])
            
    def get_shortcut(self, action_name):
        """获取指定操作的快捷键"""
        return self.shortcuts.get(action_name) or self.global_shortcuts.get(action_name)
        
    def get_all_shortcuts(self):
        """获取所有快捷键"""
        all_shortcuts = self.default_shortcuts.copy()
        all_shortcuts.update(self.shortcuts)
        return all_shortcuts
        
    def reset_shortcuts(self):
        """重置为默认快捷键"""
        self.shortcuts.clear()
        self.clear_all_global_shortcuts()
        self.setup_default_shortcuts()
        self.register_default_shortcuts()
        
    def register_default_shortcuts(self):
        """注册默认快捷键"""
        for action_name, key_sequence in self.default_shortcuts.items():
            if action_name in ['save', 'new_file', 'open_file', 'close_tab']:
                self.register_shortcut(action_name, key_sequence, is_global=True)
            else:
                self.register_shortcut(action_name, key_sequence)
                
    def clear_all_global_shortcuts(self):
        """清除所有全局快捷键"""
        for shortcut in self.global_shortcuts.values():
            if hasattr(shortcut, 'deleteLater'):
                shortcut.deleteLater()
        self.global_shortcuts.clear()
        
    def handle_key_event(self, event, target_widget=None):
        """处理键盘事件
        
        Args:
            event: 键盘事件
            target_widget: 目标控件
            
        Returns:
            bool: 是否已处理该事件
        """
        if not self.enabled:
            return False
            
        # 检查各个快捷键
        key_combinations = {
            'copy': (Qt.ControlModifier, Qt.Key_C),
            'paste': (Qt.ControlModifier, Qt.Key_V),
            'cut': (Qt.ControlModifier, Qt.Key_X),
            'undo': (Qt.ControlModifier, Qt.Key_Z),
            'redo': (Qt.ControlModifier, Qt.Key_Y),
            'find': (Qt.ControlModifier, Qt.Key_F),
            'replace': (Qt.ControlModifier, Qt.Key_H),
            'bold': (Qt.ControlModifier, Qt.Key_B),
            'italic': (Qt.ControlModifier, Qt.Key_I),
            'underline': (Qt.ControlModifier, Qt.Key_U),
            'insert_link': (Qt.ControlModifier, Qt.Key_K),
            'insert_image': (Qt.ControlModifier | Qt.ShiftModifier, Qt.Key_I),
            'insert_table': (Qt.ControlModifier, Qt.Key_T),
            'insert_code': (Qt.ControlModifier | Qt.ShiftModifier, Qt.Key_C),
        }
        
        modifiers = event.modifiers()
        key = event.key()
        
        for action, (mod, k) in key_combinations.items():
            if modifiers == mod and key == k:
                self._emit_action_signal(action)
                return True
                
        return False
        
    def _emit_action_signal(self, action_name):
        """发射对应的操作信号"""
        signal_map = {
            'copy': self.copy_requested,
            'paste': self.paste_requested,
            'cut': self.cut_requested,
            'undo': self.undo_requested,
            'redo': self.redo_requested,
            'find': self.find_requested,
            'replace': self.replace_requested,
            'bold': self.bold_requested,
            'italic': self.italic_requested,
            'underline': self.underline_requested,
            'strikethrough': self.strikethrough_requested,
            'insert_link': self.insert_link_requested,
            'insert_image': self.insert_image_requested,
            'insert_table': self.insert_table_requested,
            'insert_code': self.insert_code_requested,
        }
        
        if action_name in signal_map:
            signal_map[action_name].emit()
            logger.debug(f"触发快捷键操作: {action_name}")
            
    def set_enabled(self, enabled):
        """启用/禁用快捷键"""
        self.enabled = enabled
        
    def load_custom_shortcuts(self):
        """加载自定义快捷键配置"""
        try:
            custom_shortcuts = self.settings.value("custom_shortcuts", {})
            if isinstance(custom_shortcuts, dict):
                self.shortcuts.update(custom_shortcuts)
        except Exception as e:
            logger.error(f"加载自定义快捷键失败: {e}")
            
    def save_custom_shortcuts(self):
        """保存自定义快捷键配置"""
        try:
            self.settings.setValue("custom_shortcuts", self.shortcuts)
        except Exception as e:
            logger.error(f"保存自定义快捷键失败: {e}")
            
    def export_shortcuts_config(self, file_path):
        """导出快捷键配置到文件"""
        try:
            config = {
                'shortcuts': self.get_all_shortcuts(),
                'custom_shortcuts': self.shortcuts
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
                
            logger.info(f"快捷键配置已导出到: {file_path}")
            return True
        except Exception as e:
            logger.error(f"导出快捷键配置失败: {e}")
            return False
            
    def import_shortcuts_config(self, file_path):
        """从文件导入快捷键配置"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            if 'shortcuts' in config:
                self.shortcuts.update(config['shortcuts'])
            if 'custom_shortcuts' in config:
                self.shortcuts.update(config['custom_shortcuts'])
                
            logger.info(f"快捷键配置已从 {file_path} 导入")
            return True
        except Exception as e:
            logger.error(f"导入快捷键配置失败: {e}")
            return False


class ShortcutHandler(QObject):
    """局部快捷键处理器"""
    
    def __init__(self, widget, shortcut_manager):
        super().__init__(widget)
        self.widget = widget
        self.shortcut_manager = shortcut_manager
        self.widget.installEventFilter(self)
        
    def eventFilter(self, obj, event):
        """事件过滤器"""
        if event.type() == QEvent.KeyPress:
            if self.shortcut_manager.handle_key_event(event, self.widget):
                return True
        return super().eventFilter(obj, event)


class ShortcutDialog(QDialog):
    """快捷键配置对话框"""
    
    def __init__(self, shortcut_manager, parent=None):
        super().__init__(parent)
        self.shortcut_manager = shortcut_manager
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI"""
        self.setWindowTitle("快捷键设置")
        self.setModal(True)
        self.resize(400, 500)
        
        layout = QVBoxLayout(self)
        
        # 快捷键列表
        self.shortcut_list = QListWidget()
        self.load_shortcut_list()
        layout.addWidget(self.shortcut_list)
        
        # 按钮组
        button_layout = QHBoxLayout()
        
        self.reset_button = QPushButton("重置为默认值")
        self.reset_button.clicked.connect(self.reset_shortcuts)
        
        self.export_button = QPushButton("导出配置")
        self.export_button.clicked.connect(self.export_config)
        
        self.import_button = QPushButton("导入配置")
        self.import_button.clicked.connect(self.import_config)
        
        self.close_button = QPushButton("关闭")
        self.close_button.clicked.connect(self.accept)
        
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.import_button)
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
        
    def load_shortcut_list(self):
        """加载快捷键列表"""
        self.shortcut_list.clear()
        shortcuts = self.shortcut_manager.get_all_shortcuts()
        
        for action_name, key_sequence in shortcuts.items():
            item_text = f"{action_name}: {key_sequence}"
            self.shortcut_list.addItem(item_text)
            
    def reset_shortcuts(self):
        """重置快捷键"""
        self.shortcut_manager.reset_shortcuts()
        self.load_shortcut_list()
        
    def export_config(self):
        """导出配置"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出快捷键配置", "shortcuts.json", "JSON Files (*.json)"
        )
        if file_path:
            self.shortcut_manager.export_shortcuts_config(file_path)
            
    def import_config(self):
        """导入配置"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "导入快捷键配置", "", "JSON Files (*.json)"
        )
        if file_path:
            self.shortcut_manager.import_shortcuts_config(file_path)
            self.load_shortcut_list()


# 预定义的快捷键配置
SHORTCUT_CATEGORIES = {
    '文件操作': {
        'save': '保存',
        'save_all': '保存所有',
        'new_file': '新建文件',
        'open_file': '打开文件',
        'export': '导出',
        'print': '打印',
        'close_tab': '关闭标签页',
    },
    '编辑操作': {
        'copy': '复制',
        'paste': '粘贴',
        'cut': '剪切',
        'undo': '撤销',
        'redo': '重做',
        'find': '查找',
        'replace': '替换',
    },
    '格式化': {
        'bold': '粗体',
        'italic': '斜体',
        'underline': '下划线',
        'strikethrough': '删除线',
    },
    '插入': {
        'insert_link': '插入链接',
        'insert_image': '插入图片',
        'insert_table': '插入表格',
        'insert_code': '插入代码',
    },
    '导航': {
        'next_tab': '下一个标签页',
        'prev_tab': '上一个标签页',
    }
}