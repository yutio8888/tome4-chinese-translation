# 复核进度

更新时间：2026-09-22T00:20:10.628129+00:00

- 冻结总数：4144 条，11 组件；净变更 4143，改后恢复 1。
- Gemini 已有覆盖 10 条 + 本轮 80 条 = **90 条**。
- 待 Gemini：**4054 条**；尚未启动第 003–130 批（128 批）。
- 当前两批及全部 Sol 交叉复核已完成，全部 child 已归档；交接 Grok 4.7 从第003批接续。
- 所有语义结论只转录 REVIEWER；主代理不自行裁决或修复。

## 当前批次

| 批次 | 条目数 | 状态 | 转交 Sol 的条目 |
| --- | --- | --- | --- |
| batch-001 | 40 | reviewed_with_cross_results | entry-00004, entry-00039 |
| batch-002 | 40 | reviewed_with_cross_results | entry-00041, entry-00061, entry-00063, entry-00069, entry-00075 |

## 交叉复核

- cross-prior-spot06：completed；entry-01917
- cross-batch-001：completed；entry-00004, entry-00039
- cross-batch-002：completed；entry-00041, entry-00061, entry-00063, entry-00069, entry-00075

## 会话生命周期

- gemini-001-01：archived；归档确认 True；agent 6cb7fd21-ce24-4f0b-a871-5425013cf343
- gemini-002-01：archived；归档确认 True；agent f78c9289-915a-4810-86d3-23ab0434cd41
- sol-prior-01：archived；归档确认 True；agent 9410b36c-9364-43e6-aebe-434298513fd7
- gemini-002-02：archived；归档确认 True；agent c0abd0b6-8044-4bed-839a-8cfecef78c9b
- sol-001-01：archived；归档确认 True；agent 00574123-ca72-415b-a2bc-7baf266094ba
- sol-002-01：archived；归档确认 True；agent 0bbf285e-c4b2-48d8-9f35-74d5163114c2

第二批首次启动遭遇 TLS handshake timeout，未产出审核结果；已归档后 fresh retry 成功返回。首轮 11 条抽查的 Night Terror 是旧清单身份错误造成的额外条目，不计本轮已修改覆盖；详情见 INVENTORY-CORRECTIONS.md。inventory.json 内的状态字段是初始快照，实时状态以 STATE.json、PROGRESS.md 为准。

## grok01 接续

- 记录者：689b484a-da2e-4370-860a-1d5f67a61a41（grok/grok-4.7/medium）。历史编排者 ebbf6ea8-83ee-4fdf-85dc-bb82fbd25fe8 保持不变。
- 启动前 HEAD `ed873985f0fd527923db1bdb7e116da151ea6c5c`，工作树干净，11 个 locale 冻结哈希一致。
- 实时模型确认：Gemini 3.8 Flash / high / dangerously-skip-permissions / auto_accept；Sol gpt-5.6-sol / medium / auto-review 仍可用。本波只派 Gemini。
- 更新时间：2026-09-22T00:23:09.969034+00:00

| batch-003 | 40 | reviewed_with_cross_results | entry-00090, entry-00092, entry-00094, entry-00102, entry-00105, entry-00110, entry-00111, entry-00112 |
| batch-004 | 40 | reviewed_with_cross_results | entry-00124, entry-00126, entry-00128, entry-00136, entry-00139, entry-00144, entry-00145, entry-00146 |

- gemini-003-01：running；父级已核验 689b484a-da2e-4370-860a-1d5f67a61a41；agent bcced6b1-2c1c-43ca-bdb4-a0d4c05ba5dd
- gemini-004-01：running；父级已核验 689b484a-da2e-4370-860a-1d5f67a61a41；agent ea8ad686-8118-4d20-b6bf-0ae822262c60

## 003/004 收获

