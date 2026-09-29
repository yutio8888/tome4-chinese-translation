# 暂停交接

用户在 2026-09-22 要求：完成当前这一轮后暂停，不再继续派发。本文件是暂停时的交接。较早的 `HANDOFF-GROK.md` 是 grok01 接手时的历史说明，规则仍然有效，进度以本文件和 `STATE.json` 为准。

## 暂停时的在飞派发（已全部收尾）

不要派 batch-021，也不要再开新的 Sol。

| 派发 | Agent | 状态 | 范围 |
| --- | --- | --- | --- |
| gemini-020-01 | ee8766ef-c1a7-491a-9313-5c1864a67283 | archived，`archivedAt` `2026-09-22T03:07:21.586Z` | batch-020，entry-00761–00800，40/40 |
| sol-019-01 | a280b1fc-9281-4a7e-858c-df456b257580 | archived，`archivedAt` `2026-09-22T04:04:22.918Z`；`archive_confirmed=true` | batch-019 的九条疑点，17 claim 已转录 |

两路都已归档，workspace 内没有仍在运行的审核 child。

gemini-020 的原始报告是 `reports/gemini-020-01.md`。四处已写入 `cross-batch-020.md`，状态 `queued_paused`：entry-00763（存在疑点），entry-00768、entry-00780、entry-00781（细微观察）。文末汇总把 00780 写在附注里，条目自己的结论仍是细微观察。用户恢复前不要派这个 Sol。

sol-019 返回后只收回、归档、转录 `HUMAN-REVIEW.md`，然后停。不要为 batch-020 再派 Sol。

**2026-09-22 收尾已完成**：grok01 记录者 689b484a-da2e-4370-860a-1d5f67a61a41 因 API 402 额度耗尽中断，用户把收尾交给 session c59be24f-5acc-4fa5-b130-41a33cf142fc（pi/opencode-go/mimo-v2.6-flash/medium）。该 session 只做了收回、归档、转录：sol-019-01 最终回复原样存入 `reports/sol-019-01.md`（sha256 `f86174663a6f46759b3fa6771a344e8fdae112b3fe8a67bcd62ccf62675e1d92`），冻结输入哈希、11 个 locale 哈希与 HEAD `a711b997a4a6ca43e37d46daf893aee3d2d3e306` 全部核验通过，归档一次成功并 live 确认，交叉结论已写入 `STATE.json` 与 `HUMAN-REVIEW.md`。没有新派发、没有提交、没有 push。

按用户指令，**这批证据先不提交**：`a711b99` 仍是最新提交，batch-019/020 的证据留在工作树。原「两路都归档之后可以只提交证据」的条款被这条后到指令覆盖，恢复后先问用户再提交。

父级都是当前记录者 `689b484a-da2e-4370-860a-1d5f67a61a41`。模型仍是 antigravity/gemini-3.8-flash/high 与 codex/gpt-5.6-sol/medium/auto-review。

收回时：核对冻结输入哈希、11 个 locale 哈希、HEAD 是否仍是派发时的 `a711b997a4a6ca43e37d46daf893aee3d2d3e306`。通知若被截断，用原生转录里的最终回复，不要改写。平台超时但原生报告已经逐条写完的，按完整覆盖计入，不要整批重跑。然后归档，确认 `archivedAt`，把疑点和细微观察写入排队记录，但不要为了它们再派 Sol。活动审核期间先不要提交；两路都归档之后，可以只提交证据，不 push。

## 已提交进度

- Gemini 覆盖 **810/4144**（含尚未提交的 batch-020）。已提交基线仍是 770/4144，提交 `a711b99`。剩余 3334 条，从 batch-021 起尚未开始。
- batch-020 的四处疑点已排队但未派 Sol。sol-019 仍是暂停前最后一路交叉。
- batch-001 至 batch-019 的 Gemini 覆盖已计入。batch-019 的平台超时发生在完整 40 条报告写完之后，没有重跑。
- batch-001 至 batch-018 的疑点已有 Sol 结论并写入 `HUMAN-REVIEW.md`。语义作者是 Sol。没有自动改译文。
- 最新证据提交是 `a711b99`。没有 push，没有改 locale，没有改生产 queue、catalog 或主工作区。
- 收尾后仍是 `a711b99`：用户明确这批证据先不提交，未做任何提交。
- 历史编排者 `ebbf6ea8-83ee-4fdf-85dc-bb82fbd25fe8` 不改写。当前记录者是 grok01：`689b484a-da2e-4370-860a-1d5f67a61a41`。

## 恢复时继续遵守

- 只做编排：派发、核对覆盖、哈希、生命周期和记录。不裁决译文，不改术语，不自动修复。
- Gemini 不并行。同一时刻最多一路 Gemini，外加一路 Sol。
- 每次派发前读 live `list_profiles`。不要改用 legacy Sol profile 上的 gpt-6-astra。
- 失败的 child 归档后用新 child 重跑，不续跑已结束的 agent。
- 原始报告以模型最终回复为准。活动摘要里两边内容串在一起时，以各自原生转录为准。
- 疑点和细微观察都交 Sol。Sol 的 confirmed、refuted、pending、advisory 原样转录。术语记录不在允许输入里时保持 pending。
- 报告文末汇总如果漏了某条，以该条目自己的结论为准，仍要转交。
- 完成条件仍是 4144 条都有 Gemini 覆盖、每条疑点都有 Sol 结果、人工项清楚、child 都归档。不要求 pending 清零，不修复译文。

恢复派发前先看 `STATE.json` 的 `pause` 字段。用户明确恢复之前，不要从 batch-021 接着跑。
