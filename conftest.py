import pytest
import yaml
from common.request import HttpRequest

@pytest.fixture(scope="session")
def env_config():
    with open("config/env.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["test"]

@pytest.fixture(scope="session")
def http_client(env_config):
    client = HttpRequest(base_url=env_config["base_url"])
    yield client