- 两份完成通知和 activity 摘要都嵌了同一份 batch-004 报告。原生 transcript_full 与各自任务一致：003 覆盖 entry-00081–00120，004 覆盖 entry-00121–00160，各 40/40。原始报告按原生最终回复保存，未改写。
- activity 里的 [Edit] 对应编排者自己的 evidence 写入。11 个 locale 哈希未变，evidence 目录以外无 diff。HEAD 仍是 ed873985f0fd527923db1bdb7e116da151ea6c5c。
- 用户追加：Gemini Flash 不再并行派发。003 与 004 是该限制之前已经发出的一对，现已结束。
- Gemini 覆盖 170/4144。上述疑点和细微观察进入同一次 Sol 交叉，尚未裁决。

| batch-005 | 40 | reviewed_with_cross_results | 00164–00166 与 00184, 00185, 00191, 00195, 00198 均已有 Sol |

- gemini-005-01：running；父级已核验；agent b9da4335-d822-40bb-aa77-85a68a730a93。本波只有这一路 Gemini。
- sol-003-004-01：running；父级已核验；agent 32ebea4f-f471-4964-ac29-19412fee830b。交叉 003 与 004 的疑点和细微观察。
- 003/004 证据已提交 04048730c969b1858e9cce2841bc20142dda15cf，未 push。

## 003/004 Sol 与 005 部分收获

- sol-003-004-01 原始回复已保存，16 条全部有分档。语义作者是 Sol。
- gemini-005-01 最终回复在 entry-00173 的依据句中途结束。entry-00161–00172 计为已覆盖；00173–00200 未计覆盖。Gemini 覆盖 182/4144。
- 11 个 locale 哈希未变。HEAD 仍是 04048730c969b1858e9cce2841bc20142dda15cf。

- gemini-005-01、sol-003-004-01 已归档，archivedAt 2026-09-22T01:05:13.017Z。证据提交 2fcd543，未 push。
- gemini-005-02：running，只补 entry-00173–00200；agent 815cbd17-53cc-4db1-86be-5620c566eddc。没有第二路 Gemini。
- sol-005-partial-01：running，只交叉 entry-00164–00166；agent d3d74794-8c27-492c-b04d-aa5eaa3745af。

## 005 补缺与前三处 Sol

- gemini-005-02 覆盖 entry-00173–00200，28/28。Gemini 覆盖 210/4144。
- sol-005-partial-01 已给出 00164–00166 的分档，作者是 Sol。
- locale 哈希未变。HEAD 仍是 2fcd543be3b49430c1974180e688b18a8258e48d。

| batch-006 | 40 | reviewed_with_cross_results | 五处已有 Sol |

- sol-005-partial-01、gemini-005-02 已归档，archivedAt 2026-09-22T01:12:52.576Z。证据提交 52adbd3，未 push。
- gemini-006-01：running；agent f4873805-db24-43b6-84c5-e79f6f5ce668。只有这一路 Gemini。
- sol-005-rest-01：running；agent 788fb9bd-bea4-45a1-ae7e-820ce68ccf7e。交叉 entry-00184、00185、00191、00195、00198。

- gemini-006-01：启动时 503 Eligibility UNAVAILABLE，无复核覆盖；已归档，archivedAt 2026-09-22T01:15:28.178Z。未续跑该 agent。
- gemini-006-02：fresh retry，running；agent 56825c45-bd04-40db-b409-08ed40c9b1b3。仍只有一路 Gemini。Sol 005 其余疑点仍在跑，本波不提交。
- sol-005-rest-01 已归档，archivedAt 2026-09-22T01:18:28.518Z。

- gemini-006-02：5 分钟打印超时。完整结论只有 entry-00201、entry-00202，均为未发现问题；entry-00203 在位置行中断。Gemini 覆盖 212/4144。无新疑点可交 Sol。
- gemini-006-02 已归档，archivedAt 2026-09-22T01:26:42.100Z。证据提交 b4a706d。gemini-006-03 只补 entry-00203–00240，agent f99c28d3-5df2-4cb3-b177-80edac0a501f。
- gemini-006-03：38/38，entry-00203–00240。Gemini 覆盖 250/4144。五条待 Sol。

| batch-007 | 40 | reviewed_with_cross_results | 00244 refuted；00247 advisory；00254 confirmed |

