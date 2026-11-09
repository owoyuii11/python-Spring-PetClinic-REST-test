import yaml
from common.assertion import assert_response_code, assert_json_contain, assert_list_contain_item
from common.logger import logger

# 加载测试数据
with open("data/pet_owner_data.yaml", encoding="utf-8") as f:
    test_data = yaml.safe_load(f)

def test_owner_pet_full_flow(http_client):
    """
    完整业务流程：主人+宠物全链路（spring-petclinic-rest 实测契约）
    1.新增主人(POST /owners)         -> 201, body 返回带 id
    2.给主人新增宠物(POST /owners/{id}/pets) -> 201, body 返回带 id
    3.查询主人(GET /owners/{id})     -> 200, 校验宠物已挂在主人下
    4.修改宠物(PUT /owners/{id}/pets/{pid}) -> 204
    5.再次查询主人, 校验宠物修改生效
    6.删除宠物(DELETE /pets/{pid})   -> 204
    7.删除主人(DELETE /owners/{id})  -> 204
    """
    owner_id = None
    pet_id = None
    try:
        # Step1：新增主人，201 + body 直接返回 id（本项目 POST 返回完整 OwnerDto）
        resp_owner = http_client.post("/owners", json_data=test_data["owner_info"])
        assert_response_code(resp_owner, 201)
        owner_id = resp_owner.json()["id"]
        logger.info(f"✅ 新增主人成功，owner_id={owner_id}")

        # Step2：给这个主人新增宠物
        pet_resp = http_client.post(f"/owners/{owner_id}/pets", json_data=test_data["pet_add"])
        assert_response_code(pet_resp, 201)
        pet_id = pet_resp.json()["id"]
        logger.info(f"✅ 新增宠物成功，pet_id={pet_id}")

        # Step3：查询主人信息，校验宠物已经挂在主人下面（核心业务校验！不是只看状态码）
        get_owner_resp = http_client.get(f"/owners/{owner_id}")
        assert_response_code(get_owner_resp, 200)
        pets_list = get_owner_resp.json()["pets"]
        assert_list_contain_item(pets_list, "name", test_data["pet_add"]["name"])
        logger.info("✅ 校验：主人下存在新增的宠物")

        # Step4：修改宠物（PUT /owners/{ownerId}/pets/{petId}，返回 204）
        put_resp = http_client.put(
            f"/owners/{owner_id}/pets/{pet_id}", json_data=test_data["pet_modify"]
        )
        assert_response_code(put_resp, 204)
        logger.info("✅ 修改宠物成功")

        # Step5：再次查询主人，校验宠物修改生效
        get_owner_resp2 = http_client.get(f"/owners/{owner_id}")
        assert_response_code(get_owner_resp2, 200)
        pets_list2 = get_owner_resp2.json()["pets"]
        assert_list_contain_item(pets_list2, "name", test_data["pet_modify"]["name"])
        logger.info("✅ 校验：宠物修改成功")

    finally:
        # 【重点：小企业强制要求，不管用例成功失败，都清理脏数据！】
        # 先删宠物，再删主人（有外键约束，顺序不能反）
        if pet_id:
            del_pet = http_client.delete(f"/pets/{pet_id}")
            logger.info(f"清理宠物{pet_id},code:{del_pet.status_code}")
        if owner_id:
            del_owner = http_client.delete(f"/owners/{owner_id}")
            logger.info(f"清理主人{owner_id},code:{del_owner.status_code}")
