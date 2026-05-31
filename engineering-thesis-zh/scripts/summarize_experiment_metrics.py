#!/usr/bin/env python
"""Summarize experiment CSV metrics for evidence-grounded thesis writing."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


LOWER_IS_BETTER = {
    "makespan",
    "average_flow_time",
    "total_tardiness",
    "failure_count",
    "maintenance_count",
    "maintenance_downtime",
    "maintenance_cost",
    "composite_objective",
    "completion_time",
    "flow_time",
    "tardiness",
}
HIGHER_IS_BETTER = {"on_time_rate", "utilization"}
GROUP_COLUMNS = [
    "dispatch_rule",
    "maintenance_policy",
    "degradation_per_hour",
    "station_id",
    "station_type",
    "order_id",
]


def format_value(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.4g}"
    return str(value)


def best_row(df: pd.DataFrame, metric: str) -> pd.Series:
    if metric in HIGHER_IS_BETTER:
        return df.loc[df[metric].idxmax()]
    return df.loc[df[metric].idxmin()]


def tied_keys(df: pd.DataFrame, metric: str, group_cols: list[str]) -> tuple[pd.Series, int]:
    row = best_row(df, metric)
    best_value = row[metric]
    tied = df[df[metric] == best_value]
    return row, len(tied)


def summarize_file(path: Path) -> list[str]:
    df = pd.read_csv(path)
    lines = [f"## {path.name}", "", f"- Rows: {len(df)}", f"- Columns: {', '.join(df.columns)}"]
    group_cols = [column for column in GROUP_COLUMNS if column in df.columns]
    metrics = [column for column in df.columns if column in LOWER_IS_BETTER or column in HIGHER_IS_BETTER]

    if group_cols:
        lines.append(f"- Comparison key: {', '.join(group_cols)}")
    if not metrics:
        lines.append("- No recognized thesis metrics found.")
        return lines + [""]

    lines.append("")
    lines.append("| Metric | Best row | Best value | Thesis-safe interpretation |")
    lines.append("|---|---|---:|---|")
    for metric in metrics:
        row, tie_count = tied_keys(df, metric, group_cols)
        key = ", ".join(f"{col}={format_value(row[col])}" for col in group_cols) if group_cols else f"row={row.name}"
        direction = "higher is better" if metric in HIGHER_IS_BETTER else "lower is better"
        if tie_count == len(df) and len(df) > 1:
            interpretation = f"In this scenario, all compared rows have the same {metric}; do not claim a difference."
            key = "all compared rows"
        elif tie_count > 1:
            interpretation = f"In this scenario, {tie_count} rows tie for the best {metric} ({direction}); discuss the tie."
        else:
            interpretation = f"In this scenario, {key} has the best {metric} ({direction})."
        lines.append(f"| `{metric}` | {key} | {format_value(row[metric])} | {interpretation} |")

    return lines + [""]


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a Markdown metric summary from experiment CSV files.")
    parser.add_argument("csv_root", type=Path, help="CSV file or directory")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    paths = [args.csv_root] if args.csv_root.is_file() else sorted(args.csv_root.glob("*.csv"))
    args.output.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Experiment Metric Summary",
        "",
        "This report is generated from CSV files and is intended as thesis-writing evidence.",
        "Interpretations are scenario-bound and must not be generalized beyond the actual experiment design.",
        "",
    ]
    for path in paths:
        lines.extend(summarize_file(path))

    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"files={len(paths)}")
    print(f"output={args.output}")


if __name__ == "__main__":
    main()
