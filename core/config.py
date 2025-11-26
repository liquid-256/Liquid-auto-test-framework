"""
配置管理模块
读取和管理项目配置
"""
import os
import yaml
from typing import Dict, Any
from pathlib import Path

# 获取项目根目录
BASE_DIR = Path(__file__).parent.parent


class Config:
    """
    配置管理类
    
    负责读取和管理项目配置
    支持从YAML文件读取配置
    """
    
    _instance = None
    _config_data: Dict[str, Any] = {}
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """初始化配置"""
        if not self._config_data:
            self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        config_file = BASE_DIR / 'config' / 'config.yaml'
        
        if not config_file.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_file}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            self._config_data = yaml.safe_load(f) or {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键，支持点号分隔的嵌套键（如 'api.base_url'）
            default: 默认值
            
        Returns:
            配置值
            
        示例:
            config.get('api.base_url')
            config.get('api.timeout', 30)
        """
        keys = key.split('.')
        value = self._config_data
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_api_base_url(self) -> str:
        """获取API基础URL"""
        return self.get('api.base_url', 'http://127.0.0.1:5000')
    
    def get_api_timeout(self) -> int:
        """获取API请求超时时间"""
        return self.get('api.timeout', 30)
    
    def get_log_level(self) -> str:
        """获取日志级别"""
        return self.get('log.level', 'INFO')
    
    def get_report_dir(self) -> str:
        """获取报告目录"""
        report_dir = self.get('report.dir', 'report')
        # 如果是相对路径，转换为绝对路径
        if not os.path.isabs(report_dir):
            report_dir = str(BASE_DIR / report_dir)
        return report_dir


# 创建全局配置实例
config = Config()

