---
name: engineering-thesis-zh
description: Plan, audit, and draft Chinese engineering graduate theses from real project evidence and legally analyzed thesis-corpus patterns. Use for Chinese master's/doctoral engineering thesis outline design, software/control/mechanical thesis chapter planning, experiment chapter writing, figure/table planning, evidence mapping from code/results, similarity or AIGC risk rewriting, and corpus-based thesis-style analysis.
---

# Engineering Thesis ZH

## Overview

Use this skill to write Chinese engineering graduate theses conservatively from evidence. It combines large-corpus structure patterns with the user's real code, data, experiments, figures, and drafts.

Never invent project facts, experiment results, deployment scale, real factory data, user scale, performance claims, or unsupported innovation points. Treat the codebase, experiment outputs, supplied documents, and user-confirmed data as the authority.

## Workflow

1. Establish thesis type and evidence.
   - Identify whether the task is a software-system, control/optimization, or mechanical/manufacturing application thesis.
   - Read the project repository, experiment outputs, draft thesis, school template, and user constraints before drafting.
   - If the task uses a corpus, keep original papers and full-text extracts local and private.

2. Load focused references.
   - Software system thesis: read `references/software-system-thesis.md`.
   - Control or optimization thesis: read `references/control-optimization-thesis.md`.
   - Mechanical or intelligent-manufacturing application thesis: read `references/mechanical-manufacturing-thesis.md`.
   - Experiment sections: read `references/experiment-writing.md`.
   - Figures and evidence mapping: read `references/figure-and-evidence-rules.md`.
   - Similarity or AIGC rewriting: read `references/similarity-aigc-rewrite.md`.

3. Build an evidence map before writing.
   - Map every major claim to code, configuration, data, experiment scripts, test results, figures, logs, or user-provided materials.
   - Mark unsupported claims for deletion or conservative weakening.
   - Prefer "functional verification" and "scenario analysis" unless formal benchmarks or deployment evidence exist.

4. Draft or revise the thesis.
   - Use corpus-derived structure patterns as a guide, not as text to copy.
   - Write in Chinese academic engineering style with concrete objects, variables, methods, and results.
   - Preserve factual boundaries and explicitly state model assumptions and limitations.

5. Verify before delivery.
   - Check that every result discussed has a visible source.
   - Check that all figures/tables are supported by project evidence.
   - Check that no copyrighted paper text, extracted full text, or unsupported claims enter deliverables.

## Corpus Tooling

Use scripts in `scripts/` when a local thesis corpus is available:

- `extract_outline.py`: extract structural metadata from PDF files.
- `analyze_corpus.py`: aggregate chapter, keyword, figure/table, and thesis-type statistics.
- `quality_check.py`: check duplicate records, missing fields, and parse failures.
- `check_public_safety.py`: scan a repository before commit or push for private/copyrighted artifacts.
- `summarize_experiment_metrics.py`: summarize CSV experiment metrics for evidence-grounded experiment chapter writing.

The scripts are intentionally structural. They do not publish full text.

## Output Expectations

For planning tasks, output:

- chapter outline with up to three heading levels
- evidence map by chapter
- experiment and figure/table plan
- unsupported-claim removal list
- next verification steps

For drafting tasks, output:

- polished Chinese thesis prose
- source/evidence notes outside the manuscript text when useful
- conservative limitations and future work

For corpus-analysis tasks, output:

- aggregate statistics only
- no raw thesis text
- no long verbatim passages from source papers
