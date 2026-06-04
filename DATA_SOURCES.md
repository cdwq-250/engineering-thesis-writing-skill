# Data Sources And Corpus Strategy

This project expects thesis files to be obtained legally through the user's school-library access. Do not bypass authentication, paywalls, robots restrictions, or database terms.

## Primary Sources

- CNKI master's/doctoral thesis databases through school-library access.
- Wanfang Chinese dissertation and thesis databases through school-library access.
- CALIS thesis services when available through institutional access.
- Local school repositories or library thesis portals when downloads are permitted.

## Target Corpus

Build a 1000+ item corpus across three engineering thesis families:

- `software`: software systems, information systems, platforms, databases, web systems, management systems.
- `control`: control, optimization, scheduling, simulation, prediction, decision algorithms.
- `mechanical`: mechanical engineering, manufacturing, assembly, equipment health, maintenance, intelligent manufacturing.

Recommended first target:

```text
software   300-400 theses
control    300-400 theses
mechanical 300-400 theses
```

## Search Keyword Seeds

Use these as starting points and expand with database recommendation terms.

Software:

- 系统设计与实现
- 管理系统
- 信息系统
- 平台设计
- 数据库设计
- Web 系统
- 软件工程

Control and optimization:

- 生产调度
- 优化算法
- 维护策略
- 离散事件仿真
- 多目标优化
- 预测控制
- 强化学习

Mechanical and manufacturing:

- 智能制造
- 装配生产线
- 设备维护
- 设备健康管理
- 工艺优化
- 数字孪生
- 车间调度

## Download And Naming

Put files under ignored local folders:

```text
private_corpus/software/
private_corpus/control/
private_corpus/mechanical/
```

Recommended filename pattern:

```text
year_school_short-title.pdf
```

Examples:

```text
2024_xxx-university_equipment-maintenance-scheduling.pdf
2023_xxx-university_management-system-design.pdf
```

Prefer `PDF下载` when the database offers it. The extraction pipeline reads PDFs directly. CAJ-family files (`.caj`, `.kdh`, `.nh`) are allowed in the private manifest, but they are marked `convert_to_pdf_first` and must be converted before text extraction.

## CAJ/KDH/NH Handling

Use CAJ-family files only as a fallback when PDF is unavailable.

Recommended conversion order:

1. Open the file with an authorized CNKI/CAJ reader and export or print to PDF.
2. Save the converted PDF next to the source file in `private_corpus/...`.
3. Keep the original CAJ/KDH/NH private; never commit it.
4. Run the corpus pipeline after the PDF exists.

If the converted PDF is image-only or has poor text extraction, mark `ocr_required=yes` in the private manifest and use OCR before relying on keywords, headings, or figure/table captions.

## Metadata To Preserve

Maintain or enrich a local manifest with:

- local path
- thesis family
- title
- year
- school
- degree level
- discipline
- keywords
- source database
- download date
- file format
- conversion status
- notes about OCR/scanned pages

Only aggregate statistics may be public.

## What Must Stay Private

Do not commit:

- PDFs, CAJ, DOC, DOCX, KDH, NH
- full text extracts
- OCR text
- long verbatim passages
- screenshots of copyrighted pages
- database account or session details
