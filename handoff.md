# 翻译审核当前交接

更新时间：2026-09-25（第285批已 finalize；窗口30积压 12 条，继续审核第286批）

接手前先读 [`AGENTS.md`](AGENTS.md) 与 [审核操作指南](docs/review-operations-guide.md)。本文只写当前状态、
授权和待办；操作步骤、判据、生效裁决与已知陷阱都在指南里。历史交接正文见本文件的 git 历史
（`git log -p -- handoff.md`），当前会话授权优先。

## 一、当前状态

- 审核已闭合至第 **285** 批（`batch-fa1ef950617bf0290a74`）：80 条全为 Ashes DLC，75 done / 5 repair_required。
  surface 4 lane 的 identity 回显全部逐位一致，无错位；contextual run 只读冻结 envelope 与契约，未越界，无需 refreeze，
  复核 9 条；14 个观察逐条裁决。17 项门禁全过，审核任务快照均重放为 `DONE_VERIFIED`，
  证据提交 `cb5242c5d13ac8367d8095cb5c5e2d8b277e677a` 已 finalize。当前无 active batch。
- 修复窗口已闭合至 **29**：第 281–283 批共 21 条确认问题已修复并发布，译文提交
  `67a3a394b02b92a60a32b21c5df203ac08a1651e`；migration `33667e0f…` 的 21 个 successor
  须重新审核，不继承旧 revision 的 done 状态。窗口 29 证据 `21078cae` 已提交并推送；
  窗口 30 积压从第 284 批起累计，当前 12 条。
- 修复窗口 **27** 已完成 273–277 五批共 28 条确认问题的修复、复审、17 项门禁、译文提交、
  catalog/migration 发布及证据提交。证据提交 `351c6724d60221ffc1656ff1d97db2eecb2d0e02` 后的
  queue rebuild 通过；新 catalog 与 28 条待重新审核的 successor 均已核对。
- 窗口 27 译文提交为 `defcc44d6d01a1329d83b37b0dcbb83c56e4b631`；新 catalog 为
  `cdc76147d080c57a246273344897b397c53eded5051d701a3d7974dcb1f9e0f8`，migration 为
  `b8289b4f700157310fc4a583dab34cbd726be7c2a55895b4d24a942b607f8c63`。28 个 successor 必须重新审核，
  不继承旧 revision 的 done 状态。
- 2026-09-24 早些时候已提交并推送工具维护与文档整理，内容见第四节。
- 近六批结果：

| 批次 | batch id | 结果 | surface（gpt-6-sol） | contextual（opus-5-5） | 裁决 |
| --- | --- | --- | --- | --- | --- |
| 273 | `batch-5e69946bed52ed5a5cbc` | 78 done / 2 repair | 71 OK / 9 ISSUE | 8 OK / 1 ISSUE | 3 confirmed / 7 refuted |
| 274 | `batch-c03b7552b4059d697ec0` | 75 done / 5 repair | 69 OK / 11 ISSUE | 8 OK / 3 ISSUE | 8 confirmed / 6 refuted |
| 275 | `batch-54d2d16b94c511082107` | 74 done / 6 repair | 69 OK / 11 ISSUE | 7 OK / 4 ISSUE | 10 confirmed / 5 refuted |
| 276 | `batch-f8d6c02a3294c168f104` | 72 done / 6 repair / 2 blocked | 69 OK / 11 ISSUE | 6 OK / 5 ISSUE | 10 confirmed / 3 refuted / 3 pending observations |
| 277 | `batch-a2538cac10c65873a661` | 70 done / 9 repair / 1 blocked | 69 OK / 11 ISSUE | 7 OK / 4 ISSUE | 13 confirmed / 1 refuted / 1 pending observation |
| 278 | `batch-2dd6d21e34b360ebb6d9` | 73 done / 6 repair / 1 blocked | 69 OK / 11 ISSUE | 7 OK / 4 ISSUE | 10 confirmed / 4 refuted / 1 pending observation |
| 279 | `batch-99f8a711d02012a6de19` | 73 done / 7 repair | 70 OK / 10 ISSUE | 4 OK / 6 ISSUE | 11 confirmed / 3 refuted / 2 advisory |
| 280 | `batch-76f9078d25a218ccbe79` | 69 done / 11 repair | 61 OK / 19 ISSUE | 13 OK / 6 ISSUE | 16 confirmed / 6 refuted / 3 advisory |
| 281 | `batch-6b0d756f5c05a40663fd` | 73 done / 7 repair | 67 OK / 13 ISSUE | 7 OK / 6 ISSUE | 11 confirmed / 6 refuted / 2 advisory |
| 282 | `batch-523380060ecba03a1855` | 72 done / 8 repair | 64 OK / 16 ISSUE | 11 OK / 5 ISSUE | 13 confirmed / 3 refuted / 5 advisory |
| 283 | `batch-ecdac9654ed6a7ed78eb` | 73 done / 6 repair / 1 blocked | 67 OK / 13 ISSUE | 7 OK / 6 ISSUE | 10 confirmed / 5 refuted / 2 advisory / 2 pending |
| 284 | `batch-2693c7d9d6bb6b335806` | 72 done / 7 repair / 1 blocked | 68 OK / 12 ISSUE | 7 OK / 5 ISSUE | 10 confirmed / 4 refuted / 2 advisory / 1 pending |
| 285 | `batch-fa1ef950617bf0290a74` | 75 done / 5 repair | 71 OK / 9 ISSUE | 4 OK / 5 ISSUE | 7 confirmed / 2 refuted / 5 advisory |

