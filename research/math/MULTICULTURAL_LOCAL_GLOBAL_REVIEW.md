# 多文化的局部最优与整体最接近：五类数学模型复核

日期：2026-10-09。来源快照：culture-study/main @ f5be11213372b6ba6dbdb846e54bc1c8472b6aae。
状态：有条件的数学讨论与已有构造审查；不是已入选的新方法、完整候选 G01、实验结果或原创性裁决。本轮沿用 Research Autopilot，响应用户关于“立方体空间、多文化局部最优、整体最接近”的反馈。保留原有八项分析、J01 及其单标签/高阶限制。

## 1. 先区分三个空间与两种“局部”

对 CulturalBench-Hard 的同一原题，完整答案为 z∈Ω={0,1}⁴：四维立方体的 16 个顶点。边际置信度 p∈[0,1]⁴ 位于连续立方体；完整联合分布 q∈Δ(Ω) 位于 15 维概率单纯形。它们不是同一个优化变量。这里的坐标是同一问题的四个候选真假判断，不是把中国、印度、宗教或文化价值各当一个二元坐标。

“某文化下的最优”是条件化最优，允许各文化答案不同；“求解器陷入局部极小”是算法性质。有限状态的全局枚举能消除后者，不能解决文化知识缺失、校准错误或前者之间的冲突。原生 Hard 评分是四项全部正确；最近顶点、Hamming 距离、语义距离都不能直接代替该评分。

如果只最小化到边际 p 的欧氏距离，则
$$
\arg\min_{z∈\{0,1\}^K}\|z-p\|_2^2
=[\,1\{p_j>1/2\}\,]_{j=1}^K,
$$
因为将第 j 位从 0 改为 1 的代价差为 1−2p_j。因此“立方体最近顶点”本身严格退化为逐项判断，不能靠重新命名得到联合推理增益。平局需预先固定规则。

联合精确匹配的 Bayes 决策是 argmax_z P(z|x,c)，不是最近边际点。P 未知；模型 q 只是证据。J01 在固定边际下重估联合关系的分析仍有效，但高置信错误可被固定边际锁死，见 J01_REVIEW.md。

## 2. 一个必须保留的负面结论：共同 KL 重心可以去掉文化信息

仅在同一问题、同一语义对齐的答案支持集上，给定文化权重 w_c>0、Σ_c w_c=1 和文化条件分布 q_c，令 $\bar q=\sum_cw_cq_c$。有
$$
\sum_cw_cD_{\rm KL}(q_c\|b)
=\sum_cw_cD_{\rm KL}(q_c\|\bar q)+D_{\rm KL}(\bar q\|b)
=I_w(C;Z)+D_{\rm KL}(\bar q\|b).
$$
推导：在对数比中插入 $\bar q$，第二项求和后为 $\sum_z\bar q(z)\log[\bar q(z)/b(z)]$；第一项是联合分布 w_cq_c(z) 下的文化与答案互信息。

固定 q_c、只求 b 时，最优 b 是混合分布 $\bar q$，可作描述性总体中心。若同时改变 q_c 来缩小到 b 的距离，则在减少文化与答案的统计关联；没有额外保护时，所有 q_c=b 可令目标为零。将 b 的同一个 MAP 答案用于每种文化，可能抹去合法差异。信息重心不能自动充当文化真理。

这不意味着所有一致性都不好：在固定文化 c 内，语言/表达视角的关联可能包含可消除的噪声，但也可能含有真实信息。视角等价性、可靠性和误差多样性都需检验，不能将相关模型重复回答当成独立人类意见。

数学示例（非 benchmark 数据/实验）：两种文化的正确状态分别为 1000 与 0111，权重为 0.9 与 0.1。共同混合分布的唯一 MAP 是 1000；用它统一决策会使第二文化的整组损失为 1，虽然平均风险最小。这是“总体平均最优”与“各文化不受损”的差别，不是实际失败频率。

## 3. CUBE01：立方体上的局部近优集合与全局几何中心

