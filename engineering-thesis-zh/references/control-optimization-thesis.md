# Control And Optimization Thesis Pattern

Use this reference for theses centered on control strategy, scheduling, simulation, optimization algorithms, prediction, or decision-making models.

## Common Chapter Pattern

1. 绪论：工程场景、决策问题、研究价值、国内外研究现状、研究路线。
2. 理论基础：控制理论、优化模型、仿真方法、评价指标、相关算法基础。
3. 问题建模：集合、参数、变量、约束、目标函数、假设条件。
4. 算法或策略设计：基线规则、改进策略、算法流程、复杂度或收敛性讨论。
5. 实验设计：数据集或生成场景、参数设置、对比方法、评价指标。
6. 结果分析：基线对比、消融或敏感性分析、工程解释、局限性。
7. 总结与展望。

## Evidence Rules

- Every formula must map to implemented parameters, documented assumptions, or cited theory.
- Every metric discussed must appear in experiment output, logs, tests, CSV files, or reproducible scripts.
- If experiments use synthetic or simulated data, state that clearly.
- Do not describe a placeholder reinforcement-learning or multi-agent interface as a completed trained policy.
- Do not claim algorithm superiority unless comparisons, metric definitions, and repeated or controlled experiments support it.

## Writing Style

- Define symbols before using them.
- Separate “模型假设”“优化目标”“约束条件”“算法流程”。
- Discuss limitations: data realism, parameter calibration, scenario coverage, computation cost, and deployment boundary.
