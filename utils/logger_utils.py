import os
import logging
from logging.handlers import TimedRotatingFileHandler
from logging import StreamHandler

from db import db_manager


def setup_logger():
    # 创建日志器
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 创建文件处理器
    log_file = os.path.join(db_manager.get_user_data_dir(), 'app.log')
    # 修改 backupCount 参数为 7，实现保留 7 天日志
    file_handler = TimedRotatingFileHandler(
        log_file, when='midnight', interval=1, backupCount=7
    )
    
    # 修改日志格式，添加调用文件和所在行信息
    log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
    
    file_handler.setFormatter(log_format)

    # 创建控制台处理器
    console_handler = StreamHandler()
    console_handler.setFormatter(log_format)

    # 将处理器添加到日志器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger = logging.getLogger(__name__)
    logger.info("Logger setup complete, path=%s", log_file)
    return logger

# 默认日志记录器
logger = setup_logger()