形式对象：共同语义支持 Ω={0,1}^K、正的模型联合证据 r_c(z)、能量 E_c(z)=−log r_c(z)。定义
$$
E_c^{\min}=\min_z E_c(z),\qquad
\mathcal A_c(\delta_c)=\{z:E_c(z)≤E_c^{\min}+\delta_c\}.
$$
构造：
$$
\min_{b∈Ω,\;z_c∈\mathcal A_c(\delta_c)}
\sum_cw_c\,d_H(z_c,b).
$$
每种文化保留自己的 z_c；b 是共享几何原型，不是所有文化必须输出的答案。“局部”指各文化的条件化近优集合。

推导/求解：对每个 b，分别选取各 $\mathcal A_c$ 中距 b 最近的状态，再比较全部 b。这是精确有限优化；朴素代价 O(C K 4^K)，K=4 很小。固定 z_c 时，b 的每位是加权多数位，仍只是原型。δ_c=0 且各文化模式唯一时，z_c 完全固定，中心优化不能改变任何预测；δ_c 小于该文化第一/第二模式的能量差时，同样不变。δ 过大可使全部状态近优，恢复有害的多数收缩。

算法局部极小的纯数学示例：E(00)=0，E(01)=E(10)=1，E(11)=−1。单比特下降困在 00，枚举得到 11；这不代表真实文化任务已存在该能量景观。

假设与信息：r 必须包含真实的联合模型信息。若仅用独立 Bernoulli 乘积，求联合 MAP 又退化为逐项阈值。δ 保护的是模型能量，不是未知真实正确率。不同文化的 A 选项含义不同或不同题目，禁止直接比较位距离。

预测/证伪：模式间隙大于 δ 时预测不变；收益只能来自允许移动的近优状态。如果全局枚举与逐项基线完全一致，或可靠证据仅有边际，便没有该联合机制收益。对照是独立阈值、直接整组生成、匹配调用/上下文的重复查询及既有逻辑推理。J01/ConCoRD 属于必须保留的近邻。

结论：很适合解释 CulturalBench-Hard 的答案几何；跨文化共同中心须先具备对齐任务，不能把 CulturalBench 不同国家的不同题目拼成同一立方体。不是已通过的原创候选。
数学路径：H02/H06 → B04/B01 → D01；状态空间与代价推导已给出，真实联合信息条件未确立。

## 4. LOCAL02：文化内的信息重心与锚点信赖域

这是本轮优先继续推导的条件化构造。对于固定问题和文化 c，令 v 表示该文化内的等价表达/采样视角，r_cv 为同一语义支持 S_c 上的正模型分布，r_c0 为预先指定的文化锚点；ω_cv≥0、W_c=Σ_vω_cv>0。
$$
\boxed{
\begin{aligned}
\min_{\{q_c∈Δ(S_c)\}}\quad&
\sum_{c,v}\omega_{cv}D_{\rm KL}(q_c\|r_{cv})\\
\mathrm{s.t.}\quad&
D_{\rm KL}(q_c\|r_{c0})≤\varepsilon_c,\quad∀c.
\end{aligned}}
$$
最终只输出对应文化的 $\hat z_c=\arg\max_zq_c(z)$。全局解位于乘积空间 $\prod_cΔ(S_c)$；各文化不必具有相同支持集，也没有 q_c=q_d 约束。不同文化的 b 可以作为额外描述性统计，不能替换各 q_c 的决策。

实际推导：各文化子问题可分。加入信赖域乘子 α_c≥0 和归一化乘子，在正概率内求导，得到
$$
q_c^\star(z)\propto
r_{c0}(z)^{\alpha_c/(W_c+\alpha_c)}
\prod_vr_{cv}(z)^{\omega_{cv}/(W_c+\alpha_c)}.
$$
令 $h_c(z)=W_c^{-1}\sum_v\omega_{cv}\log r_{cv}(z)-\log r_{c0}(z)$、
$t_c=W_c/(W_c+\alpha_c)$，则
$$
q_{c,t}(z)=r_{c0}(z)e^{t h_c(z)}/Z_c(t),\quad
\frac{d}{dt}D_{\rm KL}(q_{c,t}\|r_{c0})
=t\,\mathrm{Var}_{q_{c,t}}[h_c]≥0.
$$
故先检查 t=1 的无约束解；若超预算，在 t∈[0,1] 上二分求信赖域边界。h 为常数时分布不变；ε=0 时直接回到锚点。目标严格凸，正输入与有限支持保证每个子问题的唯一解。正 ε 的 Slater 点为锚点；零 ε 单独处理。

