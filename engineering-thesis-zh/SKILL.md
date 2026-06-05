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
   - For multi-turn user collaboration, read `references/collaboration-workflow.md`, run `write_collaboration_plan.py`, then run `write_profile_questions.py` for the selected thesis type before collecting a thesis profile.
   - Read the project repository, experiment outputs, draft thesis, school template, and user constraints before drafting.
   - If the task uses a corpus, keep original papers and full-text extracts local and private.
   - If public corpus reports exist, read `public_stats/corpus/progress_report.md`, `public_stats/corpus/common_patterns.md`, `public_stats/corpus/rule_candidates.md`, `public_stats/corpus/readiness_report.md`, and `public_stats/corpus/acquisition_plan.md` before making corpus-based claims.

2. Load focused references.
   - Corpus-grounded writing rules: read `references/corpus-derived-writing-rules.md` when public corpus reports exist or when the task asks for thesis commonalities.
   - Thesis planning profile: read `references/thesis-profile-schema.md` before asking the user for project evidence or running `generate_thesis_plan.py`.
   - Software system thesis: read `references/software-system-thesis.md`.
   - Control or optimization thesis: read `references/control-optimization-thesis.md`.
   - Mechanical or intelligent-manufacturing application thesis: read `references/mechanical-manufacturing-thesis.md`.
   - Experiment sections: read `references/experiment-writing.md`.
   - Figures and evidence mapping: read `references/figure-and-evidence-rules.md`.
   - Similarity or AIGC rewriting: read `references/similarity-aigc-rewrite.md`.
   - Multi-turn collaboration gates: read `references/collaboration-workflow.md`.

3. Build an evidence map before writing.
   - Run `write_evidence_inventory.py` on the project root when the user has code/data/files but no clean evidence list yet.
   - Map every major claim to code, configuration, data, experiment scripts, test results, figures, logs, or user-provided materials.
   - Mark unsupported claims for deletion or conservative weakening.
   - Prefer "functional verification" and "scenario analysis" unless formal benchmarks or deployment evidence exist.

4. Draft or revise the thesis.
   - Use corpus-derived structure patterns as a guide, not as text to copy.
   - Use `references/corpus-derived-writing-rules.md` to shape shared chapter logic, diagnosis-design-validation flow, and claim boundaries.
   - Write in Chinese academic engineering style with concrete objects, variables, methods, and results.
   - Preserve factual boundaries and explicitly state model assumptions and limitations.
   - Treat corpus findings as preliminary until enough records exist across multiple schools, topics, and thesis families.

5. Verify before delivery.
   - Check that every result discussed has a visible source.
   - Check that all figures/tables are supported by project evidence.
   - Run `audit_manuscript_claims.py` on generated Markdown drafts before delivery when the draft contains result or deployment claims.
   - Check that no copyrighted paper text, extracted full text, or unsupported claims enter deliverables.

## Corpus Tooling

Use scripts in `scripts/` when a local thesis corpus is available:

- `archive_downloads.py`: copy legally downloaded thesis files into the ignored private corpus with hash-based deduplication and filters.
- `write_batch_tracker.py`: generate a private per-batch acquisition worksheet from the public plan before a manual CNKI/Wanfang download session.
- `sync_batch_tracker_from_screening.py`: sync `screen_downloads.py` output back into the private tracker so screening decisions and duplicates do not need manual re-entry.
- `summarize_batch_tracker.py`: summarize a filled private acquisition worksheet into batch progress, archived counts, and remaining family gaps.
- `extract_outline.py`: extract structural metadata from PDF files.
- `analyze_corpus.py`: aggregate chapter, keyword, figure/table, and thesis-type statistics.
- `quality_check.py`: check duplicate records, missing fields, and parse failures.
- `write_corpus_report.py`: generate an aggregate progress report from structural metadata.
- `write_rule_candidates.py`: generate non-promoted candidate writing rules with sample-size gates.
- `write_acquisition_plan.py`: generate the next balanced CNKI/Wanfang search plan from current sample counts, including near-term gate gaps and estimated batches.
- `check_public_safety.py`: scan a repository before commit or push for private/copyrighted artifacts.
- `summarize_experiment_metrics.py`: summarize CSV experiment metrics for evidence-grounded experiment chapter writing.
- `generate_thesis_plan.py`: generate a corpus-grounded chapter outline, evidence map, figure/table plan, and risky-claim checklist from a project profile.
- `generate_manuscript_skeleton.py`: generate a conservative Markdown thesis draft skeleton with evidence placeholders from a validated thesis profile.
- `audit_manuscript_claims.py`: scan generated Markdown drafts for unsupported strong claims against the Evidence Register.
- `validate_thesis_profile.py`: validate a thesis planning profile before generating a plan; blocks unsupported strong claims without evidence sources.
- `write_profile_questions.py`: generate focused interview questions for collecting a thesis profile through multi-turn user collaboration.
- `write_collaboration_plan.py`: generate a gated multi-turn plan that coordinates corpus acquisition, evidence collection, profile validation, outline generation, and drafting.
- `write_evidence_inventory.py`: scan a project workspace and produce a private evidence inventory with seed rows for `thesis-profile.json`.
- `seed_thesis_profile.py`: convert the private evidence inventory into an editable `thesis-profile` seed before validation.
- `run_writing_prep.py`: generate the private collaboration plan, evidence inventory, `thesis-profile` seed, and profile questions in one command.
- `run_writing_pipeline.py`: run profile validation, plan generation, skeleton generation, and claim audit in one reproducible pipeline.

The scripts are intentionally structural. They do not publish full text.

## Corpus-Grounded Rule Promotion

When turning corpus observations into writing guidance:

1. Use 1-5 records only to debug extraction quality and produce acquisition priorities.
2. Use 6-30 records to identify candidate patterns, but label them preliminary.
3. Promote a chapter pattern or writing rule into references only after it appears across multiple thesis families, schools, or topics.
4. Never copy source-paper wording into the skill. Convert observations into abstract structure rules, evidence rules, or claim-boundary rules.
5. Use `public_stats/corpus/rule_candidates.md` as the staging area for observations that are not yet safe to promote.
6. If sample distribution is unbalanced, follow `public_stats/corpus/acquisition_plan.md` before drawing stronger conclusions.

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
- sample-size caveats and next acquisition actions when the corpus is still small or unbalanced
