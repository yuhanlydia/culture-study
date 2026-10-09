# 文化条件答案决策与共享预算下的风险折中

日期：2026-10-09。整理依据：main 31814655e85d484144696bf2a24acfbf50abbfc2 的 J01、LOCAL02、PARETO03 及其边界推导。
状态：现有数学构造的统一说明与作者推导；未选定新方法，无求解器、模型或 benchmark 执行，不是正式论文或原创性结论。

## 1. 一个明确的研究问题

在保持文化条件与原生任务的前提下，冻结小模型能否利用可靠的额外证据改善完整答案决策？若各文化竞争同一有限资源，怎样尽量缩小各文化距离自身可达最优风险的差距？

这有两个不同的优化层次：

1. **题目层**：对给定问题与文化构造答案分布，再按原生损失决策。
2. **文化层**：在同一可行策略类和共享预算内比较风险，选择资源与策略配置。

文化层的“整体最接近”指风险向量接近理想点。不同文化的答案不需要相同；字母 A 在不同题目中没有可直接平均的语义。

## 2. 对象、信息与原生损失

令 i 为原生问题，c 为数据集文化标识，v 为题目在同一文化内的表达／提示视角。文化标识不是对全部居民的完备描述。
冻结模型为 f，原生答案为 Y，模型构造的分布为 q；q 不被假定为真实文化分布或校准的真值后验。

| 原生任务 | 决策空间 | 题目损失与主指标 |
|---|---|---|
| CulturalBench-Hard | $\Omega_i=\{0,1\}^{4}$ | $\ell(a,Y)=1[a\ne Y]$；四个真假判断全部正确 |
| CulturalBench-Easy | 四个选项的 categorical 空间 | 单选错误率／accuracy |
| BLEnD MCQ | 每行四个原生选项 | answer_idx 错误率；保留原生 country 与分母 |
| BLEnD SAQ | 自由文本 | $1-u_{\rm SEM-B}$、$1-u_{\rm SEM-W}$，由官方评分定义；分别报告 |

SAQ 的原生百分数在风险分析中除以 100 转成 [0,1]，最终表仍报告官方百分数。SEM-B 与 SEM-W 不能被任意合成一项损失。

真实 Bayes 决策为
$$
a_{\rm Bayes}=\arg\min_a\mathbb E[\ell(a,Y)\mid i,c].
$$
对完整集合的 0–1 损失，这是联合 MAP。用模型 q 的 MAP 是一种决策规则，只有 q 的相关证据足够准确时才可能逼近真实 Bayes 决策。
对 SAQ，最高概率字符串一般不等于官方 SEM 效用的最优答案；目前没有合法、已验证的自由文本支持对齐与效用后验。

模型可见信息仅包括问题、原生选项、明确文化条件和预先允许的表达。评分标签、人工答案别名、注释频次及测试最优策略不进入推理。

### 2.1 原生条件先于优化

[原生证据资格](NATIVE_EVIDENCE_CONTRACT.md) 核查实际固定提示、问题列与条件。
BLEnD question 文件的发布列内容与旧 prose convention 相反，现有基线已写修复；
全部原生语言／准备资格仍待 Local。inst-4／pers-3 不是已证明等价的同分布视角。
该补充给出条件漂移的对数几率分解，以及联合矩逐对可行仍无法整体共存的反例／残差下界。
它修订证据前提，不改变 J／L／P 的已知数学构造或未入选状态。

## 3. J01：文化条件下的答案集合信息投影

### 3.1 立方体与联合分布

令 $z_j=1$ 表示第 j 个原生答案陈述成立，$p_j\in(0,1)$ 为冻结模型的边际证据。
四维立方体有 16 个答案顶点；完整联合分布位于 15 维概率单纯形：
$$
q\in\Delta(\Omega),\qquad
q_0(z)=\prod_{j=1}^4p_j^{z_j}(1-p_j)^{1-z_j}.
$$

最接近边际向量的欧氏顶点是
$$
\arg\min_{z\in\{0,1\}^4}\|z-p\|_2^2
=\big(1[p_j>1/2]\big)_{j=1}^4,
$$
平局另按预声明规则处理。原因是两个坐标代价之差为 $(1-p_j)^2-p_j^2=1-2p_j$。因此“最近立方体顶点”本身没有新增联合作用。

### 3.2 优化问题

