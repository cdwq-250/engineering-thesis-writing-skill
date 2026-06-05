#!/usr/bin/env python
"""Screen downloaded thesis files before archiving them into the private corpus."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from analyze_corpus import confidence_bucket, infer_type, type_scores
from archive_downloads import SUPPORTED_SUFFIXES, existing_hashes, sha256


FAMILY_DESTINATIONS = {
    "software_system": "private_corpus/software",
    "control_optimization": "private_corpus/control",
    "mechanical_manufacturing": "private_corpus/mechanical",
}


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


def read_summary(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def family_priority(summary: dict[str, Any]) -> dict[str, int]:
    type_counts = summary.get("type_counts", {})
    families = sorted(FAMILY_DESTINATIONS, key=lambda family: int(type_counts.get(family, 0)))
    return {family: index + 1 for index, family in enumerate(families)}


def candidate_files(source: Path, pdf_only: bool) -> list[Path]:
    suffixes = {".pdf"} if pdf_only else SUPPORTED_SUFFIXES
    if not source.exists():
        return []
    return sorted(
        [path for path in source.iterdir() if path.is_file() and path.suffix.lower() in suffixes],
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )


def classify_name(path: Path) -> tuple[str, str, dict[str, int]]:
    record = {"file_name": path.name, "title_candidates": [], "keyword_candidates": [], "headings": []}
    return infer_type(record), confidence_bucket(record), type_scores(record)


def recommend_action(
    path: Path,
    duplicate: bool,
    inferred_type: str,
    confidence: str,
    priorities: dict[str, int],
) -> tuple[str, str, int, str]:
    rank = priorities.get(inferred_type, 999)
    if duplicate:
        return "skip_duplicate", "", rank, "File hash already exists in the private corpus."
    if inferred_type not in FAMILY_DESTINATIONS:
        return "manual_review", "", rank, "Filename does not match a tracked thesis family with enough confidence."
    if confidence in {"high", "medium"}:
        return (
            "archive_candidate",
            FAMILY_DESTINATIONS[inferred_type],
            rank,
            f"Filename matches {inferred_type}; family priority rank is {rank}.",
        )
    return (
        "manual_review",
        FAMILY_DESTINATIONS[inferred_type],
        rank,
        f"Filename weakly matches {inferred_type}; inspect title/abstract before archiving.",
    )


def screen_downloads(source: Path, corpus_root: Path, summary: dict[str, Any], pdf_only: bool) -> list[ScreenRow]:
    corpus_hashes = existing_hashes(corpus_root)
    priorities = family_priority(summary)
    rows: list[ScreenRow] = []
    for path in candidate_files(source, pdf_only):
        duplicate = sha256(path) in corpus_hashes
        inferred_type, confidence, _scores = classify_name(path)
        action, destination, rank, reason = recommend_action(path, duplicate, inferred_type, confidence, priorities)
        rows.append(
            ScreenRow(
                file_name=path.name,
                suffix=path.suffix.lower(),
                size_bytes=path.stat().st_size,
                duplicate_in_corpus=duplicate,
                inferred_type=inferred_type,
                confidence=confidence,
                priority_rank=rank,
                recommended_action=action,
                recommended_destination=destination,
                reason=reason,
            )
        )
    return rows


def write_csv(path: Path, rows: list[ScreenRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(ScreenRow.__dataclass_fields__.keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def write_markdown(path: Path, rows: list[ScreenRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row.recommended_action] = counts.get(row.recommended_action, 0) + 1
    lines = [
        "# Download Screening Report",
        "",
        "This is a private local report for screening downloaded thesis files before archiving. Do not publish it if it contains real thesis file names.",
        "",
        "## Summary",
        "",
    ]
    for action, count in sorted(counts.items()):
        lines.append(f"- {action}: {count}")
    if not rows:
        lines.append("- No supported downloaded files found.")
    lines.extend(
        [
            "",
            "## Recommended Actions",
            "",
            "| File | Action | Inferred Type | Confidence | Destination | Reason |",
            "|---|---|---|---|---|---|",
        ]
    )
    for row in rows:
        lines.append(
            f"| {row.file_name} | {row.recommended_action} | {row.inferred_type} | {row.confidence} | `{row.recommended_destination}` | {row.reason} |"
        )
    lines.extend(
        [
            "",
            "## Next Step",
            "",
            "- Archive only `archive_candidate` rows after checking the thesis detail page title and abstract.",
            "- Keep `manual_review` rows out of the corpus until the family is clear.",
            "- Ignore `skip_duplicate` rows unless the existing corpus copy is corrupted.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Screen downloaded thesis files before archiving.")
    parser.add_argument("--source", type=Path, default=Path("downloads"))
    parser.add_argument("--corpus-root", type=Path, default=Path("private_corpus"))
    parser.add_argument("--summary", type=Path, default=Path("public_stats/corpus/summary.json"))
    parser.add_argument("--output-csv", type=Path, default=Path("private_outputs/download_screening.csv"))
    parser.add_argument("--output-md", type=Path, default=Path("private_outputs/download_screening.md"))
    parser.add_argument("--pdf-only", action="store_true", help="Only screen PDFs.")
    args = parser.parse_args()

    rows = screen_downloads(args.source, args.corpus_root, read_summary(args.summary), args.pdf_only)
    write_csv(args.output_csv, rows)
    write_markdown(args.output_md, rows)
    print(f"screened={len(rows)}")
    print(f"screening_csv={args.output_csv}")
    print(f"screening_md={args.output_md}")


if __name__ == "__main__":
    main()
