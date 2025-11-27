# Liquid_Auto_Test_Framework

一个基于 **Python + Pytest + Requests** 的接口自动化测试框架，
支持 **YAML 参数化、API 封装、Mock 服务、Allure 报告、日志与邮件通知**，
适用于接口回归测试与个人测试开发学习实践。

---

## ✨ 项目特点

- ✅ 基于 Pytest 的接口测试执行框架
- ✅ YAML 驱动测试数据，支持多参数用例
- ✅ API Object 分层封装，降低用例复杂度
- ✅ 自带 Flask Mock 服务，无需依赖真实后端
- ✅ 支持 HTML + Allure 可视化测试报告
- ✅ 支持 SMTP 邮件自动发送测试结果
- ✅ 支持命令行参数控制执行方式

---

## 📁 项目结构

```text
Liquid_Auto_Test_Framework/
├── api/                 # 业务 API 封装层
├── core/                # 核心框架（请求、配置、日志、断言）
├── testcase/            # 测试用例
├── config/              # 配置文件（yaml）
├── mock/                # Flask Mock 服务
├── utils/               # 工具模块（邮件、通用方法）
├── logs/                # 日志目录（自动生成）
├── report/              # 测试报告目录（自动生成）
├── run.py               # 测试执行入口
├── pytest.ini           # pytest 配置
├── requirements.txt
└── README.md
```

---

## ⚙️ 环境要求

- Python ≥ 3.8
- 已安装 Allure 命令行工具（用于生成 Allure 报告）

---

## 🚀 快速开始

### 1️⃣ 创建虚拟环境并安装依赖

```bash
python -m venv .venv
# Windows
.venvScriptsactivate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

### 2️⃣ 启动 Mock 服务

```bash
python mock/mock_server.py
```

访问健康检查接口验证服务是否正常：

```text
http://127.0.0.1:5000/health
```

### 3️⃣ 执行测试

使用入口脚本运行：

```bash
python run.py
```

**常用参数：**

```bash
python run.py -v            # 显示详细输出
python run.py -t user       # 只运行 user 测试
python run.py -k success    # 按关键字筛选
```

也可以直接使用 pytest：

```bash
pytest testcase/ -v
```

### 4️⃣ 查看测试报告

**HTML 报告：**

```bash
# Windows
start report/report.html
```

**Allure 报告路径：**

```text
report/allure_report/index.html
```

---

## 🔧 核心能力说明

- **HTTP 请求封装**：统一管理 GET / POST 请求
- **API Object 封装**：每个接口对应一个业务类
- **配置集中管理**：统一由 `config.yaml` 管理
- **日志系统**：自动记录请求与响应日志
- **YAML 数据驱动**：支持参数化测试场景
- **测试报告**：HTML 报告 + Allure 报告
- **邮件通知**：支持测试完成后自动发送报告邮件

---

## 📬 邮件配置说明

需要在 `.env` 中配置邮箱密码：

```properties
EMAIL_HOST_PASSWORD=你的邮箱授权码
```

配置文件示例参考：`config/config.yaml`
