# 正式审核当前交接（2026-09-05）

当前授权为吞吐优化与后续有界基线，**未恢复无界连续审核**。本任务只实现步骤 1、2；
后续基线由 ORCHESTRATOR 另建任务执行。具体操作、计时与通过／退出条件见
[吞吐优化执行说明](review-throughput-optimization-20260905.md)。

最后已完成并 finalize 的批次为 `batch-e07e805f62a7d14ca174`。暂停时无活动批次或待归档
child；S／done 2,226（surface_only 2,179；deep_reviewed 47），待修复 0，queued 27,602。
这些是暂停快照，恢复时必须以当前 HEAD 的队列重放与检查为准，不能当作实时状态。
正式结果入口为 [batches](../evidence/production-review-v2-lite/batches/)。

后续有界基线开始时，先运行 `python3 -B tools/i18n doctor`、
`python3 -B tools/i18n production batch show`；仅在无活动 checkpoint 时运行
`python3 -B tools/i18n production queue rebuild` 与
`python3 -B tools/i18n production queue check`。有活动批次则按
[正式方案](../../docs/translation-production-review-v2-lite-plan.md)恢复，不删除 checkpoint 或另开 writer。

每批按既定 policy 稳定排序选满最多 **80 个 entry revision**，使用
`python3 -B tools/i18n production batch start --limit 80`；余量不足时记录实际 selected 数。
batch 可以混合来源，不得因 `fixed_source_identity` 变化截短 selected。
既有 adapter 按身份拆分同质 run，各 screen／run 同质且单 screen ≤80；80 是 revision
数量，不是相同文本 group 数，不能合并重复文本来超额领取。保持 selected 守恒与逐条结果。
新导出的多 run 各用 `<batch-id>-surface-000` 等独立 Paseo task，逐 run `DONE_VERIFIED`
后聚合导入；单 run 保留 batch task ID，历史已冻结路径不迁移。
实际并发数记录为操作配置（当前 3），不是契约硬上限。

逐条源码核验、冻结／preflight、角色分离、独立审核、宿主裁决、适用门禁、
`DONE_VERIFIED`、提交和 child 归档继续遵循 [工作流](../../docs/agent-workflow.md) 与
[AGENTS.md](../../AGENTS.md)。DLC 公开源码未固定 repository／commit；提取快照不作源码 pin。

原交接已按原始字节保存为[历史归档](production-review-handoff-2026-09-05-history.md)。
归档所有相对链接以原目录 `docs/` 解析，原文中的暂停、继续、push 和下一批命令仅为历史，
不构成当前指令。当前入口仅采用本文及执行说明的有界推进安排。
