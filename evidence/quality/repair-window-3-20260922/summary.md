# 修复窗口 3 出版证据

## 范围与成果

- 窗口 3 修正审核 244—246 的 14 个已确认 target：11 条原生产
  `repair_required`，另加 Rosebloom、擒抱和战吼 3 条宿主独立补充；未把补充项伪装成原生产结论。
- 译文提交为 `254ad2b418e2660a1dd5c967889691c24925e6cb`，候选及当前
  `mod-tome.lua` SHA-256 均为
  `dd793e3d0f4336c881f30e7cb4e62bdccfc90dbaa263182ce4b57a18ad4c76c8`。
  本出版阶段未修改 Lua、术语、规则或工具，也未重跑译文审核和完整门禁。
- 固定公开源码为 tome commit
  `624a67329fe2ad440c5b344785a9c73fcf22ae63`，无 DLC。机制探针只调用了与
  14 条机制结论有关的局部回调，不替代完整门禁。

## 审核、重试与验证边界

- 有效语境复审为 cycle 0 attempt 3、cycle 1 attempt 3、cycle 2 attempt 1，
  每轮各四个独立 lane；最终全量复审为 cycle 2 attempt 2、dispatch `f2a1`，
  14 条全部 `OK`。
- r0a1/r0a2 因 revision echo 错误失效；r1a1 因原生终态 provenance 不合规失效；
  r1a2 因读取未引用历史记忆失效。它们不计入有效复审。最终 record 曾误记 attempt 1，
  后来只把 terminal 坐标更正为 attempt 2；原记录、首次失败检查和更正审计均保留，
  没有改写 envelope、raw、prompt 或 native 结果，也没有宣称新增复审运行。
- 17 项完整门禁和严格 addon 构建此前已通过；冻结 checkpoint 与独立镜像探针均为
  `DONE_VERIFIED`。本次从受跟踪归档目录再次独立运行：
  `python3 -B tools/ai_state_check.py .ai/task/repair-w3-20260922/STATE.json --workspace-root /workspace/tome4-chinese-translation/evidence/quality/repair-window-3-20260922/orchestration --target DONE`，
  RC 0，stdout 为 `DONE_VERIFIED: DONE predicate verified`，stderr 为空。
  机器可读结果见 [snapshot-replay.json](snapshot-replay.json)。

归档的 [orchestration-pack-manifest.json](orchestration-pack-manifest.json) 与 producer
manifest 逐字节相同；其 464 个来源在复制前后均按声明的 SHA-256 和字节数核对，合计
3,764,919 bytes。`orchestration/` 中的 `STATE` 来自
`STATE-review-validation-checkpoint.json`，表示全部译文及审核 child 已归档且验证通过的冻结边界，
不是本次出版 child 的实时 STATE。包内路径、身份和摘要均未改写。

## Catalog、迁移与真实计时

- 第一次 queue rebuild：RC 0，`214.96572246798314` 秒。
- 单次候选 catalog build：RC 0，`3.3934438779833727` 秒。
- 单次 migration-chain：成功，总计 `224.88719244796084` 秒；plan 为 RC 0、
  `217.21182037203107` 秒，check 为 RC 0、`3.10935459198663` 秒，apply 为
  RC 0、`4.526635209971573` 秒；投影调用一次。
- 旧 catalog `2a8b6f4ac30dba6abff9e96dc37295d5e0f20acb5e4b97067160261b346e358d`
  迁移到新 catalog
  `75472e42602fb1f9a44d165829a95a5c1deaaad8fde9f56fa8db5c6d187c8c6f`；
  14 条 revision changed、29,814 条 unchanged，0 ambiguous、0 unmapped。
- migration ID 为
  `5dccee54c4aed46e7b80f17a523eb61d9058add7926f7e292ba5eb45350ad0bf`。
  catalog entries、exclusions、manifest 的 SHA-256 依次为
  `c58f39f854de7419311b31cb4e7187aa016bef4aa8440da6fe709e3728e6cd98`、
  `1288283aa25ae95c3bf311850e168ecb04d25cd09370e02fb84e5fb9110a7da0`、
  `79da8b368e78d0c892981e743d6c71ced228530b24a971f7c49ad595ea6d225f`。
  候选 catalog/schema/policy 和 migration 均为逐字节安装，未编辑字段。

原始 producer 结果与计时保存在 [publication/](publication/)：queue1、catalog、
migration-chain、migration、catalog 变化核验、先前独立 pack 回放探针和本阶段冻结范围均保持原始字节。
当前 SQLite meta 实测 `catalog_id` 为新 catalog，`evidence_head` 为译文提交
`254ad2b418e2660a1dd5c967889691c24925e6cb`。

## 尚未完成的出版步骤

本文件生成时，实际 `HEAD` 是译文提交 `254ad2b…`，实际远端 `origin/develop` 仍为
`9fb5ec1df3c74e09fd981bb7d16300d6bce25ef9`。因此证据/catalog/migration 提交、该提交后的
第二次 queue rebuild、push 及远端复核均仍待宿主完成；本文不宣称这些步骤已完成。
14 个迁移后的 successor 已入队，必须重新审核。之后按既有授权继续审核 247（默认 80 条，
每批 push，不逐批询问）。Archmage 范围外 pending 保留，`RW1-SIB-01/02` 永久排除；
本窗口没有术语或全局策略修改，也未触碰用户旧有无关未跟踪文件。
