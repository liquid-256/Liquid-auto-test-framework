"""
通用工具函数
提供各种常用的工具方法
"""
import random
import string
import time
from datetime import datetime
from typing import Optional


def generate_random_string(length: int = 10) -> str:
    """
    生成随机字符串
    
    Args:
        length: 字符串长度
        
    Returns:
        随机字符串
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_random_email(domain: str = "example.com") -> str:
    """
    生成随机邮箱
    
    Args:
        domain: 邮箱域名
        
    Returns:
        随机邮箱地址
    """
    username = generate_random_string(8)
    return f"{username}@{domain}"


def get_timestamp() -> int:
    """
    获取当前时间戳（10位）
    
    Returns:
        时间戳
    """
    return int(time.time())


def get_timestamp_ms() -> int:
    """
    获取当前时间戳（13位，毫秒）
    
    Returns:
        时间戳（毫秒）
    """
    return int(time.time() * 1000)


def get_current_time(format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    获取当前时间字符串
    
    Args:
        format_str: 时间格式
        
    Returns:
        时间字符串
    """
    return datetime.now().strftime(format_str)


def generate_user_id() -> int:
    """
    生成随机用户ID
    
    Returns:
        用户ID
    """
    return random.randint(1000, 9999)

