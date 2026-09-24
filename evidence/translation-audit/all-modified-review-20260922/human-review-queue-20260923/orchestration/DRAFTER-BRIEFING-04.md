# DRAFTER BRIEFING — SCOPE-21（public 19 项 confirmed 修复拟稿）

你是**译文拟稿人**。唯一产出是建议译文文本。**只读**：不得修改任何仓库文件；
唯一允许的写入是下文的输出文件（`.ai/` 属 gitignore 范围）。不得 stage / commit / push。

## 输入（只读）

```
.ai/task/human-review-adjudication-20260923/FIX-REQUEST-21.json
```

含 19 个条目（`items`）。每条给出：

- `entry_id`、`file`、`line`、`section`、`source_tag`
- `source`：英文原文（逐字节冻结）
- `current_target`：当前中文（逐字节冻结）
- `what_must_change`：**已确认的缺陷与必须改什么**（只描述事实，不给答案文本）
- `invariants`：必须保持的逐字节不变量
- `target_occurrences` / `source_occurrences`：已在文件中核验为各 1 次（唯一匹配）

**注意**：`line` 是记录行号，可能因先前修复位移。**以 `entry_id` + `source` 逐字节匹配为准**，
不要按行号盲改。

## 任务

对 **19 个条目逐一**产出**完整**的修正后 target。只修 `what_must_change` 描述的问题，
**其余部分逐字节保持不变**。目标文本必须是完整串（含全部 `\n`、`\t\t`、颜色码、markup）。

## 硬性约束

1. **逐字节保留**所有 `%s`/`%d`/`%0.2f`/`%%` 占位符、`#{...}#` 与 `[i]…[/i]`/`[b]…[/b]` markup、
   颜色 token、`\n` 与 `\t\t` 结构。
2. **不得增删换行**：除非 `what_must_change` 明确要求，`\n` 数量与位置必须与 `current_target` 一致。
3. **不改** `source`、`source_tag`、行号、载体数量。
4. **`entry-01605` 的 `基于魔法` 属于本轮 DEFERRED 项，不得修改**；该条只改「时空地雷」相关处。
5. **`entry-03856` 在受保护 DLC `tome-orcs.lua`，源码未固定**；只能依英文表层与术语库判定，
   在 `rationale` 中如实注明。
6. 不臆造事实；不确定处在 `rationale` 写明。
7. **覆盖全部 19 个条目，一个不少。**

## 术语依据（只列相关项）

| source | 译名 | 依据 |
|---|---|---|
| `inscriptions`（类别） | 刻印 | `terminology/talents.tsv:8` preferred |
| `Magic`（属性名） | 魔力 | 本轮不涉及（deferred） |
| `stun` | 震慑 | `terminology/combat.tsv:40`（≠ daze 眩晕） |
| `ice`（伤害类型） | 寒冰 | `terminology/combat.tsv:24` |
| `darkness`（伤害类型） | 暗影 | `terminology/combat.tsv:10` |
| `undead`（实体类型） | 亡灵 | `terminology/creatures.tsv:12` |
| `wound`（效果子类型） | 创伤 | `terminology/combat.tsv:74` |
| `construct`（实体类型） | 构装体 | `terminology/creatures.tsv:4` preferred |

## 输出

写入唯一允许的文件：

```
.ai/task/human-review-adjudication-20260923/FIX-RAW-21.json
```

```json
{
  "schema_version": 1,
  "author": "pi/cpa/gemini-3.8-flash-high",
  "items": [
    {"entry_id": "entry-01221", "file": "mod-tome.lua",
     "proposed_target": "完整修正后的 target 串",
     "rationale": "说明如何修复 what_must_change",
     "invariants_checked": ["placeholders", "markup", "newlines", "..."]}
  ]
}
```

最后回复一行：`DRAFTED <n>/19`。
