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

The `examples/` folder also contains a UAV thesis validation brief and evidence map that show how to ground thesis writing in code, tests, CSV outputs, and figures.

To summarize experiment CSV files for thesis writing, run:

```powershell
python engineering-thesis-zh\scripts\summarize_experiment_metrics.py path\to\results\csv --output examples\metric_summary.md
```
