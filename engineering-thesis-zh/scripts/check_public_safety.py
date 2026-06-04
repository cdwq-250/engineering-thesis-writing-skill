#!/usr/bin/env python
"""Scan the public repository for private thesis-corpus artifacts."""

from __future__ import annotations

import argparse
from pathlib import Path


BANNED_SUFFIXES = {".pdf", ".doc", ".docx", ".caj", ".kdh", ".nh"}
BANNED_DIRS = {"private_corpus", "private_extracts", "downloads"}
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".tmp_test"}
SUSPICIOUS_PATTERNS = [
    "本文共分为",
    "学位论文原创性声明",
    "分类号",
    "密级",
    "指导教师",
]
TEXT_SUFFIXES = {".md", ".txt", ".json", ".jsonl", ".csv", ".yaml", ".yml", ".py"}


def should_skip(rel_path: Path) -> bool:
    return any(part in SKIP_DIRS for part in rel_path.parts)


def main() -> None:
    parser = argparse.ArgumentParser(description="Check that public repo has no private thesis files.")
    parser.add_argument("root", type=Path, nargs="?", default=Path("."))
    args = parser.parse_args()

    root = args.root.resolve()
    violations: list[str] = []

    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if should_skip(rel):
            continue
        if path.is_dir():
            continue
        if any(part in BANNED_DIRS for part in rel.parts):
            continue
        if path.suffix.lower() in BANNED_SUFFIXES:
            violations.append(f"banned document file: {rel}")
            continue
        if path.name == "check_public_safety.py":
            continue
        if path.suffix.lower() in TEXT_SUFFIXES:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for pattern in SUSPICIOUS_PATTERNS:
                if pattern in text and "examples" not in rel.parts:
                    violations.append(f"suspicious thesis text pattern '{pattern}' in {rel}")
                    break

    if violations:
        print("Public safety check failed:")
        for violation in violations:
            print(f"- {violation}")
        raise SystemExit(1)
    print("Public safety check passed.")


if __name__ == "__main__":
    main()
