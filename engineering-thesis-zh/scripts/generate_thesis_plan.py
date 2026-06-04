#!/usr/bin/env python
"""Generate an evidence-grounded Chinese engineering thesis writing plan."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


THESIS_TYPES = {
    "mechanical_manufacturing": {
        "label": "机械/制造/设备维护类",
        "chapters": [
            ("第1章 绪论", ["1.1 研究背景与意义", "1.2 国内外研究现状", "1.3 研究内容与技术路线"]),
            ("第2章 理论基础与方法综述", ["2.1 相关理论基础", "2.2 关键方法与评价指标", "2.3 本文方法适用边界"]),
            ("第3章 对象现状与问题诊断", ["3.1 研究对象与流程说明", "3.2 现状指标与问题识别", "3.3 原因分析与改进需求"]),
            ("第4章 模型、策略或改进方案设计", ["4.1 设计目标与原则", "4.2 核心模型/策略/流程设计", "4.3 实施或仿真流程"]),
            ("第5章 验证与结果分析", ["5.1 场景、数据与参数设置", "5.2 对比结果与指标分析", "5.3 工程解释与局限性"]),
            ("第6章 总结与展望", ["6.1 研究工作总结", "6.2 不足与后续工作"]),
        ],
        "default_figures": ["现状流程图", "原因分析图", "方案流程图", "指标对比图"],
        "default_metrics": ["OEE", "停机时间", "维护成本", "延期时间", "产线利用率", "缺陷率"],
    },
    "control_optimization": {
        "label": "控制/优化/调度类",
        "chapters": [
            ("第1章 绪论", ["1.1 工程背景与问题来源", "1.2 国内外研究现状", "1.3 研究内容与章节安排"]),
            ("第2章 理论基础与相关算法", ["2.1 问题相关理论", "2.2 对比方法与评价指标", "2.3 技术路线"]),
            ("第3章 问题建模", ["3.1 场景描述与假设条件", "3.2 参数、变量与约束", "3.3 目标函数与模型分析"]),
            ("第4章 算法或策略设计", ["4.1 基线方法", "4.2 改进算法/策略", "4.3 求解流程与复杂度讨论"]),
            ("第5章 实验与结果分析", ["5.1 数据、参数与实验设置", "5.2 对比实验", "5.3 敏感性或消融分析"]),
            ("第6章 总结与展望", ["6.1 研究工作总结", "6.2 局限性与后续研究"]),
        ],
        "default_figures": ["问题建模示意图", "算法流程图", "实验对比图", "敏感性分析图"],
        "default_metrics": ["makespan", "tardiness", "flow time", "cost", "utilization", "runtime"],
    },
    "software_system": {
        "label": "软件系统/平台类",
        "chapters": [
            ("第1章 绪论", ["1.1 研究背景与意义", "1.2 国内外研究现状", "1.3 研究内容与组织结构"]),
            ("第2章 需求分析与关键技术", ["2.1 业务流程分析", "2.2 功能与非功能需求", "2.3 关键技术"]),
            ("第3章 系统总体设计", ["3.1 系统架构设计", "3.2 模块划分", "3.3 数据库与接口设计"]),
            ("第4章 系统详细设计与实现", ["4.1 核心模块实现", "4.2 数据处理与交互流程", "4.3 部署与运行环境"]),
            ("第5章 系统测试与验证", ["5.1 测试环境与用例", "5.2 功能测试", "5.3 边界与异常测试"]),
            ("第6章 总结与展望", ["6.1 工作总结", "6.2 不足与改进方向"]),
        ],
        "default_figures": ["系统架构图", "模块结构图", "数据库ER图", "测试截图"],
        "default_metrics": ["功能通过率", "响应时间", "异常处理覆盖", "测试用例数"],
    },
}

EVIDENCE_TYPES = {"code", "config", "csv", "test", "figure", "screenshot", "document", "user_confirmation"}
STRONG_CLAIM_WORDS = ["显著", "工业级", "国内领先", "全面解决", "最优", "投入运行", "实际应用证明"]


@dataclass
class EvidenceItem:
    claim: str
    source: str
    evidence_type: str
    allowed_wording: str


def load_profile(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_evidence(items: list[dict[str, Any]]) -> list[EvidenceItem]:
    evidence: list[EvidenceItem] = []
    for item in items:
        evidence_type = str(item.get("type", "document"))
        if evidence_type not in EVIDENCE_TYPES:
            evidence_type = "document"
        evidence.append(
            EvidenceItem(
                claim=str(item.get("claim", "")).strip(),
                source=str(item.get("source", "")).strip(),
                evidence_type=evidence_type,
                allowed_wording=str(item.get("allowed_wording", "")).strip(),
            )
        )
    return evidence


def unsupported_claims(evidence: list[EvidenceItem]) -> list[str]:
    claims = [item.claim for item in evidence if item.claim]
    flagged = [
        claim
        for claim in claims
        if any(word in claim for word in STRONG_CLAIM_WORDS)
        and not any(item.source for item in evidence if item.claim == claim)
    ]
    return flagged


def evidence_table(evidence: list[EvidenceItem]) -> list[str]:
    lines = [
        "| Claim | Evidence Source | Evidence Type | Allowed Wording |",
        "|---|---|---|---|",
    ]
    if not evidence:
        lines.append("| 待填写 | 待补充 | user_confirmation | 只能写为待验证问题 |")
        return lines
    for item in evidence:
        claim = item.claim or "待填写"
        source = item.source or "待补充"
        wording = item.allowed_wording or "按证据强度保守表述"
        lines.append(f"| {claim} | {source} | {item.evidence_type} | {wording} |")
    return lines


def chapter_lines(thesis_type: str) -> list[str]:
    spec = THESIS_TYPES[thesis_type]
    lines: list[str] = []
    for chapter, sections in spec["chapters"]:
        lines.append(f"### {chapter}")
        for section in sections:
            lines.append(f"- {section}")
        lines.append("")
    return lines


def figure_plan(thesis_type: str, evidence: list[EvidenceItem]) -> list[str]:
    spec = THESIS_TYPES[thesis_type]
    lines = ["| Figure/Table | Purpose | Evidence Needed |", "|---|---|---|"]
    for figure in spec["default_figures"]:
        lines.append(f"| {figure} | 支撑结构、流程或验证叙述 | code/config/csv/figure/screenshot/document |")
    metric_sources = [item.source for item in evidence if item.evidence_type in {"csv", "test", "figure"} and item.source]
    if metric_sources:
        lines.append(f"| 指标汇总表 | 汇总可验证指标 | {', '.join(metric_sources[:5])} |")
    return lines


def write_plan(profile: dict[str, Any], output: Path) -> None:
    thesis_type = str(profile.get("thesis_type", "mechanical_manufacturing"))
    if thesis_type not in THESIS_TYPES:
        thesis_type = "mechanical_manufacturing"
    title = str(profile.get("title", "待定题目"))
    topic_tags = [str(tag) for tag in profile.get("topic_tags", [])]
    evidence = normalize_evidence(list(profile.get("evidence", [])))
    spec = THESIS_TYPES[thesis_type]
    missing = unsupported_claims(evidence)

    lines = [
        "# Thesis Writing Plan",
        "",
        f"- Title: {title}",
        f"- Thesis type: {thesis_type} ({spec['label']})",
        f"- Topic tags: {', '.join(topic_tags) if topic_tags else '待补充'}",
        "",
        "## Corpus-Grounded Rationale",
        "",
        "Use the problem-to-method-to-validation arc: background and literature review, current-state diagnosis, design, validation, and limitations.",
        "Do not copy source thesis text. Treat corpus signals as structure guidance only.",
        "",
        "## Chapter Outline",
        "",
    ]
    lines.extend(chapter_lines(thesis_type))
    lines.extend(["## Evidence Map", ""])
    lines.extend(evidence_table(evidence))
    lines.extend(["", "## Figure And Table Plan", ""])
    lines.extend(figure_plan(thesis_type, evidence))
    lines.extend(["", "## Metric Candidates", ""])
    lines.extend([f"- {metric}" for metric in spec["default_metrics"]])
    lines.extend(["", "## Unsupported Or Risky Claims", ""])
    if missing:
        lines.extend([f"- Remove or weaken: {claim}" for claim in missing])
    else:
        lines.append("- No unsupported strong claim detected from the provided evidence map.")
    lines.extend(
        [
            "",
            "## Next Verification Steps",
            "",
            "- Fill every `待补充` evidence source before drafting result claims.",
            "- Confirm whether data are real, simulated, prototype-level, or user-confirmed.",
            "- Use conservative wording for prototype and simulation evidence.",
            "- Run public-safety checks before committing generated materials.",
            "",
        ]
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an evidence-grounded thesis writing plan.")
    parser.add_argument("--profile", type=Path, help="JSON profile with title, thesis_type, topic_tags, and evidence.")
    parser.add_argument("--output", type=Path, required=True, help="Output Markdown plan path.")
    parser.add_argument("--title", help="Title override when no profile is supplied.")
    parser.add_argument(
        "--thesis-type",
        choices=sorted(THESIS_TYPES),
        help="Thesis type override when no profile is supplied.",
    )
    args = parser.parse_args()

    profile = load_profile(args.profile)
    if args.title:
        profile["title"] = args.title
    if args.thesis_type:
        profile["thesis_type"] = args.thesis_type
    write_plan(profile, args.output)
    print(f"plan={args.output}")


if __name__ == "__main__":
    main()
