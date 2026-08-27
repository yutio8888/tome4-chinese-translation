# Paseo 历史终态译文残余缺陷审计 pilot v1

状态：抽样与推理契约冻结中；尚无裁决结果。

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
