#!/usr/bin/env python
"""Generate cautious family-level writing rule drafts from family briefs."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_pairs(value: str) -> list[tuple[str, int]]:
    pairs: list[tuple[str, int]] = []
    for chunk in value.split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        name, count = chunk.rsplit(":", 1)
        pairs.append((name, int(count)))
    return pairs


def parse_signal_pairs(value: str) -> list[tuple[str, str, int]]:
    pairs: list[tuple[str, str, int]] = []
    for chunk in value.split(";"):
        chunk = chunk.strip()
        if not chunk:
            continue
        signal_type, signal, count = chunk.split(":")
        pairs.append((signal_type, signal, int(count)))
    return pairs


def family_heading(label: str) -> str:
    return {
        "software/system": "Software/System Draft Rules",
        "control/optimization": "Control/Optimization Draft Rules",
        "mechanical/manufacturing": "Mechanical/Manufacturing Draft Rules",
    }.get(label, label)


def write_markdown(output: Path, rows: list[dict[str, str]]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Family Rule Drafts",
        "",
        "This report converts family-level aggregate signals into cautious draft rules. These are not promoted references yet. Use them as staging material before editing `references/` content.",
        "",
    ]
    for row in rows:
        family = row["family"]
        evidence_level = row["evidence_level"]
        role_pairs = parse_pairs(row["top_roles"])
        signal_pairs = parse_signal_pairs(row["top_signals"])
        lines.extend(
            [
                f"## {family_heading(family)}",
                "",
                f"- Family: `{family}`",
                f"- Records in corpus: {row['records_in_corpus']}",
                f"- Evidence level: `{evidence_level}`",
                "",
                "### Candidate Rules",
                "",
            ]
        )
        if evidence_level == "candidate":
            if role_pairs:
                lines.append(
                    f"- Prefer chapter logic that gives clear room to `{role_pairs[0][0]}` and `{role_pairs[1][0] if len(role_pairs) > 1 else role_pairs[0][0]}` before concluding effectiveness."
                )
            if signal_pairs:
                first_signal = signal_pairs[0]
                lines.append(
                    f"- Keep the family object explicit; current corpus most often exposes `{first_signal[0]}:{first_signal[1]}` as a repeated drafting anchor."
                )
            lines.append("- Treat these as structural prompts only; every result claim still needs project evidence.")
        elif evidence_level == "weak_signal":
            lines.append("- Use these observations only as weak prompts when the concrete project clearly matches the family.")
            lines.append("- Do not promote them into stable skill rules until more theses are added.")
        else:
            lines.append("- Do not use these observations as family-specific writing rules yet.")
            lines.append("- Keep relying on the general corpus-derived rules plus project evidence until this family gains more samples.")
        lines.extend(["", "### Suggested Reference Edits Later", ""])
        if role_pairs:
            lines.append(
                "- Consider adding or strengthening these chapter-role hints in the family reference: "
                + ", ".join(f"`{name}` ({count})" for name, count in role_pairs[:4])
            )
        if signal_pairs:
            lines.append(
                "- Consider adding these family-specific anchor signals in the family reference: "
                + ", ".join(f"`{signal_type}:{signal}` ({count})" for signal_type, signal, count in signal_pairs[:4])
            )
        lines.extend(["", "### Promotion Gate", ""])
        if evidence_level == "candidate":
            lines.append("- Before promotion, compare these rules against at least one more legal acquisition batch and confirm the same roles/signals still dominate.")
        else:
            lines.append("- Promotion is blocked by sparse family coverage; follow `acquisition_plan.md` before editing stable references.")
        lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")


def write_csv(output: Path, rows: list[dict[str, str]]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        fieldnames = ["family", "records_in_corpus", "evidence_level", "draft_rule_summary", "promotion_gate"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            roles = ", ".join(name for name, _count in parse_pairs(row["top_roles"])[:3])
            if row["evidence_level"] == "candidate":
                summary = f"Use {roles} as cautious structural prompts"
                gate = "recheck after another batch"
            elif row["evidence_level"] == "weak_signal":
                summary = f"Only weak prompts available for {roles}"
                gate = "need more family samples"
            else:
                summary = "No reliable family-specific rule yet"
                gate = "blocked by sparse family coverage"
            writer.writerow(
                {
                    "family": row["family"],
                    "records_in_corpus": row["records_in_corpus"],
                    "evidence_level": row["evidence_level"],
                    "draft_rule_summary": summary,
                    "promotion_gate": gate,
                }
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate cautious family-level writing rule drafts from family briefs.")
    parser.add_argument("--family-brief-csv", type=Path, default=Path("public_stats/corpus/family_writing_briefs.csv"))
    parser.add_argument("--output-md", type=Path, default=Path("public_stats/corpus/family_rule_drafts.md"))
    parser.add_argument("--output-csv", type=Path, default=Path("public_stats/corpus/family_rule_drafts.csv"))
    args = parser.parse_args()

    rows = read_csv(args.family_brief_csv)
    write_markdown(args.output_md, rows)
    write_csv(args.output_csv, rows)
    print(f"family_rule_drafts_md={args.output_md}")
    print(f"family_rule_drafts_csv={args.output_csv}")


if __name__ == "__main__":
    main()
