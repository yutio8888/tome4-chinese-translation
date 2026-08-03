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

## 三、当前问题清单（1 条，扫描于 2026-08-03 修复批次后）

| # | source | tag | 组件变体 | 状态 |
|---|---|---|---|---|
| 1 | `light` | `entity subtype` | tome：「光」（光球/发光体场景，2 处）+「轻甲」（皮甲场景）；orcs：「轻甲」（仅此场景） | **有意保留**（语境区分，术语表已双行记录：preferred「光」+ existing「轻甲」；同一组件内 tome 自身即为双译且均已标注语境） |

## 四、已修复记录

### 4.1 2026-08-03 修复批次（`<待填 commit>`）

将档案初版 26 条减至 1 条：

- **3.1 格式变体 10 条**：属性行 `+0 Strength` 系列半角逗号/空格（cults 1、orcs 4）、高分榜 tformat 尾空格（boot 2，统一为 `#GREEN# 高分榜#WHITE#` 形态）、Steam Workshop 冒号+尾空格（boot 1）、`[Allow training of talent category]`（orcs 统一为「允许训练技能树 %s（熟练度 %0.2f）」）、`#LIGHT_RED##Target# is out of sight`（orcs「将中断」→「中断了」）。
- **3.2 长文本 12 条**：狼描述（boot→engine/tome 版）、巨魔描述（boot→engine/tome 版）、板甲美女（orcs→tome 版）、无面人形（cults→tome 版）、巨大胸腔（cults→tome 版）、半智慧树（orcs→tome 版）、Epidemic 技能（cults→tome 版）、Grab a target（ashes→tome 版）、weapon Accuracy（orcs→tome 版）、混乱日志（tome→orcs 版，更通顺）、Welcome 在线功能长文（engine→boot 完整版）、网络禁用说明（engine→boot 完整版）。
- **3.2 错字**：Embers of Rage 扩展介绍（engine「兽人成为」→「兽人被称为」）。
- **3.3 待迁移**：`High Sun Paladin Aeryn` 迁移完成（possessors 1 处 + orcs entity name 1 处 + orcs 成就文本 1 处 →「高阶太阳骑士艾琳」，与 tome 一致）。

### 4.2 早期批次

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
