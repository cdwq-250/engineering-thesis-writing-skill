#!/usr/bin/env python
"""Run the profile-to-plan-to-skeleton writing pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

from audit_manuscript_claims import audit
from generate_manuscript_skeleton import write_skeleton
from generate_thesis_plan import load_profile, write_plan
from validate_thesis_profile import validate_profile


def write_report(output: Path, profile_path: Path, plan_path: Path, skeleton_path: Path, audit_errors: list[str], audit_warnings: list[str]) -> None:
    lines = [
        "# Writing Pipeline Report",
        "",
        f"- Profile: `{profile_path}`",
        f"- Plan: `{plan_path}`",
        f"- Skeleton: `{skeleton_path}`",
        f"- Claim audit errors: {len(audit_errors)}",
        f"- Claim audit warnings: {len(audit_warnings)}",
        "",
        "## Claim Audit",
        "",
    ]
    if audit_errors:
        lines.extend([f"- ERROR: {error}" for error in audit_errors])
    else:
        lines.append("- Passed: no unsupported strong claims detected.")
    if audit_warnings:
        lines.extend(["", "## Warnings", ""])
        lines.extend([f"- {warning}" for warning in audit_warnings])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run thesis profile validation, plan generation, skeleton generation, and claim audit.")
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--fail-on-audit-error", action="store_true", help="Exit 1 if generated skeleton contains unsupported strong claims.")
    args = parser.parse_args()

    profile = load_profile(args.profile)
    errors, warnings = validate_profile(profile)
    for warning in warnings:
        print(f"warning:{warning}")
    if errors:
        for error in errors:
            print(f"error:{error}")
        raise SystemExit(1)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    plan_path = args.output_dir / "thesis_plan.md"
    skeleton_path = args.output_dir / "manuscript_skeleton.md"
    report_path = args.output_dir / "pipeline_report.md"

    write_plan(profile, plan_path)
    write_skeleton(profile, skeleton_path)
    audit_errors, audit_warnings = audit(skeleton_path.read_text(encoding="utf-8"))
    write_report(report_path, args.profile, plan_path, skeleton_path, audit_errors, audit_warnings)

    print(f"plan={plan_path}")
    print(f"skeleton={skeleton_path}")
    print(f"report={report_path}")
    if audit_errors and args.fail_on_audit_error:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
