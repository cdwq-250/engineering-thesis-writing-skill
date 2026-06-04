#!/usr/bin/env python
"""Aggregate structural thesis-corpus metadata without publishing full text."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from itertools import combinations
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

TOPIC_TAGS = {
    "lean_production": ["精益生产", "价值流", "8S", "5M1E", "PDCA", "现场管理", "浪费"],
    "equipment_maintenance": ["设备", "维修", "维护", "运维", "点检", "TPM", "OEE", "预防性维护", "预测性维护"],
    "quality_management": ["质量", "缺陷", "全面质量管理", "质量控制", "质量管理体系", "客户满意度"],
    "production_scheduling": ["调度", "排程", "车间", "生产线", "产线", "装配", "流水车间", "作业车间"],
    "algorithm_modeling": ["算法", "模型", "仿真", "优化", "遗传算法", "强化学习", "深度学习", "图神经网络"],
    "software_platform": ["系统", "平台", "微服务", "数据库", "Web", "模块", "接口"],
}

CHAPTER_ROLE_KEYWORDS = {
    "background_significance": ["研究背景", "研究意义", "选题背景", "背景与意义"],
    "literature_review": ["国内外研究现状", "文献综述", "研究现状", "相关研究"],
    "research_content_route": ["研究内容", "研究方法", "技术路线", "章节安排"],
    "current_state_diagnosis": ["现状", "问题", "调查", "诊断", "短板", "瓶颈"],
    "cause_analysis": ["原因分析", "成因", "影响因素", "5M1E", "鱼骨"],
    "model_design": ["模型", "建模", "指标体系", "目标函数", "约束"],
    "scheme_design": ["方案", "策略", "流程优化", "设计", "改进"],
    "system_implementation": ["系统实现", "原型系统", "模块", "平台", "架构"],
    "experiment_evaluation": ["实验", "仿真", "测试", "验证", "评价", "性能"],
    "result_discussion": ["结果分析", "对比", "敏感性", "应用效果", "实施效果"],
    "summary_outlook": ["总结", "展望", "结论"],
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


def searchable_text(record: dict[str, Any]) -> str:
    return " ".join(
        [record.get("file_name", "")]
        + record.get("title_candidates", [])
        + record.get("keyword_candidates", [])
        + record.get("headings", [])
    ).lower()


def matched_tags(record: dict[str, Any], tag_keywords: dict[str, list[str]]) -> set[str]:
    haystack = searchable_text(record)
    return {
        tag
        for tag, keywords in tag_keywords.items()
        if any(keyword.lower() in haystack for keyword in keywords)
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


def write_pair_counter_csv(path: Path, counter: Counter[tuple[str, str]], left_name: str, right_name: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow([left_name, right_name, "count"])
        for (left, right), count in counter.most_common():
            writer.writerow([left, right, count])


def write_role_signal_csv(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    role_counts: Counter[str] = Counter()
    role_type_counts: Counter[tuple[str, str]] = Counter()
    for record in records:
        roles = matched_tags(record, CHAPTER_ROLE_KEYWORDS)
        inferred = infer_type(record)
        role_counts.update(roles)
        role_type_counts.update((inferred, role) for role in roles)

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["role", "count"])
        for role, count in role_counts.most_common():
            writer.writerow([role, count])

    write_pair_counter_csv(path.with_name("chapter_role_by_type.csv"), role_type_counts, "inferred_type", "role")


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
    topic_counts: Counter[str] = Counter()
    topic_pair_counts: Counter[tuple[str, str]] = Counter()

    for record in records:
        type_counts[infer_type(record)] += 1
        topics = sorted(matched_tags(record, TOPIC_TAGS))
        topic_counts.update(topics)
        topic_pair_counts.update(combinations(topics, 2))
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
    write_counter_csv(args.output_dir / "topic_tags.csv", topic_counts, "topic_tag")
    write_pair_counter_csv(args.output_dir / "topic_cooccurrence.csv", topic_pair_counts, "topic_a", "topic_b")
    write_role_signal_csv(args.output_dir / "chapter_role_signals.csv", records)
    write_classification_diagnostics(args.output_dir / "classification_diagnostics.csv", records)


if __name__ == "__main__":
    main()
