### 批次校验信息

- **批次编号**：batch-044
- **文件路径**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-044.md`
- **文件 SHA-256 核验**：
  - 预期值：`f050852c68631a4e9ee03084d91d5586478207675f90fa865a9d1ddb7a679824`
  - 实际值：`f050852c68631a4e9ee03084d91d5586478207675f90fa865a9d1ddb7a679824`
  - 核验结论：一致通过。
- **源码与对照依据**：
  - 来源类型：公开核心仓库 `t-engine4`（`mod-tome`）
  - 固定 commit：`624a67329fe2ad440c5b344785a9c73fcf22ae63`
  - 源码路径：`game/modules/tome/data/lore/misc.lua`（第 387 行至第 454 行）
  - 译文终点基准：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00:mod-tome.lua`（第 18000 行至第 18082 行）

---

### 逐条复核报告

#### entry-01292
- **位置**：`mod-tome.lua:18000`（`mod-tome/data/lore/misc.lua`）
- **类型**：半身人种族历史背景文献（Lore: `races-2`）
- **复核结论**：细微观察
- **核验依据**：
  1. **换行差异**：固定源码 `game/modules/tome/data/lore/misc.lua:400` 中，该多行字符串末尾在闭合标记前带有一个换行符（`...Tolak the Fair.\n]]`），而译文字符串末尾直接闭合（`...公正之王托拉克。]]`），缺少末尾换行。虽然游戏文本显示端通常容忍末尾换行差异，但字面比对存在细微不一致。
  2. **称谓与上下文协同**：原文尾句仅提及 `King Toknor`，译文译为「勇者图库纳国王」，与第一章（`King Toknor the Brave`）建立的人类国王称号一致；`King Tolak the Fair` 译为「公正之王托拉克」，亦与全书目录及历史设定一致。
  3. **词义细微观察**：末段 "enlisted the aid of sorcerers" 译为「雇佣了一些术士」，"enlist" 此处偏向于“寻求支持/征募”，译为“雇佣”略偏商业化，但整体表意通畅不影响情节理解。
  4. **术语与专名**：烈火纪（Age of Pyre）、最后的希望（Last Hope）、夏·图尔（Sher'Tul）、德斯镇（Derth）、马基·埃亚尔（Maj'Eyal）、卓越纪（Age of Ascendancy）、艾德瑞尔（Eldoral）、纳格尔（Nargol）均符合术语表与语境规范；占位符无缺失。

---

#### entry-01293
- **位置**：`mod-tome.lua:18018`（`mod-tome/data/lore/misc.lua`）
- **类型**：章节标题（Chapter 3 - Dwarves）
- **原文**：`Loremaster Greynot's Analysis of the Races - Chapter 3 - Dwarves`
- **译文**：`博学者格雷诺特关于种族的调查——第三章——矮人`
- **复核结论**：未发现问题
- **核验依据**：
  - 章节序号、破折号连接符（`——`）与前后各章完全统一。
  - 种族名 `Dwarves` 准确对应术语 `矮人`（`T.PN.RACE`）。
  - 无占位符或颜色码需求。

---

#### entry-01294
- **位置**：`mod-tome.lua:18019`（`mod-tome/data/lore/misc.lua`）
- **类型**：矮人种族历史背景文献（Lore: `races-3`）
- **复核结论**：细微观察
- **核验依据**：
  1. **词义偏向观察**：第二段原文 "known to be very resistant to any physical suffering" 译为「以超强的物理抵抗能力而闻名于世」；"suffering" 偏向于肉体痛苦/折磨受难，此处译法偏向游戏机制层面的“物理抗性/物理伤害减免”（虽然段末 "sign of suffering" 正确译为了「极度痛苦」）。
  2. **意象弱化观察**：第五段原文 "venture beyond their halls of stone" 译为「从他们的石头洞穴里出去冒险」，将矮人代表性的石厅/岩石殿堂（halls of stone）弱化为了「石头洞穴」。
  3. **核心术语与材料**：钢铁王座（Iron Throne）、斯莱特（stralite）、沃瑞钽（voratun，对应术语库最高阶金属）、世界之砧（anvil of the world）、市场调查策略（market research strategy）等专名与材料名完全符合术语库规范。
  4. **格式与标点**：引号转换（`“”`）正确，段落完整，无漏句或格式错乱。

---