令 $m_{jk}\in(0,1)$ 为额外联合查询得到的模型证据，$\phi_{jk}(z)=z_jz_k$，
$$
d_{\rm Ber}(s\|m)
=s\log(s/m)+(1-s)\log((1-s)/(1-m)).
$$
原始 J01 整理为
$$
\boxed{
\begin{aligned}
\min_{q\in\Delta(\Omega)}\quad&
D_{\rm KL}(q\|q_0)
+\lambda\sum_{j<k}
d_{\rm Ber}\!\left(\langle q,\phi_{jk}\rangle\middle\|m_{jk}\right)\\
\mathrm{s.t.}\quad&
\langle q,z_j\rangle=p_j,\quad j=1,\ldots,4.
\end{aligned}}
\tag{J}
$$
输出 $\hat z=\arg\max_z q^\star(z)$，并保留并列规则。固定边际只保护模型的一阶证据，不保证文化知识正确。

### 3.3 推导与求解

q0 是可行点。正参考分布上的 KL 严格凸；Bernoulli KL 对其第一个参数凸，矩映射线性。因此在给定正概率、有限 $\lambda\ge0$ 时，目标连续、可行域紧且凸，存在唯一分布最优解。

在内部解处，令 $s_{jk}=\langle q,\phi_{jk}\rangle$，
$$
g_{jk}=\operatorname{logit}(s_{jk})-\operatorname{logit}(m_{jk}).
$$
一阶 KKT 条件给出
$$
q^\star(z)\propto q_0(z)
\exp\!\left[-\sum_ja_jz_j-\lambda\sum_{j<k}g_{jk}z_jz_k\right].
\tag{J-KKT}
$$
a_j 是边际约束乘子，g_jk 又依赖 q；该式不是可直接代入的闭式解。只能在已满足实现前提后使用小规模凸求解器，并记录可行性、KKT 与目标残差。不能把任意固定点迭代视为收敛证明。

求解变量为 16 个概率，5 个独立等式约束（归一化＋4 个边际），另有 6 个软联合证据。一般内部可行面有 11 个自由度；若再精确固定全部二阶矩，则剩 5 个。主成本来自语言模型查询，不来自这个固定规模问题。

单个联合矩的可行区间为
$$
\max(0,p_j+p_k-1)\le s_{jk}\le\min(p_j,p_k).
$$
模型给出的 m 可以违反这些界。软惩罚仍有意义；把全部 m 强行设成等式可能导致不可行。数值裁剪必须事先声明，不按测试成绩选择。

### 3.4 退化、必要信息与失败边界

- $\lambda=0$ 或全部 $m_{jk}=p_jp_k$ 时，唯一最优为 q0，MAP 退化为逐项阈值。
- 固定一阶边际不能识别任意联合 MAP。即使全部三阶边际相同，也可存在不同唯一 MAP，反例见 [边界推导](../math/DECISION_INFORMATION_BOUNDARIES.md)。
- 在严格单标签空间 $\Omega=\{e_1,\ldots,e_K\}$ 内，固定 $\mathbb E[z_j]=p_j$ 已经固定 q(e_j)=p_j。J01 的联合自由度为零；不能沿用 Bernoulli 乘积参考到这个支持。
- 联合查询若与独立证据相同，或全部修改仍在 MAP 不变区间，就不会改善原生整组指标。
- 固定错误的一阶证据也可能阻止修正正确集合；更强置信并不代表更准。

**区分性预测**：有用收益需要额外的联合信息，并需要实际改变完整集合决策。若预算匹配的重复单项查询同样有效，则不能归因为特有的联合优化机制。
**证伪条件**：联合证据在原生错误上无可靠增量；或求解只改变概率而不改变原生答案；或收益完全由额外调用／解析替代解释。

## 4. LOCAL02：文化内视角聚合与锚点信赖域

### 4.1 优化问题

对同一 i、c，假设各视角具有已对齐的有限答案支持 S，得到正分布 $r_v$，锚点为 $r_0$。令 $\omega_v\ge0,\sum_v\omega_v=1$。
$$
\boxed{
\begin{aligned}
\min_{q\in\Delta(S)}\quad&
\sum_v\omega_vD_{\rm KL}(q\|r_v)\\
\mathrm{s.t.}\quad&
D_{\rm KL}(q\|r_0)\le\epsilon.
\end{aligned}}
\tag{L}
$$
它聚合同文化内的信息；文化之间分别求解。锚点是模型参考，$\epsilon$ 是偏离预算，不是人类文化保真保证。

### 4.2 闭式路径与一维预算求解

