# 翻译审核当前交接

更新时间：2026-10-01（第376批已 finalize，窗口59积压 4 条；按维护者要求暂停，未开第377批）

接手前先读 [`AGENTS.md`](AGENTS.md) 与 [审核操作指南](docs/review-operations-guide.md)。本文只写当前状态、
授权和待办；操作步骤、判据、生效裁决与已知陷阱都在指南里。上一版交接（含第273–372批逐批结果表、
窗口27修复清单与 2026-09-24 工具维护记录）已归档为
[`deprecated/docs/review-handoff-20260929-batch372.md`](deprecated/docs/review-handoff-20260929-batch372.md)，
更早的版本见 `git log -p -- handoff.md`。当前会话授权优先。

## 一、当前状态

- 2026-09-30：用户恢复工作，要求用 Gemini 3.8 Flash 快速复核 09-21 以来修改过的 1190 条译文（证据提交 `c4728694`，确认 83 条），随后“请合并修复”开窗口57。是否连续审核第373批以当前会话指示为准。
- 2026-10-01：审核队列耗尽、积压 3 条，用户选择“开小窗口修这 3 条”，开窗口58。
- 审核已闭合至第 **376** 批（`batch-93dd0d869b4d3e8058dc`）：80 条，77 done / 3 repair_required。
  技能说明补空格维护的 80 个 successor（全为主游戏）：surface 一组 72 OK / 8 ISSUE，无补空格误报；contextual 首轮通过。确认 3 条，窗口59积压 4。
  17 项门禁全过，审核任务快照均重放为 `DONE_VERIFIED`，证据提交 `87eb3a451088d416514587c7ca08b66f44aeb8d5` 已 finalize。当前无 active batch。
- 修复窗口已闭合至 **58**：第373、374批确认的 3 条（age-allure 副歌人称、fay-willows 夺取城门／亡灵大军／射击队列／步调一致、pocket-time 两段）已修复；译文提交 `54c307a7`；migration `2f023eaf…` 的 3 个 successor（主游戏 1、Cults 1、Orcs 1）须重新审核，不继承旧 revision 的 done 状态。
- 队列（第372批 finalize 后实测）：eligible 29828，surface 覆盖 29828/29828，done 29812
  （surface_only 28718＋deep_reviewed 1094），pending_repair 0，queued 0，**blocked 16**：
  - 10 条死键／冻结 MISS（上游改串未重生 locale key 等，已 host-block 登记，不动）；
  - 5 条按裁决保留现译、但工具没有“不改”收口路径（含 petty gods `b63b2d6946`、cleaved `922c0f9665`）；
  - 1 条 Toxic Death `aeae08fe72`，已裁定改名，列入窗口57积压。
- 待用户集中审阅的争议条目：[`pending-user-review.md`](evidence/quality/pending-user-review.md) 共 49 项，**全部已裁决**，
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

1. **审核已按维护者要求在第376批后暂停**；恢复时从第 **377** 批起：技能说明占位符补空格维护余下约 233 个 successor（约 3 批）。补空格维护（2026-10-01，译文 `a2a2d6b7`，migration `89381695…`，证据 `evidence/quality/maintenance-placeholder-spacing-20261001/`）的规则见审核操作指南 §6.4，由 strict lint `talent-placeholder-spacing` 强制；审核这些 successor 时空格本身不判问题（第375、376批 surface 均无补空格误报）。
   届时用 `.artifacts/i18n/continuation-20260923/bd.sh` 驱动（`N=<批号>; source bd.sh` 须分两句）；
   混合批按第290批（或第372批）的 stage/snapshot/close 派生，注意指南第七节列出的混合批故障。
2. 窗口 58 已完成（第373、374批确认的 3 条）：age-allure 副歌“嘿，我，现为守卫”→你（4 处）；fay-willows 骷髅转而去夺取城门、步步逼近的亡灵大军、排成射击队列，以及 FINAL 补出的两处 lockstep“步调一致”；pocket-time 精通其中几项、与吸血鬼领主正面交锋、含糊不清地咒骂了一通不公平。复审路径：execute-01 → REVIEW r0a1 3 ISSUE 全不采纳（1 驳回、2 advisory）→ FINAL f0a2 1 确认（lockstep）→ execute-02 → RE r1a1 1 advisory → FINAL f1a2 越界 grep ashes-urhrok 拒收 → f1a3（Opus 5.5）3/3，cycle 1 收敛；门禁 17/17。
   模板为窗口58：`.artifacts/i18n/repair-w58-20261001/setup_window58.py`＋`SPEC-TEMPLATE.md`＋`HOST-SUPPLEMENT-CLAIMS.json`、`wd.sh`、`check_siblings.py`（须传 WORKSET 路径）；宿主辅助脚本 `w58-tr.sh` 等在 `.artifacts/i18n/continuation-20260923/tmp-helpers-20260929/`（已 gitignore）。setup 后要手设 STATE.candidate_author_agent_id，freeze_review.py 简报条数“审N条”要按窗口改。
   advisory carry_forward：`2822ed0142` 食人魔化歌（All Star 戏仿）多句押韵意译偏离原文（stasis、“until we say it's ogre”、the years'll start coming），整首重译属歌词策略，successor 审核时再评估；`e2c9218ea9` 已在本窗口修复 lockstep。
   窗口 59 积压 **4** 条（窗口58后重新计数，主游戏 4）：第375批 `1c38f759ab` 引导异常“你可以选中引导异常作为目标”→为引导异常选择目标，并合并多拆的一行；第376批 `4e496adf1d` 太阳赞歌“三格外”→“距离三格及以上”、`5c0dc6d9d2` 阴影消隐补“受到攻击时”、`6a7d1cc720` 吞噬改为“尝试吞噬：若成功则…”；依据见各批 `.ai/task/<batch>/HOST-FINAL-DECISIONS.json`。
   第376批计时（实测，投影缓存 on）：start 1.8 s；adjudication chain（含 17 项门禁）163.6 s；finalize 138.5 s。
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
