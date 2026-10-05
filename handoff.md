# 当前恢复入口（2026-10-05 修复窗口67 完成，2 个 successor 待第405批重新审核）

用户 2026-10-05 要求开始生硬描述扫描 C 档（对话与 lore），已完成并推送：1,446 条全部裁决，修复包 12–16 修正 485 处，DeepSeek 交叉复核后再修正 8 处；搁置的 21 条由主代理逐条查源码，用户同意后改 16 行（含同运行键同步 1 行），GPT-6.1 Sol 复核无异议。见[扫描报告](evidence/quality/awkward-scan3-20261003/REPORT.md)的“C 档”一节与[搁置项处理](evidence/quality/awkward-scan3-20261003/holds-c.md)。至此 A、B、C 三档全部完成。

用户随后要求发布新版本：0.3.4 已推送至发布仓库 `yutio8888/tome4-chn-mod`（提交 `3f031fa`，由本仓库 `aea17710` 构建，12,450 条＝核心 6,989＋DLC 5,461），GitHub Release `v0.3.4` 安装包已回下载核验。凭据见 [`evidence/releases/addon-0.3.4.json`](evidence/releases/addon-0.3.4.json)。

用户随后要求对 C 档润色“再走一轮生产复核”：迁移 `87fb6882…` 排入的 494 个 successor 已于第397–403批全部审完（478 done、待修 16）。队列清空时积压 16 条＋宿主补充 9 条，未达 20 条阈值；用户选择“修完后再发一个插件版本”，窗口66 已修复这 25 条（2026-10-05，译文 `fd7c6a61`，migration `defcd152…`，详见 `evidence/quality/repair-window-66-20261005/PUBLICATION.md`）。窗口66 的全部 child 在证据提交前已由宿主确认归档，当前没有进行中的批次、窗口或 child。按用户指示随后发布 0.3.5：发布仓库提交 `d2575eb`（由本仓库 `d6def5d9` 构建，12,450 条＝核心 6,989＋DLC 5,461），GitHub Release `v0.3.5` 安装包已回下载核验，凭据见 [`evidence/releases/addon-0.3.5.json`](evidence/releases/addon-0.3.5.json)。待办与待决：

1. 窗口66 的 25 个 successor 已在第404批（`batch-8a80c5f58e2462772813`）审完：25 done / 0 repair_required，证据提交 `599bfb7b`；审核队列已无待审 successor。
2. 用户随后选择“小窗口67并含 422 行”：窗口67 已修复 2 条（宿主补充 `9d3fc01bdf` 奎科加章节“安格列文”→“安格利文”；用户授权的 `fc55a88fd6` 即 `mod-tome.lua:422` 护送奖励日志，对齐同族选项写法），复审中另确认同一奎科加条目的 2 处错误并一并修复（译文 `0de585f6`，migration `a0f4f220…`，详见 `evidence/quality/repair-window-67-20261005/PUBLICATION.md`）。窗口67 的全部 child 在证据提交前已由宿主确认归档。
3. 窗口67 的 2 个 successor 不继承旧 done，须重新审核（第405批）；下一个修复窗口（68）积压 0 条。

---

# 历史恢复入口（2026-10-04 窗口65 successor 已在第396批审完，0.3.3 已对外发布）

用户 2026-10-03 要求“重新再走一轮生产复审流程”，已全部审完：第383–395批共 13 批、**1019 个 successor**（migration `22b293c4…` 的 993 个＋窗口64 migration `629e3b1e…` 的 26 个），队列余 0。来源见[迁移记录](evidence/quality/maintenance-reaudit-20261003/README.md)，每批证据在 `evidence/quality/production-batches/<batch>-host-evidence/`。

结果：完成 981 条，host-block 4 条（`mod-tome/load.lua` 段已登记死键），确认待修 34 条。其中 25 条已在窗口64 修复并推送（`a2671655`），其余 9 条与宿主补充 2 条已在窗口65 修复（2026-10-04，译文 `9079821a`，migration `e437cb51…`，详见 `evidence/quality/repair-window-65-20261004/PUBLICATION.md`）。宿主裁决观察：confirmed 57 行、refuted 14 行、advisory 12 行（surface 与 contextual 同判的条目各记一行）。最后一批的收口提交是 `54a2cc9e`。窗口65 的 11 个 successor 已在第396批（`batch-24e16a565d59243f9467`）审完：11 done / 0 repair_required，证据提交 `3c2c3458`。

