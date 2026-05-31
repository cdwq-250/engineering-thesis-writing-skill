# UAV Maintenance Optimization Validation Brief

This public brief describes a local validation case for `engineering-thesis-zh`.
It does not include copyrighted thesis-source material.

## Project Type

Mechanical/manufacturing application thesis with control and optimization elements.

## Available Evidence

- Source code modules for configuration, equipment, maintenance policy, scheduling, simulation, metrics, and visualization.
- Experiment CSV outputs for baseline scheduling, maintenance-policy comparison, sensitivity analysis, station summary, order summary, and maintenance summary.
- Figures generated from simulation outputs.
- Automated tests covering scheduler rule names, maintenance rule names, metrics, CSV/figure export, and SimPy-style simulation.

## Verified Test Result

`python -m pytest` in the local UAV project collected 7 tests and all passed.

## Thesis Writing Uses

This case can validate whether the skill can:

- generate a graduate-thesis outline from real project evidence
- map claims to code, tests, CSV files, and figures
- write an experiment chapter from metrics such as makespan, average flow time, tardiness, on-time rate, failure count, maintenance count, downtime, cost, objective value, and utilization
- distinguish simulated assumptions from real factory deployment
- reject unsupported claims about field data, production deployment, or trained reinforcement-learning policies

See `examples/uav_evidence_map.md` for the chapter-by-chapter evidence map.
