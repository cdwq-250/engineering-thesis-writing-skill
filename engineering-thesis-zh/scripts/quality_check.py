#!/usr/bin/env python
"""Check structural metadata quality before corpus analysis."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    records = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSON at line {line_number}: {exc}") from exc
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Quality-check thesis metadata JSONL.")
    parser.add_argument("jsonl", type=Path)
    parser.add_argument("--min-headings", type=int, default=5)
    parser.add_argument("--max-error-rate", type=float, default=0.10)
    args = parser.parse_args()

    records = read_jsonl(args.jsonl)
    if not records:
        raise SystemExit("No records found.")

    paths = [record.get("path", "") for record in records]
    duplicate_paths = [path for path, count in Counter(paths).items() if count > 1]
    parse_errors = [record for record in records if record.get("parse_error")]
    weak_records = [record for record in records if len(record.get("headings", [])) < args.min_headings]

    error_rate = len(parse_errors) / len(records)
    print(f"records={len(records)}")
    print(f"parse_errors={len(parse_errors)}")
    print(f"parse_error_rate={error_rate:.3f}")
    print(f"weak_heading_records={len(weak_records)}")
    print(f"duplicate_paths={len(duplicate_paths)}")

    if duplicate_paths:
        raise SystemExit(f"Duplicate paths found: {duplicate_paths[:5]}")
    if error_rate > args.max_error_rate:
        raise SystemExit(f"Parse error rate {error_rate:.3f} exceeds {args.max_error_rate:.3f}")


if __name__ == "__main__":
    main()

