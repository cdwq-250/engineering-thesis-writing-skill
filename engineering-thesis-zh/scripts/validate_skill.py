#!/usr/bin/env python
"""Validate the minimal structure required for a Codex skill."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


NAME_PATTERN = re.compile(r"^[a-z0-9-]{1,63}$")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter.")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("SKILL.md frontmatter is not closed.")
    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    return values


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a Codex skill folder.")
    parser.add_argument("skill_dir", type=Path)
    args = parser.parse_args()

    skill_md = args.skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise SystemExit(f"SKILL.md not found: {skill_md}")

    frontmatter = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")

    if not NAME_PATTERN.match(name):
        raise SystemExit(f"Invalid skill name: {name!r}")
    if len(description) < 80:
        raise SystemExit("Skill description is too short to be useful.")

    print("Skill structure is valid.")


if __name__ == "__main__":
    main()

