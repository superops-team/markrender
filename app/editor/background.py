import time
import threading

from PySide6.QtCore import (
    QObject,
    QRunnable,
    QThreadPool,
    QMetaObject,
    Qt,
    Slot,
    QMutex,
    Signal,
    Q_ARG,
)
from db.markrender_manager import MarkRenderManager
from utils import logger

class ThreadPoolManager(QObject):
    """
    线程池管理器
    提供任务提交、取消、完成回调等功能
    """
    task_started = Signal(str)
    task_completed = Signal(str, object)
    task_failed = Signal(str, str)
    task_canceled = Signal(str)
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        # 双重检查锁定实现线程安全单例
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, parent=None):
        super().__init__(parent)
        self.thread_pool = QThreadPool.globalInstance()
        self.thread_pool.setMaxThreadCount(5)  # 限制最大线程数
        self.active_tasks = {}
        self.task_map = {}  # 任务ID到任务包装器的映射
        self.task_mutex = QMutex()  # 添加互斥锁
        self.max_task_queue_size = 20  # 最大任务队列大小

    def submit_task(self, task_id, worker, callback, timeout=30000):
        """提交任务，带超时设置(毫秒)"""
        # 检查队列大小
        if len(self.active_tasks) >= self.max_task_queue_size:
            logger.error("任务队列已满")
            return False

        self.task_mutex.lock()
        try:
            if task_id in self.active_tasks:
                logger.warning(f"任务 {task_id} 已存在")
                return False
            wrapper = self.TaskWrapper(worker, callback, task_id, self, timeout)
            self.active_tasks[task_id] = wrapper
            self.thread_pool.start(wrapper)
            self.task_started.emit(task_id)
            return True
        finally:
            self.task_mutex.unlock()

    class TaskWrapper(QRunnable):
        def __init__(self, worker, callback, task_id, manager, timeout=30000):
            super().__init__()
            self.worker = worker
            self.callback = callback
            self.task_id = task_id
            self.manager = manager
            self.canceled = False
            self.start_time = None
            self.timeout = timeout  # 任务超时时间(毫秒)

        def run(self):
            self.start_time = time.time()
            try:
                if self.canceled:
                    logger.info(f"任务 {self.task_id} 已取消")
                    self.manager.task_canceled.emit(self.task_id)
                    return

                result = self.worker.run()
                # 调用回调函数
                if self.callback:
                    logger.info(f"任务 {self.task_id} 完成")
                    QMetaObject.invokeMethod(  # pyright: ignore[reportCallIssue]
                        self.manager,
                        "on_task_complete",
                        Qt.QueuedConnection,
                        Q_ARG(str, self.task_id),
                        Q_ARG(str, str(result))
                    )
            except Exception as e:
                logger.error(f"任务 {self.task_id} 运行时出错: {e}")
                QMetaObject.invokeMethod(  # pyright: ignore[reportCallIssue]
                    self.manager,
                    "on_task_error",
                    Qt.QueuedConnection,
                    Q_ARG(str, self.task_id),
                    Q_ARG(str, str(e))
                )

    @Slot(str, str)
    def on_task_complete(self, task_id, result):
        self.task_mutex.lock()
        try:
            if task_id in self.active_tasks:
                wrapper = self.active_tasks.pop(task_id)
                # 调用用户提供的回调
                if wrapper.callback:
                    wrapper.callback(task_id, result)
                # 调用完成信号
                self.task_completed.emit(task_id, result)
        finally:
            self.task_mutex.unlock()

    @Slot(str, str)
    def on_task_error(self, task_id, error):
        self.task_mutex.lock()
        try:
            if task_id in self.active_tasks:
                wrapper = self.active_tasks.pop(task_id)
                # 调用用户提供的回调（如果有）
                if wrapper.callback:
                    wrapper.callback(None, error)
                logger.error(f"任务 {task_id} 失败: {error}")
        finally:
            self.task_mutex.unlock()

    # 添加带超时的互斥锁操作
    def _safe_task_operation(self, operation, timeout=1000):
        """安全执行任务操作，带超时处理"""
        if self.task_mutex.tryLock(timeout):
            try:
                return operation()
            finally:
                self.task_mutex.unlock()
        logger.warning("获取任务锁超时")
        return None

    def cancel_task(self, task_id):
        if task_id in self.active_tasks:
            # 设置取消标志
            self.active_tasks[task_id].canceled = True
            logger.info(f"任务 {task_id} 已取消")

    def shutdown(self, wait_ms=5000):
        """优雅关闭线程池"""
        # 取消所有任务
        self._safe_task_operation(lambda: [self.cancel_task(tid) for tid in list(self.active_tasks.keys())])

        # 等待任务完成
        if not self.thread_pool.waitForDone(wait_ms):
            logger.warning(f"线程池关闭超时，仍有{self.thread_pool.activeThreadCount()}个活跃线程")

        # 清除任务
        self._safe_task_operation(lambda: self.active_tasks.clear())
        logger.info("线程池已关闭")

    def cancel_all_tasks(self):
        """取消所有未执行的任务"""
        with self._lock:
            for task_id in list(self.active_tasks.keys()):
                self.cancel_task(task_id)

    def wait_for_completion(self, timeout_ms=1000):
        """等待所有任务完成"""
        start_time = time.time()
        while self.active_tasks and (time.time() - start_time) * 1000 < timeout_ms:
            time.sleep(0.1)  # 短暂休眠减少CPU占用
        return len(self.active_tasks) == 0


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

    def run(self):  # pyright: ignore[reportIncompatibleMethodOverride]
        if self.canceled:
            return False
        try:
            save_id = self.markrender_manager.save_item(id=self.item_id, content=self.content)
            if save_id:
                success = True
                logger.info(f"自动保存成功: {save_id}")
            else:
                success = False
                logger.warning(f"自动保存失败")
            return success
        except Exception as e:
            logger.error(f"自动保存失败: {str(e)}")
            return False

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
            return self.result
        except Exception as e:
            logger.error(f"{self.item_id}内容加载失败: {str(e)}")
            return {}