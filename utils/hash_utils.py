import hashlib


def calculate_md5(content: str) -> str:
    """计算字符串内容的MD5哈希值

    Args:
        content: 要计算哈希的字符串内容

    Returns:
        32位小写MD5哈希值
    """
    return hashlib.md5(content.encode()).hexdigest()


def calculate_sha256(content: str) -> str:
    """计算字符串内容的SHA256哈希值

    Args:
        content: 要计算哈希的字符串内容

    Returns:
        64位小写SHA256哈希值
    """
    return hashlib.sha256(content.encode()).hexdigest()