#### entry-01295
- **位置**：`mod-tome.lua:18036`（`mod-tome/data/lore/misc.lua`）
- **类型**：章节标题（Chapter 4 - Shaloren）
- **原文**：`Loremaster Greynot's Analysis of the Races - Chapter 4 - Shaloren`
- **译文**：`博学者格雷诺特关于种族的调查——第四章——永恒精灵`
- **复核结论**：未发现问题
- **核验依据**：
  - 章节序号与破折号规范与本系列文献一致。
  - 种族名 `Shaloren` 准确对应既定术语 `永恒精灵`（`T.PN.RACE`）。
  - 无占位符或格式问题。

---

#### entry-01296
- **位置**：`mod-tome.lua:18037`（`mod-tome/data/lore/misc.lua`）
- **类型**：永恒精灵种族历史背景文献（Lore: `races-4`）
- **复核结论**：细微观察
- **核验依据**：
  1. **别称处理不一致**：第二段原文 `Shaloren (or Shalore - lit "siblings of grace")` 译为 `永恒精灵（Shalore，字面意为“优雅的兄弟姐妹”）`。其中连词 "or"（「或」）漏译，且括号内直接保留了英文拉丁拼写 `Shalore` 而未作中文名处理；对比后文 entry-01298 与 entry-01300，均将括号内的单数别称处理成了中文。
  2. **术语选词观察**：第四段 "mastery of the arcane arts" 译为「在魔法上的造诣」，未直接采用术语库标准对应的「奥术」（arcane），但在此处叙事语境下意思通顺，不影响核心理解。
  3. **标点风格差异**：本条目使用的双弯引号 `“”`（如 `“Elore”`、`“优雅的兄弟姐妹”`）与后续 entry-01298、entry-01300 的直角引号 `「」` 风格不一致。
  4. **关键历史与专名**：魔法大爆炸（Spellblaze）、魔法狩猎（Spellhunt）、黄昏纪（Age of Dusk）、埃尔瓦拉（Elvala）、长老会（Council of Elders）等关键历史事件与地名均准确严谨。

---

#### entry-01297
- **位置**：`mod-tome.lua:18054`（`mod-tome/data/lore/misc.lua`）
- **类型**：章节标题（Chapter 5 - Thaloren）
- **原文**：`Loremaster Greynot's Analysis of the Races - Chapter 5 - Thaloren`
- **译文**：`博学者格雷诺特关于种族的调查——第五章——自然精灵`
- **复核结论**：未发现问题
- **核验依据**：
  - 章节序号与破折号规范与前后各章一致。
  - 种族名 `Thaloren` 准确对应既定术语 `自然精灵`（`T.PN.RACE`）。
  - 无格式或占位符异常。

---

#### entry-01298
- **位置**：`mod-tome.lua:18055`（`mod-tome/data/lore/misc.lua`）
- **类型**：自然精灵种族历史背景文献（Lore: `races-5`）
- **复核结论**：存在疑点
- **核验依据**：
  1. **种族专名疑点**：首段原文 `The Thaloren (or Thalore - lit "siblings of wrath")` 译为 `自然精灵（或木精灵——字面意为「愤怒的同胞」）`。
     - 依据源码固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63:game/modules/tome/data/birth/races/elf.lua:139-141` 及术语库 `terminology`（第 228 行），`Thalore` / `Thaloren` 在 ToME4 官方源码与既定术语规范中始终统一为「自然精灵」。
     - 英文原文中 `Thalore` 是单数/词根形式，`Thaloren` 是复数/形容词形式（与前章 `Shalore` / `Shaloren`、后章 `Nalore` / `Naloren` 结构对称）。
     - 译文在此处将 `Thalore` 自行意译为「木精灵」（Wood Elf），不仅在全库中仅此一处出现，而且脱离了游戏本身设定的种族正式称谓，可能给读者造成存在“自然精灵”与“木精灵”两种分支的误解。
  2. **其余内容与专名**：夏特尔（Shatur）、精灵木（elven-wood）、弓箭手（Archers）、法杖（staff）均核验准确；段落完整，文意通顺。

---

#### entry-01299
- **位置**：`mod-tome.lua:18068`（`mod-tome/data/lore/misc.lua`）
- **类型**：章节标题（Chapter 6 - Naloren (extinct)）
- **原文**：`Loremaster Greynot's Analysis of the Races - Chapter 6 - Naloren (extinct)`
- **译文**：`博学者格雷诺特关于种族的调查——第六章——纳鲁精灵（灭绝）`
- **复核结论**：未发现问题
- **核验依据**：
  - 括号内 `(extinct)` 译为 `（灭绝）`，与后续第八章 `兽人（灭绝）` 及第九章 `夏·图尔人（灭绝）` 的标题译法保持一致。
  - 种族名 `Naloren` 译为 `纳鲁精灵` 准确且通篇一致。

