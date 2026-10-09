# 两套原生基准的实验与 ACL 证据协议

状态：generated_unexecuted。现有完整基线／失败诊断设计的整理及条件性方法比较，非已冻结的 candidate G01、可执行候选队列或实验结果。
承接 [EXPERIMENT_DESIGN.md](../EXPERIMENT_DESIGN.md)、[NATIVE_CONTRACTS.md](../NATIVE_CONTRACTS.md) 和 [数学主稿](../model/MODEL.md)。历史负面与未完成项保留。

## 1. ACL／ARR 质量要求如何落实

2026-10-09 核查官方 [ARR Review Form](https://aclrollingreview.org/reviewform) 与 [Responsible NLP Checklist](https://aclrollingreview.org/responsibleNLPresearch/)。
本项目把要求落实为：主张对应证据、可复现的输入／源码／设置、完整计算成本与失败记录、明确局限和文化范围。
这些是通用审查维度；不代表某届录用阈值。约 20→15 是 Research Autopilot 的内部发现流程，并非 ACL 的统一实验数量要求。

## 2. 完整原生覆盖

| benchmark／task | 固定来源 | 覆盖与分母 | 实际接口 |
|---|---|---|---|
| CB Easy | kellycyy/CulturalBench，锁定 996d62a 前缀后由 Local 解析完整 SHA | 原生 1,227 question_idx | prepare → run → score |
| CB Hard | 同一发布版本 | 4,908 行／1,227 四判断组；主指标为全组正确 | prepare → run → score |
| BLEnD MCQ | nlee0212/BLEnD 7b9c131719e7fe5f9bed0f8b855532d613cc9f2b | 完整 v1.1 两分片、所有 MCQID／16 cultures；行数由 prepare 实测 | 原生 parser＋answer_idx equality |
| BLEnD SAQ | 同一作者 commit 的 original data | 16 cultures、500 shared templates、30 culture/language cells、inst-4＋pers-3；每模型 30,000 生成单位 | official soft_exact_match＋live parity |

CB 正式论文 1,696 题与当前 1,227 发布版本不同，不能套用论文分母或声称精确论文复现。
SAQ 推理生成覆盖全部发布问题，原生评分排除和有效分母仍由官方代码决定；US／UK 不重复 English。
MCQ 多个变体不是独立样本，不能用巨大行数夸大统计精度。SemEval 扩展不混入原始 scope。

## 3. 已写代码的完整基线矩阵

模型保持 llama_1b 与 qwen_7b。每模型：

| task | 固定 arms | complete runs |
|---|---|---|
| CB Easy | direct／whole-label likelihood | 2 |
| CB Hard | direct／whole-label likelihood | 2 |
| BLEnD MCQ | direct／whole-label likelihood | 2 |
| BLEnD SAQ | direct，完整两个官方 prompts | 1 |

合计 14 complete inference runs。完整 SAQ run 内的两提示按原生聚合，不能按题选择较好提示。
获取、准备、12 categorical＋2 SAQ、评分、parity 与 census 的完整现有命令在 [运行手册](../../LOCAL_AGENT_RUNBOOK.md#complete-inference-scoring-and-logs)。
所有 code、source repair 与本轮新增 audit 的状态为未执行；命令不是授权计算预算。

## 4. 条件性方法比较：先回答什么，再决定实现什么

下表是发现阶段的区分性问题。尚无 selected method，因此没有为这些构造虚构 CLI、solver、实验编号队列或冻结 thresholds。

| 待检验问题 | 必要的强／简单比较 | 机制控制 | 原生适用性 |
|---|---|---|---|
| 额外联合信息是否改善完整集合决策？ | 独立 whole-label；完整集合直接查询；匹配成本重复单项；已核查逻辑一致性方法 | λ=0；m=p_jp_k；真实联合证据 vs 预声明无信息对照；固定同一 p | J01：CB Hard；固定边际单标签必退化 |
| 聚合的是互补信息还是重复共同偏差？ | 原提示重复／投票、算术池化、几何池化、同文化既有 consensus | 视角信息与计算成本分别匹配；ε=0；κ／实际触边；共同错误与支持遗漏分析 | Easy／MC 使用 categorical；Hard 需完整联合支持；SAQ 仍待支持资格 |
| 最大参考差距是否改变共享资源取舍？ | 同预算平均风险、最坏群体风险／Group DRO、已有 Tchebycheff／STCH | 同一可行类；去除共享约束；固定参考／尺度；独立开发风险与成本 | 每个 benchmark 的文化条件风险分别计算 |
| 文化条件是否被平均化？ | 同文化条件基线、已核查 CuMA 类文化条件机制 | 仅在语义与数据允许时定义条件比较，保留真实文化差异 | 不把不同题目的 A／B／C／D 对齐 |

λ=0 等是同一构造的消融，不是独立新 idea。框架名称不是已合格 comparator：必须核查实际实现、模型／训练资源／输入权限与 native scorer，不能无依据宣称 SOTA。
训练型 CuMA／Group DRO 不自动满足本轮冻结推理与无训练预算；可以作为机制近邻，实际纳入 empirical arm 需明确合法数据与公平训练成本。

如果最后选择 J01，就不能预先承诺同一个联合投影改善 BLEnD 单标签任务。第二套数据仍完整保留，并检验适用边界／其他已获证据的构造。
若要声称“一个方法在两个 benchmark 都有效”，必须先有同一个有效构造在各 native task 上的定义，不能用不同算法名字共用来凑覆盖。

## 5. 信息、公平成本和小模型可行性

冻结 1B／7B 模型，不使用较大 teacher、外部 API、隐含翻译／embedding 模型或测试标签检索。
默认无训练、无 LoRA。若未来需要训练，另行明确实际数据、成本与 scope，不通过代码接口悄悄增加。

每 arm 保留：完整 prompt、canonical label tokens、额外模型查询、forward_calls、processed_tokens、generated_tokens、elapsed_seconds、peak_allocated_bytes，求解／预处理时间，以及必要缓存／I/O。
完整标签 likelihood 具有额外 forward 成本，不能称与单次直接生成等预算。
新候选必须与预先声明的成本匹配简单替代比较，同时报告性能／成本曲线；单个调用的长短和前缀重算也计入。

单一 GPU 计数来自项目对话；实际可执行分配、型号／VRAM、CPU／RAM／磁盘、wall-time／GPU-hours／spend 仍待确认。不借用其他项目资源。
7B 和 1B 顺序驻留。新内存源码减少概率临时张量，实测吞吐／峰值未知，不据此发布“低显存可运行”结论。
OOM、上下文溢出、token boundary 或 scaler 依赖错误停止受影响任务。不能偷偷换量化、截断、缩小 benchmark 或改变精度救分。

## 6. 开发、测试与独立确认

当前 inspected releases 没有建立可用于本项目拟合的 native train/dev 资源：

| 用途 | 现有数据可做什么 | 当前限制 |
|---|---|---|
| source／scorer qualification | 按原生 IDs 与官方定义核查 | 不构造手工 eval 替代 |
| baseline diagnosis | 固定设置下完整测量与残余分析 | 只能标 exploratory／developmental evidence |
| 参数／视角／权重／策略选择 | 需要合法非 test 开发数据，或完全事先固定、不随成绩改变的理论规则 | 当前未闭合 |
| fresh confirmation | 需要在结果之前冻结算法、IDs、设置、分析与预算，并说明曝光史 | 当前未闭合 |

重新抽 seed 不产生新的未见题目；事后把已读 test 分成 dev/test 也不制造原始未见确认。
无标签的 κ／KKT／成本诊断可以预先记录，但不能在看到测试改进后用它们选择 ε、λ、视角数或 culture thresholds。
任何作用于结果的改动保存 child protocol／source／run 目录和全部历史。

## 7. 统计、文化粒度和精度

CB 使用 question_idx 作为成对独立分析单位，四行 Hard 不独立。BLEnD 使用原始 shared ID 作为 cluster，保留全部文化、语言、提示和 MCQ variants。
报告 micro、native culture/language cells；如额外报告 equal-culture macro，必须明确其 estimand。宏平均、最坏文化与官方总分不同，不能互换。

对总体推断需要可信 live analysis callback：成对抽样 native clusters，并在每次样本中重新计算声明的 native aggregate／culture macro。比例有效分母、SEM-W 与最坏群体尤其不能用普通独立行均值的误差条替代。
当前该 callback 尚未实现或验收，故可先报告有限发布集描述值，不声称统计显著。

确认之前冻结 family={(model,endpoint,treatment,control)}、主要 endpoint、效应 margin 与 multiplicity policy，例如对预声明 family 使用 Holm；不能在看到分数后缩小 family。
没有统一“三个 seeds”标准。随机混合／采样需要其真实随机性重复，确定性贪心的同 seed 重跑不增加独立样本。
精度应由合法开发的成对差异方差与 native cluster 数决定，不能用假设测得方差填数。样本不足时保留不确定结论，而不是删掉表现差的文化。

## 8. 源码修复资格与 E04

新 [audit-likelihood](../implementation/README.md#5-修复的完整-native-接受入口) 仅比较完整 old/new native runs 的软件性质。它不产生 native benchmark 分数或通过标记。
保留相同 prepared/model/config/hardware，并分别记录源身份、logprob／答案差异；容差与原因在观察之前声明。

每个 coherent batch 返回 E04：实现语义、模型／输入／baseline 资格、完整分母、official scorer parity、实际设置／成本、合理的 dev-only 敏感性和全部失败。
遇到 parser／数值／支持／成本混杂时先修复证据，不能直接裁决方法失败或有效。
科学判定必须使用实际完整比较、原生 replay 与冻结阈值；本文件不伪造 PASS／REVISE／KILL。

## 9. 主张与最低证据

| 希望讨论的主张 | 必须返回的证据 | 当前状态 |
|---|---|---|
| 小模型具有某种真实残余失败 | 两模型 full native predictions／score／census，强简单替代与来源归因 | 未执行 |
| 联合信息改善整组决策 | 同 p 的 paired Hard 比较、m 可靠性、成本匹配与机制控制 | 未实现／未选择 |
| 同文化聚合带来互补信息 | view 资格、支持覆盖、纠错与共同错误、简单池化／投票成本匹配 | 条件分析 |
| 共享预算改善最被牺牲文化的差距 | 同一 ΘB、合法参考风险／误差、真实成本、所有文化风险和不伤害检验 | 条件分析 |
| 1B／7B 可复现运行 | 固定版本、真实硬件／日志／完整输出、环境／数值／scorer 资格 | 源码存在，未验收 |
| 文学／宗教或社会文化保真 | 相关 native 内容与独立适用证据 | 当前不作超出数据的主张 |

## 10. 下一动作与关闭条件

先按真实 Local runbook 接受本轮 source repair，完成已有 native scorer／baseline／census。独立数学和来源整理可继续；不要求用户重复授权 GitHub 写入。
只有原生证据、开发／确认、Parent／value／完整数学池与选择、碰撞／IPCG和方法边界满足后，才完成被选候选的 solver、比较代码、candidate G01 与冻结协议。

作者任务的整理里程碑与完整研究目标分别记载；提交成功不是科学成功。完整作者交付或实际独立工作耗尽时，保存下一动作并停用同一有限任务，不能无限重复讨论或制造进度。
