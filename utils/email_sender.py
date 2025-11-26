"""
邮件发送工具
发送完整 Allure 报告 ZIP 文件
"""
import os
import smtplib
import yaml
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from core.logger import get_logger

logger = get_logger(__name__)


def load_email_config():
    """加载邮件配置 + 环境变量密码"""
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    if "email" not in cfg:
        raise KeyError("配置文件中缺少 email 配置项")

    email_cfg = cfg["email"].copy()

    password = os.getenv("EMAIL_HOST_PASSWORD")
    if not password:
        raise ValueError("环境变量 EMAIL_HOST_PASSWORD 未设置，请检查 .env 文件")

    email_cfg["password"] = password
    return email_cfg


def send_report_email(zip_file_path: str):
    """发送 Allure ZIP 报告"""

    try:
        cfg = load_email_config()
    except FileNotFoundError as e:
        logger.warning(f"未找到邮件配置文件，已跳过邮件发送: {e}")
        return
    except (KeyError, ValueError) as e:
        logger.warning(f"邮件配置不完整或环境变量缺失，已跳过邮件发送: {e}")
        return

    zip_path = Path(zip_file_path)
    if not zip_path.exists():
        logger.error(f"报告 ZIP 文件不存在: {zip_file_path}")
        return

    logger.info(f"正在发送邮件到: {cfg['receiver']}")
    logger.info(f"邮件附件: {zip_path}")

    # 创建邮件
    msg = MIMEMultipart()
    msg["From"] = cfg["sender"]
    msg["To"] = cfg["receiver"]
    msg["Subject"] = "自动化测试报告 - Allure 报告"

    # 邮件正文
    body = "自动化测试已完成，Allure 报告已作为 ZIP 附件发送。\n\n请解压后打开 index.html。"
    msg.attach(MIMEText(body, "plain", "utf-8"))

    # 添加附件（ZIP 文件）
    with open(zip_path, "rb") as f:
        part = MIMEBase("application", "zip")
        part.set_payload(f.read())

    encoders.encode_base64(part)
    part.add_header("Content-Disposition", "attachment", filename="allure_report.zip")
    msg.attach(part)

    # 发送邮件
    try:
        smtp = smtplib.SMTP_SSL(cfg["smtp_server"], cfg["smtp_port"])
        smtp.login(cfg["sender"], cfg["password"])
        smtp.sendmail(cfg["sender"], cfg["receiver"], msg.as_string())
        smtp.quit()
        logger.info("✓ 邮件发送成功")

    except Exception as e:
        logger.error(f"邮件发送失败: {e}")
        # 邮件发送失败不影响整体测试执行，记录日志后返回
        return



