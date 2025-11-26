# MyAutoTestFramework - 接口自动化测试框架

一个基于 **Python + Pytest + Requests + Allure** 的接口自动化测试框架，内置 Mock 服务、统一配置管理、日志记录、HTML/Allure 报告和邮件通知，适合作为学习与实战的接口测试工程项目。

---

## 一、项目简介

- 使用 Pytest 组织与执行接口自动化脚本
- 使用 Requests 封装 HTTP 客户端，统一处理请求、响应与超时
- 提供 API 封装层（类似 Page Object），提升用例复用性与可维护性
- 集成 Flask Mock 服务，无需真实后端即可在本地完整演示
- 自动生成 HTML 报告和 Allure 可视化报告，并支持邮件发送报告
- 配置驱动，支持通过配置文件和环境变量管理不同环境

---

## 二、项目结构

```text
a_MyAutoTestFramework/
├── api/                 # API 封装层
│   ├── user_api.py      # 用户相关接口封装
│   └── message_api.py   # 消息相关接口封装
├── config/              # 配置文件
│   ├── config.yaml      # 项目配置（接口地址、超时等）
│   └── test_data.yaml   # 用例数据
├── core/                # 核心框架模块
│   ├── http_client.py   # HTTP 客户端封装
│   ├── config.py        # 配置管理
│   ├── logger.py        # 日志管理
│   └── assertion.py     # 断言工具
├── mock/                # Mock 服务
│   └── mock_server.py   # 基于 Flask 的模拟接口服务
├── testcase/            # 测试用例
│   ├── test_user.py     # 用户接口相关用例
│   └── test_message.py  # 消息接口相关用例
├── utils/               # 工具函数
│   └── common.py        # 通用工具
├── logs/                # 日志文件（运行时生成）
├── report/              # 报告文件（运行时生成）
├── .env.example         # 环境变量示例
├── .gitignore
├── pytest.ini
├── requirements.txt
├── run.py               # 统一执行入口
└── README.md
```

**说明：**

- `logs/` 和 `report/` 为运行时生成目录，已在 `.gitignore` 中忽略。
- `.env` 由 `.env.example` 复制生成，不提交到仓库。

---

## 三、环境准备

1. **安装 Python**（推荐 3.8+）。
2. **在项目根目录创建并激活虚拟环境**（推荐）：

   Windows：

   ```bash
   python -m venv .venv
   .venvScriptsactivate
   ```

   Linux / macOS：

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. **安装依赖**：

   ```bash
   pip install -r requirements.txt
   ```
4. **配置环境变量**：

   - 复制 `.env.example` 为 `.env`
   - 根据实际情况填写邮箱授权码等敏感信息，例如：

     ```properties
     EMAIL_HOST_PASSWORD=你的邮箱授权码
     ```

---

## 四、启动 Mock 服务

Mock 服务提供模拟接口，便于在本地运行框架而不依赖真实后端。

1. **启动**：

   ```bash
   python mock/mock_server.py
   ```
2. **验证服务是否正常**：

   在浏览器或命令行访问：

   ```text
   http://127.0.0.1:5000/health
   ```

---

## 五、运行方式

### 1. 使用统一入口脚本

在项目根目录执行：

- **运行所有用例**：

  ```bash
  python run.py
  ```
- **运行指定模块用例**（例如用户模块）：

  ```bash
  python run.py -t user
  ```
- **运行消息模块用例**：

  ```bash
  python run.py -t message
  ```
- **按关键字筛选用例**：

  ```bash
  python run.py -k "success"
  ```
- **显示详细输出**（verbose 模式）：

  ```bash
  python run.py -v
  ```

### 2. 直接使用 Pytest

- **运行所有用例**：
  ```bash
  pytest testcase/ -v
  ```

---

## 六、报告查看

执行完成后，会在 `report/` 目录生成多种报告：

- **HTML 报告**：

  ```text
  report/report.html
  ```
- **JUnit XML 报告**（用于 CI/CD 集成）：

  ```text
  report/junit.xml
  ```
- **Allure 结果目录**：

  ```text
  report/allure_results/
  ```

如果本机已安装 Allure 命令行工具（`allure`），`run.py` 会自动生成 Allure HTML 报告：

- **Allure 报告入口**：
  ```text
  report/allure_report/index.html
  ```

  用浏览器直接打开即可查看可视化报告页面。

---

## 七、核心功能示例

### 1. HTTP 客户端封装（core/http_client.py）

统一封装 GET / POST 请求，自动拼接 base_url、处理超时与日志。

**示例：**

```python
from core.http_client import HttpClient

client = HttpClient(base_url="http://127.0.0.1:5000")

# GET 请求
resp = client.get("/api/user/info", params={"user_id": 1001})

# POST 请求
resp = client.post(
    "/api/user/add",
    json_data={"username": "test", "email": "test@example.com"}
)
```

### 2. API 封装层（api/）

用类的方式封装具体业务接口，使用例代码更简洁，便于复用和维护。

**示例：**

```python
from api.user_api import UserApi

user_api = UserApi()

# 获取用户信息
resp = user_api.get_user_info(user_id=1001)

# 新增用户
resp = user_api.add_user(username="test", email="test@example.com")
```

### 3. 断言工具（core/assertion.py）

提供常用断言方法，如状态码、JSON 字段存在与值校验、响应时间等。

**示例：**

```python
from core.assertion import Assertion

Assertion.assert_status_code(resp, 200)
Assertion.assert_json_contains(resp, "data.user_id")
Assertion.assert_json_value(resp, "code", 200)
Assertion.assert_response_time(resp, 1.0)
```

### 4. 配置管理（core/config.py）

统一从 `config/config.yaml` 中读取接口地址、超时等配置，并支持与环境变量结合。

**示例配置（config/config.yaml）：**

```yaml
api:
  base_url: http://127.0.0.1:5000
  timeout: 30
```

**使用方式：**

```python
from core.config import config

base_url = config.get_api_base_url()
timeout = config.get_api_timeout()
```

### 5. 日志记录（core/logger.py）

基于 `logging` 封装统一 Logger，自动按日期生成日志文件，记录请求与响应信息。

**示例：**

```python
from core.logger import get_logger

logger = get_logger(__name__)
logger.info("这是一条示例日志")
```

日志默认保存在 `logs/` 目录下，例如：

```text
logs/test_20251125.log
```

---


## 八、设计思路与扩展

1. **分层架构**

   ```text
   testcase/   → 只关注场景与断言
   api/        → 统一封装业务接口
   core/       → HTTP / 配置 / 日志 / 断言等通用能力
   mock/       → 提供可控的模拟服务
   ```
2. **配置驱动**

   - 所有可变信息集中在 `config.yaml` 与 `.env` 中
   - 方便根据不同环境（本地、测试环境等）切换配置
3. **易于扩展**

   - 新增业务接口：在 `api/` 下添加新类或方法
   - 新增场景：在 `testcase/` 下新增对应测试文件
   - 新增通用能力：在 `core/` 或 `utils/` 中扩展实现
