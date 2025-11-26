"""
HTTP客户端封装
提供统一的HTTP请求接口，支持GET、POST等方法
"""
import requests
import json
from typing import Dict, Any, Optional
from core.logger import get_logger

logger = get_logger(__name__)


class HttpClient:
    """
    HTTP客户端类
    
    封装requests库，提供简洁的HTTP请求接口
    支持自动记录请求和响应日志
    """
    
    def __init__(self, base_url: str = "", timeout: int = 30):
        """
        初始化HTTP客户端
        
        Args:
            base_url: 基础URL，所有请求会拼接这个URL
            timeout: 请求超时时间（秒）
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()  # 使用session保持连接和Cookie
    
    def _build_url(self, path: str) -> str:
        """
        构建完整URL
        
        Args:
            path: 接口路径
            
        Returns:
            完整的URL
        """
        if path.startswith('http'):
            return path
        return f"{self.base_url}/{path.lstrip('/')}"
    
    def _log_request(self, method: str, url: str, **kwargs):
        """记录请求日志"""
        logger.info(f"[请求] {method} {url}")
        if 'json' in kwargs:
            logger.debug(f"[请求体] {json.dumps(kwargs['json'], ensure_ascii=False, indent=2)}")
        elif 'data' in kwargs:
            logger.debug(f"[请求体] {kwargs['data']}")
        if 'params' in kwargs:
            logger.debug(f"[请求参数] {kwargs['params']}")
    
    def _log_response(self, response: requests.Response):
        """记录响应日志"""
        try:
            response_json = response.json()
            logger.info(f"[响应] 状态码: {response.status_code}")
            logger.debug(f"[响应体] {json.dumps(response_json, ensure_ascii=False, indent=2)}")
        except:
            logger.info(f"[响应] 状态码: {response.status_code}")
            logger.debug(f"[响应体] {response.text[:500]}")
    
    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs
    ) -> requests.Response:
        """
        发送HTTP请求
        
        Args:
            method: 请求方法（GET、POST、PUT、DELETE等）
            path: 接口路径
            params: URL参数（用于GET请求）
            data: 表单数据（用于POST请求，Content-Type: application/x-www-form-urlencoded）
            json_data: JSON数据（用于POST请求，Content-Type: application/json）
            headers: 请求头
            **kwargs: 其他requests参数
            
        Returns:
            Response对象
        """
        url = self._build_url(path)
        
        # 准备请求参数
        request_kwargs = {
            'timeout': self.timeout,
            **kwargs
        }
        
        if params:
            request_kwargs['params'] = params
        if data:
            request_kwargs['data'] = data
        if json_data:
            request_kwargs['json'] = json_data
        if headers:
            request_kwargs['headers'] = headers
        
        # 记录请求日志
        self._log_request(method, url, **request_kwargs)
        
        try:
            # 发送请求
            response = self.session.request(method, url, **request_kwargs)
            
            # 记录响应日志
            self._log_response(response)
            
            # 如果状态码不是2xx，记录警告
            if not response.ok:
                logger.warning(f"请求失败: {response.status_code} - {response.text[:200]}")
            
            return response
            
        except requests.exceptions.Timeout:
            logger.error(f"请求超时: {url}")
            raise
        except requests.exceptions.ConnectionError:
            logger.error(f"连接失败: {url}")
            raise
        except Exception as e:
            logger.error(f"请求异常: {str(e)}")
            raise
    
    def get(self, path: str, params: Optional[Dict] = None, headers: Optional[Dict] = None, **kwargs) -> requests.Response:
        """
        发送GET请求
        
        Args:
            path: 接口路径
            params: URL参数
            headers: 请求头
            **kwargs: 其他requests参数
            
        Returns:
            Response对象
        """
        return self.request('GET', path, params=params, headers=headers, **kwargs)
    
    def post(
        self,
        path: str,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs
    ) -> requests.Response:
        """
        发送POST请求
        
        Args:
            path: 接口路径
            data: 表单数据（Content-Type: application/x-www-form-urlencoded）
            json_data: JSON数据（Content-Type: application/json）
            headers: 请求头
            **kwargs: 其他requests参数
            
        Returns:
            Response对象
        """
        return self.request('POST', path, data=data, json_data=json_data, headers=headers, **kwargs)
    
    def put(
        self,
        path: str,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        **kwargs
    ) -> requests.Response:
        """发送PUT请求"""
        return self.request('PUT', path, data=data, json_data=json_data, headers=headers, **kwargs)
    
    def delete(self, path: str, headers: Optional[Dict] = None, **kwargs) -> requests.Response:
        """发送DELETE请求"""
        return self.request('DELETE', path, headers=headers, **kwargs)
    
    def close(self):
        """关闭session"""
        self.session.close()

