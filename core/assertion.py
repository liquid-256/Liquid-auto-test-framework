"""
断言工具模块
提供各种断言方法，用于验证接口响应
"""
from typing import Any, Dict, List
from core.logger import get_logger

logger = get_logger(__name__)


class Assertion:
    """
    断言工具类
    
    提供各种断言方法，用于验证接口响应是否符合预期
    """
    
    @staticmethod
    def assert_status_code(response, expected_code: int):
        """
        断言HTTP状态码
        
        Args:
            response: Response对象
            expected_code: 期望的状态码
            
        Raises:
            AssertionError: 如果状态码不匹配
        """
        actual_code = response.status_code
        assert actual_code == expected_code, \
            f"状态码断言失败: 期望 {expected_code}, 实际 {actual_code}"
        logger.info(f"✓ 状态码断言通过: {actual_code}")
    
    @staticmethod
    def assert_json_contains(response, key: str, expected_value: Any = None):
        """
        断言JSON响应包含指定字段（可选：验证值）
        
        Args:
            response: Response对象
            key: 字段名（支持点号分隔的嵌套字段，如 'data.user.name'）
            expected_value: 期望的值（可选，如果提供则验证值是否匹配）
            
        Raises:
            AssertionError: 如果字段不存在或值不匹配
        """
        try:
            json_data = response.json()
        except:
            raise AssertionError(f"响应不是有效的JSON格式: {response.text[:200]}")
        
        # 支持嵌套字段访问
        keys = key.split('.')
        value = json_data
        
        try:
            for k in keys:
                value = value[k]
            
            if expected_value is not None:
                assert value == expected_value, \
                    f"字段值断言失败: {key} 期望 {expected_value}, 实际 {value}"
                logger.info(f"✓ 字段值断言通过: {key} = {value}")
            else:
                logger.info(f"✓ 字段存在断言通过: {key}")
                
        except (KeyError, TypeError):
            raise AssertionError(f"字段不存在: {key}")
    
    @staticmethod
    def assert_json_equal(response, expected_data: Dict):
        """
        断言JSON响应完全匹配
        
        Args:
            response: Response对象
            expected_data: 期望的JSON数据
            
        Raises:
            AssertionError: 如果响应不匹配
        """
        try:
            actual_data = response.json()
        except:
            raise AssertionError(f"响应不是有效的JSON格式: {response.text[:200]}")
        
        # 只比较期望数据中的字段
        for key, expected_value in expected_data.items():
            keys = key.split('.')
            actual_value = actual_data
            
            try:
                for k in keys:
                    actual_value = actual_value[k]
            except (KeyError, TypeError):
                raise AssertionError(f"字段不存在: {key}")
            
            assert actual_value == expected_value, \
                f"字段 {key} 不匹配: 期望 {expected_value}, 实际 {actual_value}"
        
        logger.info("✓ JSON完全匹配断言通过")
    
    @staticmethod
    def assert_response_time(response, max_time: float):
        """
        断言响应时间
        
        Args:
            response: Response对象
            max_time: 最大响应时间（秒）
            
        Raises:
            AssertionError: 如果响应时间超过最大值
        """
        actual_time = response.elapsed.total_seconds()
        assert actual_time <= max_time, \
            f"响应时间过长: {actual_time:.2f}s > {max_time}s"
        logger.info(f"✓ 响应时间断言通过: {actual_time:.2f}s")
    
    @staticmethod
    def assert_success(response):
        """
        断言请求成功（状态码2xx）
        
        Args:
            response: Response对象
            
        Raises:
            AssertionError: 如果状态码不是2xx
        """
        assert response.ok, f"请求失败: 状态码 {response.status_code}"
        logger.info("✓ 请求成功断言通过")

