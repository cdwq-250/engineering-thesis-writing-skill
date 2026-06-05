#!/usr/bin/env python
"""Compare family rule drafts against current family references."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


REFERENCE_MAP = {
    "software/system": "software-system-thesis.md",
    "control/optimization": "control-optimization-thesis.md",
    "mechanical/manufacturing": "mechanical-manufacturing-thesis.md",
}


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def extract_draft_sections(text: str) -> dict[str, dict[str, list[str] | str]]:
    sections: dict[str, dict[str, list[str] | str]] = {}
    current_family: str | None = None
    current_mode: str | None = None
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("## ") and "Draft Rules" in line:
            current_family = None
            current_mode = None
        elif line.startswith("- Family: `"):
            current_family = line.split("`")[1]
            sections[current_family] = {"candidate_rules": [], "suggested_reference_edits": [], "promotion_gate": ""}
        elif line == "### Candidate Rules":
            current_mode = "candidate_rules"
        elif line == "### Suggested Reference Edits Later":
            current_mode = "suggested_reference_edits"
        elif line == "### Promotion Gate":
            current_mode = "promotion_gate"
        elif current_family and line.startswith("- "):
            if current_mode == "promotion_gate":
                sections[current_family]["promotion_gate"] = line[2:]
            elif current_mode in {"candidate_rules", "suggested_reference_edits"}:
                sections[current_family][current_mode].append(line[2:])
    return sections


def normalize_term(term: str) -> str:
    cleaned = term.replace("`", "")
    if "(" in cleaned:
        cleaned = cleaned.split("(")[0]
    return cleaned.strip().lower()


def extract_terms(item: str) -> list[str]:
    if ":" in item:
        payload = item.split(":", 1)[1]
    else:
        payload = item
    parts = [part.strip() for part in payload.split(",")]
    return [part for part in parts if part]


def term_covered(reference_text: str, term: str) -> bool:
    normalized_reference = reference_text.lower()
    normalized_term = normalize_term(term)
    if ":" in normalized_term:
        normalized_term = normalized_term.split(":", 1)[1]
    return normalized_term in normalized_reference


def analyze_alignment(drafts_text: str, references_dir: Path) -> list[dict[str, str]]:
    sections = extract_draft_sections(drafts_text)
    rows: list[dict[str, str]] = []
    for family, file_name in REFERENCE_MAP.items():
        reference_text = (references_dir / file_name).read_text(encoding="utf-8")
        draft = sections.get(family, {})
        evidence_level = ""
        if "blocked by sparse family coverage" in str(draft.get("promotion_gate", "")):
            evidence_level = "hold_sparse"
        elif "compare these rules against at least one more legal acquisition batch" in str(draft.get("promotion_gate", "")):
            evidence_level = "candidate_recheck"
        else:
            evidence_level = "unknown"
        for item in draft.get("suggested_reference_edits", []):
            for term in extract_terms(item):
                covered = term_covered(reference_text, term)
                rows.append(
                    {
                        "family": family,
                        "reference_file": file_name,
                        "draft_item": term,
                        "covered_in_reference": "yes" if covered else "no",
                        "promotion_gate": str(draft.get("promotion_gate", "")),
                        "recommended_action": "hold" if evidence_level == "hold_sparse" else ("review_merge" if not covered else "already_covered"),
                    }
                )
    return rows


def write_markdown(output: Path, rows: list[dict[str, str]]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Reference Alignment Report",
        "",
        "This report compares family rule drafts against the current stable family references. It does not auto-edit the references.",
        "",
        "## Alignment Rows",
        "",
        "| Family | Reference | Covered | Recommended Action | Draft Item |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['family']} | `{row['reference_file']}` | {row['covered_in_reference']} | {row['recommended_action']} | {row['draft_item']} |"
        )
    lines.extend(
        [
            "",
            "## Next Step",
            "",
            "- `hold` means the family still lacks enough evidence and the reference should stay unchanged.",
            "- `already_covered` means the existing family reference already contains a close hint and does not need a new edit yet.",
            "- `review_merge` means the family evidence is no longer fully blocked and the draft item is not obviously covered in the current reference.",
            "",
        ]
    )
    output.write_text("\n".join(lines), encoding="utf-8")


def write_csv(output: Path, rows: list[dict[str, str]]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["family", "reference_file", "draft_item", "covered_in_reference", "promotion_gate", "recommended_action"],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare family rule drafts against current family references.")
    parser.add_argument("--draft-md", type=Path, default=Path("public_stats/corpus/family_rule_drafts.md"))
    parser.add_argument("--references-dir", type=Path, default=Path("engineering-thesis-zh/references"))
    parser.add_argument("--output-md", type=Path, default=Path("public_stats/corpus/reference_alignment_report.md"))
    parser.add_argument("--output-csv", type=Path, default=Path("public_stats/corpus/reference_alignment_report.csv"))
    args = parser.parse_args()

    rows = analyze_alignment(args.draft_md.read_text(encoding="utf-8"), args.references_dir)
    write_markdown(args.output_md, rows)
    write_csv(args.output_csv, rows)
    print(f"reference_alignment_md={args.output_md}")
    print(f"reference_alignment_csv={args.output_csv}")


if __name__ == "__main__":
    main()
