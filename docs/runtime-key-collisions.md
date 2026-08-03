# ToME4 运行时键（同 TAG 多译）冲突档案

> 本档案记录**所有**同 `(source, source_tag)` 多译检测问题。ToME4 当前翻译机制下，同键多译会导致译文覆盖，因此必须逐条追踪处置状态，不能仅依赖临时报告。
>
> 维护命令：`python3 -B tools/scan_runtime_collisions.py`（输出 JSON/MD 到 `.artifacts/i18n/`）；本档案按扫描结果人工维护。

## 一、运行时机制背景

- ToME4 翻译运行时键 = `(component, source, source_tag)`；游戏引擎加载多个 locale 文件时，**同键多条目由后加载者覆盖先加载者**。
- 同一组件内同键不同 target：`tools/i18n lint` 已作为 `runtime-collision`（error 级）检测，`policy.allowed_runtime_collisions` 可豁免。
- **跨组件**同键不同 target：lint 不检测（逐文件独立判定），但引擎加载时同样发生覆盖——本档案针对此缺口。
- 同键多条目但 target 相同（重复声明）：仅计数（`duplicate_runtime_keys`），无覆盖风险。

## 二、检测语义

扫描 `manifest.components` 全部译文，聚合键 `(source, source_tag)`：

- 键在 **≥2 个组件**中出现，且
- target 集合 **> 1**

即判定为跨组件运行时覆盖风险项。

## 三、当前问题清单（26 条，扫描于 2026-08-03）

### 3.1 格式变体（同义异形，应统一；部分已在修复批次中处理）

| # | source | tag | 变体 | 状态 |
|---|---|---|---|---|
| 1 | `#LIGHT_BLUE# * +0 Strength, +0 Dexterity, +0 Constitution` | `_t` | cults「+0 力量 , +0 敏捷 , +0 体质」/ tome「+0 力量，+0 敏捷，+0 体质」 | 待统一（tome 全角无空格为规范） |
| 2 | `#LIGHT_BLUE# * +0 Strength, +3 Dexterity, +0 Constitution` | `_t` | orcs 半角逗号 / tome 全角 | 待统一 |
| 3 | `#LIGHT_BLUE# * +0 Strength, +0 Dexterity, +3 Constitution` | `_t` | orcs 半角逗号 / tome 全角 | 待统一 |
| 4 | `#LIGHT_BLUE# * +0 Strength, +4 Dexterity, +0 Constitution` | `_t` | orcs 半角逗号 / tome 全角 | 待统一 |
| 5 | `#LIGHT_BLUE# * +5 Strength, +0 Dexterity, +1 Constitution` | `_t` | orcs 半角逗号 / tome 全角 | 待统一 |
| 6 | `#{bold}##GOLD#%s#GREEN# High Scores#WHITE##{normal}#\n\n` | `tformat` | boot「高分榜 」/ engine「高分榜」 | 待统一（去尾空格） |
| 7 | `#{bold}##GOLD#%s(%s)#GREEN# High Scores#WHITE##{normal}#\n\n` | `tformat` | boot「高分榜 」/ engine「高分榜」 | 待统一 |
| 8 | `You can get new addons on #LIGHT_BLUE##{underline}#Steam Workshop#{normal}#` | `_t` | boot 冒号+尾空格 / engine 无 | 待统一（engine 为规范） |
| 9 | `[Allow training of talent category %s (at mastery %0.2f)]` | `tformat` | orcs「解锁技能树…（掌握度）」/ tome「允许训练技能树…（熟练度）」 | 待裁决 |
| 10 | `#LIGHT_RED##Target# is out of sight of its master; direct control will break!` | `_t` | cults/tome「中断了」/ orcs「将中断」 | 待统一（了） |

### 3.2 长文本跨组件重复（真实覆盖风险：加载顺序决定生效译文）

