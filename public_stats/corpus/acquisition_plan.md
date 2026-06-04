# Acquisition Plan

This plan is generated from aggregate corpus counts. It does not include source documents or full text.

## Current Counts

- software: 0
- control/optimization: 2
- mechanical/manufacturing: 0

## Next Search Tasks

| Priority | Family | Batch Target | Query | Destination |
|---:|---|---:|---|---|
| 1 | software | 20 | 系统设计与实现 | `private_corpus/software` |
| 2 | software | 20 | 管理系统 设计与实现 | `private_corpus/software` |
| 3 | software | 20 | 信息系统 软件工程 | `private_corpus/software` |
| 4 | mechanical/manufacturing | 20 | 智能制造 装配生产线 | `private_corpus/mechanical` |
| 5 | mechanical/manufacturing | 20 | 设备维护 健康管理 | `private_corpus/mechanical` |
| 6 | mechanical/manufacturing | 20 | 工艺优化 制造 | `private_corpus/mechanical` |
| 7 | control/optimization | 20 | 生产调度 优化 | `private_corpus/control` |
| 8 | control/optimization | 20 | 维护策略 优化 | `private_corpus/control` |
| 9 | control/optimization | 20 | 离散事件仿真 调度 | `private_corpus/control` |

## Execution Notes

- Search in CNKI or Wanfang through authorized school-library access.
- Enter a thesis detail page and prefer `PDF下载` when available.
- After downloading, run the archiver in dry-run mode first.
- Archive only files that match the intended thesis batch; keep unrelated local files out of `private_corpus`.

Recommended archiver command:

```powershell
python engineering-thesis-zh\scripts\archive_downloads.py --dry-run --pdf-only --since-days 7 --include "维护|优化|调度|系统|设计|制造|装配|设备|质量|管理"
```
