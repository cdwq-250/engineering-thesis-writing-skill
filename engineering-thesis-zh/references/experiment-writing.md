# Experiment Chapter Writing

Use this reference whenever writing or revising an experiment chapter.

## Required Elements

- Experiment purpose.
- Environment and dependency versions when relevant.
- Scenario or dataset source.
- Parameter settings.
- Baseline methods.
- Evaluation metrics.
- Reproducible command or script.
- Result table/figure.
- Analysis tied to observed values.
- Limitations.

## Evidence Checklist

Before writing a result sentence, verify:

- The metric exists in CSV, logs, images, tests, or notebook output.
- The comparison method was actually run.
- The direction of improvement is correct.
- The result is not overgeneralized beyond the scenario.

## Safe Wording

- Use "在设定仿真场景下" for simulated experiments.
- Use "结果表明该策略在本实验参数下..." rather than universal claims.
- Use "功能验证" when the test is scenario-based rather than statistically rigorous.
- Use "敏感性分析" only when parameters were intentionally varied.

## Unsafe Wording

Avoid:

- "显著优于" without statistical evidence.
- "适用于所有..." without broad validation.
- "工业现场验证" without field data.
- "实时优化" unless runtime constraints and measurements exist.

