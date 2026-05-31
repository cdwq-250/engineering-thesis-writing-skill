#!/usr/bin/env python
"""Aggregate structural thesis-corpus metadata without publishing full text."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


TYPE_KEYWORDS = {
    "software_system": ["系统", "平台", "管理", "设计与实现", "软件", "Web", "数据库"],
    "control_optimization": ["控制", "优化", "调度", "算法", "预测", "模型", "仿真"],
    "mechanical_manufacturing": ["机械", "制造", "装配", "工艺", "设备", "加工", "智能制造"],
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def infer_type(record: dict[str, Any]) -> str:
    haystack = " ".join(record.get("title_candidates", []) + record.get("keyword_candidates", []) + record.get("headings", []))
    scores = {
        thesis_type: sum(1 for keyword in keywords if keyword.lower() in haystack.lower())
        for thesis_type, keywords in TYPE_KEYWORDS.items()
    }
    best, score = max(scores.items(), key=lambda item: item[1])
    return best if score > 0 else "unknown"


def chapter_prefix(heading: str) -> str:
    match = re.match(r"^(第[一二三四五六七八九十0-9]+章)", heading)
    if match:
        return match.group(1)
    match = re.match(r"^([0-9]+\.[0-9]+)", heading)
    if match:
        return match.group(1)
    return heading[:20]


def write_counter_csv(path: Path, counter: Counter[str], field_name: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([field_name, "count"])
        for key, count in counter.most_common():
            writer.writerow([key, count])


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze thesis structural metadata.")
    parser.add_argument("jsonl", type=Path, help="JSONL produced by extract_outline.py")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for aggregate statistics")
    args = parser.parse_args()

    records = read_jsonl(args.jsonl)
    type_counts: Counter[str] = Counter()
    heading_counts: Counter[str] = Counter()
    keyword_counts: Counter[str] = Counter()
    figure_table_counts: Counter[str] = Counter()
    chapter_count_distribution: Counter[str] = Counter()

    for record in records:
        type_counts[infer_type(record)] += 1
        headings = record.get("headings", [])
        chapter_count_distribution[str(sum(1 for h in headings if h.startswith("第") and "章" in h))] += 1
        heading_counts.update(chapter_prefix(h) for h in headings)
        keyword_counts.update(record.get("keyword_candidates", []))
        for title in record.get("figure_table_titles", []):
            figure_table_counts.update([title[:1]])

    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "record_count": len(records),
        "parse_error_count": sum(1 for r in records if r.get("parse_error")),
        "type_counts": dict(type_counts),
        "chapter_count_distribution": dict(chapter_count_distribution),
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_counter_csv(args.output_dir / "heading_patterns.csv", heading_counts, "heading_pattern")
    write_counter_csv(args.output_dir / "keywords.csv", keyword_counts, "keyword")
    write_counter_csv(args.output_dir / "figure_table_counts.csv", figure_table_counts, "label")


if __name__ == "__main__":
    main()

