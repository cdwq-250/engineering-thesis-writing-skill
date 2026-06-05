# Thesis Writing Plan

- Title: 基于OEE的合成车间设备维护流程优化研究
- Thesis type: mechanical_manufacturing (机械/制造/设备维护类)
- Topic tags: equipment_maintenance, production_scheduling, quality_management

## Corpus-Grounded Rationale

Use the problem-to-method-to-validation arc: background and literature review, current-state diagnosis, design, validation, and limitations.
Do not copy source thesis text. Treat corpus signals as structure guidance only.

## Chapter Outline

### 第1章 绪论
- 1.1 研究背景与意义
- 1.2 国内外研究现状
- 1.3 研究内容与技术路线

### 第2章 理论基础与方法综述
- 2.1 相关理论基础
- 2.2 关键方法与评价指标
- 2.3 本文方法适用边界

### 第3章 对象现状与问题诊断
- 3.1 研究对象与流程说明
- 3.2 现状指标与问题识别
- 3.3 原因分析与改进需求

### 第4章 模型、策略或改进方案设计
- 4.1 设计目标与原则
- 4.2 核心模型/策略/流程设计
- 4.3 实施或仿真流程

### 第5章 验证与结果分析
- 5.1 场景、数据与参数设置
- 5.2 对比结果与指标分析
- 5.3 工程解释与局限性

### 第6章 总结与展望
- 6.1 研究工作总结
- 6.2 不足与后续工作

## Evidence Map

| Claim | Evidence Source | Evidence Type | Allowed Wording |
|---|---|---|---|
| 合成案例数据支持维护流程规范化分析 | examples/synthetic_maintenance_cases.csv | csv | 合成案例数据支持维护流程规范化分析 |
| 原型流程图说明维护决策节点 | examples/synthetic_maintenance_flow.md | figure | 原型流程图说明维护决策节点 |

## Figure And Table Plan

| Figure/Table | Purpose | Evidence Needed |
|---|---|---|
| 现状流程图 | 支撑结构、流程或验证叙述 | code/config/csv/figure/screenshot/document |
| 原因分析图 | 支撑结构、流程或验证叙述 | code/config/csv/figure/screenshot/document |
| 方案流程图 | 支撑结构、流程或验证叙述 | code/config/csv/figure/screenshot/document |
| 指标对比图 | 支撑结构、流程或验证叙述 | code/config/csv/figure/screenshot/document |
| 指标汇总表 | 汇总可验证指标 | examples/synthetic_maintenance_cases.csv, examples/synthetic_maintenance_flow.md |

## Metric Candidates

- OEE
- 停机时间
- 维护成本
- 延期时间
- 产线利用率
- 缺陷率

## Unsupported Or Risky Claims

- No unsupported strong claim detected from the provided evidence map.

## Next Verification Steps

- Fill every `待补充` evidence source before drafting result claims.
- Confirm whether data are real, simulated, prototype-level, or user-confirmed.
- Use conservative wording for prototype and simulation evidence.
- Run public-safety checks before committing generated materials.
