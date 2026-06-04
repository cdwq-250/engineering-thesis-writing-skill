#!/usr/bin/env python
"""Generate a conservative thesis manuscript skeleton from a thesis profile."""

from __future__ import annotations

import argparse
from pathlib import Path

from generate_thesis_plan import THESIS_TYPES, load_profile, normalize_evidence
from validate_thesis_profile import validate_profile


SECTION_PROMPTS = {
    "绪论": "写清工程背景、研究对象、问题来源、研究意义、研究内容和技术路线。",
    "理论": "只写与本课题方法、指标和验证直接相关的理论基础。",
    "综述": "按方法和问题类型组织国内外研究现状，最后收束到本文缺口。",
    "现状": "描述研究对象、流程、数据来源和现有问题，先给证据再下判断。",
    "问题": "把问题与原因、指标、场景对应起来，避免直接跳到方案有效。",
    "模型": "定义假设、参数、变量、目标、约束、输入输出和适用边界。",
    "方案": "说明设计目标、核心流程、策略规则、实施步骤和预期验证方式。",
    "设计": "说明架构、模块、流程、数据、接口或算法步骤。",
    "实验": "列出数据来源、参数设置、基线方法、指标定义和结果分析方式。",
    "验证": "只写有证据支持的验证结论，区分仿真、案例、原型和真实部署。",
    "测试": "写测试环境、测试用例、预期结果、实际结果和截图/日志证据。",
    "总结": "总结已完成工作，明确局限性和后续工作。",
}


def prompt_for(section: str) -> str:
    for key, prompt in SECTION_PROMPTS.items():
        if key in section:
            return prompt
    return "围绕本节标题写作，所有结论必须绑定证据来源。"


def evidence_summary(profile: dict) -> list[str]:
    evidence = normalize_evidence(list(profile.get("evidence", [])))
    if not evidence:
        return ["- 待补充证据：请先填写 thesis profile 的 `evidence[]`。"]
    lines = []
    for item in evidence:
        source = item.source or "待补充"
        wording = item.allowed_wording or "按证据强度保守表述"
        lines.append(f"- {item.claim or '待填写'} | {source} | {item.evidence_type} | {wording}")
    return lines


def write_skeleton(profile: dict, output: Path) -> None:
    thesis_type = str(profile.get("thesis_type", "mechanical_manufacturing"))
    if thesis_type not in THESIS_TYPES:
        thesis_type = "mechanical_manufacturing"
    spec = THESIS_TYPES[thesis_type]
    title = str(profile.get("title", "待定题目"))
    constraints = [str(item) for item in profile.get("constraints", [])]
    known_gaps = [str(item) for item in profile.get("known_gaps", [])]

    lines = [
        f"# {title}",
        "",
        "> Draft skeleton generated from corpus-grounded rules. Replace placeholders only with verified project evidence.",
        "",
        "## 摘要",
        "",
        "[待写：研究背景、问题、方法、验证方式、主要结论。不得写无证据的效率提升或部署结论。]",
        "",
        "## 关键词",
        "",
        "[待写：3-5个关键词，优先来自研究对象、方法、指标和场景。]",
        "",
        "## Evidence Register",
        "",
        "| Claim | Source | Type | Allowed Wording |",
        "|---|---|---|---|",
    ]
    for item in evidence_summary(profile):
        if item.startswith("- "):
            parts = [part.strip() for part in item[2:].split("|")]
            if len(parts) == 4:
                lines.append(f"| {parts[0]} | {parts[1]} | {parts[2]} | {parts[3]} |")
            else:
                lines.append(f"| {item[2:]} | 待补充 | user_confirmation | 只能写为待验证问题 |")
    lines.extend(["", "## Writing Constraints", ""])
    if constraints:
        lines.extend([f"- {constraint}" for constraint in constraints])
    else:
        lines.append("- 待补充学校模板、数据边界、实验边界和格式要求。")
    lines.extend(["", "## Known Gaps", ""])
    if known_gaps:
        lines.extend([f"- {gap}" for gap in known_gaps])
    else:
        lines.append("- 待补充缺失数据、缺失实验、缺失图表或待确认结论。")
    lines.extend(["", "## Main Text", ""])

    for chapter, sections in spec["chapters"]:
        lines.extend([f"## {chapter}", ""])
        for section in sections:
            lines.extend(
                [
                    f"### {section}",
                    "",
                    f"[写作任务] {prompt_for(section)}",
                    "",
                    "[证据要求] 写作前列出本节可用证据；没有证据时只能写问题、方法或计划，不能写结果。",
                    "",
                    "[禁止] 不得使用“显著提升”“工业级应用”“国内领先”“全面解决”“最优”等无证据强表述。",
                    "",
                ]
            )

    lines.extend(
        [
            "## Pre-Delivery Check",
            "",
            "- 每个结果 claim 都能回到 Evidence Register。",
            "- 仿真、案例、原型、真实部署边界已经明确。",
            "- 所有图表都有来源、单位、指标含义或截图/日志证据。",
            "- 没有复制语料论文原文。",
            "",
        ]
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a thesis manuscript skeleton from a profile.")
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--validate-profile", action="store_true")
    args = parser.parse_args()

    profile = load_profile(args.profile)
    if args.validate_profile:
        errors, warnings = validate_profile(profile)
        for warning in warnings:
            print(f"warning:{warning}")
        if errors:
            for error in errors:
                print(f"error:{error}")
            raise SystemExit(1)
    write_skeleton(profile, args.output)
    print(f"skeleton={args.output}")


if __name__ == "__main__":
    main()
