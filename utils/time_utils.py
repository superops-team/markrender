from datetime import datetime, timezone, timedelta
from typing import Optional

def now():
    # 创建北京时间时区（UTC+8）
    beijing_tz = timezone(timedelta(hours=8))
    # 获取当前北京时间
    now = datetime.now(beijing_tz)
    return now

def get_current_timestamp() -> str:
    """获取当前UTC时间戳，格式为ISO 8601

    Returns:
        ISO 8601格式的UTC时间字符串，如'2023-11-15T12:30:45.123456+00:00'
    """
    return now().isoformat()

def get_duration(start: datetime, end: datetime):
    return end - start

def format_datetime(
        dt: Optional[datetime] = None,
        fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
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

def get_readable_time(modified_time: datetime):
    if isinstance(modified_time, datetime):
        # 确保 now 和 modified_time 时区一致
        if modified_time.tzinfo is None:
            now = datetime.now()
        else:
            now = datetime.now(timezone.utc)
        delta = now - modified_time
        if delta < timedelta(seconds=60):
            return f'{delta.seconds}秒前'
        elif delta < timedelta(minutes=60):
            return f'{delta.seconds // 60}分钟前'
        elif delta < timedelta(hours=24):
            return f'{delta.seconds // 3600}小时前'
        elif delta < timedelta(days=30):
            return f'{delta.days}天前'
        elif delta < timedelta(days=365):
            return f'{delta.days // 30}个月前'
        else:
            return f'{delta.days // 365}年前'
    return str(modified_time)

def parse_datetime(
        datetime_str: str,
        fmt: str = '%Y-%m-%d %H:%M:%S') -> datetime:
    """将字符串解析为datetime对象

    Args:
        datetime_str: 日期时间字符串
        fmt: 解析格式，默认为'%Y-%m-%d %H:%M:%S'

    Returns:
        解析后的datetime对象
    """
    return datetime.strptime(datetime_str, fmt)
