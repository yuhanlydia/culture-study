# Culture Study

面向 ACL 的跨文化小语言模型研究。当前研究入口为 CulturalBench + BLEnD，模型范围为 1B–7B，重点是已有方法的失败机制、数学建模与优化。

## 当前阶段

已收到生成研究 idea、代码和完整实验设计并写入本仓库的指令。仓库初始化只建立任务与续接记录；文献核查、数学审查、代码、实验设计和实际实验结果尚未完成。

后台作者任务以实际定时自动化推进。它执行研究与代码编写，并按仓库记录续接；后台请求、源码交付、软件验收和科学结果分别记录，不能相互替代。

## 任务入口

- [长期目标与完成判据](LONG_TERM_TASK.md)
- [执行边界与协作说明](AGENTS.md)
- [当前进度](research/PROGRESS.md)
- [后台状态记录](research/background-task.json)
- [首轮研究交接](rounds/r001/WEB_HANDOFF.md)

完成后应包含：原始论文/作者源码/原生评测核查，约 20 个有依据的数学候选及逐卡审查、完整排名和前 15 选择，选定方法的完整实现与公平比较代码，覆盖两个 benchmark 的 G01 实验设计，README/AGENTS/LOCAL_AGENT_RUNBOOK.md/WEB_HANDOFF.md 和准确运行命令。

所有新研究代码与实验设计在本 Web 作者阶段标记为 `generated_unexecuted`。科学项目测试、模型运行和实验评分由后续 Local 验收提供。当前没有跑分，也没有性能提升结论。

## 交付范围

用户指定交付到 `yuhanlydia/culture-study` 的 `main`；沿用仓库当前公开可见性，不改变设置。Hugging Face 输出目标与实际 GPU/预算尚未知；本轮交付的是研究材料、代码和设计，不创建 HF 仓库或上传权重。

## 数学优化方向讨论

已保存 [研究要求](research/MATHEMATICAL_MODEL_BRIEF.md)、[答案集合优化推导](rounds/r001/ANSWER_SET_OPTIMIZATION.md) 和 [来源核查](rounds/r001/SOURCE_AUDIT.md)。这是一个未入选的数学讨论稿，包含原生损失、目标/约束、KKT、反例和失败边界；尚无方法代码、完整 G01 或科学结果。用户最新要求和后台设置已续接，后台实际执行状态仍未获证。