令 $h(z)=\sum_v\omega_v\log r_v(z)-\log r_0(z)$。在有约束的内部情形，KKT 给出
$$
q_t(z)=\frac{r_0(z)e^{t h(z)}}{Z(t)},\qquad
t=\frac1{1+\eta}\in(0,1],
\tag{L-path}
$$
$\eta\ge0$ 是信赖域乘子。等价地，
$$
q_t(z)\propto r_0(z)^{1-t}\prod_vr_v(z)^{t\omega_v}.
$$
设 $K(t)=D_{\rm KL}(q_t\|r_0)$。配分函数求导得到
$$
K'(t)=t\,\mathrm{Var}_{q_t}[h]\ge0.
$$
若 K(1)≤ε，取 t=1；否则在 [0,1] 上求 K(t)=ε。ε=0 时 q=r0；h 为常数时整条路径都为 r0。每次预算检查为 O(|S|)，再乘一维搜索迭代数；实际耗时未测。

### 4.3 什么时候保护约束允许改变答案？

令锚点唯一模式概率为 A，第二大概率为 B，A>B>0。到 MAP 边界的最小 KL 为
$$
\boxed{\kappa(r_0)=-\log\!\left[1-(\sqrt A-\sqrt B)^2\right].}
$$
若 ε<κ，任何可行 q 都保留原答案；ε=κ 可接触平局。
对特定池化路径，竞争答案 b 触边还需要
$$
h(b)>h(a),\qquad
t_{ab}=\frac{\log[r_0(a)/r_0(b)]}{h(b)-h(a)}\in(0,1].
$$
这是“允许改变”“实际改变”和“改变后更正确”三个不同问题。前两项可由模型证据检查，最后一项必须用原生评分。

### 4.4 文化差异与信息丢失

若同时优化各文化分布 qc 并令它们靠近共同中心，设 $w_c\ge0,\sum_cw_c=1$，则
$$
\min_u\sum_cw_cD_{\rm KL}(q_c\|u)
=\sum_cw_cD_{\rm KL}(q_c\|\bar q)
=I(C;Z),\quad \bar q=\sum_cw_cq_c.
$$
继续最小化这项会鼓励减少答案中的文化信息。只计算固定 qc 的中心用于描述不会修改原分布；把这个中心用于文化无条件的共同决策才会引入平均化问题。

**区分性预测**：若各视角互补且支持有效，聚合可能修正锚点错误；若它们复制同一系统偏差，低分歧仍可能一致错误。
**证伪条件**：收益被预算匹配投票完全解释；视角等价性／支持对齐失败；保护预算导致答案不变；或原生风险增加。
相关偏差与遗漏支持的完整推导见 [RELIABILITY_AND_SUPPORT.md](RELIABILITY_AND_SUPPORT.md)。

## 5. PARETO03：各文化分别最优、共享约束下整体最接近

### 5.1 同一可行类与理想点

令 ΘB 为冻结模型、允许的决策规则与共享预算 B 组成的同一策略类，R_c(θ) 为文化 c 的原生期望风险。
$$
a_c=\inf_{\theta\in\Theta_B}R_c(\theta).
$$
理想向量 a 一般无法由同一 θ 达到。定义正尺度 s_c，求
$$
\boxed{
\begin{aligned}
\min_{\theta\in\Theta_B}\quad&
\max_c\frac{R_c(\theta)-a_c}{s_c}\\
\mathrm{s.t.}\quad&
R_c(\theta)\le R_c(\theta_0)+\delta_c,\quad\forall c.
\end{aligned}}
\tag{P}
$$
$\delta_c\ge0$ 是预先声明的允许风险偏移。s_c=1 对同一 [0,1] 原生损失给出百分点差距；其他尺度必须有来源，并避免极小分母放大误差。不同 native endpoint 分开建模。

这不是要求每种文化都输出共同答案，而是尽量缩小最被牺牲文化距自身可达最优的风险差距。
若 Θ 是各文化策略类的完全直积、风险各自独立且没有共享约束，则理想点可同时达到，不存在这个取舍。不能人为加限制来制造漂亮的 Pareto 曲线。

### 5.2 适合小模型的有限策略解释

考虑已固定的 H 个冻结推理规则，文化 c 的混合权重为 π_ch。风险为 R_ch，成本为 k_ch：
$$
R_c(\pi)=\sum_h\pi_{ch}R_{ch},\qquad
\sum_{c,h}w_c\pi_{ch}k_{ch}\le B.
$$
同一 ΘB 内的 epigraph 是
$$
\begin{aligned}
\min_{\pi,t}\quad&t\\
\mathrm{s.t.}\quad&
\sum_h\pi_{ch}R_{ch}\le a_c+s_ct,\\
&\sum_h\pi_{ch}=1,\quad\pi_{ch}\ge0,\\
&\sum_{c,h}w_c\pi_{ch}k_{ch}\le B,\\
&R_c(\pi)\le R_c(\pi_0)+\delta_c.
\end{aligned}
\tag{P-LP}
$$
有 CH+1 个变量。固定风险／成本后，这是已有线性规划，而不是新的训练算法。基础模型不更新，不需要同时驻留两套权重。

