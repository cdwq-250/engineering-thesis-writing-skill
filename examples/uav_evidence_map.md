# UAV Thesis Evidence Map

This evidence map validates `engineering-thesis-zh` against the local UAV digital-twin maintenance-optimization project. It is a public, non-copyright artifact: it records project evidence types and writing boundaries rather than thesis prose.

## Thesis Type

Primary type: control/optimization thesis with mechanical/manufacturing application context.

Secondary type: software/simulation prototype thesis.

## Chapter Evidence

| Thesis chapter | Supported content | Evidence sources | Allowed wording | Forbidden wording |
|---|---|---|---|---|
| 绪论 | UAV assembly, production scheduling, equipment health, maintenance pressure, digital-twin simulation value | Project README, thesis draft outline, experiment plan | "面向无人机装配产线的仿真原型" | "已在真实工厂部署" |
| 相关理论基础 | Digital twin, discrete-event simulation, scheduling rules, maintenance policies, multi-objective evaluation | `docs/thesis_framework.md`, `docs/model_assumptions.md`, source module names | "为模型设计提供理论基础" | "提出完整工业级数字孪生平台" |
| 问题建模与模型假设 | Orders, process steps, stations, equipment health degradation, maintenance triggers, objective metrics | `src/order.py`, `src/process.py`, `src/workstation.py`, `src/equipment.py`, `src/config.py`, `docs/model_assumptions.md` | "在设定仿真假设下建模" | "基于真实现场采集数据建模" |
| 仿真模型设计 | Scheduling, maintenance, simulation event flow, metric collection, visualization | `src/scheduler.py`, `src/maintenance.py`, `src/simulation.py`, `src/simpy_foundation.py`, `src/metrics.py`, `src/visualization.py` | "实现规则驱动的仿真流程" | "完成多智能体强化学习训练" |
| 仿真系统实现 | Python modules, command-line entry, CSV export, figure export, SimPy-compatible foundation | `main.py`, `requirements.txt`, `src/*.py` | "实现可运行实验原型" | "实现生产级平台服务" |
| 实验设计与结果分析 | Baseline scheduling, maintenance comparison, sensitivity analysis, order/station/maintenance summaries | `experiments/*.py`, `results/csv/*.csv`, `results/figures/*.png` | "在本实验参数下比较策略表现" | "显著优于所有同类方法" |
| 测试与验证 | Scheduler names, maintenance policy names, metrics, CSV/figure output, SimPy event log | `tests/test_mvp_contract.py`, `tests/test_simpy_foundation.py`, `python -m pytest` result | "测试覆盖核心合同和输出流程" | "通过工业验收测试" |
| 总结与展望 | Completed simulation prototype, limitations, future sensor data, calibration, expanded policies | README, assumptions, experiment plan | "为后续数据接入和策略扩展提供基础" | "已形成可直接推广的生产优化系统" |

## Metrics Available For Experiment Writing

The existing CSV outputs support discussion of:

- `makespan`
- `average_flow_time`
- `total_tardiness`
- `on_time_rate`
- `failure_count`
- `maintenance_count`
- `preventive_maintenance_count`
- `corrective_maintenance_count`
- `maintenance_downtime`
- `maintenance_cost`
- `composite_objective`
- `utilization`

These metrics may be discussed only in relation to the generated experiment scenario and parameter settings.

## Verified Local Test Evidence

The local project test suite collected 7 tests and all passed. This supports claims about prototype-level correctness for:

- scheduling rule names
- maintenance rule names
- core metric keys
- CSV and figure output creation
- SimPy-style order generation, operation completion, failure repair, and event logging

## Recommended Figures

- System/simulation architecture diagram based on source modules.
- Process/event flow diagram based on `src/simulation.py` and `src/simpy_foundation.py`.
- Maintenance state transition diagram based on equipment health and maintenance policies.
- Strategy comparison charts from `results/csv/baseline.csv` and `results/csv/maintenance_compare.csv`.
- Sensitivity analysis chart from `results/csv/sensitivity_analysis.csv`.

## Unsupported Claims To Remove Or Weaken

- Real factory deployment.
- Real sensor-data integration.
- Field-calibrated degradation parameters.
- Completed reinforcement-learning or multi-agent training.
- Production-grade digital-twin platform.
- Statistical superiority without repeated trials or significance tests.
- Large-scale concurrency or real-time performance.

