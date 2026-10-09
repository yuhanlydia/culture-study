# 1B／7B 实现索引与数学映射

状态：generated_unexecuted。本目录连接真实源码，不提供一套重复的示例实现。
当前源码为冻结模型的原生基线、评分桥接和证据诊断；J01／LOCAL02／PARETO03 尚未实现，不存在可调用的候选 solver 或训练入口。

## 1. 当前模型与计算范围

| 模型键 | 输入模型 | 版本／访问 |
|---|---|---|
| llama_1b | meta-llama/Llama-3.2-1B-Instruct | 1B 类；Local bind 固定完整 revision，复用合法 gated 访问 |
| qwen_7b | Qwen/Qwen2.5-7B-Instruct | 7B 类；a09a35458c702b33eeacc393d103063234e8bc28 |

冻结模型、无训练、单设备顺序驻留、batch=1、bfloat16、eager attention；实际 GPU／VRAM、CPU／RAM／磁盘和预算待 Local 核查。7B 类权重本身约为参数数 × 2 bytes，另加激活、缓存和运行开销；不能据此宣称任意显存都可运行。

这两个模型来自不同家族，其差异不能单独用来证明参数规模的因果规律。本轮不扩大默认模型矩阵。

## 2. 实际源码与公式的对应

| 已存在源码 | 数学／数据契约 | 输出 |
|---|---|---|
| [assets.py](../../culture_study/assets.py) | 固定模型、数据、scorer 输入身份 | bindings／acquisition／校验 |
| [prepare.py](../../culture_study/prepare.py) | 原生任务空间与完整 IDs；标签不构造提示 | 四个 task JSONL、coverage |
| [inference.py](../../culture_study/inference.py) | 贪心生成与完整标签序列 log likelihood | 每个 native unit 的原始答案、token 分数与成本 |
| [official.py](../../culture_study/official.py) | 固定作者 scorer／parser 函数 | 原生桥接函数与源身份 |
| [scoring.py](../../culture_study/scoring.py) | CB 四判断全对；BLEnD 原生 MC／SEM | 原生 score／outcomes、SAQ parity |
| [census.py](../../culture_study/census.py) | 同题基线与简单替代的残余失败 | 原始证据，机制字段保留待审查 |
| [likelihood_audit.py](../../culture_study/likelihood_audit.py) | 源码修复前后的完整标签分数与输出对照 | 全部单位 comparisons、audit，不产生 benchmark 分数 |
| [io.py](../../culture_study/io.py) | 身份、完整性与有限数值 JSON | SHA-256／manifest／原子输出 |
| [CLI](../../culture_study/__main__.py) | 上述真实接口 | bind、acquire、prepare、run、score、parity-saq、census、audit-likelihood |

## 3. 标签概率与 J01 输入证据的区别

令 x 为真实 chat template 渲染后的提示，标签 h 的 token 序列为 t1…tK。
完整标签基线计算
$$
s_h=\sum_{k=1}^{K}\log P_f(t_k\mid x,t_{<k}),\qquad
\widehat h=\arg\max_hs_h.
$$
对前缀互斥的规范标签，保留
$$
p_h=\frac{e^{s_h}}{\sum_{h'}e^{s_{h'}}}.
$$
这是“模型输出落在这些合法标签前缀事件内”的条件概率，不是已校准的文化真值概率。
新增 label_probabilities 字段只提供这种证据记录，不改变 argmax 答案；direct arm 仍没有该概率字段的实测内容。

CB Hard 的四个 p_True 可作为之后审查 J01 的一阶证据。现有 runner 没有联合查询 m_jk，也没有 q solver；不能据此声称 J01 已完成。
CB Easy／BLEnD MC 的 categorical 概率不具有固定边际 J01 的联合自由度。

## 4. 本轮 7B 内存与数值修复

