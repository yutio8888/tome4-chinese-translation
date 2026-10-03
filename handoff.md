# 当前恢复入口（2026-10-03 机制改写撤回完成）

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

更新时间：2026-10-01（第382批已 finalize，窗口64积压 0 条，审核队列已清空）

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
- 审核已闭合至第 **382** 批（`batch-554490d4847b278842b9`）：1 条，1 done / 0 repair_required。
  窗口63 successor 1 条（主游戏，意志之力）：surface 1 个 child 判 OK；无 deep 条目，走 surface-only 裁决，未跑 contextual。窗口64积压 0；审核队列已清空。
  17 项门禁全过，审核任务快照均重放为 `DONE_VERIFIED`，证据提交 `32da8d421c2236208dfdc165ab56d8a0ab745629` 已 finalize。当前无 active batch。
- 修复窗口已闭合至 **63**：窗口62（译文 `1f4395f6`）与窗口63（第381批确认的意志之力 maces“权杖”→“狼牙棒” 1 条，译文 `7a7d8653`，migration `f0e5ef72…`）均已修复；窗口63 的 1 个 successor 须重新审核，不继承旧 revision 的 done 状态（窗口61、62 的 successor 已于第381批审完）。
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

1. 审核队列已清空：第382批审完窗口63 的 1 个 successor（无新增确认），窗口64积压 0 条。addon 0.3.1 已发布（发布仓库 `c53351a`，GitHub Release `v0.3.1`，12,131 条）。下一步待用户指示。补空格维护（2026-10-01，译文 `a2a2d6b7`，migration `89381695…`，证据 `evidence/quality/maintenance-placeholder-spacing-20261001/`）的规则见审核操作指南 §6.4，由 strict lint `talent-placeholder-spacing` 强制。
   届时用 `.artifacts/i18n/continuation-20260923/bd.sh` 驱动（`N=<批号>; source bd.sh` 须分两句）；
   混合批按第290批（或第372批）的 stage/snapshot/close 派生，注意指南第七节列出的混合批故障。
2. 窗口 63 已完成（1 条，主游戏）：第381批确认的意志之力（Strength of Purpose）maces“权杖”→“狼牙棒”（与其覆盖的武器掌握同句式一致），并按整句对照把第一行改为“当使用剑、斧、狼牙棒、匕首或者弓箭时，增加 %d%% 武器伤害和 30 点物理强度。”（去掉逗号后多余空格、补谓语）。用户 2026-10-01 批准在未达 20 条时开窗。复审路径：execute-01 → REVIEW r0a1（GPT-6.1 Sol）1 OK → FINAL f0a2（Opus 5.5）1/1，cycle 0 收敛；门禁 17/17。
   窗口62（killer_message 凶手主语 50 条、黑暗领主 2 条、苦痛链接 1 条）详见 `evidence/quality/repair-window-62-20261001/PUBLICATION.md`；教训：killer_message 被 `" "..src.killer_message` 拼在凶手名后，译文不得以标点起头。
   窗口58遗留的 `2822ed0142` 食人魔化歌意译仍待 successor 审核时再评估。
   窗口 64 积压 **0** 条（窗口63后重新计数）：无。窗口61–63 的 successor 已全部审完。
   第382批计时（实测，投影缓存 on）：start 1.9 s；adjudication chain（含 17 项门禁）166.6 s；finalize 153.3 s。
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
