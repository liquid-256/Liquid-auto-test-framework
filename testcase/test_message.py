"""
消息接口测试用例
测试消息相关的所有接口
"""
import pytest
from pathlib import Path
from api.message_api import MessageApi
from core.assertion import Assertion
from core.logger import get_logger
from utils.common import load_yaml

logger = get_logger(__name__)


class TestMessageApi:
    """消息API测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """每个测试前的准备工作"""
        self.message_api = MessageApi()
        logger.info("=" * 50)
        logger.info("开始执行消息接口测试")
        yield
        logger.info("消息接口测试执行完成")
        logger.info("=" * 50)
    
    def test_get_message_list_success(self):
        """
        测试用例1: 正常获取消息列表
        验证: 状态码200，返回消息列表
        """
        response = self.message_api.client.get("/api/message/list")
        
        Assertion.assert_status_code(response, 200)
        Assertion.assert_json_contains(response, "code", 200)
        Assertion.assert_json_contains(response, "data.total")
        Assertion.assert_json_contains(response, "data.messages")
    
    def test_get_message_list_with_pagination(self):
        """
        测试用例2: 获取消息列表 - 分页参数
        验证: 状态码200，分页功能正常
        """
        response = self.message_api.client.get(
            "/api/message/list",
            params={"page": 1, "page_size": 5}
        )
        
        Assertion.assert_status_code(response, 200)
        data = response.json()["data"]
        assert data["page"] == 1
        assert data["page_size"] == 5
        assert len(data["messages"]) <= 5
    
    def test_get_message_list_page2(self):
        """
        测试用例3: 获取消息列表 - 第二页
        验证: 状态码200，返回第二页数据
        """
        response = self.message_api.client.get(
            "/api/message/list",
            params={"page": 2, "page_size": 10}
        )
        
        Assertion.assert_status_code(response, 200)
        data = response.json()["data"]
        assert data["page"] == 2
        assert len(data["messages"]) <= 10
    
    def test_get_message_list_structure(self):
        """
        测试用例4: 获取消息列表 - 验证响应结构
        验证: 响应包含所有必要字段，消息对象结构正确
        """
        response = self.message_api.client.get("/api/message/list")
        
        Assertion.assert_status_code(response, 200)
        data = response.json()["data"]
        
        # 验证分页信息
        assert "total" in data
        assert "page" in data
        assert "page_size" in data
        assert "messages" in data
        
        # 验证消息对象结构
        if data["messages"]:
            message = data["messages"][0]
            assert "message_id" in message
            assert "title" in message
            assert "content" in message
            assert "sender_id" in message
            assert "receiver_id" in message
            assert "created_at" in message
    
    def test_send_message_success(self):
        """
        测试用例5: 正常发送消息
        验证: 状态码200，消息发送成功
        """
        response = self.message_api.client.post(
            "/api/message/send",
            json_data={
                "receiver_id": 1002,
                "content": "这是一条测试消息",
                "title": "测试标题"
            }
        )
        
        Assertion.assert_status_code(response, 200)
        Assertion.assert_json_contains(response, "code", 200)
        Assertion.assert_json_contains(response, "message", "消息发送成功")
        Assertion.assert_json_contains(response, "data.message_id")
    
    def test_send_message_missing_receiver(self):
        """
        测试用例6: 发送消息 - 缺少接收者ID
        验证: 状态码400，返回错误信息
        """
        response = self.message_api.client.post(
            "/api/message/send",
            json_data={
                "content": "消息内容"
            }
        )
        
        Assertion.assert_status_code(response, 400)
        Assertion.assert_json_contains(response, "code", 400)
        Assertion.assert_json_contains(response, "message")
    
    def test_send_message_missing_content(self):
        """
        测试用例7: 发送消息 - 缺少消息内容
        验证: 状态码400，返回错误信息
        """
        response = self.message_api.client.post(
            "/api/message/send",
            json_data={
                "receiver_id": 1002
            }
        )
        
        Assertion.assert_status_code(response, 400)
        Assertion.assert_json_contains(response, "code", 400)
        Assertion.assert_json_contains(response, "message")
    
    def test_send_message_without_title(self):
        """
        测试用例8: 发送消息 - 不提供标题（可选参数）
        验证: 状态码200，使用默认标题
        """
        response = self.message_api.client.post(
            "/api/message/send",
            json_data={
                "receiver_id": 1002,
                "content": "没有标题的消息"
            }
        )
        
        Assertion.assert_status_code(response, 200)
        Assertion.assert_json_contains(response, "code", 200)
    
    def test_send_message_response_time(self):
        """
        测试用例9: 发送消息 - 响应时间测试
        验证: 响应时间在合理范围内（< 1秒）
        """
        response = self.message_api.client.post(
            "/api/message/send",
            json_data={
                "receiver_id": 1002,
                "content": "性能测试消息"
            }
        )
        
        Assertion.assert_status_code(response, 200)
        Assertion.assert_response_time(response, 1.0)
    
    def test_get_message_list_after_send(self):
        """
        测试用例10: 发送消息后获取列表 - 验证消息已添加
        验证: 新发送的消息出现在列表中
        """
        # 发送消息
        send_response = self.message_api.client.post(
            "/api/message/send",
            json_data={
                "receiver_id": 1003,
                "content": "验证消息",
                "title": "验证标题"
            }
        )
        message_id = send_response.json()["data"]["message_id"]
        
        # 获取消息列表
        list_response = self.message_api.client.get("/api/message/list")
        messages = list_response.json()["data"]["messages"]
        
        # 验证新消息在列表中
        message_ids = [msg["message_id"] for msg in messages]
        assert message_id in message_ids
    
    # YAML参数化测试用例
    @pytest.fixture
    def message_api(self):
        """提供MessageApi实例的Fixture"""
        return MessageApi()
    
    @pytest.mark.parametrize("case", load_yaml("config/test_data.yaml")["send_message_cases"])
    def test_send_message_param(self, message_api, case):
        """
        测试用例11: YAML参数化测试 - 发送消息
        验证: 使用YAML文件中的测试数据，批量测试发送消息接口
        """
        # 发送消息
        response = message_api.client.post(
            "/api/message/send",
            json_data=case
        )
        
        # 断言
        Assertion.assert_status_code(response, 200)
        Assertion.assert_json_contains(response, "code", 200)
        Assertion.assert_json_contains(response, "message", "消息发送成功")
        Assertion.assert_json_contains(response, "data.message_id")
        
        # 验证返回的消息ID存在
        message_id = response.json()["data"]["message_id"]
        assert message_id is not None, "消息ID不应为空"
        assert isinstance(message_id, int), "消息ID应为整数"

