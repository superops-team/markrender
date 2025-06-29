import os
from db.db_manager import get_user_data_dir
import logging
from logging.handlers import TimedRotatingFileHandler


def setup_logger(
        name: str = __name__,
        log_level: int = logging.INFO) -> logging.Logger:
    """配置并返回一个标准化的日志记录器

    Args:
        name: 日志记录器名称
        log_level: 日志级别, 默认为INFO

    Returns:
        配置好的日志记录器实例
    """
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.propagate = False  # 防止日志重复传播

    # 如果已经有处理器，直接返回
    if logger.handlers:
        return logger

    # 创建日志格式
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    # 获取用户路径
    log_dir = get_user_data_dir()
    # 创建日志目录
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'app.log')
    
    # 修改文件处理器为 TimedRotatingFileHandler，设置保留 5 天日志
    file_handler = TimedRotatingFileHandler(
        log_file, when='midnight', interval=1, backupCount=5
    )
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    return logger


# 默认日志记录器
logger = setup_logger("markrender")
