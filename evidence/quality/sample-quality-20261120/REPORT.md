# 抽样质量检查与分析报告（2026-11-20，v0.3.15）

## 1. 抽样设计与范围

- **评估对象**：`tome4-chinese-translation` 内容基线 `f6e64afc0`（对应已发布插件 `tome4-chn-mod v0.3.15`，发布提交 `772d6f5`，GitHub Release `v0.3.15`）。
- **抽样脚本与数据**：[`sample.py`](sample.py)（固定种子 `20261120`）、[`sample.json`](sample.json)。
- **总体与分层**：从 `29,554` 个 release-required 单元中排除 22 条已知死键（`29,532` 条活单元），按与 `2026-11-03` 及 `2026-11-19` 完全相同的 **组件 × 原文长度** 矩阵分层随机抽取 **120 条**（与 `2026-11-19` 仅随机重叠 2 条，为独立新抽样）：
  - 组件分布：`mod-tome.lua` 60、`tome-orcs.lua` 20、`tome-cults.lua` 15、`tome-ashes-urhrok.lua` 11、`engine.lua` 14；
  - 长度分布：短（`S`, ≤30 字符）42、中（`M`, 31–200 字符）54、长（`L`, 201–1500 字符）24（总计 14,663 英文字符）；
  - 来源切分：90 条属于 `v0.3.15` 插件实际下发条目（`in_addon_delta=true`），30 条为未覆盖、沿用官方中文基线的条目（`in_addon_delta=false`）。
- **结构自动校验**：120 条样本中 `printf` 占位符、`@var@` 变量、`#COLOR#` 标签与未译检测异常均为 **0**。
- **独立双盲评审**（均不读 `handoff.md`、历史抽样、账本或 git 历史，均已归档）：
  - 评审 A：`claude/claude-opus-5-5`，结果 [`opus.json`](opus.json)；
  - 评审 B：`codex/gpt-6.2-sol`，结果 [`codex.json`](codex.json)。
  - 所有任一方打分 ≤3 或列入 `problems` 的条目（并集 19 条，全部来自评审 B）均由宿主对照固定核心源码（`t-engine4 @ 624a67329fe2`）及公开 DLC 源码（`/workspace/tome4-dlcs/`，源码未固定）逐条核验裁决。

---

## 2. 总体评分与纵向对比

### 2.1 两路独立评审汇总（1–5 分）

| 评审 | 准确 `acc` | 流畅 `flu` | 语境 `ctx` | 最低分 5 | 最低分 4 | 最低分 3 | 最低分 ≤2 | ≤3 占比 | Major 错译（评审报告 / 宿主确认） | 发布判定 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| **Opus 5.5 (2026-11-20, v0.3.15)** | **4.94** | **4.88** | **4.97** | 100 | 20 | 0 | 0 | 0.0% | 0 / 0 | `yes` |
| **GPT-6.2-Sol (2026-11-20, v0.3.15)** | **4.64** | **4.49** | **4.81** | 50 | 51 | 16 | 3 | 15.8% | 3 / **1**（`#55`） | `yes_with_caveats` |
| *参考：Opus 5.5 (2026-11-19, v0.3.14)* | *4.93* | *4.88* | *4.96* | *100* | *19* | *1* | *0* | *0.8%* | *0 / 0* | *`yes`* |
| *参考：GPT-6.1-Sol (2026-11-19, v0.3.14)* | *4.86* | *4.57* | *4.90* | *66* | *45* | *9* | *0* | *7.5%* | *0 / 0* | *`yes_with_caveats`* |
| *参考：Opus 5.5 (2026-11-03, 基线)* | *4.88* | *4.79* | *4.86* | *93* | *20* | *7* | *0* | *5.8%* | *0 / 0* | *`yes`* |

