#!/usr/bin/env python
"""Write a gated multi-turn collaboration plan for thesis work."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


STAGES = [
    {
        "stage": 0,
        "name": "Scope and Corpus Status",
        "user_input": "Thesis family, school constraints, and whether new corpus acquisition is allowed.",
        "codex_output": "Corpus readiness summary and next acquisition decision.",
        "gate": "Read `readiness_report.md`, `common_patterns.md`, and `acquisition_plan.md`.",
    },
    {
        "stage": 1,
        "name": "Project Evidence Inventory",
        "user_input": "Code, data, experiment outputs, figures, logs, drafts, templates, and known limitations.",
        "codex_output": "Evidence inventory and missing-material list.",
        "gate": "Every intended strong claim has a source or is removed/softened.",
    },
    {
        "stage": 2,
        "name": "Thesis Profile",
        "user_input": "Answers to `write_profile_questions.py` for the selected thesis type.",
        "codex_output": "A local `thesis-profile.json` draft.",
        "gate": "`validate_thesis_profile.py` passes.",
    },
    {
        "stage": 3,
        "name": "Plan and Outline",
        "user_input": "Confirmed profile, school format, and chapter constraints.",
        "codex_output": "Chapter outline, evidence map, figure/table plan, and risky-claim checklist.",
        "gate": "User approves scope and unsupported claims are listed.",
    },
    {
        "stage": 4,
        "name": "Draft Skeleton",
        "user_input": "Approved plan plus any newly supplied evidence.",
        "codex_output": "Markdown manuscript skeleton with evidence placeholders.",
        "gate": "`audit_manuscript_claims.py` passes.",
    },
    {
        "stage": 5,
        "name": "Manuscript Iteration",
        "user_input": "Corrections, new evidence, template requirements, and target sections.",
        "codex_output": "Revised sections, final manuscript workflow, or DOCX handoff.",
        "gate": "Public-safety scan and claim audit pass before delivery or publishing.",
    },
]


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def readiness_level(readiness_report: Path) -> str:
    if not readiness_report.exists():
        return "missing"
    for line in readiness_report.read_text(encoding="utf-8").splitlines():
        if line.startswith("Overall readiness:"):
            return line.split("`")[1] if "`" in line else line.split(":", 1)[1].strip()
    return "unknown"


def thesis_type_guidance(thesis_type: str) -> list[str]:
    if thesis_type == "software_system":
        return [
            "Collect repository paths for controllers/services/models/database migrations/tests.",
            "Require screenshots, API examples, or test output before writing implementation effects.",
            "Do not claim production deployment unless deployment logs or user confirmation exist.",
        ]
    if thesis_type == "control_optimization":
        return [
            "Collect variables, objectives, constraints, assumptions, datasets, and baseline methods.",
            "Require experiment CSV/log outputs before writing performance comparisons.",
            "Separate simulation results from real operational data.",
        ]
    if thesis_type == "mechanical_manufacturing":
        return [
            "Collect process object, current-state indicators, diagnosis evidence, and validation method.",
            "Require OEE/cost/downtime/quality data before writing improvement claims.",
            "Separate case calculations, simulation, expert review, and field trial evidence.",
        ]
    return ["Pick one thesis type before collecting a final profile."]


def write_plan(
    output: Path,
    thesis_type: str,
    summary: dict[str, Any],
    readiness: str,
) -> None:
    type_counts = summary.get("type_counts", {})
    lines = [
        "# Thesis Collaboration Plan",
        "",
        "This local plan coordinates multi-turn thesis writing. Keep project-specific versions in private folders when they contain real project details.",
        "",
        "## Current Corpus Status",
        "",
        f"- Thesis type target: `{thesis_type}`",
        f"- Records analyzed: {summary.get('record_count', 'unknown')}",
        f"- Readiness: `{readiness}`",
        f"- Software/system records: {type_counts.get('software_system', 0)}",
        f"- Control/optimization records: {type_counts.get('control_optimization', 0)}",
        f"- Mechanical/manufacturing records: {type_counts.get('mechanical_manufacturing', 0)}",
        "",
        "## Type-Specific Evidence Focus",
        "",
    ]
    lines.extend(f"- {item}" for item in thesis_type_guidance(thesis_type))
    lines.extend(["", "## Stage Plan", ""])
    for item in STAGES:
        lines.extend(
            [
                f"### Stage {item['stage']}: {item['name']}",
                "",
                f"- User input: {item['user_input']}",
                f"- Codex output: {item['codex_output']}",
                f"- Gate: {item['gate']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Immediate Next Questions",
            "",
            "1. Which thesis family should be the current writing target: software_system, control_optimization, or mechanical_manufacturing?",
            "2. What real project evidence is already available: code, data, experiment output, figures, draft, or school template?",
            "3. Which strong claims do you want to make, and what concrete evidence supports each one?",
            "",
            "## Stop Conditions",
            "",
            "- Do not draft result claims without evidence.",
            "- Do not promote corpus observations while readiness is not `balanced_large`.",
            "- Do not publish private corpus files, full-text extracts, screening reports, or project-specific drafts.",
            "",
        ]
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a gated thesis collaboration plan.")
    parser.add_argument(
        "--thesis-type",
        choices=["software_system", "control_optimization", "mechanical_manufacturing", "undecided"],
        default="undecided",
    )
    parser.add_argument("--summary", type=Path, default=Path("public_stats/corpus/summary.json"))
    parser.add_argument("--readiness-report", type=Path, default=Path("public_stats/corpus/readiness_report.md"))
    parser.add_argument("--output", type=Path, default=Path("private_outputs/collaboration_plan.md"))
    args = parser.parse_args()

    write_plan(args.output, args.thesis_type, read_json(args.summary), readiness_level(args.readiness_report))
    print(f"collaboration_plan={args.output}")


if __name__ == "__main__":
    main()
