"""
通用工具函数
提供各种常用的工具方法
"""
import random
import string
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import yaml  # 新增

# 项目根目录：.../a_MyAutoTestFramework
BASE_DIR = Path(__file__).resolve().parent.parent


def generate_random_string(length: int = 10) -> str:
    """生成随机字符串"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_random_email(domain: str = "example.com") -> str:
    """生成随机邮箱"""
    username = generate_random_string(8)
    return f"{username}@{domain}"


def get_timestamp() -> int:
    """获取当前时间戳（10位）"""
    return int(time.time())


def get_timestamp_ms() -> int:
    """获取当前时间戳（13位，毫秒）"""
    return int(time.time() * 1000)


def get_current_time(format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """获取当前时间字符串"""
    return datetime.now().strftime(format_str)


def generate_user_id() -> int:
    """生成随机用户ID"""
    # 注意这里不要带逗号，否则返回的是 (int,) 元组
    return random.randint(1000, 9999)


def load_yaml(rel_path: str):
    """
    从项目根目录加载 YAML 文件，并返回解析后的内容

    Args:
        rel_path: 以项目根为基准的相对路径，例如 "data/test_message.yaml"

    Returns:
        解析后的 Python 对象（dict / list 等）
    """
    yaml_path = BASE_DIR / rel_path
    if not yaml_path.exists():
        raise FileNotFoundError(f"YAML 文件不存在: {yaml_path}")

    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