| # | source | 涉及组件 | 状态 |
|---|---|---|---|
| 11 | `Lean, mean, and shaggy, it stares at you with hungry eyes.`（狼） | boot / engine / tome | 待统一（tome/engine 一致，boot 差异） |
| 12 | `A large and athletic troll with an extremely tough and warty hide.` | boot / engine / tome | 待统一（boot 差异） |
| 13 | `A beautiful woman, clad in shining plate armour. Power radiates from her.` | orcs / tome | 待统一 |
| 14 | `A small faceless humanoid with vaguely Dwarven features...` | cults / tome | 待统一 |
| 15 | `The massive ribcage in the middle beats with loud, audible cracks...` | cults / tome | 待统一 |
| 16 | `A very strong near-sentient tree, which has become hostile...` | orcs / tome | 待统一 |
| 17 | `Welcome to #LIGHT_GREEN#Tales of Maj'Eyal#LAST#!...`（在线功能长文） | boot / engine | 待统一（boot 版含「游戏内聊天」等完整段落；engine 版为旧精简版） |
| 18 | `#{bold}##GOLD#Embers of Rage - Expansion#LAST##{normal}#...` | boot / engine | 待统一（「兽人成为/被称为」等小差异） |
| 19 | `You are about to disable all connectivity to the network....` | boot / engine | 待统一（engine 版为旧精简，boot 版为新完整版） |
| 20 | `Infects the target with a very contagious disease...`（Epidemic） | cults / tome | 待统一 |
| 21 | `Grab a target and pull it next to you, covering it with frost...` | ashes-urhrok / tome | 待统一 |
| 22 | `Hits the target with your weapon...Accuracy is reduced...` | orcs / tome | 待统一 |

### 3.3 有意保留（语境区分 / 历史迁移）

| # | source | 说明 |
|---|---|---|
| 23 | `High Sun Paladin Aeryn`（`_t`、`entity name`） | possessors/orcs 用旧译「太阳骑士艾琳」，tome 用新译「高阶太阳骑士艾琳」——**注意：属待迁移**，需在后续批次将 possessors/orcs 同步为新译（batch 19 只覆盖了 tome） |
| 24 | `light`（`entity subtype`） | 语境区分：tome 光球场景「光」+ 皮甲场景「轻甲」；orcs 仅「轻甲」。术语表已记录两行（preferred 光 + existing 轻甲），属设计内区分 |
| 25 | `A very strong near-sentient tree...`（见 3.2 #16） | — |
| 26 | `High Sun Paladin Aeryn` 两行合并计数 | — |

## 四、已修复记录（同 tag 多译 → 已统一）

以下问题在历次批次中已修复并验证（同 tag 多译清零或仅剩本档案 3.1/3.2/3.3 所列）：

| 批次 commit | 内容 |
|---|---|
| `df62a15`（2026-08-03） | 33 条同组件同 tag 多译统一：ladder 台阶/梯子(40 处)、Stat modifiers 空格(6)、属性行半角/空格(4)、Blond Beard 空格(6)、her 她/她的、Active 启动/激活、exit to the worldmap 出口、raging volcano 喷发中的火山、snowy tree 积雪的树、错译修正（She looks tired/时空虫洞/太阳之墙）等 |
| `e1c4528`（2026-08-03） | steamtech 领域修正；Air 资源补录 |
| 历次批次（b7–b22、note1–2、补修 `5d26960`） | farportal 空格、#GOLD#Stat modifiers 无空格形式、致盲！全角、吸血鬼领主、骇异 subtype 等 |

## 五、维护规则

1. 每次译文批量修改后运行 `python3 -B tools/scan_runtime_collisions.py`，将新增/消失项同步到本档案。
2. 新发现的同键多译先补入本档案（状态=待统一/待裁决），再按批次修复；修复 commit 后更新状态并记录 commit 号。
3. 有意保留项必须注明理由（语境区分须有术语表多行记录；历史迁移须有目标批次）。
4. 本档案与 `terminology.tsv` 的 `status=review` 条目、lint 的 `runtime-collision`/`editorial-collision` 形成三层防线：组件内 error（lint）、跨组件档案（本文件）、术语表裁决（TSV）。
