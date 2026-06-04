#!/usr/bin/env python
"""Validate a thesis planning profile before generating a writing plan."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SUPPORTED_THESIS_TYPES = {"mechanical_manufacturing", "control_optimization", "software_system"}
SUPPORTED_EVIDENCE_TYPES = {"code", "config", "csv", "test", "figure", "screenshot", "document", "user_confirmation"}
STRONG_CLAIM_WORDS = ["显著", "工业级", "国内领先", "全面解决", "最优", "投入运行", "实际应用证明"]


def load_profile(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid_json: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("invalid_profile: top-level JSON value must be an object")
    return data


def validate_profile(profile: dict[str, Any]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    title = profile.get("title")
    if not isinstance(title, str) or not title.strip():
        errors.append("title: required non-empty string")

    thesis_type = profile.get("thesis_type")
    if thesis_type not in SUPPORTED_THESIS_TYPES:
        errors.append("thesis_type: must be one of " + ", ".join(sorted(SUPPORTED_THESIS_TYPES)))

    if "topic_tags" not in profile:
        warnings.append("topic_tags: missing; planner can run but topic grounding will be weaker")
    elif not isinstance(profile.get("topic_tags"), list):
        errors.append("topic_tags: must be a list when present")

    for optional_list in ["constraints", "known_gaps"]:
        if optional_list not in profile:
            warnings.append(f"{optional_list}: missing; add it if planning decisions depend on it")
        elif not isinstance(profile.get(optional_list), list):
            errors.append(f"{optional_list}: must be a list when present")

    evidence = profile.get("evidence")
    if not isinstance(evidence, list):
        errors.append("evidence: required list")
        evidence = []

    for index, item in enumerate(evidence, 1):
        if not isinstance(item, dict):
            errors.append(f"evidence[{index}]: must be an object")
            continue
        claim = item.get("claim", "")
        source = item.get("source", "")
        evidence_type = item.get("type", "document")
        if not isinstance(claim, str) or not claim.strip():
            errors.append(f"evidence[{index}].claim: required non-empty string")
        if evidence_type not in SUPPORTED_EVIDENCE_TYPES:
            errors.append(f"evidence[{index}].type: unsupported evidence type `{evidence_type}`")
        if any(word in str(claim) for word in STRONG_CLAIM_WORDS) and not str(source).strip():
            errors.append(f"evidence[{index}].source: strong claim requires concrete evidence source")
        if not item.get("allowed_wording"):
            warnings.append(f"evidence[{index}].allowed_wording: missing; planner will use generic conservative wording")

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a thesis profile JSON file.")
    parser.add_argument("profile", type=Path)
    args = parser.parse_args()

    profile = load_profile(args.profile)
    errors, warnings = validate_profile(profile)
    for warning in warnings:
        print(f"warning:{warning}")
    for error in errors:
        print(f"error:{error}")
    if errors:
        raise SystemExit(1)
    print("profile_valid=true")


if __name__ == "__main__":
    main()
