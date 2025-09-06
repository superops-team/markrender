"""
请求模型定义
定义前后端通信的请求模型
"""

class RequestModel:
    """纯Python实现的RequestModel类"""
    def __init__(self, action: str, data: dict = None, item_id: str = None):
        self.action = action
        self.data = data or {}
        self.item_id = item_id
        
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            action=data.get('action'),
            data=data.get('data'),
            item_id=data.get('itemId')
        )