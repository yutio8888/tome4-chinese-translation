# Paseo 历史终态译文残余缺陷审计 pilot v1

状态：探索性 pilot 已完成；结果不是独立人工 ground truth。

日期：2026-08-27

本实验从 [Paseo provenance snapshot v1](../paseo-provenance-snapshot-v1/README.md) 的 P2 `DONE` 任务中按审核链分层，先抽任务、再从该任务的终态 contextual input 抽一条译文。模型只读取匿名 `H001`–`H020` 的 source、target 与当时冻结的 context，不读取任务 ID、模型家族、旧 finding 或旧 verdict。

这是小样本探索性残余审计，不是因果实验。四层的题材和批次结构不同，原始译文生成者仍未知；因此层间差异不能直接归因于 reviewer 或 orchestrator。没有独立人工审核者时，模型 finding 只作为候选，后续必须逐条按固定源码标为 `confirmed`、`refuted`、`indeterminate` 或 `unreachable`，并如实称为源码约束裁决。

重建抽样：

```bash
node select.mjs \
  --repo /path/to/tome4-chinese-translation \
  --snapshot ../paseo-provenance-snapshot-v1/SNAPSHOT.json \
  --out .
```

`HOLDOUT.json` 是模型可见输入；`PROVENANCE-KEY.json` 和 `SAMPLING.json` 不提供给模型。选择器要求生产仓库 HEAD 与快照记录完全一致。

## 结果

五条完整任务路线都通过运行时身份、schema、覆盖和顺序检查。纯路线的候选数为 Codex 1、Opus 2、Fable 1、GLM 0；Opus+Fable Advisor 复合路线为 0。三条不重复候选经固定源码裁决后为 1 条 `confirmed`、2 条 `refuted`：

| 候选 | 路线 | 裁决 | 要点 |
| --- | --- | --- | --- |
| H013 | Codex、Opus | confirmed | 把“玩家的闪避面对下个房间兽人时表现如何”写成“闪避对兽人如何作用”，改变了防御关系。 |
| H016 | Opus | refuted | 增加的施加者死亡移除和能够行动条件均由运行时源码确认，且是历史任务明确要求补足的机制。 |
| H020 | Fable | refuted | 项目冻结术语明确规定 `darkness=暗影`，不存在候选声称的“应为黑暗”错误。 |

唯一确认项来自 S3（GPT 修改、Grok-only contextual review、GPT 编排），而不是 GPT-only reviewer 层。按 reviewer 组合汇总，本 pilot 的 15 条 GPT-only reviewer 样本中发现 0 条确认缺陷，5 条非 GPT-only reviewer 样本中发现 1 条。这只是模型候选联合集上的确认下界：其余 17 条没有做独立逐条源码审计，四层题材也不匹配，不能将 `0/15` 与 `1/5` 当成稳定缺陷率或 reviewer 因果效应。

Advisor 删除了纯 Opus 的两条候选，既删除一条误报，也删除唯一确认缺陷；因此本次没有带来净改进。完整结构化结果见 `RESULT.json`，逐条证据见 `ADJUDICATION.json`。

## 解释

这个 pilot 没有为“GPT-only 历史审核留下更多残余缺陷”提供证据，但也远不足以否定 GPT 系统性偏差。它更直接说明：跨族复审本身不保证无盲点，且自然历史样本受题材、批次、上下文和工作流强烈混淆。下一步应转向带客观变异标签的 reviewer × translation-origin 交叉实验，而不是扩大对这 20 条自然样本的事后解释。
