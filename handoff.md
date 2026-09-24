# 翻译审核当前交接

更新时间：2026-09-24（审核276已 finalize；修复积压19条；连续审核已恢复）

接手前先读 [`AGENTS.md`](AGENTS.md) 与 [审核操作指南](docs/review-operations-guide.md)。本文只写当前状态、
授权和待办；操作步骤、判据、生效裁决与已知陷阱都在指南里。历史交接正文见本文件的 git 历史
（`git log -p -- handoff.md`），当前会话授权优先。

## 一、当前状态

- 审核已闭合至第 **276** 批（`batch-f8d6c02a3294c168f104`，证据及规则修复 `f4caea17`，finalize 通过）。
  下一批是 277，默认 80 条。没有 active batch。
- 修复窗口已闭合至 **26**（证据 `b2ebc16d`）。下一个窗口是 27，等积压达到 20 条再开。
- 2026-09-24 已提交并推送工具维护与文档整理（本交接所在提交），内容见第四节。
- 近四批结果：

| 批次 | batch id | 结果 | surface（gpt-6-sol） | contextual（opus-5-5） | 裁决 |
| --- | --- | --- | --- | --- | --- |
| 273 | `batch-5e69946bed52ed5a5cbc` | 78 done / 2 repair | 71 OK / 9 ISSUE | 8 OK / 1 ISSUE | 3 confirmed / 7 refuted |
| 274 | `batch-c03b7552b4059d697ec0` | 75 done / 5 repair | 69 OK / 11 ISSUE | 8 OK / 3 ISSUE | 8 confirmed / 6 refuted |
| 275 | `batch-54d2d16b94c511082107` | 74 done / 6 repair | 69 OK / 11 ISSUE | 7 OK / 4 ISSUE | 10 confirmed / 5 refuted |
| 276 | `batch-f8d6c02a3294c168f104` | 72 done / 6 repair / 2 blocked | 69 OK / 11 ISSUE | 6 OK / 5 ISSUE | 10 confirmed / 3 refuted / 3 pending observations |

每批证据摘要在 `evidence/quality/production-batches/<batch>-host-evidence/summary.md`。

## 二、授权与节奏（用户指示）

- 2026-09-23：先做工具维护，然后持续推进审核，不需逐批确认；有争议的条目列入 pending，等用户集中审阅。
- 2026-09-24：修复先记录，**积压达到 20 条或以上再一并修复**，取代原来每批审核后接一个小修复窗口的 1:1 节奏。
- 每批（或每个窗口）完全收口后 push；批次进行期间不得提交任何东西。
- 用户随后明确要求推进新批次，暂停已解除。第 276 批的 DLC reviewer 边界修复与按原模型重派也已获明确授权。
- 审核模型：surface `codex/gpt-6-sol`（medium，auto-review），contextual `claude/claude-opus-5-5`（medium，auto）；
  修复 EXECUTOR `codex/gpt-5.6-sol`。

## 三、修复积压（19 条，窗口 27 的范围）

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

范围与源码依据：273 见 `.ai/task/batch-5e69946bed52ed5a5cbc/WINDOW27-REPAIR-DECISION.json`，274–276 见各自
`.ai/task/<batch>/REPAIR-BACKLOG-DECISION.json` 与 `HOST-FINAL-DECISIONS.json`。
宿主目录里的 `setup_window27_task.py` 只按 273 的 2 条生成、**未运行**；开窗时要改成多来源批次版本
（preflight 一次最多 3 个 batch id，现有 4 个来源批次；开窗时需按指南处理输入分组，不可直接运行旧脚本）。

## 四、本轮工具维护与文档整理（2026-09-24）

- `queue.rebuild` 在 carry scope 内把完整重放交给后续步骤复用（仍每次完整重放）。
- 新增 `run_batch_steps.py rollover-chain --limit N`：关闭后的 queue rebuild + 下一批 start，只重放一次历史（约省 4 分钟）。
- 新增 `run_repair_steps.py publish-chain`：译文提交后的 queue rebuild + catalog build + migration plan/check/apply，
  只重放一次历史（每个窗口约省 4 分钟）。
- 新增 5 个回归测试；完整门禁 17/17 通过（含严格构建）。
- 新增 [审核操作指南](docs/review-operations-guide.md) 与 [宿主辅助件模板](docs/review-operations/templates/README.md)；
  删除过期的 `docs/baseline-batch-runbook-2026-09-06.md`、`docs/handoff-history-through-20260919.md`、
  `docs/review-handoff-20260918-batch192.md`，其中仍生效的裁决已并入指南第六节；引用处已改指向指南。
- 尚未实施的提速项：把 `surface-import` 与 `contextual-export` 合成一次调用（需放宽 `prepare_contextualN.py`
  的 phase 断言到 `deep_ready`），见指南 4.3 节。

## 五、下一步（恢复后）

1. 审核277：`python3 -B tools/orchestration/run_batch_steps.py rollover-chain --limit 80` 可直接开批（首次使用，
   留意输出里的 batch id 与 rebuild 报告）；或沿用 `production batch start --limit 80`。
   脚本从本批已闭合的 `*276.py` 生成，见指南第三节。
2. 继续攒批；积压达到 20 条后开合并修复窗口 27（指南第五节，首次使用 `publish-chain`）。
3. 用户集中审阅 pending：[待用户集中审阅的争议条目](evidence/quality/pending-user-review.md)（当前 21 项，含
   `cunning` 叙事语境、若干技能／神器命名、死亡描述表等）。

## 六、环境备忘

- 宿主工作目录 `.artifacts/i18n/continuation-20260923`（已 gitignore），Paseo workspace `wks_420314270844170b`，
  live profiles 快照 `$C/profiles-live-01.json`。
- 上游源码 `/workspace/t-engine4`，固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`；子 agent 看不到这个检出，
  它们报“commit 不存在、证据不足”时由宿主自查。
- 未跟踪文件 `.ai/consult/`、`recipe` 与旧的 `evidence/quality/production-batches/*-source-workset.json`（15 个）
  是既有遗留，保持不动。
- 历史保留边界：Archmage `8b977dd836…` 仍为范围外 pending；`RW1-SIB-01`、`RW1-SIB-02` 永久排除，不计阈值。
- 第 276 批 contextual 原本按主游戏 6 条、Ashes DLC 5 条拆成两个 Opus run；DLC 两次旧输出因 `find /` 越界被拒收并归档。
  规则 prompt 与契约现明确禁止从 `/` 或无关目录扫描，并在新 envelope 中给出本批 DLC checkout；同 event 重冻后两路 reviewer 均通过读取边界检查与 `DONE_VERIFIED`。
