#!/usr/bin/env python
"""Write a public, aggregate progress report for the local thesis corpus."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv_rows(path: Path, limit: int = 10) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))[:limit]


def read_records(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def pct(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.0%"
    return f"{numerator / denominator * 100:.1f}%"


def bullet_counter(rows: list[dict[str, str]], key_name: str) -> list[str]:
    lines = []
    for row in rows:
        key = row.get(key_name, "")
        count = row.get("count", "")
        if key:
            lines.append(f"- {key}: {count}")
    return lines


def bullet_pair_counter(rows: list[dict[str, str]], left_name: str, right_name: str) -> list[str]:
    lines = []
    for row in rows:
        left = row.get(left_name, "")
        right = row.get(right_name, "")
        count = row.get("count", "")
        if left and right:
            lines.append(f"- {left} + {right}: {count}")
    return lines


def next_batch_advice(summary: dict[str, Any], target_per_family: int) -> list[str]:
    type_counts = summary.get("type_counts", {})
    advice = []
    labels = [
        ("software_system", "software"),
        ("control_optimization", "control/optimization"),
        ("mechanical_manufacturing", "mechanical/manufacturing"),
    ]
    for key, label in labels:
        current = int(type_counts.get(key, 0))
        remaining = max(target_per_family - current, 0)
        advice.append(f"- {label}: current {current}, next target +{min(remaining, 20)} files")
    return advice


def write_report(stats_dir: Path, records_path: Path, output: Path, target_per_family: int) -> None:
    summary = read_json(stats_dir / "summary.json")
    records = read_records(records_path)
    record_count = int(summary.get("record_count", 0))
    parse_errors = int(summary.get("parse_error_count", 0))
    heading_rows = read_csv_rows(stats_dir / "heading_patterns.csv")
    keyword_rows = read_csv_rows(stats_dir / "keywords.csv")
    figure_rows = read_csv_rows(stats_dir / "figure_table_counts.csv")
    topic_rows = read_csv_rows(stats_dir / "topic_tags.csv")
    topic_pair_rows = read_csv_rows(stats_dir / "topic_cooccurrence.csv")
    role_rows = read_csv_rows(stats_dir / "chapter_role_signals.csv")

    heading_counts = [len(record.get("headings", [])) for record in records]
    keyword_counts = [len(record.get("keyword_candidates", [])) for record in records]
    figure_counts = [len(record.get("figure_table_titles", [])) for record in records]

    avg_headings = sum(heading_counts) / len(heading_counts) if heading_counts else 0
    avg_keywords = sum(keyword_counts) / len(keyword_counts) if keyword_counts else 0
    avg_figures = sum(figure_counts) / len(figure_counts) if figure_counts else 0

    lines = [
        "# Corpus Progress Report",
        "",
        "This report is generated from local structural metadata. It intentionally excludes original theses, full text extracts, and long verbatim passages.",
        "",
        "## Current Coverage",
        "",
        f"- Records analyzed: {record_count}",
        f"- Parse errors: {parse_errors} ({pct(parse_errors, record_count)})",
        f"- Average extracted headings per record: {avg_headings:.1f}",
        f"- Average extracted keywords per record: {avg_keywords:.1f}",
        f"- Average extracted figure/table labels per record: {avg_figures:.1f}",
        f"- Weak heading records: {summary.get('weak_heading_record_count', 0)}",
        f"- Classification method: {summary.get('classification_method', 'not recorded')}",
        "",
        "## Type Distribution",
        "",
    ]
    for key, value in summary.get("type_counts", {}).items():
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## Classification Confidence", ""])
    confidence_counts = summary.get("classification_confidence_counts", {})
    if confidence_counts:
        for key, value in confidence_counts.items():
            lines.append(f"- {key}: {value}")
    else:
        lines.append("- No confidence data yet.")

    lines.extend(["", "## Common Heading Patterns", ""])
    lines.extend(bullet_counter(heading_rows, "heading_pattern") or ["- No heading data yet."])

    lines.extend(["", "## Common Keyword Candidates", ""])
    lines.extend(bullet_counter(keyword_rows, "keyword") or ["- No keyword data yet."])

    lines.extend(["", "## Figure/Table Label Counts", ""])
    lines.extend(bullet_counter(figure_rows, "label") or ["- No figure/table data yet."])

    lines.extend(["", "## Topic Tags", ""])
    lines.extend(bullet_counter(topic_rows, "topic_tag") or ["- No topic tag data yet."])

    lines.extend(["", "## Topic Co-Occurrence", ""])
    lines.extend(bullet_pair_counter(topic_pair_rows, "topic_a", "topic_b") or ["- No topic co-occurrence data yet."])

    lines.extend(["", "## Chapter Role Signals", ""])
    lines.extend(bullet_counter(role_rows, "role") or ["- No chapter role data yet."])

    lines.extend(
        [
            "",
            "## Interpretation Guardrails",
            "",
            "- Treat current commonalities as preliminary until each target family has a larger sample.",
            "- Do not infer writing rules from one or two theses; use early records mainly to validate extraction quality.",
            "- Promote a pattern into the skill only after it appears across multiple schools, topics, and thesis families.",
            "",
            "## Next Acquisition Batch",
            "",
        ]
    )
    lines.extend(next_batch_advice(summary, target_per_family))
    lines.extend(
        [
            "",
            "Recommended immediate action: download another 10-20 legally accessible PDF theses from CNKI or Wanfang, then run `archive_downloads.py` and `run_corpus_pipeline.py`.",
            "",
        ]
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a public corpus progress report.")
    parser.add_argument("--stats-dir", type=Path, default=Path("public_stats/corpus"))
    parser.add_argument("--records", type=Path, default=Path("private_extracts/records.jsonl"))
    parser.add_argument("--output", type=Path, default=Path("public_stats/corpus/progress_report.md"))
    parser.add_argument("--target-per-family", type=int, default=300)
    args = parser.parse_args()

    write_report(args.stats_dir, args.records, args.output, args.target_per_family)
    print(f"report={args.output}")


if __name__ == "__main__":
    main()
