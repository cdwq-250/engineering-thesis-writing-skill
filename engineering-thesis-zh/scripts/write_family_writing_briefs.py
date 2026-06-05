#!/usr/bin/env python
"""Generate per-family writing briefs from aggregate corpus outputs."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


FAMILIES = {
    "software_system": "software/system",
    "control_optimization": "control/optimization",
    "mechanical_manufacturing": "mechanical/manufacturing",
}


def read_summary(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def top_roles(rows: list[dict[str, str]], family_key: str, limit: int = 6) -> list[dict[str, str]]:
    filtered = [row for row in rows if row["inferred_type"] == family_key]
    return sorted(filtered, key=lambda row: (-int(row["count"]), row["role"]))[:limit]


def top_family_signals(rows: list[dict[str, str]], family_key: str, limit: int = 6) -> list[dict[str, str]]:
    support_key = f"{family_key}_support"
    rate_key = f"{family_key}_rate"
    filtered = [row for row in rows if int(row.get(support_key, "0")) > 0]
    return sorted(
        filtered,
        key=lambda row: (-int(row[support_key]), -float(row[rate_key]), row["signal_type"], row["signal"]),
    )[:limit]


def evidence_label(count: int) -> str:
    if count >= 10:
        return "candidate"
    if count >= 5:
        return "weak_signal"
    return "very_sparse"


def write_markdown(
    output: Path,
    summary: dict[str, Any],
    role_rows: list[dict[str, str]],
    signal_rows: list[dict[str, str]],
) -> None:
    type_counts = summary.get("type_counts", {})
    lines = [
        "# Family Writing Briefs",
        "",
        "This report is generated from aggregate metadata only. It summarizes family-level writing tendencies without publishing thesis files, full text, or long source excerpts.",
        "",
    ]
    for family_key, label in FAMILIES.items():
        current = int(type_counts.get(family_key, 0))
        lines.extend(
            [
                f"## {label}",
                "",
                f"- Records in corpus: {current}",
                f"- Evidence level: `{evidence_label(current)}`",
                "",
                "### Frequent Chapter Roles",
                "",
            ]
        )
        family_roles = top_roles(role_rows, family_key)
        if family_roles:
            for row in family_roles:
                lines.append(f"- `{row['role']}`: {row['count']} records")
        else:
            lines.append("- No role signal is available yet.")
        lines.extend(["", "### Frequent Structure And Topic Signals", ""])
        family_signals = top_family_signals(signal_rows, family_key)
        if family_signals:
            for row in family_signals:
                support = row[f"{family_key}_support"]
                rate = row[f"{family_key}_rate"]
                lines.append(
                    f"- `{row['signal_type']}:{row['signal']}`: support {support}, family rate {rate}, interpretation `{row['interpretation']}`"
                )
        else:
            lines.append("- No family-specific commonality signal is available yet.")
        lines.extend(
            [
                "",
                "### Use In Writing",
                "",
            ]
        )
        if current >= 10:
            lines.extend(
                [
                    "- Use these signals as candidate structural prompts when drafting a thesis in this family.",
                    "- Keep every technical claim tied to project evidence, not corpus frequency alone.",
                ]
            )
        elif current >= 5:
            lines.extend(
                [
                    "- Treat these patterns as weak prompts only; verify against the concrete project before using them.",
                    "- Download more theses from this family before promoting any stronger family-specific writing rule.",
                ]
            )
        else:
            lines.extend(
                [
                    "- Evidence is too sparse for reliable family-specific writing guidance.",
                    "- Prioritize new acquisition in this family before using the observed patterns as writing rules.",
                ]
            )
        lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_csv(output: Path, summary: dict[str, Any], role_rows: list[dict[str, str]], signal_rows: list[dict[str, str]]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "family",
        "records_in_corpus",
        "evidence_level",
        "top_roles",
        "top_signals",
    ]
    type_counts = summary.get("type_counts", {})
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for family_key, label in FAMILIES.items():
            current = int(type_counts.get(family_key, 0))
            writer.writerow(
                {
                    "family": label,
                    "records_in_corpus": current,
                    "evidence_level": evidence_label(current),
                    "top_roles": "; ".join(f"{row['role']}:{row['count']}" for row in top_roles(role_rows, family_key)),
                    "top_signals": "; ".join(
                        f"{row['signal_type']}:{row['signal']}:{row[f'{family_key}_support']}"
                        for row in top_family_signals(signal_rows, family_key)
                    ),
                }
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate per-family writing briefs from aggregate corpus outputs.")
    parser.add_argument("--summary", type=Path, default=Path("public_stats/corpus/summary.json"))
    parser.add_argument("--role-csv", type=Path, default=Path("public_stats/corpus/chapter_role_by_type.csv"))
    parser.add_argument("--commonality-csv", type=Path, default=Path("public_stats/corpus/commonality_matrix.csv"))
    parser.add_argument("--output-md", type=Path, default=Path("public_stats/corpus/family_writing_briefs.md"))
    parser.add_argument("--output-csv", type=Path, default=Path("public_stats/corpus/family_writing_briefs.csv"))
    args = parser.parse_args()

    summary = read_summary(args.summary)
    role_rows = read_csv(args.role_csv)
    signal_rows = read_csv(args.commonality_csv)
    write_markdown(args.output_md, summary, role_rows, signal_rows)
    write_csv(args.output_csv, summary, role_rows, signal_rows)
    print(f"family_briefs_md={args.output_md}")
    print(f"family_briefs_csv={args.output_csv}")


if __name__ == "__main__":
    main()
