"""
用户API封装
提供用户相关的接口调用方法
"""
from typing import Dict, Optional
from core.http_client import HttpClient
from core.config import config
from core.logger import get_logger

logger = get_logger(__name__)


class UserApi:
    """
    用户API类
    
    封装用户相关的所有接口调用
    """
    
    def __init__(self, client: Optional[HttpClient] = None):
        """
        初始化用户API
        
        Args:
            client: HTTP客户端实例，如果不提供则创建新实例
        """
        if client is None:
            base_url = config.get_api_base_url()
            timeout = config.get_api_timeout()
            self.client = HttpClient(base_url=base_url, timeout=timeout)
        else:
            self.client = client
    
    def get_user_info(self, user_id: int) -> Dict:
        """
        获取用户信息
        
        Args:
            user_id: 用户ID
            
        Returns:
            用户信息字典
        """
        logger.info(f"获取用户信息: user_id={user_id}")
        response = self.client.get(f"/api/user/info", params={"user_id": user_id})
        response.raise_for_status()  # 如果状态码不是2xx，抛出异常
        return response.json()
    
    def add_user(self, username: str, email: str, age: Optional[int] = None) -> Dict:
        """
        添加用户
        
        Args:
            username: 用户名
            email: 邮箱
            age: 年龄（可选）
            
        Returns:
            创建结果字典
        """
        logger.info(f"添加用户: username={username}, email={email}")
        data = {
            "username": username,
            "email": email
        }
        if age is not None:
            data["age"] = age
        
        response = self.client.post("/api/user/add", json_data=data)
        response.raise_for_status()
        return response.json()
    
    def update_user(self, user_id: int, **kwargs) -> Dict:
        """
        更新用户信息
        
        Args:
            user_id: 用户ID
            **kwargs: 要更新的字段（如 username, email, age等）
            
        Returns:
            更新结果字典
        """
        logger.info(f"更新用户: user_id={user_id}, data={kwargs}")
        response = self.client.put(f"/api/user/{user_id}", json_data=kwargs)
        response.raise_for_status()
        return response.json()
    
    def delete_user(self, user_id: int) -> Dict:
        """
        删除用户
        
        Args:
            user_id: 用户ID
            
        Returns:
            删除结果字典
        """
        logger.info(f"删除用户: user_id={user_id}")
        response = self.client.delete(f"/api/user/{user_id}")
        response.raise_for_status()
        return response.json()

