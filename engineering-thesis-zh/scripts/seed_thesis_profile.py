#!/usr/bin/env python
"""Create an editable thesis-profile seed from an evidence inventory."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_TOPIC_TAGS = {
    "software_system": ["software_platform"],
    "control_optimization": ["algorithm_modeling", "production_scheduling"],
    "mechanical_manufacturing": ["equipment_maintenance", "production_scheduling"],
}

SUPPORTED_TYPES = set(DEFAULT_TOPIC_TAGS)


def read_inventory(path: Path) -> dict[str, list[dict[str, str]]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit("inventory_json: top-level value must be an object")
    normalized: dict[str, list[dict[str, str]]] = {}
    for evidence_type, items in data.items():
        if isinstance(items, list):
            normalized[evidence_type] = [item for item in items if isinstance(item, dict)]
    return normalized


def build_profile_seed(
    inventory: dict[str, list[dict[str, str]]],
    thesis_type: str,
    title: str,
    max_evidence_per_type: int,
) -> dict[str, Any]:
    evidence: list[dict[str, str]] = []
    for evidence_type in sorted(inventory):
        for item in inventory[evidence_type][:max_evidence_per_type]:
            evidence.append(
                {
                    "claim": item.get("claim_template", "待补充：说明该证据支撑的论文 claim。"),
                    "source": item.get("path", ""),
                    "type": evidence_type,
                    "allowed_wording": item.get("allowed_wording", "按证据强度保守表述。"),
                }
            )

    return {
        "title": title,
        "thesis_type": thesis_type,
        "topic_tags": DEFAULT_TOPIC_TAGS[thesis_type],
        "constraints": [
            "replace every seed claim with a concrete project-specific claim before drafting",
            "do not add unsupported strong claims without evidence sources",
        ],
        "known_gaps": [
            "claim templates still need manual refinement",
            "topic tags, constraints, and evidence coverage should be reviewed with the user",
        ],
        "evidence": evidence,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an editable thesis-profile seed from evidence inventory JSON.")
    parser.add_argument("--inventory-json", type=Path, default=Path("private_outputs/evidence_inventory.json"))
    parser.add_argument("--thesis-type", choices=sorted(SUPPORTED_TYPES), required=True)
    parser.add_argument("--title", default="待定题目")
    parser.add_argument("--max-evidence-per-type", type=int, default=3)
    parser.add_argument("--output", type=Path, default=Path("private_outputs/thesis-profile.seed.json"))
    args = parser.parse_args()

    profile = build_profile_seed(
        read_inventory(args.inventory_json),
        args.thesis_type,
        args.title,
        args.max_evidence_per_type,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"profile_seed={args.output}")


if __name__ == "__main__":
    main()
