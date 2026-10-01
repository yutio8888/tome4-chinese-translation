# 翻译审核当前交接

更新时间：2026-10-01（修复窗口62已完成、待宿主证据提交与推送；下一步审核窗口61、62 的 successor）

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
- 审核已闭合至第 **380** 批（`batch-1c8107aa6a8d3b70ae53`）：38 条，38 done / 0 repair_required。
  全 Orcs，审核队列余下的全部 38 条：补空格 successor 31 条＋窗口59 successor 6 条＋窗口58 successor 1 条：surface 一组 35 OK / 3 ISSUE，无补空格误报；contextual 首轮通过（3 OK）。无新增确认，窗口61积压仍为 9（另宿主补充 1 条）；审核队列已清空。
  17 项门禁全过，审核任务快照均重放为 `DONE_VERIFIED`，证据提交 `922c3ca265bf78170098fd76c5c74b67c9851513` 已 finalize。当前无 active batch。
- 修复窗口已闭合至 **62**：窗口61（译文 `276e8b2d`）与窗口62（pending #50 B killer_message 凶手主语 50 条＋#51 B 黑暗领主 2 条＋苦痛链接 1 条，译文 `1f4395f6`，migration `67a73acf…`）均已修复；两窗共 75 个 successor 须重新审核，不继承旧 revision 的 done 状态。
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

1. 下一步审核窗口61、62 的 successor（共 75 个，审核队列重建后可见）。补空格维护（2026-10-01，译文 `a2a2d6b7`，migration `89381695…`，证据 `evidence/quality/maintenance-placeholder-spacing-20261001/`）的规则见审核操作指南 §6.4，由 strict lint `talent-placeholder-spacing` 强制。
   届时用 `.artifacts/i18n/continuation-20260923/bd.sh` 驱动（`N=<批号>; source bd.sh` 须分两句）；
   混合批按第290批（或第372批）的 stage/snapshot/close 派生，注意指南第七节列出的混合批故障。
2. 窗口 62 已完成（53 条：主游戏 44、Cults 5、Ashes 3、Orcs 1）：按用户 2026-10-01 裁决 pending #50 B，其余 50 条 killer_message 全部改为以凶手为主语的“并将其…”主动分句（Wrathroot“并让树人们将其化为养分”、Norgos“并任由群狼分食其尸”、Tannen“并使其从此下落不明、杳无音讯”；`, who …`、`(how pathetic)` 等本不以死者为被动主语者不在范围）；pending #51 B dreadfell dark Master 2 条→“并将其献祭给她/他的黑暗领主”；窗口61 advisory 苦痛链接效果说明 victim→“另一名受害者”。Cults `0071abb36c` 同串为死键未动。复审路径：execute-01 → REVIEW r0a1 2 确认（苦痛链接“另一名”、Murgol“冲进了大海”）→ execute-02 → RE r1a1 53 OK → FINAL f1a2 1 确认（Tannen 以全角逗号起头，PartyDeath.lua:94 前置半角空格渲染为“坦能 ，”）→ execute-03 → RE r2a1 53 OK → FINAL f2a2（Opus 5.5）53/53，cycle 2 收敛（max_cycles 5）；门禁 17/17。
   教训：killer_message 被 `" "..src.killer_message` 拼在 killer 名后，译文不得以标点起头。模板：`.artifacts/i18n/repair-w62-20261001/`（rewrites.json 为整条改写表，make_claims.py 带 new_target）。
   窗口58遗留的 `2822ed0142` 食人魔化歌意译仍待 successor 审核时再评估。
   窗口 63 积压 **0** 条。窗口61 的 22 个与窗口62 的 53 个 successor 待重新审核。
   第380批计时（实测，投影缓存 on）：start 1.8 s；adjudication chain（含 17 项门禁）165.6 s；finalize 143.2 s。
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
- 发布插件：0.3.0 已于 2026-09-29 推送到 tome4-chn-mod（`717078b`，对应本仓库 `ce0b3a34`）；此后的译文改动尚未发布。
- 历史保留边界：`RW1-SIB-01`、`RW1-SIB-02` 永久排除，不计阈值。
- 不要打开 reviewer 的 agent tab（会清掉 attentionReason，harvest 失败只能整批 abandon）。
