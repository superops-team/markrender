from datetime import datetime, timezone
from typing import Optional


def get_current_timestamp() -> str:
    """获取当前UTC时间戳，格式为ISO 8601

    Returns:
        ISO 8601格式的UTC时间字符串，如'2023-11-15T12:30:45.123456+00:00'
    """
    return datetime.now(timezone.utc).isoformat()


def format_datetime(dt: Optional[datetime] = None, fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
    """格式化日期时间为指定字符串格式

    Args:
        dt: 要格式化的datetime对象，默认为当前本地时间
        fmt: 日期时间格式字符串，默认为'%Y-%m-%d %H:%M:%S'

    Returns:
        格式化后的日期时间字符串
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime(fmt)


def parse_datetime(datetime_str: str, fmt: str = '%Y-%m-%d %H:%M:%S') -> datetime:
    """将字符串解析为datetime对象

    Args:
        datetime_str: 日期时间字符串
        fmt: 解析格式，默认为'%Y-%m-%d %H:%M:%S'

    Returns:
        解析后的datetime对象
    """
    return datetime.strptime(datetime_str, fmt)