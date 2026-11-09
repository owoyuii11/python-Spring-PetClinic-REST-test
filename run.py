import pytest
import os

if __name__ == "__main__":
    pytest.main()
    # 优先用 allure 命令行工具生成报告：优先绝对路径（兼容 PATH 未刷新的终端），否则用系统 PATH 里的 allure
    allure_bin = "C:\\allure\\allure-2.46.1\\bin\\allure.bat"
    if not os.path.exists(allure_bin):
        allure_bin = "allure"
    os.system(f'"{allure_bin}" generate allure-results -o reports/allure --clean')
