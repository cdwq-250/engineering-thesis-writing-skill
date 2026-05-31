# Software System Thesis Pattern

Use this reference for Chinese engineering theses centered on a software platform, management system, web application, data system, or digital-twin prototype.

## Common Chapter Pattern

1. 绪论: background, problem, research significance, domestic/foreign status, research content.
2. 需求分析: user roles, business process, functional requirements, non-functional requirements.
3. 总体设计: architecture, module design, data flow, database design, security or permission design.
4. 详细设计与实现: key modules, interfaces, algorithms, data persistence, front-end/back-end interaction.
5. 系统测试: environment, functional test cases, boundary/error cases, result screenshots.
6. 总结与展望: completed work, limitations, future improvements.

## Evidence Rules

- Map every module to source files, routes, services, database tables, configuration, or screenshots.
- If there is no running system screenshot, write "原型验证" or "功能验证" rather than "上线运行".
- Do not claim high concurrency, production deployment, large user scale, or security hardening unless logs/tests/config prove it.
- Database design must match actual schema or entity definitions.

## Writing Style

- Use concrete module names and workflow verbs.
- Prefer "实现了...功能" and "支持...流程" over broad claims such as "显著提升效率".
- Testing chapter should include input, operation, expected result, actual result, and evidence source.

