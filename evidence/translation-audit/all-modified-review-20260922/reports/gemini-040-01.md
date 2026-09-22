# 译文复核报告：batch-040（entry-01230 至 entry-01249）

## 复核元数据与前置校验
- **复核批次**：`batch-040`
- **条目范围**：`entry-01230` ～ `entry-01249`（共 20 条，已全部逐条覆盖）
- **批次文件哈希核对**：
  - 预期 SHA-256：`f03137dd39b5d4cf3e5ca08d9c1cbb74628f707f69f6effde4869c22cd3b868a`
  - 实测 SHA-256：`f03137dd39b5d4cf3e5ca08d9c1cbb74628f707f69f6effde4869c22cd3b868a`（完全一致）
- **源码与译文锚点**：
  - 译文仓库终点：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`
  - 公开源码基准：固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（`game/modules/tome/data/lore/` 对应文件）

---

## 逐条复核结论与核验依据

### entry-01230
- **位置**：`mod-tome.lua:16072`（`mod-tome/data/lore/high-peak.lua`）
- **复核结论**：细微观察
- **核验依据**：
  1. 源码核对：文本对应固定 commit 源码中 `elandar-1` 叙事（埃兰达日记 1）。专名术语如生命之血（Blood of Life）、夏·图尔（Sher'Tul）、安格利文（Angolwen）、泰恩（Tannen）、远行传送门（farportal）、盖里克（Gerlyk）均完全符合设定与术语库。
  2. 格式与控制标签：`#{italic}#humanity.#{normal}#` 译为 `#{italic}#人性#{normal}#。`、`#{italic}#exists#{normal}#` 译为 `#{italic}#存在#{normal}#`、`#{italic}#herself#{normal}#` 译为 `#{italic}#她自己#{normal}#` 均正确闭合且标点外置合理。
  3. 细微观察：原文 `she's almost #{italic}#too#{normal}# rational.` 中仅强调副词 `too`，译文处理为 `她几乎#{italic}#理智得过了头#{normal}#。`，将整个谓语修饰短语置于斜体标签内。属于中文语感下强调程度的合理润色，不影响游戏机制与主旨传达，供后续维护参考。

### entry-01231
- **位置**：`mod-tome.lua:16112`（`mod-tome/data/lore/high-peak.lua`）
- **复核结论**：未发现问题
- **核验依据**：
  1. 源码核对：对应 `elandar-2`。专名吸能法杖（Staff of Absorption）、盖里克（Gerlyk）、艾格尼尔（Argoniel）、魔法大爆炸（Spellblaze）、埃亚尔（Eyal）均翻译准确。
  2. 格式与控制标签：原文 `#{italic}#em#{normal}#power` 对应译文 `#{italic}#增#{normal}#力`，词缀局部强调与标签闭合极为精确；段落换行与标点完全匹配。

### entry-01232
- **位置**：`mod-tome.lua:16173`（`mod-tome/data/lore/infinite-dungeon.lua`）
- **复核结论**：未发现问题
- **核验依据**：
  1. 源码核对：对应 `infinite-dungeon-history-1`（猎人与猎物 第一章）。文本中出现的专名与复合词：布兰伊尔（Branzir）、远行传送门（Farportal）、凯尔帝勒（Caldizar）、猎神行动（Godhunt）、巨剑玛卓斯（great sword Madrath）、“弑神者”（"Godslayer"）、厄格莫斯（Ugg'matho）、普塔利亚斯（Pertolias）、亚多契（Xadoch）、安维恩（Anvion）、古龙伦湖（Glonglum lake）、欺诈者瑞尔克（Ralkur the Deceptor）均严格契合背景叙事，译文笔触庄严流畅，无漏译错译。

### entry-01233
- **位置**：`mod-tome.lua:16218`（`mod-tome/data/lore/iron-throne.lua`）
- **复核结论**：未发现问题
- **核验依据**：
  1. 源码核对：对应 `iron-throne-profits-1`（钢铁王座利润历史：厄流纪）。
  2. 格式与控制标签：编年条目 3800 至 7494 共 10 处 `#{bold}#年份: #{normal}#` 标签完整保留并规范对应中文全角冒号 `#{bold}#年份：#{normal}#`。
  3. 数值与专名：斯莱特（stralite）、大工匠达克顿（Grand Smith Dakhtun）、永恒精灵（Shaloren）、夏·图尔（Sher'Tul）、伊格兰斯教团（Ziguranth order，按规则教团指称使用“伊格兰斯”而非“伊格”）、赤红巨龙库洛塔（Kroltar the Crimson Wyrm）均准确无误；数值两千万（20 million）、七百万（7 million）、人均损失标准 350 金（350 gold per capita lost）、一千三百万（13 million）、利润率 186% 完全吻合。