**用户 2026-10-03 指示：本轮完成后暂停并撰写 handoff；2026-10-04 用户指示开窗口65（“现在开”），窗口已完成；2026-10-04 用户指示“开始审核，审核后即可对外发布”，第396批已审完。** 第396批的 child 均已确认归档，当前没有进行中的批次、窗口或 child。待办与待决：

1. 对外发布已完成：0.3.3 已推送至公开发布仓库 `yutio8888/tome4-chn-mod`，提交 `9d1c9ac`；GitHub Release `v0.3.3` 安装包已回下载核验。凭据见 [`evidence/releases/addon-0.3.3.json`](evidence/releases/addon-0.3.3.json)。
2. 生硬描述扫描 C 档仍待用户决定。
3. 下一个修复窗口（66）积压 0 条，未达 20 条阈值；审核队列已无待审 successor。

`tome-possessors.lua`、`tome-items-vault.lua` 的 13 条改动不在目录内，没有进入复审。
---

# 历史恢复入口（2026-10-03 生硬解释调整完成）

机制改写撤回之后，用户要求调整补充扫描清单；已完成 16 条（13 条英文外扩写、3 条措辞精简），4 条排除项未动。两轮独立复审通过，适用门禁及 DONE_VERIFIED 通过，3 次 child dispatch 全部确认归档。见 [调整完成记录](evidence/quality/awkward-explanations-adjust-20261003/SUMMARY.md) 与 [扫描记录](evidence/quality/awkward-explanations-scan-20261003/REPORT.md)。

本次仅本地译文和证据交付，对外 0.3.2 未变。后续英文／源码差异处理原则及对外版本仍待讨论，无新机制改写、连续批次、规则修改或发布授权。用户无关改动保留。

---

# 历史恢复入口（2026-10-03 机制改写撤回完成）

用户要求撤回本轮因英文与代码不一致而做的机制改写，保留普通翻译修正；已在翻译仓库完成。165 条盘点中修改137条（122条撤回、15条混合），另28条完整保留普通修正。独立范围复审、修复后的完整终审与适用运行验证通过，任务 DONE_VERIFIED，6次 child dispatch 全部确认归档。

详见 [撤回完成记录](evidence/quality/mechanics-rollback-20261003/SUMMARY.md) 和 [后续讨论建议](evidence/quality/mechanics-rollback-20261003/WITHDRAWAL-DECISION.md)。本次只提交本地撤回及证据，对外0.3.2仓库、标签、Release和资产未动。下一步与用户讨论英文／源码差异的处理原则及对外版本；没有新机制改写、规则修改或发布授权。MMR-026“生命汲取（物理）”与UPSTREAM054撤销误报决定保留，用户无关改动保留。

下文为历史交接，旧连续推进指令、未决事项和采用状态均以本段及新撤回记录为准，不得据旧记录自动续跑。

---

# 当前恢复入口

第014主包及暮光回响两条伴随包均已DONE_VERIFIED；累计135/169原claim，14/18主包，3个附属任务。主包提交5bc6d339；伴随包准备提交后连续015—018。MMR-026术语决定仍待既有答复。全部child已确认归档，无push/PR/发布授权。

详见 evidence/quality/modified-mechanics-repair-20261002/HANDOFF.md。用户无关改动保留。

---

# 当前恢复入口

第014主包9条已DONE_VERIFIED，累计134/169原claim、14/18主包；准备提交后先运行已授权暮光回响两条companion，再015—018。所有8次派发已归档。用户已批准撤销args_order误报；最终有效终审全部9条OK。

详见 evidence/quality/modified-mechanics-repair-20261002/HANDOFF.md。保留用户无关改动，无push/PR/发布授权。

---

2026-10-03更新：用户已明确批准撤销参数顺序误报并继续。收束检查发现宿主给RE_REVIEW及FINAL_REVIEW重复cycle1/attempt1，旧final已保留为无效派发诊断（raw不改、用户裁决不改）；fresh FINAL_REVIEW attempt2 601d3a67-2732-467c-a8ff-169b39bf16a9运行中，candidate未变。完成后收束主包→companion→015—018。

# 当前恢复入口

