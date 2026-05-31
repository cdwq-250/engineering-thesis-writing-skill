# UAV Experiment Section Draft

This draft demonstrates how `engineering-thesis-zh` turns project CSV metrics into conservative Chinese thesis prose. It is a writing example, not a final manuscript section.

## 6.2 调度规则对比实验分析

为比较不同调度规则在无人机装配仿真场景中的表现，实验选取 FIFO、EDD、SPT、CR 和 ATCS 五种规则作为对比对象，并从完工时间、平均流动时间、总延期时间、准时率、综合目标值和工位利用率等指标进行评价。由 `baseline.csv` 可知，在当前订单集合和参数设置下，EDD 规则的完工时间为 21.0，平均流动时间为 16.5，总延期时间为 0，准时率为 1.0，综合目标值为 21.0，在交期相关指标和综合目标值上表现较优。该结果说明，在本文设定的交期约束场景中，优先考虑最早交期有助于降低订单延期风险，并使综合目标值保持较低水平。

FIFO 与 SPT 在本组实验中的完工时间均为 21.5，平均流动时间均为 18.1667，总延期时间均为 3.5，综合目标值均为 301.5；CR 与 ATCS 的完工时间均为 26.5，总延期时间均为 8.5，综合目标值均为 706.5。上述结果表明，不同调度规则对订单完成顺序和交期满足情况具有直接影响。不过，本实验中的故障次数、维护次数、维护停机时间和维护成本在各调度规则下均为 0，因此不能据此说明调度规则对设备维护行为产生了差异性影响。

## 6.3 维护策略对比实验分析

维护策略对比实验包括故障后维护、基于运行时间的预防性维护、基于健康阈值的维护以及瓶颈工位优先维护等策略。由 `maintenance_compare.csv` 可知，在当前实验参数下，四类维护策略的完工时间、平均流动时间、总延期时间、准时率、维护次数、维护停机时间、维护成本、综合目标值和利用率等指标完全相同。其中，完工时间均为 21.0，平均流动时间均为 16.5，总延期时间均为 0，准时率均为 1.0。

该结果说明，在当前退化参数和订单规模下，设备健康状态尚未触发故障维修或预防性维护过程，因此不同维护策略没有表现出可观测差异。论文写作中应将该结果解释为“当前参数下维护压力不足”，而不能写成某一种维护策略优于其他策略。若要进一步比较维护策略，需要在后续实验中提高退化速率、延长仿真周期、增加订单规模，或设置更严格的健康阈值，使维护触发机制能够进入有效对比区间。

## 6.4 敏感性分析

敏感性分析改变了设备单位加工时间退化率，取值包括 0.02、0.04、0.06 和 0.08。由 `sensitivity_analysis.csv` 可知，在上述参数范围内，完工时间均为 21.0，平均流动时间均为 16.5，总延期时间均为 0，准时率均为 1.0，故障次数和维护次数均为 0，综合目标值均为 21.0。说明在当前订单规模和仿真周期下，退化率变化尚未传导为故障或维护事件，系统主要受调度顺序和工艺流程约束影响。

因此，本组敏感性分析的合理结论不是“系统对退化率不敏感”，而是“在当前参数范围内尚未观察到由退化率变化引起的指标差异”。后续若要验证设备退化对生产维护协同的影响，应扩大退化参数范围或增加高负载场景，使设备健康状态能够跨越维护触发阈值。

## 6.5 订单与工位结果分析

由 `order_summary.csv` 可知，UAV-001 的完成时间和流动时间均为 14.0，在三项订单中最短；UAV-001 和 UAV-003 的延期时间均为 0，说明两项订单在设定交期内完成，而 UAV-002 的延期时间为 3.5，构成当前场景中的主要延期来源。该结果可用于解释调度规则评价中总延期时间的来源，并为后续优化订单排序提供依据。

由 `station_summary.csv` 可知，电子装配工位 E1 的利用率为 0.5116，在四个工位中最高；装配工位 A1、测试工位 T1 和检验工位 I1 的利用率分别为 0.4651、0.3953 和 0.2791。该结果表明，不同工位在当前工艺路线中的负载水平并不一致，电子装配工位承担了相对更高的加工压力。后续在扩展模型时，可结合工位利用率与设备健康状态设计瓶颈工位维护或动态调度策略。

## Writing Boundaries

- Do not claim field deployment or real factory validation.
- Do not claim maintenance policies are superior in the current parameter setting.
- Do not claim degradation sensitivity when all compared rows have identical metrics.
- Do not claim trained reinforcement-learning or multi-agent optimization from placeholder interfaces.
- Keep all conclusions bound to the simulated scenario and current parameters.
