#!/usr/bin/env python
"""Aggregate multiple private batch tracker CSV files into a progress dashboard."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


TRUTHY = {"1", "true", "yes", "y", "checked", "done"}


@dataclass
class TrackerRow:
    batch_file: str
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


def is_truthy(value: str) -> bool:
    return value.strip().lower() in TRUTHY


def norm(value: str) -> str:
    return value.strip().lower()


def read_tracker(path: Path) -> list[TrackerRow]:
    rows: list[TrackerRow] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            rows.append(
                TrackerRow(
                    batch_file=path.name,
                    slot=int(row["slot"]),
                    family=row["family"],
                    milestone_focus=row["milestone_focus"],
                    query=row["query"],
                    source_database=row["source_database"],
                    current_records=int(row["current_records"]),
                    commonality_gap_records=int(row["commonality_gap_records"]),
                    readiness_gap_records=int(row["readiness_gap_records"]),
                    deep_gap_records=int(row["deep_gap_records"]),
                    title=row["title"],
                    school=row["school"],
                    year=row["year"],
                    detail_page_checked=row["detail_page_checked"],
                    abstract_checked=row["abstract_checked"],
                    download_format=row["download_format"],
                    local_file_name=row["local_file_name"],
                    screening_action=row.get("screening_action", ""),
                    recommended_destination=row.get("recommended_destination", ""),
                    screening_reason=row.get("screening_reason", ""),
                    archive_status=row.get("archive_status", ""),
                    notes=row.get("notes", ""),
                )
            )
    return rows


def find_tracker_files(root: Path, pattern: str) -> list[Path]:
    return sorted(path for path in root.rglob(pattern) if path.is_file())


def aggregate(rows: list[TrackerRow]) -> dict[str, object]:
    total_batches = len({row.batch_file for row in rows})
    total_rows = len(rows)
    family_stats: dict[str, Counter[str]] = defaultdict(Counter)
    query_stats: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    screening_actions: Counter[str] = Counter()
    archive_statuses: Counter[str] = Counter()

    for row in rows:
        family = row.family
        query_key = (row.family, row.query)
        family_stats[family]["slots"] += 1
        query_stats[query_key]["slots"] += 1
        if row.title.strip():
            family_stats[family]["titles"] += 1
            query_stats[query_key]["titles"] += 1
        if is_truthy(row.detail_page_checked):
            family_stats[family]["detail_checked"] += 1
            query_stats[query_key]["detail_checked"] += 1
        if is_truthy(row.abstract_checked):
            family_stats[family]["abstract_checked"] += 1
            query_stats[query_key]["abstract_checked"] += 1
        if row.download_format.strip():
            family_stats[family]["downloaded"] += 1
            query_stats[query_key]["downloaded"] += 1
        if norm(row.archive_status) == "archived":
            family_stats[family]["archived"] += 1
            query_stats[query_key]["archived"] += 1
        if row.screening_action.strip():
            screening_actions[norm(row.screening_action)] += 1
            query_stats[query_key][f"screen_{norm(row.screening_action)}"] += 1
        if row.archive_status.strip():
            archive_statuses[norm(row.archive_status)] += 1
            query_stats[query_key][f"archive_{norm(row.archive_status)}"] += 1

    family_progress = []
    for family, counter in sorted(family_stats.items()):
        slots = counter.get("slots", 0)
        archived = counter.get("archived", 0)
        family_progress.append(
            {
                "family": family,
                "slots": slots,
                "detail_checked": counter.get("detail_checked", 0),
                "abstract_checked": counter.get("abstract_checked", 0),
                "downloaded": counter.get("downloaded", 0),
                "archived": archived,
                "archive_yield": f"{(archived / slots):.3f}" if slots else "0.000",
            }
        )

    query_progress = []
    for (family, query), counter in sorted(query_stats.items(), key=lambda item: (-item[1].get("archived", 0), item[0][0], item[0][1])):
        slots = counter.get("slots", 0)
        archived = counter.get("archived", 0)
        query_progress.append(
            {
                "family": family,
                "query": query,
                "slots": slots,
                "detail_checked": counter.get("detail_checked", 0),
                "abstract_checked": counter.get("abstract_checked", 0),
                "downloaded": counter.get("downloaded", 0),
                "archived": archived,
                "archive_yield": f"{(archived / slots):.3f}" if slots else "0.000",
                "manual_review": counter.get("screen_manual_review", 0),
                "duplicates": counter.get("archive_duplicate", 0),
            }
        )

    return {
        "batches": total_batches,
        "rows": total_rows,
        "family_progress": family_progress,
        "query_progress": query_progress,
        "screening_actions": dict(screening_actions),
        "archive_statuses": dict(archive_statuses),
    }


def write_markdown(path: Path, summary: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Batch Tracker Aggregate Dashboard",
        "",
        "This is a private local dashboard aggregated from multiple acquisition batch trackers. Do not publish it if it contains real thesis titles or schools.",
        "",
        "## Scope",
        "",
        f"- Batch tracker files: {summary['batches']}",
        f"- Total tracker rows: {summary['rows']}",
        "",
        "## Family Yield",
        "",
        "| Family | Slots | Detail Checked | Abstract Checked | Downloaded | Archived | Archive Yield |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary["family_progress"]:
        lines.append(
            f"| {row['family']} | {row['slots']} | {row['detail_checked']} | {row['abstract_checked']} | "
            f"{row['downloaded']} | {row['archived']} | {row['archive_yield']} |"
        )
    lines.extend(["", "## Query Yield", ""])
    for row in summary["query_progress"]:
        lines.append(
            f"- {row['family']} / {row['query']}: archived {row['archived']}/{row['slots']} "
            f"(yield {row['archive_yield']}), manual_review {row['manual_review']}, duplicates {row['duplicates']}"
        )
    lines.extend(["", "## Next Step", ""])
    if summary["query_progress"]:
        top = summary["query_progress"][0]
        lines.append(
            f"- Highest-yield query so far: `{top['family']} / {top['query']}` with archive yield `{top['archive_yield']}`."
        )
    lines.extend(
        [
            "- Keep expanding queries whose archived yield stays high after abstract checking.",
            "- Replace or tighten queries that produce many `manual_review` rows or duplicates.",
            "- Use this dashboard together with the public acquisition plan before the next manual batch.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()) if rows else ["family", "query"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate multiple private batch tracker CSV files into a dashboard.")
    parser.add_argument("--root", type=Path, default=Path("private_outputs"))
    parser.add_argument("--pattern", default="*batch_tracker.csv")
    parser.add_argument("--output-md", type=Path, default=Path("private_outputs/batch_tracker_dashboard.md"))
    parser.add_argument("--output-csv", type=Path, default=Path("private_outputs/batch_tracker_dashboard.csv"))
    args = parser.parse_args()

    tracker_files = find_tracker_files(args.root, args.pattern)
    rows: list[TrackerRow] = []
    for path in tracker_files:
        rows.extend(read_tracker(path))
    summary = aggregate(rows)
    write_markdown(args.output_md, summary)
    write_csv(args.output_csv, summary["query_progress"])
    print(f"tracker_files={len(tracker_files)}")
    print(f"tracker_rows={len(rows)}")
    print(f"dashboard_md={args.output_md}")
    print(f"dashboard_csv={args.output_csv}")


if __name__ == "__main__":
    main()