- **置信区间（Wilson 95% CI, n=120）**：
  - 经宿主源码核验确认的 Major 机制错译：`1/120 = 0.8%`（95% CI：`0.1%–4.6%`，仅 `#55` `Conversion` 失衡值方向误述，已在后续批次 `0560`/`0561` 修复）；
  - 经宿主源码核验确认应修复的次要缺陷（Confirmed minor/fixable）：`7/120 = 5.8%`（95% CI：`2.9%–11.6%`）；
  - 总计采纳并落盘修复条目：`8/120 = 6.7%`（95% CI：`3.4%–12.6%`）；
  - 两路评审并集 ≤3 分比例（含风格润色与驳回项）：`19/120 = 15.8%`（95% CI：`10.4%–23.4%`）。
- **同模型纵向对比（Opus 5.5：`2026-11-03 → 2026-11-19 → 2026-11-20`）**：
  - 三维均分连续小幅抬升并站稳高位：`acc 4.88 → 4.93 → 4.94`，`flu 4.79 → 4.88 → 4.88`，`ctx 4.86 → 4.96 → 4.97`，≤3 分条目由 `7 → 1 → 0`；
  - 重点改进区间表现显著：**长文本 `L` 档 `flu` 由 `4.50` 升至 `4.79`（`+0.29`）**，**`engine.lua` `flu` 由 `4.71` 升至 `4.93`（`+0.22`）**，直接呼应了 `v0.3.15` 清理长技能 Lua 冗余注水与精修选项说明的改动方向。
- **跨模型尺度差异说明**：
  - 本次评审 B 从 `gpt-6.1-sol` 切换为 `gpt-6.2-sol`，其对英文原稿本身瑕疵（如 `#50`）、未展开 Lua 早退分支（如 `#52`）及文风顺滑度的扣分尺度明显更严（48/120 双审全 5 分，18/120 双审均 ≤4 分，0/120 双审均 ≤3 分），不可直接将 `gpt-6.2-sol` 绝对均分与 `2026-11-19` 的 `gpt-6.1-sol` 等同比较；但更严格的评审 B 确实帮助挖出了 1 条真实逆向资源误述（`#55`）及 7 条值得修复的准确度/流畅度缺陷。

---

## 3. 分维度拆解（组件 × 文本长度 × 覆盖来源）

### 3.1 按组件

| 组件（样本数） | Opus 5.5 `acc / flu / ctx` (≤3) | GPT-6.2-Sol `acc / flu / ctx` (≤3) | 特征 |
| --- | --- | --- | --- |
| `mod-tome.lua` (60) | `4.97 / 4.85 / 4.97` (0) | `4.63 / 4.50 / 4.88` (8) | 准确度整体稳健；检出 1 条失衡值方向错误（`#55`）与 2 条技能细微表述缺陷（`#52`、`#59`） |
| `tome-orcs.lua` (20) | `5.00 / 4.85 / 4.95` (0) | `4.90 / 4.40 / 4.90` (2) | 准确度最高（Opus 5.00 / Codex 4.90），仅 2 条偏文风润色（`#69`、`#80`） |
| `tome-cults.lua` (15) | `4.80 / 5.00 / 4.93` (0) | `4.47 / 4.33 / 4.60` (5) | 检出 3 条值得收紧的短中文本语义/书名号细节（`#88`、`#90`、`#91`） |
| `tome-ashes-urhrok.lua` (11) | `5.00 / 4.91 / 5.00` (0) | `4.55 / 4.64 / 4.73` (1) | 整体稳健；仅 1 条「全体伤害加成」宜明确为「所有伤害」（`#101`） |
| `engine.lua` (14) | `4.86 / 4.93 / 5.00` (0) | `4.57 / 4.64 / 4.64` (3) | Opus 流畅度较 v0.3.14 上升 `+0.22`；Codex 3 条中 1 条为共享运行提示误判（`#108`）、1 条属 boot 菜单（`#114`）、1 条商城说明可润色（`#118`） |

### 3.2 按原文长度

