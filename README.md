# engineering-thesis-writing-skill

Public Codex skill and tooling for evidence-grounded Chinese engineering graduate thesis writing.

This repository is designed for a local, legally accessed thesis corpus. It does **not** include copyrighted thesis PDFs, DOCX files, CAJ files, or full-text extracts. Public artifacts are limited to reusable scripts, anonymized aggregate statistics, synthetic examples, and the `engineering-thesis-zh` skill.

## Workflow

1. Collect Chinese engineering graduate theses through authorized school-library access.
2. Store original files only under ignored private directories such as `private_corpus/`.
3. Build a private manifest for the local corpus.
4. Run the extraction script to create structural metadata.
5. Optionally extract a local Markdown thesis draft for validation.
6. Run quality checks and aggregate analysis.
7. Use `engineering-thesis-zh` to plan and write thesis sections from real project evidence.
8. Run the public-safety scan before committing or pushing.

See `ENVIRONMENT.md` for Python dependency setup.

## Repository Layout

```text
engineering-thesis-writing-skill/
|-- engineering-thesis-zh/
|   |-- SKILL.md
|   |-- references/
|   `-- scripts/
|-- examples/
|-- public_stats/
`-- README.md
```

## Safety Rule

Do not commit original theses, converted documents, extracted full text, or long verbatim passages from copyrighted papers. The scripts intentionally focus on structure, labels, counts, and aggregate statistics.

See `PUBLISHING.md` for the GitHub publishing checklist.

## One-Command Local Pipeline

After placing legally obtained PDFs under `private_corpus/`, run:

```powershell
python engineering-thesis-zh\scripts\run_corpus_pipeline.py
```

After manually downloading PDFs or CAJ-family files into the browser download folder, archive new files into the ignored private corpus first:

```powershell
python engineering-thesis-zh\scripts\archive_downloads.py --dry-run --pdf-only --since-days 7 --include "维护|优化|调度|系统|设计|制造|装配|设备|质量|管理"
```

Before archiving a mixed download folder, screen files against the current family gaps:

```powershell
python engineering-thesis-zh\scripts\screen_downloads.py --source downloads --corpus-root private_corpus --summary public_stats\corpus\summary.json --pdf-only
```

The screening report is private by default under `private_outputs/`. If the archive preview is correct, rerun `archive_downloads.py` without `--dry-run`. The pipeline writes aggregate statistics, a public progress report, common-pattern coverage, rule candidates, a readiness gate report, and the next acquisition plan under `public_stats/corpus/`.

Check whether the current corpus is large and balanced enough before promoting observations into broad writing rules:

```powershell
python engineering-thesis-zh\scripts\check_corpus_readiness.py --summary public_stats\corpus\summary.json --output public_stats\corpus\readiness_report.md
```

Use `--strict` only for CI or release gates that must fail unless the corpus is large and balanced across thesis families.

To inspect shared signals across thesis families, read:

- `public_stats/corpus/common_patterns.md`
- `public_stats/corpus/commonality_matrix.csv`

The common-pattern report separates balanced cross-family candidates from sparse cross-family signals so that undersampled families do not create false generalizations.

The `examples/` folder also contains a UAV thesis validation brief and evidence map that show how to ground thesis writing in code, tests, CSV outputs, and figures.

To summarize experiment CSV files for thesis writing, run:

```powershell
python engineering-thesis-zh\scripts\summarize_experiment_metrics.py path\to\results\csv --output examples\metric_summary.md
```

## Evidence-Grounded Writing Pipeline

Use the writing pipeline after you have a project idea, code/data evidence, and a thesis family. It does not invent results; it creates a plan and draft skeleton with evidence placeholders.

1. Generate a gated collaboration plan:

```powershell
python engineering-thesis-zh\scripts\write_collaboration_plan.py --thesis-type mechanical_manufacturing --output private_outputs\collaboration_plan.md
```

2. Generate interview questions for the selected thesis type:

```powershell
python engineering-thesis-zh\scripts\write_profile_questions.py --thesis-type mechanical_manufacturing --output private_outputs\profile_questions.md
```

3. Fill a local `thesis-profile.json` using `engineering-thesis-zh\references\thesis-profile-schema.md`.

4. Validate the profile:

```powershell
python engineering-thesis-zh\scripts\validate_thesis_profile.py private_outputs\thesis-profile.json
```

5. Run the full writing pipeline:

```powershell
python engineering-thesis-zh\scripts\run_writing_pipeline.py --profile private_outputs\thesis-profile.json --output-dir private_outputs\writing_run
```

The pipeline writes:

- `thesis_plan.md`
- `manuscript_skeleton.md`
- `pipeline_report.md`

A public synthetic example is included under `examples/synthetic_thesis_profile.json` and `examples/synthetic_writing_pipeline/`. It contains no real thesis text or factory data.

Before any draft is delivered, audit unsupported strong claims:

```powershell
python engineering-thesis-zh\scripts\audit_manuscript_claims.py private_outputs\writing_run\manuscript_skeleton.md
```

Keep generated project-specific drafts under ignored private folders unless the user explicitly wants a public synthetic example.

## Validation

Run the local tests with:

```powershell
python -m pytest
```

Validate the skill and public-safety rules with:

```powershell
python engineering-thesis-zh\scripts\validate_skill.py engineering-thesis-zh
python engineering-thesis-zh\scripts\check_public_safety.py .
```
