### batch-032 译文复核报告

#### 批次文件哈希核验
- **核验文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-032.md`
- **预期 SHA-256**：`d15c953ea24bfdf833014367e12248be4442336c7e38c8ce3aec80df60be3717`
- **实测 SHA-256**：`d15c953ea24bfdf833014367e12248be4442336c7e38c8ce3aec80df60be3717`
- **核验结论**：哈希完全一致，文件冻结有效。

本批次共 5 条条目（`entry-01215` 至 `entry-01219`），全部属于 `mod-tome` 模块。公开源码依据固定提交 `624a67329fe2ad440c5b344785a9c73fcf22ae63`（通过 `git -C /workspace/t-engine4 show` 读取），当前仓库译文语境固定于提交 `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`。

---

### 逐条复核记录

#### entry-01215
- **位置**：`mod-tome.lua:14230`
- **Section**：`mod-tome/data/lore/angolwen.lua`（源码对应 `game/modules/tome/data/lore/angolwen.lua`，条目 ID `angolwen-tarelion-magic`）
- **核验结果**：**存在疑点 / 细微观察**
- **可核验依据**：
  1. **概念对比与术语混淆（存在疑点）**：
     - **原文第二段**：
       > "Alchemists will tell you that the world is made up of many base materials - lead, copper, iron, gold and so on. They are fixated on splitting things down into these components and investigating how they react with each other. However there is more to the world than this. Certainly they represent the physical make-up of things, but they do not show the forces and energy that bring everything into motion. The forces of fire, cold, lightning and life itself are all very real effects, and these we call the Elements of Eyal."
     - **当前译文**：
       > “炼金师会告诉你这世界是由许多基本材料构成——铅、铜、铁、金等等。他们专注于将物品分解成**基本元素**来分析**他们**是如何互相影响的。但这只是世界的一面，**基本元素**虽然表现了物质面上世界的构成，却不能解释推动万物运动的力量与能量。火之力、冰之力、闪电之力、乃至生命之力都是真实存在的，而这些力量我们称之为**埃亚尔元素**。”
     - **依据**：原文作者大法师泰尔兰（Tarelion）是在进行哲学对比——炼金术士着眼于物质组分（`base materials` / `these components`，如铅铜铁金），而法师认为真正驱动世界的是自然之力（`Elements of Eyal`，即埃亚尔元素）。译文将 `these components` 翻译为了“基本元素”，不仅与前面的“基本材料”重复脱节，更提前使用了“元素”一词，导致后句“而这些力量我们称之为埃亚尔元素”的论述逻辑发生混淆与撞车。此外，“分析他们是如何互相影响的”中指代无生命组分，代词误用为人字旁“他们”（宜为“它们”）。
  2. **末段修辞与意译偏差（细微观察）**：
     - **原文末段**：
       > "Magic is simply an extension of the forces of nature, and are we not natural creatures that use it? But remember that magic is still a powerful force that can be used for good or ill. Magic is indeed a tool of immense value - use it wisely."
     - **当前译文**：
       > “魔法只是自然之力的延伸，我们身为自然生物为何不能去尝试运用它？但你们要谨记魔法的存在仍是一柄双刃剑。作为工具它确实能产生极大的价值——明智的使用它。”
     - **依据**：原文 `magic is still a powerful force that can be used for good or ill` 直述“魔法依然是一股强大的力量，可用于善行亦可用于恶行”，译文意译为“仍是一柄双刃剑”，增加了原文没有的武器修辞并略去了“强大力量”的表述；文末“明智的使用它”副词修饰动词应作“地”。此外，“作为安格利文里的学生我假定你们都是不同意这种说法的。”句中缺少逗号停顿。
  3. **控制码与格式**：`#{bold}#`、`#{italic}#`、`#{normal}#` 闭合完整，人名 Tarelion 译为“泰尔兰”、地名 Angolwen 译为“安格利文”，与同 section 上下文统一。

---

#### entry-01216
- **位置**：`mod-tome.lua:14450`
- **Section**：`mod-tome/data/lore/daikara.lua`（源码对应 `game/modules/tome/data/lore/daikara.lua`，条目 ID `daikara-dragonsfire-trap`）
- **核验结果**：**存在疑点**
- **可核验依据**：
  1. **标点与双引号方向错误（存在疑点）**：
     - **原文第 1 段结尾**：`and I don't want to add "being charred to a crisp" to my list of troubles today.`
     - **当前译文第 1 段结尾**：`而我可不想让今天的麻烦清单再多出”被烧成焦炭”这一项。`
     - **依据**：译文中引文首字符误用了右双引号（U+201D，闭引号 `”`），导致开闭引号均为闭引号 `”被烧成焦炭”`。对比同模块、同模板条目 `entry-01217` 中的正确配对（`“被彻底冻住”`），此处属于明确的排版标点错误。
  2. **机制与叙事文本**：该 Lore 在被玩家阅读后若拥有设陷类技能树则解锁“龙火陷阱”（`T_DRAGONSFIRE_TRAP`）。译文中角色名（科纳克人战士瑞丽、希安、苏达罗斯特）、装置原理（炼金药瓶、压力板、龙火）翻译准确，控制码 `#{bold}#` 与 `#{italic}#` 配对完整。