| 长度档位（样本数） | Opus 5.5 `acc / flu / ctx` (≤3) | GPT-6.2-Sol `acc / flu / ctx` (≤3) | 特征 |
| --- | --- | --- | --- |
| 短 `S` (≤30, n=42) | `4.98 / 4.90 / 4.95` (0) | `4.90 / 4.90 / 4.76` (2) | 极高一致性；2 条 Codex ≤3 均为语境偏好/共享键（`#83`、`#108`） |
| 中 `M` (31–200, n=54) | `4.91 / 4.91 / 4.96` (0) | `4.61 / 4.43 / 4.87` (10) | 含 4 条可修细节（`#88`、`#90`、`#91`、`#101`）与 5 条文风/boot 项 |
| 长 `L` (>200, n=24) | `4.96 / 4.79 / 5.00` (0) | `4.25 / 3.92 / 4.75` (7) | Opus 相比 v0.3.14 的 `4.50` 提升 `+0.29`；Codex 严苛审查集中于长技能条目（含 `#55`、`#52`、`#59`、`#118`） |

### 3.3 插件覆盖条目 vs 继承官方基线

| 来源（样本数） | Opus 5.5 `acc / flu / ctx` (≤3) | GPT-6.2-Sol `acc / flu / ctx` (≤3) |
| --- | --- | --- |
| 插件下发 `addon_delta` (90) | `4.94 / 4.87 / 4.97` (0) | `4.60 / 4.41 / 4.81` (15) |
| 沿用官方 `official_only` (30) | `4.93 / 4.93 / 4.97` (0) | `4.77 / 4.73 / 4.80` (4) |

说明：高复杂度技能与 DLC 文本几乎全部落在 `addon_delta` 中（90 条含绝大部分 `L` 档条目），而 `official_only` 多为短标签与简单句，因此 Codex 在 `addon_delta` 上的严格扣分相对更集中；Opus 在两类来源上均保持 `acc ≥ 4.93 / ctx = 4.97`。

---

## 4. 宿主源码核验与逐项裁决（全部 19 条 ≤3 分条目）

