#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
插件加载器
负责加载和管理插件页面
"""

import os
import json
from typing import Dict, Any, Optional
from utils import logger


def setup_plugin_system(web_engine_view, web_engine_page, plugin_manager, plugin_api):
    """设置插件系统"""
    try:
        # 创建插件加载器实例
        loader = PluginLoader(web_engine_view, web_engine_page, plugin_manager, plugin_api)
        logger.info("插件加载器初始化完成")
        return loader
    except Exception as e:
        logger.error(f"设置插件系统失败: {e}")
        return None


class PluginLoader:
    """插件加载器"""
    
    def __init__(self, web_engine_view, web_engine_page, plugin_manager, plugin_api):
        self.web_engine_view = web_engine_view
        self.web_engine_page = web_engine_page
        self.plugin_manager = plugin_manager
        self.plugin_api = plugin_api
        self.logger = logger
        self.loaded_plugins = {}
        
    def load_plugin_page(self, web_view, plugin_id: str, page_id: str) -> bool:
        """加载插件页面"""
        try:
            if not self.plugin_manager:
                self.logger.error("插件管理器未初始化")
                return False
                
            # 获取插件信息
            plugin_info = self.plugin_manager.get_plugin_info(plugin_id)
            if not plugin_info:
                self.logger.error(f"插件不存在: {plugin_id}")
                return False
                
            # 构建插件页面路径
            plugin_path = plugin_info.get('path', '')
            if not plugin_path:
                self.logger.error(f"插件路径为空: {plugin_id}")
                return False
                
            index_html = os.path.join(plugin_path, 'index.html')
            if not os.path.exists(index_html):
                self.logger.error(f"插件入口文件不存在: {index_html}")
                return False
                
            # 加载HTML页面
            from PySide6.QtCore import QUrl
            web_view.load(QUrl.fromLocalFile(index_html))
            
            self.logger.info(f"插件页面加载成功: {plugin_id} -> {page_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"加载插件页面失败 {plugin_id}: {e}")
            return False
    
    def get_plugin_list(self) -> Dict[str, Any]:
        """获取插件列表"""
        if not self.plugin_manager:
            return {"plugins": [], "total": 0, "active": 0}
            
        return self.plugin_manager.get_plugin_list()
    
    def get_plugin_info(self, plugin_id: str) -> Optional[Dict[str, Any]]:
        """获取插件详细信息"""
        if not self.plugin_manager:
            return None
            
        return self.plugin_manager.get_plugin_info(plugin_id)