### entry-01234
- **位置**：`mod-tome.lua:16258`（`mod-tome/data/lore/iron-throne.lua`）
- **复核结论**：未发现问题
- **核验依据**：
  1. 源码核对：对应 `iron-throne-profits-4`（钢铁王座利润历史：卓越纪）。
  2. 格式与术语：纪年 28、115、120 的加粗标签匹配完备。联合王国（Allied Kingdom）、钢铁王座（Iron Throne）、恐魔（horrors）、恶魔（demons）、沃瑞钽和斯莱特材料（voratun and stralite materials）术语统一，行文严密准确。

### entry-01235
- **位置**：`mod-tome.lua:16276`（`mod-tome/data/lore/iron-throne.lua`）
- **复核结论**：未发现问题
- **核验依据**：
  1. 源码核对：对应 `iron-throne-trade-ledger`（钢铁王座交易账簿）。
  2. 格式与控制标签：`#{bold}#`、`#{italic}#` 及 `#{normal}#` 完全配对闭合。
  3. 账目细节与专名：最后的希望（Last Hope）、德斯镇（Derth）、安格利文（Angolwen）、伊格兰斯（ziguranth，指教团袭扰部队）全数准确；板甲、长剑、长矛、钉头锤、手斧及宝石物料数量规格（500pcs、460pcs、170pcs、200pcs、150pcs、2,200pcs、50pcs、65pcs、500,000pcs、1,000tons、50pcs、40pcs、20pcs）及末尾署名批注（- D. / - S. -> ——D / ——S）准确对应。

### entry-01236
- **位置**：`mod-tome.lua:16332`（`mod-tome/data/lore/iron-throne.lua`）
- **复核结论**：未发现问题
- **核验依据**：
  1. 源码核对：对应 `deep-bellow-1` 的标题名称（`name = _t"Deep Bellow excavation report 1"`）。与全库 Deep Bellow 统一地名译名“深渊咆哮”保持完全一致，序号与文本无误。

### entry-01237
- **位置**：`mod-tome.lua:16346`（`mod-tome/data/lore/iron-throne.lua`）
- **复核结论**：未发现问题
- **核验依据**：
  1. 源码核对：对应 `deep-bellow-2` 的标题名称（`name = _t"Deep Bellow excavation report 2"`）。地名与序号翻译准确。

### entry-01238
- **位置**：`mod-tome.lua:16360`（`mod-tome/data/lore/iron-throne.lua`）
- **复核结论**：未发现问题
- **核验依据**：
  1. 源码核对：对应 `deep-bellow-3` 的标题名称（`name = _t"Deep Bellow excavation report 3"`）。地名与序号翻译准确。

### entry-01239
- **位置**：`mod-tome.lua:16406`（`mod-tome/data/lore/keepsake.lua`）
- **复核结论**：未发现问题
- **核验依据**：
  1. 源码核对：对应遗物任务线 Lore `keepsake-banders-notes`（班德的笔记）。
  2. 格式与标签：前导首行 `#{italic}#...#{normal}#` 标签闭合无误；6 项列表标记 `* ` 结构与换行完整保留。
  3. 人名与专名：班德（Bander）、泰里克（Terrik）、贾克（Jak）、贝里斯（Berethh）、阿尔瓦（Alva）、凯勒斯（Kyless，符合三方裁定取代旧译克里斯的最新基准）均一致，英文原注引号与状态描述词翻译准确。

### entry-01240
- **位置**：`mod-tome.lua:16434`（`mod-tome/data/lore/keepsake.lua`）
- **复核结论**：未发现问题
- **核验依据**：
  1. 源码核对：对应 `keepsake-acorn`（铁橡果拾取叙事）。
  2. 细节核验：人物关联（班德的父母、班德童年、贝里斯、凯勒斯及玩家角色“你”）对应准确；“cold iron bites into your skin”译为“冰冷的铁压得皮肤生疼”，修辞与语境高度契合。

### entry-01241
- **位置**：`mod-tome.lua:16460`（`mod-tome/data/lore/keepsake.lua`）
- **复核结论**：未发现问题
- **核验依据**：
  1. 源码核对：对应 `keepsake-dreams-end`（梦境终结/草原醒来）。
  2. 机制与剧情核对：此处文本为诅咒系职业任务叙事，“Your hate is burning inside you again”正确转译为叙事语境的“你心中的仇恨再次燃起”；凯勒斯藏匿所得（'profits'）的洞穴秘密小径叙事准确传达。

