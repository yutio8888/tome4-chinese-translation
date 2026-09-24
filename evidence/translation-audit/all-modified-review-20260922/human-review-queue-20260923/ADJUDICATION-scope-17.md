# SCOPE-17 farportal 统一与授权删除报告

task_id: `human-review-adjudication-20260923`
phase: `scope-17`
日期: 2026-09-24
drafter: `pi/cliproxyapi/gemini-3.8-flash-high`（high）
executor: `codex/gpt-6-sol`（medium）

## 1. 检查结论：farportal 翻译现状

`Farportal` 相关 `t()` 调用共 **85 个**。词形普查（改动前）：

| 形态 | 次数 | 判定 |
| --- | --- | --- |
| **远行传送门** | **89** | **既定术语**（`terminology/items.tsv:37` `exploratory farportal`=探索用远行传送门，`preferred`；`entry-03070` `Farportal`=远行传送门） |
| 虚空传送门 | 13 | `void farportal`，另一实体，**正确，不动** |
| 传送门是…（描述句） | 9 | 未用术语 |
| 夏·图尔传送门 | 6 | 未用术语 |
| 远距传送门 | 1 | **异形**（疑似笔误） |
| 远程传送门 | 1 | 异形 |
| 远传送门 | 1 | **缺字** |
| 失落的传送门 | 1 | 未用术语 |

> 官方 locale（`zh_hans.lua`）用的是**远古传送门**，与本项目选定的**远行传送门**不同。
> 这是项目自身的术语选择，未采纳官方译法。

**发现 19 处「源含 farportal 但译文未用既定术语」**，另加描述句族中 2 个已用术语但
**第二句与多数派不一致**的载体，合计 **21 处**。

## 2. 处置：21 处 target 修改

### A 组 · 描述句族（11 个载体）

共享英文首句：

> A farportal is a way to travel incredible distances in the blink of an eye.

统一为：

> **远行传送门能让人眨眼间跨越难以想象的距离。**

**11/11 逐字节一致**。各载体后半句按自身源文本保留（源文本本就分三支：
`They usually require an external item to use.` 1 处 / 加 `You have no idea if it is even two-way.` 8 处 /
`They were left behind by the powerful Sher'tul race.` 2 处）。

第二句 `You have no idea if it is even two-way.` 原有 6:2 两种译法，已统一为多数派
**「你不知道这道门是否为双向的。」**（`40331`、`6936` 由「你甚至不知道它是否能双向通行。」改齐）。

`38725`、`38730` 的 `\n` 后前导空格按静态排版政策保留。

### B 组 · 其余 10 个载体

| 位置 | 改动 |
| --- | --- |
| `12275` | 夏·图尔远程传送门 → 夏·图尔**远行**传送门 |
| `14630`（2 处） | 夏·图尔传送门 → 夏·图尔远行传送门 |
| `15094` | 同上 |
| `17791` | 同上 |
| `18119`（3 处） | 传送门 → 远行传送门 |
| `19407` | 失落的传送门 → 失落的**远行**传送门 |
| `19408` | 夏·图尔传送门 → 夏·图尔远行传送门 |
| `20290` | 远传送门能量 → **远行**传送门能量（补缺字） |
| `38485` | 远距传送门：灼烧之痕 → **远行**传送门：灼烧之痕 |
| `39386` | 传送门的能量 → 远行传送门的能量 |

## 3. 授权删除（2 个陈旧键）

| entry | 位置 | 删除的旧英文 |
| --- | --- | --- |
| `entry-01984` | `mod-tome.lua:25923` | `Open a hole in space, summoning an animated blade for 10 turns.` |
| `entry-01988` | `mod-tome.lua:25973` | Heroism 旧版说明（无 `to a maximum of 100%%`） |

两者均为**活跃 `t()` 调用**但英文在固定源码已不存在（`horrors.lua:671` 已是 `15 turns`；
`inscriptions.lua:247` 已含 `to a maximum of 100%%`）。活跃孪生条 `entry-01986` / `entry-02000` 保留。
删除后已核验两串在文件中**不再存在**。

## 4. 门禁

| 检查 | 结果 |
| --- | --- |
| `tools/i18n lint --strict` | **30305 条，0 错 0 警**（因删 2 键由 30307 降至 30305） |
| `git diff --check` | clean |
| 变更文件 | `mod-tome.lua`、`tome-orcs.lua` |
| 占位符／markup／颜色码／换行／前导空格不变量 | **21/21 通过** |
| 删除后源串不存在 | 2/2 确认 |
| 描述句族首句字节一致 | **11/11 确认** |

最终词形普查：**远行传送门 111 次**，`远距`/`远传`/`远程` 异形 **0**，虚空传送门 13 次（不动）。

## 5. 生命周期

- `drafter-02`（`e71ee0ca…`）与 `executor-17`（`d5b39528…`）均 `archived` + `archive_confirmed=true`，
  `lineage_verified=true`，parent 均为 `330b8a33…`。
- 本阶段结束后活跃 child：**0**。
- `held_items` 已清空：`entry-02982` 由本次统一一并解决；`entry-01984`/`entry-01988` 已授权删除。