- gemini-006-03 已归档，archivedAt 2026-09-22T01:32:26.995Z。证据提交 465ed38，未 push。
- gemini-007-01：running；agent 9830f32d-d2c1-4787-9a56-4a50048c6335。只有这一路 Gemini。
- sol-006-01：running；agent e6edd402-b616-482d-bad8-60436c53a538。交叉 00216、00221、00223、00226、00231。
- gemini-007-01：40/40。Gemini 覆盖 290/4144。三处细微观察排队等 Sol；sol-006-01 仍在运行，不并行再派 Sol。

| batch-008 | 40 | reviewed_with_cross_results | 六处已有 Sol |

- gemini-007-01 已归档，archivedAt 2026-09-22T01:37:41.633Z。三处细微观察仍排队，等本路 Sol 归档后再派。
- gemini-008-01：running；agent fd4aa2f8-26a3-4483-93dd-70f023a0617b。只有这一路 Gemini。记录补写于派发之后，父级与模型已在派发时核验。
- sol-006-01 已归档，archivedAt 2026-09-22T01:39:34.387Z。sol-007-01 接着交叉 00244、00247、00254；agent 9fc8bea8-451e-40d8-8fe2-ef5667abdde5。gemini-008 仍在跑，本波不提交。
- sol-007-01：3/3 已有分档。gemini-008-01 仍在运行，本波不提交，也不再派 Sol。
- sol-007-01 已归档，archivedAt 2026-09-22T01:44:04.175Z。
- gemini-008-01：工具结束后 5 分钟内没有最终回复。原生转录没有逐条复核。0/40，不交 Sol。
- gemini-008-01 已归档，archivedAt 2026-09-22T01:50:08.572Z。证据提交 86e4ba3。gemini-008-02 重试整批 40 条，agent cff6df9d-ee34-47f6-b91b-a04133cffc23。
- gemini-008-02：40/40。Gemini 覆盖 330/4144。六条待 Sol。

| batch-009 | 40 | reviewed_with_cross_results | 四处已有 Sol |

- gemini-008-02 已归档，archivedAt 2026-09-22T01:56:28.488Z。证据提交 9ee4287，未 push。
- gemini-009-01：running；agent d224a483-0537-4ddf-bcd6-59a02382cd45。只有这一路 Gemini。
- sol-008-01：running；agent a7de38dd-9888-49db-a6c9-a7ed7379d52c。交叉 00284、00286、00288、00298、00299、00318。
- gemini-009-01：40/40。Gemini 覆盖 370/4144。四处排队交 Sol。
- sol-008-01：6/6 已有分档，作者是 Sol。

| batch-010 | 40 | reviewed_with_cross_results | 00368/00373/00374 confirmed；00393–00400 advisory |

- gemini-009-01、sol-008-01 已归档，archivedAt 2026-09-22T02:03:31.521Z。证据提交 8c19c13，未 push。
- gemini-010-01：running；agent 6f75bf3e-12f3-4f58-ad39-e2d2692234a2。只有这一路 Gemini。
- sol-009-01：running；agent 652fea27-31a4-4470-84a7-e67d18f38ecf。交叉 00334、00344、00345、00354。
- gemini-010-01：40/40。Gemini 覆盖 410/4144。十一条待 Sol。
- sol-009-01：4/4 已有分档，作者是 Sol。

| batch-011 | 40 | reviewed_with_cross_results | 五处已有 Sol |

- gemini-010-01、sol-009-01 已归档，archivedAt 2026-09-22T02:09:07.345Z。证据提交 1290db9，未 push。
- gemini-011-01：running；agent 4bbac91d-bf68-4436-a68e-2e86c5df52eb。只有这一路 Gemini。
- sol-010-01：running；agent e80e8b96-f866-4b18-b9e7-c75d3440a49e。交叉 00368、00373、00374、00393–00400。
- gemini-011-01：40/40。Gemini 覆盖 450/4144。五条排队等 Sol；sol-010-01 仍在运行，不并行再派 Sol。
- sol-010-01：11/11 已有分档，作者是 Sol。gemini-011 已归档，下一批尚未派出。

