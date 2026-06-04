#!/usr/bin/env python
"""Audit a generated thesis manuscript for unsupported strong claims."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


STRONG_CLAIM_WORDS = ["显著", "工业级", "国内领先", "全面解决", "最优", "投入运行", "实际应用证明"]


def display(value: object) -> str:
    """Return ASCII-safe text for CI consoles with non-UTF-8 encodings."""
    return str(value).encode("ascii", errors="backslashreplace").decode("ascii")


@dataclass
class EvidenceRow:
    claim: str
    source: str
    evidence_type: str
    wording: str


def split_markdown_row(line: str) -> list[str]:
    return [part.strip() for part in line.strip().strip("|").split("|")]


def parse_evidence_register(text: str) -> list[EvidenceRow]:
    rows: list[EvidenceRow] = []
    in_table = False
    for line in text.splitlines():
        if line.strip().startswith("| Claim | Source | Type |"):
            in_table = True
            continue
        if not in_table:
            continue
        if not line.strip().startswith("|"):
            if rows:
                break
            continue
        if re.match(r"^\|\s*-+", line):
            continue
        parts = split_markdown_row(line)
        if len(parts) < 4:
            continue
        rows.append(EvidenceRow(parts[0], parts[1], parts[2], parts[3]))
    return rows


def strong_claim_lines(text: str) -> list[tuple[int, str, str]]:
    result = []
    for line_number, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("|"):
            continue
        for word in STRONG_CLAIM_WORDS:
            if word in line:
                result.append((line_number, word, line.strip()))
                break
    return result


def has_support(line: str, rows: list[EvidenceRow]) -> bool:
    for row in rows:
        if not row.source or row.source == "待补充":
            continue
        if row.claim and row.claim in line:
            return True
        if row.wording and row.wording in line:
            return True
    return False


def audit(text: str) -> tuple[list[str], list[str]]:
    rows = parse_evidence_register(text)
    errors: list[str] = []
    warnings: list[str] = []
    if not rows:
        warnings.append("Evidence Register not found or empty.")
    for line_number, word, line in strong_claim_lines(text):
        if not has_support(line, rows):
            errors.append(f"line {line_number}: strong claim `{word}` lacks matching Evidence Register support: {line}")
    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit a thesis manuscript Markdown file for unsupported strong claims.")
    parser.add_argument("manuscript", type=Path)
    args = parser.parse_args()

    text = args.manuscript.read_text(encoding="utf-8")
    errors, warnings = audit(text)
    for warning in warnings:
        print(f"warning:{display(warning)}")
    for error in errors:
        print(f"error:{display(error)}")
    if errors:
        raise SystemExit(1)
    print("claim_audit_passed=true")


if __name__ == "__main__":
    main()
