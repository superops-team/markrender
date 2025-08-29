import os
import threading
from typing import Dict, Optional, Any, Callable, Union
from enum import Enum
from dataclasses import dataclass

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, QObject, Signal
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile, QWebEngineSettings
from PySide6.QtWebChannel import QWebChannel

from utils import logger
from db import db_manager


# 页面类型枚举定义
class PageType(Enum):
    """页面类型枚举，定义所有支持的页面类型"""
    MARKDOWN = "markdown"
    LANDING = "landing"
    EXCALIDRAW = "excalidraw"
    
    @property
    def html_file(self) -> str:
        """获取对应的HTML文件名"""
        mapping = {
            PageType.MARKDOWN: "cherry-markdown/index.html",
            PageType.LANDING: "landing.html",
            PageType.EXCALIDRAW: "excalidraw/index.html"  # 修复路径，指向excalidraw文件夹中的index.html
        }
        return mapping.get(self, "index.html")
    
    @property
    def display_name(self) -> str:
        """获取页面类型的显示名称"""
        mapping = {
            PageType.MARKDOWN: "Markdown编辑器",
            PageType.LANDING: "首页",
            PageType.EXCALIDRAW: "绘图板"
        }
        return mapping.get(self, "未知页面")


@dataclass
class PageConfig:
    """页面配置类，用于管理页面创建参数"""
    page_type: PageType
    backend_interface: Optional[QObject] = None
    preload: bool = False
    cache_enabled: bool = True
    performance_mode: bool = True
    
    def __post_init__(self):
        if isinstance(self.page_type, str):
            # 如果传入字符串，转换为PageType枚举
            try:
                self.page_type = PageType(self.page_type)
            except ValueError:
                logger.warning(f"未知页面类型: {self.page_type}，使用默认MARKDOWN类型")
                self.page_type = PageType.MARKDOWN


# 增强的CustomWebEnginePage类，集成WebChannel
class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.channel = QWebChannel()
        self.channel_ready = False
        
    def javaScriptConsoleMessage(self, level, message, line_number, source_id):
        super().javaScriptConsoleMessage(level, message, line_number, source_id)
        logger.debug(f"JS Console: {message} (Line {line_number} in {source_id})", level)

    def acceptNavigationRequest(self, url, nav_type, is_main_frame):
        """限制导航请求"""
        allowed_schemes = ['file']
        allowed_domains = ['localhost', '127.0.0.1']
        
        if url.scheme() in allowed_schemes:
            return True
        if url.host() in allowed_domains:
            return True
        
        logger.debug(f"Blocked navigation to: {url.toString()}")
        return False

    def contextMenuEvent(self, event):
        logger.debug("Right-click menu suppressed")

    def initialize_web_channel(self, backend_interface):
        """初始化WebChannel并注册后端接口"""
        if self.channel_ready or not self.channel:
            return
            
        if backend_interface:
            self.channel.registerObject('backendInterface', backend_interface)
            self.setWebChannel(self.channel)
            self.channel_ready = True
            logger.debug("WebChannel initialized for page")

    def cleanup(self):
        """清理WebChannel资源"""
        if self.channel:
            self.channel.deleteLater()
            self.channel = None
        self.channel_ready = False


