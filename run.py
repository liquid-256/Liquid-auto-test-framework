"""
测试框架入口文件
用于启动测试并生成报告 + 邮件发送
"""
import os
import sys
import argparse
import subprocess
import pytest
from pathlib import Path
from dotenv import load_dotenv
from core.config import config
from core.logger import get_logger
import shutil

# 加载环境变量
load_dotenv()

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description='接口自动化测试框架')
    parser.add_argument('-t', '--test', type=str, help='指定测试文件')
    parser.add_argument('-m', '--mark', type=str, help='运行指定标记用例')
    parser.add_argument('-v', '--verbose', action='store_true', help='详细输出')
    parser.add_argument('-k', '--keyword', type=str, help='按关键字过滤')

    args = parser.parse_args()

    # pytest 参数
    pytest_args = []

    test_dir = Path(__file__).parent / 'testcase'
    pytest_args.append(str(test_dir))

    if args.verbose:
        pytest_args.append('-v')
    else:
        pytest_args.append('-q')

    if args.test:
        pytest_args.append(f'testcase/test_{args.test}.py')

    if args.mark:
        pytest_args.extend(['-m', args.mark])

    if args.keyword:
        pytest_args.extend(['-k', args.keyword])

    # 报告目录
    report_dir = Path(config.get_report_dir())
    report_dir.mkdir(parents=True, exist_ok=True)

    # Allure 结果目录
    allure_results_dir = report_dir / "allure_results"
    allure_results_dir.mkdir(parents=True, exist_ok=True)

    # Allure 报告目录
    allure_report_dir = report_dir / "allure_report"

    pytest_args.extend([
        '--html', f'{report_dir}/report.html',
        '--self-contained-html',
        '--junit-xml', f'{report_dir}/junit.xml',
        '--alluredir', str(allure_results_dir)
    ])

    logger.info("=" * 60)
    logger.info("开始执行自动化测试")
    logger.info(f"测试目录: {test_dir}")
    logger.info(f"报告目录: {report_dir}")
    logger.info("=" * 60)

    exit_code = pytest.main(pytest_args)

    # 生成 Allure 报告（依赖本地已安装 Allure 命令行）
    logger.info("正在生成 Allure 报告...")

    # 1) 优先用 shutil.which 在当前进程 PATH 中查找 allure
    allure_cmd = shutil.which("allure")

    # 2) 如果没找到，尝试读环境变量 ALLURE_CMD（你可以在 .env 里显式配置）
    if not allure_cmd:
        allure_cmd = os.getenv("ALLURE_CMD")

    if not allure_cmd:
        logger.warning("未找到 allure 命令，请先安装 Allure 命令行工具或配置 ALLURE_CMD 环境变量")
        logger.warning("参考文档: https://docs.qameta.io/allure/")
    else:
        logger.info(f"使用 Allure 命令: {allure_cmd}")
        try:
            # Windows 上建议 shell=False + 绝对路径
            subprocess.run(
                [
                    allure_cmd,
                    "generate",
                    str(allure_results_dir),
                    "-o",
                    str(allure_report_dir),
                    "--clean",
                ],
                check=True,
            )
            logger.info(f"Allure 报告生成成功: {allure_report_dir}/index.html")
        except subprocess.CalledProcessError as e:
            logger.warning(f"Allure 生成失败，退出码 {e.returncode}: {e}")
        except Exception as e:
            logger.warning(f"Allure 生成失败: {e}")


    #  压缩 Allure 报告 ZIP（用于邮件发送）
    try:
        zip_path = shutil.make_archive(
            base_name=str(report_dir / "allure_report"),
            format="zip",
            root_dir=allure_report_dir
        )
        logger.info(f"Allure 报告 ZIP 打包成功: {zip_path}")
    except Exception as e:
        logger.error(f"Allure ZIP 打包失败: {e}")
        zip_path = None

    #  发送邮件
    if zip_path:
        try:
            from utils.email_sender import send_report_email
            send_report_email(zip_path)
        except Exception as e:
            logger.warning(f"邮件发送失败: {e}")

    return exit_code


if __name__ == '__main__':
    sys.exit(main())
