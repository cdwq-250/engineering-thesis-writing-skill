# Acquisition Plan

This plan is generated from aggregate corpus counts. It does not include source documents or full text.

## Current Counts

- software: 0
- control/optimization: 22
- mechanical/manufacturing: 25

## Batch Policy

- Fill the lowest-count family first; do not add more mechanical/manufacturing papers until software and control/optimization coverage improve.
- Accept a paper only when the title and abstract match the family filter; skip irrelevant business-only or management-only papers.
- Clear the near-term commonality gate first, then the balanced readiness gate, then the deep corpus target.
- After each batch, run the corpus pipeline and read `readiness_report.md` plus `common_patterns.md` before deciding the next batch.

## Coverage Milestones

| Family | Current | Commonality Gate | Readiness Gate | Deep Target | Batches To Readiness | Batches To Deep Target |
|---|---:|---:|---:|---:|---:|---:|
| software | 0 | 10 gap to 10 | 100 gap to 100 | 300 gap to 300 | 5 | 15 |
| control/optimization | 22 | 0 gap to 10 | 78 gap to 100 | 278 gap to 300 | 4 | 14 |
| mechanical/manufacturing | 25 | 0 gap to 10 | 75 gap to 100 | 275 gap to 300 | 4 | 14 |

## Next Search Tasks

| Priority | Family | Commonality Gap | Readiness Gap | Deep Gap | Batch Target | Query | Destination |
|---:|---|---:|---:|---:|---:|---|---|
| 1 | software | 10 | 100 | 300 | 20 | 系统设计与实现 | `private_corpus/software` |
| 2 | software | 10 | 100 | 300 | 20 | 管理系统 设计与实现 | `private_corpus/software` |
| 3 | software | 10 | 100 | 300 | 20 | 信息系统 软件工程 | `private_corpus/software` |
| 4 | control/optimization | 0 | 78 | 278 | 20 | 生产调度 优化 | `private_corpus/control` |
| 5 | control/optimization | 0 | 78 | 278 | 20 | 维护策略 优化 | `private_corpus/control` |
| 6 | control/optimization | 0 | 78 | 278 | 20 | 离散事件仿真 调度 | `private_corpus/control` |
| 7 | mechanical/manufacturing | 0 | 75 | 275 | 20 | 智能制造 装配生产线 | `private_corpus/mechanical` |
| 8 | mechanical/manufacturing | 0 | 75 | 275 | 20 | 设备维护 健康管理 | `private_corpus/mechanical` |
| 9 | mechanical/manufacturing | 0 | 75 | 275 | 20 | 工艺优化 制造 | `private_corpus/mechanical` |

## Acceptance Filters

- software: Title should describe a software/system/platform design and implementation thesis.
- control/optimization: Title should center on optimization, scheduling, control, simulation, or algorithmic decision models.
- mechanical/manufacturing: Title should be mechanical, manufacturing, workshop, equipment, maintenance, process, or production-line focused.

## Execution Notes

- Search in CNKI or Wanfang through authorized school-library access.
- Enter a thesis detail page and prefer `PDF下载` when available.
- After downloading, run the archiver in dry-run mode first.
- Archive only files that match the intended thesis batch; keep unrelated local files out of `private_corpus`.
- For the current corpus, prioritize `private_corpus/software` and `private_corpus/control` before adding more mechanical/manufacturing papers.

Recommended archiver command:

```powershell
python engineering-thesis-zh\scripts\archive_downloads.py --dry-run --pdf-only --since-days 7 --include "系统|设计|实现|平台|调度|优化|控制|算法|仿真|模型"
```