# 高性能多页面管理器 
class WebPageManager(QObject):
    """高性能单进程多页面管理器，集成WebChannel管理和智能预加载"""
    
    # 类级信号
    page_created = Signal(str, str)      # page_id, page_type
    page_loaded = Signal(str, bool)      # page_id, success
    page_switched = Signal(str, str)     # from_page_id, to_page_id
    page_removed = Signal(str)           # page_id
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    # 初始化QObject父类
                    super(WebPageManager, cls._instance).__init__()
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        # 防止重复初始化
        if hasattr(self, '_initialized') and self._initialized:
            return
            
        # 不调用super().__init__()，因为在__new__中已经调用过
        self.pages: Dict[str, QWebEngineView] = {}
        self.backend_interfaces: Dict[str, QObject] = {}
        self.page_configs: Dict[str, PageConfig] = {}  # 存储页面配置
        self.preloaded_pages: Dict[PageType, QWebEngineView] = {}  # 预加载页面缓存
        self.current_page_id: Optional[str] = None
        
        self._initialized = True
        logger.info("WebPageManager初始化完成，启用高性能多页面管理")
        
    def create_page(self, page_id: str, backend_interface=None, config: Optional[PageConfig] = None) -> Optional[QWebEngineView]:
        """
        创建新页面并初始化WebChannel
        
        Args:
            page_id: 页面唯一标识
            backend_interface: 后端接口对象（可选）
            config: 页面配置对象
            
        Returns:
            QWebEngineView实例
        """
        if page_id in self.pages:
            logger.warning(f"页面 {page_id} 已存在，返回现有页面")
            return self.pages[page_id]
        
        # 如果没有提供配置，创建默认配置
        if not config:
            config = PageConfig(
                page_type=PageType.MARKDOWN,
                backend_interface=backend_interface
            )
        
        # 参数过滤机制：只保留PageConfig支持的参数
        valid_config_keys = {'page_type', 'backend_interface', 'preload', 'cache_enabled', 'performance_mode'}
        filtered_params = {k: v for k, v in config.__dict__.items() if k in valid_config_keys}
        config = PageConfig(**filtered_params)
        
        try:
            logger.info(f"开始创建页面: {page_id}, 类型: {config.page_type.value}, 预加载: {config.preload}")
            
            # 创建视图和页面
            view = QWebEngineView()
            page = CustomWebEnginePage(view)
            
            view.setPage(page)
            self._apply_profile(page)
            
            # 性能优化设置
            settings = page.settings()
            if config.performance_mode:
                self._apply_performance_settings(settings)
            
            # 存储页面、配置和后端接口
            self.pages[page_id] = view
            self.page_configs[page_id] = config
            
            if backend_interface:
                self.backend_interfaces[page_id] = backend_interface
                # 立即初始化WebChannel
                page.initialize_web_channel(backend_interface)
                logger.debug(f"页面 {page_id} WebChannel初始化完成")
            
            # 发送页面创建信号
            self.page_created.emit(page_id, config.page_type.value)
            
            logger.info(f"页面创建成功: {page_id} ({config.page_type.display_name})")
            return view
            
        except Exception as e:
            logger.error(f"创建页面失败 {page_id}: {e}", exc_info=True)
            return None

    def set_backend_interface(self, page_id: str, backend_interface):
        """为页面设置后端接口并初始化WebChannel"""
        if page_id not in self.pages:
            logger.warning(f"Page {page_id} not found")
            return False
            
        self.backend_interfaces[page_id] = backend_interface
        
        # 获取页面并初始化WebChannel
        view = self.pages[page_id]
        page = view.page()
        if isinstance(page, CustomWebEnginePage):
            page.initialize_web_channel(backend_interface)
            return True
        
        return False

    def get_backend_interface(self, page_id: str):
        """获取页面的后端接口"""
        return self.backend_interfaces.get(page_id)

    def remove_page(self, page_id: str) -> bool:
        """移除页面并清理WebChannel资源"""
        if page_id not in self.pages:
            logger.warning(f"页面 {page_id} 不存在")
            return False
            
        try:
            logger.info(f"开始移除页面: {page_id}")
            
            # 清理页面和WebChannel
            view = self.pages[page_id]
            page = view.page()
            
            if isinstance(page, CustomWebEnginePage):
                page.cleanup()
                logger.debug(f"页面 {page_id} WebChannel清理完成")
            
            view.deleteLater()
            
            # 清理存储
            del self.pages[page_id]
            if page_id in self.backend_interfaces:
                del self.backend_interfaces[page_id]
            if page_id in self.page_configs:
                del self.page_configs[page_id]
            
            # 更新当前页面ID
            if self.current_page_id == page_id:
                self.current_page_id = None
                
            # 发送页面移除信号
            self.page_removed.emit(page_id)
                
            logger.info(f"页面移除成功: {page_id}")
            return True
            
        except Exception as e:
            logger.error(f"移除页面失败 {page_id}: {e}", exc_info=True)
            return False
    
    def _apply_profile(self, page: QWebEnginePage):
        """应用共享配置"""
        try:
            cache_path = db_manager.get_user_data_dir() + '/web_cache'
            storage_path = db_manager.get_user_data_dir() + '/web_storage'
            os.makedirs(cache_path, exist_ok=True)
            os.makedirs(storage_path, exist_ok=True)
            profile = page.profile()
            profile.setCachePath(cache_path)
            profile.setPersistentStoragePath(storage_path)
            # 使用字符串值而不是枚举常量来避免兼容性问题
            # profile.setHttpCacheType(QWebEngineProfile.DiskHttpCache)
            # 设置缓存大小为 100MB
            profile.setHttpCacheMaximumSize(100 * 1024 * 1024)
            
            # 新增性能优化配置
            # profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)
            profile.setSpellCheckEnabled(False)  # 禁用拼写检查提高性能
        except Exception as e:
            logger.warning(f"应用配置文件时出错: {e}")

    def _apply_performance_settings(self, settings):
        """应用性能优化设置"""
        try:
            # 使用字符串而不是常量来设置，避免兼容性问题
            settings.setAttribute(settings.WebAttribute.JavascriptEnabled, True)
            settings.setAttribute(settings.WebAttribute.LocalStorageEnabled, True)
            settings.setAttribute(settings.WebAttribute.AutoLoadImages, True)
            # 其他设置可能需要根据具体的PySide6版本进行调整
            logger.debug("性能优化设置已应用")
        except Exception as e:
            logger.warning(f"应用性能设置时出错: {e}")
    
    def load_html(self, page_id: str, file_name: str, callback: Optional[Callable[[bool], None]] = None) -> bool:
        """
        从plugins目录加载HTML文件
        
        Args:
            page_id: 页面ID
            file_name: HTML文件名（不含扩展名）
            callback: 加载完成回调函数，参数为(bool)表示成功与否
            
        Returns:
            是否成功开始加载
        """
        if page_id not in self.pages:
            logger.warning(f"Page {page_id} not found, creating new page")
            self.create_page(page_id)
            return False
        
        try:
            # 构建文件路径
            plugins_dir = os.path.join(os.path.dirname(__file__), 'plugins')
            html_file = os.path.join(plugins_dir, f"{file_name}")
            
            if not os.path.exists(html_file):
                logger.error(f"HTML file not found: {html_file}")
                if callback:
                    callback(False)
                return False
            
            view = self.pages[page_id]
            
            # 连接加载完成信号
            if callback:
                # 使用lambda包装，确保只触发一次
                def on_load_finished(success):
                    view.loadFinished.disconnect()  # 断开连接避免重复调用
                    callback(success)
                
                view.loadFinished.connect(on_load_finished)
            
            # view.setHtml(html_content, QUrl.fromLocalFile(html_file))
            logger.info(f"load html path: {html_file}")
            view.setUrl(QUrl.fromLocalFile(html_file))
            return True    
        except Exception as e:
            logger.error(f"Failed to load HTML file {page_id}: {e}")
            if callback:
                callback(False)
            return False
    
    def load_url(self, page_id: str, url: str) -> bool:
        """
        加载URL
        
        Args:
            page_id: 页面ID
            url: 要加载的URL
            
        Returns:
            是否成功加载
        """
        if page_id not in self.pages:
            logger.error(f"Page {page_id} not found")
            return False
        
        try:
            view = self.pages[page_id]
            view.load(QUrl(url))
            return True  
        except Exception as e:
            logger.error(f"Failed to load URL {url} for page {page_id}: {e}")
            return False
    
    def get_page(self, page_id: str):
        """获取页面的QWebEnginePage对象"""
        if page_id in self.pages:
            return self.pages[page_id].page()
        return None
    

    
    def get_page_count(self) -> int:
        """获取当前页面数量"""
        return len(self.pages)
    
    def get_all_page_ids(self) -> list:
        """获取所有页面ID"""
        return list(self.pages.keys())
    
    def get_or_create_page(self, page_id: str, page_type: PageType, backend_interface=None) -> Optional[QWebEngineView]:
        """获取或创建页面（为每个page_id创建独立实例，确保数据隔离）"""
        logger.info(f"请求页面: {page_id}, 类型: {page_type.value}")
        
        # 如果页面已存在，直接返回
        if page_id in self.pages:
            logger.debug(f"页面 {page_id} 已存在，直接返回")
            old_page_id = self.current_page_id
            self.current_page_id = page_id
            if old_page_id != page_id:
                self.page_switched.emit(old_page_id or "", page_id)
            return self.pages[page_id]
        
        # 对于Board/Excalidraw类型，每个page_id都创建独立实例以确保数据隔离
        if page_type == PageType.EXCALIDRAW:
            logger.info(f"为 {page_type.value} 创建独立页面实例: {page_id}")
            config = PageConfig(
                page_type=page_type,
                backend_interface=backend_interface
            )
            new_view = self.create_page(page_id, backend_interface, config)
            if new_view:
                old_page_id = self.current_page_id
                self.current_page_id = page_id
                if old_page_id != page_id:
                    self.page_switched.emit(old_page_id or "", page_id)
            return new_view
        
        # 对于其他类型（如markdown、landing），可以考虑复用
        # 智能复用：查找已存在的相同类型页面
        existing_page_id = self._find_existing_page_by_type(page_type)
        if existing_page_id:
            logger.info(f"复用现有的 {page_type.value} 页面: {existing_page_id} -> {page_id}")
            existing_view = self.pages[existing_page_id]
            
            # 将现有页面重新映射到新page_id
            self.pages[page_id] = existing_view
            # 保持原有映射，支持多个page_id指向同一个页面实例
            
            # 更新后端接口映射
            if backend_interface:
                self.backend_interfaces[page_id] = backend_interface
            
            old_page_id = self.current_page_id
            self.current_page_id = page_id
            if old_page_id != page_id:
                self.page_switched.emit(old_page_id or "", page_id)
            
            return existing_view
        
        # 检查是否有预加载的同类型页面可以复用
        if page_type in self.preloaded_pages:
            logger.info(f"复用预加载的 {page_type.value} 页面")
            preloaded_view = self.preloaded_pages.pop(page_type)
            self.pages[page_id] = preloaded_view
            
            # 更新后端接口
            if backend_interface:
                self.backend_interfaces[page_id] = backend_interface
                page = preloaded_view.page()
                if isinstance(page, CustomWebEnginePage):
                    page.initialize_web_channel(backend_interface)
            
            # 异步预加载新的同类型页面以备后用
            self._async_preload_page_type(page_type)
            
            old_page_id = self.current_page_id
            self.current_page_id = page_id
            if old_page_id != page_id:
                self.page_switched.emit(old_page_id or "", page_id)
            
            return preloaded_view
        
        # 创建新页面
        config = PageConfig(
            page_type=page_type,
            backend_interface=backend_interface
        )
        return self.create_page(page_id, backend_interface, config)
    
    def _find_existing_page_by_type(self, page_type: PageType) -> Optional[str]:
        """查找已存在的相同类型页面"""
        for page_id, config in self.page_configs.items():
            if config.page_type == page_type and page_id in self.pages:
                logger.debug(f"找到现有的 {page_type.value} 页面: {page_id}")
                return page_id
        return None
    
    def preload_page_type(self, page_type: PageType, backend_interface=None) -> bool:
        """预加载指定类型的页面模板"""
        if page_type in self.preloaded_pages:
            logger.debug(f"页面类型 {page_type.value} 已预加载")
            return True
        
        preload_id = f"preload_{page_type.value}_{id(self)}"
        logger.info(f"开始预加载页面类型: {page_type.value}")
        
        config = PageConfig(
            page_type=page_type,
            backend_interface=backend_interface,
            preload=True
        )
        
        view = self.create_page(page_id=preload_id, backend_interface=backend_interface, config=config)
        if view:
            # 加载页面内容
            self.load_page_content(preload_id, page_type)
            self.preloaded_pages[page_type] = view
            logger.info(f"页面类型 {page_type.value} 预加载完成")
            return True
        
        logger.error(f"页面类型 {page_type.value} 预加载失败")
        return False
    
    def _async_preload_page_type(self, page_type: PageType):
        """异步预加载页面类型"""
        from PySide6.QtCore import QTimer
        # 延迟预加载，避免阻塞当前操作
        QTimer.singleShot(100, lambda: self.preload_page_type(page_type))
    
    def load_page_content(self, page_id: str, page_type: Optional[PageType] = None) -> bool:
        """加载页面内容"""
        if page_id not in self.pages:
            logger.error(f"页面 {page_id} 不存在")
            return False
        
        if not page_type and page_id in self.page_configs:
            page_type = self.page_configs[page_id].page_type
        
        if not page_type:
            logger.error(f"无法确定页面 {page_id} 的类型")
            return False
        
        html_file = page_type.html_file
        logger.info(f"加载页面内容: {page_id} -> {html_file}")
        
        return self.load_html(page_id, html_file, 
                            callback=lambda success: self.page_loaded.emit(page_id, success))