成本：缓存各视角证据需 O(V|S_c|)，每次二分 O(|S_c|)。CB-Hard 支持大小为 16；调用数、token、翻译/候选生成和语义映射可能占据主要成本，未测时延/VRAM。解法无需训练基础模型，不等于整个方法无开销。

差异保持的条件性边界：自然对数下 Pinsker 给出 TV(q_c,r_c0)≤sqrt(ε_c/2)。对拥有共同语义支持的 c,d，
$$
\mathrm{TV}(q_c,q_d)≥
\mathrm{TV}(r_{c0},r_{d0})
-\sqrt{\varepsilon_c/2}-\sqrt{\varepsilon_d/2}.
$$
若右侧为正，两文化分布不可能完全相同。对锚点唯一模式的概率间隙 Δ_c，Δ_c>sqrt(2ε_c) 又保证该文化 MAP 不变。这些保护的是模型证据差异；锚点错误时也可能保护错误。对不同语义支持的文化，此 TV 对比不成立。

严格反例边界：若每个视角的联合状态分布均为独立 Bernoulli 乘积，几何池化后的 q 仍为乘积；单个候选的合并 logit 是对应视角 logit 的加权平均。这个恒等式不要求各视角的误差独立。仅套用立方体名字不产生新的高阶依赖，也不能把它计为 J01 的联合信息收益。

退化/预测/证伪：所有视角等于锚点、ε=0 时回到原模型；大模式间隙时不会改变原生预测。候选收益应来自等价视角提供的互补信息、并在有限偏移内选择更好的状态。若简单几何池化、直接重问、same-culture multilingual consensus 或匹配预算的投票解释全部作用，则新机制必要性不足。若锚点系统性错误、视角共享同一偏差、不同语言实际上改变文化条件，拒绝“保护约束改善知识”的解释。

任务映射：CB-Hard 使用同一题的整组状态，但须保留原生四行输出及整组评分；CB-Easy/BLEnD MC 使用各题自己的 categorical 支持，不沿用 J01 固定边际，因此没有其 one-hot 自由度退化。BLEnD 原始 MCQ 主要为英文，不能声称原生 MC 提供多语言视角；可讨论同文化重复模型证据，额外提示改写必须预先固定且匹配比较资源。SAQ 的跨语言支持/同义答案映射需要 label-blind 候选与资格核查；现在尚未完成，仍使用原生 SEM-B/SEM-W。

文献地位：log-opinion pooling、KL 信赖域与同文化一致性都是已有构造；Cross-Lingual Consensus 是已记录的直接近邻，CuMA 是文化条件化/平均坍缩的重要近邻。可检验的剩余问题是保护预算、答案模式间隙及联合结构如何决定真实原生得失；不能把本公式本身宣称原创。
数学路径：B01/B02 → D01/D02 → D03 → C04/H06。证据可靠性与等价视角条件待核查。

## 5. PARETO03：各文化风险形成向量，“整体”是 Pareto 权衡

令 θ 为共享决策策略/模型参数，R_c(θ) 为固定文化的真实原生期望损失。对象为风险向量 (R_1,...,R_C)，不是所有文化答案的平均文本。
$$
\min_\theta\sum_cw_cR_c(\theta)
\quad\mathrm{s.t.}\quad
R_c(\theta)≤R_c(\theta_0)+\delta_c,\quad∀c.
$$
θ_0 是实际基线，δ_c 为预先声明的容忍损失。这比使用未知的文化 oracle 最优风险更可操作。δ≥0 时 θ_0 可行；正权重下，全局最优不会被另一个所有文化风险均不更坏且至少一项更好的策略支配。神经网络的局部求解不保证找到该全局解。