第001—013包完成，125/169原claim；第014主包9条已修并通过完整门禁及RE_REVIEW，FINAL_REVIEW对等离子飞弹提出与上一轮相反的缺失args_order疑点。宿主已证伪：冻结context及实际DLC产物均为{3,1,2,4,5}，固定formatter探针正确。按AGENTS同revision复审分歧规则WAIT_USER，等待是否撤销误报、保持候选并据宿主裁决收束。全部child已确认归档；无活动执行者。第014未DONE/未提交。

证据：package-014-review-wait/DECISION.json、published-args-014-proof.json、format-runtime-014-proof.json及task/reviews/dispatch-evidence。用户此前9＋2拆分授权持续有效，不重问；主包若获准收束后先做014-companion两条，再015—018。伴随包prepare helper已准备但未执行。用户无关文件不动；无push/PR/发布授权。

---

# 当前交接入口（2026-10-02）

当前工作是[修改译文机制修正任务](evidence/quality/modified-mechanics-repair-20261002/HANDOFF.md)：已完成 **13/18 包、125/169 个原始claim**。第013包提交 `0c739d7f`，独立复审、终审与完整门禁通过，5个child均已归档；用户已回复“请继续”，用户已批准第014包拆为9＋2条，当前正在执行拆分；主9条及暮光2条伴随包分别完整验证后提交。当前细节见任务交接。下一步及MMR-026待决术语事项以该交接为准。

本轮用户要求更新handoff，已记录当前状态。既有连续修正范围保持；本任务未获push／PR／发布授权。下文保留第382批生产队列历史，其中旧授权、模型配置和“无未决项”等结论仅属当时任务，不覆盖当前机制修正交接。

---

# 翻译审核当前交接

更新时间：2026-10-05（修复窗口67已完成，2 个 successor 待第405批重新审核）

接手前先读 [`AGENTS.md`](AGENTS.md) 与 [审核操作指南](docs/review-operations-guide.md)。本文只写当前状态、
授权和待办；操作步骤、判据、生效裁决与已知陷阱都在指南里。上一版交接（含第273–372批逐批结果表、
窗口27修复清单与 2026-09-24 工具维护记录）已归档为
[`deprecated/docs/review-handoff-20260929-batch372.md`](deprecated/docs/review-handoff-20260929-batch372.md)，
更早的版本见 `git log -p -- handoff.md`。当前会话授权优先。

## 一、当前状态

- 2026-09-30：用户恢复工作，要求用 Gemini 3.8 Flash 快速复核 09-21 以来修改过的 1190 条译文（证据提交 `c4728694`，确认 83 条），随后“请合并修复”开窗口57。是否连续审核第373批以当前会话指示为准。
- 2026-10-01：审核队列耗尽、积压 3 条，用户选择“开小窗口修这 3 条”，开窗口58。
- 2026-10-01：第376批后按维护者要求暂停；用户“先补术语库”（`8e2fae4e`，181 行），三方讨论改为 gpt-6-astra／opus-5-5／gemini-3.8-flash，同意统一 21 个名称并开窗口59；裁定 Phoenix＝凤凰、“恢复失衡值”保留不改。
- 2026-10-01：用户裁定 deeprock 技能树改“深岩”（Deeprock Form 保持“深岩形态”），并要求一并修复 Korbek 实验笔记标题等非阻断问题，开窗口60。
- 2026-10-01：审核队列清空后，用户要求系统性分析死亡信息表（`cd2d0d7e`）；同意把 12 条句式与拼接缺陷并入积压，开窗口61；随后裁定 pending #50（killer_message 改凶手主语）与 #51（dark Master→黑暗领主）均采用 B，排入窗口62。窗口62 已于同日完成并推送。
- 2026-10-05：生硬描述 C 档完成并发布 0.3.4 后，用户要求“再走一轮生产复核”。迁移 `87fb6882…`（catalog `47745ecc…`）把 C 档修复包、交叉复核修正与搁置项处理涉及的 494 个 successor 排入队列（证据 `evidence/quality/maintenance-reaudit-20261005/`）。
- 审核已闭合至第 **404** 批（`batch-8a80c5f58e2462772813`）：25 条，25 done / 0 repair_required。
  窗口66 successor 审核 25 条（主游戏 14、Orcs 4、Ashes 2、Cults 5）：surface 25 OK / 0 ISSUE；无 deep；无观察；无新增修复，窗口67积压 0；余 0 个 successor。
  17 项门禁全过，审核任务快照均重放为 `DONE_VERIFIED`，证据提交 `599bfb7b6d577b971cacd1f29e28ffe6d58401ee` 已 finalize。当前无 active batch。
