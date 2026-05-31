# Experiment Metric Summary

This report is generated from CSV files and is intended as thesis-writing evidence.
Interpretations are scenario-bound and must not be generalized beyond the actual experiment design.

## baseline.csv

- Rows: 5
- Columns: dispatch_rule, makespan, average_flow_time, total_tardiness, on_time_rate, failure_count, maintenance_count, preventive_maintenance_count, corrective_maintenance_count, maintenance_downtime, maintenance_cost, composite_objective, utilization
- Comparison key: dispatch_rule

| Metric | Best row | Best value | Thesis-safe interpretation |
|---|---|---:|---|
| `makespan` | dispatch_rule=EDD | 21 | In this scenario, dispatch_rule=EDD has the best makespan (lower is better). |
| `average_flow_time` | dispatch_rule=EDD | 16.5 | In this scenario, dispatch_rule=EDD has the best average_flow_time (lower is better). |
| `total_tardiness` | dispatch_rule=EDD | 0 | In this scenario, dispatch_rule=EDD has the best total_tardiness (lower is better). |
| `on_time_rate` | dispatch_rule=EDD | 1 | In this scenario, dispatch_rule=EDD has the best on_time_rate (higher is better). |
| `failure_count` | all compared rows | 0 | In this scenario, all compared rows have the same failure_count; do not claim a difference. |
| `maintenance_count` | all compared rows | 0 | In this scenario, all compared rows have the same maintenance_count; do not claim a difference. |
| `maintenance_downtime` | all compared rows | 0 | In this scenario, all compared rows have the same maintenance_downtime; do not claim a difference. |
| `maintenance_cost` | all compared rows | 0 | In this scenario, all compared rows have the same maintenance_cost; do not claim a difference. |
| `composite_objective` | dispatch_rule=EDD | 21 | In this scenario, dispatch_rule=EDD has the best composite_objective (lower is better). |
| `utilization` | dispatch_rule=EDD | 0.4226 | In this scenario, dispatch_rule=EDD has the best utilization (higher is better). |

## experiment_summary.csv

- Rows: 1
- Columns: dispatch_rule, maintenance_policy, makespan, average_flow_time, total_tardiness, on_time_rate, failure_count, maintenance_count, preventive_maintenance_count, corrective_maintenance_count, maintenance_downtime, maintenance_cost, composite_objective, utilization
- Comparison key: dispatch_rule, maintenance_policy

| Metric | Best row | Best value | Thesis-safe interpretation |
|---|---|---:|---|
| `makespan` | dispatch_rule=FIFO, maintenance_policy=CM_ONLY | 21.5 | In this scenario, dispatch_rule=FIFO, maintenance_policy=CM_ONLY has the best makespan (lower is better). |
| `average_flow_time` | dispatch_rule=FIFO, maintenance_policy=CM_ONLY | 18.17 | In this scenario, dispatch_rule=FIFO, maintenance_policy=CM_ONLY has the best average_flow_time (lower is better). |
| `total_tardiness` | dispatch_rule=FIFO, maintenance_policy=CM_ONLY | 3.5 | In this scenario, dispatch_rule=FIFO, maintenance_policy=CM_ONLY has the best total_tardiness (lower is better). |
| `on_time_rate` | dispatch_rule=FIFO, maintenance_policy=CM_ONLY | 0.6667 | In this scenario, dispatch_rule=FIFO, maintenance_policy=CM_ONLY has the best on_time_rate (higher is better). |
| `failure_count` | dispatch_rule=FIFO, maintenance_policy=CM_ONLY | 0 | In this scenario, dispatch_rule=FIFO, maintenance_policy=CM_ONLY has the best failure_count (lower is better). |
| `maintenance_count` | dispatch_rule=FIFO, maintenance_policy=CM_ONLY | 0 | In this scenario, dispatch_rule=FIFO, maintenance_policy=CM_ONLY has the best maintenance_count (lower is better). |
| `maintenance_downtime` | dispatch_rule=FIFO, maintenance_policy=CM_ONLY | 0 | In this scenario, dispatch_rule=FIFO, maintenance_policy=CM_ONLY has the best maintenance_downtime (lower is better). |
| `maintenance_cost` | dispatch_rule=FIFO, maintenance_policy=CM_ONLY | 0 | In this scenario, dispatch_rule=FIFO, maintenance_policy=CM_ONLY has the best maintenance_cost (lower is better). |
| `composite_objective` | dispatch_rule=FIFO, maintenance_policy=CM_ONLY | 301.5 | In this scenario, dispatch_rule=FIFO, maintenance_policy=CM_ONLY has the best composite_objective (lower is better). |
| `utilization` | dispatch_rule=FIFO, maintenance_policy=CM_ONLY | 0.4128 | In this scenario, dispatch_rule=FIFO, maintenance_policy=CM_ONLY has the best utilization (higher is better). |

## maintenance_compare.csv

