#!/usr/bin/env python
"""Summarize a filled private acquisition batch tracker."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


TRUTHY = {"1", "true", "yes", "y", "checked", "done"}


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
    archive_status: str
    notes: str


def read_tracker(path: Path) -> list[TrackerRow]:
    rows: list[TrackerRow] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            rows.append(
                TrackerRow(
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
                    screening_action=row["screening_action"],
                    archive_status=row["archive_status"],
                    notes=row["notes"],
                )
            )
    return rows


def is_truthy(value: str) -> bool:
    return value.strip().lower() in TRUTHY


def norm(value: str) -> str:
    return value.strip().lower()


def summarize(rows: list[TrackerRow]) -> dict[str, object]:
    families = sorted({row.family for row in rows})
    per_family_archived: Counter[str] = Counter()
    per_family_slots: Counter[str] = Counter()
    by_query: dict[str, Counter[str]] = defaultdict(Counter)
    download_formats: Counter[str] = Counter()
    screening_actions: Counter[str] = Counter()
    archive_statuses: Counter[str] = Counter()

    detail_checked = 0
    abstract_checked = 0
    titled_rows = 0

    for row in rows:
        per_family_slots[row.family] += 1
        if row.title.strip():
            titled_rows += 1
        if is_truthy(row.detail_page_checked):
            detail_checked += 1
            by_query[row.query]["detail_page_checked"] += 1
        if is_truthy(row.abstract_checked):
            abstract_checked += 1
            by_query[row.query]["abstract_checked"] += 1
        if row.download_format.strip():
            download_formats[norm(row.download_format)] += 1
            by_query[row.query]["downloaded"] += 1
        if row.screening_action.strip():
            screening_actions[norm(row.screening_action)] += 1
            by_query[row.query][f"screen_{norm(row.screening_action)}"] += 1
        if row.archive_status.strip():
            archive_statuses[norm(row.archive_status)] += 1
            by_query[row.query][f"archive_{norm(row.archive_status)}"] += 1
        if norm(row.archive_status) == "archived":
            per_family_archived[row.family] += 1
            by_query[row.query]["archived"] += 1

    family_progress: list[dict[str, object]] = []
    for family in families:
        family_rows = [row for row in rows if row.family == family]
        if not family_rows:
            continue
        sample = family_rows[0]
        archived = per_family_archived[family]
        family_progress.append(
            {
                "family": family,
                "current_records": sample.current_records,
                "archived_this_batch": archived,
                "projected_records": sample.current_records + archived,
                "remaining_commonality_gap": max(sample.commonality_gap_records - archived, 0),
                "remaining_readiness_gap": max(sample.readiness_gap_records - archived, 0),
                "remaining_deep_gap": max(sample.deep_gap_records - archived, 0),
                "tracker_slots": per_family_slots[family],
            }
        )

    return {
        "tracker_rows": len(rows),
        "families": families,
        "titled_rows": titled_rows,
        "detail_checked": detail_checked,
        "abstract_checked": abstract_checked,
        "download_formats": dict(download_formats),
        "screening_actions": dict(screening_actions),
        "archive_statuses": dict(archive_statuses),
        "family_progress": family_progress,
        "query_progress": {query: dict(counter) for query, counter in sorted(by_query.items())},
    }


def write_markdown(path: Path, summary: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Batch Tracker Summary",
        "",
        "This is a private local summary generated from a filled acquisition batch tracker. Do not publish it if it contains real thesis titles or schools.",
        "",
        "## Overall Progress",
        "",
        f"- Tracker rows: {summary['tracker_rows']}",
        f"- Rows with a title filled in: {summary['titled_rows']}",
        f"- Detail pages checked: {summary['detail_checked']}",
        f"- Abstracts checked: {summary['abstract_checked']}",
        "",
        "## Family Progress",
        "",
        "| Family | Current | Archived This Batch | Projected Records | Remaining Commonality Gap | Remaining Readiness Gap | Remaining Deep Gap |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary["family_progress"]:
        lines.append(
            f"| {row['family']} | {row['current_records']} | {row['archived_this_batch']} | {row['projected_records']} | "
            f"{row['remaining_commonality_gap']} | {row['remaining_readiness_gap']} | {row['remaining_deep_gap']} |"
        )
    lines.extend(["", "## Query Progress", ""])
    query_progress = summary["query_progress"]
    if not query_progress:
        lines.append("- No query progress was recorded.")
    else:
        for query, counter in query_progress.items():
            lines.append(
                f"- {query}: detail {counter.get('detail_page_checked', 0)}, "
                f"abstract {counter.get('abstract_checked', 0)}, downloaded {counter.get('downloaded', 0)}, "
                f"archived {counter.get('archived', 0)}"
            )
    lines.extend(["", "## Counts By Action", ""])
    for label, counts in (
        ("Download Formats", summary["download_formats"]),
        ("Screening Actions", summary["screening_actions"]),
        ("Archive Statuses", summary["archive_statuses"]),
    ):
        lines.append("")
        lines.append(f"### {label}")
        if counts:
            for key, value in sorted(counts.items()):
                lines.append(f"- {key}: {value}")
        else:
            lines.append("- No entries recorded.")
    lines.extend(
        [
            "",
            "## Next Step",
            "",
            "- If `archived` rows are still 0, keep downloading inside the top-priority family before rerunning the corpus pipeline.",
            "- If `manual_review` is high, tighten the query or family filter before downloading more.",
            "- If many rows are `convert_to_pdf_first`, finish PDF conversion before extraction.",
            "- After archiving enough files for the current family, rerun `run_corpus_pipeline.py` and compare the new readiness gaps.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_csv(path: Path, summary: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    family_rows = summary["family_progress"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "family",
                "current_records",
                "archived_this_batch",
                "projected_records",
                "remaining_commonality_gap",
                "remaining_readiness_gap",
                "remaining_deep_gap",
                "tracker_slots",
            ],
        )
        writer.writeheader()
        for row in family_rows:
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize a filled private acquisition batch tracker.")
    parser.add_argument("tracker_csv", type=Path)
    parser.add_argument("--output-md", type=Path, default=Path("private_outputs/batch_tracker_summary.md"))
    parser.add_argument("--output-csv", type=Path, default=Path("private_outputs/batch_tracker_summary.csv"))
    args = parser.parse_args()

    summary = summarize(read_tracker(args.tracker_csv))
    write_markdown(args.output_md, summary)
    write_csv(args.output_csv, summary)
    print(f"tracker_rows={summary['tracker_rows']}")
    print(f"summary_md={args.output_md}")
    print(f"summary_csv={args.output_csv}")


if __name__ == "__main__":
    main()
