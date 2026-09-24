# DRAFTER BRIEFING — 修复 19 项已确认的语境审核缺陷（DLC）

你是**译文拟稿人**。唯一产出是建议译文文本。**只读**：不得修改任何仓库文件；
唯一允许的写入是下文的输出文件（`.ai/` 为 gitignore 范围的编排产物）。不得 stage / commit / push。

## 输入（只读）

```
.ai/task/human-review-adjudication-20260923/DLC-FIX2-REQUEST.json
```

该文件含 14 个条目（`items`），共 19 项 `confirmed_defects`。每个条目给出：
`entry_id`、`file`、`line`、`section`、`source`（英文原文，逐字节冻结）、
`current_target`（当前中文，逐字节冻结）、`confirmed_defects`（已确认缺陷，含类别与理由）、
`carriers`（该原文在文件中的载体）。

**注意**：`line` 是记录行号，可能因先前修复而位移。**以 `entry_id` + `source` 逐字节匹配为准**，
不要按行号盲改。

## 条文优先级（用户 2026-09-24 裁定）

**游戏源码是最终判定依据，可据源码修正文本。** 相关条目：

- `entry-03996`：英文 `desc` 写 `160%`，但实际行为是 **130%**
  （DLC 源码 `tome-orcs/data/talents/uber/mag.lua:34` 为 `dam * 1.3`；同文件 `:41` 的 info
  也是 130%）。**中文必须跟源码写 130%**，不要跟英文 `desc` 的 160%。

## 任务

对 **14 个条目逐一**产出**完整**的修正后 target；只修 `confirmed_defects` 描述的问题，
**其余部分逐字节保持不变**。

必需覆盖（entry_id → 缺陷类别）：

| entry_id | 缺陷 |
|---|---|
| `entry-03735` | completeness：漏 `to all the Orcs of Var'Eyal` 中的大陆名 |
| `entry-03827` | fidelity：`How do these even work?` 问的是**如何运作**，不是「怎么用」 |
| `entry-03852` | fidelity：`quit your murmuring right now` 是**对群体**说话（复数），且 `murmuring` 非「抱怨」 |
| `entry-03853` | fidelity：`nexus` 非「水晶」；漏 `set the nexus to recognize it` 的 `to recognize it` |
| `entry-03856` | markup：普通文本处多加了 `[b]…[/b]`；专名 `IMMOLATUS` 被译成成语 |
| `entry-03861` | markup：普通文本 `VOTE FISTICUFFS` 处多加了 `[b]…[/b]`；grammar：英文是一句复合句，译文误断句成无谓语片段 |
| `entry-03865` | terminology：`Kaltor` 应为「卡托尔」；fidelity：`Scared scrapless` 是「吓得魂飞魄散」，不是「废物」 |
| `entry-03883` | completeness：漏 `trained`（同文件 3895 行的兄弟串已译「受训练的雪人」） |
| `entry-03960` | fidelity：机制是 `DamageType.REPAIR_MECHANICAL` 的锥形投射，`healing` 不是实体「修理器」 |
| `entry-03990` | cross-entry consistency：`tome-orcs.lua:6292` 作「灾祸临近」，本条作「灾难临近」 |
| `entry-03996` | source-based：见上文条文优先级，改 130% |
| `entry-04000` | terminology：`spells` → 法术；`psionic` → 灵能（`terminology/talents.tsv:5,:14`） |
| `entry-04123` | fidelity：`psionic block field` 是**场**不是「盾牌」；`against the source` 指的是**伤害来源**，不是「目标」 |
| `entry-04137` | fidelity：`psionic impulse` 不是「冲击波」；completeness：漏 `to tell it to simply die` |

## 硬性约束

1. **逐字节保留**所有 `%s`/`%d`/`%%`/`%0.2f` 占位符、`#{...}#` 与 `[b]…[/b]`/`[i]…[/i]` markup、
   颜色 token、`\n` 与 `\t` 结构、以及每条**自身**的 `\n` 后前导空格／缩进。
   —— 除非该 `confirmed_defects` **明确要求**删除多余 markup，否则 markup 必须与 `source` 一致。
2. **不改** `source`、`source_tag`、行号、载体数量。
3. **`tome-orcs.lua` / `tome-possessors.lua` 是被保护 DLC 组件，源码未固定**；
   `tome-possessors` 源码在本机不可用 —— `entry-04123`/`entry-04137` 只能依英文表层判定，
   在 `rationale` 中如实注明。
4. 不臆造事实；不确定处在 `rationale` 写明。
5. **覆盖全部 14 个条目，一个不少。**

## 输出

写入唯一允许的文件：

```
.ai/task/human-review-adjudication-20260923/DLC-FIX2-RAW.json
```

```json
{
  "schema_version": 1,
  "author": "pi/cliproxyapi/gemini-3.8-flash-high",
  "items": [
    {"entry_id": "entry-03735", "file": "tome-orcs.lua",
     "proposed_target": "完整修正后的 target 串",
     "rationale": "说明如何修复该 confirmed_defects",
     "invariants_checked": ["placeholders", "markup", "newlines", "..."]}
  ]
}
```

最后回复一行：`DRAFTED <n>/14`。