---

#### entry-01300
- **位置**：`mod-tome.lua:18069`（`mod-tome/data/lore/misc.lua`）
- **类型**：纳鲁精灵种族历史背景文献（Lore: `races-6`）
- **复核结论**：未发现问题
- **核验依据**：
  - 首段将 `The Naloren (or Nalore - lit "siblings of spirit")` 完整译为 `纳鲁精灵（或纳精灵——字面意为「精魂同胞」）`，结构与释义皆准确。
  - 大灾变（Cataclysm）、马基·埃亚尔（Maj'Eyal）、夏·图尔（Sher'Tul）、奥术之力（arcane abilities）、永恒精灵（Shaloren）、兽人（orcs）等关键历史事件与种族名词均符合术语表。
  - 四个自然段结构严整，无漏译、错译，标点与排版规范。

---

#### entry-01301
- **位置**：`mod-tome.lua:18082`（`mod-tome/data/lore/misc.lua`）
- **类型**：章节标题（Chapter 7 - Ogres）
- **原文**：`Loremaster Greynot's Analysis of the Races - Chapter 7 - Ogres`
- **译文**：`博学者格雷诺特关于种族的调查——第七章——食人魔`
- **复核结论**：未发现问题
- **核验依据**：
  - 章节序号、破折号规范与系列章节完全一致。
  - 种族名 `Ogres` 准确对应术语 `食人魔`（`T.PN.RACE`）。
  - 无占位符或格式问题。

---

### 复核总结汇总表

| 条目编号 | 源码位置 / Section | 结论 | 核心依据简述 |
| :--- | :--- | :--- | :--- |
| **entry-01292** | `mod-tome.lua:18000` (`mod-tome/data/lore/misc.lua`) | 细微观察 | 译文末尾较源码少一个换行符 `\n`；"enlisted" 译为「雇佣」略偏商业化；人名称谓前后协同良好。 |
| **entry-01293** | `mod-tome.lua:18018` (`mod-tome/data/lore/misc.lua`) | 未发现问题 | 标题格式、符号、章数及种族名「矮人」完全准确且与全书统一。 |
| **entry-01294** | `mod-tome.lua:18019` (`mod-tome/data/lore/misc.lua`) | 细微观察 | "physical suffering" 译为「物理抵抗能力」略带机制偏向；"halls of stone" 弱化为「石头洞穴」；关键金属与地名术语均准确。 |
| **entry-01295** | `mod-tome.lua:18036` (`mod-tome/data/lore/misc.lua`) | 未发现问题 | 标题格式规范，种族名「永恒精灵」符合术语标准。 |
| **entry-01296** | `mod-tome.lua:18037` (`mod-tome/data/lore/misc.lua`) | 细微观察 | `(or Shalore)` 漏译 "or" 且直接保留英文拉丁字母；"arcane arts" 译为「魔法」；引号风格为弯引号与后文直角引号不一致。 |
| **entry-01297** | `mod-tome.lua:18054` (`mod-tome/data/lore/misc.lua`) | 未发现问题 | 标题格式规范，种族名「自然精灵」符合术语标准。 |
| **entry-01298** | `mod-tome.lua:18055` (`mod-tome/data/lore/misc.lua`) | 存在疑点 | 将单数别称 `Thalore` 意译为「木精灵」，脱离 ToME4 官方设定及既定术语规范（统称「自然精灵」），易造成子种族概念混淆。 |
| **entry-01299** | `mod-tome.lua:18068` (`mod-tome/data/lore/misc.lua`) | 未发现问题 | 标题与 `（灭绝）` 标签与第八、九章完全一致，种族名准确。 |
| **entry-01300** | `mod-tome.lua:18069` (`mod-tome/data/lore/misc.lua`) | 未发现问题 | 四段翻译完整流畅，双称谓结构与精魂同胞释义准确，术语无偏差。 |
| **entry-01301** | `mod-tome.lua:18082` (`mod-tome/data/lore/misc.lua`) | 未发现问题 | 标题格式规范，种族名「食人魔」符合术语标准。 |