# 修复窗口 5 出版证据

## 范围与成果

- 审核 250、251 均已完成。窗口 5 因高影响机制问题在审核 251 的安全边界提前进入修复，
  没有等待第三批。
- 本窗口修正 18 个 target：两次真实 repair preflight 共 16 条，其中审核 250 为 10 条、
  审核 251 为 6 条；另有审核 251 的宿主独立补充 2 条。两条补充没有被伪装成生产
  `repair_required`，18 条也不是单一生产批次的结果。
- 译文提交为 `f0560f5d888a9c5a84f21c1216e43eb1645437d3`，只修改
  `mod-tome.lua` 的 18 个 target。`source`、`source_tag`、`args_order`、placeholder、markup
  等保持不变；仅原授权 `e56b636891…` 按源码恢复为 1 个 LF、2 个 TAB。没有术语库变更。
- 本出版阶段没有修改 Lua、术语、规则、工具或 `.ai`，也没有重跑 queue、catalog、
  migration-chain、复审或完整门禁。

## 复审、暂停与裁决

- 三轮上限后的最终全量复审发现 `188` 段的 `hum` 被译为“呼吸”，任务据此真实暂停为
  `WAIT_USER`。用户以“同意”授权额外一轮；SENIOR 范围校准结论为 `keep`，唯一新增修复
  是改为“嗡嗡作响”。本任务的 `max_cycles=4` 只来自这次明确授权，不构成以后任务默认
  四轮的依据。
- 最新最终全量原始结果是 16 `OK` 加 2 `ISSUE`，不是 18 `OK`。宿主逐项裁决后，范围内
  没有 accepted 或 deferred finding，任务因此 completed。回忆录 source 358 的清醒时喂水
  限定、source 380 的前往 Elvala 子句保持 `pending`；Corruptor 职业 birth descriptor 的
  existing 条目不强制映射叙事 `_t`，保持 `advisory`。历轮其他范围外回忆录和称谓建议
  保留原记录，没有借机新增修复。
- 被拒收的身份或读取边界复审尝试及其 fresh retries 均保留；无效结果没有被用作审核依据。
  归档包含全部有效独立审查、两次 scope audit、用户暂停与授权、三次不同候选的完整门禁
  以及 child 生命周期记录。
- 最终完整门禁 `run.rlohbmvk` 为 17/17 通过，包含严格 addon 构建；任务状态为
  `DONE_VERIFIED`。此前两次候选门禁保留为历史记录，不替代最终候选门禁。

## 冻结归档与重放

归档的 [orchestration-pack-manifest.json](orchestration-pack-manifest.json) 与 producer manifest
逐字节相同。清单的 738 个目标在复制前后均按声明的 SHA-256 和字节数核对，合计
8,798,915 bytes。归档 `STATE.json` 明确来自 immutable
`STATE-review-validation-checkpoint.json`，不是出版时的可变 `STATE.json`。冻结源码、SPEC
和原始报告均按原始字节复制，未清洗 literal 行末空白。

producer 的独立 snapshot 重放结果保存在
[PACK-REPLAY-PROBE.json](publication/PACK-REPLAY-PROBE.json)。本出版阶段又从受跟踪归档目录运行：

`python3 -B tools/ai_state_check.py .ai/task/repair-w5-20260922/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-5-20260922/orchestration --target DONE`

实际结果为 RC 0，stdout 为 `DONE_VERIFIED: DONE predicate verified`，stderr 为空。

## Catalog、迁移与真实计时

- 第一次 queue rebuild：RC 0，`232.7815691640135` 秒。
- 单次候选 catalog build：RC 0，`3.418567003973294` 秒。
- 单次 migration-chain：成功，总计 `233.8951888839947` 秒；plan 为 RC 0、
  `226.05682895501377` 秒，check 为 RC 0、`3.197756087000016` 秒，apply 为 RC 0、
  `4.600126059958711` 秒；投影调用一次。
- catalog 从 `4763c0b4c71f1ba7a64a5603aca78da83e689f658738d6bc31feaaa9d8f68f08`
  迁移到 `c267a00eaf39f49b99266912241cfed79dfcbda440903763975ea2e4334a239d`。
  18 条 revision changed、29,810 条 unchanged，0 ambiguous、0 unmapped；18 个 successor
  已入队，后续必须重新审核，不能继承旧 revision 的完成态。
- migration ID 为
  `198b6812cf2fc2865016eb39153f90a70f244d3984a6ca81009bde8c2e897b6a`。
  catalog entries、exclusions、manifest 的 SHA-256 依次为
  `55d2c2ffbe77f8531a51e7350011215885d11413ea1a864c1828c73ef3858df5`、
  `1288283aa25ae95c3bf311850e168ecb04d25cd09370e02fb84e5fb9110a7da0`、
  `a56fba9c769fbfbee32fbf69b6c7d7beec44f7e52b9d3d4548f6d42e862aa89c`。
  候选 catalog/schema/policy 与 migration 均逐字节安装，没有编辑字段。

原始 producer 核验、计时和日志保存在 [publication/](publication/)；五个候选 catalog 文件、
migration、12 个 publication 原始附件以及 `mod-tome.lua` 相对译文提交均已逐字节复核。

## 尚未完成的出版步骤

本文件生成时实际 `HEAD` 为译文提交 `f0560f5d…`，本地远端跟踪引用 `origin/develop` 为
`29bac12f…`。本次证据/catalog/migration commit、提交后的第二次 queue rebuild、push 与远端
复核仍待宿主执行；本文不宣称这些步骤已经完成。闭合后继续审核 252，默认 80 条。

旧 Archmage、范围外 pending、旧 blocked 以及 `RW1-SIB-01/02` 的边界不扩大。
`.ai/consult/`、`recipe` 和 15 个旧 source-workset 保留，不纳入本次提交或清理。
