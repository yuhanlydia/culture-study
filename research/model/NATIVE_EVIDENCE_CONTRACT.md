# 原生提示、语言列与数学证据的资格

日期：2026-10-09。恢复来源：culture-study/main 的 4eb29eef4f5469daeeb5f827cb02930a362a8316。
状态：作者条件推导、原生来源审查与既有基线输入修复；generated_unexecuted。
本文件深化现有 J01／LOCAL02，不新增入选候选、求解器、原生实验或新颖性结论。

## 1. 本轮实际解决的缺口

仅有同一 country、ID 或四个选项字母，不能证明两个查询在估计同一个对象。
本轮从锁定 BLEnD 发布文件发现一个先于优化的真实输入错误：
现有 prepare.py 依据论文／README 的列说明，将 Question 当作英文、Translation 当作本地语言；
然而读取的发布文件行具有相反的内容。所读 UTF-8 源字节与锁定 Git blob 一致。

| 发布文件与文化 | 本轮所读内容 | 此修订采用的绑定 |
|---|---|---|
| 原始14个非英语文化的 question CSV | Question 为本地文本，Translation 为英文 | English → Translation；本地语言 → Question |
| US／UK question CSV | 两列均为英文，UK 有本地措辞差异 | 保留 Question 的国家特定措辞；各只有一个 English cell |
| 16个 culture 的 prompt CSV | English 为英文模板，Translation 为本地模板 | English → English；本地语言 → Translation |

读取范围明确限制为各 question 文件的表头及前3或8行，共63个原生行；
不是全部500题的语言审核。所有16个 prompt 文件已完整读取，语义检查聚焦 inst-4／pers-3。
全量语言、ID与准备结果仍由 Local 验收，不能把有限预览升级为完整数据资格。
固定版本与逐文件读取范围见 [来源记录](../sources/NATIVE_VIEW_AUDIT.json)。

论文附录 A.1 和此 commit 的 README 沿用相反的 question 列说明；
model_inference.py 的默认列分支也沿用该说明，并读取在线提示表。
本修订依据实际固定发布字节，不声称复制那个脚本或历史作者运行的精确输出。
US／UK 继续使用 Question，是明确的国家特定发布输入选择；
不把它描述成作者脚本默认 Translation 分支的严格复现。

所读 English inst-4 对16个文化使用同一个单答案指令；
pers-3 还引入属于目标文化、向外国人解释的角色条件。
二者是官方分别评估的提示条件，不能仅凭共同 ID 就视作同分布的重复样本。
本地翻译的存在也不证明任意语义漂移为零；本轮没有对13种语言作完备等价性认证。

## 2. LOCAL02 聚合需要什么“共同对象”？

固定题目 i 与文化 c，先声明条件签名
$$
\sigma_{icv}=
(\text{原生ID},\text{文化指代},\text{问题含义},
 \text{答案支持},\text{角色},\text{输出语言},\text{原生效用}).
$$

如果 v 只是等价表达，需有不读取测试标签的答案映射
$\chi_v:S\to S_v$，使同一个答案对象可以跨视角比较。
对单选的排列可用已知选项置换；对不同 MCQID 的不同选项集合，
同一个全局模板 ID 不足以提供这种映射。
自由文本的语言翻译／同义映射不能从评分答案别名反向构造。

设映射后的正模型分布为 r_v，语义理想分布为 P_v。
两者是条件分析对象；P_v 未被观察，r_v 也不是人群分布。
若用共同参考 P_0 考察答案 a、b，定义
$$
M_{ab}=\log\frac{P_0(a)}{P_0(b)},\quad
d_{v,ab}=\log\frac{P_v(a)}{P_v(b)}-M_{ab},\quad
e_{v,ab}=\log\frac{r_v(a)}{r_v(b)}
                 -\log\frac{P_v(a)}{P_v(b)}.
$$
d 是条件／语义漂移，e 是模型误差。它们不能仅由模型间分歧识别。

对固定 $\omega_v\ge0,\sum_v\omega_v=1$，几何池化
$g(z)\propto\prod_vr_v(z)^{\omega_v}$ 的对数几率满足精确恒等式
$$
\boxed{\log\frac{g(a)}{g(b)}
=M_{ab}+\sum_v\omega_v(d_{v,ab}+e_{v,ab}).}
\tag{V1}
$$
证明：归一化因子在同一分布的比值中消去，再代入各项分解。
这不是跨不同条件的归一化常数可以任意相消的论断。
即使所有模型误差 e 为零，只要漂移 d 非零，聚合仍可能改变参考对象的答案。

