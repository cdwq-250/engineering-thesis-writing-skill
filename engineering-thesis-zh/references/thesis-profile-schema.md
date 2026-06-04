# Thesis Profile Schema

Use this profile before running `scripts/generate_thesis_plan.py`. The profile
captures the user's thesis topic, thesis family, topic tags, and available
evidence. It is intentionally small so users can fill it during an interactive
planning conversation.

## JSON Fields

Required fields:

- `title`: thesis title or tentative title.
- `thesis_type`: one of `mechanical_manufacturing`, `control_optimization`,
  or `software_system`.
- `evidence`: list of evidence items.

Optional fields:

- `topic_tags`: list of corpus topic tags, such as `equipment_maintenance`,
  `production_scheduling`, `algorithm_modeling`, `lean_production`,
  `quality_management`, or `software_platform`.
- `constraints`: list of school, template, time, data, or format constraints.
- `known_gaps`: list of missing data, missing experiments, uncertain claims, or
  user decisions still needed.

Each evidence item supports:

- `claim`: the claim that the thesis may make.
- `source`: file path, experiment output, screenshot, document, or user
  confirmation backing the claim.
- `type`: one of `code`, `config`, `csv`, `test`, `figure`, `screenshot`,
  `document`, or `user_confirmation`.
- `allowed_wording`: conservative wording allowed by the evidence.

## Example

```json
{
  "title": "基于OEE的车间设备维护优化研究",
  "thesis_type": "mechanical_manufacturing",
  "topic_tags": ["equipment_maintenance", "production_scheduling"],
  "constraints": ["无真实部署数据，只能写案例和仿真验证"],
  "known_gaps": ["缺少维护成本历史记录"],
  "evidence": [
    {
      "claim": "原型验证表明设备维护流程可被规范化",
      "source": "outputs/maintenance_cases.csv",
      "type": "csv",
      "allowed_wording": "案例数据支持流程规范化分析"
    }
  ]
}
```

## Validation Rules

- `title` must be non-empty.
- `thesis_type` must match one supported type.
- `evidence` must be a list.
- Every evidence item should include `claim`.
- Strong claims need a concrete `source`.
- Unknown evidence `type` values should be corrected before plan generation.
- The validator reports warnings for missing `topic_tags`, `constraints`, and
  `known_gaps`; these are useful but not mandatory.

