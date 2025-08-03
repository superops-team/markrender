import json
import uuid
import threading

from PySide6.QtCore import QObject, Slot, QRunnable, QThreadPool
from pydantic import BaseModel, ValidationError, Field
from PySide6.QtCore import Signal
from PySide6.QtWebChannel import QWebChannel
from utils import logger

# 添加RequestModel定义
class RequestModel(BaseModel):
    action: str
    data: dict = Field(default_factory=dict)
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class WebCommunicationManager(QObject):
    # 删除重复的text_changed定义
    # 添加channel_ready信号定义
    channel_ready = Signal()
    
    # 单例实现简化
    _instance = None
    _lock = threading.Lock()  # 保留线程安全锁

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

    def __init__(self, markdown_manager=None, parent=None):
        # 防止重复初始化
        if hasattr(self, '_initialized'):
            return
        super().__init__(parent)
        self._initialized = True
        self.markdown_manager = markdown_manager  # 注入依赖
        self.python_handlers = {}
        self.document_map = {}
        self.ready = False  # 添加就绪状态标志
        self.page = None  # Initialize page attribute
        self.channel = None
        self.web_handlers = {}
        self.web_callbacks = {}
        self.document_map = {}  # 文档ID到MarkdownDocument的映射

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
        # 延迟发送的初始化消息可以在这里触发

    # 添加处理器注册方法
    def register_python_handler(self,
                               action: str,
                               handler: callable,
                               is_async: bool = False):
        """注册Python处理器到通信管理器"""
        # Store handler and async flag as tuple
        self.python_handlers[action] = (handler, is_async)

    # 添加文档注册处理器
    def register_document_handler(self, document):
        """注册文档到document_map"""
        if document.file_id:
            self.document_map[document.file_id] = document
            return True
        return False

    @Slot(str, result=str)  # 添加Slot装饰器，指定参数类型和返回值类型
    def dispatch_request(self, request_json):
        """增强请求分发，添加文档ID路由"""
        try:
            request_data = json.loads(request_json)
            request = RequestModel(**request_data)
            # 从请求数据中提取文档ID
            doc_id = request.data.get("docId")
            document = self.document_map.get(doc_id)

            if not document and request.action != "registerDocument":
                existing_ids = list(self.document_map.keys())
                return json.dumps({
                    "success": False,
                    "error": f"Document {doc_id} not found. Existing IDs: {existing_ids}"
                })
            handler_tuple = self.python_handlers.get(request.action)
            if not handler_tuple:
                return json.dumps({
                    "success": False,
                    "error": f"Unknown action: {request.action}"
                })
            handler, is_async = handler_tuple
            
            # 使用线程池处理耗时操作
            # 修改处理器调用方式
            if is_async:
                return self._dispatch_async_request(request, handler, document)
            else:
                # 同步处理 - 将文档实例作为第一个参数传递
                result = handler(document, **request.data)
                return json.dumps({
                    "success": True,
                    "result": result
                })
        except ValidationError as e:
            return json.dumps({
                "success": False,
                "error": f"Validation error: {str(e)}"
            })
        except Exception as e:
            return json.dumps({
                "success": False,
                "error": str(e)
            })

    def send_web_request(self, action, data=None, callback=None):
        if not self.channel or not self.document:
            return

        request_id = str(uuid.uuid4())
        if callback:
            self.web_callbacks[request_id] = callback

        request = {
            'id': request_id,
            'action': action,
            'data': data or {}
        }

        js_code = f"window.dispatchWebRequest({json.dumps(request)});"
        self.document.page().runJavaScript(js_code)
    
    # 添加send_message方法实现
    def send_message(self, action: str, data: dict = None, callback=None):
        """发送消息到前端页面，添加回调支持"""
        if not self.page:
            logger.warning("无法发送消息 - 页面未初始化")
            return False

        data = data or {}
        try:
            request_id = str(uuid.uuid4()) if callback else None
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
        if request_id:
            logger.debug(f"收到前端响应: {request_id} - {result}")
            if request_id in self.web_callbacks:
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
                    logger.error(f"处理回调时出错: {str(e)}")
                    callback({'success': False, 'error': str(e)})
                finally:
                    # 确保无论回调执行结果如何都移除回调引用
                    if request_id in self.web_callbacks:
                        del self.web_callbacks[request_id]
            else:
                logger.warning(f"收到未知request_id的响应: {request_id}")
        logger.debug(f"消息发送完成: {request_id or '无回调消息'}")
    
    def _send_web_response(self, callback_id, result):
        response = {
            'id': callback_id,
            'result': result
        }
        js_code = f"window.handlePythonResponse({json.dumps(response)});"
        self.document.page().runJavaScript(js_code)

    def _send_web_error(self, callback_id, error_msg):
        response = {
            'id': callback_id,
            'error': error_msg,
            'result': None
        }
        js_code = f"window.handlePythonResponse({json.dumps(response)});"
        self.document.page().runJavaScript(js_code)

    # 默认处理器实现
    def on_content_changed(self, content):
        self.content_changed.emit(content)  # 发射信号而非直接调用

    def on_js_error(self, error_info):
        self.js_error_occurred.emit(error_info)
        logger.error(f"JS错误: {error_info}")

    def get_markdown_content(self, file_id):
        return self.markdown_manager.get_markdown_content(file_id)

    def _dispatch_async_request(self, request, handler):
        """异步请求处理"""
        task_id = str(uuid.uuid4())
        
        class AsyncRequestHandler(QRunnable):
            def __init__(self, handler, data, task_id, manager):
                super().__init__()
                self.handler = handler
                self.data = data
                self.task_id = task_id
                self.manager = manager
            
            def run(self):
                try:
                    result = self.handler(**self.data)
                    self.manager._send_async_response(
                        self.task_id, True, result
                    )
                except Exception as e:
                    self.manager._send_async_response(
                        self.task_id, False, str(e)
                    )
        
        # 提交到线程池
        QThreadPool.globalInstance().start(
            AsyncRequestHandler(handler, request.data, task_id, self)
        )
        
        # 返回任务ID
        return json.dumps({
            "success": True,
            "task_id": task_id
        })
    
    def _send_async_response(self, task_id, success, data):
        """发送异步响应到Web端"""
        if self.page:
            js_code = f"window.handleAsyncResponse('{task_id}', {success}, {json.dumps(data)})"
            self.page.runJavaScript(js_code)
    
    def call_web_method(self, method, params=None, callback=None):
        """调用Web端方法"""
        if not self.page or not self.channel:
            logger.error("Web page not attached")
            return
        
        request_id = str(uuid.uuid4()) if callback else None
        if callback and request_id:
            self.web_callbacks[request_id] = callback
        
        js_code = f"window.webComm.callMethod('{method}', {json.dumps(params or {})}, '{request_id or ''}')"
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

    def on_document_text_changed(self, text):
        """转发文档变更到前端"""
        self.send_message("textChanged", {"content": text})

    def unregister_document(self, file_id):
        """注销文档对象"""
        if file_id:
            logger.info(f"注销文档对象: {file_id}")
        if self.channel:
            self.channel = None
    
    def cleanup(self):
        """清理资源"""
        if self.channel:
            self.channel = None
        if self.page:
            self.page.setWebChannel(None)
        self.web_callbacks.clear()