- 修复窗口已闭合至 **67**：窗口66（第397–403批第二轮重新复审确认 16 条＋宿主补充 9 条，译文 `fd7c6a61`，migration `defcd152…`；25 个 successor 已在第404批审完）与窗口67（宿主补充 1 条＋用户授权 1 条，译文 `0de585f6`，migration `a0f4f220…`）均已修复；窗口67 的 2 个 successor 须重新审核，不继承旧 revision 的 done 状态。
- 队列（第372批 finalize 后实测）：eligible 29828，surface 覆盖 29828/29828，done 29812
  （surface_only 28718＋deep_reviewed 1094），pending_repair 0，queued 0，**blocked 16**：
  - 10 条死键／冻结 MISS（上游改串未重生 locale key 等，已 host-block 登记，不动）；
  - 5 条按裁决保留现译、但工具没有“不改”收口路径（含 petty gods `b63b2d6946`、cleaved `922c0f9665`）；
  - 1 条 Toxic Death `aeae08fe72`，已裁定改名，列入窗口57积压。
- 待用户集中审阅的争议条目：[`pending-user-review.md`](evidence/quality/pending-user-review.md) 共 51 项，**全部已裁决**，
  无未决项。

| 批次 | batch id | 结果 | surface（gpt-6-sol） | contextual（opus-5-5） | 裁决 |
| --- | --- | --- | --- | --- | --- |
| 368 | `batch-3cfa49c3b0ee7cc07337` | 49 done / 6 repair | 40 OK / 15 ISSUE | 11 OK / 4 ISSUE | 7 confirmed / 8 refuted / 4 advisory |
| 369 | `batch-ee4d1e47a33a7b8cc828` | 18 done / 1 repair | 14 OK / 5 ISSUE | 4 OK / 1 ISSUE | 2 confirmed / 3 refuted / 1 advisory |
| 370 | `batch-6bd34a6ffb2c19accea1` | 2 done / 0 repair | 2 OK / 0 ISSUE | 0 OK / 0 ISSUE |  |
| 371 | `batch-80b3265ec45a9b152247` | 7 done / 0 repair | 6 OK / 1 ISSUE | 1 OK / 0 ISSUE | 1 refuted |
| 372 | `batch-c9ca70f29bc203b33050` | 29 done / 0 repair | 27 OK / 2 ISSUE | 2 OK / 0 ISSUE | 2 refuted |
| 373 | `batch-eb93936e38c73186d222` | 78 done / 2 repair | 68 OK / 12 ISSUE | 10 OK / 2 ISSUE | 2 confirmed / 6 refuted / 6 advisory |
| 374 | `batch-2e8beab0b2f9b05c4c94` | 6 done / 1 repair | 6 OK / 1 ISSUE | 0 OK / 1 ISSUE | 2 confirmed |
| 375 | `batch-9da6a86a32b67cc82ddf` | 79 done / 1 repair | 79 OK / 1 ISSUE | 0 OK / 1 ISSUE | 2 confirmed |
| 376 | `batch-93dd0d869b4d3e8058dc` | 77 done / 3 repair | 72 OK / 8 ISSUE | 7 OK / 1 ISSUE | 4 confirmed / 3 refuted / 2 advisory |
| 377 | `batch-f66787c8049fa3542bf3` | 78 done / 2 repair | 75 OK / 5 ISSUE | 4 OK / 1 ISSUE | 3 confirmed / 2 refuted / 1 advisory |
| 378 | `batch-aab3f1f803f7e019bc0d` | 76 done / 3 repair | 72 OK / 8 ISSUE | 5 OK / 3 ISSUE | 6 confirmed / 5 refuted |
| 379 | `batch-0c287579511c7ffee8a8` | 76 done / 4 repair | 68 OK / 12 ISSUE | 10 OK / 2 ISSUE | 5 confirmed / 9 refuted |
| 380 | `batch-1c8107aa6a8d3b70ae53` | 38 done / 0 repair | 35 OK / 3 ISSUE | 3 OK / 0 ISSUE | 2 refuted / 1 advisory |
| 381 | `batch-4584eb6ddb5e3110acab` | 74 done / 1 repair | 74 OK / 1 ISSUE | 1 OK / 0 ISSUE | 1 confirmed |
| 382 | `batch-554490d4847b278842b9` | 1 done / 0 repair | 1 OK / 0 ISSUE | 0 OK / 0 ISSUE |  |
| 383 | `batch-fe24f4f2a420a35a72cc` | 80 done / 0 repair | 79 OK / 1 ISSUE | 0 OK / 1 ISSUE | 2 advisory |
| 384 | `batch-e63ec4963b48bd6eee9a` | 77 done / 3 repair | 77 OK / 3 ISSUE | 1 OK / 2 ISSUE | 5 confirmed |
| 385 | `batch-ea91b26c880d0eb75606` | 75 done / 4 repair | 76 OK / 4 ISSUE | 1 OK / 3 ISSUE | 7 confirmed |
| 386 | `batch-aa1fb47399d4777a57f0` | 78 done / 2 repair | 76 OK / 4 ISSUE | 2 OK / 2 ISSUE | 4 confirmed / 1 refuted / 1 advisory |
| 387 | `batch-96dcbe7098ab7a8a87f7` | 78 done / 1 repair | 76 OK / 4 ISSUE | 3 OK / 1 ISSUE | 2 confirmed / 2 refuted / 1 advisory |
| 388 | `batch-563560854ae20160c9d5` | 76 done / 3 repair | 76 OK / 4 ISSUE | 3 OK / 1 ISSUE | 4 confirmed / 1 advisory |
| 389 | `batch-8ddbfa00da4d0d50cdaa` | 78 done / 2 repair | 77 OK / 3 ISSUE | 1 OK / 2 ISSUE | 4 confirmed / 1 refuted |
| 390 | `batch-f199ae8241b6a0369acf` | 78 done / 2 repair | 77 OK / 3 ISSUE | 1 OK / 2 ISSUE | 4 confirmed / 1 advisory |
| 391 | `batch-ac27e658ed64b3f7f270` | 71 done / 8 repair | 71 OK / 9 ISSUE | 3 OK / 6 ISSUE | 14 confirmed / 1 refuted |
| 392 | `batch-3506bffc1094e8909c28` | 78 done / 2 repair | 75 OK / 5 ISSUE | 4 OK / 1 ISSUE | 3 confirmed / 1 refuted / 2 advisory |
| 393 | `batch-af9aadc82f05ae27f3d8` | 79 done / 1 repair | 76 OK / 4 ISSUE | 1 OK / 3 ISSUE | 2 confirmed / 5 refuted |
| 394 | `batch-f4001cace434a973dcfb` | 76 done / 4 repair | 72 OK / 8 ISSUE | 7 OK / 1 ISSUE | 5 confirmed / 3 refuted / 1 advisory |
| 395 | `batch-4158eeb47c02308774eb` | 57 done / 2 repair | 55 OK / 4 ISSUE | 2 OK / 2 ISSUE | 3 confirmed / 3 advisory |
| 396 | `batch-24e16a565d59243f9467` | 11 done / 0 repair | 10 OK / 1 ISSUE | 1 OK / 0 ISSUE | 1 refuted |
| 397 | `batch-eb3fc24942d20a7b5e71` | 78 done / 2 repair | 75 OK / 5 ISSUE | 3 OK / 2 ISSUE | 4 confirmed / 3 advisory |
| 398 | `batch-62c5a69973fcdab9c29f` | 78 done / 2 repair | 77 OK / 3 ISSUE | 1 OK / 2 ISSUE | 4 confirmed / 1 advisory |
| 399 | `batch-32839b9d4e0ed9f6554b` | 79 done / 1 repair | 78 OK / 2 ISSUE | 1 OK / 1 ISSUE | 2 confirmed / 1 refuted |
| 400 | `batch-2fd158c709697a888ae1` | 77 done / 3 repair | 74 OK / 6 ISSUE | 3 OK / 3 ISSUE | 6 confirmed / 2 refuted / 1 advisory |
| 401 | `batch-58d155a7410203c41728` | 77 done / 3 repair | 70 OK / 10 ISSUE | 7 OK / 3 ISSUE | 5 confirmed / 1 refuted / 7 advisory |
| 402 | `batch-fd4663c4b4a995cd5928` | 76 done / 4 repair | 74 OK / 6 ISSUE | 3 OK / 3 ISSUE | 6 confirmed / 3 advisory |
| 403 | `batch-9ac9ee56fc05e6b82dbe` | 13 done / 1 repair | 12 OK / 2 ISSUE | 0 OK / 2 ISSUE | 2 confirmed / 2 advisory |
| 404 | `batch-8a80c5f58e2462772813` | 25 done / 0 repair | 25 OK / 0 ISSUE | 0 OK / 0 ISSUE | — |

