#!/usr/bin/env python
"""Generate the next legal thesis-corpus acquisition plan."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


FAMILIES = {
    "software_system": {
        "label": "software",
        "folder": "private_corpus/software",
        "queries": [
            "系统设计与实现",
            "管理系统 设计与实现",
            "信息系统 软件工程",
            "Web系统 设计",
            "数据库设计 管理平台",
            "平台设计与实现",
        ],
        "acceptance_filter": "Title should describe a software/system/platform design and implementation thesis.",
    },
    "control_optimization": {
        "label": "control/optimization",
        "folder": "private_corpus/control",
        "queries": [
            "生产调度 优化",
            "维护策略 优化",
            "离散事件仿真 调度",
            "多目标优化 生产系统",
            "预测控制 设备维护",
            "强化学习 调度",
        ],
        "acceptance_filter": "Title should center on optimization, scheduling, control, simulation, or algorithmic decision models.",
    },
    "mechanical_manufacturing": {
        "label": "mechanical/manufacturing",
        "folder": "private_corpus/mechanical",
        "queries": [
            "智能制造 装配生产线",
            "设备维护 健康管理",
            "工艺优化 制造",
            "数字孪生 车间调度",
            "装配线 平衡优化",
            "设备故障 预测维护",
        ],
        "acceptance_filter": "Title should be mechanical, manufacturing, workshop, equipment, maintenance, process, or production-line focused.",
    },
}


@dataclass
class PlanRow:
    priority: int
    family: str
    current_records: int
    target_records: int
    gap_records: int
    batch_target: int
    query: str
    database: str
    destination_folder: str
    priority_reason: str
    acceptance_filter: str
    stop_condition: str
    notes: str


def read_summary(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_plan(summary: dict[str, Any], target_per_family: int, batch_size: int) -> list[PlanRow]:
    type_counts = summary.get("type_counts", {})
    rows: list[PlanRow] = []
    priority = 1
    sorted_families = sorted(FAMILIES.items(), key=lambda item: int(type_counts.get(item[0], 0)))
    for family_key, spec in sorted_families:
        current = int(type_counts.get(family_key, 0))
        remaining = max(target_per_family - current, 0)
        batch_target = min(batch_size, remaining)
        if batch_target <= 0:
            continue
        reason = (
            f"Gap {remaining} records to target {target_per_family}; "
            "prioritized because readiness and commonality gates need balanced family coverage."
        )
        stop_condition = (
            f"Stop this batch after {batch_target} accepted PDFs or when search results no longer match the family filter."
        )
        for query in spec["queries"][:3]:
            rows.append(
                PlanRow(
                    priority=priority,
                    family=spec["label"],
                    current_records=current,
                    target_records=target_per_family,
                    gap_records=remaining,
                    batch_target=batch_target,
                    query=query,
                    database="CNKI/Wanfang school-library access",
                    destination_folder=spec["folder"],
                    priority_reason=reason,
                    acceptance_filter=spec["acceptance_filter"],
                    stop_condition=stop_condition,
                    notes="Prefer PDF; use CAJ/KDH/NH only when PDF is unavailable and convert to PDF before extraction.",
                )
            )
            priority += 1
    return rows


def write_csv(path: Path, rows: list[PlanRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(PlanRow.__dataclass_fields__.keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def write_markdown(path: Path, rows: list[PlanRow], summary: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Acquisition Plan",
        "",
        "This plan is generated from aggregate corpus counts. It does not include source documents or full text.",
        "",
        "## Current Counts",
        "",
    ]
    for family_key, spec in FAMILIES.items():
        lines.append(f"- {spec['label']}: {summary.get('type_counts', {}).get(family_key, 0)}")

    lines.extend(
        [
            "",
            "## Batch Policy",
            "",
            "- Fill the lowest-count family first; do not add more mechanical/manufacturing papers until software and control/optimization coverage improve.",
            "- Accept a paper only when the title and abstract match the family filter; skip irrelevant business-only or management-only papers.",
            "- After each batch, run the corpus pipeline and read `readiness_report.md` plus `common_patterns.md` before deciding the next batch.",
            "",
            "## Next Search Tasks",
            "",
            "| Priority | Family | Gap | Batch Target | Query | Destination |",
            "|---:|---|---:|---:|---|---|",
        ]
    )
    for row in rows:
        lines.append(
            f"| {row.priority} | {row.family} | {row.gap_records} | {row.batch_target} | {row.query} | `{row.destination_folder}` |"
        )

    lines.extend(["", "## Acceptance Filters", ""])
    seen_filters: set[tuple[str, str]] = set()
    for row in rows:
        key = (row.family, row.acceptance_filter)
        if key in seen_filters:
            continue
        seen_filters.add(key)
        lines.append(f"- {row.family}: {row.acceptance_filter}")

    lines.extend(
        [
            "",
            "## Execution Notes",
            "",
            "- Search in CNKI or Wanfang through authorized school-library access.",
            "- Enter a thesis detail page and prefer `PDF下载` when available.",
            "- After downloading, run the archiver in dry-run mode first.",
            "- Archive only files that match the intended thesis batch; keep unrelated local files out of `private_corpus`.",
            "- For the current corpus, prioritize `private_corpus/software` and `private_corpus/control` before adding more mechanical/manufacturing papers.",
            "",
            "Recommended archiver command:",
            "",
            "```powershell",
            'python engineering-thesis-zh\\scripts\\archive_downloads.py --dry-run --pdf-only --since-days 7 --include "系统|设计|实现|平台|调度|优化|控制|算法|仿真|模型"',
            "```",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the next thesis acquisition plan.")
    parser.add_argument("--summary", type=Path, default=Path("public_stats/corpus/summary.json"))
    parser.add_argument("--output-md", type=Path, default=Path("public_stats/corpus/acquisition_plan.md"))
    parser.add_argument("--output-csv", type=Path, default=Path("public_stats/corpus/acquisition_plan.csv"))
    parser.add_argument("--target-per-family", type=int, default=300)
    parser.add_argument("--batch-size", type=int, default=20)
    args = parser.parse_args()

    summary = read_summary(args.summary)
    rows = build_plan(summary, args.target_per_family, args.batch_size)
    write_markdown(args.output_md, rows, summary)
    write_csv(args.output_csv, rows)
    print(f"plan_md={args.output_md}")
    print(f"plan_csv={args.output_csv}")


if __name__ == "__main__":
    main()
