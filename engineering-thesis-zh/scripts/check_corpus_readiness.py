#!/usr/bin/env python
"""Gate whether aggregate corpus statistics are ready for broad thesis-writing claims."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


FAMILIES = {
    "software_system": "software/system",
    "control_optimization": "control/optimization",
    "mechanical_manufacturing": "mechanical/manufacturing",
}


@dataclass
class Gate:
    name: str
    passed: bool
    detail: str


def read_summary(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def pct(numerator: int, denominator: int) -> float:
    if denominator <= 0:
        return 0.0
    return numerator / denominator


def classify_readiness(gates: list[Gate], total: int, type_counts: dict[str, int], target_per_family: int) -> str:
    if all(gate.passed for gate in gates):
        return "balanced_large"
    mechanical = type_counts.get("mechanical_manufacturing", 0)
    if total >= 30 and mechanical >= min(20, target_per_family) and mechanical == max(type_counts.values() or [0]):
        return "candidate_mechanical_only"
    return "insufficient"


def build_gates(
    summary: dict[str, Any],
    min_total_records: int,
    target_per_family: int,
    max_parse_error_rate: float,
    max_weak_heading_rate: float,
) -> list[Gate]:
    total = int(summary.get("record_count", 0))
    parse_errors = int(summary.get("parse_error_count", 0))
    weak_headings = int(summary.get("weak_heading_record_count", 0))
    type_counts = {key: int(value) for key, value in summary.get("type_counts", {}).items()}

    gates = [
        Gate(
            "minimum total records",
            total >= min_total_records,
            f"{total}/{min_total_records} records",
        ),
        Gate(
            "parse error rate",
            pct(parse_errors, total) <= max_parse_error_rate,
            f"{parse_errors}/{total} = {pct(parse_errors, total):.1%}; threshold <= {max_parse_error_rate:.1%}",
        ),
        Gate(
            "weak heading rate",
            pct(weak_headings, total) <= max_weak_heading_rate,
            f"{weak_headings}/{total} = {pct(weak_headings, total):.1%}; threshold <= {max_weak_heading_rate:.1%}",
        ),
    ]

    for family_key, label in FAMILIES.items():
        current = type_counts.get(family_key, 0)
        gates.append(
            Gate(
                f"{label} coverage",
                current >= target_per_family,
                f"{current}/{target_per_family} records",
            )
        )
    return gates


def write_report(
    output: Path,
    summary: dict[str, Any],
    gates: list[Gate],
    readiness: str,
    target_per_family: int,
) -> None:
    total = int(summary.get("record_count", 0))
    type_counts = {key: int(value) for key, value in summary.get("type_counts", {}).items()}
    weak_headings = int(summary.get("weak_heading_record_count", 0))
    parse_errors = int(summary.get("parse_error_count", 0))

    lines = [
        "# Corpus Readiness Report",
        "",
        "This report is generated from aggregate metadata only. It does not publish thesis files, full text, or long source excerpts.",
        "",
        f"Overall readiness: `{readiness}`",
        "",
        "## Current Scope",
        "",
        f"- Records analyzed: {total}",
        f"- Parse errors: {parse_errors} ({pct(parse_errors, total):.1%})",
        f"- Weak heading records: {weak_headings} ({pct(weak_headings, total):.1%})",
        "",
        "## Family Coverage",
        "",
        "| Family | Current Records | Target Records | Gap |",
        "|---|---:|---:|---:|",
    ]
    for family_key, label in FAMILIES.items():
        current = type_counts.get(family_key, 0)
        gap = max(target_per_family - current, 0)
        lines.append(f"| {label} | {current} | {target_per_family} | {gap} |")

    lines.extend(
        [
            "",
            "## Gates",
            "",
            "| Gate | Status | Detail |",
            "|---|---|---|",
        ]
    )
    for gate in gates:
        status = "PASS" if gate.passed else "FAIL"
        lines.append(f"| {gate.name} | {status} | {gate.detail} |")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
        ]
    )
    if readiness == "balanced_large":
        lines.append(
            "The corpus is large and balanced enough to promote cross-family writing rules, subject to continued citation and public-safety checks."
        )
    elif readiness == "candidate_mechanical_only":
        lines.extend(
            [
                "The corpus can support cautious candidate rules for mechanical/manufacturing-style theses.",
                "It is not ready for broad claims about all Chinese engineering graduate theses because software/system and control/optimization coverage remains insufficient.",
            ]
        )
    else:
        lines.extend(
            [
                "The corpus is not ready to promote general thesis-writing rules.",
                "Use current outputs only as debugging signals or acquisition guidance until coverage and quality gates pass.",
            ]
        )

    lines.extend(
        [
            "",
            "## Next Actions",
            "",
            "- Prioritize the families with the largest coverage gaps in `acquisition_plan.md`.",
            "- Keep copyrighted source files under ignored private folders only.",
            "- Rerun `run_corpus_pipeline.py` after each legal acquisition batch.",
            "",
        ]
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Check whether aggregate corpus metadata is ready for broad claims.")
    parser.add_argument("--summary", type=Path, default=Path("public_stats/corpus/summary.json"))
    parser.add_argument("--output", type=Path, default=Path("public_stats/corpus/readiness_report.md"))
    parser.add_argument("--min-total-records", type=int, default=100)
    parser.add_argument("--target-per-family", type=int, default=100)
    parser.add_argument("--max-parse-error-rate", type=float, default=0.10)
    parser.add_argument("--max-weak-heading-rate", type=float, default=0.25)
    parser.add_argument("--strict", action="store_true", help="Exit 1 unless the corpus is balanced_large.")
    args = parser.parse_args()

    summary = read_summary(args.summary)
    type_counts = {key: int(value) for key, value in summary.get("type_counts", {}).items()}
    gates = build_gates(
        summary,
        args.min_total_records,
        args.target_per_family,
        args.max_parse_error_rate,
        args.max_weak_heading_rate,
    )
    readiness = classify_readiness(gates, int(summary.get("record_count", 0)), type_counts, args.target_per_family)
    write_report(args.output, summary, gates, readiness, args.target_per_family)

    print(f"readiness={readiness}")
    print(f"report={args.output}")
    if args.strict and readiness != "balanced_large":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