每批证据摘要在 `evidence/quality/production-batches/<batch>-host-evidence/summary.md`。

## 二、授权与节奏（用户指示，现行）

- 2026-09-23：持续推进审核，不需逐批确认；有争议的条目列入 pending，等用户集中审阅。
- 2026-09-24：修复先记录，**积压达到 20 条或以上再开一个合并修复窗口**。审核队列耗尽而积压不足 20 时，
  询问用户是开小窗口还是暂停。
- 每批（或每个窗口）完全收口后 push；批次进行期间不得提交任何东西。审核外发与 push 无需再次询问。
- 2026-09-25：修复窗口 `max_cycles` 默认 5（STATE 同时写 `max_cycles_user_authorized=true`）；reviewer 可写 `/tmp`
  scratch，仓库与工作区写入仍违规。
- 2026-09-27：纯名称类 pending 先双向查冲突，再由 Gemini 3.8 Flash 裁决并报告；非名称类仍逐条问用户。
  antigravity 认证失败时改用 Paseo 的 `pi/cpa/gemini-3.8-flash-high` 通道（2026-09-29 实测可用）。
- 审核模型：surface `codex/gpt-6.1-sol`（medium，auto-review），contextual `claude/claude-opus-5-5`（medium，auto）；
  修复 EXECUTOR `codex/gpt-5.6-sol`；修复窗口 FINAL 用 Claude Opus 5.5。
