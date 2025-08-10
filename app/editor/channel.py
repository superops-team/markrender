import json
import threading
import time
import json
import traceback

from PySide6.QtCore import QObject, Slot, QRunnable, QThreadPool, Signal, QTimer
from PySide6.QtWebChannel import QWebChannel
from utils import logger
from db.markdown_manager import MarkdownManager

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


class WebCommunicationManager(QObject):
    # 添加异步响应信号
    async_response_ready = Signal(str, bool, dict)  # task_id, success, data
    channel_ready = Signal()
    document_associated = Signal(str)
    
    # 单例实现简化
    _instance = None
    _lock = threading.Lock()
    _request_counter = 0
    
    def __init__(self, parent=None):
        # 防止重复初始化
        if hasattr(self, '_initialized'):
            return
        super().__init__(parent)
        self._initialized = True
        self.markdown_manager = MarkdownManager()
        self.python_handlers = {}
        self.ready = False
        self.page = None
        self.channel = None
        self.web_handlers = {}
        self.web_callbacks = {}
        
        # 连接信号到槽函数，确保线程安全
        self.async_response_ready.connect(self._send_async_response_safe)

    @classmethod
    def _generate_request_id(cls):
        """生成与前端格式一致的请求ID"""
        with cls._lock:
            request_id = f"req_{int(time.time() * 1000)}_{cls._request_counter}"
            cls._request_counter += 1
            return request_id

    @classmethod
    def instance(cls):
        """Singleton access method"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    # 直接调用父类构造，避免__new__二次锁定
                    cls._instance = super().__new__(cls)
                    cls._instance.__init__()  # 显式初始化
        return cls._instance

    def __init__(self, parent=None):
        # 防止重复初始化
        if hasattr(self, '_initialized'):
            return
        super().__init__(parent)
        self._initialized = True
        self.markdown_manager = MarkdownManager()  # 注入依赖
        self.python_handlers = {}
        self.ready = False  # 添加就绪状态标志
        self.page = None  # Initialize page attribute
        self.channel = None
        self.web_handlers = {}
        self.web_callbacks = {}

    @Slot(str)
    def handle_web_response(self, response_json):
        """处理前端返回的响应数据"""
        try:
            response_data = json.loads(response_json)
            request_id = response_data.get('requestId')
            result = response_data.get('result')

            if request_id and request_id in self.web_callbacks:
                callback = self.web_callbacks.pop(request_id)
                callback(result)
            else:
                logger.warning(f"未找到requestId对应的回调: {request_id}")
        except Exception as e:
            logger.error(f"处理Web响应失败: {str(e)}")

    @Slot()
    def frontend_ready(self):
        self.ready = True
        self.channel_ready.emit()

    # 添加处理器注册方法
    def register_python_handler(self,
                               action: str,
                               handler: callable,
                               is_async: bool = False):
        """注册Python处理器到通信管理器"""
        self.python_handlers[action] = (handler, is_async)

    @Slot(str, result=str)  # 添加Slot装饰器，指定参数类型和返回值类型
    def dispatch_request(self, request_json):
        """增强请求分发，添加文档ID路由"""
        try:
            request_data = json.loads(request_json)
            logger.debug(f"Received request: {request_data}")
            request = RequestModel.from_dict(request_data)
            if not request.request_id:
                logger.warning("请求缺少requestId")
                return json.dumps({
                    "success": False,
                    "requestId": request.request_id,
                    "error": "Missing requestId"
                })
            handler_tuple = self.python_handlers.get(request.action)
            if not handler_tuple:
                return json.dumps({
                    "success": False,
                    "requestId": request.request_id,
                    "error": f"Unknown action: {request.action}"
                })
            handler, is_async = handler_tuple
            # 异步处理
            if is_async:
                return self._dispatch_async_request(request, handler)
            else:
                # 同步处理 - 将文档实例作为第一个参数传递
                handler(request.data)
                return json.dumps({
                    "success": True,
                    "requestId": request.request_id,
                })
        except Exception as e:
            return json.dumps({
                "success": False,
                "requestId": request.request_id,
                "error": str(e)
            })
    
    # 添加send_message方法实现
    def send_message(self, action: str, data: dict = None, callback=None):
        """发送消息到前端页面，添加回调支持"""
        if not self.page:
            logger.warning("无法发送消息 - 页面未初始化")
            return False

        data = data or {}
        try:
            request_id = self._generate_request_id() if callback else None
            if callback and request_id:
                self.web_callbacks[request_id] = callback

            # 构造JavaScript代码，调用前端的handlePythonMessage函数
            # 使用json.dumps确保所有参数正确转义
            js_code = f"window.handlePythonMessage({json.dumps(action)}, {json.dumps(data)}, {json.dumps(request_id) if request_id else 'null'});"
            self.page.runJavaScript(js_code, lambda result: self._on_message_sent(request_id, result))
            return True
        except Exception as e:
            logger.error(f"发送消息失败: {str(e)}")
            return False

    def _on_message_sent(self, request_id, result):
        if not request_id:
            logger.debug(f"消息发送完成: 无回调消息")
            return
        logger.debug(f"收到前端响应: {request_id} - {result}")
        if request_id not in self.web_callbacks:
            if result:
                logger.warning(f"收到未知request_id的响应: {request_id} - {result}")
            return
        callback = self.web_callbacks.pop(request_id)
        try:
            # 验证响应数据结构
            if isinstance(result, dict) and 'content' in result:
                callback({'success': True, 'result': result})
            else:
                # 标准化响应格式，确保包含content字段
                callback({
                    'success': True,
                    'result': {'content': result} if not isinstance(result, dict) else result
                })
        except Exception as e:
            logger.error(f"处理回调时出错: {str(e)}, request_id: {request_id}, result: {result}")
            callback({'success': False, 'error': str(e)})
        finally:
            # 确保无论回调执行结果如何都移除回调引用
            if request_id in self.web_callbacks:
                del self.web_callbacks[request_id]            
    
    def _send_web_response(self, callback_id, result):
        response = {
            'id': callback_id,
            'result': result
        }
        js_code = f"window.handlePythonResponse({json.dumps(response)});"
        self.page.runJavaScript(js_code)

    def _send_web_error(self, callback_id, error_msg):
        response = {
            'id': callback_id,
            'error': error_msg,
            'result': None
        }
        js_code = f"window.handlePythonResponse({json.dumps(response)});"
        self.page.runJavaScript(js_code)

    def on_js_error(self, error_info):
        self.js_error_occurred.emit(error_info)
        logger.error(f"JS错误: {error_info}")

    def get_markdown_content(self, file_id):
        detail = self.markdown_manager.get_detail(file_id)
        return detail.content

    def _dispatch_async_request(self, request, handler):
        """修复后的异步请求处理"""
        task_id = request.request_id or self._generate_request_id()
        
        class AsyncRequestHandler(QRunnable):
            def __init__(self, handler, data, task_id, manager):
                super().__init__()
                self.handler = handler
                self.data = data
                self.task_id = task_id
                self.manager = manager
                self.setAutoDelete(True)
            
            def run(self):
                try:
                    result = self.handler(self.data)
                    if result is None:
                        result = {"success": True}
                    # 通过信号槽机制发送结果到主线程
                    self.manager.async_response_ready.emit(self.task_id, True, result)
                except Exception as e:
                    logger.error(f"异步任务失败: {str(e)}, traceback: {traceback.format_exc()}")
                    self.manager.async_response_ready.emit(
                        self.task_id, False, {"error": str(e), "success": False}
                    )
        
        # 使用全局线程池
        thread_pool = QThreadPool.globalInstance()
        if thread_pool.activeThreadCount() < thread_pool.maxThreadCount():
            thread_pool.start(AsyncRequestHandler(handler, request.data, task_id, self))
        else:
            # 线程池满，延迟执行
            QTimer.singleShot(10, lambda: self._dispatch_async_request(request, handler))
        
        return json.dumps({
            "success": True,
            "task_id": task_id,
            "message": "任务已提交到线程池"
        })

    @Slot(str, bool, dict)
    def _send_async_response_safe(self, task_id, success, data):
        """线程安全的响应发送"""
        if self.page and hasattr(self.page, 'runJavaScript'):
            try:
                response_data = json.dumps({
                    "success": success,
                    "task_id": task_id,
                    "data": data
                })
                js_code = f"window.handleAsyncResponse('{task_id}', {response_data})"
                self.page.runJavaScript(js_code)
            except Exception as e:
                logger.error(f"发送异步响应失败: {str(e)}")

    def cleanup(self):
        """增强清理逻辑"""
        if self.channel:
            self.channel = None
        if self.page:
            try:
                self.page.setWebChannel(None)
            except:
                pass  # 页面可能已销毁
        self.web_callbacks.clear()
        
        # 清理线程池
        thread_pool = QThreadPool.globalInstance()
        thread_pool.waitForDone(1000)  # 等待1秒
    
    def call_web_method(self, method, params=None, callback=None):
        """调用Web端方法"""
        if not self.page or not self.channel:
            logger.error("Web page not attached")
            return
        
        request_id = self._generate_request_id() if callback else None
        if callback and request_id:
            self.web_callbacks[request_id] = callback
        
        js_code = f"window.handlePythonMessage('{method}', {json.dumps(params or {})}, '{request_id or ''}')"
        self.page.runJavaScript(js_code)
    
    @Slot(str, str)
    def on_web_response(self, request_id, response_json):
        """处理Web端响应"""
        callback = self.web_callbacks.pop(request_id, None)
        if callback:
            try:
                response = json.loads(response_json)
                callback(response.get('success'), response.get('result'), response.get('error'))
            except Exception as e:
                callback(False, None, str(e))

    def attach_to_page(self, page):
        """附加到页面并初始化WebChannel"""
        if self.page == page:
            return
        
        self.page = page
        self._init_channel()
        
    def _init_channel(self):
        """内部初始化QWebChannel"""
        if self.channel:
            del self.channel
        
        self.channel = QWebChannel()
        self.channel.registerObject('backendInterface', self)
        self.page.setWebChannel(self.channel)
        self.channel_ready.emit()
    
    def cleanup(self):
        """清理资源"""
        if self.channel:
            self.channel = None
        if self.page:
            self.page.setWebChannel(None)
        self.web_callbacks.clear()