| # | `unit_id` / 文件 / 来源 | 原文 → 现译（摘录） | 评审意见 | 宿主源码核验与裁决 |
| ---: | --- | --- | --- | --- |
| **55** | `e5b60119fbd6`<br>`mod-tome.lua` (`delta=True`) | `...restores ... %d equilibrium... The heal and resource gain will improve...` → `……回复……%d 点失衡值……增益效果受精神强度加成。` | Codex `(2,3,3)` Major；Opus `(5,5,5)` | **confirmed (major, acc/ctx)**：查固定源码 `feedback.lua:139` 实际调用 `incEquilibrium(-val)`（降低失衡值，逆向资源），「回复失衡值」易误导为升高失衡值，「增益效果」也未指明治疗量与资源回复量。**已纳入批次 `0560`/`0561` 修复**。 |
| **52** | `46a1fdd523bd`<br>`mod-tome.lua` (`delta=True`) | `If any effect causes the target's turn to fail they fumble and injure themself, taking %0.2f physical damage.` → `如果因任何原因，敌人技能使用失败，对方将弄伤自己，造成 %0.2f 物理伤害。` | Codex `(2,4,4)` Major（要求展开 `Actor.lua` 失衡早退分支）；Opus `(5,4,5)`（指出「造成」宜作「受到」） | **confirmed (minor, acc/flu — 降级自 Major)**：按编辑原则**不展开** Lua 内部早退分支；但现译确实漏译 `turn to fail` 且误将 `taking` 译成「造成」，同时修齐尾部缩进 `\n\t\t`。**已纳入批次 `0560`/`0561` 修复**。 |
| **50** | `81874f15866a`<br>`mod-tome.lua` (`delta=True`) | `...when talents compare combat stats that are on different tiers...` → 忠实对应英文越层教程 | Codex `(2,5,5)` Major（自承「此误导沿袭自英文」）；Opus `(5,4,5)` | **rejected (非 Major 错译)**：译文忠实呈现英文教程原句，Codex 亦承认偏差来自英文原稿本身，不计为翻译 Major 错译。 |
| **59** | `5afa5478601c`<br>`mod-tome.lua` (`delta=True`) | `Minotaurs cannot stay summoned for long... increased damage%%, resistance penetration %%...` → `米诺陶不会呆很长时间……增加百分比伤害、抗性穿透……` | Codex `(3,3,5)`；Opus `(5,4,5)` | **confirmed (minor, acc/flu)**：两路均指出口语化（「不会呆很长时间」），且补回两处字面 `%%` 并明确「伤害加成%%」避免歧义。**已纳入批次 `0560`/`0561` 修复**。 |
| **88** | `d263176c718c`<br>`tome-cults.lua` (`delta=True`) | `Fast does not always win.\n\n#GOLD#Rumoured to be able to combine with the Shoes of Moving Quickly.` → `快不一定是好事。……` | Codex `(3,5,5)`；Opus `(4,5,5)` | **confirmed (minor, acc)**：两路均指出「快不一定是好事」弱化了 Slow Shoes 与疾行之靴的输赢对照，改为「快未必总能取胜。\n\n#GOLD#传闻它可以与疾行之靴合成。」。**已纳入批次 `0560` 修复**。 |
| **90** | `d4a8dc505eca`<br>`tome-cults.lua` (`delta=True`) | `#PURPLE#Make sure you are connected and joined the main Tales of Maj'Eyal chat channel.` → `……加入了马基·埃亚尔的传说的主聊天频道。` | Codex `(4,3,4)`；Opus `(5,5,4)` | **confirmed (minor, flu/ctx)**：全库 177 处均作「马基·埃亚尔」，加书名号《马基·埃亚尔的传说》消除连「的」边界不清，并对照 `fortress-multiverse.lua:40-42` 将 `connected` 明确为「连接至在线服务」。**已纳入批次 `0560`/`0561` 修复**。 |
| **91** | `6da8f2d574ee`<br>`tome-cults.lua` (`delta=True`) | `#DARK_SEA_GREEN#A not yet digested foe burst out from the sack!` → `……从消化袋里掉了出来！` | Codex `(3,4,5)`；Opus `(4,5,5)` | **confirmed (minor, acc)**：两路均指出 `burst out` 被弱化为「掉了出来」，改为「猛地冲了出来！」。**已纳入批次 `0560` 修复**。 |
| **101** | `b03dd63517fc`<br>`tome-ashes-urhrok.lua` (`delta=True`) | `Increases all damage by 1% for each point of your Shadow Power.` → `每点“阴影强度”增加1%全体伤害加成。` | Codex `(3,4,3)`；Opus `(5,5,5)` | **confirmed (minor, acc/ctx)**：源码写入 `inc_damage.all`（所有类型伤害），改为「每点“阴影强度”使所有伤害提高 1%。」避免与群体范围混淆。**已纳入批次 `0560`/`0561` 修复**。 |
| **118** | `ec8f9bca5cdd`<br>`engine.lua` (`delta=True`) | `For every donations you've ever made you have earned voratun coins...` → `你历次所做的每一笔捐赠……让这游戏更加持久！` | Codex `(4,3,5)`；Opus `(5,4,5)` | **confirmed (minor, flu)**：两路均指出开头累赘与结语偏弱，已润色收紧。**已纳入批次 `0560` 修复**。 |
| **108** | `f15adfdfe847`<br>`engine.lua` (`delta=False` 官方) | `Running...` → `跑步中……` | Codex `(3,5,3)` 建议改为「自动探索中……」；Opus `(5,5,5)` | **rejected (共享键误判)**：查源码 `Running...` 同时被 `PlayerExplore.lua:428` 与 `PlayerRun.lua:49,99`（普通奔跑）共享，改成「自动探索中……」会破坏普通奔跑场景，维持原译。 |
| **114** | `0a6aeafa110c`<br>`engine.lua` (`delta=False` 官方) | `#LIGHT_RED#Donator Status: Disabled` → `#LIGHT_RED#捐赠者状态：禁用` | Codex `(4,5,3)`；Opus `(5,5,5)` | **advisory (boot 菜单限制)**：该串位于 `engine/modules/boot/dialogs/Addons.lua`，属游戏启动菜单（addon 加载前生效，不被插件覆盖），记录备查，暂不改动。 |
| **34** | `0d12f2f02f11`<br>`mod-tome.lua` (`delta=False` 官方) | `shertul.lua` 壁画拼接片段 | Codex `(4,3,5)`；Opus `(5,5,5)` | **advisory (文风润色)**：语义忠实，官方既有译文，保持稳定。 |
| **35** | `ba95b0c01fd3`<br>`mod-tome.lua` (`delta=False` 官方) | `world-artifacts.lua` 触手触发日志 | Codex `(5,3,5)`；Opus `(5,5,5)` | **advisory (文风润色)**：语义无误，官方既有译文，保持稳定。 |
| **38** | `2754a5d7c678`<br>`mod-tome.lua` (`delta=True`) | `shertul.lua` 壁画描述 | Codex `(5,3,5)`；Opus `(5,5,5)` | **advisory (文风润色)**：语义准确，不改。 |
| **56** | `8ba4880576f8`<br>`mod-tome.lua` (`delta=True`) | `kinetic-mastery.lua` 动能精通 | Codex `(4,3,4)`；Opus `(5,5,5)` | **advisory (文风润色)**：Codex 已确认机制忠实，仅文风偏好。 |
| **69** | `a748bd0b808d`<br>`tome-orcs.lua` (`delta=True`) | `palace-fumes/npcs.lua` 战斗描写 | Codex `(5,3,5)`；Opus `(5,5,5)` | **advisory (文风润色)**：准确度满分，仅文风偏好。 |
| **80** | `cf4d177adf0e`<br>`tome-orcs.lua` (`delta=True`) | `slumbering-caves.lua` 长篇 lore | Codex `(4,3,5)`；Opus `(5,5,5)` | **advisory (文风润色)**：长篇 lore 语义准确，仅修辞偏好。 |
| **83** | `b593954886a0`<br>`tome-cults.lua` (`delta=True`) | `Digestive Sack` → `消化袋` | Codex `(5,4,3)` 建议「消化囊」；Opus `(5,5,5)` | **advisory (全库术语一致)**：全库多处与日志统一作「消化袋」，不单独改写以免割裂。 |
| **89** | `a5e2d615d4f7`<br>`tome-cults.lua` (`delta=True`) | `demented.lua` 职业背景句 | Codex `(5,3,5)`；Opus `(5,5,5)` | **advisory (文风润色)**：准确度满分，仅句式偏好。 |

