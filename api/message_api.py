"""
消息API封装
提供消息相关的接口调用方法
"""
from typing import Dict, Optional
from core.http_client import HttpClient
from core.config import config
from core.logger import get_logger

logger = get_logger(__name__)


class MessageApi:
    """
    消息API类
    
    封装消息相关的所有接口调用
    """
    
    def __init__(self, client: Optional[HttpClient] = None):
        """
        初始化消息API
        
        Args:
            client: HTTP客户端实例，如果不提供则创建新实例
        """
        if client is None:
            base_url = config.get_api_base_url()
            timeout = config.get_api_timeout()
            self.client = HttpClient(base_url=base_url, timeout=timeout)
        else:
            self.client = client
    
    def get_message_list(self, page: int = 1, page_size: int = 10) -> Dict:
        """
        获取消息列表
        
        Args:
            page: 页码，从1开始
            page_size: 每页数量
            
        Returns:
            消息列表字典
        """
        logger.info(f"获取消息列表: page={page}, page_size={page_size}")
        params = {
            "page": page,
            "page_size": page_size
        }
        response = self.client.get("/api/message/list", params=params)
        response.raise_for_status()
        return response.json()
    
    def send_message(self, receiver_id: int, content: str, title: Optional[str] = None) -> Dict:
        """
        发送消息
        
        Args:
            receiver_id: 接收者ID
            content: 消息内容
            title: 消息标题（可选）
            
        Returns:
            发送结果字典
        """
        logger.info(f"发送消息: receiver_id={receiver_id}, title={title}")
        data = {
            "receiver_id": receiver_id,
            "content": content
        }
        if title:
            data["title"] = title
        
        response = self.client.post("/api/message/send", json_data=data)
        response.raise_for_status()
        return response.json()