### entry-01242
- **位置**：`mod-tome.lua:16517`（`mod-tome/data/lore/keepsake.lua`）
- **复核结论**：未发现问题
- **核验依据**：
  1. 源码核对：对应 `keepsake-kyless-journal-1` 的标题名称（`name = _t"Kyless' Journal: First Entry"`）。
  2. 人名与标点：Kyless 统一为“凯勒斯”，英文冒号对应全角冒号，序号“第一篇”规范标准。

### entry-01243
- **位置**：`mod-tome.lua:16518`（`mod-tome/data/lore/keepsake.lua`）
- **复核结论**：未发现问题
- **核验依据**：
  1. 源码核对：对应 `keepsake-kyless-journal-1` 正文。首行斜体提示标签匹配完整。
  2. 叙事连贯性：商队雇佣另外两名搬运工（“a couple of other porters”译为“另外两名搬运工”，与任务线中凯勒斯、贝里斯与主角三人入队事实完全吻合），行文流畅准确。

### entry-01244
- **位置**：`mod-tome.lua:16537`（`mod-tome/data/lore/keepsake.lua`）
- **复核结论**：未发现问题
- **核验依据**：
  1. 源码核对：对应 `keepsake-kyless-journal-2` 的标题名称（`name = _t"Kyless' Journal: Second Entry"`）。译为“凯勒斯的日记：第二篇”，格式与专名无误。

### entry-01245
- **位置**：`mod-tome.lua:16538`（`mod-tome/data/lore/keepsake.lua`）
- **复核结论**：细微观察
- **核验依据**：
  1. 源码核对：对应 `keepsake-kyless-journal-2` 正文。首行斜体标签完备；巨魔（trolls）、心灵感应与低语（whispers）、操控（Control）等叙事翻译准确。
  2. 细微观察：原文第 3 行 `Berethh found something in the woods...a dead man and a few dead trolls.` 译为 `贝里斯在森林中发现了什么——一具男尸和几具巨魔尸体。`。此处“发现了什么——”略带不定代词直译痕迹（口语叙事感尚可，但若作“有了发现——”或“发现了一些东西——”更为书面地道），不造成实质歧义，予以记录。

### entry-01246
- **位置**：`mod-tome.lua:16561`（`mod-tome/data/lore/keepsake.lua`）
- **复核结论**：未发现问题
- **核验依据**：
  1. 源码核对：对应 `keepsake-kyless-journal-3` 的标题名称（`name = _t"Kyless' Journal: Third Entry"`）。译为“凯勒斯的日记：第三篇”，格式与专名无误。

### entry-01247
- **位置**：`mod-tome.lua:16562`（`mod-tome/data/lore/keepsake.lua`）
- **复核结论**：细微观察
- **核验依据**：
  1. 源码核对：对应 `keepsake-kyless-journal-3` 正文。首行斜体标签完备；人物贾克（Jak）专名一致；强盗反杀与洞穴藏金剧情准确。
  2. 细微观察：
     - 原文 `The fear on their faces when I struck was priceless.` 译为 `我攻击他们时，他们脸上惊恐的表情令我感到无比快意。`，此处 “priceless” 采取意译传达其变态心理，语意传神；
     - 原文 `I'll stay with the caravan.` 译作 `我还会和商队呆在一起。`，其中“呆”字为口语通假俗写（规范推荐写作“待在一起”），不影响理解，供文字润色参考。

### entry-01248
- **位置**：`mod-tome.lua:16581`（`mod-tome/data/lore/keepsake.lua`）
- **复核结论**：未发现问题
- **核验依据**：
  1. 源码核对：对应 `keepsake-kyless-journal-4` 的标题名称（`name = _t"Kyless' Journal: Fourth Entry"`）。译为“凯勒斯的日记：第四篇”，格式与专名无误。

### entry-01249
- **位置**：`mod-tome.lua:16582`（`mod-tome/data/lore/keepsake.lua`）
- **复核结论**：未发现问题
- **核验依据**：
  1. 源码核对：对应 `keepsake-kyless-journal-4` 正文。首行斜体标签完备；贝里斯（Berethh）背叛、封印洞穴入口、攻击导致结界增强（wards -> 结界）等描述与固定源码事实完全契合，段落换行与标点无误。

---

## 总结
本批次 20 条译文（全部属于 `mod-tome` 模块的历史与背景 Lore）在固定源码 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 下完成核验：
- 共有 **17 条未发现问题**；
- 共有 **3 条记录为细微观察**（`entry-01230` 斜体标签跨度微调、`entry-01245` 代词直译修辞倾向、`entry-01247` “呆/待”俗写用字与意译细节），均无破坏性缺陷或代码逻辑阻断。全部条目未发现占位符错乱、参数颠倒、未闭合控制码或关键机制性误译。