每批证据摘要在 `evidence/quality/production-batches/<batch>-host-evidence/summary.md`。

## 二、授权与节奏（用户指示）

- 2026-09-23：先做工具维护，然后持续推进审核，不需逐批确认；有争议的条目列入 pending，等用户集中审阅。
- 2026-09-24：修复先记录，**积压达到 20 条或以上再一并修复**，取代原来每批审核后接一个小修复窗口的 1:1 节奏。
- 每批（或每个窗口）完全收口后 push；批次进行期间不得提交任何东西。
- 用户随后明确要求推进新批次，暂停已解除。第 276 批的 DLC reviewer 边界修复与按原模型重派也已获明确授权。
- 2026-09-25：第278批后的暂停已由用户明确解除（“验收完毕后合入主开发区，然后让主开发区空闲的 opus5.5 agent
  继续推进审核工作”）。主持由 Opus 5.5 接手，从第279批起按既定顺序连续推进；停止条件照常生效。
- 无需再次询问审核外发或 push 授权；现有授权继续有效。
- 审核模型：surface `codex/gpt-6-sol`（medium，auto-review），contextual `claude/claude-opus-5-5`（medium，auto）；
  修复 EXECUTOR `codex/gpt-5.6-sol`。

## 三、窗口 27 已修历史（28 条）

下表是窗口 27 已完成的冻结修复范围，仅作历史记录，不再是当前待修积压。

