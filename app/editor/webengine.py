import os
import threading
from typing import Dict, Optional, Callable, List
from PySide6.QtWidgets import QStackedWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtCore import QUrl, QTimer, Signal, QObject, QMetaObject, Qt, QThread

from utils import logger
from db import db_manager
from app.editor.js_scripts import JSScriptManager

# 定义页面类型枚举
class PageType:
    MARKDOWN = "markdown"
    EXCALIDRAW = "excalidraw"
    LANDING = "landing"
    
    @classmethod
    def all_types(cls) -> List[str]:
        return [cls.MARKDOWN, cls.EXCALIDRAW, cls.LANDING]

# 页面配置类
class PageConfig:
    def __init__(self, page_type: str, 
                 preload: bool = False, 
                 cache_enabled: bool = True, 
                 performance_mode: bool = True):
        self.page_type = page_type
        self.preload = preload
        self.cache_enabled = cache_enabled
        self.performance_mode = performance_mode

# 页面-通道绑定类，用于管理页面和后端接口的一对一关系
class PageChannelBinding:
    def __init__(self, page_type: str, view: QWebEngineView):
        self.page_type = page_type
        self.view = view
        self.is_ready = False
        self.backend_interface = None
    
    def set_ready(self, ready: bool):
        self.is_ready = ready
    
    def set_backend_interface(self, backend_interface):
        self.backend_interface = backend_interface

# 自定义WebEnginePage类
class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.backend_interface = None
        self.page_type = None

