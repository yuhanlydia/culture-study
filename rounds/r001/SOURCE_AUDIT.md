# r001 来源核查与未完成项

观察时间：2026-10-08，约 23:30 UTC。读取来自本次数学方向讨论与任务设置续接；不是后台 worker 已执行的证明。以下均是静态来源阅读，没有运行科学代码、数据/模型下载或 scorer。

本次交付父提交已经新增 research/SOURCE_AUDIT.md、NATIVE_CONTRACTS.md、CLOSEST_WORK.md、math/OBJECTIVE_ANALYSIS.md 等审计；均已读取并保留。该数学讨论补充 LoCo/ConCoRD 阅读及联合概率构造，不覆盖或删除先前记录。

## Benchmark 与原生语义

1. CulturalBench ACL 2025 正式论文：
   https://aclanthology.org/2025.acl-long.1247.pdf
   已读原生任务构造、问题类型及第 3–4 节评分相关段落。Hard 为每原题四次二元判断，四项全对才计该原题正确。正式论文描述 1696 原题、6784 二元判断；不把旧版数目混作正式版分母。

2. 当前 HF 发布卡：
   https://huggingface.co/datasets/kellycyy/CulturalBench/blob/main/README.md
   页面显示提交标记 996d62a；卡内仍描述 1227 原题、4908 Hard 行，两个 config 均指定 test。这里只读卡、字段说明及发布页面，没有 materialize CSV 或逐条标签核查。当前 research/NATIVE_CONTRACTS.md 已明确选择该公开 1227 原题版本；不把 1696 论文版数目套入这个版本。沿用已固定的来源身份；未解决的是正式版与发布版的关系、完整完整性及官方/忠实 scorer 的 Local 资格。本项目没有获证的开发划分；不能在上述 test 上拟合或选择参数。

3. BLEnD 作者仓库：
   https://github.com/nlee0212/BLEnD/tree/7b9c131719e7fe5f9bed0f8b855532d613cc9f2b
   已读 README 更新/数据/评价说明、递归源码清单及以下实际源文件：
   - evaluation/multiple_choice_evaluation.py，multiple_choice_score：按 country 过滤后，比较 answer_idx 与 final_ans 的逐行准确率。
   - evaluation/evaluate.py，evaluate_all_metrics：短答案调用 soft_exact_match 并输出 SEM-B、SEM-W；MC 是另一接口。
   - evaluation/exact_match.py，soft_exact_match：包含可答条件过滤、母语/英语词形匹配、标注投票权重与有效问题分母。
   读取不等于运行或验证忠实性；语言依赖、入口参数、完整输入文件/版本和缺失答案处理尚未 Local 资格验证。README 的新增 SemEval 扩展不自动成为本项目评测范围。

## 最接近的技术与初步语义比较

- LoCo-LMs：全文 https://arxiv.org/html/2409.13724v1 ，另读早期推导 https://arxiv.org/html/2404.12843v1 中概率与语义损失段落。已明确存在用真值概率与逻辑约束改善一致性的构造，不能宣传“概率逻辑约束”本身为新贡献。
  作者仓库旧路径跳转至 ddidacus/loco-llm；已读取源码树、models/loco/trainer.py 的训练/评分编排及 models/loco/model.py 的相关概率/事实损失接口，固定源码修订 e3fe10231a7a80308a4924050fb9c5eb6608f4fe 。尚未逐行资格验证完整逻辑损失与环境/数据路径，不把它描述为已复现基线。

- ConCoRD：作者源 https://github.com/eric-mitchell/concord/tree/4f0c7fee44d3d61020c9c4a5a523beba80c4c55d ，实际读取 nlic/solver.py 中概率到 log-odds 权重、归一化选项、加权约束和 RC2 求解路径。
  J01 的待核查差异是固定边际并优化分布中的联合依赖，再按原生整组损失决策；ConCoRD 已有置信与关系结合的求解机制。这是语义比较问题，尚无独立碰撞裁决或原生本任务适配证明。

- 2026 问法对称研究：https://arxiv.org/html/2607.05552v1 ，已读其逻辑等价改写、标签/顺序分解与对称化段落。不能把正反问法对称化本身宣称为新贡献。该论文讨论道德判断，不能自动移植其数值或结论到文化事实知识。

- ACL/ARR 官方评审：https://aclrollingreview.org/reviewform ，已读 soundness 与 main/Findings 说明。数学构造需要可靠论证与可复现评价；公式数量不是录用标准。

上述相关性不等于已完成全面 originality/IPCG 审计。需要检索最大熵、固定边际耦合、后验约束、结构化多标签 Bayes 判决、联合 elicitation 与文化 benchmark 的同构方法；由当前 skill 规定的独立审查角色进行实际 adjudication，而非生成者自证原创。

## 当前真实产物与下一步

前一来源里程碑含八项有条件的数学分析，本次在其基础上增加讨论卡 J01；已核验/入选的新方法候选仍为 0，未完成代码或 G01。数学反例是证明材料，不是人造评测样本。

优先沿用原生发布选择，完成小模型 baseline/scorer/census 的独立作者材料与 Local 交接；实际失败证据、约20候选逐卡审查与全池排序仍待完成。可复用当前来源读段；不重新初始化，不把科学前提改成通过，不把 J01 的单标签退化隐藏。尚缺完整 Parent/Natural Gate 0/IPCG、正式方法审查、两套完整原生设计及 Local 验收。
