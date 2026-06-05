#!/usr/bin/env python
"""Sync screening results into a private acquisition batch tracker."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass, fields
from pathlib import Path


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


@dataclass
class ScreenRow:
    file_name: str
    suffix: str
    size_bytes: int
    duplicate_in_corpus: bool
    inferred_type: str
    confidence: str
    priority_rank: int
    recommended_action: str
    recommended_destination: str
    reason: str


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
                    screening_action=row.get("screening_action", ""),
                    recommended_destination=row.get("recommended_destination", ""),
                    screening_reason=row.get("screening_reason", ""),
                    archive_status=row.get("archive_status", ""),
                    notes=row.get("notes", ""),
                )
            )
    return rows


def read_screening(path: Path) -> dict[str, ScreenRow]:
    rows: dict[str, ScreenRow] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            screen = ScreenRow(
                file_name=row["file_name"],
                suffix=row["suffix"],
                size_bytes=int(row["size_bytes"]),
                duplicate_in_corpus=str(row["duplicate_in_corpus"]).strip().lower() == "true",
                inferred_type=row["inferred_type"],
                confidence=row["confidence"],
                priority_rank=int(row["priority_rank"]),
                recommended_action=row["recommended_action"],
                recommended_destination=row["recommended_destination"],
                reason=row["reason"],
            )
            rows[screen.file_name] = screen
    return rows


def sync_rows(tracker_rows: list[TrackerRow], screening_rows: dict[str, ScreenRow]) -> tuple[list[TrackerRow], dict[str, int]]:
    counts = {"matched": 0, "unmatched_tracker_rows": 0, "duplicate_updates": 0, "archive_candidate_updates": 0}
    updated: list[TrackerRow] = []
    for row in tracker_rows:
        file_name = row.local_file_name.strip()
        if not file_name or file_name not in screening_rows:
            counts["unmatched_tracker_rows"] += 1
            updated.append(row)
            continue
        screen = screening_rows[file_name]
        row.screening_action = screen.recommended_action
        row.recommended_destination = screen.recommended_destination
        row.screening_reason = screen.reason
        if not row.archive_status.strip():
            if screen.recommended_action == "skip_duplicate":
                row.archive_status = "duplicate"
                counts["duplicate_updates"] += 1
            elif screen.recommended_action == "archive_candidate":
                counts["archive_candidate_updates"] += 1
        counts["matched"] += 1
        updated.append(row)
    return updated, counts


def write_tracker(path: Path, rows: list[TrackerRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=[field.name for field in fields(TrackerRow)])
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def write_report(path: Path, counts: dict[str, int], updated_rows: list[TrackerRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    actionable = sum(1 for row in updated_rows if row.screening_action == "archive_candidate")
    duplicates = sum(1 for row in updated_rows if row.screening_action == "skip_duplicate")
    manual = sum(1 for row in updated_rows if row.screening_action == "manual_review")
    lines = [
        "# Tracker Sync Report",
        "",
        "This is a private local report describing how screening results were synced into the acquisition batch tracker.",
        "",
        "## Summary",
        "",
        f"- Matched tracker rows: {counts['matched']}",
        f"- Unmatched tracker rows: {counts['unmatched_tracker_rows']}",
        f"- Rows marked duplicate during sync: {counts['duplicate_updates']}",
        f"- Rows updated to archive candidate with empty archive status: {counts['archive_candidate_updates']}",
        "",
        "## Resulting Screening Mix",
        "",
        f"- archive_candidate: {actionable}",
        f"- manual_review: {manual}",
        f"- skip_duplicate: {duplicates}",
        "",
        "## Next Step",
        "",
        "- Review rows with `archive_candidate` and archive them into the intended private family folder.",
        "- Keep `manual_review` rows in the tracker until the thesis title/abstract is checked again.",
        "- Rerun the batch summary after archive statuses are filled.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync screening results into a private acquisition batch tracker.")
    parser.add_argument("tracker_csv", type=Path)
    parser.add_argument("screening_csv", type=Path)
    parser.add_argument("--output-csv", type=Path, default=None)
    parser.add_argument("--output-md", type=Path, default=Path("private_outputs/tracker_sync_report.md"))
    args = parser.parse_args()

    tracker_rows = read_tracker(args.tracker_csv)
    screening_rows = read_screening(args.screening_csv)
    updated_rows, counts = sync_rows(tracker_rows, screening_rows)
    output_csv = args.output_csv or args.tracker_csv
    write_tracker(output_csv, updated_rows)
    write_report(args.output_md, counts, updated_rows)
    print(f"matched={counts['matched']}")
    print(f"tracker_csv={output_csv}")
    print(f"sync_report={args.output_md}")


if __name__ == "__main__":
    main()
