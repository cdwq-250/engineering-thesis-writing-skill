#!/usr/bin/env python
"""Write a focused interview checklist for building a thesis profile."""

from __future__ import annotations

import argparse
from pathlib import Path


COMMON_QUESTIONS = [
    ("题目", "暂定论文题目是什么？如果还不确定，给出研究对象、方法、场景三个关键词。"),
    ("学校要求", "是否有学校模板、章节数量、字数、查重/AIGC、图表格式或参考文献格式要求？"),
    ("真实材料", "已有材料有哪些：代码、配置、CSV、实验日志、截图、工厂记录、访谈、问卷、设计图、初稿？"),
    ("证据边界", "哪些结果来自真实数据，哪些来自仿真/案例/原型，哪些只是设想？"),
    ("风险 claim", "是否想写效率提升、成本降低、最优、部署应用等强结论？对应证据在哪里？"),
    ("缺口", "目前最缺什么：数据、实验、图、参考文献、章节结构、系统截图、指标解释？"),
]

TYPE_QUESTIONS = {
    "mechanical_manufacturing": [
        ("对象", "研究对象是设备、产线、车间、工艺、维护流程、质量流程，还是生产管理流程？"),
        ("现状指标", "现状有哪些可量化指标：OEE、停机时间、维护成本、缺陷率、利用率、延期时间、产量？"),
        ("问题诊断", "问题原因如何归类：人、机、料、法、环、测、管理、数据，或 TPM/OEE/5M1E/鱼骨图？"),
        ("方案", "准备设计什么：维护策略、点检流程、排程模型、质量改进方案、仿真系统、原型系统？"),
        ("验证", "能做哪些验证：前后对比、案例计算、仿真、敏感性分析、专家确认、流程试运行？"),
    ],
    "control_optimization": [
        ("场景", "优化对象是什么：调度、路径、维护策略、库存、控制参数、预测模型？"),
        ("模型", "集合、参数、变量、目标函数、约束条件和假设是否已有？"),
        ("数据", "数据来自真实记录、公开数据集、仿真生成，还是人工构造场景？"),
        ("基线", "对比方法是什么：规则策略、传统算法、现有流程、无优化方案，还是文献算法？"),
        ("指标", "评价指标是什么：makespan、tardiness、flow time、cost、utilization、runtime、accuracy？"),
    ],
    "software_system": [
        ("业务流程", "系统服务的业务流程是什么？用户角色、输入、输出和异常路径分别是什么？"),
        ("代码证据", "核心代码、接口、数据库表、配置、部署脚本、测试用例分别在哪里？"),
        ("模块", "系统模块如何划分？每个模块解决哪个业务问题？"),
        ("测试", "已有测试证据是什么：功能用例、边界用例、接口返回、截图、日志、数据库记录？"),
        ("边界", "系统是原型、本地运行、内网试用，还是正式部署？不能无证据写上线运行。"),
    ],
}


def write_questions(thesis_type: str, output: Path) -> None:
    questions = TYPE_QUESTIONS[thesis_type]
    lines = [
        "# Thesis Profile Interview",
        "",
        f"- Thesis type: `{thesis_type}`",
        "- Goal: collect enough evidence to generate `thesis-profile.json`, run `validate_thesis_profile.py`, then run `generate_thesis_plan.py`.",
        "",
        "## Common Questions",
        "",
    ]
    for label, question in COMMON_QUESTIONS:
        lines.append(f"- **{label}**: {question}")
    lines.extend(["", "## Type-Specific Questions", ""])
    for label, question in questions:
        lines.append(f"- **{label}**: {question}")
    lines.extend(
        [
            "",
            "## Output Profile Fields",
            "",
            "- `title`",
            f"- `thesis_type`: `{thesis_type}`",
            "- `topic_tags`",
            "- `constraints`",
            "- `known_gaps`",
            "- `evidence[]`: each item should include `claim`, `source`, `type`, and `allowed_wording`",
            "",
            "## Stop Conditions",
            "",
            "- Do not draft result claims until every strong claim has a concrete evidence source.",
            "- Do not claim deployment or field application unless the user provides deployment evidence.",
            "- Do not treat simulated data as real factory data.",
            "",
        ]
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a thesis-profile interview checklist.")
    parser.add_argument("--thesis-type", choices=sorted(TYPE_QUESTIONS), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    write_questions(args.thesis_type, args.output)
    print(f"questions={args.output}")


if __name__ == "__main__":
    main()
