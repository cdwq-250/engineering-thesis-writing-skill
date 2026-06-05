# Collaboration Workflow

Use this workflow when thesis writing requires multiple rounds with the user.
The goal is to prevent unsupported drafting and keep corpus, project evidence,
and manuscript work in separate gated stages.

## Stage Gates

| Stage | Purpose | User Input | Codex Output | Gate |
|---|---|---|---|---|
| 0 | Scope and corpus status | Thesis family, school constraints, available corpus access | Corpus readiness summary and next acquisition decision | `readiness_report.md` and `acquisition_plan.md` reviewed |
| 1 | Project evidence inventory | Code, data, experiments, figures, drafts, templates | Evidence inventory and missing-material list | Every intended strong claim has a source or is removed |
| 2 | Thesis profile | Answers to profile interview questions | `thesis-profile.json` draft | `validate_thesis_profile.py` passes |
| 3 | Plan and outline | Confirmed thesis profile and school format | Chapter outline, evidence map, figure/table plan | User approves scope; unsupported claims listed |
| 4 | Draft skeleton | Approved plan | Markdown manuscript skeleton with evidence placeholders | `audit_manuscript_claims.py` passes |
| 5 | Manuscript iteration | User corrections, new evidence, template requirements | Revised sections or final DOCX workflow | Public-safety and claim audit pass before delivery |

## Communication Rules

- Ask only for materials needed to pass the next gate.
- Treat missing data as a writing constraint, not as permission to invent.
- Keep real thesis PDFs, extracts, project drafts, and screening reports in ignored private folders.
- Use corpus signals only as structure guidance unless readiness gates prove balanced coverage.
- Re-run the relevant script after each new evidence batch or corpus acquisition batch.

## Stop Conditions

- Stop drafting if the user wants a strong result claim without evidence.
- Stop corpus rule promotion if `readiness_report.md` is not `balanced_large`.
- Stop public publishing if `check_public_safety.py` finds source documents or private extracts.
- Stop final delivery if claim audit reports unsupported deployment, superiority, or effectiveness claims.
