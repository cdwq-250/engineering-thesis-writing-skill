#!/usr/bin/env python
"""Run the local thesis writing preparation workflow end to end."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from seed_thesis_profile import build_profile_seed, read_inventory
from write_collaboration_plan import read_json, readiness_level, write_plan as write_collaboration_plan
from write_evidence_inventory import build_inventory, write_json as write_inventory_json, write_markdown as write_inventory_md
from write_profile_questions import write_questions


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate collaboration plan, evidence inventory, thesis-profile seed, and interview questions."
    )
    parser.add_argument(
        "--thesis-type",
        choices=["software_system", "control_optimization", "mechanical_manufacturing"],
        required=True,
    )
    parser.add_argument("--project-root", type=Path, default=Path("."))
    parser.add_argument("--summary", type=Path, default=Path("public_stats/corpus/summary.json"))
    parser.add_argument("--readiness-report", type=Path, default=Path("public_stats/corpus/readiness_report.md"))
    parser.add_argument("--title", default="待定题目")
    parser.add_argument("--output-dir", type=Path, default=Path("private_outputs/writing_prep"))
    parser.add_argument("--max-evidence-per-type", type=int, default=3)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    collaboration_plan = args.output_dir / "collaboration_plan.md"
    evidence_inventory_md = args.output_dir / "evidence_inventory.md"
    evidence_inventory_json = args.output_dir / "evidence_inventory.json"
    thesis_profile_seed = args.output_dir / "thesis-profile.seed.json"
    profile_questions = args.output_dir / "profile_questions.md"

    write_collaboration_plan(
        collaboration_plan,
        args.thesis_type,
        read_json(args.summary),
        readiness_level(args.readiness_report),
    )

    inventory = build_inventory(args.project_root.resolve())
    write_inventory_md(evidence_inventory_md, args.project_root.resolve(), args.thesis_type, inventory)
    write_inventory_json(evidence_inventory_json, inventory)

    seed = build_profile_seed(read_inventory(evidence_inventory_json), args.thesis_type, args.title, args.max_evidence_per_type)
    thesis_profile_seed.write_text(json.dumps(seed, ensure_ascii=False, indent=2), encoding="utf-8")

    write_questions(args.thesis_type, profile_questions)

    print(f"collaboration_plan={collaboration_plan}")
    print(f"evidence_inventory_md={evidence_inventory_md}")
    print(f"evidence_inventory_json={evidence_inventory_json}")
    print(f"profile_seed={thesis_profile_seed}")
    print(f"profile_questions={profile_questions}")


if __name__ == "__main__":
    main()
