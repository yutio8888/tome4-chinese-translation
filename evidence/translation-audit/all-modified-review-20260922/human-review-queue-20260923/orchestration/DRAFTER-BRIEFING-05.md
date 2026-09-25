# DRAFTER BRIEFING — SCOPE-22（wave 1–3 confirmed 修复拟稿）

你是**译文拟稿人**。唯一产出是建议译文文本。**只读**：不得修改任何仓库文件；
唯一允许的写入是下文的输出文件（`.ai/` 属 gitignore 范围）。不得 stage / commit / push。

## 输入（只读）

```
.ai/task/human-review-adjudication-20260923/FIX-REQUEST-22.json
```

含 11 个条目。每条给出 `entry_id` / `file` / `section` / `source` / `current_target` /
`what_must_change`（已确认缺陷与必须改什么，只描述事实，不给答案文本）/ `invariants`，
并已核验 `source`、`current_target` 在文件中各恰好出现 1 次。

## 任务

对 **11 个条目逐一**产出**完整**的修正后 target。只修 `what_must_change` 描述的问题，
**其余部分逐字节保持不变**。

## 硬性约束

1. **逐字节保留**所有 `%s`/`%d`/`%%` 占位符、`#{...}#` 与 `[i]…[/i]`/`[b]…[/b]` markup、
   颜色 token（`#LIGHT_UMBER#`、`#WHITE#`、`#DARK_ORCHID#`、`#LIGHT_RED#`、`#LIGHT_GREEN#` 等）、
   `\n` 结构，以及 `source` 中出现的特殊分隔符 **`§`**（如 `infusions§runes`）。
2. **不得增删换行**：`\n` 数量与位置必须与 `current_target` 一致。
3. **不改** `source`、`source_tag`、行号、载体数量。
4. **`entry-00111` / `entry-00145`**：整条字符串内的 `嵌件系统`/`嵌件` 共 4 处都要改；
   同一字符串的 Tinker system 行与 Salves 行都要覆盖。
5. 不臆造事实；不确定处在 `rationale` 写明。
6. **覆盖全部 11 个条目，一个不少。**

## 术语依据

| source | 译名 | 依据 |
|---|---|---|
| `tinker`（实体类型） | 蒸汽工具 | `terminology/items.tsv:24`，`existing`；仓内 `蒸汽工具` 10 处 |
| `Writhing One`（birth descriptor） | 蜿蜒怪人 | `terminology/classes.tsv:43`，`existing`；`tome-cults.lua:4972` |
| `Mana`（资源） | 法力值 | `terminology/resources.tsv:3`，`existing` |
| `mag`（属性） | 魔力 | `terminology/combat.tsv:127`（与 Mana 区分） |

## 输出

写入唯一允许的文件：

```
.ai/task/human-review-adjudication-20260923/FIX-RAW-22.json
```

```json
{
  "schema_version": 1,
  "author": "pi/cpa/gemini-3.8-flash-high",
  "items": [
    {"entry_id": "entry-00111", "file": "engine.lua",
     "proposed_target": "完整修正后的 target 串",
     "rationale": "说明如何修复 what_must_change",
     "invariants_checked": ["placeholders", "markup", "newlines", "§ separator"]}
  ]
}
```

最后回复一行：`DRAFTED <n>/11`。
