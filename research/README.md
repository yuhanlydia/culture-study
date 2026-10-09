# 研究包阅读入口

目标：在 CulturalBench 与 BLEnD 的原生任务上，研究冻结 1B／7B 语言模型的文化条件答案决策与共享资源下的文化风险折中。

本入口整理现有材料，不移动或覆盖历史推导。数学论证、代码生成、软件验收、原生实验与论文结论分别记录。

## 建议阅读顺序

| 顺序 | 文件 | 内容与当前状态 |
|---|---|---|
| 1 | [统一数学主稿](model/MODEL.md) | 对象、目标、约束、推导、求解与适用边界；作者条件性分析 |
| 2 | [偏差、相关性与支持覆盖](model/RELIABILITY_AND_SUPPORT.md) | 同文化聚合为何也可能失败；新增代数分析，无实测 |
| 3 | [实现与数学映射](implementation/README.md) | 现有 1B／7B 基线源码、内存修复、未实现候选及验收条件 |
| 4 | [实验与 ACL 证据方案](experiments/ACL_PROTOCOL.md) | 两个 benchmark 的完整覆盖、必要比较、统计与漏项；候选部分为条件性设计 |
| 5 | [运行手册](../LOCAL_AGENT_RUNBOOK.md) | 真实输入获取、固定版本、已存在 CLI、原生评分与日志返回 |
| 6 | [当前交接](../rounds/r001/WEB_HANDOFF.md) | 按实际交付 commit 开始 Local 验收 |

当前来源修订：[原生语言、提示与证据资格](model/NATIVE_EVIDENCE_CONTRACT.md)；
[逐文件读取记录](sources/NATIVE_VIEW_AUDIT.json)。它修复实际发布列绑定，并推导条件漂移进入几何池化、联合矩逐对可行但整体不可行的边界。不是新候选或效果结论。

## 历史与来源

- [原始答案集合优化 J01](../rounds/r001/ANSWER_SET_OPTIMIZATION.md)、[J01 审查](math/J01_REVIEW.md)。
- [五类局部／整体模型](math/MULTICULTURAL_LOCAL_GLOBAL_REVIEW.md)、[精确决策边界与联合可识别性](math/DECISION_INFORMATION_BOUNDARIES.md)。
- [八项早期分析](math/OBJECTIVE_ANALYSIS.md)、[原生契约](NATIVE_CONTRACTS.md)、[固定来源](sources.lock.json)。
- [相关方法](CLOSEST_WORK.md)、[来源快照](math/MULTICULTURAL_SOURCE_SNAPSHOT.json)、[完整基线设计](EXPERIMENT_DESIGN.md)。

## 状态

已有源码是完整的基线／评分／残余失败诊断作者实现，仍为 generated_unexecuted。J01、LOCAL02、PARETO03 是未入选的讨论构造；DRO04、OT05 是已知比较框架。尚无新方法实现、原生小模型结果、合格 20→15 池或已通过的科学 gate。

先完成独立数学与源码整理；新增候选投资继续依赖原生逐题证据、开发／确认隔离与方法验证。不得把本索引解释为任务已经全部完成。