- Rows: 4
- Columns: maintenance_policy, makespan, average_flow_time, total_tardiness, on_time_rate, failure_count, maintenance_count, preventive_maintenance_count, corrective_maintenance_count, maintenance_downtime, maintenance_cost, composite_objective, utilization
- Comparison key: maintenance_policy

| Metric | Best row | Best value | Thesis-safe interpretation |
|---|---|---:|---|
| `makespan` | all compared rows | 21 | In this scenario, all compared rows have the same makespan; do not claim a difference. |
| `average_flow_time` | all compared rows | 16.5 | In this scenario, all compared rows have the same average_flow_time; do not claim a difference. |
| `total_tardiness` | all compared rows | 0 | In this scenario, all compared rows have the same total_tardiness; do not claim a difference. |
| `on_time_rate` | all compared rows | 1 | In this scenario, all compared rows have the same on_time_rate; do not claim a difference. |
| `failure_count` | all compared rows | 0 | In this scenario, all compared rows have the same failure_count; do not claim a difference. |
| `maintenance_count` | all compared rows | 0 | In this scenario, all compared rows have the same maintenance_count; do not claim a difference. |
| `maintenance_downtime` | all compared rows | 0 | In this scenario, all compared rows have the same maintenance_downtime; do not claim a difference. |
| `maintenance_cost` | all compared rows | 0 | In this scenario, all compared rows have the same maintenance_cost; do not claim a difference. |
| `composite_objective` | all compared rows | 21 | In this scenario, all compared rows have the same composite_objective; do not claim a difference. |
| `utilization` | all compared rows | 0.4226 | In this scenario, all compared rows have the same utilization; do not claim a difference. |

## maintenance_summary.csv

- Rows: 4
- Columns: station_id, equipment_id, failure_count, maintenance_count, preventive_maintenance_count, corrective_maintenance_count, maintenance_downtime
- Comparison key: station_id

| Metric | Best row | Best value | Thesis-safe interpretation |
|---|---|---:|---|
| `failure_count` | all compared rows | 0 | In this scenario, all compared rows have the same failure_count; do not claim a difference. |
| `maintenance_count` | all compared rows | 0 | In this scenario, all compared rows have the same maintenance_count; do not claim a difference. |
| `maintenance_downtime` | all compared rows | 0 | In this scenario, all compared rows have the same maintenance_downtime; do not claim a difference. |

## order_summary.csv

- Rows: 3
- Columns: order_id, due_date, priority, completion_time, flow_time, tardiness
- Comparison key: order_id

| Metric | Best row | Best value | Thesis-safe interpretation |
|---|---|---:|---|
| `completion_time` | order_id=UAV-001 | 14 | In this scenario, order_id=UAV-001 has the best completion_time (lower is better). |
| `flow_time` | order_id=UAV-001 | 14 | In this scenario, order_id=UAV-001 has the best flow_time (lower is better). |
| `tardiness` | order_id=UAV-001 | 0 | In this scenario, 2 rows tie for the best tardiness (lower is better); discuss the tie. |

## sensitivity_analysis.csv

- Rows: 4
- Columns: degradation_per_hour, makespan, average_flow_time, total_tardiness, on_time_rate, failure_count, maintenance_count, preventive_maintenance_count, corrective_maintenance_count, maintenance_downtime, maintenance_cost, composite_objective, utilization
- Comparison key: degradation_per_hour

| Metric | Best row | Best value | Thesis-safe interpretation |
|---|---|---:|---|
| `makespan` | all compared rows | 21 | In this scenario, all compared rows have the same makespan; do not claim a difference. |
| `average_flow_time` | all compared rows | 16.5 | In this scenario, all compared rows have the same average_flow_time; do not claim a difference. |
| `total_tardiness` | all compared rows | 0 | In this scenario, all compared rows have the same total_tardiness; do not claim a difference. |
| `on_time_rate` | all compared rows | 1 | In this scenario, all compared rows have the same on_time_rate; do not claim a difference. |
| `failure_count` | all compared rows | 0 | In this scenario, all compared rows have the same failure_count; do not claim a difference. |
| `maintenance_count` | all compared rows | 0 | In this scenario, all compared rows have the same maintenance_count; do not claim a difference. |
| `maintenance_downtime` | all compared rows | 0 | In this scenario, all compared rows have the same maintenance_downtime; do not claim a difference. |
| `maintenance_cost` | all compared rows | 0 | In this scenario, all compared rows have the same maintenance_cost; do not claim a difference. |
| `composite_objective` | all compared rows | 21 | In this scenario, all compared rows have the same composite_objective; do not claim a difference. |
| `utilization` | all compared rows | 0.4226 | In this scenario, all compared rows have the same utilization; do not claim a difference. |

## station_summary.csv

- Rows: 4
- Columns: station_id, station_type, final_health, operating_time, utilization
- Comparison key: station_id, station_type

| Metric | Best row | Best value | Thesis-safe interpretation |
|---|---|---:|---|
| `utilization` | station_id=E1, station_type=electronics | 0.5116 | In this scenario, station_id=E1, station_type=electronics has the best utilization (higher is better). |
