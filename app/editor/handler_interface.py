"""
处理器接口定义
定义统一的处理器接口，确保所有处理器有一致的签名
"""

from utils import logger

class HandlerInterface:
    """统一的处理器接口，确保所有处理器有一致的签名"""
    def __init__(self, name: str):
        self.name = name
    
    def handle(self, data: dict) -> dict:
        """处理请求并返回结果"""
        raise NotImplementedError("子类必须实现handle方法")

class DefaultHandler(HandlerInterface):
    """默认处理器实现"""
    def __init__(self, name: str, handler_func: callable):
        super().__init__(name)
        self.handler_func = handler_func
    
    def handle(self, data: dict) -> dict:
        """处理请求并返回结果"""
        try:
            result = self.handler_func(data)
            if isinstance(result, dict):
                return result
            else:
                return {"success": True, "data": result}
        except Exception as e:
            logger.error(f"处理器 {self.name} 执行失败: {str(e)}", exc_info=True)
            return {"success": False, "error": str(e)}