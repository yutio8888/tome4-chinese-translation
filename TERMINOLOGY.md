# ToME4 汉化术语库

这是基于当前翻译文件维护的术语库。它记录“英文原文—中文译名—语义类别”的关系，不直接替换游戏翻译文件。

数据文件为 [`terminology/`](./terminology/)。采用 TSV 是为了让 Lua、Shell、表格工具都能读取；字段中的英文原文必须保持游戏源码中的大小写、空格和标点。

## 字段

| 字段 | 含义 |
| --- | --- |
| `source` | 游戏源码中的英文字符串，大小写敏感 |
| `target` | 当前采用的中文译名 |
| `category` | 本术语库的规范类别，见下表 |
| `domain` | 游戏领域（功能域），见“领域分类”一节 |
| `source_tag` | 现有翻译系统 `t(...)` 的第三参数，保留原始上下文；TSV 中字面量 `nil` 表示 Lua `nil`，空字段表示空字符串，两者不互配 |
| `status` | `existing` 表示从当前翻译中整理，`review` 表示需要统一或复核，`preferred` 表示已确认的规范译法 |
| `scope` | 术语适用的组件范围：`core`、`addon`、`dlc`、`global` 或 `multi`，见下表 |
| `notes` | 语境、别名、冲突或审校说明 |

### `scope` 语义

| 值 | 匹配组件 |
| --- | --- |
| `global` | 全部组件 |
| `multi` | 全部组件；保留该值以表示跨组件语境 |
| `dlc` | 工具链既有 DLC 分组：`ashes-urhrok`、`cults`、`items-vault`、`orcs`、`possessors` |
| `core` | 除上述五个 `dlc` 组件以外的全部组件 |
| `addon` | `addon-dev`、`items-vault`、`possessors` |

`addon` 是独立的语义集，允许与 `dlc`/`core` 分组重叠：`items-vault` 和 `possessors` 同时属于 `addon` 与 `dlc`，`addon-dev` 同时属于 `addon` 与 `core`。未知 `scope` 是非法值，不匹配任何组件。

## 规范类别

类别使用 `T.` 前缀，表示它们是建立在现有 `t`/`tDef` 分类上的术语类别，而不是替代原始标签。

| 类别 | 用途 | 常见现有 `source_tag` |
| --- | --- | --- |
| `T.PN.PERSON` | 人物、角色名 | `entity name`、`birth descriptor name` |
| `T.PN.PLACE` | 城镇、区域、地图地点 | `entity name`、`_t` |
| `T.PN.FACTION` | 阵营、组织、部族 | `faction name`、`entity keyword` |
| `T.PN.RACE` | 种族及其形容词 | `birth descriptor name`、`entity subtype` |
| `T.PN.WORLD` | 世界、时代、历史事件 | `_t`、`effect subtype` |
| `T.GAME.CLASS` | 职业、角色类别 | `birth descriptor name`、`talent type` |
| `T.GAME.TALENT` | 技能名称 | `talent name` |
| `T.GAME.TALENT_CATEGORY` | 技能树、技能类别 | `talent category`、`talent type` |
| `T.GAME.DAMAGE` | 伤害类型及伤害变体 | `damage type` |
| `T.GAME.EFFECT` | 状态、效果、控制类型 | `effect subtype` |
| `T.GAME.ENTITY` | 生物、物品、地形的实体字段 | `entity name`、`entity type`、`entity subtype`、`entity keyword` |
| `T.GAME.RESOURCE` | 角色资源及其消耗/回复 | `_t`、`stat name`、`stat short_name` |
| `T.GAME.STAT` | 命中、闪避、护甲、强度等战斗属性 | `_t`、`stat name`、`stat short_name` |
| `T.GAME.MISC` | 未归入专门类别的游戏杂项名词 | `_t` |
| `T.UI.LABEL` | 菜单、按钮、界面标签 | `_t`、`save name` |
| `T.NARRATIVE.LORE` | 世界观、传说、日历文本 | `newLore category`、`calendar *`、`init.lua load_tips` |
| `T.NARRATIVE.ACHIEVEMENT` | 成就名称 | `achievement name` |
| `T.DIALOGUE.CHAT` | 对话选项和对话文本 | `chat*`、`say`、`saySimple` |
| `T.RUNTIME.LOG` | 战斗日志、系统提示 | `log`、`logSeen`、`logPlayer`、`logCombat` |
| `T.TECH.FORMAT` | 带占位符的格式模板 | `tformat` |
| `T.TECH.INTERNAL` | 仅供脚本或调试使用的内部字符串 | `nil`、`easing`、`dialog_portal` |

## 领域分类

`domain` 是比 `category` 更高的游戏功能域维度，用于按领域浏览、统计和维护术语表。同一领域可包含多个类别；`T.GAME.ENTITY` 按语义细分到物品、生物或地点领域。

