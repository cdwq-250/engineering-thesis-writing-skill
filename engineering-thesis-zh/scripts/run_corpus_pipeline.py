#!/usr/bin/env python
"""Run the local thesis-corpus pipeline end to end."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def run(command: list[str]) -> None:
    print("+ " + " ".join(command))
    subprocess.run(command, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run manifest, extraction, quality check, and aggregate analysis.")
    parser.add_argument("--corpus-root", type=Path, default=Path("private_corpus"))
    parser.add_argument("--private-dir", type=Path, default=Path("private_extracts"))
    parser.add_argument("--public-dir", type=Path, default=Path("public_stats/corpus"))
    parser.add_argument("--min-headings", type=int, default=5)
    parser.add_argument("--max-pages", type=int, default=40)
    parser.add_argument("--allow-empty", action="store_true", help="Allow an empty corpus for smoke testing.")
    args = parser.parse_args()

    corpus_root = args.corpus_root
    private_dir = args.private_dir
    public_dir = args.public_dir
    manifest = private_dir / "manifest.csv"
    records = private_dir / "records.jsonl"

    pdfs = list(corpus_root.rglob("*.pdf")) if corpus_root.exists() else []
    if not pdfs and not args.allow_empty:
        raise SystemExit(
            f"No PDF files found under {corpus_root}. Add legally obtained PDFs or pass --allow-empty for a smoke test."
        )

    run([sys.executable, str(SCRIPT_DIR / "build_manifest.py"), str(corpus_root), "--output", str(manifest)])

    if pdfs:
        run(
            [
                sys.executable,
                str(SCRIPT_DIR / "extract_outline.py"),
                str(corpus_root),
                "--output",
                str(records),
                "--max-pages",
                str(args.max_pages),
            ]
        )
        run(
            [
                sys.executable,
                str(SCRIPT_DIR / "quality_check.py"),
                str(records),
                "--min-headings",
                str(args.min_headings),
            ]
        )
        run([sys.executable, str(SCRIPT_DIR / "analyze_corpus.py"), str(records), "--output-dir", str(public_dir)])
        run(
            [
                sys.executable,
                str(SCRIPT_DIR / "write_corpus_report.py"),
                "--stats-dir",
                str(public_dir),
                "--records",
                str(records),
                "--output",
                str(public_dir / "progress_report.md"),
            ]
        )
        run(
            [
                sys.executable,
                str(SCRIPT_DIR / "write_acquisition_plan.py"),
                "--summary",
                str(public_dir / "summary.json"),
                "--output-md",
                str(public_dir / "acquisition_plan.md"),
                "--output-csv",
                str(public_dir / "acquisition_plan.csv"),
            ]
        )
        run(
            [
                sys.executable,
                str(SCRIPT_DIR / "write_rule_candidates.py"),
                "--stats-dir",
                str(public_dir),
                "--output",
                str(public_dir / "rule_candidates.md"),
            ]
        )
    else:
        print("No PDFs found; manifest smoke test completed.")


if __name__ == "__main__":
    main()