---

#### entry-01217
- **位置**：`mod-tome.lua:14458`
- **Section**：`mod-tome/data/lore/daikara.lua`（源码对应 `game/modules/tome/data/lore/daikara.lua`，条目 ID `daikara-freezing-trap`）
- **核验结果**：**未发现问题**
- **可核验依据**：
  1. **机制与内容对应**：该 Lore 解锁“冰冻陷阱”（`T_FREEZING_TRAP`）。译文将 `being frozen solid` 译为 `“被彻底冻住”`，`a blast of ice` 译为 `爆发出寒冰`，准确契合游戏设陷机制。
  2. **格式与标点规范**：控制码 `#{bold}#...#{normal}#` 及 `#{italic}#...#{normal}#` 配对闭合完整；首尾双引号使用规范（开引号 `“` 与闭引号 `”` 正确闭合）；人物译名与专有名词（科纳克人战士瑞丽、苏达罗斯特、希安）与上下文保持一致。

---

#### entry-01218
- **位置**：`mod-tome.lua:14722`
- **Section**：`mod-tome/data/lore/elvala.lua`（源码对应 `game/modules/tome/data/lore/elvala.lua`，条目 ID `spellblaze-chronicles-2`）
- **核验结果**：**存在疑点**
- **可核验依据**：
  1. **对话引号方向系统性错误（存在疑点）**：
     - 译文多处对话的前引号误使用了右双引号（U+201D，闭引号 `”`）：
       - 第 160 行：`似乎对眼前的景色颇为享受，”还是说你不够男人？”`
       - 第 168 行：`她小声咕哝着，”快来吧，我有点无聊了。”`
       - 第 180 行：`撤去了周身的火焰。”别抢了我的乐子！”她大喊道`
       - 第 188 行：`我气喘吁吁地说道，”我已经记不清了，到底是谁杀的更多…”。`
  2. **标点重复与嵌套异常（存在疑点）**：
     - 第 150 行：`“你在做什么呢？”，我轻轻问道。`（问号与引号外逗号并存）
     - 第 154 行：`“我立刻就召集突击队迎敌。”，我不顾礼仪地从床上坐起。`（句号与引号外逗号并存）
     - 第 178 行：`“对你来说是不是有些太热了呢，艾伦尼恩先生？”。`（问号与引号外句号并存）
     - 第 188 行：`到底是谁杀的更多…”。`（省略号在引号内，引号外额外跟句号）
  3. **段落结构拆分与句末标点缺失（存在疑点）**：
     - **原文**：`As a ring of dark swords and spears and halberds gathered round us Linaniil turned to me with a wild smile. “Time to dance.”`（同一段末尾带有完整句号闭合的引语）
     - **译文**：将该句强行拆分为单独段落，且末尾完全缺失句号或感叹号：
       > `当一圈黑沉沉的刀剑、长矛和戟将我们团团围住时，莱娜尼尔转向我，露出狂野的笑容。`  
       > （换行空行）  
       > `“舞会开始了”`
  4. **机制与叙事背景（细微观察）**：
     - 文本生动展现了魔法剑士（Arcane Blade）主角艾伦尼恩·加威尔（Aranion Gawaeil）的技能组合（斩月剑双手巨剑、火焰/寒冰/闪电附魔、地脉震波、气流软垫、相位移动）与莱娜尼尔（Linaniil）的高阶奥术火系魔法，专有名词与背景完全契合。
     - 第 178 行莱娜尼尔调侃调情直呼其名 `“Too hot for ye, Aranion?”`，译文添译为“艾伦尼恩先生”，同辈议员兼亲密关系下称“先生”略显生硬，属于语气润色层面的细微观察。

---

#### entry-01219
- **位置**：`mod-tome.lua:14813`
- **Section**：`mod-tome/data/lore/elvala.lua`（源码对应 `game/modules/tome/data/lore/elvala.lua`，条目 ID `spellblaze-chronicles-3` 之 `name`）
- **核验结果**：**未发现问题**
- **可核验依据**：
  1. **原文**：`The Spellblaze Chronicles(3): The Farportal`
  2. **译文**：`魔法大爆炸纪事(3)：远行传送门`
  3. **依据**：
     - 系列标题格式 `魔法大爆炸纪事(N)：...` 与同文件中的第 (1) 篇至第 (8) 篇保持严格统一。
     - 术语库标准：`Spellblaze` 译为“魔法大爆炸”，`The Farportal` 译为“远行传送门”，完全符合全游戏关于夏·图尔远行传送门实体的标准规范。
     - 标点符号与冒号使用全角，括号及编号无误，未发现任何问题。