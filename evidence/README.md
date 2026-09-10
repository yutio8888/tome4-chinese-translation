# Evidence

本目录保存需要长期保留的人工裁决（adjudicated）证据，以及支撑其身份核验的
小型锚点文件；可由工具从源码、版本清单或 inventory 重新生成的派生产物（derived）
仍放在被忽略的 `.artifacts/` 下。判定规则是：能按已记录输入和工具重新生成、且不含
不可替代人工判断的输出属于 derived；包含人工判断、裁决结果，或在源工件清理后仍需
保留以核验裁决身份的不可重生成内容属于 adjudicated，必须放在受版本控制的
`evidence/` 下。

## Production-review shadow baseline

`evidence/production-review/` 保存 WP1 校准所需的内容寻址 locator snapshot、catalog、一次性 shadow journal/checkpoint 与 shadow batch。它们是当前输入的受跟踪核验锚点，但 marker 固定为非权威／不可派发／不可提升，不是人工裁决、正式 queue、ownership 或完成覆盖率；真实 surface consumer 必须拒绝它们；默认 ledger CLI 合并工具仓库 ROOT 与所选 `--root` 的 exact shadow manifest forbidden provenance set，generic library replay 仅作 legacy 状态机结构验证，formal catalog flag 在 WP2 exact validator 实现前拒绝所有 catalog，未来 validator 仍须应用 forbidden set。相同 ID 只接受相同 bytes；drift 和 reconciliation report 位于被忽略的 `.artifacts/i18n/production-review/`。WP2 不得把这些 artifact 当 parent；publication 在新的单锁 generation transaction 能于锁内精确完成 WP1 retirement、父目录 fsync、五 family/总预算预检及五 family publication/恢复前完全不可用。详细配方与 128 MiB 预算见 [`docs/translation-production-catalog-queue-v1-plan.md`](../deprecated/docs/translation-production-catalog-queue-v1-plan.md)。

## 批次文件迁移

以下 29 个文件从 `.artifacts/` 迁入 `evidence/`；每一项均为一对一映射，basename
保持不变。迁入文件内容未作任何修改，包括没有改写 JSON 内部的路径字段。

| 旧路径 | 新路径 |
|---|---|
| `.artifacts/i18n/p1/batch1-visibility-triage.json` | `evidence/quality/p1/batch1-visibility-triage.json` |
| `.artifacts/i18n/p1-batches/p1-b1-mechanics-numeric.json` | `evidence/quality/p1-batches/p1-b1-mechanics-numeric.json` |
| `.artifacts/i18n/p1-batches/p1-b1-s2-verification.json` | `evidence/quality/p1-batches/p1-b1-s2-verification.json` |
| `.artifacts/i18n/p1-batches/p1-b2-condition-controlled.json` | `evidence/quality/p1-batches/p1-b2-condition-controlled.json` |
| `.artifacts/i18n/p1-batches/p1-b2-s2-verification.json` | `evidence/quality/p1-batches/p1-b2-s2-verification.json` |
| `.artifacts/i18n/p1-batches/p1-b3-s2-verification.json` | `evidence/quality/p1-batches/p1-b3-s2-verification.json` |
| `.artifacts/i18n/p1-batches/p1-b4-mechanics-numeric.json` | `evidence/quality/p1-batches/p1-b4-mechanics-numeric.json` |
| `.artifacts/i18n/p1-batches/p1-b4-s2-verification.json` | `evidence/quality/p1-batches/p1-b4-s2-verification.json` |
| `.artifacts/i18n/p1-batches/p1-b5-format-binding.json` | `evidence/quality/p1-batches/p1-b5-format-binding.json` |
| `.artifacts/i18n/p1-batches/p1-b5-s2-verification.json` | `evidence/quality/p1-batches/p1-b5-s2-verification.json` |
| `.artifacts/i18n/p1-batches/p1-b6-markup-token.json` | `evidence/quality/p1-batches/p1-b6-markup-token.json` |
| `.artifacts/i18n/p1-batches/p1-b6-s2-verification.json` | `evidence/quality/p1-batches/p1-b6-s2-verification.json` |
| `.artifacts/i18n/p1-batches/p1-b7-args-order.json` | `evidence/quality/p1-batches/p1-b7-args-order.json` |
| `.artifacts/i18n/p1-batches/p1-b7-s2-verification.json` | `evidence/quality/p1-batches/p1-b7-s2-verification.json` |
| `.artifacts/i18n/p1-batches/p1-b8-adjudication.json` | `evidence/quality/p1-batches/p1-b8-adjudication.json` |
| `.artifacts/i18n/p1-batches/p1-b8-args-order-census.json` | `evidence/quality/p1-batches/p1-b8-args-order-census.json` |
| `.artifacts/i18n/p1-batches/p1-quality-random-batch-001.json` | `evidence/quality/p1-batches/p1-quality-random-batch-001.json` |
| `.artifacts/i18n/p2-batches/p2-ashes-b1-host-verification.json` | `evidence/quality/p2-batches/p2-ashes-b1-host-verification.json` |
| `.artifacts/i18n/p2-batches/p2-ashes-b1-player-mechanics-numeric.json` | `evidence/quality/p2-batches/p2-ashes-b1-player-mechanics-numeric.json` |
| `.artifacts/i18n/p2-batches/p2-ashes-status-b1-host-verification.json` | `evidence/quality/p2-batches/p2-ashes-status-b1-host-verification.json` |
| `.artifacts/i18n/p2-batches/p2-ashes-status-b1-player-visible.json` | `evidence/quality/p2-batches/p2-ashes-status-b1-player-visible.json` |
| `.artifacts/i18n/p2-batches/p2-cults-b1-host-verification.json` | `evidence/quality/p2-batches/p2-cults-b1-host-verification.json` |
| `.artifacts/i18n/p2-batches/p2-cults-b1-player-mechanics-numeric.json` | `evidence/quality/p2-batches/p2-cults-b1-player-mechanics-numeric.json` |
| `.artifacts/i18n/p2-batches/p2-cults-status-b2-host-verification.json` | `evidence/quality/p2-batches/p2-cults-status-b2-host-verification.json` |
| `.artifacts/i18n/p2-batches/p2-cults-status-b2-player-visible.json` | `evidence/quality/p2-batches/p2-cults-status-b2-player-visible.json` |
| `.artifacts/i18n/p2-batches/p2-orcs-b1-host-verification.json` | `evidence/quality/p2-batches/p2-orcs-b1-host-verification.json` |
| `.artifacts/i18n/p2-batches/p2-orcs-b1-steam-mechanics-numeric.json` | `evidence/quality/p2-batches/p2-orcs-b1-steam-mechanics-numeric.json` |
| `.artifacts/i18n/p2-batches/p2-orcs-status-b1-host-verification.json` | `evidence/quality/p2-batches/p2-orcs-status-b1-host-verification.json` |
| `.artifacts/i18n/p2-batches/p2-orcs-status-b1-player-visible.json` | `evidence/quality/p2-batches/p2-orcs-status-b1-player-visible.json` |

