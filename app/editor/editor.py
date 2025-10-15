import json  # 添加json导入
import time

from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import QObject, Signal, Property, QTimer
from app.preference import AppStyle
from app.editor.backend_interface import BackendInterface
from app.editor.webengine import WebPageManager  # 导入页面管理器
from utils import logger
from db.markrender_manager import MarkRenderManager
from db.settings_manager import SettingsManager

from app.editor.export_manager import ExportManager


class MarkRenderItem(QObject):
    text_changed = Signal(str)

    def __init__(self, item_id, page_type, text=""):
        super().__init__()
        self.item_id = item_id
        self.page_type = page_type
        self._text = text

    def get_text(self):
        return self._text

    def set_text(self, text):
        self._text = text
        self.text_changed.emit(text)  # 触发文档内部变更

    def reset(self):
        """重置文档状态"""
        self._text = ""
        self.text_changed.emit("")  # 发射清空内容的信号

    text = Property(str, get_text, set_text, notify=text_changed)


class MarkRenderEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 初始化页面管理器
        self.page_manager = WebPageManager()
        self.page_loaded = False
        self._close_ready = False
        
        # 初始化页面管理器
        self.page_manager = WebPageManager()
        self.page_type = 'markdown' # 首次初始化默认加载markdown
        
        # 初始化文档
        self.item = MarkRenderItem(item_id="", page_type="")
        # 建立信号连接
        self.item.text_changed.connect(self.on_item_text_changed)

        # 初始化其他组件
        self.markrender_manager = MarkRenderManager()
        
        # 设置UI
        self.setup_ui()
        
    def get_page_type(self):
        return self.page_type

    def setup_ui(self):        
        # 创建通信管理器（每个页面一个实例）
        self.backend_interface = BackendInterface(self.page_type)  # 使用实际页面类型
        
        # 创建布局
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)
        self.setLayout(layout)

        # 预加载常用页面类型
        logger.info("开始预加载常用页面类型...")
        
        # 预加载页面，后续插件化动态加载
        self.page_manager.preload_page_type("markdown")
        self.page_manager.preload_page_type("excalidraw")
 
        # 创建预览页面，默认创建markdown页面
        self.preview = self.page_manager.get_or_create_page(
            page_type="markdown",
            backend_interface=self.backend_interface
        )
        
        if not self.preview:
            logger.error("创建页面失败")
            return
        
        # 将通信管理器附加到页面管理器
        self.backend_interface.set_page(self.preview.page())  # 直接设置页面对象
        
        # 加载HTML文件
        success = self.page_manager.load_page_content("markdown")
        if not success:
            logger.error(f"加载HTML文件失败: markdown")
        layout.addWidget(self.page_manager)
        # 设置样式
        self.setStyleSheet(AppStyle().get_editor_parent() + AppStyle().get_editor_preview())
        
        # 连接页面管理器信号
        self.page_manager.page_loaded.connect(self._on_page_loaded)
        self.page_manager.page_switched.connect(self._on_page_switched)
        
        logger.info("编辑器UI初始化完成")
    
    def _on_page_loaded(self, page_type):
        """页面加载完成回调"""
        logger.info(f"页面加载完成: {page_type}")
        self.page_loaded = True
        
        # 设置页面功能特性
        self._setup_page_features()
        
        # 如果有待设置的初始内容，则设置它
        if hasattr(self, 'initial_content') and self.initial_content is not None:
            logger.info(f"设置初始内容，长度: {len(self.initial_content)}")
            self.set_text_content(self.initial_content)
            # 清除初始内容，避免重复设置
            delattr(self, 'initial_content')

    def on_item_text_changed(self, text):
        """转发文档变更到前端"""
        logger.debug(f"文档变更: {text}")
        # 通知前端文档变更
        self.set_text_content(text)

    def init_auto_save(self):
        """初始化自动保存功能"""
        # TODO: 传递到前端让前端周期性自动保存
        self.general_settings = SettingsManager().get_settings_dict('general') or {}
        self.auto_save_enabled = self.general_settings.get('auto_save', True)
        self.auto_save_interval = self.general_settings.get('auto_save_interval', 30) * 1000

    def _setup_page_features(self):
        """设置页面功能特性"""
        # TODO 初始化页面在服务器端的配置
    
    def _reset_frontend_state(self):
        """重置前端页面状态，确保数据隔离"""
        try:
            logger.info("重置前端页面状态")
            # 使用JSScriptManager获取重置脚本
            from app.editor.js_scripts import JSScriptManager
            reset_script = JSScriptManager.get_script("reset_page_state")
            if reset_script:
                # 异步执行重置脚本
                if hasattr(self, 'preview') and self.preview:
                    self.preview.page().runJavaScript(reset_script)
                    logger.info("前端状态重置脚本已执行")
            else:
                logger.error("获取前端状态重置脚本失败")
        except Exception as e:
            logger.error(f"重置前端状态失败: {e}")

    def _on_page_switched(self, from_page_type, to_page_type):  
        """页面切换回调 - 优化版本，避免布局重排，添加转场效果"""        
        try:
            logger.info(f"页面切换from {from_page_type} -> {to_page_type}")
            
            # 更新页面类型和backend接口
            self.page_type = to_page_type
            if hasattr(self, 'backend_interface') and self.backend_interface:
                self.backend_interface.set_page_type(to_page_type)
            # 重置前端页面状态，确保数据隔离
            self._reset_frontend_state()
        except Exception as e:
            logger.error(f"页面切换失败: {e}")
    
    def set_current_item(self, item_id, page_type, content):
        """设置当前编辑的文档项"""
        self.item.item_id = item_id
        self.item.page_type = page_type
        self.item.set_text(content)

    def save_current_item(self):
        """保存当前文档内容 - 增强版，确保获取到最新内容"""        
        try:
            # 检查页面是否已加载
            if not self.page_loaded:
                logger.warning("页面未加载完成，跳过保存")
                return False
            
            # 使用同步方法获取当前编辑内容，确保获取到最新内容
            logger.info("发送getContent消息获取编辑器内容（同步方式）")
            result = self.backend_interface.send_message_sync('getContent', {}, item_id=self.item.item_id, timeout=15000)
            if result is None:
                logger.error("获取编辑器内容失败（同步方式）")
                return False
            # 解析JavaScript返回的数据
            parsed_data = self._parse_js_response(result)
            if not parsed_data.get('success', False):
                # 只有当success为False时才认为获取内容失败
                error_msg = parsed_data.get('error', '未知错误') if parsed_data else '获取内容失败'
                logger.error(f"获取编辑器内容失败: {error_msg}")
                return False
            content = parsed_data.get("content", "")
            frontend_item_id = parsed_data.get("item_id", "")
            # 验证item_id一致性
            if frontend_item_id and self.item.item_id and frontend_item_id != self.item.item_id:
                logger.warning(f"保存时发现item_id不一致: 前端={frontend_item_id}, 后端={self.item.item_id}")
                # 使用前端返回的item_id
                self.item.item_id = frontend_item_id
            # 无论content是否为空，都尝试保存到数据库
            item_id = self.item.item_id
            if not item_id:
                logger.error(f"无法确保有效的item_id，跳过保存, page_type: {self.page_type}")
                return False
            success = self.markrender_manager.save_item(
                id=item_id, 
                content=content
            )
            
            if success:
                logger.info(f"手动保存成功: {item_id}，内容长度: {len(content)}")
                # 通知父窗口重新加载快速选择面板中的数据
                if hasattr(self.parent, 'update_quickpick_list'):
                    self.parent.update_quickpick_list()
                return True
            else:
                logger.error("保存到数据库失败")
                return False
        except Exception as e:
            logger.error(f"保存文档失败: {str(e)}，但允许继续切换")
            return False

    def save_item(self):
        """保存当前文档内容 - 兼容旧接口"""
        save_result = None  # 改为None以区分未开始和失败
        try:
            # 检查页面是否已加载
            if not self.page_loaded:
                logger.warning(f"页面未加载完成，跳过保存, page_type: {self.page_type}")
                return True
            # 获取当前编辑内容
            def handle_save_content(data):
                nonlocal save_result
                try:
                    # 解析JavaScript返回的数据
                    parsed_data = self._parse_js_response(data) if data is not None else {'success': False, 'error': '无响应数据'}
                    if parsed_data.get('success', False):
                        content = parsed_data.get("content", "")
                        item_id = self.item.item_id          
                        success = self.markrender_manager.save_item(
                            id=item_id, 
                            content=content
                        )
                        if success:
                            logger.info(f"手动保存成功: {item_id}，内容长度: {len(content)}")
                            save_result = True
                        else:
                            logger.error("保存到数据库失败")
                            save_result = False
                    else:
                        # 只有当success为False时才认为获取内容失败
                        error_msg = parsed_data.get('error', '未知错误') if parsed_data else '获取内容失败'
                        logger.error(f"获取编辑器内容失败: {error_msg}")
                        # 在切换时，即使获取内容失败也返回True，避免阻塞用户操作
                        save_result = True
                except Exception as e:
                    logger.error(f"处理保存内容时出错: {e}")
                    save_result = True  # 避免阻塞切换            
            # 使用增强版获取内容方法
            self.get_content_with_retry(handle_save_content)
            
            # 等待回调完成，但设置更短的超时
            import time
            from PySide6.QtWidgets import QApplication
            start_time = time.time()
            timeout = 2.0  # 增加到2秒超时，确保有足够时间获取内容
            while save_result is None and time.time() - start_time < timeout:
                QApplication.processEvents()
                time.sleep(0.01)
            
            # 如果超时，认为保存成功（避免阻塞切换）
            if save_result is None:
                logger.warning("保存操作超时，但允许继续切换")
                return True
            
            return save_result if isinstance(save_result, bool) else True
            
        except Exception as e:
            logger.error(f"保存文档失败: {str(e)}，但允许继续切换")
            return True  # 避免阻塞用户操作

    def reset(self):
        self.item.item_id = ""
        self.item.page_type = ""
        self.item.reset()  # 调用文档的 reset 方法
        # 通过channel发送清空内容请求
        self.backend_interface.send_message("setValue", {
            "content": ""
        }, item_id=self.item.item_id)

    def set_item_id(self, item_id):
        self.item.item_id = item_id
        # 通知前端当前文件ID
        if hasattr(self, 'backend_interface') and self.backend_interface:
            # 发送文件ID变更通知到前端
            self.backend_interface.send_message('setCurrentItemId', {
                'item_id': item_id
            }, item_id=item_id)
            logger.debug(f"已通知前端当前文件ID: {item_id}")
        else:
            logger.warning("backend_interface未初始化，无法通知前端当前文件ID变更")

    def get_content(self, callback):
        """获取markdown内容"""
        # 设置5秒超时
        timeout_timer = QTimer()
        timeout_timer.setSingleShot(True)
        timeout_timer.timeout.connect(lambda: callback({
            'success': False,
            'error': '获取内容超时'
        }))
        timeout_timer.start(5000)

        # 发送获取请求
        self.backend_interface.send_message(
            'getContent',
            callback=lambda response: (
                timeout_timer.stop(),
                # 解析响应数据
                callback(self._parse_js_response(response))
            ),
            item_id=self.item.item_id
        )
    
    def get_content_with_retry(self, callback, retry_count=5):
        """增强版获取内容方法，支持重试机制"""
        def internal_callback(response):
            logger.debug(f"获取内容回调，响应: {response}")
            parsed_data = self._parse_js_response(response)
            logger.debug(f"解析后的数据: {parsed_data}")
            
            # 检查是否成功获取内容
            if parsed_data.get('success', False) and 'content' in parsed_data:
                logger.info(f"成功获取内容，内容长度: {len(parsed_data.get('content', ''))}")
                callback(parsed_data)
            else:
                # 检查是否有错误信息
                error_msg = parsed_data.get('error', '未知错误')
                logger.error(f"获取内容失败: {error_msg}")
                
                # 如果失败且还有重试次数，等待后重试
                if retry_count > 0:
                    logger.warning(f"获取内容失败，剩余重试次数: {retry_count}，等待后重试")
                    from PySide6.QtCore import QTimer
                    retry_timer = QTimer()
                    retry_timer.setSingleShot(True)
                    retry_timer.timeout.connect(lambda: self.get_content_with_retry(callback, retry_count-1))
                    retry_timer.start(500)  # 增加等待时间到500ms
                else:
                    # 重试次数用完，返回失败
                    logger.error("获取内容失败，重试次数用完")
                    callback({
                        'success': False,
                        'error': '获取内容失败，重试次数用完: ' + error_msg
                    })
        
        # 使用同步方法获取内容
        logger.info("开始同步获取编辑器内容")
        result = self.backend_interface.send_message_sync('getContent', {}, item_id=self.item.item_id, timeout=15000)
        logger.debug(f"同步获取结果: {result}")
        internal_callback(result)
    
    def _parse_js_response(self, response):
        """解析JavaScript返回的响应"""
        logger.debug(f"原始响应: {response}")
        if isinstance(response, dict):
            # 已经是字典格式，检查是否包含success字段
            if 'success' not in response:
                # 如果没有success字段，假设操作成功
                response['success'] = True
            return response
        elif isinstance(response, str):
            try:
                # 尝试解析JSON
                parsed = json.loads(response)
                # 检查是否包含success字段
                if 'success' not in parsed:
                    # 如果没有success字段，假设操作成功
                    parsed['success'] = True
                return parsed
            except json.JSONDecodeError:
                # 如果解析失败，假设这是内容本身
                return {'success': True, 'content': response}
        else:
            # 其他情况，返回None或默认值
            return {'success': response is not None, 'content': response if response is not None else ''}
    
    def set_text_content(self, text_content):
        # 检查item_id是否已初始化
        if not self.item.item_id:
            logger.error("item_id未初始化，无法设置内容")
            return False
        # 检查backend_interface是否已初始化
        if not self.backend_interface or not self.backend_interface.page:
            logger.error("backend_interface未初始化或页面未加载，无法设置内容")
            return False
    
        # 检查页面是否已加载
        if not self.page_loaded:
            # 页面未加载，存储初始内容，等待页面加载完成后再设置
            logger.warning("页面未加载，存储初始内容等待后续设置")
            self.initial_content = text_content
            return False
    
        # 直接设置内容和item_id
        success = self.backend_interface.send_message("setValue", {
            "content": text_content,
            "item_id": self.item.item_id
        }, item_id=self.item.item_id)
        
        if success:
            logger.debug(f"内容已成功设置到前端，item_id: {self.item.item_id}")
        else:
            logger.error(f"设置内容失败，item_id: {self.item.item_id}")
        
        return success

    def set_text_content_with_retry(self, text_content, retry_count=3):
        """带重试机制的内容设置方法"""
        def internal_set_content(current_retry=0):
            success = self.set_text_content(text_content)
            if not success and current_retry < retry_count:
                logger.warning(f"设置内容失败，剩余重试次数: {retry_count - current_retry}")
                from PySide6.QtCore import QTimer
                retry_timer = QTimer()
                retry_timer.setSingleShot(True)
                retry_timer.timeout.connect(lambda: internal_set_content(current_retry + 1))
                retry_timer.start(500)  # 等待500ms后重试
            elif not success:
                logger.error("设置内容失败，重试次数用完")
            else:
                logger.info("内容设置成功")
        
        internal_set_content(0)

    def resizeEvent(self, event):
        """窗口大小改变时触发，确保编辑区高度自适应"""
        super().resizeEvent(event)
        # 可以在这里添加额外的调整逻辑
        # 布局管理器会自动处理子部件的大小

    def closeEvent(self, event):
        # 1. 快速检查是否真的需要保存
        need_save = self._check_if_save_needed()
        
        if need_save:
            logger.info(f"检测到需要保存文档: {self.item.item_id}")
            # 执行保存，但不阻止事件传播
            self._perform_save_on_close()
        
        # 无论是否需要保存，都接受事件，让主窗口决定关闭流程
        event.accept()
    
    def _perform_save_on_close(self):
        """在关闭时执行保存操作，不涉及事件处理"""
        try:
            # 退出前同步拉取数据并保存
            result = self.backend_interface.send_message_sync("getContent", {}, item_id=self.item.item_id, timeout=10000)
            if result and result.get('success', False): 
                content = result.get('content', '') if result else ''
                if self.item.item_id == result.get('item_id', ''):
                    self.markrender_manager.save_item(id=self.item.item_id, content=content)
                    logger.debug(f"文档已保存: {self.item.item_id}")
            self._close_ready = True
        except Exception as e:
            logger.error(f"发送getContent消息时出错: {e}")
            self._close_ready = True

    def update_theme(self, theme=None):
        """更新编辑器主题"""
        try:
            logger.info(f"更新编辑器主题: {theme}")
            # 这里可以实现主题更新逻辑
            # 例如，向前端发送主题更新消息
            if hasattr(self, 'backend_interface') and self.backend_interface:
                self.backend_interface.send_message('updateTheme', {'theme': theme})
        except Exception as e:
            logger.error(f"更新主题失败: {e}")

    def _check_if_save_needed(self):
        """快速检查是否需要保存"""
        # 基本条件检查
        if not (hasattr(self, 'backend_interface') and self.backend_interface):
            return False
        if not (hasattr(self, 'item') and self.item and self.item.item_id):
            return False
        return True

    def _cleanup_resources(self):
        # 释放Web通信资源
        if hasattr(self, 'backend_interface'):
            self.backend_interface.cleanup()

    def export_file(self, format):
        """
        导出指定格式的文件
        :param format: 导出文件的格式，支持 'html', 'md', 'pdf', 'epub'
        """
        content = self.item.get_text()
        export_manager = ExportManager(self, content)
        export_manager.export_file(format)