更直接对应“各文化局部最优、整体最接近”的参考点形式：先固定共享可行策略类 Θ（可为冻结模型上的提示/决策策略；不一定是需训练的参数），定义
$
R_c^\star=\inf_{\theta∈\Theta}R_c(\theta),\quad
a=(R_1^\star,\ldots,R_C^\star),\quad
u_c(\theta)=\frac{R_c(\theta)-R_c^\star}{s_c},\quad s_c>0.
$
a 是各文化分别优化得到的理想风险向量，通常不对应一个可实现的共享策略；s_c 是预先声明的尺度，不是文化重要性的客观数值。此处“局部”仍指固定文化的子目标，不是求解器局部极小。若把各文化 oracle 定义在不同、更大的策略类，必须另记可行类，不能混作同一个 Θ。比较的是文化风险坐标，所以不需要将不同题目的 A/B/C/D 强行对齐。

“整体最近”可取加权 L2、平均后悔或最大后悔，选择不同会改变结论。特别是正尺度的 Tchebycheff 形式
$
\min_{\theta∈\Theta}\max_cu_c(\theta)
=\min_{\theta,t}t\quad\mathrm{s.t.}\quad
R_c(\theta)≤R_c^\star+s_ct,\quad∀c
$
直接最小化最被牺牲文化相对其自身最优的距离。可叠加上面的基线不受损约束。区别于标准 Group DRO 的 max R_c：这里先减掉各文化不可避免/可行类内的最低风险并声明尺度，不会自动把最难任务等同于最需要补偿的后悔。

数学例子（非实验）：Θ=[0,1]、R_1(θ)=θ²、R_2(θ)=(1−θ)²，两个文化分别在 θ=0 和 θ=1 最优，理想向量为 (0,0) 但不可共同实现。0.9/0.1 加权平均在 θ=0.1 达到最优，风险为 (0.01,0.81)；同尺度最大后悔在 θ=0.5 达到最优，风险为 (0.25,0.25)。因此“整体最优”必须声明对谁、用什么距离、容许什么损失，不是一张立方体图自动决定。

精确全局最优的最大后悔仅保证弱 Pareto 最优：所有坐标严格下降会严格降低最大值，但非瓶颈坐标下降可能仍平局。若需排除被支配的平局，可用字典序二阶段（先最小化 max u，再在最优集合内最小化 Σu），或明确采用增强目标 max u+ρΣu、ρ>0；后者会略改变原最大后悔取舍。增强目标在每个风险坐标严格递增，因而被另一可行策略支配将使目标严格更小，这是 Pareto 性质的直接证明，不保证神经求解的全局性。

现实边界：R_c^\star 未知，单文化训练/提示试验的最好观测也不是其证明。不可从测试标签调出“oracle”、尺度和权重，再报告同一测试改进。实际需合法开发上固定参考策略/尺度、风险估计误差和新确认；对未知 oracle 可保留理论形式，或换成预先锁定的参考风险并诚实称为参考点差距。只有共享策略类有真实资源/参数/调用限制，理想点不可实现的问题才有内容；任意独立文化 oracle 的笛卡尔积若可行，问题便退化为各自最优。

经典参考点/Tchebycheff 是已知多目标构造，不计新方法。Lin 等 ICML 2024 的 Smooth Tchebycheff 已有光滑化及全局最优/驻点的区分：本轮实际读取 §2 和 §3.3，未借其“mild conditions”省略原定理条件。Xi-L/STCH @ 869217dc8d73f2d002c353ba1d65be84dbf1ea4c 的 PSL 入口使用 ideal/nadir 归一化和 logsumexp；MTL STCH.py 则含 warmup、平均损失参考及对数比变换。这些设置不是上面的真实原生风险/oracle 差距，不能直接移植数学结论。源码静态读取，未执行。

