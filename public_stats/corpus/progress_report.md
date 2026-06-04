# Corpus Progress Report

This report is generated from local structural metadata. It intentionally excludes original theses, full text extracts, and long verbatim passages.

## Current Coverage

- Records analyzed: 33
- Parse errors: 0 (0.0%)
- Average extracted headings per record: 12.0
- Average extracted keywords per record: 4.0
- Average extracted figure/table labels per record: 3.2
- Weak heading records: 6
- Classification method: weighted keywords over file name, title candidates, keywords, and headings

## Type Distribution

- mechanical_manufacturing: 26
- control_optimization: 3
- mixed: 3
- software_system: 1

## Classification Confidence

- high: 29
- medium: 1
- tie: 3

## Common Heading Patterns

- 1.2: 68
- 1.1: 46
- 5.2: 22
- 3.3: 17
- 1.3: 17
- 4.3: 17
- Abstract: 16
- 4.2: 15
- 3.2: 12
- 第四章: 11

## Common Keyword Candidates

- 精益生产: 5
- 设备管理: 4
- TPM: 4
- 全面质量管理: 2
- 优化方案: 2
- 设备综合效率: 2
- OEE: 2
- 设备维护: 2
- 5M1E: 2
- 分析: 2

## Figure/Table Label Counts

- 图: 81
- 表: 26

## Topic Tags

- equipment_maintenance: 28
- algorithm_modeling: 26
- production_scheduling: 17
- software_platform: 10
- lean_production: 8
- quality_management: 7

## Topic Co-Occurrence

- algorithm_modeling + equipment_maintenance: 23
- algorithm_modeling + production_scheduling: 14
- equipment_maintenance + production_scheduling: 14
- algorithm_modeling + software_platform: 8
- equipment_maintenance + software_platform: 8
- algorithm_modeling + lean_production: 7
- production_scheduling + software_platform: 7
- algorithm_modeling + quality_management: 6
- lean_production + quality_management: 5
- equipment_maintenance + quality_management: 5

## Chapter Role Signals

- current_state_diagnosis: 29
- background_significance: 24
- scheme_design: 21
- literature_review: 20
- model_design: 12
- cause_analysis: 10
- experiment_evaluation: 9
- research_content_route: 7
- system_implementation: 5
- summary_outlook: 2

## Interpretation Guardrails

- Treat current commonalities as preliminary until each target family has a larger sample.
- Do not infer writing rules from one or two theses; use early records mainly to validate extraction quality.
- Promote a pattern into the skill only after it appears across multiple schools, topics, and thesis families.

## Next Acquisition Batch

- software: current 1, next target +20 files
- control/optimization: current 3, next target +20 files
- mechanical/manufacturing: current 26, next target +20 files

Recommended immediate action: download another 10-20 legally accessible PDF theses from CNKI or Wanfang, then run `archive_downloads.py` and `run_corpus_pipeline.py`.
