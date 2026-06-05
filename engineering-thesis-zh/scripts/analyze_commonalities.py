#!/usr/bin/env python
"""Compute cross-record commonality signals from private thesis metadata."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from analyze_corpus import CHAPTER_ROLE_KEYWORDS, TOPIC_TAGS, infer_type, matched_tags


MAIN_FAMILIES = {
    "software_system": "software/system",
    "control_optimization": "control/optimization",
    "mechanical_manufacturing": "mechanical/manufacturing",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def rate(count: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return count / total


def signal_interpretation(signal_type: str, support_by_family: dict[str, int], family_totals: Counter[str]) -> str:
    supported_families = [family for family in MAIN_FAMILIES if support_by_family.get(family, 0) > 0]
    mechanical = support_by_family.get("mechanical_manufacturing", 0)
    if len(supported_families) >= 2:
        return "cross_family_candidate"
    if mechanical >= 3 and mechanical == max(support_by_family.values() or [0]):
        return "mechanical_weighted_candidate"
    if signal_type == "role" and support_by_family:
        return "structure_signal_needs_more_families"
    return "insufficient_support"


def collect_signal_rows(records: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], Counter[str]]:
    family_totals: Counter[str] = Counter(infer_type(record) for record in records)
    signal_support: dict[tuple[str, str], set[int]] = defaultdict(set)
    family_support: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)

    for index, record in enumerate(records):
        family = infer_type(record)
        signals = {
            ("topic", tag) for tag in matched_tags(record, TOPIC_TAGS)
        } | {
            ("role", role) for role in matched_tags(record, CHAPTER_ROLE_KEYWORDS)
        }
        for signal in signals:
            signal_support[signal].add(index)
            family_support[signal][family] += 1

    rows: list[dict[str, Any]] = []
    total_records = len(records)
    for (signal_type, signal), indexes in sorted(
        signal_support.items(),
        key=lambda item: (-len(item[1]), item[0][0], item[0][1]),
    ):
        support = len(indexes)
        support_by_family = family_support[(signal_type, signal)]
        row: dict[str, Any] = {
            "signal_type": signal_type,
            "signal": signal,
            "total_records": total_records,
            "total_support": support,
            "total_rate": f"{rate(support, total_records):.3f}",
            "support_family_count": sum(1 for family in MAIN_FAMILIES if support_by_family.get(family, 0) > 0),
            "interpretation": signal_interpretation(signal_type, support_by_family, family_totals),
        }
        for family in MAIN_FAMILIES:
            count = support_by_family.get(family, 0)
            row[f"{family}_support"] = count
            row[f"{family}_rate"] = f"{rate(count, family_totals.get(family, 0)):.3f}"
        rows.append(row)
    return rows, family_totals


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "signal_type",
        "signal",
        "total_records",
        "total_support",
        "total_rate",
        "support_family_count",
        "software_system_support",
        "software_system_rate",
        "control_optimization_support",
        "control_optimization_rate",
        "mechanical_manufacturing_support",
        "mechanical_manufacturing_rate",
        "interpretation",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def format_row(row: dict[str, Any]) -> str:
    return (
        f"- `{row['signal_type']}:{row['signal']}` appears in {row['total_support']}/{row['total_records']} records "
        f"(software {row['software_system_support']}, control {row['control_optimization_support']}, "
        f"mechanical {row['mechanical_manufacturing_support']}); interpretation: `{row['interpretation']}`"
    )


def write_markdown(path: Path, rows: list[dict[str, Any]], family_totals: Counter[str], min_support: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    cross = [
        row
        for row in rows
        if row["total_support"] >= min_support and row["interpretation"] == "cross_family_candidate"
    ][:12]
    mechanical = [
        row
        for row in rows
        if row["total_support"] >= min_support and row["interpretation"] == "mechanical_weighted_candidate"
    ][:12]
    weak = [row for row in rows if row["total_support"] < min_support][:8]

    lines = [
        "# Common Patterns Report",
        "",
        "This report is generated from aggregate metadata only. It does not publish thesis files, full text, or long source excerpts.",
        "",
        "## Evidence Boundary",
        "",
        f"- Total records: {sum(family_totals.values())}",
        f"- Software/system records: {family_totals.get('software_system', 0)}",
        f"- Control/optimization records: {family_totals.get('control_optimization', 0)}",
        f"- Mechanical/manufacturing records: {family_totals.get('mechanical_manufacturing', 0)}",
        f"- Mixed/unknown records: {family_totals.get('mixed', 0) + family_totals.get('unknown', 0)}",
        "",
        "Current cross-family patterns are candidates only when they appear across at least two main thesis families. Mechanical-weighted patterns must not be generalized to all engineering theses.",
        "",
        "## Cross-Family Candidate Patterns",
        "",
    ]
    lines.extend([format_row(row) for row in cross] or ["- No cross-family candidate patterns meet the current support gate."])
    lines.extend(["", "## Mechanical-Weighted Candidate Patterns", ""])
    lines.extend([format_row(row) for row in mechanical] or ["- No mechanical-weighted candidate patterns meet the current support gate."])
    lines.extend(["", "## Low-Support Signals", ""])
    lines.extend([format_row(row) for row in weak] or ["- No low-support signals were emitted."])
    lines.extend(
        [
            "",
            "## Use In Writing",
            "",
            "- Use cross-family candidate patterns as cautious structure prompts, not final claims.",
            "- Use mechanical-weighted patterns only for mechanical/manufacturing thesis planning.",
            "- Require project evidence before writing any claim about effectiveness, superiority, deployment, or novelty.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate aggregate commonality reports from thesis metadata records.")
    parser.add_argument("records", type=Path, help="Private records.jsonl produced by extract_outline.py")
    parser.add_argument("--output-md", type=Path, default=Path("public_stats/corpus/common_patterns.md"))
    parser.add_argument("--output-csv", type=Path, default=Path("public_stats/corpus/commonality_matrix.csv"))
    parser.add_argument("--min-support", type=int, default=3)
    args = parser.parse_args()

    rows, family_totals = collect_signal_rows(read_jsonl(args.records))
    write_csv(args.output_csv, rows)
    write_markdown(args.output_md, rows, family_totals, args.min_support)
    print(f"common_patterns={args.output_md}")
    print(f"commonality_matrix={args.output_csv}")


if __name__ == "__main__":
    main()
