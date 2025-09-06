import json
import threading

from PySide6.QtCore import QObject, Slot, QRunnable, QThreadPool, Signal, QEventLoop, QTimer
from PySide6.QtWebEngineCore import QWebEnginePage
from utils import logger
from db.markrender_manager import MarkRenderManager
# Add the import statement at the top with other imports
from app.editor.js_scripts import JSScriptManager

# 纯Python实现的RequestModel类
class RequestModel:
    def __init__(self, action: str, data: dict = None, request_id: str = None):
        self.action = action
        self.data = data or {}
        self.request_id = request_id
        
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            action=data.get('action'),
            data=data.get('data'),
            request_id=data.get('requestId')
        )


class BackendInterface(QObject):
    # 信号定义
    js_error_occurred = Signal(str)
    async_response_ready = Signal(str, bool, dict)  # 添加异步响应信号
    
    def __init__(self, page_type: str, parent=None):
        super().__init__(parent)
        self.page_type = page_type
        self.markdown_manager = MarkRenderManager()
        self.item_map = {}
        self.handlers = {}
        self.web_callbacks = {}
        self.page = None  # 添加page属性，初始为None
        # 移除ready属性，不再需要WebChannel就绪状态
    
    def set_page(self, page):
        """设置页面对象"""
        self.page = page
    
    def set_page_type(self, page_type):
        """设置页面类型"""
        self.page_type = page_type
        
    def attach_to_page_manager(self, page_manager):
        """附加到页面管理器并获取页面对象"""
        success = page_manager.set_backend_interface(self.page_type, self)
        if success:
            logger.debug(f"通信管理器 {self.page_type} 成功附加到页面管理器")
        else:
            logger.warning(f"通信管理器 {self.page_type} 附加到页面管理器失败")
        return success
    
    # 移除handle_web_response方法，不再需要处理前端响应
    
    # 移除frontend_ready方法，不再需要前端就绪回调
        
    # 添加处理器注册方法
    def register_handler(self, action: str, handler: callable, is_async: bool = False):
        """注册Python处理器到通信管理器"""
        self.handlers[action] = (handler, is_async)

    # 移除dispatch_request方法，不再需要处理前端请求

    def send_message_sync(self, action: str, data: dict = None, item_id: str = None, timeout: int = 15000):
        """
        同步发送消息到前端页面，使用QEventLoop阻塞主线程直到获取到数据
        """
        if not self.page:
            logger.warning(f"[{self.page_type}] 无法发送消息 - 页面未初始化")
            return {'success': False, 'error': '页面未初始化'}
            
        data = data or {}
        result = None
        error_occurred = False
        error_message = ""
        
        try:
            # 根据action构造相应的JavaScript代码
            js_code = self._construct_js_code(action, data, item_id)
            
            if not js_code:
                logger.error(f"[{self.page_type}] 无法构造JavaScript代码: {action}")
                return {'success': False, 'error': '无法构造JavaScript代码'}

            logger.debug(f"[{self.page_type}] 同步执行JavaScript代码: {js_code[:100]}...")
            
            # 创建事件循环
            loop = QEventLoop()
            
            # 设置超时定时器
            timeout_timer = QTimer()
            timeout_timer.setSingleShot(True)
            timeout_timer.timeout.connect(lambda: (
                logger.error(f"[{self.page_type}] JavaScript执行超时: {action}"),
                setattr(self, '_sync_error', True),
                setattr(self, '_sync_error_message', 'JavaScript执行超时'),
                loop.quit()
            ))
            timeout_timer.start(timeout)
            
            # 执行JavaScript代码并等待结果
            def js_callback(js_result):
                nonlocal result
                try:
                    logger.debug(f"[{self.page_type}] JavaScript执行完成，action: {action}, result: {js_result}")
                    
                    # 解析JSON结果
                    if isinstance(js_result, str):
                        try:
                            result = json.loads(js_result)
                            logger.debug(f"[{self.page_type}] 解析后的结果: {result}")
                        except json.JSONDecodeError:
                            # 如果不是JSON格式，直接返回原始结果
                            result = js_result
                    else:
                        result = js_result
                        
                except Exception as e:
                    logger.error(f"[{self.page_type}] 处理JavaScript结果时出错: {str(e)}", exc_info=True)
                    error_occurred = True
                    error_message = str(e)
                finally:
                    # 停止超时定时器并退出事件循环
                    timeout_timer.stop()
                    loop.quit()
            
            # 执行JavaScript
            self.page.runJavaScript(js_code, js_callback)
            
            # 运行事件循环直到获取到结果或超时
            loop.exec()
            
            # 检查是否有错误
            if hasattr(self, '_sync_error') and self._sync_error:
                delattr(self, '_sync_error')
                error_msg = getattr(self, '_sync_error_message', '未知错误')
                if hasattr(self, '_sync_error_message'):
                    delattr(self, '_sync_error_message')
                return {'success': False, 'error': error_msg}
            
            if error_occurred:
                return {'success': False, 'error': error_message}
                
            # 如果没有结果，返回空结果
            if result is None:
                logger.warning(f"[{self.page_type}] JavaScript执行返回空结果: {action}")
                return {'success': True, 'content': ''}
                
            return result
            
        except Exception as e:
            logger.error(f"[{self.page_type}] 同步执行JavaScript失败: {str(e)}", exc_info=True)
            return {'success': False, 'error': f'同步执行JavaScript失败: {str(e)}'}

    def send_message(self, action: str, data: dict = None, callback=None, item_id: str = None):
        """发送消息到前端页面，改为直接执行JavaScript"""
        if not self.page:
            logger.warning(f"[{self.page_type}] 无法发送消息 - 页面未初始化")
            return False
            
        data = data or {}
        try:
            # 根据action构造相应的JavaScript代码
            js_code = self._construct_js_code(action, data, item_id)
            
            if not js_code:
                logger.error(f"[{self.page_type}] 无法构造JavaScript代码: {action}")
                return False

            logger.debug(f"[{self.page_type}] 执行JavaScript代码: {js_code[:100]}...")
            
            # 执行JavaScript代码
            if callback:
                self.page.runJavaScript(js_code, lambda result: self._handle_js_result(result, callback, action))
            else:
                self.page.runJavaScript(js_code, lambda result: self._log_js_result(result, action))
                
            return True
        except Exception as e:
            logger.error(f"[{self.page_type}] 执行JavaScript失败: {str(e)}", exc_info=True)
            return False

    def _construct_js_code(self, action: str, data: dict, item_id: str = None):
        """根据action构造相应的JavaScript代码"""
        try:
            # 使用JSScriptManager获取预定义的脚本
            if action == "setValue":
                content = data.get("content", "")
                item_id_param = data.get("item_id", item_id or "")
                # 转义内容中的特殊字符
                return JSScriptManager.get_script("set_editor_content", content=content, item_id=item_id_param)
            elif action == "getContent":
                return JSScriptManager.get_script("get_editor_content")
            elif action == "getCurrentItemId":
                return JSScriptManager.get_script("get_current_item_id")
            elif action == "setCurrentItemId":
                item_id_param = data.get("item_id", "")
                return JSScriptManager.get_script("set_current_item_id", item_id=item_id_param)
            elif action == "reset":
                return JSScriptManager.get_script("reset_editor_content")
            elif action == "registerEditorEvents":
                return JSScriptManager.get_script("register_editor_events")
            elif action == "setupContentChangeListener":
                return JSScriptManager.get_script("setup_content_change_listener")
            elif action == "textChanged":
                return JSScriptManager.get_script("text_changed")
            else:
                # 对于其他action，构造通用的消息处理代码
                return JSScriptManager.get_script("handle_backend_message", 
                                                action=action, 
                                                data=data, 
                                                request_id=item_id or "")
        except Exception as e:
            logger.error(f"[{self.page_type}] 构造JavaScript代码时出错: {str(e)}", exc_info=True)
            return None

    def _handle_js_result(self, result, callback, action):
        """处理JavaScript执行结果"""
        try:
            logger.debug(f"[{self.page_type}] JavaScript执行完成，action: {action}, result: {result}")
            
            # 解析JSON结果
            if isinstance(result, str):
                try:
                    parsed_result = json.loads(result)
                    logger.debug(f"[{self.page_type}] 解析后的结果: {parsed_result}")
                    callback(parsed_result)
                    return
                except json.JSONDecodeError:
                    # 如果不是JSON格式，直接返回原始结果
                    pass
            
            # 直接返回结果
            callback(result)
        except Exception as e:
            logger.error(f"[{self.page_type}] 处理JavaScript结果时出错: {str(e)}", exc_info=True)
            # 即使处理结果出错，也要调用回调函数
            try:
                callback(None)
            except:
                pass

    def _log_js_result(self, result, action):
        """仅记录JavaScript执行结果"""
        logger.debug(f"[{self.page_type}] JavaScript执行完成，action: {action}, result: {result}")

    def _on_message_sent(self, request_id, result):
        # 简化处理，不再需要复杂的回调机制
        logger.debug(f"[{self.page_type}] JavaScript执行完成")
    
    def _generate_request_id(self):
        """已废弃：不再生成随机请求ID，使用item id代替"""
        import uuid
        logger.warning("_generate_request_id方法已废弃，请使用item id作为request标识")
        return str(uuid.uuid4())
    
    def _send_web_response(self, callback_id, result):
        # 不再需要发送响应到前端
        pass

    def _send_web_error(self, callback_id, error_msg):
        # 不再需要发送错误到前端
        pass
    
    def _dispatch_async_request(self, request: RequestModel, handler: callable):
        # 不再需要异步请求分发
        pass
    
    def cleanup(self):
        # 简化清理过程
        self.web_callbacks.clear()