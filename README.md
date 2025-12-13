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

## 环境变量配置 (.env)

在项目根目录的 `.env` 文件中需要配置以下变量：

- `EMAIL_HOST_PASSWORD`：邮箱 SMTP 授权码，用于发送测试报告邮件。
- `ALLURE_CMD`：可选，Allure 命令行工具路径，用于自动生成 Allure 报告。  
  例如（Windows）：  
  `ALLURE_CMD=E:\allure-2.35.1\bin\allure.bat`  
  如果未配置或本机未安装 Allure CLI，则只会生成 HTML 报告 `report/report.html`，不会生成 Allure 报告。

### 配置文件说明

- 仓库已提供示例配置 `config/config.example.yaml`，使用前请复制为本地配置：
  ```bash
  cp config/config.example.yaml config/config.yaml
  ```
- 复制后在 `config.yaml` 中根据环境修改：
  - `api.base_url`：Mock 服务地址或真实接口地址
  - `email.sender` / `email.receiver`：你的发件人与收件人邮箱
- 邮箱授权码不要写入 `config.yaml`，在 `.env` 中通过 `EMAIL_HOST_PASSWORD` 配置。
- `config.yaml` 与 `.env` 属于本地私有配置，已在 `.gitignore` 中忽略，不会提交到 GitHub。

---

## 🚀 快速开始

### 1️⃣ 创建虚拟环境并安装依赖

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# 如果使用 PowerShell，可以执行 .\.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

### 2️⃣ 启动 Mock 服务

```bash
python mock/mock_server.py
```

> 提示：Mock 服务启动后请保持此终端窗口不要关闭，另开一个新的终端执行后续的 `python run.py` 或 `pytest` 命令。

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

## Allure 报告查看方式

- 测试执行完成后，Allure 静态报告生成在 `report/allure_report` 目录（通过 `python run.py` 执行会自动生成）。

**方式一（推荐）：使用 Allure CLI**

```bash
cd E:\Liquid_Auto_Test_Framework\report\allure_report
allure open .
```

- 此命令会自动启动本地 HTTP 服务，并在浏览器中打开类似 `http://127.0.0.1:xxxx/index.html` 的地址，可查看 Overview、Suites、Graphs 等可视化信息。

**方式二：使用 Python 自带 HTTP Server（未安装 Allure CLI 时）**

```bash
cd E:\Liquid_Auto_Test_Framework\report\allure_report
python -m http.server 8000
```

- 在浏览器访问 `http://127.0.0.1:8000/index.html` 即可查看同样的 Allure 报告。

**通过邮件附件查看 Allure 报告**

- 框架会自动将 `report/allure_report` 目录打包为 `allure_report.zip` 并通过邮件发送。
- 收件人查看步骤：
  - 将附件 `allure_report.zip` 保存并解压，例如解压到 `D:\reports\allure_report`
  - 在该目录下打开终端并执行：
    ```bash
    cd /d D:\reports\allure_report
    python -m http.server 8000
    ```
  - 或（如果已安装 Allure CLI）：
    ```bash
    cd /d D:\reports\allure_report
    allure open .
    ```
  - 浏览器访问 `http://127.0.0.1:8000/index.html` 或 CLI 自动打开的地址，即可查看完整报告。
