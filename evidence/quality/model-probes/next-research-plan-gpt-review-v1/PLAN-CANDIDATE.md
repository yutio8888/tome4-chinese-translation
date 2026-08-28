# 下一步研究候选方案 v0

## 当前证据

- 24 条受控变异实验包含 12 个注入变异和 12 个历史终态 controls；源码裁决发现其中一个 control 自带自然缺陷。四路线对注入变异的单次命中为 12/12、11/12、12/12、11/12。
- 新 UI/日志实验使用 4 个注入变异和 4 个推理前完整源码核验的 controls，完全相同地运行三次。四路线三轮命中依次为 `4/4,4/4,4/4`、`3/4,3/4,2/4`、`3/4,3/4,4/4`、`2/4,4/4,4/4`。
- 三轮中，较直接的两个变异在所有 12 个路线运行中均被命中；条件主体变异为 6/12，运行时持续时间变异为 10/12。48 个 control 机会中出现一个经固定源码驳回的候选。
- 这些实验不能估计自然残余缺陷率、语言质量或 reviewer × translation-origin 同族偏差，也不足以形成稳定模型排名。

## 阶段一：源码上下文消融

建议目录：`controlled-mutation-context-ablation-v1/`。

从未进入现有实验或 prompt 设计的新类别中冻结 36 条：18 个源码验证 clean controls 和 18 个注入变异。按证据需求分成三个层级，每层 6 个变异和 6 个 controls：

1. `lint_detectable`：占位符、参数顺序、格式数量等确定性检查可发现。
2. `surface_bilingual`：仅凭 source/target 可以判断。
3. `runtime_source_required`：必须跟踪源码调用、状态主体、持续时间或总量/逐回合关系。

建立两个输入臂：A 只含 source/target；B 含 source/target 和脱敏 fixed source context。四个 reviewers 都审核两个输入臂，每个输入臂逐字节重复两次，共 16 次 reviewer 调用。所有路线独立首审，不讨论、不交换输出。

主要指标是 runtime 层 B 相对 A 的配对 recall 增量。次要指标包括各层 recall、clean specificity、FINDING-only、正确 UNCERTAIN、两次运行的逐条一致率、成本和确定性 lint 覆盖率。

决策规则：若 source context 改善 runtime recall 且没有明显增加 control 候选，后续 reviewer 实验统一提供 fixed context；若 lint 可确定性覆盖，则从模型主分数中剥离。controls 在推理前不能证明干净则不运行。两轮完成后停止本设计。

## 阶段二：Reviewer × Translation Origin pilot

建议目录：`reviewer-origin-factorial-pilot-v1/`。只有阶段一确定 reviewer 标准输入契约后启动。

选择 16 个新的、可由源码完整验证的原文条目。由四个模型家族分别生成译文，共 64 个 origin variants。对所有基础译文逐条源码核验，天然有客观缺陷者不得直接作为 clean control。使用平衡 Latin-square 分配机械、可逆、有源码证据的变异，使每个 origin、类别和位置上的 mutant/control 数量相等。

四个 reviewers 对匿名化、固定顺序的全部 variants 独立审核。reviewer 部分运行两次。主要对比是 GPT reviewer 审核 GPT-origin 变异的检出率，与其审核非 GPT-origin 变异的检出率之差；同时报告完整 reviewer × origin 交互、clean false-positive rate 和逐条重复稳定性。

只有在两次运行方向一致、效应不由少数条目独占、controls 不能解释差异、控制条目与变异类别后方向仍保持时，才称为同族偏差信号。pilot 信号弱或区间宽时报告证据不足，不事后追加样本追求显著性。

## 阶段三：前瞻性自然残余审计

建议目录：`prospective-residual-audit-v2/`。

从未进入历史 finding/reference 的总体中确定性抽样至少 40 条，按 same-family-only、cross-family 等历史流程特征分层，并尽量匹配题材、任务年代和上下文质量。四路线独立提名候选；无论模型是否提名，每条都必须完成固定源码审计，输出 `confirmed`、`refuted`、`indeterminate` 或 `unreachable`。

该实验只估计客观机制残余率，不声称独立人工语言审核，也不裁决文采、社区偏好或文化语气。

## 统一产物与门禁

每个新实验先提交冻结点，再运行推理；保留 `EXPERIMENT.json`、prompt、schema、RAW、候选、裁决、`RESULT.json` 和字节重建 verifier。结果必须区分实测、派生统计和人工建议，不得用 union/consensus 多数票代替源码裁决。