| batch-012 | 40 | reviewed_with_cross_results | 五处已有 Sol |

- gemini-011-01 已归档，archivedAt 2026-09-22T02:14:12.651Z。sol-010-01 已归档，archivedAt 2026-09-22T02:15:18.346Z。证据提交 0648abc，未 push。
- gemini-012-01：running；agent ae5f30bf-3a08-4dc3-af04-22a11a559795。只有这一路 Gemini。
- sol-011-01：running；agent b9f547f7-bc10-44fa-ad35-24d0aac1e28c。交叉 00419、00423、00428、00429、00434。
- gemini-012-01：40/40。Gemini 覆盖 490/4144。五条待 Sol。
- sol-011-01：5/5 已有分档，作者是 Sol。

| batch-013 | 40 | reviewed_with_cross_results | 五处已有 Sol |

- gemini-012-01、sol-011-01 已归档，archivedAt 2026-09-22T02:20:50.501Z。证据提交 62e6739，未 push。
- gemini-013-01：running；agent dde5f034-04ab-4151-9dbe-c6cb1552542c。只有这一路 Gemini。
- sol-012-01：running；agent 66a8ebae-e663-413b-8019-ff3ba17b282e。交叉 00443、00448、00455、00458、00476。
- gemini-013-01：40/40。Gemini 覆盖 530/4144。五条排队等 Sol；sol-012-01 仍在运行，不并行再派 Sol。

| batch-014 | 40 | reviewed_with_cross_results | 四处已有 Sol |

- gemini-013-01 已归档，archivedAt 2026-09-22T02:25:34.587Z。sol-012-01 仍在运行，本波不提交，也不再派 Sol。
- gemini-014-01：running；agent be2e7cd1-49cb-4fe8-ae30-e3139a5e2107。只有这一路 Gemini。
- sol-012-01：5/5 已有分档，作者是 Sol。gemini-014 仍在运行，本波不提交。
- gemini-014-01：40/40。Gemini 覆盖 570/4144。四处排队等 Sol。
- sol-012-01 已归档，archivedAt 2026-09-22T02:28:16.199Z。sol-013-01 记录补写，agent fa503905-f9f8-4974-9c1a-98055318c144，仍在运行。本波不提交。

| batch-015 | 40 | reviewed_with_cross_results | 四处已有 Sol |

- gemini-014-01 已归档，archivedAt 2026-09-22T02:29:54.021Z。sol-013-01 仍在运行，本波不提交，也不再派 Sol。
- gemini-015-01：running；agent ecdfa6b2-3bca-4707-98ad-0a2047ba9af6。只有这一路 Gemini。
- gemini-015-01：40/40。Gemini 覆盖 610/4144。四处排队，等 batch-014 的 Sol 结束后再派。
- sol-013-01：5/5 已有分档，作者是 Sol。

| batch-016 | 40 | reviewed_with_cross_results | 七处已有 Sol |

- gemini-015-01、sol-013-01 已归档，archivedAt 2026-09-22T02:34:33.874Z。证据提交 a48a54d，未 push。
- gemini-016-01：running；agent 0ad5c015-ca6b-4a0c-b16b-be9bc2f5a28f。只有这一路 Gemini。
- sol-014-01：running；agent 73a47a61-8a12-4864-92c2-91d0409720aa。交叉 00522、00527、00553、00560。batch-015 四处仍排队。
- gemini-016-01：40/40。Gemini 覆盖 650/4144。七条排队，等 batch-015 的 Sol 结束后再派。
- sol-014-01：4/4 已有分档，作者是 Sol。

| batch-017 | 40 | reviewed_with_cross_results | 八处已有 Sol |

- gemini-016-01、sol-014-01 已归档，archivedAt 2026-09-22T02:40:28.291Z。证据提交 9eff951，未 push。
- gemini-017-01：running；agent e0be0358-25ed-4062-be50-d849ea55a309。只有这一路 Gemini。
- sol-015-01：running；agent f6da8198-ee44-4e81-9ea6-ba82873c53e1。交叉 00570、00574、00579、00581。batch-016 七条仍排队。
- gemini-017-01：40/40。Gemini 覆盖 690/4144。八条排队，等 batch-016 的 Sol 结束后再派。文末汇总漏了 entry-00653，已按条目结论纳入。
- sol-015-01：4/4 已有分档，作者是 Sol。