求解视角：对可微代理损失 L_c 的梯度 g_c，MGDA 解
$$
\alpha^\star=\arg\min_{\alpha∈Δ_C}\|\sum_c\alpha_cg_c\|_2^2,\quad
\bar g=\sum_c\alpha_c^\star g_c.
$$
凸包投影的一阶最优性给出 $(g_c-\bar g)^\top\bar g≥0$，因而当 $\bar g\ne0$ 时 $g_c^\top(-\bar g)≤-\|\bar g\|^2<0$：是所有代理损失的共同一阶下降方向。零向量只给 Pareto 驻点；非凸时不证明全局 Pareto 最优。小步长、精确梯度和代理损失光滑性是条件，不保证有限训练步骤后的原生准确率。

复杂度：P 个可训练参数、C 文化，形成 Gram 矩阵朴素 O(C²P)，每文化梯度还需计算/存储；小 QP 不代表反向传播便宜。若使用 LoRA 或 MGDA-UB，必须说明改变的参数空间/度量及其假设。未取得合法开发数据与 GPU/预算，当前不推荐直接微调队列。

预测/证伪：梯度存在共同下降方向时可能同时改善代理目标；冲突完全抵消时应停在驻点或承认权衡。若训练代理下降而 native Hard/MC/SEM 或某文化恶化，就没有原生不受损保证。对照为单文化优化、固定宏平均、匹配资源的普通 LoRA 及原始 MGDA；不把 MGDA 换文化名称当创新。

源实现：Sener & Koltun 2018 的真实训练入口与 MinNormSolver 已读。入口可选梯度归一化，含非 SGD 优化器；原始求解器使用 0.999/0.001 端点近似及迭代容差。因此上面的精确共同下降证明不能自动认证该代码、Adam 或神经训练。数学路径 D01 → H02/H05；经验风险估计和原生代理关系未知。

## 6. DRO04：最坏文化风险，作为必要比较复用 M08

$$
\min_\theta\max_cR_c(\theta)
=\min_{\theta,t}t\quad\mathrm{s.t.}\ R_c(\theta)≤t
=\min_\theta\max_{\pi∈Δ_C}\sum_c\pi_cR_c(\theta).
$$
最后一式对固定 θ 由线性目标在单纯形顶点取得最大值得出，不主张非凸 min/max 能交换。标准指数权重更新为 $\pi_c^+\propto\pi_c\exp(\eta\hat R_c)$。该框架关心最坏群体，不要求文化输出相同，也不保证每个文化都不受损。

已有 M08 应复用，不新增候选名额。Sagawa 等 ICLR 2020 已覆盖 Group DRO，loss.py 的组均值与 adversarial probability 更新已读；代码包含 group adjustment、归一化/BTL 分支与估计计数，不能忽略其实际设置。

预测/证伪：有限容量下会偏向高损失群体，可能牺牲平均或其他群体；最坏训练风险下降不证明最坏测试风险下降。弱文化小样本、噪声和不可约难度会影响估计。对照为同预算宏平均、固定权重与正则化 Group DRO。若它已解决有后果的残余问题，则优先简化，不制造新方法。

资源/任务：须有合法 non-test 开发/训练来源；保持原生文化损失和分母。当前缺这些数据及实测，因此仅作框架/对照。数学路径 D01/D02（复用 M08），经验可靠性条件未确立。

## 7. OT05：Wasserstein 重心，讨论语义最近但保留评分不匹配

在固定且有依据的语义支持与地面代价 d(a,b) 上，
$$
W_d(r_c,b)=\min_{\Pi_c≥0}
\sum_{i,j}d(a_i,a_j)\Pi_{c,ij},\quad
\Pi_c\mathbf1=r_c,\quad\Pi_c^\top\mathbf1=b,
$$
$$
b^\star=\arg\min_b\sum_cw_cW_d(r_c,b).
$$
固定有限支持时这是可写为联合线性规划的标准重心；不保证唯一。加熵并用 Sinkhorn 求解改变了原目标，需保留正则化/容差；b 仍是总体描述，不应作为每文化统一答案。

