#!/usr/bin/env python
"""Generate candidate thesis-writing rules from aggregate corpus metadata."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_counter(path: Path, key_name: str, limit: int) -> list[tuple[str, int]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = []
        for row in csv.DictReader(handle):
            key = row.get(key_name, "")
            count = int(row.get("count", "0") or 0)
            if key:
                rows.append((key, count))
        return rows[:limit]


def read_rows(path: Path, limit: int) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))[:limit]


def read_pair_counter(path: Path, left_name: str, right_name: str, limit: int) -> list[tuple[str, str, int]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = []
        for row in csv.DictReader(handle):
            left = row.get(left_name, "")
            right = row.get(right_name, "")
            count = int(row.get("count", "0") or 0)
            if left and right:
                rows.append((left, right, count))
        return rows[:limit]


def evidence_level(record_count: int) -> str:
    if record_count < 6:
        return "debug_only"
    if record_count < 31:
        return "candidate"
    return "promotable_after_manual_review"


def write_rule_candidates(stats_dir: Path, output: Path) -> None:
    summary = read_json(stats_dir / "summary.json")
    record_count = int(summary.get("record_count", 0))
    parse_error_count = int(summary.get("parse_error_count", 0))
    level = evidence_level(record_count)
    headings = read_counter(stats_dir / "heading_patterns.csv", "heading_pattern", 12)
    keywords = read_counter(stats_dir / "keywords.csv", "keyword", 12)
    labels = read_counter(stats_dir / "figure_table_counts.csv", "label", 8)
    topic_tags = read_counter(stats_dir / "topic_tags.csv", "topic_tag", 10)
    topic_pairs = read_pair_counter(stats_dir / "topic_cooccurrence.csv", "topic_a", "topic_b", 10)
    roles = read_counter(stats_dir / "chapter_role_signals.csv", "role", 10)
    diagnostics = read_rows(stats_dir / "classification_diagnostics.csv", 12)

    lines = [
        "# Rule Candidates",
        "",
        "This file records candidate writing-rule observations derived from aggregate structural metadata. It does not contain original thesis text.",
        "",
        "## Evidence Gate",
        "",
        f"- Records analyzed: {record_count}",
        f"- Parse errors: {parse_error_count}",
        f"- Evidence level: `{level}`",
        "",
    ]

    if level == "debug_only":
        lines.extend(
            [
                "Current sample size is too small to promote any corpus observation into the skill as a general rule.",
                "Use the observations below only to check extraction quality and to guide the next acquisition batch.",
                "",
            ]
        )
    elif level == "candidate":
        lines.extend(
            [
                "Current sample size supports preliminary candidate patterns only.",
                "Before promotion, verify the pattern across multiple schools, topics, and thesis families.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "Current sample size may support rule promotion after manual review.",
                "Promote only abstract structure rules, evidence rules, or claim-boundary rules.",
                "",
            ]
        )

    lines.extend(["## Candidate Structural Signals", ""])
    lines.extend([f"- heading `{key}` appears {count} time(s)" for key, count in headings] or ["- No heading signals yet."])

    lines.extend(["", "## Candidate Keyword Signals", ""])
    lines.extend([f"- keyword `{key}` appears {count} time(s)" for key, count in keywords] or ["- No keyword signals yet."])

    lines.extend(["", "## Candidate Figure/Table Signals", ""])
    lines.extend([f"- label `{key}` appears {count} time(s)" for key, count in labels] or ["- No figure/table signals yet."])

    lines.extend(["", "## Candidate Topic Signals", ""])
    lines.extend([f"- topic `{key}` appears in {count} record(s)" for key, count in topic_tags] or ["- No topic signals yet."])

    lines.extend(["", "## Candidate Topic Co-Occurrence Signals", ""])
    lines.extend(
        [f"- topics `{left}` + `{right}` co-occur in {count} record(s)" for left, right, count in topic_pairs]
        or ["- No topic co-occurrence signals yet."]
    )

    lines.extend(["", "## Candidate Chapter Role Signals", ""])
    lines.extend([f"- role `{key}` appears in {count} record(s)" for key, count in roles] or ["- No chapter role signals yet."])

    lines.extend(["", "## Classification Diagnostics", ""])
    if diagnostics:
        for row in diagnostics:
            lines.append(
                "- "
                f"{row.get('inferred_type', 'unknown')} / {row.get('confidence', 'unknown')}: "
                f"{row.get('record_count', '0')} record(s), "
                f"{row.get('weak_heading_records', '0')} weak heading record(s)"
            )
    else:
        lines.append("- No classification diagnostics yet.")

    lines.extend(
        [
            "",
            "## Promotion Checklist",
            "",
            "- The observation appears in more than one thesis.",
            "- The observation appears outside a single school or narrow topic.",
            "- The observation can be expressed as a structure, evidence, or claim-boundary rule without source wording.",
            "- The rule does not imply unsupported results, deployment, novelty, or superiority.",
            "- The public-safety scan passes after any reference update.",
            "",
        ]
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate corpus-derived rule candidates.")
    parser.add_argument("--stats-dir", type=Path, default=Path("public_stats/corpus"))
    parser.add_argument("--output", type=Path, default=Path("public_stats/corpus/rule_candidates.md"))
    args = parser.parse_args()

    write_rule_candidates(args.stats_dir, args.output)
    print(f"rule_candidates={args.output}")


if __name__ == "__main__":
    main()