旧实现对完整长度 L 的 logits 全部转换为 float32 并做 log-softmax。新实现只处理标签预测位置 P−1…P+K−2：
$$
s_h=\sum_{k=0}^{K-1}
\log\operatorname{softmax}(\mathrm{logits}_{P-1+k})[t_{k+1}].
$$
对数概率临时张量从 O(LV) 改为 O(KV)，V 为词表大小；底层模型仍输出 O(LV) logits，权重与其他激活成本也仍存在。
标签 teacher-forcing 关闭不用的 KV cache，标签循环及时释放 float32 临时张量。

保留完整标签所有 token、prefix identity 检查、真实 continuation 上下文上限、未归一化 argmax 与确定性 tie 规则。不会截断原生提示。
非有限 label logprob 会停止该 unit；JSON 写入拒绝 NaN／Infinity，避免把坏数值当有效证据。

这些是源码层计算与内存分析。没有测得峰值节省、速度收益或软件数值一致性；use_cache=False 与张量切片的实际数值资格仍待 Local。

## 5. 修复的完整 native 接受入口

Local 在同一准备输入、模型快照、配置和硬件上，分别保留旧／新源码的完整 categorical run。读取先于此修复的实际 commit 与本轮交付 receipt，不能修改 old manifest，也不能续写旧 source_digest 的目录。

真实新增 CLI：

~~~bash
conda run -n culture-study python -m culture_study audit-likelihood \
  --prepared "$ACL_PREPARED_DIR" \
  --left-run "$ACL_OLD_LIKELIHOOD_RUN" \
  --right-run "$ACL_NEW_LIKELIHOOD_RUN" \
  --out "$ACL_LIKELIHOOD_AUDIT_DIR"
~~~

变量由 Local 绑定到真实绝对路径。命令是已实现的 inner argv；执行仍属于已有 run_harness 的 admitted task。

审查 audit.json 与全量 comparisons.jsonl：标签 tokenization、每标签 logprob 差、原始／strict／final 答案变动、调用／处理 token 数及观测峰值。数值容差须在结果前给出理由；该工具只报告，不从观察结果挑容差，不给 gate PASS。
有答案变动、非有限值、输入／模型／硬件差异或不完整 run 时，保留失败，停止受影响接受；再以官方／已验证 faithful scorer 检查原生行为，遵守有限修复预算。

## 6. 候选代码边界

| 数学构造 | 所需后续实现 | 当前缺口 |
|---|---|---|
| J01 | 文化条件联合查询、16 状态凸求解、残差、预算匹配对照 | 原生残余机制／可靠联合证据；Parent／池／选择／碰撞资格 |
| LOCAL02 | 合法 view 支持映射、几何池化／KL 预算求解、κ／触边诊断 | 视角等价与支持资格，原生可靠性、合法开发／确认 |
| PARETO03 | 固定策略类风险／成本、共享预算 LP、统计风险保护 | 真实共享约束与合法开发估计；原生风险／成本、选择资格 |

这些是数学到实现的待办映射，不是未完成函数或可调度命令。缺口不能由手工 case、测试标签调参或假源码验证回执补齐。


## 7. 原生语言列输入修复

新 prepare.py 从 sources.lock.json 的 saq_input_contract 读取每个文化／语言的实际 question 列；
prompt 模板列保持分别绑定。14个非英语文化采用 English→Translation、本地语言→Question；
US／UK 保留国家特定 Question 与单一 English cell。
每题 source 和 input_digest 记录 question_column、prompt_column、contract_id；
coverage 记录完整映射，源 commit 不同或文化／语言映射缺失时停止。

这是依据固定发布字节修复既有基线，不是候选 solver。原始 ID／标签／SEM 函数和14-run矩阵保留。
[证据与推导](../model/NATIVE_EVIDENCE_CONTRACT.md)、
[Local 新输入接受](../../LOCAL_AGENT_RUNBOOK.md#native-language-column-repair)、
[逐文件来源](../sources/NATIVE_VIEW_AUDIT.json)提供完整影响与下一动作。
新旧输入不相同，不能用 audit-likelihood 将该修复认证为“数值等价”；需独立原生重资格。