关键推导：若按 exact-match 对全部不同答案用 d(a,b)=1[a≠b]，最优耦合匹配 Σ_a min(r(a),b(a)) 的同状态质量，其余质量全部代价 1，故 $W_d(r,b)=\mathrm{TV}(r,b)$。语义几何的额外好处来自改变地面代价，不由 exact-match 原生损失自动认可。Hamming/embedding 的“接近”不能推出四项全对。

成本：M 个状态的耦合为 M² 量，固定支持的 Sinkhorn 核更新约 O(CM²) 每步，另计语义编码/候选采样；16 状态是小矩阵，但 SAQ 自由文本支持/文化人群分布并未由标签给定。

预测/证伪：合理语义代价可能改善别名/表达鲁棒性；若代价把错误文化答案当成近义，运输距离下降而 native SEM/MC/Hard 不升，则应拒绝代理有效性解释。比较 exact 0/1 运输/TV、无语义代价、同预算 KL/直接回答，保留原生 scorer。

相关工作：Cuturi & Doucet ICML 2014 已覆盖 Wasserstein barycenter；DOVE（ICML 2026 正式元数据与 arXiv v4 分开保留）已在文化价值评价中使用 codebook + debiased unbalanced OT，真实源码 uot_cost/prepare_sem_matrix/calculate_debiased_uot 已读。它衡量人类长文本价值分布，不是本项目 CB/BLEnD 的替代 scorer。本轮不添加 DOVE 为新 agreed benchmark，不宣称 OT+文化是原创。
数学路径 D01 → B06/H06；语义地面代价与人群分布的识别条件待核查。

## 8. 讨论优先级与可区分的下一步

| 讨论次序 | 框架 | 保留理由 | 主要缺口 |
|---|---|---|---|
| 1 | LOCAL02 | 文化内聚合、文化间分别决策；有明确保护预算/求解/模式间隙预测；适合冻结 1B–7B 的理论讨论 | 既有池化与一致性覆盖；可靠锚点/等价视角/原生效益未知 |
| 2 | CUBE01 / J01 | 精确区分边际近点、联合 MAP、算法局部极小，直接贴合 Hard | 多答案联合信息必要性与跨文化语义对齐未建立 |
| 3 | PARETO03 | 以文化分别最优的风险构造理想点，最大后悔表达整体最近；跨任务文化风险可用 | 未知 oracle/尺度/共享可行类，合法开发/代理到原生/梯度成本未闭合 |
| 4 | DRO04 | 必须保留的强简单公平性比较；复用 M08 | 已有方法，无法单凭套用构成新贡献 |
| 5 | OT05 | 解释语义空间的整体最近及代理边界 | 地面代价、任务匹配与 DOVE 等近邻；不宜先扩展 |

这是数学讨论的优先级，不是 method-selection 的完整全池排名/前15批准。五类框架不计为五个原创候选；已有机制/复用 M08/边界分析分别保留。当前 admitted novel pool=0/20，selected methods=0/15；没有运行 verify_methods，也不创建虚假通过记录。

本轮只给有条件的比较问题：在固定本地文化条件与语义支持下，额外视角的收益能否超过同预算重问/已有池化；信赖域的模式稳定边界是否与原生得失对应；原生平均与各文化风险是否冲突。尚无已执行诊断或候选实验矩阵。代码/完整 G01 继续等待可信原生基线/强简单替代逐题结果、合法开发和新确认及候选池/原创性前提；旧基线代码保持 generated_unexecuted。

## 9. 本轮联合阅读的范围与边界

新增主来源与实际实现：