- 2026-09-30：用户指示此后凡用 GPT-6-Sol 处一律改用 `codex/gpt-6.1-sol`（显式 thinking medium）；Codex 0.159.1 原生会话已纳入 harvest 白名单（`88e29cf9`）。

## 三、下一步

1. **第二轮重新复审已完成**（第397–403批，494/494：478 done、待修 16）。窗口66 已修复，其 25 个 successor 已在第404批审完（25 done / 0 repair_required；surface 全 OK、无 deep 条目，按第360批先例走 surface-only 路径，派生件 `$C/finalize_host_gen_404.py`、`/tmp/mkfin_404.py`、`/tmp/handoff_gen_404.py`、`$C/close_tpl_404.sh`）；本轮派生脚本见 `$C/reaudit2-helpers/`（start_re2.sh、derive_re2.sh、mkfin_re2.py、backlog66.json），收口用 `finalize_host_gen_re2.py` 与 `close_tpl_re2.sh`。
   窗口67 的派生件在 `.artifacts/i18n/repair-w67-20261005/`（rewrites.py、setup_window67.py、freeze_review.py、wd.sh、w67-tr.sh、w67-close.sh、w67-scope.tmpl、make_handoff_next.py），下一个窗口可从此派生；handoff 由宿主写好全文、publication child 核对基线 SHA 后整份替换。
   本轮新增经验（第392–395批）：
   - 一批有多个 contextual run 时，`finalize_host_gen_re.py` 与 `/tmp/mkfin_re.py` 已能处理；`close_review<N>.py` 的 `for run in (...)` 仍须按 run 数手改。
   - Orcs、Cults 等 DLC 死键（如 DebugMain section 的 lore 副本）带快照身份，不能 host-block；按第353/368批先例照常审核，被指出的问题记 advisory，并核对生效行。
   - contextual child 因 Claude 会话额度用尽而无输出时：harvest 会拒收，改用 `review_lifecycle.py reject --notified --capture <terminal> --evidence <证据>` → archive-intent → archive → archive-confirm；然后按 attempt 2（`full-001`，`retry_of`）重派，并在 snapshot 脚本中加入 `{batch}-*-rejection-evidence` 收录。fin 中可用 `contextual_reviewer_en` 覆盖 reviewer 描述（第395批先例）。
   - 宿主可对 workset 做 LF／TAB／全角空格的预扫描，这类问题 surface 常漏。没被任何 lane 指出的，只能经 `review<N>-extra.json` 作为宿主补充登记（第394批先例）。
