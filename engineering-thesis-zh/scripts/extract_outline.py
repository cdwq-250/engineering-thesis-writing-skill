#!/usr/bin/env python
"""Extract structural metadata from local Chinese thesis PDFs.

The output is JSON Lines. It is intended for private/local processing first.
Do not commit records that include copyrighted source text beyond structural
labels such as headings or figure/table captions.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from pypdf import PdfReader

try:
    import pdfplumber
except Exception:  # pragma: no cover - optional dependency fallback
    pdfplumber = None


HEADING_PATTERNS = [
    re.compile(r"^(第[一二三四五六七八九十0-9]+章\s+.{2,60})$"),
    re.compile(r"^([0-9]+\.[0-9]+(?:\.[0-9]+)?\s+.{2,60})$"),
    re.compile(r"^(绪论|摘要|Abstract|结论|总结与展望|参考文献|致谢|附录)$", re.I),
]
FIGURE_PATTERN = re.compile(r"^([图表]\s*[0-9一二三四五六七八九十\-\.]+[\s:：、]*(.{2,80}))$")
KEYWORD_PATTERN = re.compile(r"(关键词|关键字)\s*[:：]\s*(.{2,120})")


@dataclass
class ThesisRecord:
    path: str
    file_name: str
    page_count: int
    title_candidates: list[str]
    keyword_candidates: list[str]
    headings: list[str]
    figure_table_titles: list[str]
    parse_error: str | None = None


def iter_pdfs(root: Path) -> Iterable[Path]:
    if root.is_file() and root.suffix.lower() == ".pdf":
        yield root
        return
    yield from sorted(root.rglob("*.pdf"))


def clean_line(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip())


def unique_keep_order(items: Iterable[str], limit: int) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        item = clean_line(item)
        if not item or item in seen:
            continue
        seen.add(item)
        result.append(item)
        if len(result) >= limit:
            break
    return result


def extract_text_with_pdfplumber(pdf_path: Path, max_pages: int | None) -> list[str]:
    if pdfplumber is None:
        raise RuntimeError("pdfplumber is not installed")
    with pdfplumber.open(pdf_path) as pdf:
        pages = pdf.pages if max_pages is None else pdf.pages[:max_pages]
        return [page.extract_text() or "" for page in pages]


def extract_text_with_pypdf(reader: PdfReader, max_pages: int | None) -> list[str]:
    pages = reader.pages if max_pages is None else reader.pages[:max_pages]
    texts: list[str] = []
    for page in pages:
        try:
            texts.append(page.extract_text() or "")
        except Exception:
            texts.append("")
    return texts


def looks_like_heading(line: str) -> bool:
    if len(line) > 80:
        return False
    return any(pattern.match(line) for pattern in HEADING_PATTERNS)


def split_keywords(raw: str) -> list[str]:
    return [part for part in re.split(r"[;；,，、\s]+", raw) if part]


def extract_record(pdf_path: Path, root: Path, max_pages: int | None) -> ThesisRecord:
    try:
        reader = PdfReader(str(pdf_path))
        page_count = len(reader.pages)
        try:
            texts = extract_text_with_pdfplumber(pdf_path, max_pages)
        except Exception:
            texts = extract_text_with_pypdf(reader, max_pages)

        lines = [clean_line(line) for text in texts for line in text.splitlines()]
        lines = [line for line in lines if line]

        headings = unique_keep_order((line for line in lines if looks_like_heading(line)), 200)

        figure_titles: list[str] = []
        for line in lines:
            match = FIGURE_PATTERN.match(line)
            if match:
                figure_titles.append(line)

        keywords: list[str] = []
        for line in lines[:200]:
            match = KEYWORD_PATTERN.search(line)
            if match:
                keywords.extend(split_keywords(match.group(2)))

        title_candidates = [
            line
            for line in lines[:80]
            if 8 <= len(line) <= 50 and not looks_like_heading(line) and "大学" not in line
        ]

        return ThesisRecord(
            path=str(pdf_path.relative_to(root)) if pdf_path.is_relative_to(root) else str(pdf_path),
            file_name=pdf_path.name,
            page_count=page_count,
            title_candidates=unique_keep_order(title_candidates, 5),
            keyword_candidates=unique_keep_order(keywords, 20),
            headings=headings,
            figure_table_titles=unique_keep_order(figure_titles, 120),
        )
    except Exception as exc:
        return ThesisRecord(
            path=str(pdf_path),
            file_name=pdf_path.name,
            page_count=0,
            title_candidates=[],
            keyword_candidates=[],
            headings=[],
            figure_table_titles=[],
            parse_error=f"{type(exc).__name__}: {exc}",
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract thesis PDF structural metadata.")
    parser.add_argument("input", type=Path, help="PDF file or directory containing PDFs")
    parser.add_argument("--output", type=Path, required=True, help="Output JSONL path")
    parser.add_argument("--max-pages", type=int, default=40, help="Pages to inspect per PDF; 0 means all pages")
    args = parser.parse_args()

    root = args.input.resolve()
    max_pages = None if args.max_pages == 0 else args.max_pages
    args.output.parent.mkdir(parents=True, exist_ok=True)

    with args.output.open("w", encoding="utf-8") as handle:
        for pdf_path in iter_pdfs(root):
            record = extract_record(pdf_path.resolve(), root, max_pages)
            handle.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