进一步令锚点 r_0 的误差为 e_0，现有 LOCAL02 路径为
$q_t\propto r_0^{1-t}g^t$，$0\le t\le1$。直接代入得到
$$
\boxed{\log\frac{q_t(a)}{q_t(b)}
=M_{ab}+(1-t)e_{0,ab}
       +t\sum_v\omega_v(d_{v,ab}+e_{v,ab}).}
\tag{V2}
$$
若在同一有限支持上有真实且同时有效的界
$|e_{0,ab}|\le E_{0,ab}$、
$|d_{v,ab}|\le D_{v,ab}$、
$|e_{v,ab}|\le E_{v,ab}$，则 P_0 的唯一模式 a 在
$$
M_{ab}>
(1-t)E_{0,ab}+t\sum_v\omega_v(D_{v,ab}+E_{v,ab}),
\qquad \forall b\ne a
\tag{V3}
$$
下被 q_t 保留。证明仅用三角不等式及严格正的对数几率。
界为零时回到等价、无误差视角；t=0 回到锚点；相同错误视角仍保留共同错误。

这是充分条件，不是置信区间或原生正确性保证。
P_0、D、E 当前未知，不能把模型一致性、同语言或小 KL 当作这些界的证明。
V1/V2 可以解释漂移如何进入优化；V3 只用于条件推理，不提供测试集调参规则。
与既有 MAP/KL 阈值、共同偏差分析一致，没有以新名称包装一个新池化算法。

**可区分预测与证伪：** 若只是等价表达，增加互补视角应体现为同一原生效用上的纠错；
若变化来自角色／语言条件、答案支持或解析，则不能将总分变化单独归因于联合优化。
全部收益由匹配成本重复查询／投票或输入修复解释时，特有优化机制的主张被削弱或证伪。
这些是尚待原生证据的预测，不是已观察到的小模型失败。

## 3. J01：逐对可行不等于存在同一个联合分布

现有标签基线提供的是
$$
p_j=P_f(\text{True前缀}\mid x_j,\text{合法标签前缀事件}),
$$
其中 x_j 是第 j 个单项提示。拟议联合证据
$m_{jk}$ 来自另一个包含两项的提示 $x_{jk}$。
不同提示的信息与合法输出条件不同；这些概率不会自动成为
同一个 $q(Z\mid i,c)$ 的边际与二阶矩。

现有 Fréchet 区间
$$
\max(0,p_j+p_k-1)\le m_{jk}\le\min(p_j,p_k)
$$
只是逐对必要条件。考虑前三位，逐状态都有
$$
z_1+z_2+z_3-z_1z_2-z_1z_3-z_2z_3\le1.
$$
按激活位数 n=0,1,2,3 检查，左边分别是0,1,1,0。
所以任何联合分布都必须满足
$$
\boxed{s_{12}+s_{13}+s_{23}\ge p_1+p_2+p_3-1,}
\quad s_{jk}=\mathbb E_q[z_jz_k].
\tag{J-coherence}
$$

一个纯数学反例：取四个边际均为1/2，前三对目标都为
$\eta\in(0,1/6)$，其余三对设为1/4。
每一对目标分别落在[0,1/2]中，且概率严格为正；
但前三对总和 $3\eta<1/2$，不可能来自这些固定边际的同一联合分布。
它不是手工 benchmark 样例、失败比例或实验结果。

这还给出 J01 不可避免的目标残差。
设其前三对 Bernoulli 惩罚为 $\sum d_{\rm Ber}(s_{jk}\|\eta)$。
由 Jensen 与 J-coherence，平均 s 至少1/6。
当 $s>\eta$ 时
$$
\frac{\partial}{\partial s}d_{\rm Ber}(s\|\eta)
=\log\frac{s(1-\eta)}{\eta(1-s)}>0,
$$
故对任何可行 q，
$$
\sum_{\{12,13,23\}}d_{\rm Ber}(s_{jk}\|\eta)
\ge3d_{\rm Ber}(1/6\|\eta)>0.
$$
J01 的其余 KL 项非负，因而有限 $\lambda>0$ 时
$$
\boxed{F(q^\star)\ge3\lambda d_{\rm Ber}(1/6\|\eta)>0.}
\tag{J-residual}
$$
两条独立代数检查是逐状态指标不等式与凸 Jensen 导数；
没有执行求解器、穷举程序或科学测试。

因此软惩罚可以保持原 J01 问题可行、严格凸且唯一，但不能满足互相矛盾的原始证据。
额外查询可能改变一阶证据对应的条件；冻结 p 会把这种冲突变成不可消除残差。
如果采用完整集合查询来确保矩来自同一个模型分布，还需与该查询自身的 MAP 直接比较；
不能忽略它已有的联合信息／计算成本，再把任何变化归功于投影。
逐对兼容性与共同矩域是诊断，不是新方法；高阶不可识别和单标签退化继续保留。