---

## 5. 综合结论

1. **质量结论**：**`tome4-chn-mod v0.3.15` 整体质量保持在高位，且针对 `v0.3.14` 暴露的短板取得了可验证的改善**。同模型（Opus 5.5）独立新抽样三维均分达到 `4.94 / 4.88 / 4.97`（0 条 ≤3 分），其中长文本 `L` 档流畅度提升 `+0.29`（`4.50 → 4.79`）、`engine.lua` 流畅度提升 `+0.22`（`4.71 → 4.93`）。
2. **严苛复核的收获**：更严苛的评审 B（`gpt-6.2-sol`）检出 1 条经固定源码核实的逆向资源误述（`#55` `Conversion` 降低失衡值）及 7 条准确的语义/标点/流畅度小缺陷（`#52`、`#59`、`#88`、`#90`、`#91`、`#101`、`#118`）；上述 8 条已全部合入后续精修批次（`0560`/`0561`）并通过双路盲审与严格校验。
3. **方法论备忘**：跨期趋势对比应以同模型基线（Opus 5.5）为主，跨模型评审（GPT-6.2-Sol）用于扩大问题召回，所有疑似 Major 或共享键问题仍必须以源码核验作为最终裁决依据（本次成功拦截了 `#50`、`#108` 误改及 `#52` 过度展开 Lua 分支）。
