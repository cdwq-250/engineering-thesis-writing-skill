# Corpus Readiness Report

This report is generated from aggregate metadata only. It does not publish thesis files, full text, or long source excerpts.

Overall readiness: `candidate_mechanical_only`

## Current Scope

- Records analyzed: 51
- Parse errors: 0 (0.0%)
- Weak heading records: 4 (7.8%)

## Family Coverage

| Family | Current Records | Target Records | Gap |
|---|---:|---:|---:|
| software/system | 0 | 100 | 100 |
| control/optimization | 22 | 100 | 78 |
| mechanical/manufacturing | 25 | 100 | 75 |

## Near-Term Milestones

| Family | Milestone | Target | Gap | Estimated Batches |
|---|---|---:|---:|---:|
| software/system | commonality family sample | 10 | 10 | 1 |
| software/system | balanced readiness family coverage | 100 | 100 | 5 |
| control/optimization | commonality family sample | 10 | 0 | 0 |
| control/optimization | balanced readiness family coverage | 100 | 78 | 4 |
| mechanical/manufacturing | commonality family sample | 10 | 0 | 0 |
| mechanical/manufacturing | balanced readiness family coverage | 100 | 75 | 4 |

## Gates

| Gate | Status | Detail |
|---|---|---|
| minimum total records | FAIL | 51/100 records |
| parse error rate | PASS | 0/51 = 0.0%; threshold <= 10.0% |
| weak heading rate | PASS | 4/51 = 7.8%; threshold <= 25.0% |
| software/system coverage | FAIL | 0/100 records |
| control/optimization coverage | FAIL | 22/100 records |
| mechanical/manufacturing coverage | FAIL | 25/100 records |

## Interpretation

The corpus can support cautious candidate rules for mechanical/manufacturing-style theses.
It is not ready for broad claims about all Chinese engineering graduate theses because software/system and control/optimization coverage remains insufficient.

## Next Actions

- Prioritize the families with the largest coverage gaps in `acquisition_plan.md`.
- Keep copyrighted source files under ignored private folders only.
- Rerun `run_corpus_pipeline.py` after each legal acquisition batch.
