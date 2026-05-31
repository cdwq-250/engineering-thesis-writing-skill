# Environment Setup

This repository is designed to run with Python 3.12.

## Current Core Dependencies

The core scripts use:

- `pypdf` for PDF text extraction
- `pandas` for CSV and metric tables
- `scikit-learn` for later corpus clustering or topic features
- `matplotlib` for future aggregate charts
- `pyyaml` for skill metadata workflows

Install with:

```powershell
python -m pip install -r requirements.txt
```

## Optional Dependencies

The following packages are recommended for richer local analysis:

- `pdfplumber`: better layout-aware PDF extraction
- `python-docx`: DOCX thesis draft inspection
- `jieba`: Chinese tokenization for keyword and topic analysis

They are included in `requirements.txt`, but the current v1 scripts can run without them except for future richer analysis paths.

## GitHub CLI

Publishing requires an authenticated `gh` session:

```powershell
gh auth login
gh auth status
```

If a stale token causes failure:

```powershell
gh auth logout -h github.com -u cdwq-250
gh auth login -h github.com
```

## Local Corpus Layout

Place legally obtained thesis PDFs under:

```text
private_corpus/software/
private_corpus/control/
private_corpus/mechanical/
```

These folders are ignored by git.

