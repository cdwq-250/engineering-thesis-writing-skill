# Similarity And AIGC Rewrite Rules

Use this reference when rewriting Chinese thesis text to reduce similarity or AIGC risk while preserving truth.

## Principles

- Preserve project facts before changing style.
- Rewrite sentence logic and paragraph structure, not just synonyms.
- Add concrete project evidence where generic wording is causing template-like prose.
- Delete unsupported claims instead of polishing them.
- Do not fabricate experiments, data, citations, deployment, or novelty.

## Rewrite Moves

- Replace generic background with project-specific scenario constraints.
- Split over-polished long sentences into observation, method, and implication.
- Convert vague claims into evidence-bound claims.
- Move repeated definitions into a theory chapter and keep implementation chapters concrete.
- Add limitations where claims would otherwise sound absolute.

## Before/After Pattern

Unsafe:

`本文系统具有较高的实用价值和推广意义，能够显著提升企业生产效率。`

Safer:

`在本文设定的无人机装配仿真场景中，系统能够记录订单流转、工位利用率和维护停机时间等指标，为后续比较不同调度与维护策略提供实验基础。`

## Final Check

- Does the rewritten paragraph still match the code/data?
- Did any new claim appear without evidence?
- Does the paragraph read like this specific project rather than a generic template?