| 来源批次 | revision（前 8 位） | 修复内容 |
| --- | --- | --- |
| 273 | `fcb8219f` | “反魔法”提示第三行“拒绝使用法术”→无法使用法术与奥术驱动的装备（forbid_arcane 是硬限制） |
| 273 | `fd267689` | 领袖的皇冠描述整句（许多人而非大部分、秩序与纪律、效忠皇冠、称呼统一为“皇冠”、纳格尔领土而非大陆） |
| 274 | `fd89fad0` | 裂解：每目标每回合可各除一项物理和一项魔法增益；补回物理伤害→物理、时空伤害→魔法的对应关系 |
| 274 | `fd9c72bf` | 技能名 Unstoppable Nature“自然世界”→“势不可挡的自然”一类 |
| 274 | `fda88c96` | 技能名 Reflex Defense“闪避神经”→“反射防御”一类（机制是减伤与降低受暴击倍率） |
| 274 | `fdff442a` | 粘液：友方单位条件“经过”→处在粘液中 |
| 274 | `fe42c359` | 半身人炼金术士对话末句：恢复“越晚回来”与“冒烟的弹坑” |
| 275 | `fe5a84a1` | 燃烧之手：补“（及武器）”，体力回复改“每次命中” |
| 275 | `fe90619e` | 恶魔空间：补“每回合”、持续光环、“法术结束时” |
| 275 | `fec0939b` | 黑暗者古尔莫特墓志铭拆回三行（LF 6→5 实测） |
| 275 | `ff47fb86` | 回复纹身加载提示整句（预判伤害、提前准备；物品名统一“回复纹身”） |
| 275 | `ff585d0b` | 任务名 From bellow, it devours 与 mod-tome.lua:38225 对齐为“来自深渊，吞噬四方” |
| 275 | `ff658fab` | wispy purple cloak“脆弱的”→“缥缈的” |
| 276 | `ffb21dd4` | `seems less dangerous`：“平静了下来”→威胁降低 |
| 276 | `ffe80f4c` | 传送门描述补回 `strange` 的“奇异”限定 |
| 276 | `fff84873` | 石傀儡 `can become unstoppable`：改为可进入该状态，不写成永久不可阻挡 |
| 276 | `0523b499` | Ashes 灼热土地平台分裂的时序与意象，避免写成醒后已分离 |
| 276 | `0c22616d` | `treacherous road` 改为险途，保留世界之巅与引号 |
| 276 | `0ed56881` | `Most simply run` 改回逃跑，`destruction's engines` 不添战争机器 |
| 277 | `10419e2e` | black flame 恢复黑色，避免误作邪恶火焰 |
| 277 | `119af893` | extracting / willing 的斜体强调位置与原文对齐 |
| 277 | `120d3d48` | 水晶记忆对白恢复踏板、束缚装置及被删时序，不添“思维”限定 |
| 277 | `12c3c45f` | 3 arms 改“三条手臂”，非“三只手” |
| 277 | `1be82f2f` | primary ambush 改首轮伏击，并写明已脱身 |
| 277 | `218c180b` | 乌鲁洛克认可库马纳的心智、同条专名一致、锦标赛错字及体能耐力 |
| 277 | `21d89ecd` | 堡垒停在兵工厂上方而非主动瞄准；修复“怀着／所拥有”等错字和增译 |
| 277 | `28ea9897` | fiery display 恢复炽烈/火焰意象，不用闪电 |
| 277 | `295b84f0` | 恶魔形态说明后续行恢复两个制表符缩进；“半径”有机制依据，保留 |

范围与源码依据：273 见 `.ai/task/batch-5e69946bed52ed5a5cbc/WINDOW27-REPAIR-DECISION.json`，274–277 见各自
`.ai/task/<batch>/REPAIR-BACKLOG-DECISION.json` 与 `HOST-FINAL-DECISIONS.json`。
本窗发布记录见 [`evidence/quality/repair-window-27-20260924/PUBLICATION.md`](evidence/quality/repair-window-27-20260924/PUBLICATION.md)。

## 四、本轮工具维护与文档整理（2026-09-24）

- `queue.rebuild` 在 carry scope 内把完整重放交给后续步骤复用（仍每次完整重放）。
- 新增 `run_batch_steps.py rollover-chain --limit N`：关闭后的 queue rebuild + 下一批 start，只重放一次历史（约省 4 分钟）。
- 新增 `run_repair_steps.py publish-chain`：译文提交后的 queue rebuild + catalog build + migration plan/check/apply，
  只重放一次历史（每个窗口约省 4 分钟）。
- 新增 5 个回归测试；完整门禁 17/17 通过（含严格构建）。
- 新增 [审核操作指南](docs/review-operations-guide.md) 与 [宿主辅助件模板](docs/review-operations/templates/README.md)；
  删除过期的 `docs/baseline-batch-runbook-2026-09-06.md`、`docs/handoff-history-through-20260919.md`、
  `docs/review-handoff-20260918-batch192.md`，其中仍生效的裁决已并入指南第六节；引用处已改指向指南。
- 2026-09-25 工具优化（已合入 `d6dc518e`，随第279批一并推送）：A 门禁测试 fixture 隔离父进程缓存变量，
  父 shell `I18N_PROJECTION_CACHE=on` 可直接跑 prepare-evidence 与完整门禁，不再需要 unset（第279批已实测 17/17）；
  B 单次投影内复用完整相同行字节的已成功 catalog 行校验，cache-off 完整投影中位 251.99→87.58 s（实测），
  峰值 RSS +13.5%。磁盘缓存仍默认关闭；门禁运行期间不要编辑 `tools/`。详见
  [`docs/review-tool-speed-results-20260925.md`](docs/review-tool-speed-results-20260925.md)。
- 尚未实施的提速项：把 `surface-import` 与 `contextual-export` 合成一次调用（需放宽 `prepare_contextualN.py`
  的 phase 断言到 `deep_ready`），见指南 4.3 节。

## 五、下一步

