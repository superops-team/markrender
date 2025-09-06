import time

from PySide6.QtCore import (
    QRunnable,
)
from db.markrender_manager import MarkRenderManager
from utils import logger


class AutoSaveWorker(QRunnable):
    """
    自动保存工作线程
    """
    def __init__(self, item_id, content):
        super().__init__()
        self.item_id = item_id
        self.content = content
        self.markrender_manager = MarkRenderManager()
        self.result = None
        self.canceled = False

    def run(self):
        if self.canceled:
            return
        try:
            save_id = self.markrender_manager.save_item(id=self.item_id, content=self.content)
            if save_id:
                logger.info(f"自动保存成功: {save_id}")
            else:
                logger.warning(f"自动保存失败")
        except Exception as e:
            logger.error(f"自动保存失败: {str(e)}")

    def cancel(self):
        """取消任务"""
        self.canceled = True

# ContentLoader类做类似修改
class ContentLoader(QRunnable):
    """
    内容加载工作线程
    """
    def __init__(self, item_id):
        super().__init__()
        self.item_id = item_id
        self.markrender_manager = MarkRenderManager()
        self.result = None

    def run(self):
        try:
            self.result = self.markrender_manager.get_detail(self.item_id)
        except Exception as e:
            logger.error(f"{self.item_id}内容加载失败: {str(e)}")