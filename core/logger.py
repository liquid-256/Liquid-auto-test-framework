"""
日志管理模块
提供统一的日志记录功能
"""
import logging
import os
from pathlib import Path
from datetime import datetime

# 获取项目根目录
BASE_DIR = Path(__file__).parent.parent

# 日志目录
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

# 日志文件路径
LOG_FILE = LOG_DIR / f"test_{datetime.now().strftime('%Y%m%d')}.log"


def setup_logger(name: str = __name__, level: str = 'INFO') -> logging.Logger:
    """
    设置日志记录器
    
    Args:
        name: 日志记录器名称（通常是模块名）
        level: 日志级别（DEBUG、INFO、WARNING、ERROR）
        
    Returns:
        Logger对象
    """
    logger = logging.getLogger(name)
    
    # 如果已经配置过，直接返回
    if logger.handlers:
        return logger
    
    # 设置日志级别
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # 日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台处理器（输出到终端）
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器（输出到文件）
    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = __name__, level: str = None) -> logging.Logger:
    """
    获取日志记录器（快捷方法）
    
    Args:
        name: 日志记录器名称
        level: 日志级别（可选，如果不提供则从配置读取）
        
    Returns:
        Logger对象
    """
    if level is None:
        try:
            from core.config import config
            level = config.get_log_level()
        except:
            level = 'INFO'  # 默认级别
    return setup_logger(name, level)

