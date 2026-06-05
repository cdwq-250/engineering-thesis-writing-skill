#!/usr/bin/env python
"""Scan a project workspace and write a thesis evidence inventory."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Iterable


EXCLUDED_DIRS = {
    ".git",
    ".pytest_cache",
    ".tmp_test",
    "__pycache__",
    "downloads",
    "node_modules",
    "private_corpus",
    "private_extracts",
    "private_outputs",
    "venv",
}

EVIDENCE_SUFFIXES = {
    "code": {".py", ".js", ".ts", ".tsx", ".java", ".cpp", ".c", ".cc", ".cs", ".go", ".rs"},
    "config": {".json", ".yaml", ".yml", ".toml", ".ini", ".cfg"},
    "csv": {".csv", ".tsv"},
    "figure": {".png", ".jpg", ".jpeg", ".webp", ".svg"},
    "document": {".md", ".txt"},
}

TEST_PATTERNS = ("test_", "_test", ".spec.", ".test.")


def iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative_parts = path.relative_to(root).parts
        if any(part in EXCLUDED_DIRS for part in relative_parts):
            continue
        yield path


def classify(path: Path) -> str | None:
    name = path.name.lower()
    if "test" in {part.lower() for part in path.parts} or any(token in name for token in TEST_PATTERNS):
        return "test"
    suffix = path.suffix.lower()
    for evidence_type, suffixes in EVIDENCE_SUFFIXES.items():
        if suffix in suffixes:
            return evidence_type
    return None


def conservative_wording(evidence_type: str, rel_path: str) -> str:
    if evidence_type == "code":
        return f"代码实现可支撑相关功能、流程或模块设计说明（来源：{rel_path}）。"
    if evidence_type == "config":
        return f"配置文件可支撑系统参数、环境设置或流程约束说明（来源：{rel_path}）。"
    if evidence_type == "csv":
        return f"数据文件可支撑案例级或实验级指标分析（来源：{rel_path}）。"
    if evidence_type == "figure":
        return f"图像文件可支撑界面、流程或结果展示说明（来源：{rel_path}）。"
    if evidence_type == "test":
        return f"测试文件可支撑功能验证或边界验证说明（来源：{rel_path}）。"
    return f"文档可支撑背景、流程或约束说明（来源：{rel_path}）。"


def build_inventory(root: Path) -> dict[str, list[dict[str, str]]]:
    inventory: dict[str, list[dict[str, str]]] = defaultdict(list)
    for path in iter_files(root):
        evidence_type = classify(path)
        if evidence_type is None:
            continue
        rel_path = path.relative_to(root).as_posix()
        inventory[evidence_type].append(
            {
                "path": rel_path,
                "claim_template": f"待补充：说明 `{rel_path}` 支撑的论文 claim。",
                "allowed_wording": conservative_wording(evidence_type, rel_path),
            }
        )
    for evidence_type in inventory:
        inventory[evidence_type].sort(key=lambda item: item["path"])
    return dict(inventory)


def write_markdown(output: Path, root: Path, thesis_type: str, inventory: dict[str, list[dict[str, str]]]) -> None:
    lines = [
        "# Evidence Inventory",
        "",
        "This is a private local inventory for thesis evidence mapping. Do not publish it when it contains real project paths or private data references.",
        "",
        f"- Project root: `{root}`",
        f"- Thesis type: `{thesis_type}`",
        "",
        "## Summary",
        "",
    ]
    if not inventory:
        lines.append("- No supported evidence files found.")
    else:
        for evidence_type in sorted(inventory):
            lines.append(f"- {evidence_type}: {len(inventory[evidence_type])}")
    lines.extend(
        [
            "",
            "## Suggested `evidence[]` Seeds",
            "",
            "Use these rows to draft `thesis-profile.json`. Replace each claim template with a concrete, conservative claim.",
            "",
        ]
    )
    for evidence_type in sorted(inventory):
        lines.extend([f"### {evidence_type}", "", "| Path | Claim Template | Allowed Wording |", "|---|---|---|"])
        for item in inventory[evidence_type]:
            lines.append(f"| `{item['path']}` | {item['claim_template']} | {item['allowed_wording']} |")
        lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_json(output: Path, inventory: dict[str, list[dict[str, str]]]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan a project and write a thesis evidence inventory.")
    parser.add_argument("--project-root", type=Path, default=Path("."))
    parser.add_argument(
        "--thesis-type",
        choices=["software_system", "control_optimization", "mechanical_manufacturing", "undecided"],
        default="undecided",
    )
    parser.add_argument("--output-md", type=Path, default=Path("private_outputs/evidence_inventory.md"))
    parser.add_argument("--output-json", type=Path, default=Path("private_outputs/evidence_inventory.json"))
    args = parser.parse_args()

    inventory = build_inventory(args.project_root.resolve())
    write_markdown(args.output_md, args.project_root.resolve(), args.thesis_type, inventory)
    write_json(args.output_json, inventory)
    print(f"evidence_inventory_md={args.output_md}")
    print(f"evidence_inventory_json={args.output_json}")


if __name__ == "__main__":
    main()
