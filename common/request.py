import requests
from common.logger import logger

class HttpRequest:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.headers = {
            "Content-Type": "application/json"
        }

    def send(self, method, path, json_data=None, params=None):
        url = self.base_url + path
        try:
            logger.info(f"【请求】 {method.upper()} {url}")
            logger.info(f"请求头：{self.headers}")
            logger.info(f"请求体：{json_data}")
            resp = self.session.request(
                method=method,
                url=url,
                headers=self.headers,
                json=json_data,
                params=params,
                timeout=10
            )
            logger.info(f"响应码: {resp.status_code}")
            logger.info(f"响应内容: {resp.text}")
            return resp
        except Exception as e:
            logger.error(f"请求异常：{str(e)}")
            raise e

    def get(self, path, params=None):
        return self.send("get", path, params=params)

    def post(self, path, json_data=None):
        return self.send("post", path, json_data=json_data)

    def put(self, path, json_data=None):
        return self.send("put", path, json_data=json_data)

    def delete(self, path):
        return self.send("delete", path)
