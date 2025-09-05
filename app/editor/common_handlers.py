"""
通用处理器集合
提供所有页面类型都需要的基础handlers
"""

from utils import logger

class CommonHandlers:
    """通用处理器集合，提供所有页面类型都需要的基础handlers"""
    
    @staticmethod
    def get_common_handlers() -> dict:
        """获取通用handlers"""
        return {
            'frontendReady': CommonHandlers.frontend_ready_handler,
            'reportError': CommonHandlers.report_error_handler,
            'setValue': CommonHandlers.set_value_handler,
            'getContent': CommonHandlers.get_content_handler,
        }
    
    @staticmethod
    def frontend_ready_handler(data: dict) -> dict:
        """前端就绪处理器"""
        return {
            "success": True,
            "message": "Frontend ready acknowledged"
        }
    
    @staticmethod
    def report_error_handler(data: dict) -> dict:
        """错误报告处理器"""
        logger.error(f"前端报告错误: {data}")
        return {
            "success": True,
            "message": "Error logged"
        }
    
    @staticmethod
    def set_value_handler(data: dict) -> dict:
        """设置值处理器"""
        # 通用实现，具体页面类型可以覆盖
        logger.debug(f"收到setValue请求: {data}")
        return {
            "success": True,
            "message": "Value set"
        }
    
    @staticmethod
    def get_content_handler(data: dict) -> dict:
        """获取内容处理器"""
        # 通用实现，具体页面类型可以覆盖
        logger.debug(f"收到getContent请求: {data}")
        return {
            "success": True,
            "content": ""
        }