"""
Pytest配置文件
定义全局的Fixture和Hook函数
"""
import pytest
from core.logger import get_logger

logger = get_logger(__name__)


@pytest.fixture(scope="session", autouse=True)
def setup_session():
    """
    测试会话级别的Fixture
    在整个测试会话开始前执行
    """
    logger.info("=" * 60)
    logger.info("测试会话开始")
    logger.info("=" * 60)
    yield
    logger.info("=" * 60)
    logger.info("测试会话结束")
    logger.info("=" * 60)


@pytest.fixture(scope="function", autouse=True)
def setup_test():
    """
    测试函数级别的Fixture
    在每个测试用例执行前后执行
    """
    logger.info("-" * 60)
    yield
    logger.info("-" * 60)

