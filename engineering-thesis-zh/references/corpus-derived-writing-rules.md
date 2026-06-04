# Corpus-Derived Writing Rules

Use this reference after reading `public_stats/corpus/progress_report.md` and
`public_stats/corpus/rule_candidates.md`. It converts aggregate structural
signals from the local thesis corpus into conservative writing guidance. It does
not contain source-paper prose.

## Evidence Basis

Current promoted guidance is based on aggregate structural metadata from 33
Chinese engineering graduate theses:

- 33 records analyzed.
- 0 parse errors.
- 26 mechanical/manufacturing-like records.
- 3 control/optimization-like records.
- 1 software/system-like record.
- 3 mixed records with tied classification signals.
- 29 records have high classification confidence, 1 has medium confidence,
  and 3 are ties.
- 6 records have weak heading extraction and should be checked manually before
  promoting fine-grained chapter rules.
- Common heading signals include `1.1`, `1.2`, `1.3`, `3.2`, `3.3`, `4.2`,
  `4.3`, `5.1`, and `5.2`.
- Common keyword signals include 精益生产, 设备管理, TPM, OEE, 设备维护,
  预防性维护, 生产管理, 全面质量管理, 5M1E, and 优化方案.
- Figure/table signals show substantially more figures than tables in the
  current corpus.

This sample is strongest for production, equipment, maintenance, quality,
manufacturing-management, and industrial optimization theses. It is large enough
to promote only abstract structure, evidence, and claim-boundary rules after
manual review. It is not large enough to claim a universal thesis template for
all Chinese engineering schools, and it is not balanced enough to generalize
software-system thesis rules.

## Shared Chapter Logic

Most engineering theses in this corpus follow a problem-to-method-to-validation
arc:

1. Introduce the engineering scene and problem.
2. Review background literature, tools, or management methods.
3. Diagnose the current object, process, equipment, model, or system.
4. Design an optimization, model, system, algorithm, or management scheme.
5. Verify the scheme through cases, experiments, comparison, simulation,
   prototype testing, or implementation evidence.
6. Summarize contributions, limitations, and future work.

When drafting a thesis, make every chapter answer a distinct question:

- Chapter 1: Why is this problem worth solving, and what exactly will this
  thesis do?
- Chapter 2: What theories, methods, technologies, and prior work define the
  solution space?
- Chapter 3: What is the current state or formal problem, and where is the
  gap?
- Chapter 4: What method, model, system, or scheme is designed to close the
  gap?
- Chapter 5: What evidence shows the design is valid within stated conditions?
- Final chapter: What was completed, what remains limited, and what can be
  improved next?

## Chapter 1 Rules

Use `1.1` for research background and significance. The corpus repeatedly uses
background sections to connect the thesis object to a concrete industrial,
equipment, production, maintenance, management, or scheduling problem.

Use `1.2` for domestic and international research status, literature review, or
related work. Do not write this section as a source list. Organize it by method
families, engineering objects, and unresolved gaps.

Use `1.3` for research content, methods, route, or thesis organization. End the
chapter with a precise work package list:

- object or system being studied
- problem to be diagnosed or modeled
- method, algorithm, system, or improvement scheme to be built
- validation route and measurable indicators

Forbidden moves:

- claiming novelty without comparing the actual method boundary
- saying the research has "important value" without naming the object, metric,
  or scenario
- promising deployment, industrialization, or efficiency gains before evidence
  exists

## 问题诊断 Rules

For production, maintenance, equipment, quality, and management topics, include
a diagnosis chapter before proposing a solution. The corpus signals show many
sections around current-state analysis, cause analysis, OEE/TPM/5M1E, quality
management, process inspection, and operational bottlenecks.

Diagnosis sections should separate:

- object description: company, workshop, line, equipment, process, system, or
  dataset
- current-state indicators: downtime, OEE, defect rate, waiting time, flow
  time, utilization, maintenance cost, customer satisfaction, or schedule delay
