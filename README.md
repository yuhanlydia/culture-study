# Culture Study

面向 ACL 的跨文化小语言模型研究：CulturalBench + BLEnD，1B–7B，按数学优化问题研究具体失败机制。

当前交付的是 **来源与数学审查，以及原生基线/评分核查/失败诊断的完整作者代码**。所有科学代码与设计均为 `generated_unexecuted`；没有执行测试、模型、训练、评分或 benchmark，没有性能提升结论。

## 研究材料

- [目标与完成判据](LONG_TERM_TASK.md)、[协作与执行边界](AGENTS.md)、[当前进度](research/PROGRESS.md)
- [版本与逐文件来源锁定](research/sources.lock.json)、[来源审查](research/SOURCE_AUDIT.md)、[原生评分契约](research/NATIVE_CONTRACTS.md)
- [当前相关方法与碰撞](research/CLOSEST_WORK.md)、[八项数学推导](research/math/OBJECTIVE_ANALYSIS.md)
- [数学优化要求](research/MATHEMATICAL_MODEL_BRIEF.md)、[J01 答案集合优化讨论稿](rounds/r001/ANSWER_SET_OPTIMIZATION.md)、[J01 审查与一阶扰动推导](research/math/J01_REVIEW.md)、[该讨论的补充来源](rounds/r001/SOURCE_AUDIT.md)
- [Parent Problem 草稿](research/PARENT_PROBLEM_DRAFT.md)、[方法验证状态](research/METHOD_VERIFICATION_STATUS.md)

J01 未入选；新审查补充了固定边际投影的一阶作用与 MAP 不变边界，并指出单标签参考分布不能直接沿用独立 Bernoulli 乘积。已知数学与既有机制不计为原创候选。尚无合格约20候选池、完整排名/前15选择或新方法批准。

## 代码、设计和本地交接

- [完整基线源码](culture_study)：真实版本获取/校验、完整原生数据准备、直接生成与完整标签概率、官方 BLEnD 函数桥接、SAQ live parity、日志续跑和残余失败输出
- [固定模型/任务/生成配置](configs/prelude.json)、[环境](environment.yml)、[静态代码审查](research/CODE_REVIEW.md)
- [两个模型类、全部原生任务的诊断实验设计](research/EXPERIMENT_DESIGN.md)
- [LOCAL_AGENT_RUNBOOK.md](LOCAL_AGENT_RUNBOOK.md)，含[真实输入获取与固定版本](LOCAL_AGENT_RUNBOOK.md#exact-source-binding-and-acquisition)、[多语言官方评分依赖](LOCAL_AGENT_RUNBOOK.md#multilingual-official-scorer-acquisition)、顺序命令/日志/有限修复/验收
- [首轮 WEB_HANDOFF](rounds/r001/WEB_HANDOFF.md)

CulturalBench 采用公开发布的 1,227 原题版本，不能套用正式论文的 1,696 分母。BLEnD 使用原始16文化与完整 v1.1 MCQ 两分片；2026 SemEval 扩展单独保留。test 不参与拟合、参数选择或标签检索。

## 未完成的科学前提

新方法代码和候选 G01 仍缺已核查的小模型逐题残余失败、强简单替代与原生评分资格，以及合法开发/独立确认资源。诊断代码不能替代这些观测，也不能把数学讨论稿称为已验证主方法。CB 提取器及多语言资源的 faithful qualification 明确待 Local；verify_methods 没有运行。

用户授权目的地是本仓库 literal `main`，保留公开可见性。实际 SSH/GPU/VRAM/预算和 HF 输出目的地仍未知。任务身份与真实交付/关闭记录见 [background-task.json](research/background-task.json) 和 [workflow-checkpoint.json](research/workflow-checkpoint.json)。

按用户最新指令，同一后台作者任务已恢复启用，并请求立即运行；实际执行状态尚未获确认。基线作者交付已完成；新方法与完整候选 G01 仍缺原生实测证据，GPU 实验尚未启动。[确切交付及未完成项](research/DELIVERY_RECEIPT.json)记录源码提交、逐文件回读和下一项 Local 验收；最新恢复回执见 [background-task.json](research/background-task.json)。


## 最新续接结果
源码修复及 J01 适用边界已发布于 [fe2a572](https://github.com/yuhanlydia/culture-study/commit/fe2a5722a37dda2c6e78ae691d32b6d73229de85)，8 个文件逐一回读确认。代码仍为 generated_unexecuted，尚无实测成绩。当前同一作者任务因缺少原生逐题基线/评分证据再次暂停；上面的“已恢复”是历史状态。下一步见 [LOCAL_AGENT_RUNBOOK.md](LOCAL_AGENT_RUNBOOK.md)，新方法和完整候选 G01 未完成。


## 多文化局部最优与整体最接近（2026-10-09）

已补充[五类数学模型的推导与边界](research/math/MULTICULTURAL_LOCAL_GLOBAL_REVIEW.md)及[续接要求](research/MULTICULTURAL_REVIEW_BRIEF.md)：立方体答案空间、文化内受约束信息重心、Pareto 文化风险、复用 Group DRO、Wasserstein/原生评分边界。跨文化共同 KL 收缩等价于减少文化—答案互信息；优先在同文化内聚合表达，文化之间分别决策。立方体最近边际点严格退化为逐项阈值。

这是有条件的讨论/来源审查，已有框架不计原创候选；当前 admitted=0/20、selected=0/15，没有新方法代码或实验结果。新近 CuMA、MGDA、Group DRO、DOVE 作者实现和原生任务的读取范围见[来源快照](research/math/MULTICULTURAL_SOURCE_SNAPSHOT.json)；SAQ 支持映射仍待核查。原后台任务已纳入该反馈并恢复启用；启动请求与实际生产/科学执行分开记录，见 research/background-task.json。
