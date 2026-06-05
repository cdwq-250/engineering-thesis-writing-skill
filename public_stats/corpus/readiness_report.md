# Corpus Readiness Report

This report is generated from aggregate metadata only. It does not publish thesis files, full text, or long source excerpts.

Overall readiness: `candidate_mechanical_only`

## Current Scope

- Records analyzed: 34
- Parse errors: 0 (0.0%)
- Weak heading records: 6 (17.6%)

## Family Coverage

| Family | Current Records | Target Records | Gap |
|---|---:|---:|---:|
| software/system | 1 | 100 | 99 |
| control/optimization | 3 | 100 | 97 |
| mechanical/manufacturing | 26 | 100 | 74 |

## Gates

| Gate | Status | Detail |
|---|---|---|
| minimum total records | FAIL | 34/100 records |
| parse error rate | PASS | 0/34 = 0.0%; threshold <= 10.0% |
| weak heading rate | PASS | 6/34 = 17.6%; threshold <= 25.0% |
| software/system coverage | FAIL | 1/100 records |
| control/optimization coverage | FAIL | 3/100 records |
| mechanical/manufacturing coverage | FAIL | 26/100 records |

## Interpretation

The corpus can support cautious candidate rules for mechanical/manufacturing-style theses.
It is not ready for broad claims about all Chinese engineering graduate theses because software/system and control/optimization coverage remains insufficient.

## Next Actions

- Prioritize the families with the largest coverage gaps in `acquisition_plan.md`.
- Keep copyrighted source files under ignored private folders only.
- Rerun `run_corpus_pipeline.py` after each legal acquisition batch.
