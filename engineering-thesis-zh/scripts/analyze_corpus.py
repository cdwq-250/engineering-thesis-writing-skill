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
    "software_system": {
        "系统": 3,
        "平台": 3,
        "设计与实现": 3,
        "软件": 3,
        "Web": 3,
        "数据库": 2,
        "信息系统": 3,
        "微服务": 3,
        "模块": 1,
    },
    "control_optimization": {
        "控制": 2,
        "优化": 2,
        "调度": 3,
        "排程": 3,
        "算法": 3,
        "预测": 2,
        "模型": 2,
        "仿真": 2,
        "策略": 1,
        "强化学习": 3,
        "遗传算法": 3,
        "NSGA": 3,
    },
    "mechanical_manufacturing": {
        "机械": 3,
        "制造": 3,
        "装配": 3,
        "工艺": 2,
        "设备": 3,
        "维修": 3,
        "维护": 3,
        "运维": 3,
        "加工": 2,
        "智能制造": 3,
        "生产线": 3,
        "产线": 3,
        "车间": 3,
        "TPM": 3,
        "OEE": 3,
        "精益生产": 3,
        "质量管理": 2,
        "预防性维护": 3,
    },
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def type_scores(record: dict[str, Any]) -> dict[str, int]:
    haystack = " ".join(
        [record.get("file_name", "")]
        + record.get("title_candidates", [])
        + record.get("keyword_candidates", [])
        + record.get("headings", [])
    ).lower()
    return {
        thesis_type: sum(weight for keyword, weight in keywords.items() if keyword.lower() in haystack)
        for thesis_type, keywords in TYPE_KEYWORDS.items()
    }


def infer_type(record: dict[str, Any]) -> str:
    scores = type_scores(record)
    if not scores:
        return "unknown"
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    best, score = sorted_scores[0]
    if score == 0:
        return "unknown"
    if len(sorted_scores) > 1 and score == sorted_scores[1][1]:
        return "mixed"
    return best


def confidence_bucket(record: dict[str, Any]) -> str:
    scores = {
        thesis_type: score
        for thesis_type, score in type_scores(record).items()
        if score > 0
    }
    if not scores:
        return "unknown"
    sorted_scores = sorted(scores.values(), reverse=True)
    if len(sorted_scores) > 1 and sorted_scores[0] == sorted_scores[1]:
        return "tie"
    if sorted_scores[0] >= 6:
        return "high"
    if sorted_scores[0] >= 3:
        return "medium"
    return "low"


def chapter_prefix(heading: str) -> str:
    match = re.match(r"^(第[一二三四五六七八九十0-9]+章)", heading)
    if match:
        return match.group(1)
    match = re.match(r"^([0-9]+\.[0-9]+)", heading)
    if match:
        return match.group(1)
    return heading[:20]


def chapter_count(headings: list[str]) -> int:
    return sum(1 for heading in headings if re.match(r"^第[一二三四五六七八九十0-9]+章", heading))


def write_counter_csv(path: Path, counter: Counter[str], field_name: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([field_name, "count"])
        for key, count in counter.most_common():
            writer.writerow([key, count])


def write_classification_diagnostics(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "inferred_type",
            "confidence",
            "record_count",
            "weak_heading_records",
            "average_headings",
            "average_keywords",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
        for record in records:
            key = (infer_type(record), confidence_bucket(record))
            grouped.setdefault(key, []).append(record)
        for (inferred_type, confidence), group in sorted(grouped.items()):
            heading_counts = [len(record.get("headings", [])) for record in group]
            keyword_counts = [len(record.get("keyword_candidates", [])) for record in group]
            writer.writerow(
                {
                    "inferred_type": inferred_type,
                    "confidence": confidence,
                    "record_count": len(group),
                    "weak_heading_records": sum(count < 5 for count in heading_counts),
                    "average_headings": f"{sum(heading_counts) / len(heading_counts):.1f}",
                    "average_keywords": f"{sum(keyword_counts) / len(keyword_counts):.1f}",
                }
            )


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
        chapter_count_distribution[str(chapter_count(headings))] += 1
        heading_counts.update(chapter_prefix(heading) for heading in headings)
        keyword_counts.update(record.get("keyword_candidates", []))
        for title in record.get("figure_table_titles", []):
            figure_table_counts.update([title[:1]])

    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary = {
        "record_count": len(records),
        "parse_error_count": sum(1 for record in records if record.get("parse_error")),
        "type_counts": dict(type_counts),
        "classification_method": "weighted keywords over file name, title candidates, keywords, and headings",
        "classification_confidence_counts": dict(Counter(confidence_bucket(record) for record in records)),
        "weak_heading_record_count": sum(1 for record in records if len(record.get("headings", [])) < 5),
        "chapter_count_distribution": dict(chapter_count_distribution),
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_counter_csv(args.output_dir / "heading_patterns.csv", heading_counts, "heading_pattern")
    write_counter_csv(args.output_dir / "keywords.csv", keyword_counts, "keyword")
    write_counter_csv(args.output_dir / "figure_table_counts.csv", figure_table_counts, "label")
    write_classification_diagnostics(args.output_dir / "classification_diagnostics.csv", records)


if __name__ == "__main__":
    main()
