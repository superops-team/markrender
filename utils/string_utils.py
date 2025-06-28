import re
from typing import Optional, List


def trim_whitespace(text: str) -> str:
    """去除字符串首尾的空白字符

    Args:
        text: 输入字符串

    Returns:
        去除首尾空白后的字符串
    """
    return text.strip()


def split_into_lines(text: str) -> List[str]:
    """将文本按行分割

    Args:
        text: 输入文本

    Returns:
        行字符串列表
    """
    return text.split('\n')


def remove_empty_lines(text: str) -> str:
    """移除文本中的空行

    Args:
        text: 输入文本

    Returns:
        移除空行后的文本
    """
    lines = [line for line in text.split('\n') if line.strip()]
    return '\n'.join(lines)


def replace_multiple_spaces(text: str) -> str:
    """将多个连续空格替换为单个空格

    Args:
        text: 输入文本

    Returns:
        处理后的文本
    """
    return re.sub(' +', ' ', text)


def truncate_text(text: str, max_length: int, ellipsis: str = '...') -> str:
    """截断文本到指定长度，并在末尾添加省略号

    Args:
        text: 输入文本
        max_length: 最大长度
        ellipsis: 省略号字符串

    Returns:
        截断后的文本
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(ellipsis)] + ellipsis