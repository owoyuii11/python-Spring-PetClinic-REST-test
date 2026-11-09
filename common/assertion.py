from common.logger import logger

def assert_response_code(resp, expect_code=200):
    actual = resp.status_code
    assert actual == expect_code, f"状态码错误！预期:{expect_code},实际:{actual}"

def assert_json_contain(resp_json, key, expect_val):
    """校验json里面某个key等于期望值"""
    assert key in resp_json, f"返回结果缺少字段 {key}"
    assert resp_json[key] == expect_val, f"字段{key}预期{expect_val},实际{resp_json[key]}"

def assert_list_contain_item(resp_list, key, expect_val):
    """列表里面包含符合条件的对象，用来校验主人下面存在这条宠物"""
    find = False
    for item in resp_list:
        if item.get(key) == expect_val:
            find = True
            break
    assert find, f"列表中没有找到 {key}={expect_val} 的数据"
