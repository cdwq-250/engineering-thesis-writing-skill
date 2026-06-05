#!/usr/bin/env python
"""Generate a private acquisition batch tracker from the public acquisition plan."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PlanRow:
    priority: int
    family: str
    current_records: int
    commonality_target_records: int
    commonality_gap_records: int
    readiness_target_records: int
    readiness_gap_records: int
    target_records: int
    gap_records: int
    batch_target: int
    estimated_batches_to_readiness: int
    estimated_batches_to_deep_target: int
    query: str
    database: str
    destination_folder: str
    priority_reason: str
    acceptance_filter: str
    stop_condition: str
    notes: str


@dataclass
class TrackerRow:
    slot: int
    family: str
    milestone_focus: str
    query: str
    source_database: str
    current_records: int
    commonality_gap_records: int
    readiness_gap_records: int
    deep_gap_records: int
    title: str
    school: str
    year: str
    detail_page_checked: str
    abstract_checked: str
    download_format: str
    local_file_name: str
    screening_action: str
    recommended_destination: str
    screening_reason: str
    archive_status: str
    notes: str


def read_plan(path: Path) -> list[PlanRow]:
    rows: list[PlanRow] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            rows.append(
                PlanRow(
                    priority=int(row["priority"]),
                    family=row["family"],
                    current_records=int(row["current_records"]),
                    commonality_target_records=int(row["commonality_target_records"]),
                    commonality_gap_records=int(row["commonality_gap_records"]),
                    readiness_target_records=int(row["readiness_target_records"]),
                    readiness_gap_records=int(row["readiness_gap_records"]),
                    target_records=int(row["target_records"]),
                    gap_records=int(row["gap_records"]),
                    batch_target=int(row["batch_target"]),
                    estimated_batches_to_readiness=int(row["estimated_batches_to_readiness"]),
                    estimated_batches_to_deep_target=int(row["estimated_batches_to_deep_target"]),
                    query=row["query"],
                    database=row["database"],
                    destination_folder=row["destination_folder"],
                    priority_reason=row["priority_reason"],
                    acceptance_filter=row["acceptance_filter"],
                    stop_condition=row["stop_condition"],
                    notes=row["notes"],
                )
            )
    return rows


def milestone_focus(plan: PlanRow) -> str:
    if plan.commonality_gap_records > 0:
        return f"reach_commonality_{plan.commonality_target_records}"
    if plan.readiness_gap_records > 0:
        return f"reach_readiness_{plan.readiness_target_records}"
    return f"extend_deep_target_{plan.target_records}"


def build_tracker_rows(plan_rows: list[PlanRow], family: str | None, slots_per_query: int) -> list[TrackerRow]:
    filtered = [row for row in plan_rows if family is None or row.family == family]
    tracker_rows: list[TrackerRow] = []
    slot = 1
    for row in filtered:
        planned_slots = min(slots_per_query, row.batch_target)
        for _ in range(planned_slots):
            tracker_rows.append(
                TrackerRow(
                    slot=slot,
                    family=row.family,
                    milestone_focus=milestone_focus(row),
                    query=row.query,
                    source_database=row.database,
                    current_records=row.current_records,
                    commonality_gap_records=row.commonality_gap_records,
                    readiness_gap_records=row.readiness_gap_records,
                    deep_gap_records=row.gap_records,
                    title="",
                    school="",
                    year="",
                    detail_page_checked="",
                    abstract_checked="",
                    download_format="",
                    local_file_name="",
                    screening_action="",
                    recommended_destination="",
                    screening_reason="",
                    archive_status="",
                    notes="",
                )
            )
            slot += 1
    return tracker_rows


def write_csv(path: Path, rows: list[TrackerRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(TrackerRow.__dataclass_fields__.keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def write_markdown(path: Path, rows: list[TrackerRow], plan_rows: list[PlanRow], family: str | None, slots_per_query: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    filtered = [row for row in plan_rows if family is None or row.family == family]
    lines = [
        "# Acquisition Batch Tracker",
        "",
        "This is a private local worksheet for tracking thesis downloads during one manual acquisition batch. Do not publish it if it contains real thesis titles or schools.",
        "",
        f"- Family filter: {family or 'all'}",
        f"- Queries included: {len(filtered)}",
        f"- Slots per query: {slots_per_query}",
        f"- Total tracker rows: {len(rows)}",
        "",
        "## Batch Focus",
        "",
    ]
    if not filtered:
        lines.append("- No matching plan rows were found.")
    else:
        for row in filtered:
            lines.append(
                f"- {row.family} / {row.query}: current {row.current_records}, "
                f"commonality gap {row.commonality_gap_records}, readiness gap {row.readiness_gap_records}, deep gap {row.gap_records}, "
                f"batch target {row.batch_target}"
            )
    lines.extend(
        [
            "",
            "## Data Entry Rules",
            "",
            "- Fill `detail_page_checked=yes` only after opening the thesis detail page.",
            "- Fill `abstract_checked=yes` only after confirming the abstract matches the intended family filter.",
            "- Use `download_format` such as `pdf`, `caj`, `kdh`, or `nh`.",
            "- Use `screening_action` such as `archive_candidate`, `manual_review`, or `skip_duplicate` after running `screen_downloads.py`.",
            "- `recommended_destination` and `screening_reason` can be filled automatically from the screening CSV.",
            "- Use `archive_status` such as `archived`, `duplicate`, `rejected`, or `convert_to_pdf_first`.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a private worksheet for one manual thesis acquisition batch.")
    parser.add_argument("--plan-csv", type=Path, default=Path("public_stats/corpus/acquisition_plan.csv"))
    parser.add_argument("--family", choices=["software", "control/optimization", "mechanical/manufacturing"], default=None)
    parser.add_argument("--slots-per-query", type=int, default=8)
    parser.add_argument("--output-csv", type=Path, default=Path("private_outputs/acquisition_batch_tracker.csv"))
    parser.add_argument("--output-md", type=Path, default=Path("private_outputs/acquisition_batch_tracker.md"))
    args = parser.parse_args()

    plan_rows = read_plan(args.plan_csv)
    tracker_rows = build_tracker_rows(plan_rows, args.family, args.slots_per_query)
    write_csv(args.output_csv, tracker_rows)
    write_markdown(args.output_md, tracker_rows, plan_rows, args.family, args.slots_per_query)
    print(f"tracker_rows={len(tracker_rows)}")
    print(f"tracker_csv={args.output_csv}")
    print(f"tracker_md={args.output_md}")


if __name__ == "__main__":
    main()
