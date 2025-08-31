import json
import traceback

from PySide6.QtCore import QObject, Slot, QRunnable, QThreadPool, Signal, QTimer
from PySide6.QtWebChannel import QWebChannel
from utils import logger
from db.markrender_manager import MarkRenderManager

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
    # 信号定义
    channel_ready = Signal()
    js_error_occurred = Signal(str)
    async_response_ready = Signal(str, bool, dict)  # 添加异步响应信号
    
    # 移除单例模式，每个页面一个实例
    def __init__(self, page_id: str, parent=None):
        super().__init__(parent)
        self.page_id = page_id
        self.markdown_manager = MarkRenderManager()
        self.python_handlers = {}
        self.web_callbacks = {}
        self.page = None  # 添加page属性，初始为None
        self.ready = False
        self.page_type = None  # 添加页面类型属性
    
    def set_page(self, page):
        """设置页面对象"""
        self.page = page
        
    def set_page_type(self, page_type):
        """设置页面类型"""
        self.page_type = page_type
        
    def attach_to_page_manager(self, page_manager):
        """附加到页面管理器并获取页面对象"""
        page_manager.set_backend_interface(self.page_id, self)
        # 获取对应的页面对象
        if hasattr(page_manager, 'get_page'):
            self.page = page_manager.get_page(self.page_id)
        elif hasattr(page_manager, 'pages') and self.page_id in page_manager.pages:
            self.page = page_manager.pages[self.page_id].page()
        
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
        """前端就绪回调"""
        logger.info(f"[{self.page_id}] 前端就绪回调被调用")
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
            logger.debug(f"[{self.page_id}] Received request: {request_data}")
            request = RequestModel.from_dict(request_data)
            if not request.request_id:
                logger.warning(f"[{self.page_id}] 请求缺少requestId")
                return json.dumps({
                    "success": False,
                    "requestId": request.request_id,
                    "error": "Missing requestId"
                })
            handler_tuple = self.python_handlers.get(request.action)
            if not handler_tuple:
                logger.warning(f"[{self.page_id}] 未知的action: {request.action}")
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
                # 同步处理 - 调用处理器并获取返回结果
                result = handler(request.data)
                
                # 处理器可能返回不同格式的结果
                if isinstance(result, dict):
                    # 如果处理器返回字典，直接使用
                    response_data = {
                        "requestId": request.request_id,
                        **result  # 展开处理器返回的结果
                    }
                else:
                    # 如果处理器返回其他类型，包装为标准格式
                    response_data = {
                        "success": True,
                        "requestId": request.request_id,
                        "data": result
                    }
                
                logger.debug(f"[{self.page_id}] 返回响应: {response_data}")
                return json.dumps(response_data)
        except Exception as e:
            logger.error(f"[{self.page_id}] 处理请求失败: {str(e)}", exc_info=True)
            return json.dumps({
                "success": False,
                "requestId": request.request_id,
                "error": str(e)
            })
    
    # 添加send_message方法实现
    def send_message(self, action: str, data: dict = None, callback=None):
        """发送消息到前端页面，添加回调支持"""
        if not self.page:
            logger.warning(f"[{self.page_id}] 无法发送消息 - 页面未初始化")
            return False

        data = data or {}
        try:
            request_id = self._generate_request_id() if callback else None
            if callback and request_id:
                self.web_callbacks[request_id] = callback

            # 构造JavaScript代码，调用前端的handlePythonMessage函数
            # 使用json.dumps确保所有参数正确转义
            js_code = f"window.handlePythonMessage({json.dumps(action)}, {json.dumps(data)}, {json.dumps(request_id) if request_id else 'null'});"
            logger.debug(f"[{self.page_id}] 发送JavaScript代码: {js_code[:100]}...")
            self.page.runJavaScript(js_code, lambda result: self._on_message_sent(request_id, result))
            return True
        except Exception as e:
            logger.error(f"[{self.page_id}] 发送消息失败: {str(e)}", exc_info=True)
            return False

    def _on_message_sent(self, request_id, result):
        if not request_id:
            logger.debug(f"[{self.page_id}] 消息发送完成: 无回调消息")
            return
        logger.debug(f"[{self.page_id}] 收到前端响应: {request_id} - {result}")
        if request_id not in self.web_callbacks:
            if result:
                logger.warning(f"[{self.page_id}] 收到未知request_id的响应: {request_id} - {result}")
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
            import traceback
            logger.error(f"[{self.page_id}] 处理回调时出错: {str(traceback.format_exc())}, request_id: {request_id}, result: {result}")
            callback({'success': False, 'error': e})
        finally:
            # 确保无论回调执行结果如何都移除回调引用
            if request_id in self.web_callbacks:
                del self.web_callbacks[request_id]            
    
    def _generate_request_id(self):
        """生成唯一的请求ID"""
        import uuid
        return str(uuid.uuid4())
    
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
            'error': error_msg
        }
        js_code = f"window.handlePythonResponse({json.dumps(response)});"
        self.page.runJavaScript(js_code)
    
    def _dispatch_async_request(self, request: RequestModel, handler: callable):
        """异步请求分发"""
        request_id = request.request_id
        
        def async_handler():
            try:
                result = handler(request.data)
                response_data = {
                    "success": True,
                    "requestId": request_id,
                    "data": result
                }
                response_json = json.dumps(response_data)
                self.async_response_ready.emit(request_id, True, response_data)
                return response_json
            except Exception as e:
                logger.error(f"异步处理请求失败: {str(e)}", exc_info=True)
                response_data = {
                    "success": False,
                    "requestId": request_id,
                    "error": str(e)
                }
                self.async_response_ready.emit(request_id, False, response_data)
                return json.dumps(response_data)
        
        # 使用线程池执行异步任务
        QThreadPool.globalInstance().start(QRunnable.create(async_handler))
        # 返回一个临时响应，表示请求已接受
        return json.dumps({
            "success": True,
            "requestId": request_id,
            "message": "Request accepted for async processing"
        })
    
    def cleanup(self):
        self.web_callbacks.clear()