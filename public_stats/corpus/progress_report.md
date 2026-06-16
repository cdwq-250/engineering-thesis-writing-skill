# Corpus Progress Report

This report is generated from local structural metadata. It intentionally excludes original theses, full text extracts, and long verbatim passages.

## Current Coverage

- Records analyzed: 51
- Parse errors: 0 (0.0%)
- Average extracted headings per record: 32.6
- Average extracted keywords per record: 4.2
- Average extracted figure/table labels per record: 18.3
- Weak heading records: 4
- Classification method: weighted keywords over file name, title candidates, keywords, and headings

## Type Distribution

- mechanical_manufacturing: 25
- control_optimization: 22
- unknown: 1
- mixed: 3

## Classification Confidence

- high: 46
- medium: 1
- unknown: 1
- tie: 3

## Common Heading Patterns

- 1.2: 178
- 2.2: 143
- 2.1: 122
- 3.2: 122
- 3.3: 101
- 2.3: 83
- 1.3: 74
- 1.1: 71
- 3.1: 64
- 3.4: 50

## Common Keyword Candidates

- 多智能体系统: 6
- 精益生产: 5
- 深度强化学习: 5
- 设备管理: 4
- TPM: 4
- 强化学习: 4
- 全面质量管理: 2
- 优化方案: 2
- 设备综合效率: 2
- OEE: 2

## Figure/Table Label Counts

- 图: 648
- 表: 287

## Topic Tags

- algorithm_modeling: 42
- equipment_maintenance: 29
- software_platform: 22
- production_scheduling: 19
- lean_production: 10
- quality_management: 9

## Topic Co-Occurrence

- algorithm_modeling + equipment_maintenance: 26
- algorithm_modeling + software_platform: 18
- algorithm_modeling + production_scheduling: 17
- equipment_maintenance + production_scheduling: 14
- algorithm_modeling + lean_production: 9
- algorithm_modeling + quality_management: 9
- equipment_maintenance + software_platform: 9
- production_scheduling + software_platform: 8
- equipment_maintenance + lean_production: 7
- equipment_maintenance + quality_management: 7

## Chapter Role Signals

- current_state_diagnosis: 47
- literature_review: 40
- scheme_design: 39
- background_significance: 38
- research_content_route: 33
- model_design: 23
- experiment_evaluation: 23
- cause_analysis: 12
- result_discussion: 9
- summary_outlook: 7

## Interpretation Guardrails

- Treat current commonalities as preliminary until each target family has a larger sample.
- Do not infer writing rules from one or two theses; use early records mainly to validate extraction quality.
- Promote a pattern into the skill only after it appears across multiple schools, topics, and thesis families.

## Next Acquisition Batch

- software: current 0, next target +20 files
- control/optimization: current 22, next target +20 files
- mechanical/manufacturing: current 25, next target +20 files

Recommended immediate action: download another 10-20 legally accessible PDF theses from CNKI or Wanfang, then run `archive_downloads.py` and `run_corpus_pipeline.py`.
