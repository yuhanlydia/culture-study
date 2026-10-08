# Culture Study：后台研究作者目标

## 本轮目标与范围

用户在同一 ACL 项目中选择 CulturalBench + BLEnD，要求 1B–7B 小模型可以运行，通过数学建模与优化改进已有方法，生成 idea、代码及完整实验设计，写入 https://github.com/yuhanlydia/culture-study 并后台完成。

当前入口为从零探索。此前只恢复了项目聊天摘要，未取得另一个聊天全文；检索失败不代表已有方法或结果不存在。本仓库初始化时确认为空，因此不能假定已有数学卡、代码、实验或通过的科学 gate。

本轮源文件交付目标为本仓库 literal main。沿用已存在的 public 可见性。HF 输出目的地与实际计算资源未知；本轮先完成用户指定的 GitHub 研究材料/代码/设计，不创建或上传 HF，也不将未知记录为明确不用。

## 后台路由与授权来源

此前对话已说明当前没有持续 Work 目标的启动接口，可用的是定时自动化，并询问是否改用该方式。用户随后继续要求“写到这个里面”“后台完成”，并明确给出本仓库。本轮据此采用可用的 cloud-scheduled authoring 后台任务推进，而不是再次询问是否继续。

这是一项实际生产任务，不是提醒或证据监控。真实任务身份、启用状态、请求运行与观察时间见 research/background-task.json。任务创建/请求运行不证明作者工作已经完成，也不证明具有持续 Work 模式或连续活跃状态。

## 作者工作及顺序

1. **来源与原生协议核查。** 联合阅读 CulturalBench、BLEnD 的原始论文全文、作者实际源码/基线实现、发布数据字段/IDs/splits/labels/原生 scorer。固定源版本、读取范围和缺口，核对当前相关方法；保留来源与推断的区别。形成具体失败机制、简单替代、Parent Problem、适用 Natural Gate 0、方法碰撞与 IPCG 证据。不得编造实测观测或 PASS。
2. **数学发现与选择。** 新探索建立约 20 个有依据的候选卡，逐卡包含形式对象、假设、关键推导、构造、独特预测、证伪条件、强/简单比较、方法碰撞和任务适用性。全部实际核验，完整排序后选择前 15；不足则保持缺口，不能补名字或装饰方程。已覆盖机制作为 comparator，不包装为原创贡献。
3. **方法与比较代码。** 在实际代码生成前提满足后，完成选定主方法以及必要基线、控制与消融。交付推导到代码映射、配置、native 数据适配、推理/必要训练接口、原生评分、日志及结果收集、来源固定和实际获取/校验命令。不能交付伪评价器、pass/TODO 骨架或随机数据替代实验。
4. **完整 G01 设计。** 覆盖两个 agreed benchmark 的完整原生任务与分母、1B/7B 模型、公平资源比较、机制消融、dev/调参/独立 confirmation 隔离、统计单位与精度、多重比较及效应/失败规则、准确命令、条件性预算/设备假设和有限 repair/park/stop。test 不参与拟合、参数选择或标签检索。
5. **方法边界与交接。** 在适用 code/experiment-design 边界使用当前 method-verification 证据和 verify_methods 只读检查。不可运行/不可用检查明确保持待验收，不伪造日志、批准或通过状态。生成完整 README、AGENTS、LOCAL_AGENT_RUNBOOK.md 和首轮 WEB_HANDOFF；具体运行命令只在真实接口完成后写入。
6. **交付与关闭。** 每个实质里程碑提交 scoped 文件及进度到 main，保留当前父提交并回读 exact commit/content。作者产物完整交付后报告文件/commit，停用同一任务。平台中断时保存已完成产物与下一步，续接同一任务；不重置历史或开重复写入任务。

## 方法卡最低内容

每个候选必须回答：具体失败是什么，优化对象是什么，在哪些假设下成立，推导如何产生实现，为什么强简单替代不能解释全部作用，什么原生可观察预测区分机制，出现什么结果会证伪，哪些论文/源码已覆盖关键机制。

## 角色及实际执行

角色为 web_supervisor。源文件审查、作者生产和 GitHub 交付由后台任务完成；新科学代码与设计标记 generated_unexecuted。当前没有运行项目 tests、模型、训练、推理、科学 scorer 或 benchmark。

Local 后续通过真实 SSH/native Conda 资源执行验收和实验。本任务不连接 SSH/GPU、不安装运行服务、不下载数据或大模型、不使用 Docker/其他容器、不启动付费计算。未知硬件/预算不能借用其他项目。后台成功、代码交付、软件验收和科学有效性分别记载。

## 完成判据

| 产物 | 完成要求 |
| --- | --- |
| 文献/实现/benchmark 审查 | 真实 source/version、读取范围、局限及碰撞证据可追溯 |
| 数学池与选择 | 合格卡逐项审查、全池排名、前 15 选择与排除理由；缺口不伪装完成 |
| 方法源码和比较 | 选定方法与必要基线/控制/消融接口完整，具有推导映射和来源/配置 |
| 原生完整设计 | CulturalBench 与 BLEnD 全部约定评测覆盖、准确 scorer/分母及 dev-confirm 隔离 |
| Local 交接 | README/AGENTS/runbook/WEB_HANDOFF 指向真实源文件、命令、获取/校验/日志/修复/验收 |
| 实际交付 | main 上获得 exact commit/readback；准确说明 generated_unexecuted 和待 Local 验收 |
| 后台关闭 | 作者交付完成或独立工作耗尽且遇到真实阻塞后，保存下一步并停用同一任务 |

不预先保证性能提升、原创性最终成立或 ACL 录用。实验结论依赖实际原生结果、E04 和独立确认。保留所有负面、失败、缺比较和未完成记录。

## 技能及续接

使用实际可用的 Research Autopilot 插件及适用模块，不将私有 skill 源文件复制到公开仓库。当前读取过插件入口、workflow-harness、web-background-work、initial-intake、artifact-contracts、repository-round-trips 与 host-adapters；后台进入数学/代码/G01 边界时读取相应模块及真实 source revision。

每次首先读取 research/PROGRESS.md、research/workflow-checkpoint.json 与本文件，核对最新 main 和真实 task 身份。缺失前提阻塞受影响后代，继续独立合法工作。完成一个实质可审查里程碑，不只更新待办；本次初始化不算文献、数学、代码或设计完成。