2. 窗口 67 已完成（2 条：主游戏 1、Cults 1）：宿主补充 `9d3fc01bdf`（Cults 奎科加章节，源文 records of Anglowen，“安格列文”→“安格利文”，按 terminology/places.tsv:20）＋用户 2026-10-05 授权的 `fc55a88fd6`（`mod-tome.lua:422` 护送奖励日志“%s技能 %s（+%d 级）”，对齐 425 行与 tome-orcs.lua:582），新译文由宿主写定、EXECUTOR 逐字替换；窗口内复审另确认奎科加条目的 2 处错误并一并修复。复审路径：REVIEW r0a1（gpt-6.1-sol）1 OK／1 ISSUE，确认忠实性 1 条（奎科加章节 librarians 被译作“记录者”）＋宿主同条确认 1 条（might be 被写成“其实是”），execute-02 → RE_REVIEW r1a1 2/2 OK → FINAL f1a2（Opus 5.5）2/2 OK；第 1 轮收敛（max_cycles 5），无无效尝试；门禁 17/17。详见 `evidence/quality/repair-window-67-20261005/PUBLICATION.md`。
   窗口66（第二轮重新复审确认 16 条＋补充 9 条，第 3 轮收敛）详见 `evidence/quality/repair-window-66-20261005/PUBLICATION.md`；窗口65（重新复审确认 9 条＋补充 2 条）详见 `evidence/quality/repair-window-65-20261004/PUBLICATION.md`；窗口64 详见 `evidence/quality/repair-window-64-20261003/PUBLICATION.md`；窗口63（意志之力 maces 1 条）详见 `evidence/quality/repair-window-63-20261001/PUBLICATION.md`；窗口62 教训：killer_message 被 `" "..src.killer_message` 拼在凶手名后，译文不得以标点起头。
   窗口58遗留的 `2822ed0142` 食人魔化歌意译仍待 successor 审核时再评估。
   下一个修复窗口（68）积压 **0** 条。主游戏 `mod-tome/load.lua` 段的奎科加旧版副本（`e4824491182e`）是已登记死键（`batch-ac27e658…` 中经 host-block 放行），译文不生效，与 Cults 现行条目措辞不同步属预期，不登记。
   第404批计时（实测，投影缓存 on）：start 1.9 s（另有一次因 evidence-head 漂移失败的 start，重建队列后重跑）；adjudication（surface-only）＋prepare-evidence（含 17 项门禁）172.0 s；finalize 178.3 s。
3. 窗口56的教训：长篇 lore 进窗口后每轮复审都会冒出旧错，第二轮起宿主应整条对照源文一次补齐；
   Opus FINAL 截断输出记 INVALID 后 attempt+1 重派，不计 max_cycles。

## 四、环境备忘

- 宿主工作目录 `.artifacts/i18n/continuation-20260923`（已 gitignore），Paseo workspace `wks_420314270844170b`；
  跑门禁或收口前 `export TOME_PASEO_WORKSPACE=wks_420314270844170b I18N_PROJECTION_CACHE=on`，并从 PATH 去掉 `/opt/agents/bin`。
- 上游源码 `/workspace/t-engine4`，固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`；DLC 源码在
  `/workspace/tome4-dlcs/<component>`（仓库与 commit 未固定）。子 agent 看不到上游检出，
  它们报“commit 不存在、证据不足”时由宿主自查。
- 未跟踪文件 `.ai/consult/`、`recipe` 与旧的 `evidence/quality/production-batches/*-source-workset.json`（15 个）
  是既有遗留，保持不动。
- 发布插件：最新 0.3.4（2026-10-05，tome4-chn-mod `3f031fa`，对应本仓库 `aea17710`），凭据见 `evidence/releases/addon-0.3.4.json`。
- 历史保留边界：`RW1-SIB-01`、`RW1-SIB-02` 永久排除，不计阈值。
- 不要打开 reviewer 的 agent tab（会清掉 attentionReason，harvest 失败只能整批 abandon）。