1. 继续审核第 **286** 批；默认 80 条，按既有连续批次授权推进。先核对 HEAD、queue evidence HEAD、无 active batch。
2. 窗口 30 积压 **12** 条（第284–285批）。第284批 7 条：`ba84fb70`（德瑞宝传送研究 reverse-engineering/工艺品）`bade8870`（空间控制者击杀信息 teleported）
   `bc6203b6`（玛·洛克的历史（误译）标题）`bce9bc97`（战术简报：近战火球、写死“他”、may、增译手段，整段预检）
   `bfd436bc`（唯余灰烬末句“范围”重复；4 格括注贴合实现须保留）`c254cf06`（疫火权杖 go out of their way）`c6e8c8e4`（腐化之光“全体伤害”）。
   依据见 `.ai/task/batch-2693c7d9d6bb6b335806/HOST-FINAL-DECISIONS.json`；宿主补充建议 `a5ef7ca9`（乌尔罗格 fearsome to behold）仍待后续覆盖。
   第284批计时（实测，投影缓存 on）：start 89.3 s；adjudication chain（含 17 项门禁）160.4 s；finalize 91.1 s。
   第285批 5 条：`cdac06c9`（死亡之刃描述命名梗、巨剑、无与伦比）`ce3b5489`（遗失的记忆（1）：patch him up、眼睛、subpar、bubbles，整段预检）
   `d3c0b76c`（灵魂焚净 \n\t\t 两处）`d3db2e0a`（黑之铠描述残骸位置与引号）`dac57e56`（轨道基地战斗情报便条：拽走、双刃、构装体、打断、炸毁、隔离、写死“他”）。
   依据见 `.ai/task/batch-fa1ef950617bf0290a74/HOST-FINAL-DECISIONS.json`。
   第285批计时（实测，投影缓存 on）：start 1.7 s；adjudication chain（含 17 项门禁）160.8 s；finalize 91.7 s。
3. 窗口 28 的操作教训：同一 cycle 内 `RE_REVIEW` 之后冻结 `FINAL_REVIEW` 时，逻辑 attempt 使用 2；
   长 lore 条目开窗时由宿主先逐句预检，再合并进入修复与复审。
4. 专名待用户集中审阅：[待用户集中审阅的争议条目](evidence/quality/pending-user-review.md)（当前 25 项；第278/283批 Osmosis Regen(eration) 同族 pending，第277/284批 Corruption of the Doomed 同族 pending）。
5. 全 DLC 批次的操作要点：adjudication chain 一开始就传 SHA 核验的 `reviewN-source-root`；首次 contextual envelope 不含 checkout
   位置（`--ashes-checkout` 只在 refreeze 路径生效），Opus 可能自行搜寻而越界（第277、280批各一次），届时拒收并按 refreeze 重派；
   surface 某 lane 判废须整组用 `tools/surface_screen_manifest.py build --attempt 2 --group-id group-000-retry-02` 重建（envelope 字节不变）。

## 六、环境备忘

- 宿主工作目录 `.artifacts/i18n/continuation-20260923`（已 gitignore），Paseo workspace `wks_420314270844170b`，
  live profiles 快照 `$C/profiles-live-01.json`。
- 上游源码 `/workspace/t-engine4`，固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`；子 agent 看不到这个检出，
  它们报“commit 不存在、证据不足”时由宿主自查。
- 未跟踪文件 `.ai/consult/`、`recipe` 与旧的 `evidence/quality/production-batches/*-source-workset.json`（15 个）
  是既有遗留，保持不动。
- 历史保留边界：Archmage `8b977dd836…` 仍为范围外 pending；`RW1-SIB-01`、`RW1-SIB-02` 永久排除，不计阈值。
- 第 277 批 contextual 首轮 Opus 为找 DLC checkout 枚举 `/workspace`，输出被拒收并确认归档；重冻后单个 Opus run 读取边界通过并 DONE_VERIFIED。
- 第 276 批 contextual 原本按主游戏 6 条、Ashes DLC 5 条拆成两个 Opus run；DLC 两次旧输出因 `find /` 越界被拒收并归档。
  规则 prompt 与契约现明确禁止从 `/` 或无关目录扫描，并在新 envelope 中给出本批 DLC checkout；同 event 重冻后两路 reviewer 均通过读取边界检查与 `DONE_VERIFIED`。
