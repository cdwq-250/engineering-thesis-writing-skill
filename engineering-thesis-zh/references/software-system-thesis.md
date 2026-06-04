# Software System Thesis Pattern

Use this reference for Chinese engineering theses centered on a software platform, management system, web application, data system, or digital-twin prototype.

## Common Chapter Pattern

1. 绪论：研究背景、问题来源、研究意义、国内外现状、研究内容与技术路线。
2. 需求分析：用户角色、业务流程、功能需求、非功能需求、可行性或约束条件。
3. 总体设计：系统架构、模块划分、数据流、数据库设计、权限或安全设计。
4. 详细设计与实现：关键模块、接口、算法、数据持久化、前后端交互或部署结构。
5. 系统测试：测试环境、功能测试用例、边界和异常测试、结果截图或日志证据。
6. 总结与展望：完成工作、局限性、后续改进方向。

## Evidence Rules

- Map every module to source files, routes, services, database tables, configuration, logs, or screenshots.
- If there is no running-system evidence, write “原型验证” or “功能验证” rather than “上线运行”。
- Do not claim high concurrency, production deployment, large user scale, security hardening, or commercial use unless logs, tests, configuration, or user evidence prove it.
- Database design must match actual schema, entity definitions, migration files, or SQL scripts.

## Writing Style

- Use concrete module names and workflow verbs.
- Prefer “实现了……功能”“支持……流程”“完成……数据处理” over broad claims such as “显著提升效率”。
- Testing chapters should include input, operation, expected result, actual result, and evidence source.