**证伪与下一证据：** 将来每次联合查询必须记录完整提示、语义支持、标签事件与 token 概率。
需要原生 per-ID 的联合可靠性与预算匹配简单替代。
优化收敛、矩相容或 KKT 小残差都不证明文化真值或原生 exact-match 改善。

## 4. 对两个 benchmark 和三条数学路线的实际影响

| 原生任务／讨论 | 本轮可确定事项 | 仍未满足 |
|---|---|---|
| CB Hard／J01 | 保留四行原生真假判断；联合证据不自动共边际；共同矩域比逐对界更严格 | 原生残余失败、可靠联合查询、完整池／选择与碰撞 |
| CB Easy／BLEnD MC | 选项字母只在同一题内有意义；严格单标签固定边际仍退化 | 合法等价视角与同支持比较 |
| BLEnD SAQ／LOCAL02 | 修正发布语言列；保留两个官方提示分开评分及官方平均 | label-blind 自由文本支持／效用映射，不能用 SEM 别名构造支持 |
| PARETO03 | 每个风险必须绑定真实语言／提示／效用条件；先修输入再估风险 | 合法开发风险、参考点、共享预算与真实成本 |

本轮不创建第二套 benchmark、训练任务、大 teacher 或额外模型。
1B／7B 模型、14个完整基线 run、16 cultures、30个 SAQ language cells、
两个官方 SAQ prompts、原生 SEM-B／SEM-W、CB／MCQ 分母均保留。
SAQ 官方两提示分数的平均是**评价聚合**，不是融合两提示答案的推理算法。
论文／README 的来源说明冲突记录为负面证据；不改写历史文件或旧运行。

## 5. 实际源码修复与 Local 下一动作

prepare.py 读取 sources.lock.json 中固定的逐文化 saq_input_contract；
将 question_column、prompt_column、contract_id 纳入每题 source／input_digest，
coverage 也保存完整语言列映射。未改数据、标签、scorer、模型、温度或提示模板。
这是既有基线的输入修复，不是 J01／LOCAL02 实现。

source_lock 与 prepared／source digest 都改变：
旧绑定、acquisition、prepared、runs 和 score 不能当作本修订的接受回执。
保留旧产物在原始身份下；使用独立 child 路径，详见
[Local 接受与命令](../../LOCAL_AGENT_RUNBOOK.md#native-language-column-repair)。
不要用 audit-likelihood 对照不同输入语言的两个 run；
该工具要求相同 prepared 数据，不能认证这次输入修复。

下一最早可执行证据步骤是 Local 在真实资源／既有 harness 下：
1. 接受此固定源码与列契约，获取／校验原始输入，按新路径完整 prepare。
2. 对全部文化确认原生文本列、提示列、文化指代及ID，不向输入注入答案。
3. 资格化原生 scorer，完成固定1B／7B基线／简单替代、返回 per-ID 输出、分母、成本和失败。
4. 明确合法非 test 开发与独立确认，再恢复 Parent／value／实际数学池审查排序与 collision／IPCG。

本轮有界来源与条件数学作者稿已完成；继续候选投资所需 native 证据仍不可用。
仅靠下一次作者定时续接不能生成这些观测。保存完整依赖后暂停同一任务，
不将此暂停称作完整研究完成。源码未 import／compile／test，
无模型／数据下载、scorer、推理／训练／GPU／SSH动作，verify_methods 也未运行。

## 6. 原始来源与审查范围

- [BLEnD 原始论文](https://proceedings.neurips.cc/paper_files/paper/2024/file/8eb88844dafefa92a26aaec9f3acad93-Paper-Datasets_and_Benchmarks_Track.pdf)：§3、§4.1–4.2、Appendix A.1 的题目／提示／语言与评估说明。
- [锁定 BLEnD 源](https://github.com/nlee0212/BLEnD/tree/7b9c131719e7fe5f9bed0f8b855532d613cc9f2b)：16个 prompts、question 受限行、README、model_inference.py，以及 utils.py 国家替换／语言表、MC prompt 构造和评价按条件记录的实际代码。
- [CulturalBench ACL 2025](https://aclanthology.org/2025.acl-long.1247.pdf)：§2.3、§4、Appendix D 的任务／四判断评分／提示；现有1227发布分母继续保留。
- [已有近邻](../CLOSEST_WORK.md)、[模型主稿](MODEL.md)、[决策信息边界](../math/DECISION_INFORMATION_BOUNDARIES.md)的来源和负面边界继续有效。
  本文的 Jensen／矩域／对数几率结果是标准数学操作的作者条件推导，没有进行新的全面原创性审计。

审查性质：同一作者上下文的源码／代数检查，无独立代理审查、机器池验证或性能结论。