a_c 必须在同一个共享可行类内计算。只有预算不限制各文化单独最佳策略的可达性时，才可把它简写为 min_h R_ch。
混合成本是期望成本；逐题硬预算、整数调度和文化内自适应路由是不同问题，不享有这个 LP 的同一保证。成本必须包含生成、额外查询和求解，不只数“调用次数”。

### 5.3 实际风险未知：参考点与不伤害约束

开发集上的估计参考称为“有限策略类参考点”，不能称为已知 oracle。
若在预先固定可行类上有一致风险误差 e_c、参考误差 d_c，且尺度固定，则
$$
\eta=\max_c\frac{e_c+d_c}{s_c},\qquad
F_a(\hat\theta)\le\inf_\theta F_a(\theta)+2\eta+\tau,
$$
τ 是全局求解误差。这是条件误差界；目前 e、d、τ 均没有实测证据。

“估计风险不增”不能直接当成“真实风险不增”。若成对开发风险差
$$
D_{ch}=R_{ch}-R_{c0}
$$
具有同时有效上界 $D_{ch}\le\widehat D_{ch}+u_{ch}$，则
$$
\sum_h\pi_{ch}(\widehat D_{ch}+u_{ch})\le\delta_c
$$
是条件性的保守风险约束。对基线自身应使用 D_c0=0 的恒等式，上界也为 0，使可行预算内的基线保留可行性。误差界必须来自合法开发数据与正确的原生聚类，不能杜撰或测试集拟合。

最大后悔最优一般只保证弱 Pareto 性质。若需要排除可行类内的严格支配，在同一最优 t 上再最小化正权风险和，或预声明 augmented Tchebycheff；不能把平滑替代或局部驻点声称为全局 Pareto 最优。

**区分性预测**：只有共享可行类确实产生竞争时，最坏参考差距与平均风险才可能不同。不同文化使用不同策略并不要求答案语义对齐。
**证伪条件**：可行类实际可分；经验理想点误差淹没取舍；策略选择泄漏测试标签；或所谓公平收益只来自提高预算。

## 6. 怎样形成清楚的 ACL 方法叙事

一个候选主方法应解释一条真实机制，而不是把 J、L、P 全部堆进一个系统：

- 若残余错误来自整组判断，J 是 Hard 的题目层问题，L／P 是单独分析或比较。
- 若可靠的同文化表达互补，L 是主要候选；Hard 的联合支持必须先取得，MC 使用 categorical 支持，SAQ 仍缺合法支持。
- 若问题是共享成本导致的文化风险冲突，P 是文化层目标；必须先取得同一策略类的开发风险与成本。

DRO04 的最坏群体风险与 P 的参考差距不同；OT05 依赖可辩护的语义距离，不能替换 SEM 评分。二者保留比较地位。

现阶段最清楚的形式化主线是：**文化内条件化的答案决策＋共享预算下的文化风险向量**。选哪个构造作为方法取决于原生失败证据与近邻差异，不取决于公式外观。

## 7. 来源与当前资格

原生定义：[CulturalBench](https://aclanthology.org/2025.acl-long.1247/)、[BLEnD 论文](https://proceedings.neurips.cc/paper_files/paper/2024/file/8eb88844dafefa92a26aaec9f3acad93-Paper-Datasets_and_Benchmarks_Track.pdf)、[BLEnD 作者源码](https://github.com/nlee0212/BLEnD/tree/7b9c131719e7fe5f9bed0f8b855532d613cc9f2b)。
既有优化／多文化近邻与读取范围见 [CLOSEST_WORK.md](../CLOSEST_WORK.md) 和 [来源快照](../math/MULTICULTURAL_SOURCE_SNAPSHOT.json)，包括 ConCoRD、MGDA、Group DRO、STCH、CuMA、DOVE；标准 KL 投影、信息池化与 Tchebycheff 不能换名计作原创贡献。

本轮是同一作者上下文中的代数核查与整理，不是独立审稿、形式验证或完整碰撞审计。J01／LOCAL02／PARETO03 没有入选，无新方法代码／候选 G01 资格。代码状态与后续证据要求分别见 [实现索引](../implementation/README.md)、[ACL 实验协议](../experiments/ACL_PROTOCOL.md)。
