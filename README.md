Spring PetClinic REST API 自动化测试
基于 Postman + Newman 的接口自动化测试项目，覆盖主人、宠物、就诊等核心业务链路的功能验证与回归测试。

测试设计：Postman 组织测试集，覆盖 POST/GET/PUT 接口，内置状态码、响应结构、字段值断言及跨请求参数传递

自动化执行：Newman 命令行运行，生成 HTML 报告

持续集成：GitHub Actions 自动触发测试流水线

验证 API 在完整业务流下的功能正确性与数据一致性，为后续性能测试、契约测试提供基础。
