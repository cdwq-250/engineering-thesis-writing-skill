#!/usr/bin/env python
"""Extract structural metadata from local Markdown thesis drafts.

This is useful for validating the skill against a user's own draft before a
large PDF corpus is available.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


KEYWORD_PATTERN = re.compile(r"(关键词|关键字)\s*[:：]\s*(.+)")


@dataclass
class MarkdownRecord:
    path: str
    file_name: str
    line_count: int
    title_candidates: list[str]
    keyword_candidates: list[str]
    headings: list[str]
    figure_table_titles: list[str]
    parse_error: str | None = None


def iter_markdown(root: Path) -> Iterable[Path]:
    if root.is_file() and root.suffix.lower() in {".md", ".markdown"}:
        yield root
        return
    for pattern in ("*.md", "*.markdown"):
        yield from sorted(root.rglob(pattern))


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def unique(items: Iterable[str], limit: int) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        item = clean(item)
        if not item or item in seen:
            continue
        seen.add(item)
        result.append(item)
        if len(result) >= limit:
            break
    return result


def extract_one(path: Path, root: Path) -> MarkdownRecord:
    try:
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        headings = []
        figure_titles = []
        keywords = []
        title_candidates = []

        for line in lines:
            stripped = clean(line)
            if stripped.startswith("#"):
                heading = clean(stripped.lstrip("#"))
                headings.append(heading)
                if stripped.startswith("# ") and len(heading) >= 8:
                    title_candidates.append(heading)
            if stripped.startswith(("图", "表")) and len(stripped) <= 100:
                figure_titles.append(stripped)
            match = KEYWORD_PATTERN.search(stripped)
            if match:
                keywords.extend(re.split(r"[；;，,、\s]+", match.group(2)))

        return MarkdownRecord(
            path=str(path.relative_to(root)) if path.is_relative_to(root) else str(path),
            file_name=path.name,
            line_count=len(lines),
            title_candidates=unique(title_candidates, 5),
            keyword_candidates=unique(keywords, 20),
            headings=unique(headings, 300),
            figure_table_titles=unique(figure_titles, 120),
        )
    except Exception as exc:
        return MarkdownRecord(
            path=str(path),
            file_name=path.name,
            line_count=0,
            title_candidates=[],
            keyword_candidates=[],
            headings=[],
            figure_table_titles=[],
            parse_error=f"{type(exc).__name__}: {exc}",
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract Markdown thesis-draft outline metadata.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    root = args.input.resolve()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for path in iter_markdown(root):
            record = extract_one(path.resolve(), root)
            handle.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()