- cause structure: human, machine, material, method, environment, management,
  data, or process causes
- evidence source: questionnaire, interview, logs, historical records,
  simulated data, code output, or user-confirmed facts

Do not jump from "there is a problem" directly to "therefore this scheme is
effective". The thesis needs an explicit cause-to-scheme mapping.

## Design Chapter Rules

The design chapter should transform the diagnosis into an implementable method.
Use one of these patterns:

- software/system thesis: requirement analysis -> architecture -> module design
  -> database/interface/process design -> implementation evidence
- optimization/model thesis: assumptions -> parameters -> variables ->
  constraints -> objective -> algorithm or solution process
- production/maintenance thesis: current-state cause -> improvement principle ->
  policy/rule/process redesign -> implementation or simulation route

For every design item, specify:

- input data or triggering condition
- processing rule, model, algorithm, module, or management step
- output result or decision
- evidence needed for validation

Avoid decorative diagrams. Figures should explain architecture, process flow,
state transition, scheduling logic, maintenance decision flow, algorithm flow,
or value stream mapping.

## Validation Chapter Rules

The validation chapter should not be a narrative summary. It must bind claims to
observable evidence.

For software systems, use:

- test environment
- functional test cases
- boundary or exception tests
- screenshots, logs, database records, or API results

For optimization and scheduling, use:

- scenario or dataset source
- parameter settings
- baseline methods
- metrics and units
- repeated comparison, sensitivity analysis, or ablation when available

For production, equipment, maintenance, and quality topics, use:

- before/after indicators when real data exists
- simulated or case-study indicators when field data does not exist
- OEE, utilization, downtime, maintenance cost, defect rate, flow time,
  makespan, tardiness, or satisfaction indicators
- explanation of why the indicator matters operationally

Allowed wording depends on evidence:

- If evidence is simulated, say "在仿真场景下".
- If evidence is a prototype, say "原型验证表明".
- If evidence is a case calculation, say "案例计算结果显示".
- If there is no real deployment, do not say "实际应用证明" or "已投入运行".

## Figure And Table Rules

The current corpus has more figure signals than table signals, so engineering
thesis writing should plan figures early. Use figures to carry structure and
tables to carry parameters, indicators, and comparisons.

Minimum practical figure/table plan:

- Chapter 1: technical route or research framework figure when the school
  format permits it.
- Chapter 2: method taxonomy or theoretical framework only if it clarifies the
  literature logic.
- Chapter 3: current process, equipment state, value stream, problem tree, or
  cause analysis figure.
- Chapter 4: architecture, algorithm flow, process redesign, module structure,
  or maintenance decision flow figure.
- Chapter 5: result comparison chart plus parameter, test-case, or indicator
  table.

Every figure/table must answer one of these:

- What object is being analyzed?
- What process or model is being designed?
- What evidence supports a result claim?
- What comparison shows a difference under controlled conditions?

## Claim-Boundary Rules

Use conservative engineering claims:

- "降低了仿真场景下的平均延期时间" only when the metric is measured.
- "提高了设备管理流程的规范性" only when process rules, forms, or workflow
  evidence exist.
- "支持生产排程与维护策略联动" only when the model or system implements both
  sides.
- "为后续现场应用提供基础" when evidence is prototype or simulation level.

Avoid unsupported strong claims:

- "显著提升企业效益"
- "实现工业级应用"
- "达到国内领先水平"
- "全面解决设备维护问题"
- "证明算法最优"

## Writing Checklist

Before drafting or revising, check:

- Is the thesis family identified?
- Does Chapter 1 end with concrete research tasks?
- Does the literature review lead to a gap rather than a list?
- Does the diagnosis chapter provide evidence before proposing a scheme?
- Does the design chapter define inputs, process, outputs, and validation
  evidence?
- Does the validation chapter name metrics, baselines, parameters, and evidence
  source?
- Are all deployment, superiority, efficiency, and novelty claims supported?
- Are source-paper observations expressed only as abstract rules?
