"""
用户接口测试用例
测试用户相关的所有接口
"""
import pytest
from api.user_api import UserApi
from core.assertion import Assertion
from core.logger import get_logger

logger = get_logger(__name__)


class TestUserApi:
    """用户API测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """每个测试前的准备工作"""
        self.user_api = UserApi()
        logger.info("=" * 50)
        logger.info("开始执行用户接口测试")
        yield
        logger.info("用户接口测试执行完成")
        logger.info("=" * 50)
    
    def test_get_user_info_success(self):
        """
        测试用例1: 正常获取用户信息
        验证: 状态码200，返回用户信息
        """
        # 执行请求
        response = self.user_api.client.get("/api/user/info", params={"user_id": 1001})
        
        # 断言
        Assertion.assert_status_code(response, 200)
        Assertion.assert_json_contains(response, "code", 200)
        Assertion.assert_json_contains(response, "message", "success")
        Assertion.assert_json_contains(response, "data.user_id")
        Assertion.assert_json_contains(response, "data.username")
        Assertion.assert_json_contains(response, "data.email")
    
    def test_get_user_info_missing_param(self):
        """
        测试用例2: 获取用户信息 - 缺少参数
        验证: 状态码400，返回错误信息
        """
        response = self.user_api.client.get("/api/user/info")
        
        Assertion.assert_status_code(response, 400)
        Assertion.assert_json_contains(response, "code", 400)
        Assertion.assert_json_contains(response, "message")
    
    def test_add_user_success(self):
        """
        测试用例3: 正常添加用户
        验证: 状态码200，用户创建成功
        """
        response = self.user_api.client.post(
            "/api/user/add",
            json_data={
                "username": "test_user_001",
                "email": "test001@example.com",
                "age": 25
            }
        )
        
        Assertion.assert_status_code(response, 200)
        Assertion.assert_json_contains(response, "code", 200)
        Assertion.assert_json_contains(response, "message", "用户创建成功")
        Assertion.assert_json_contains(response, "data.user_id")
        Assertion.assert_json_contains(response, "data.username", "test_user_001")
    
    def test_add_user_missing_username(self):
        """
        测试用例4: 添加用户 - 缺少用户名
        验证: 状态码400，返回错误信息
        """
        response = self.user_api.client.post(
            "/api/user/add",
            json_data={
                "email": "test@example.com"
            }
        )
        
        Assertion.assert_status_code(response, 400)
        Assertion.assert_json_contains(response, "code", 400)
        Assertion.assert_json_contains(response, "message")
    
    def test_add_user_missing_email(self):
        """
        测试用例5: 添加用户 - 缺少邮箱
        验证: 状态码400，返回错误信息
        """
        response = self.user_api.client.post(
            "/api/user/add",
            json_data={
                "username": "test_user"
            }
        )
        
        Assertion.assert_status_code(response, 400)
        Assertion.assert_json_contains(response, "code", 400)
        Assertion.assert_json_contains(response, "message")
    
    def test_add_user_invalid_email(self):
        """
        测试用例6: 添加用户 - 邮箱格式错误
        验证: 状态码400，返回错误信息
        """
        response = self.user_api.client.post(
            "/api/user/add",
            json_data={
                "username": "test_user",
                "email": "invalid_email"  # 无效邮箱格式
            }
        )
        
        Assertion.assert_status_code(response, 400)
        Assertion.assert_json_contains(response, "code", 400)
        Assertion.assert_json_contains(response, "message")
    
    def test_add_user_duplicate_username(self):
        """
        测试用例7: 添加用户 - 用户名重复
        验证: 状态码409，返回冲突信息
        """
        # 先创建一个用户
        self.user_api.client.post(
            "/api/user/add",
            json_data={
                "username": "duplicate_user",
                "email": "dup1@example.com"
            }
        )
        
        # 尝试用相同的用户名创建用户
        response = self.user_api.client.post(
            "/api/user/add",
            json_data={
                "username": "duplicate_user",
                "email": "dup2@example.com"
            }
        )
        
        Assertion.assert_status_code(response, 409)
        Assertion.assert_json_contains(response, "code", 409)
        Assertion.assert_json_contains(response, "message", "用户已存在")
    
    def test_add_user_with_optional_age(self):
        """
        测试用例8: 添加用户 - 包含可选参数age
        验证: 状态码200，用户创建成功，age字段正确
        """
        response = self.user_api.client.post(
            "/api/user/add",
            json_data={
                "username": "user_with_age",
                "email": "age@example.com",
                "age": 30
            }
        )
        
        Assertion.assert_status_code(response, 200)
        Assertion.assert_json_contains(response, "code", 200)
        
        # 验证用户信息中包含age字段
        user_info = self.user_api.get_user_info(response.json()["data"]["user_id"])
        assert user_info["data"]["age"] == 30
    
    def test_get_user_info_response_structure(self):
        """
        测试用例9: 获取用户信息 - 验证响应结构
        验证: 响应包含所有必要字段，字段类型正确
        """
        response = self.user_api.client.get("/api/user/info", params={"user_id": 1001})
        
        Assertion.assert_status_code(response, 200)
        data = response.json()
        
        # 验证响应结构
        assert "code" in data
        assert "message" in data
        assert "data" in data
        
        # 验证data字段结构
        user_data = data["data"]
        assert "user_id" in user_data
        assert "username" in user_data
        assert "email" in user_data
        assert isinstance(user_data["user_id"], int)
        assert isinstance(user_data["username"], str)
        assert isinstance(user_data["email"], str)
    
    def test_add_user_response_time(self):
        """
        测试用例10: 添加用户 - 响应时间测试
        验证: 响应时间在合理范围内（< 1秒）
        """
        response = self.user_api.client.post(
            "/api/user/add",
            json_data={
                "username": "performance_test",
                "email": "perf@example.com"
            }
        )
        
        Assertion.assert_status_code(response, 200)
        Assertion.assert_response_time(response, 1.0)  # 响应时间应小于1秒