| batch-018 | 40 | reviewed_with_cross_results | 五处已有 Sol |

- gemini-017-01、sol-015-01 已归档，archivedAt 2026-09-22T02:45:30.333Z。证据提交 7595f2d，未 push。
- gemini-018-01：running；agent 4d10fe09-6550-40b2-a3d6-2ab68722f25d。只有这一路 Gemini。
- sol-016-01：running；agent c773999c-33ae-4847-8f7b-b28ad1bbf633。交叉 00604、00605、00615、00620、00621、00623、00634。batch-017 八条仍排队。
- gemini-018-01：40/40。Gemini 覆盖 730/4144。五条排队等 Sol。sol-016-01 仍在运行，batch-017 八条也还在它前面。本波不提交。

| batch-019 | 40 | reviewed_awaiting_cross | entry-00722, entry-00723, entry-00728, entry-00730, entry-00731, entry-00733, entry-00740, entry-00746, entry-00752 |

- gemini-018-01 已归档，archivedAt 2026-09-22T02:50:08.412Z。gemini-019-01 记录补写，agent 7f9ae5dd-0b64-41c8-89cc-19f74b918f27，仍在运行。
- sol-016-01：7/7 已有分档。gemini-019 仍在跑，本波不提交。
- sol-016-01 已归档，archivedAt 2026-09-22T02:52:20.129Z。sol-017-01 接着交叉 batch-017 八条；agent 15448ca5-a9da-46ca-a160-9e3fe20543e8。gemini-019 仍在跑，本波不提交。batch-018 五条仍排队。
- sol-017-01：8/8 已有分档，作者是 Sol。gemini-019 仍在运行，本波不提交。
- sol-017-01 已归档，archivedAt 2026-09-22T02:57:03.811Z。sol-018-01 接着交叉 00683、00684、00712、00713、00719；agent b93ffa6b-2a6a-4d2b-8272-de7bcb354718。gemini-019 仍在跑，本波不提交。
- gemini-019-01：平台 5 分钟超时，但原生报告已含 40/40。Gemini 覆盖 770/4144。九条待 Sol。文末汇总漏了 00733 和 00746，已按条目结论纳入。
- sol-018-01：5/5 已有分档，作者是 Sol。

| batch-020 | 40 | reviewed_awaiting_cross | entry-00763, entry-00768, entry-00780, entry-00781；暂停，未派 Sol |

- gemini-019-01 已归档，archivedAt 2026-09-22T03:02:04.659Z。sol-018-01 已归档，archivedAt 2026-09-22T03:02:04.662Z。证据提交 a711b99，未 push。
- gemini-020-01：running；agent ee8766ef-c1a7-491a-9313-5c1864a67283。只有这一路 Gemini。
- sol-019-01：running；agent a280b1fc-9281-4a7e-858c-df456b257580。交叉 00722、00723、00728、00730、00731、00733、00740、00746、00752。
- 用户要求完成本轮后暂停。交接见 HANDOFF-PAUSE.md。收回这两路后归档落盘，不派 batch-021，不再开新的 Sol。审核还在跑，暂停记录尚未提交。
- gemini-020-01：40/40。Gemini 覆盖 810/4144。四处已写入 cross-batch-020，按暂停不派 Sol。sol-019-01 仍在运行。

## 暂停收尾（sol-019 收获，未提交）

