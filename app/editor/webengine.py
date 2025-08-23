import os
import threading
from typing import Dict, Optional

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineProfile, QWebEngineSettings
from PySide6.QtWebChannel import QWebChannel

from utils import logger
from db import db_manager

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
        if self.channel_ready:
            return
            
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
class WebPageManager:
    """高性能单进程多页面管理器，集成WebChannel管理"""
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
            
        self._initialized = True
        self.pages: Dict[str, QWebEngineView] = {}
        self.backend_interfaces: Dict[str, QObject] = {}
        
    def create_page(self, page_id: str, backend_interface) -> QWebEngineView:
        """
        创建新页面并初始化WebChannel
        
        Args:
            page_id: 页面唯一标识
            backend_interface: 后端接口对象（可选）
            
        Returns:
            QWebEngineView实例
        """
        if page_id in self.pages:
            logger.warning(f"Page {page_id} already exists, returning existing")
            return self.pages[page_id]
        
        try:
            # 创建视图和页面
            view = QWebEngineView()
            page = CustomWebEnginePage(view)
            
            view.setPage(page)
            self._apply_profile(page)
            
            # 性能优化设置
            settings = page.settings()
            self._apply_performance_settings(settings)
            
            # 存储页面和后端接口
            self.pages[page_id] = view
            if backend_interface:
                self.backend_interfaces[page_id] = backend_interface
                # 立即初始化WebChannel
                page.initialize_web_channel(backend_interface)
            
            logger.info(f"Created page {page_id} with WebChannel integration")
            return view
            
        except Exception as e:
            logger.error(f"Failed to create page {page_id}: {e}")
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
            logger.warning(f"Page {page_id} not found")
            return False
            
        try:
            # 清理页面和WebChannel
            view = self.pages[page_id]
            page = view.page()
            
            if isinstance(page, CustomWebEnginePage):
                page.cleanup()
            
            view.deleteLater()
            
            # 清理存储
            del self.pages[page_id]
            if page_id in self.backend_interfaces:
                del self.backend_interfaces[page_id]
                
            logger.info(f"Removed page {page_id} with WebChannel cleanup")
            return True
            
        except Exception as e:
            logger.error(f"Failed to remove page {page_id}: {e}")
            return False
    
    def _apply_profile(self, page: QWebEnginePage):
        """应用共享配置"""
        cache_path = db_manager.get_user_data_dir() + '/web_cache'
        storage_path = db_manager.get_user_data_dir() + '/web_storage'
        os.makedirs(cache_path, exist_ok=True)
        os.makedirs(storage_path, exist_ok=True)
        profile = page.profile()
        profile.setCachePath(cache_path)
        profile.setPersistentStoragePath(storage_path)
        profile.setHttpCacheType(QWebEngineProfile.DiskHttpCache)
        # 设置缓存大小为 100MB
        profile.setHttpCacheMaximumSize(100 * 1024 * 1024)
        
        # 新增性能优化配置
        profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)
        profile.setSpellCheckEnabled(False)  # 禁用拼写检查提高性能

    def _apply_performance_settings(self, settings):
        """应用性能优化设置"""
        optimizations = {
            QWebEngineSettings.Accelerated2dCanvasEnabled: True,
            QWebEngineSettings.WebGLEnabled: True,
            QWebEngineSettings.TouchIconsEnabled: False,
            QWebEngineSettings.FocusOnNavigationEnabled: False,
            QWebEngineSettings.ErrorPageEnabled: True,
            QWebEngineSettings.PluginsEnabled: True,
            QWebEngineSettings.JavascriptCanOpenWindows: True,
            QWebEngineSettings.LocalStorageEnabled: True,
            QWebEngineSettings.LocalContentCanAccessRemoteUrls: False,
            QWebEngineSettings.JavascriptEnabled: True,
            QWebEngineSettings.AutoLoadImages: True,
            QWebEngineSettings.JavascriptCanAccessClipboard: True,
        }
        
        for setting, value in optimizations.items():
            settings.setAttribute(setting, value)
    
    def load_html(self, page_id: str, file_name: str, callback: callable = None) -> bool:
        """
        从resources目录加载HTML文件
        
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
            resources_dir = os.path.join(os.path.dirname(__file__), 'resources')
            html_file = os.path.join(resources_dir, f"{file_name}.html")
            
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
    
    def remove_page(self, page_id: str) -> bool:
        """移除页面并清理资源"""
        if page_id not in self.pages:
            logger.warning(f"Page {page_id} not found")
            return False
            
        try:
            # 清理页面
            view = self.pages[page_id]
            view.deleteLater()
            
            # 清理存储
            del self.pages[page_id]
                
            logger.info(f"Removed page {page_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to remove page {page_id}: {e}")
            return False
    
    def get_page_count(self) -> int:
        """获取当前页面数量"""
        return len(self.pages)
    
    def get_all_page_ids(self) -> list:
        """获取所有页面ID"""
        return list(self.pages.keys())