| 领域 | 说明 | 主要类别 | 条目数 |
| --- | --- | --- | --- |
| `combat` | 战斗机制：伤害类型、状态效果、战斗属性 | `T.GAME.DAMAGE`、`T.GAME.EFFECT`、`T.GAME.STAT` | 161 |
| `talents` | 技能与技能树 | `T.GAME.TALENT`、`T.GAME.TALENT_CATEGORY` | 216 |
| `classes` | 职业与成长 | `T.GAME.CLASS` | 45 |
| `resources` | 角色资源 | `T.GAME.RESOURCE` | 12 |
| `items` | 装备、物品与材料 | `T.GAME.ENTITY`（物品/材料子集） | 57 |
| `creatures` | 生物与种族 | `T.GAME.ENTITY`（生物子集）、`T.PN.RACE` | 72 |
| `places` | 地点、地形与世界 | `T.PN.PLACE`、`T.PN.WORLD`、`T.GAME.ENTITY`（地形/场所子集） | 46 |
| `society` | 势力、组织与人物 | `T.PN.PERSON`、`T.PN.FACTION` | 33 |
| `narrative` | 叙事、传说与成就 | `T.NARRATIVE.LORE`、`T.NARRATIVE.ACHIEVEMENT` | 52 |
| `ui` | 界面与交互 | `T.UI.LABEL` | 12 |
| `tech` | 技术格式与内部字符串 | `T.TECH.FORMAT`、`T.GAME.MISC` | 2 |

术语表按 `domain → category → 原行序` 排序；新增条目时请先确认领域归属，再选择类别。

## 使用规则

1. 原始 `source_tag` 和 `category` 必须同时保留。相同英文词只有在 `source_tag`、section 或语义相同的情况下才可以复用译文。
2. `T.PN.*` 优先沿用现有专名译法；新专名先标为 `review`，不要在多个文件中各自创造译名。
3. `T.GAME.DAMAGE`、`T.GAME.EFFECT`、`T.GAME.RESOURCE`、`T.GAME.STAT` 是核心机制词，优先统一；同一词在不同类别中的译法可以不同。例如 `light` 在伤害语境中是“光系”，在装备重量语境中是“轻甲”。
4. 职业名称、技能树名称和具体技能名称分开记录，不因英文词形相同而合并。
5. `T.TECH.FORMAT` 的 `%s`、`%d`、`%0.1f`、颜色标记和换行必须原样保留；术语库只约束其中的自然语言部分。
6. 日志和调试文本不自动提升为公共术语。只有在玩家可见且反复出现时，才将其加入 `T.RUNTIME.LOG` 或 `T.UI.LABEL`。
7. 术语状态建议按 `existing → review → preferred` 推进；未经审校的现有译文不应直接视为最终规范。

## 初始维护流程

- 从提取结果按 `source_tag`、section 和出现频次生成候选词。
- 先整理种族、地点、阵营、职业、资源、伤害和效果等高复用词。
- 对同一英文词的多个中文译法建立多行记录，并在 `notes` 中注明语境；审校后只保留一个 `preferred` 译法或明确允许的别名。
- 确实新增或修改高复用术语时，在既有授权范围内先更新术语库，再修改对应译文；普通译文修订不要求更新术语库。主代理可主动登记具体疑点并核验，不能用术语库覆盖源码事实。验证按[工作流矩阵](docs/agent-workflow.md#验证矩阵)执行。

## 维护门禁

术语表改动后须覆盖以下审计（脚本在 `tools/`，报告写入 `.artifacts/i18n/terminology-audit/`）；完整门禁已包含时不另行重复执行。本说明文档的修订按纯文档任务验证：

| 命令 | 检查项 | 预期 |
| --- | --- | --- |
| `python3 -B tools/audit_static.py` | 错别字、标点/格式、同源同类别多译、类别边界、字段完整性 | 错字/标点 0；同源冲突仅限 review 迁移记录 |
| `python3 -B tools/audit_dynamic.py` | preferred 术语在译文中的使用率、多译、高频未录候选 | 术语与译文脱节数应持续下降 |
| `python3 -B tools/annotate_domains.py` | 领域标注一致性 | 全部行映射到 11 领域 |
| `python3 -B tools/classify_runtime_keys.py` | 重复运行键分类 | 全部同 target（跨文件合法重复） |

另见 [`docs/agent-workflow.md`](docs/agent-workflow.md) 的批次门禁与 `docs/runtime-key-collisions.md` 跨组件同键档案；根级触发条件以 [`AGENTS.md`](AGENTS.md) 为准。

## 本轮提取范围

本轮从仓库内 11 个 Lua 翻译文件按 `source_tag` 聚合候选词，优先纳入出现频次较高或对游戏结构有明确意义的职业、种族、技能树、属性、状态、伤害类型、实体类别和世界观地点。通用地形内部键（例如 `floor`、`wall`）及长句没有直接提升为术语；同一英文词在不同标签下仍分别记录。

出现多个译法的条目保留为 `review`，例如 `Constrict` 和 `eldritch`，待审校决定规范译名后再提升为 `preferred`（第二轮术语审核已把二者及 `Atmos Tribe` 定为 `preferred` 并在 `notes` 中注明统一语境；当前 `review=0`，术语状态以 `terminology/` 与 `tools/audit_dynamic.py` 输出为准）。

## DLC 首轮种子范围

首轮 DLC 候选通过按组件分别执行 `tools/i18n extract --component ashes-urhrok`、`tools/i18n extract --component cults`、`tools/i18n extract --component orcs` 生成，再与对应的规范译文按 `source_tag` 对齐。`terminology/` 中新增的 `scope=dlc` 条目优先覆盖以下高复用类别：阵营与地点、战役手札、资源与界面属性、DLC 技能树、伤害/效果类型以及实体类型。当前译文被保留为 `existing`；存在跨文本译名差异的 `Atmos Tribe` 标为 `review`，待后续统一“部族/部落”语境（第二轮术语审核已统一为“气之部族”并提升为 `preferred`）。

长对话、一次性物品名和普通叙述句暂不提升为术语。后续扩展 DLC 术语时，仍应先通过受审计提取器更新候选，再按组件和上下文补录；机制核验可以只读使用三个 GPL v3 官方 DLC 的固定公开源码。