- [CulturalBench ACL 2025](https://aclanthology.org/2025.acl-long.1247.pdf)：§2–4 的多答案构造与整组评分复读。正式 1696 原题与项目锁定发布版 1227 区分，后者与 4908 Hard 行不变。
- [BLEnD NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/file/8eb88844dafefa92a26aaec9f3acad93-Paper-Datasets_and_Benchmarks_Track.pdf)：原始共同问题/不同文化与语言的结构复读；nlee0212/BLEnD @ 7b9c131719e7fe5f9bed0f8b855532d613cc9f2b 的 MC/evaluation_utils/exact_match 源码及 China_questions.csv 七行读取。SEM 参考别名、排除、计数是 scorer 的信息，不能作为方法推理输入。
- [Multi-Task Learning as Multi-Objective Optimization](https://papers.nips.cc/paper_files/paper/2018/file/432aca3a1e345e339f35a30c8f65edce-Paper.pdf)：§3.1–3.3；isl-org/MultiObjectiveOptimization @ bf5bbb30371489a47f6440691d8934b70f7dfc3b 的 train_multi_task.py、min_norm_solvers.py 及 numpy 版。未执行，非文化基线的已复现结果。
- [Smooth Tchebycheff ICML 2024](https://proceedings.mlr.press/v235/lin24y.html)：官方元数据；[arXiv v3](https://arxiv.org/pdf/2402.19078) §2 的参考点/Tchebycheff 与 §3.3 的全局/驻点区分实际读取。官方链接的 PDF 返回不支持 content-type、替代 PMLR PDF 也未取到，不宣称正式 PDF 全文已读取；IIASA WP-79-066 原文被访问墙挡住。Xi-L/STCH @ 869217dc8d73f2d002c353ba1d65be84dbf1ea4c 的 STCH_MTL/LibMTL/weighting/STCH.py 和 STCH_PSL/run_stch_psl.py 全文静态阅读，未执行。
- [Group DRO](https://arxiv.org/pdf/1911.08731)：§2–3；kohpangwei/group_DRO @ cbbc1c5b06844e46b87e264326b56056d2a437d1 的 loss.py 与 README 阅读。不改变 native 文化任务。
- [Fast Computation of Wasserstein Barycenters](https://proceedings.mlr.press/v32/cuturi14.pdf)：§2–3；经典求解/几何为已有数学，未完整复现该作者算法。
- [CuMA ACL 2026](https://aclanthology.org/2026.acl-long.1265.pdf)：§2–3、Theorem 2.1 与 Appendix 的定位。定理采用单分量指数族/高斯代理；不能推出任意文化条件化稠密 LLM 无法表达多峰。Throll/CuMA @ 0ba7659e9ec166818c4b8a49a16819d1474c797e 的 models/cuma_model.py 路由/LoRA 部分实际静态读取；top-k 实现对 softmax 后概率再次 softmax，不直接假设等价于论文在选中 logits 上归一化。非本项目性能或 scorer 资格。
- [DOVE arXiv 2604.06210v4](https://arxiv.org/html/2604.06210v4)：§3.2–3.3、Appendix F.4；[ICML 2026 元数据](https://proceedings.mlr.press/v306/lee26bj.html)正式 PDF 抓取失败，不假装全文已读。JaehyeokLee-119/DOVE @ fe9aa23d5b61857c50dbc05aa3bfa07c1c1928d9 的 src/evaluation/UOT_measure_alignment.py 实际阅读 UOT、语义代价和自距离去偏。
- [CAReDiO ICML 2026](https://proceedings.mlr.press/v306/yao26p.html) 仅定位元数据；正式 PDF 与尝试的 arXiv HTML 未成功取得，不给出其算法排除结论。

检索日期 2026-10-09；检索用文化平均坍缩、Pareto/group DRO、Wasserstein barycenter、文化条件化/多元对齐、具体标题与作者仓库。详见 MULTICULTURAL_SOURCE_SNAPSHOT.json 的查询、版本定位和读取范围；原始工具响应仅留在会话，不构成可回放的完整碰撞包。当前是同一上下文的有界来源比较，未做独立新颖性裁决/全家族饱和；缺失代码/全文不是不存在先例的证据。

本轮没有科学代码、测试、求解器运行、评分、数据/模型下载、训练、推理或 GPU/SSH 操作。数学恒等式、反例和条件性界均为分析，不是 benchmark 观测。下一步先以原生证据分辨校准、知识缺失、联合关系、表达变化与预算效应，再决定是否需要新方法。
