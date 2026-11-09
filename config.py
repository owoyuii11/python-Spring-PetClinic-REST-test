import os

# 默认使用本地 PetClinic 测试环境
BASE_URL = os.getenv(
    "TEST_BASE_URL",
    "http://localhost:9966/petclinic"
)

TIMEOUT = 10

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}