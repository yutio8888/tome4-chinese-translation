# SCOPE-16 收尾批裁决与执行报告

task_id: `human-review-adjudication-20260923`
phase: `scope-16`（601 行裁决完成后的遗留项处置）
日期: 2026-09-24
baseline: `d39131a8`（派发时 HEAD `d77cfab4`）
executor: `claude/claude-opus-5-5`（medium）
drafter: `pi/cliproxyapi/gemini-3.8-flash-high`（high）

## 1. 范围

本批处置此前 19 项 `deferred`（来自 `PENDING-ITEMS.json`）。**主代理不撰写任何译文**：
所有新 target 由 Gemini 3.8 Flash 拟稿，EXECUTOR 逐字节落盘。

处置分类：

| 分类 | 数量 | 说明 |
| --- | --- | --- |
| 应用 target 修改 | 11 处（10 entry） | 族内对齐 5 项 + 用户批准修改 5 项 |
| 术语登记 | 1 行 | `manaburn arcane` → 奥术法力燃烧 |
| 暂缓（held） | 3 项 | 见 §4 |
| 仅记录 no_change | 9 项 | 用户裁定不改 / 主工作区已修 / 上游缺陷 |

## 2. 应用的修改（11 处）

| entry | 文件:行 | 改动 | 依据 |
| --- | --- | --- | --- |
| `entry-00216` | mod-tome.lua:403 | 迷路的腐化者 → **迷路的堕落者** | Defiler=堕落系 类别名；避与 Corruptor=腐化者 同名 |
| `entry-00730` | mod-tome.lua:8265 | 它的眼睛 → **它所有的眼睛都** | 补回漏译 `all`；参照 8270「它所有的眼睛」 |
| `entry-00730` | mod-tome.lua:37898 | 同上（**逐字节相同**） | 同源同键孪生载体 |
| `entry-01262` | mod-tome.lua:17299 | 加斯塔德 → **加斯塔德内斯** | 补全挪威语姓氏词尾 `-nes` |
| `entry-01290` | mod-tome.lua:17978 | 大爆炸→**大灾变**；猎魔者→**魔法猎手** | 同节 `entry-01300`；`Spellhunter's Guide`=魔法猎手 |
| `entry-03323` | mod-tome.lua:43240 | 同上；**保留 `\n\n` 后前导空格** | 近孪生（英文仅差一空格）；静态排版不整理 |
| `entry-02456` | mod-tome.lua:31266 | 枯萎能量 → **堕落力量** | 觉醒技能「堕落之壳」；corruption=堕落 |
| `entry-02791` | mod-tome.lua:36742 | 时空克隆 → **时空复制体** | 同节 36741 |
| `entry-03149` | mod-tome.lua:40781 | 推挤 → **击退攻击** | 技能名 27003；教程 32976 |
| `entry-03149` | mod-tome.lua:40782 | 推挤 → **击退攻击** | 同技能名缺陷（**不同源串**，非孪生） |
| `entry-04115` | tome-orcs.lua:8341 | 3 处修正 | `This IS relevant` 被译反；`Neither` 主语漂移；`filthy`→肮脏 |

**术语登记**：`terminology/combat.tsv:26` `manaburn arcane` → `奥术法力燃烧`，
status `existing` → `preferred`。

> 来源：DLC `tome-orcs.lua` 源码**未固定**（`source_pinning: unpinned`），
> `entry-04115` 的核验以实际可读公开源码为准。

## 3. 门禁

| 检查 | 结果 |
| --- | --- |
| `tools/i18n lint --strict` | 30307 条，**0 错 0 警** |
| `git diff --check` | clean |
| 变更文件 | `mod-tome.lua`、`tome-orcs.lua`、`terminology/combat.tsv`（+ 台账） |
| 占位符／markup／颜色码／换行不变量 | 11/11 通过（含 `entry-03323` 前导空格保留） |
| 术语审计 `audit_static` / `audit_dynamic` / `annotate_domains` | 通过；**无新增 finding**（既有 S1.1 Aeryn、Air mismatch 与本批无关） |
| 独立逐条核验（ORCHESTRATOR） | 11/11 落盘值 == spec `new_target` |

## 4. 暂缓项（held，需用户决定）

| entry | 原因 |
| --- | --- |
| `entry-01984` | **不是**用户定义的「失效键」。用户策略针对 `-- old translated text` 注释块内的键（全文件仅 `mod-tome.lua:1131` 一处）。这是**活跃** `t()` 调用：其英文在固定源码已不存在（`horrors.lua:671` 改为 `15 turns`），但**官方 locale 仍保留旧键**（`zh_hans.lua:25855`），canonical 刻意同时保留新旧两版。删除属结构性编辑，会抬高 `official_only` 差值。 |
| `entry-01988` | 同 `entry-01984`（官方 `zh_hans.lua:25905` 亦为旧版）。 |
| `entry-02982` | **依据被推翻**。先前称「9/10 载体已用远行传送门」，实测**恰好相反**：11 个载体中 **9 个用「传送门是」**、仅 2 个用「远行传送门」（`mod-tome.lua:40331`、`tome-orcs.lua:6936`）；主工作区同为 9:1。改本条会**逆多数**。需先定族级策略。 |

## 5. 记录为 no_change（9 项）

- 用户裁定不改：`entry-00634`（death_message 词表维持冻结）、`entry-00646`/`entry-00653`（保留现译并登记术语）、`entry-02212`（A 组 flame 暂不修改）
- 主工作区已修，合并即生效：`entry-00184`、`entry-00492`
- 上游缺陷：`entry-02067`（`races.lua:692` 的 `tformat` 实参顺序与英文相反）
- 拟稿结论无需修改：`entry-02850`（片段经 `args_order={2,1}` 拼入句中，本不应带句末标点）

## 6. 观察（未改）

- `entry-03149` 符文名 `mod-tome.lua:40780`「启蒙符文：冲撞」未改：符文名自成一套用词（Mana Gale 符文=法力风暴，而其技能名=魔法风暴），与技能名缺陷不同源。
- `entry-02212` 技能名 `Mana Gale`=魔法风暴 vs 其符文名=法力风暴，为既有分歧，不在本批范围。

## 7. 生命周期

- `drafter-01`（`c8c03659…`）与 `executor-16`（`406b5b16…`）均 `archived` + `archive_confirmed=true`，`lineage_verified=true`，parent 均为 `330b8a33…`。
- 本批结束后活跃 child：**0**。
