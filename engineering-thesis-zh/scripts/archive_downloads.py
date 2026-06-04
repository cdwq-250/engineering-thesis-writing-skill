#!/usr/bin/env python
"""Archive newly downloaded thesis files into the private corpus.

This script copies files only. It does not delete or move anything from the
browser download directory.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path


SUPPORTED_SUFFIXES = {".pdf", ".caj", ".kdh", ".nh", ".doc", ".docx"}
PARTIAL_SUFFIXES = {".crdownload", ".tmp", ".download"}


@dataclass
class ArchiveResult:
    copied: int = 0
    duplicate: int = 0
    skipped: int = 0


def display(value: object) -> str:
    """Return ASCII-safe text for CI consoles with non-UTF-8 encodings."""
    return str(value).encode("ascii", errors="backslashreplace").decode("ascii")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_candidate_files(source: Path) -> list[Path]:
    return sorted(
        (
            path
            for path in source.iterdir()
            if path.is_file()
            and path.suffix.lower() in SUPPORTED_SUFFIXES
            and not any(path.name.lower().endswith(suffix) for suffix in PARTIAL_SUFFIXES)
        ),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )


def matches_filters(
    path: Path,
    include: list[re.Pattern[str]],
    exclude: list[re.Pattern[str]],
    since: datetime | None,
    pdf_only: bool,
) -> tuple[bool, str]:
    name = path.name
    if pdf_only and path.suffix.lower() != ".pdf":
        return False, "not_pdf"
    if since is not None and datetime.fromtimestamp(path.stat().st_mtime) < since:
        return False, "older_than_since"
    if include and not any(pattern.search(name) for pattern in include):
        return False, "include_filter"
    if exclude and any(pattern.search(name) for pattern in exclude):
        return False, "exclude_filter"
    return True, ""


def existing_hashes(destination: Path) -> set[str]:
    hashes: set[str] = set()
    if not destination.exists():
        return hashes
    for path in destination.rglob("*"):
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
            hashes.add(sha256(path))
    return hashes


def unique_destination(destination: Path, file_name: str) -> Path:
    target = destination / file_name
    if not target.exists():
        return target
    stem = target.stem
    suffix = target.suffix
    for index in range(1, 10_000):
        candidate = destination / f"{stem}-{index}{suffix}"
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Could not find a unique destination for {file_name}")


def compile_patterns(patterns: list[str]) -> list[re.Pattern[str]]:
    return [re.compile(pattern, re.I) for pattern in patterns]


def archive_downloads(
    source: Path,
    destination: Path,
    limit: int | None,
    dry_run: bool,
    include: list[str] | None = None,
    exclude: list[str] | None = None,
    since_days: int | None = None,
    pdf_only: bool = False,
) -> ArchiveResult:
    if not source.exists():
        raise FileNotFoundError(f"Download directory does not exist: {source}")

    destination.mkdir(parents=True, exist_ok=True)
    seen_hashes = existing_hashes(destination)
    result = ArchiveResult()
    copied_this_run = 0
    include_patterns = compile_patterns(include or [])
    exclude_patterns = compile_patterns(exclude or [])
    since = datetime.now() - timedelta(days=since_days) if since_days is not None else None

    for path in iter_candidate_files(source):
        if limit is not None and copied_this_run >= limit:
            break
        matched, reason = matches_filters(path, include_patterns, exclude_patterns, since, pdf_only)
        if not matched:
            result.skipped += 1
            print(f"skip:{reason}\t{display(path.name)}")
            continue
        file_hash = sha256(path)
        if file_hash in seen_hashes:
            result.duplicate += 1
            print(f"duplicate\t{display(path.name)}")
            continue
        target = unique_destination(destination, path.name)
        print(f"{'would_copy' if dry_run else 'copy'}\t{display(path)}\t->\t{display(target)}")
        if not dry_run:
            shutil.copy2(path, target)
            seen_hashes.add(file_hash)
        result.copied += 1
        copied_this_run += 1

    return result


def default_downloads_dir() -> Path:
    home = Path.home()
    return home / "Downloads"


def main() -> None:
    parser = argparse.ArgumentParser(description="Copy downloaded thesis files into a private corpus folder.")
    parser.add_argument("--source", type=Path, default=default_downloads_dir(), help="Browser download directory")
    parser.add_argument(
        "--destination",
        type=Path,
        default=Path("private_corpus/cnki_manual"),
        help="Private corpus destination directory",
    )
    parser.add_argument("--limit", type=int, default=None, help="Maximum number of new files to copy")
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        help="Case-insensitive regex that the file name must match; repeat for OR matching",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Case-insensitive regex for file names to skip; repeat for OR matching",
    )
    parser.add_argument(
        "--since-days",
        type=int,
        default=7,
        help="Only consider files modified in the last N days; pass -1 to disable",
    )
    parser.add_argument("--pdf-only", action="store_true", help="Only archive PDF files")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be copied without writing files")
    args = parser.parse_args()

    since_days = None if args.since_days < 0 else args.since_days
    result = archive_downloads(
        args.source.resolve(),
        args.destination.resolve(),
        args.limit,
        args.dry_run,
        include=args.include,
        exclude=args.exclude,
        since_days=since_days,
        pdf_only=args.pdf_only,
    )
    print(f"copied={result.copied}")
    print(f"duplicates={result.duplicate}")
    print(f"skipped={result.skipped}")


if __name__ == "__main__":
    main()
