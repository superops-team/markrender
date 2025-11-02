from PySide6.QtWidgets import QTabWidget, QMenu, QWidget
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QAction, QIcon
from app.editor.editor import MarkRenderEditor
from utils.logger_utils import logger
from utils.path import get_icon_path
from app.preference import AppStyle


class TabManager(QTabWidget):
    """标签页管理器，支持多标签页编辑"""
    
    # 定义标签页关闭信号
    tab_closed = Signal(int)  # 传递关闭的标签页索引
    current_tab_changed = Signal(int)  # 传递当前标签页索引
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        self.app_style = AppStyle()
        
        # 设置标签页样式
        self.setStyleSheet(self.app_style.get_tab_style())
        
        # 配置标签页行为
        self.setTabsClosable(True)  # 允许关闭标签页
        self.setMovable(True)  # 允许拖拽标签页
        self.setDocumentMode(True)  # 使用文档模式，更紧凑的标签栏
        
        # 连接信号
        self.tabCloseRequested.connect(self.close_tab)
        self.currentChanged.connect(self.on_current_tab_changed)
        
        # 启用右键菜单
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
        # 存储标签页对应的编辑器实例
        self.editors = {}  # {tab_index: editor_instance}
        
    def add_tab_for_item(self, item_data):
        """为指定的quickpick项目添加标签页"""
        item_id = item_data.get('id')
        title = item_data.get('title', 'Unknown')
        page_type = item_data.get('page_type', 'markdown')
        
        # 检查是否已存在相同项目的标签页
        existing_index = self.find_tab_by_item_id(item_id)
        if existing_index != -1:
            # 如果已存在，直接切换到该标签页
            self.setCurrentIndex(existing_index)
            return existing_index
        
        # 创建新的编辑器实例
        editor = MarkRenderEditor(parent=self._parent)
        
        # 设置编辑器内容
        content = ""
        if self._parent and hasattr(self._parent, 'markrender_manager'):
            try:
                item_detail = self._parent.markrender_manager.get_detail(item_id)
                content = item_detail.get('content', '') if item_detail else ""
            except Exception as e:
                logger.error(f"获取项目内容失败: {e}")
        
        # 设置当前项目
        editor.set_current_item(item_id, page_type, content)
        
        # 根据page_type切换到正确的页面类型
        try:
            # 确保页面管理器已初始化
            if hasattr(editor, 'page_manager'):
                # 获取或创建对应类型的页面
                page_view = editor.page_manager.get_or_create_page(
                    page_type=page_type,
                    backend_interface=editor.backend_interface
                )
                
                if page_view:
                    # 切换到正确的页面类型
                    editor.page_manager.switch_to_page(page_type)
                    
                    # 设置页面内容
                    if content:
                        # 延迟设置内容，确保页面已完全加载
                        from PySide6.QtCore import QTimer
                        QTimer.singleShot(100, lambda: editor.set_text_content(content))
                else:
                    logger.error(f"无法创建 {page_type} 页面")
        except Exception as e:
            logger.error(f"切换页面类型失败: {e}")
        
        # 添加标签页
        icon_path = item_data.get('icon_path')
        # 处理icon_path为None的情况
        if not icon_path:
            icon_path = f'icons/file-{page_type}.svg'
        
        # 安全地处理图标路径
        try:
            icon_filename = icon_path.replace('icons/', '').replace('.svg', '') if icon_path else f'file-{page_type}'
            icon = QIcon(get_icon_path(icon_filename, selected=False))
        except Exception as e:
            logger.warning(f"加载图标失败，使用默认图标: {e}")
            icon = QIcon()  # 使用空图标
        
        tab_index = self.addTab(editor, icon, title)
        self.editors[tab_index] = editor
        
        # 设置标签页可关闭
        self.tabBar().setTabButton(tab_index, self.tabBar().ButtonPosition.RightSide, self.tabBar().tabButton(tab_index, self.tabBar().ButtonPosition.RightSide))
        
        # 切换到新标签页
        self.setCurrentIndex(tab_index)
        
        return tab_index
    
    def find_tab_by_item_id(self, item_id):
        """根据项目ID查找对应的标签页索引"""
        for index, editor in self.editors.items():
            if hasattr(editor, 'item') and editor.item.item_id == item_id:
                return index
        return -1
    
    def close_tab(self, index):
        """关闭指定索引的标签页"""
        if index < 0 or index >= self.count():
            return
            
        # 获取要关闭的编辑器
        editor = self.editors.get(index)
        if editor:
            # 保存编辑器内容
            try:
                editor.save_current_item()
            except Exception as e:
                logger.error(f"保存标签页内容失败: {e}")
            
            # 清理编辑器资源
            if hasattr(editor, '_cleanup_resources'):
                editor._cleanup_resources()
            
            # 从编辑器字典中移除
            if index in self.editors:
                del self.editors[index]
        
        # 移除标签页
        self.removeTab(index)
        
        # 发送标签页关闭信号
        self.tab_closed.emit(index)
        
        # 重新索引剩余的编辑器
        self._reindex_editors()
    
    def _reindex_editors(self):
        """重新索引编辑器字典"""
        new_editors = {}
        for i in range(self.count()):
            # 查找原来的编辑器实例
            for old_index, editor in self.editors.items():
                if self.widget(i) == editor:
                    new_editors[i] = editor
                    break
        self.editors = new_editors
    
    def on_current_tab_changed(self, index):
        """当前标签页改变时的处理"""
        self.current_tab_changed.emit(index)
        
        # 更新父窗口的当前项目引用
        if self._parent and hasattr(self._parent, 'current_item'):
            editor = self.editors.get(index)
            if editor and hasattr(editor, 'item'):
                self._parent.current_item = {
                    'id': editor.item.item_id,
                    'title': self.tabBar().tabText(index),
                    'page_type': editor.item.page_type
                }
    
    def show_context_menu(self, position):
        """显示标签页右键菜单"""
        tab_index = self.tabBar().tabAt(position)
        if tab_index == -1:
            return
            
        menu = QMenu(self)
        
        # 关闭当前标签页
        close_action = QAction("关闭标签页", self)
        close_action.triggered.connect(lambda: self.close_tab(tab_index))
        menu.addAction(close_action)
        
        # 关闭其他标签页
        if self.count() > 1:
            close_others_action = QAction("关闭其他标签页", self)
            close_others_action.triggered.connect(lambda: self.close_other_tabs(tab_index))
            menu.addAction(close_others_action)
        
        # 关闭所有标签页
        close_all_action = QAction("关闭所有标签页", self)
        close_all_action.triggered.connect(self.close_all_tabs)
        menu.addAction(close_all_action)
        
        menu.exec(self.tabBar().mapToGlobal(position))
    
    def close_other_tabs(self, keep_index):
        """关闭除指定索引外的所有标签页"""
        # 从后往前关闭，避免索引变化影响
        for i in range(self.count() - 1, -1, -1):
            if i != keep_index:
                self.close_tab(i)
    
    def close_all_tabs(self):
        """关闭所有标签页"""
        # 从后往前关闭，避免索引变化影响
        for i in range(self.count() - 1, -1, -1):
            self.close_tab(i)
    
    def get_current_editor(self):
        """获取当前标签页的编辑器"""
        current_index = self.currentIndex()
        return self.editors.get(current_index)
    
    def save_all_tabs(self):
        """保存所有标签页的内容"""
        for editor in self.editors.values():
            try:
                editor.save_current_item()
            except Exception as e:
                logger.error(f"保存标签页内容失败: {e}")