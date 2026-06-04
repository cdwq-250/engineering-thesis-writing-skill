#!/usr/bin/env python
"""Build a private corpus manifest from local thesis files."""

from __future__ import annotations

import argparse
import csv
from datetime import date
from pathlib import Path


DIRECT_EXTRACTION_SUFFIXES = {".pdf"}
CONVERSION_REQUIRED_SUFFIXES = {".caj", ".kdh", ".nh", ".doc", ".docx"}
SUPPORTED_SUFFIXES = DIRECT_EXTRACTION_SUFFIXES | CONVERSION_REQUIRED_SUFFIXES
FAMILY_NAMES = {"software", "control", "mechanical"}


def infer_family(path: Path) -> str:
    parts = {part.lower() for part in path.parts}
    for family in FAMILY_NAMES:
        if family in parts:
            return family
    return "unknown"


def iter_files(root: Path) -> list[Path]:
    return sorted(
        path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    )


def conversion_status(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in DIRECT_EXTRACTION_SUFFIXES:
        return "ready_for_extraction"
    if suffix in {".caj", ".kdh", ".nh"}:
        return "convert_to_pdf_first"
    return "convert_or_export_to_pdf_first"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a private thesis-corpus manifest CSV.")
    parser.add_argument("corpus_root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    root = args.corpus_root.resolve()
    files = iter_files(root)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    fields = [
        "local_path",
        "file_name",
        "file_format",
        "thesis_family",
        "title",
        "year",
        "school",
        "degree_level",
        "discipline",
        "keywords",
        "source_database",
        "download_date",
        "conversion_status",
        "ocr_required",
        "notes",
    ]

    with args.output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for path in files:
            rel = path.relative_to(root)
            writer.writerow(
                {
                    "local_path": str(rel),
                    "file_name": path.name,
                    "file_format": path.suffix.lower().lstrip("."),
                    "thesis_family": infer_family(rel),
                    "title": "",
                    "year": "",
                    "school": "",
                    "degree_level": "",
                    "discipline": "",
                    "keywords": "",
                    "source_database": "",
                    "download_date": date.today().isoformat(),
                    "conversion_status": conversion_status(path),
                    "ocr_required": "",
                    "notes": "",
                }
            )

    print(f"files={len(files)}")
    print(f"manifest={args.output}")


if __name__ == "__main__":
    main()