- grok01 记录者 689b484a-da2e-4370-860a-1d5f67a61a41 因 API 402 额度耗尽中断（live 状态 error）。用户把暂停收尾交给新 session c59be24f-5acc-4fa5-b130-41a33cf142fc（pi/opencode-go/mimo-v2.6-flash/medium），只做收回、归档、转录。
- sol-019-01 已 idle：动作前复查 status/attention 面与原生 rollout `01a0c710-d48c-7163-8c0d-3a5dceb0a267`，含 `task_complete`，无进行中运行。最终回复 4687 字符，原样存入 `reports/sol-019-01.md`，sha256 `f86174663a6f46759b3fa6771a344e8fdae112b3fe8a67bcd62ccf62675e1d92`，未改写。
- 收回核验全部通过：cross-batch-019 / batch-019 / gemini-019-01 / batch-020 / cross-batch-020 冻结哈希一致；11 个 locale 哈希一致；HEAD 仍是派发时的 `a711b997a4a6ca43e37d46daf893aee3d2d3e306`；diff 只在本 evidence 目录，reviewer 无写入。
- 归档前先持久化 `archive_attempts_started=1`，`paseo archive` 一次成功，live 复查 `Archived=true`、`archivedAt` `2026-09-22T04:04:22.918Z`、`Status=closed`。sol-019-01 lifecycle=archived、archive_confirmed=true、harvested=true、readonly_guard=passed。
- cross-batch-019 转录完成：17 claim = 11 confirmed / 3 pending / 3 advisory / 0 refuted，语义作者 Codex/gpt-5.6-sol/medium，已写入 STATE 的 recorded_cross_verdicts 与 HUMAN-REVIEW.md。batch-019 状态改为 reviewed_with_cross_results。
- 本 workspace 再无运行中的审核 child：gemini-020-01 与 sol-019-01 均已归档。按用户指令到此停：不派 batch-021、不为 cross-batch-020 开 Sol、不提交证据、不 push、不改译文和术语。cross-batch-020 仍为 queued_paused。
- 当前覆盖 810/4144（已提交基线仍为 770/4144，`a711b99`），batch-019/020 证据留在工作树未提交。
- 更新时间见 STATE.json `updated_at`。

## 恢复派发与 020/021 收获

- 用户授权恢复（handoff 文件不提交，其余提交），`pause.status=resumed`，记录于 STATE。
- 恢复前读 live profiles：Sol 用 `agent_profile_mt3s8sou_fggrhfnq1gj`（codex/gpt-5.6-sol/auto-review/medium），Gemini 用 `agent_profile_review_fallback_antigravity_gemini37_flash`（antigravity/gemini-3.8-flash/dangerously-skip-permissions/high）；live provider 元数据确认可用，未换用 legacy gpt-6-astra profile。传输为 paseo CLI（与 mcp 同语义），父级 c59be24f-5acc-4fa5-b130-41a33cf142fc，lineage 已核验。
- 同一时刻 1 Gemini + 1 Sol：gemini-021-01 agent 1578f5fb-4d10-42e5-8d89-76e7e28b5053；sol-020-01 agent 2a4400f6-1e3a-461e-afb8-1817e1c0b9f8。
- gemini-021-01：40/40（entry-00802–entry-00841）。Gemini 覆盖 **850/4144**。四处标记：00804 细微观察，00805、00820、00840 存在疑点，与报告汇总一致。原始报告 sha256 `37318e01c2aec1927736b17d1b92dce474587f050597a1a18370fc867a62c9a1`。
- sol-020-01：4/4 条目共 10 claim（6 confirmed、2 pending、1 advisory、1 refuted），语义作者 Codex/gpt-5.6-sol/medium，已写入 cross-batch-020 与 HUMAN-REVIEW。原始报告 sha256 `0aea896a58c27b20e8da9b99ec4232e3df1cba2280e1103159f9010509ef5d54`。
- 收回核验：batch-021 / cross-batch-020 / batch-020 / gemini-020 冻结哈希一致；11 个 locale 哈希一致；HEAD 由 `3f6f49e` 变为 `8146bfd` 仅因编排者自己的记录提交，locale 无 diff；evidence 目录以外无改动。
- 归档：两路均先持久化 `archive_attempts_started=1`，一次成功，live 复查 `Archived=true`：sol-020-01 `2026-09-22T04:42:10.551Z`，gemini-021-01 `2026-09-22T04:42:12.138Z`。
- 本轮无未归档 child。batch-021 四处疑点待派 Sol，见 cross-batch-021。
- 更新时间见 STATE.json `updated_at`。
