# Corpus Workflow

This workflow explains how to read a legally obtained local corpus of Chinese engineering graduate theses.

## 1. Put Thesis Files In Private Folders

Download theses through authorized school-library access. Store them locally under ignored private folders:

```text
private_corpus/
|-- software/
|-- control/
`-- mechanical/
```

Accepted v1 input is PDF. If a thesis is downloaded as CAJ, convert it to PDF with an authorized reader/tool before analysis.

Do not commit PDF, DOC, DOCX, CAJ, KDH, or full-text extracts.

After manually downloading papers through CNKI or another authorized portal, archive new files from the browser download folder:

```powershell
python engineering-thesis-zh\scripts\archive_downloads.py --limit 20
```

For a no-write preview:

```powershell
python engineering-thesis-zh\scripts\archive_downloads.py --dry-run
```

The archiver copies files into `private_corpus/cnki_manual/` and skips files already present by SHA-256 hash. It does not delete or move anything from `Downloads`.

## 2. Extract Structural Metadata

First build a private manifest:

```powershell
python engineering-thesis-zh\scripts\build_manifest.py private_corpus --output private_extracts\manifest.csv
```

Fill or enrich the blank metadata columns when practical. The manifest stays private.

To run the full PDF pipeline in one command, use:

```powershell
python engineering-thesis-zh\scripts\run_corpus_pipeline.py
```

For an empty-directory smoke test, use:

```powershell
python engineering-thesis-zh\scripts\run_corpus_pipeline.py --allow-empty
```

Run:

```powershell
python engineering-thesis-zh\scripts\extract_outline.py private_corpus --output private_extracts\records.jsonl
```

For an existing Markdown thesis draft, run:

```powershell
python engineering-thesis-zh\scripts\extract_markdown_outline.py path\to\thesis.md --output private_extracts\draft_records.jsonl
```

The extractor records structural fields such as:

- file name
- page count
- title candidates
- keyword candidates
- chapter headings
- figure/table titles
- parse errors

It is not intended to publish full thesis text.

## 3. Check Metadata Quality

Run:

```powershell
python engineering-thesis-zh\scripts\quality_check.py private_extracts\records.jsonl --min-headings 5
```

If many records have too few headings, inspect a sample manually. Some PDFs may be scanned images and require OCR outside this repository.

## 4. Produce Public Aggregate Statistics

Run:

```powershell
python engineering-thesis-zh\scripts\analyze_corpus.py private_extracts\records.jsonl --output-dir public_stats\corpus
```

Review outputs before committing. Public statistics should remain aggregate and non-reconstructive.

## 5. Safety Scan Before Commit Or Push

Run:

```powershell
python engineering-thesis-zh\scripts\check_public_safety.py .
```

The check fails if private directories contain files, if banned document formats appear in public paths, or if suspicious thesis-source text appears in public files.

## 6. Use The Skill

After aggregate analysis, use `engineering-thesis-zh` to:

- compare common chapter patterns across thesis types
- plan a Chinese engineering graduate thesis from real project evidence
- write experiment sections from actual metrics
- map claims to code, tests, CSV files, logs, figures, or screenshots
- rewrite similarity/AIGC-risk paragraphs without changing facts
