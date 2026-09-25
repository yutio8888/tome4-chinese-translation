# 最终报告：已修改译文的全量审核与修复

- task_id：`human-review-adjudication-20260923`（父任务）
- 路线：`translation_contextual_v2`（有界 bundle 独立复审）＋ 主代理逐条源码裁决 ＋ 模型拟稿 ＋ EXECUTOR 落盘 ＋ cycle-1 有界复审
- 工作区固定版本：public `commit:624a6732`；DLC 快照 `snapshot:c49975dd…`（源码未固定）
- 生成时间：2026-09-25
- 主代理未撰写任何译文；所有 target 文本由 `pi/cpa/gemini-3.8-flash-high` 拟稿

## 一、审核覆盖

| 范围 | 规模 | 结果 |
| --- | --- | --- |
| 人工批阅队列（601 行） | 15 个批次 | 全部裁决；`scope-16`/`scope-17` 处置遗留 19 项 |
| DLC 语境复审（v2） | 5 bundle / 89 修订 | 5/5 `DONE_VERIFIED`；15 finding → 19 confirmed / 3 advisory / 2 pending |
| DLC 修复后 cycle-1 | 14 修订 | `ctx2-dlc-fix-01` `DONE_VERIFIED`（1 finding） |
| public 语境复审（v2） | **42 bundle / 497 修订** | **42/42 `DONE_VERIFIED`** |
| public 修复后 cycle-1 | 30 修订 | `ctx2-fix21-pub-01`（18）、`ctx2-fix22-pub-01`（11）均 `DONE_VERIFIED`，0 issue |

public finding 合计 54（wave 1–3 15 + 后续 39），DLC 15，修复后复审新增 2。

## 二、已落盘的修复

| 阶段 | 文件 | 编辑数 | 内容 |
| --- | --- | --- | --- |
| scope-16 | `mod-tome.lua`、`tome-orcs.lua`、`terminology/combat.tsv` | 11 + 1 术语 | 族内对齐与用户批准项；`manaburn arcane`=奥术法力燃烧 |
| scope-17 | `mod-tome.lua`、`tome-orcs.lua` | 21 + 删 2 陈旧键 | farportal 统一为「远行传送门」 |
| scope-20 | `tome-orcs.lua`、`tome-possessors.lua` | 19 缺陷 / 14 条目 | DLC confirmed 修复（含依源码把 160% 改为 130%） |
| scope-21 | `mod-tome.lua`、`tome-orcs.lua` | 19 | 后续 v2 confirmed（术语、机制、完整性） |
| scope-22 | `mod-tome.lua`、`engine.lua`、`mod-boot.lua` | 11 | wave 1–3 confirmed（tinker→蒸汽工具、Writhing One→蜿蜒怪人、change level、brew、Sorcerers、exploded、mana、an other place） |

合计落盘 **61 处 target 编辑 + 1 条术语登记 + 2 个陈旧键删除**，覆盖 4 个 Lua 文件。

## 三、门禁（逐批）

| 检查 | 结果 |
| --- | --- |
| `tools/i18n lint --strict` | **30305 条，0 错 0 警** |
| `git diff --check` | clean |
| 占位符／markup／颜色码／换行／`§` 不变量 | 每批 100% 通过 |
| 逐字节验证 | 每批 `baseline + edits == 当前文件`（EXACT MATCH） |
| 运行键扫描 `classify_runtime_keys.py` | 桶 B 0 / 桶 C 0（无新增同 section 冲突） |
| 术语审计 `audit_static` / `audit_dynamic` | 与既有基线一致，无新增 finding |
| `tools/i18n build --profile full` | **exit 0**，engine/boot/tome/example 全 OK |
| `tools/i18n build --profile addon --require-complete` | exit 5（**既有**：DLC 层 `baseline-pending`，官方 locale/源码未固定；core-addon 层 OK） |

> `tools/i18n proposal --strict` 不适用：工具链 workset 以 `stable_entry_id`（sha256）为键，本任务以
> `entry-NNNNN` 为键，命名空间不兼容；已用等价严格检查替代。

## 四、未修改（记录在案）

**用户裁定不改**
- `entry-00866` / `entry-00873`：`restorative` 沿用官方 zh_hans 译法「振奋的／振奋」。

**族级问题（本轮记录，待定）**
1. `Magic` 作为属性值：属性名 = **魔力**（`t("Magic","魔力","stat name")`、官方 locale、术语库），
   但自由文本 `based on Magic` 仓内多数为「基于魔法」（21 vs 3）。涉及 `entry-01625`（deferred）、`entry-01605`。
2. `frenzy` 效果名：`EFF_FRENZY`（吞噬者／Bloodrage／神器施放）效果自身显示名为「狂热」，
   术语库却记 `frenzy=狂乱`。涉及 `entry-01976`（advisory）。
3. `undead` 自由文本：官方结构化术语 `undead=亡灵`／`Undead=不死族`，自由文本官方自身混用四种。
   涉及 `entry-01256`（advisory）。

**上游问题**
- `entry-02644`（英文 `long_desc` 写 poison resistance，机制实为 poison_immune）、
  `entry-02125`（英文自身把 Accuracy/damage 次序写反）、`entry-02067`（`races.lua:692` tformat 实参倒置）。

**已在主工作区修复，本 worktree 不改**
- `entry-00184`、`entry-00492`。

**advisory**
- 共 19 + 3 条（静态排版、早前已裁决过的同类 claim、风格/语体），见
  `ADJUDICATION-v2-PUBLIC.md` 与 `CONTEXTUAL-V2-DLC-FINDINGS.json`。

## 五、记录更正

- `entry-00111`/`entry-00145` 的 `scope_note` 曾称兄弟串属工作集之外的另一个 revision；
  逐字节复核后**不成立**（`嵌件` 4 处都在同一条 `t()` 内），已更正并一并修复（scope-22）。
- provider 别名 `cliproxyapi` → `cpa`；驱动完成判定改为 `STATE.state == DONE`。

## 六、生命周期

- 全部 v2 reviewer／drafter／executor 均已结束；reviewer 已 `archive` 且 `archive_confirmed=true`。
- 被 v2 取代的 v1 任务 `ctx-public-20260924` / `ctx-dlc-20260924` 已置 `STOP`（`SUPERSEDED`），子 agent 已归档。
- 当前 live 子 agent：**0**。
