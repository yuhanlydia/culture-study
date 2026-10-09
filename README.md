# Culture Study

面向 ACL 的跨文化小语言模型研究：CulturalBench＋BLEnD，冻结 1B／7B 模型，以数学优化问题研究文化条件答案决策与共享资源下的风险折中。

**研究包入口：[research/README.md](research/README.md)。** 当前交付包括数学主稿、真实基线代码与证据工具、完整原生基线设计和条件性候选比较。全部科学源码／设计仍为 generated_unexecuted，没有测试、模型实验或性能提升结果。

最新输入修订：已读 BLEnD 发布文件的 Question／Translation 内容与论文列说明相反，现已写入固定逐文化语言映射。先读 [原生证据资格](research/model/NATIVE_EVIDENCE_CONTRACT.md) 和 [Local 语言列接受](LOCAL_AGENT_RUNBOOK.md#native-language-column-repair)。源码未执行，旧绑定／prepared／run 不能充当此修订的验收。

## 数学、实现与实验

| 内容 | 阅读入口 | 当前资格 |
|---|---|---|
| 答案集合、文化内聚合与 Pareto 理想点 | [统一数学主稿](research/model/MODEL.md) | 对象／目标／约束／推导／求解与退化；作者条件性分析 |
| 共同偏差、相关性与遗漏支持 | [可靠性分析](research/model/RELIABILITY_AND_SUPPORT.md) | 新增代数推导，无原生效果结论 |
| 1B／7B 基线及数学到代码映射 | [实现索引](research/implementation/README.md)、[源码](culture_study) | 原生数据／模型／推理／评分／诊断接口已写；未验收 |
| 两个 benchmark 全部原生任务 | [ACL 实验协议](research/experiments/ACL_PROTOCOL.md)、[14-run 基线设计](research/EXPERIMENT_DESIGN.md) | 完整基线作者设计；候选 G01 未闭合 |

本轮修复 whole-label 概率计算的内存中间张量、补充合法标签条件概率与有限数值保护，并新增 [完整 native old/new 源码对照](culture_study/likelihood_audit.py)。它是基线证据工具，不是 J01 solver。

J01 的四个真假判断对应立方体的 16 个答案顶点；固定边际联合优化只适合实际联合空间。文化内 KL 聚合保留文化条件，Pareto 目标比较共享可行类内的文化风险。三个构造均未入选或实现为新方法；现有 admitted=0/20、selected=0/15。

## Local Codex: start here

在 [最新原生证据交付回执](research/native-evidence-delivery-receipt.json) 指定的确切 commit 阅读：

1. [AGENTS.md](AGENTS.md) 与 [LONG_TERM_TASK.md](LONG_TERM_TASK.md)。
2. [LOCAL_AGENT_RUNBOOK.md](LOCAL_AGENT_RUNBOOK.md)，包括 [固定来源获取](LOCAL_AGENT_RUNBOOK.md#exact-source-binding-and-acquisition)、[多语言 scorer 依赖](LOCAL_AGENT_RUNBOOK.md#multilingual-official-scorer-acquisition)、[新源码接受](LOCAL_AGENT_RUNBOOK.md#likelihood-memory-repair-and-native-source-audit)。
3. [rounds/r001/WEB_HANDOFF.md](rounds/r001/WEB_HANDOFF.md)。

Local 通过真实 SSH／native Conda／既有 admitted harness 验收与执行，保留旧 source_digest 的运行目录。实际主机路径、分配、GPU 型号／VRAM 和累计预算待恢复；不使用容器、不借用其他项目资源。HF 输出目的地未选，本轮只交付本 GitHub literal main。

## 原生版本与证据要求

CB 使用已锁定公开发布的 1,227 原题／4,908 Hard 行，正式论文 1,696 分母不混用。BLEnD 保留原始 16 cultures、完整 original SAQ 与 v1.1 MCQ 两分片。SAQ 用原生 SEM-B／SEM-W 和有效分母，不能换成自制 exact-match。

下一科学前提是可信 native baseline／强简单替代／scorer／逐题 census，以及合法非 test 开发与 fresh confirmation。test 不用于拟合、视角／参数／策略选择或标签检索。约20数学卡、完整审查／排名／前15、Parent／value／碰撞／IPCG和方法边界仍待完成；本轮不伪造 PASS。

## 历史与状态

- [原始 J01 讨论稿](rounds/r001/ANSWER_SET_OPTIMIZATION.md)、[J01 边界审查](research/math/J01_REVIEW.md)。
- [八项分析](research/math/OBJECTIVE_ANALYSIS.md)、[五类局部／整体模型](research/math/MULTICULTURAL_LOCAL_GLOBAL_REVIEW.md)、[精确决策／信息边界](research/math/DECISION_INFORMATION_BOUNDARIES.md)。
- [来源锁定](research/sources.lock.json)、[原生契约](research/NATIVE_CONTRACTS.md)、[近邻方法](research/CLOSEST_WORK.md)、[源码审查](research/CODE_REVIEW.md)。
- [进度与历史交付](research/PROGRESS.md)、[现有任务身份](research/background-task.json)、[工作 checkpoint](research/workflow-checkpoint.json)、[方法验证状态](research/METHOD_VERIFICATION_STATUS.md)。

后台配置、启动请求、实际作者交付与科学执行分别记录；同一任务续接，保留所有历史暂停／失败／未完成项。组织里程碑的提交成功不代表完整研究目标或新方法作者交付已完成。