# 更新WebPageManager类中的create_page方法
class WebPageManager(QStackedWidget):
    """高性能单进程多页面管理器，基于QStackedWidget实现页面切换"""
    
    # 类级信号
    page_created = Signal(str)      # page_type
    page_loaded = Signal(str, bool) # page_type, success
    page_switched = Signal(str, str) # from_page_type, to_page_type
    page_removed = Signal(str)      # page_type

    def __init__(self, parent=None):
        super().__init__(parent)
        self.backend_interfaces: Dict[str, QObject] = {}  # 页面类型 -> 后端接口
        self.page_configs: Dict[str, PageConfig] = {}     # 页面类型 -> 页面配置
        self.preloaded_pages: Dict[str, QWebEngineView] = {}  # 页面类型 -> 视图实例
        self.page_bindings: Dict[str, PageChannelBinding] = {}  # 页面类型 -> 页面通道绑定
        self.current_page_type: Optional[str] = None
        self._lock = threading.RLock()  # 用于线程安全操作
        
        logger.info("WebPageManager初始化完成，启用高性能多页面管理")
        
    def create_page(self, page_type: str, backend_interface=None, config: Optional[PageConfig] = None) -> Optional[QWebEngineView]:
        """
        创建新页面
        
        Args:
            page_type: 页面类型
            backend_interface: 后端接口对象（可选）
            config: 页面配置对象
            
        Returns:
            QWebEngineView实例
        """
        with self._lock:
            if page_type in self.preloaded_pages:
                logger.warning(f"页面 {page_type} 已存在，返回现有页面")
                return self.preloaded_pages[page_type]
            
            # 如果没有提供配置，创建默认配置
            if not config:
                config = PageConfig(
                    page_type=page_type,
                    preload=False
                )
            
            try:
                logger.info(f"开始创建页面: {page_type}, 类型: {config.page_type}, 预加载: {config.preload}")
                
                # 创建视图和页面
                view = QWebEngineView()
                page = CustomWebEnginePage(view)
                page.page_type = page_type  # 设置页面类型
                
                view.setPage(page)
                self._apply_profile(page)
                
                # 性能优化设置
                settings = page.settings()
                if config.performance_mode:
                    self._apply_performance_settings(settings)
                
                # 存储页面、配置
                self.preloaded_pages[page_type] = view
                self.page_configs[page_type] = config
                
                # 添加到QStackedWidget中
                self.addWidget(view)
                
                # 发送页面创建信号
                self.page_created.emit(page_type)
                
                logger.info(f"页面创建成功: {page_type}")
                return view
                
            except Exception as e:
                logger.error(f"创建页面失败 {page_type}: {e}", exc_info=True)
                return None

    def set_backend_interface(self, page_type: str, backend_interface) -> bool:
        """为页面设置后端接口"""
        with self._lock:
            if page_type not in self.preloaded_pages:
                logger.warning(f"Page {page_type} not found")
                return False
                
            self.backend_interfaces[page_type] = backend_interface
            
            # 获取页面并设置通信管理器的页面引用
            view = self.preloaded_pages[page_type]
            page = view.page()
            
            if isinstance(page, CustomWebEnginePage):
                # 设置通信管理器的页面引用
                backend_interface.set_page(page)
                
                logger.debug(f"页面 {page_type} 后端接口设置完成")
                return True
            
            return False

    def get_backend_interface(self, page_type: str) -> Optional[QObject]:
        """获取页面的后端接口"""
        with self._lock:
            return self.backend_interfaces.get(page_type)
    
    def remove_page(self, page_type: str) -> bool:
        """移除页面并清理资源"""
        with self._lock:
            if page_type not in self.preloaded_pages:
                logger.warning(f"页面 {page_type} 不存在")
                return False
                
            try:
                logger.info(f"开始移除页面: {page_type}")
                
                # 清理页面
                view = self.preloaded_pages[page_type]
                page = view.page()
                if isinstance(page, CustomWebEnginePage):
                    pass
                logger.debug(f"页面 {page_type} 清理完成")
                
                # 从QStackedWidget中移除
                self.removeWidget(view)
                view.deleteLater()
                
                # 清理存储
                del self.preloaded_pages[page_type]
                if page_type in self.backend_interfaces:
                    del self.backend_interfaces[page_type]
                if page_type in self.page_configs:
                    del self.page_configs[page_type]
                
                # 更新当前页面类型
                if self.current_page_type == page_type:
                    self.current_page_type = None
                    
                # 发送页面移除信号
                self.page_removed.emit(page_type)
                    
                logger.info(f"页面移除成功: {page_type}")
                return True
                
            except Exception as e:
                logger.error(f"移除页面失败 {page_type}: {e}", exc_info=True)
                return False
    
    def switch_to_page(self, page_type: str) -> bool:
        """切换到指定页面类型
        
        Args:
            page_type: 要切换到的页面类型
            
        Returns:
            是否成功切换
        """
        with self._lock:
            if page_type not in self.preloaded_pages:
                logger.warning(f"页面类型 {page_type} 不存在")
                return False
                
            view = self.preloaded_pages[page_type]
            current_index = self.currentIndex()
            new_index = self.indexOf(view)
            
            if current_index != new_index:
                old_page_type = self.current_page_type
                self.current_page_type = page_type
                self.setCurrentIndex(new_index)
                self.page_switched.emit(
                    old_page_type or "", 
                    page_type
                )
                logger.info(f"页面切换: {old_page_type} -> {page_type}")
            else:
                logger.debug(f"页面已在显示中: {page_type}")
                
            return True
    
    def get_or_create_page(self, page_type: str, backend_interface=None) -> Optional[QWebEngineView]:
        """获取或创建页面（为每个page_type创建独立实例，确保数据隔离）"""
        logger.info(f"请求页面: {page_type}")
        
        with self._lock:
            # 检查是否有预加载的同类型页面可以复用
            if page_type in self.preloaded_pages:
                logger.info(f"复用预加载的 {page_type} 页面")
                preloaded_view = self.preloaded_pages[page_type]
                
                # 更新后端接口映射
                if backend_interface:
                    self.backend_interfaces[page_type] = backend_interface
                    page = preloaded_view.page()
                    if isinstance(page, CustomWebEnginePage):
                        # 设置通信管理器的页面引用
                        backend_interface.set_page(page)
                
                # 重置页面状态，确保数据隔离
                self._reset_page_state(preloaded_view, page_type)
                return preloaded_view
            
            # 创建新页面
            config = PageConfig(
                page_type=page_type,
                cache_enabled=True
            )
            view = self.create_page(page_type, backend_interface, config)
            
            return view
    
    def preload_page_type(self, page_type: str, backend_interface=None):
        """预加载指定类型的页面"""
        try:
            logger.info(f"预加载页面类型: {page_type}")
            
            with self._lock:
                # 检查是否已经预加载
                if page_type in self.preloaded_pages:
                    logger.warning(f"页面类型 {page_type} 已经预加载过")
                    return
                
                # 创建预加载页面配置
                config = PageConfig(
                    page_type=page_type,
                    preload=True
                )
                
                # 创建预加载页面
                preload_view = self.create_page(page_type, backend_interface, config)
                if preload_view:
                    # 加载页面内容
                    html_file = f"{page_type}/index.html"
                    self.load_html(page_type, html_file)
                    
                    # 存储到预加载缓存
                    self.preloaded_pages[page_type] = preload_view
                    logger.info(f"页面类型 {page_type} 预加载完成")
                else:
                    logger.error(f"页面类型 {page_type} 预加载失败")
        except Exception as e:
            logger.error(f"预加载页面类型 {page_type} 失败: {e}", exc_info=True)
    
    def _async_preload_page_type(self, page_type: str, backend_interface=None):
        """异步预加载页面类型"""
        QTimer.singleShot(100, lambda: self.preload_page_type(page_type, backend_interface))
    
    def load_page_content(self, page_type: Optional[str] = None) -> bool:
        """加载页面内容"""
        if not page_type and self.current_page_type:
            page_type = self.current_page_type
        
        if not page_type:
            logger.error(f"无法确定页面类型")
            return False
        
        # 根据页面类型选择正确的HTML文件
        html_file = f"{page_type}/index.html"
        logger.info(f"加载页面内容: {page_type} -> {html_file}")
        
        return self.load_html(
            page_type, html_file, 
            callback=lambda success: self.page_loaded.emit(page_type, success)
        )
    
    def get_page(self, page_type: str) -> Optional[QWebEnginePage]:
        """获取页面的QWebEnginePage对象"""
        with self._lock:
            if page_type in self.preloaded_pages:
                return self.preloaded_pages[page_type].page()
            return None
    
    def _reset_page_state(self, view: QWebEngineView, page_type: str):
        """重置页面状态，确保数据隔离"""
        try:
            logger.info(f"重置页面状态: {page_type}")
            
            # 使用JSScriptManager获取重置脚本
            from app.editor.js_scripts import JSScriptManager
            reset_script = JSScriptManager.get_script("reset_page_state")
            
            if reset_script:
                # 异步执行重置脚本
                view.page().runJavaScript(reset_script)
                logger.info("页面状态重置脚本已执行")
            else:
                logger.error("获取页面状态重置脚本失败")
            
        except Exception as e:
            logger.error(f"重置页面状态失败: {page_type}, 错误: {e}")

    def get_page_count(self) -> int:
        """获取当前页面数量"""
        with self._lock:
            return len(self.preloaded_pages)
    
    def get_all_page_types(self) -> list:
        """获取所有页面类型"""
        with self._lock:
            return list(self.preloaded_pages.keys())
    
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
            # 设置缓存大小为 100MB
            profile.setHttpCacheMaximumSize(100 * 1024 * 1024)
            
            # 禁用拼写检查提高性能
            profile.setSpellCheckEnabled(False)
        except Exception as e:
            logger.warning(f"应用配置文件时出错: {e}")

    def _apply_performance_settings(self, settings):
        """应用性能优化设置"""
        try:
            settings.setAttribute(settings.WebAttribute.JavascriptEnabled, True)
            settings.setAttribute(settings.WebAttribute.LocalStorageEnabled, True)
            settings.setAttribute(settings.WebAttribute.AutoLoadImages, True)
            settings.setAttribute(settings.WebAttribute.WebGLEnabled, True)  # Enable WebGL
            settings.setAttribute(settings.WebAttribute.Accelerated2dCanvasEnabled, True)  # Enable GPU canvas
            settings.setAttribute(settings.WebAttribute.PluginsEnabled, True)  # Enable plugins
            logger.debug("Performance settings applied with WebGL enabled")
        except Exception as e:
            logger.warning(f"Failed to apply performance settings: {e}")
    
    def load_html(self, page_type: str, file_name: str, callback: Optional[Callable[[bool], None]] = None) -> bool:
        """
        从plugins目录加载HTML文件
        
        Args:
            page_type: 页面类型
            file_name: HTML文件名
            callback: 加载完成回调函数，参数为(bool)表示成功与否
            
        Returns:
            是否成功开始加载
        """
        with self._lock:
            if page_type not in self.preloaded_pages:
                logger.warning(f"Page {page_type} not found, creating new page")
                self.create_page(page_type)
                return False
            
            try:
                # 构建文件路径
                plugins_dir = os.path.join(os.path.dirname(__file__), 'plugins')
                html_file = os.path.join(plugins_dir, file_name)
                
                if not os.path.exists(html_file):
                    logger.error(f"HTML file not found: {html_file}")
                    if callback:
                        callback(False)
                    return False
                
                view = self.preloaded_pages[page_type]
                
                # 连接加载完成信号
                if callback:
                    # 使用lambda包装，确保只触发一次
                    def on_load_finished(success):
                        view.loadFinished.disconnect()  # 断开连接避免重复调用
                        callback(success)
                    
                    view.loadFinished.connect(on_load_finished)
                
                abs_file = os.path.abspath(html_file)
                local_url = QUrl.fromLocalFile(abs_file)
                logger.info(f"load html path: {html_file} {local_url}")
                view.load(local_url)
                return True    
            except Exception as e:
                logger.error(f"Failed to load HTML file {page_type}: {e}")
                if callback:
                    callback(False)
                return False
    
    def load_url(self, page_type: str, url: str) -> bool:
        """
        加载URL
        
        Args:
            page_type: 页面类型
            url: 要加载的URL
            
        Returns:
            是否成功加载
        """
        with self._lock:
            if page_type not in self.preloaded_pages:
                logger.error(f"Page {page_type} not found")
                return False
            
            try:
                view = self.preloaded_pages[page_type]
                view.load(QUrl(url))
                return True  
            except Exception as e:
                logger.error(f"Failed to load URL {url} for page {page_type}: {e}")
                return False