其中 `p1/batch1-visibility-triage.json` 是 100 条 `untranslated-existing` 的可见性三方核验记录，
`categories` 含 6 个键：其中 5 个是带 `count` 与 `rationale` 的类目对象，显式计数依次为
0／46／31／4／9，合计 90；第 6 个键 `A_candidates_demoted` 是长度为 4 的列表，不含
`count` 或 `rationale`。余下 10 条的合计数仅在 `conclusion` 中明示；`A_candidates_demoted` 另含 4 组候选明细
（含 `verdict` 与 `evidence`），但无 per-item count，无法仅凭结构建立逐条对应关系。
多项 `rationale`／evidence 带源码定位，但并非全部。文件没有顶层 `notes` 键，而
`A_translatable_player_visible.rationale` 中却写「见 notes」，这是原始证据内部的悬空引用，
只如实记录，不修改该 JSON。它是
`docs/p1-execution-plan.md` §1.1 第三条裁决的证据，包含不可重生成的人工判断。

这些 JSON 中的 `batch`／`batch_path`／`inventory_run` 字段是历史定位串，不是迁移后
路径的规范化引用。批次校验记录中，b1、b2 使用 `batch`，b3–b7 使用 `batch_path`，
b8 没有 `batch` 或 `batch_path`；批次生成记录中的 `inventory_run` 也只表示历史位置。
权威绑定以 `batch_sha256` 等内容哈希为准；迁移过程不修改这些历史字段。

## B3 抽样重放

2026-08-21 的只读重放结论是：精确成功（25/25）。配方如下：

- 总体取 `.artifacts/i18n/quality/runs/20260817T130842.064026Z-inventory/inventory.jsonl`
  中 `component == "tome"` 的条目，共 23294 条；总体
  `inventory_sha256` = `5ed11d8f62db1d470e29e5516d0cf963d88c088137b9a9f1ffcdbca433be6502`。
- `item_id` = `"translation-" + revision_id`。
- 选择规则：`random.Random(seed_int).sample(sorted(item_ids), 25)`。
- `seed_int = int.from_bytes(sha256(seed_str)[:8], "big")`；本次实测值为
  `18289353853053488059`。

B3 的 25 条 `item_id` 全部存在于该总体（25/25）。上述总体哈希和选择规则是重放所需的
内容身份锚点；文件内部的路径字段仅保留历史记录含义。

## Inventory run 锚点与已接受缺口

13 个被引用 run 各自只跟踪 `inventory-manifest.json` 与 `inventory-summary.json`，作为
核验锚点。已接受的缺口是：这 13 个 run 的 `inventory.jsonl`（约 630 MB）不跟踪；这些
可重生成的大型明细文件继续留在被忽略的 `.artifacts/` 中，`evidence/` 下绝不包含或跟踪
任何 `inventory.jsonl`。
