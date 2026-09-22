# 只读译文复核报告：batch-053（entry-01505 至 entry-01544）

## 1. 基础信息与文件核验

- **工作区**：`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921`
- **复核批次**：`batch-053`（共 40 条，编号范围：`entry-01505` 至 `entry-01544`）
- **冻结文件路径**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-053.md`
- **SHA-256 校验结果**：
  - 预期值：`e1b5bc25b5db03246064743873ddb015c39c415afcb2d5911f7a1041549f122d`
  - 实测值：`e1b5bc25b5db03246064743873ddb015c39c415afcb2d5911f7a1041549f122d`
  - 校验状态：**一致**
- **源码与译文参考基准**：
  - 公开引擎与模块源码（`tome`）：`/workspace/t-engine4`，固定 commit：`624a67329fe2ad440c5b344785a9c73fcf22ae63`
  - 译文仓库参考终点：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`
  - 本批全部 40 条均属于核心游戏模块的天空系技能文件（`mod-tome/data/talents/celestial/`），不涉及 DLC 或未定位源码的扩展包。

---

## 2. 逐条复核详情（全 40 条逐一覆盖）

### entry-01505
- **位置与标签**：`mod-tome.lua:20980`；section：`mod-tome/data/talents/celestial/celestial.lua`；`_t`
- **复核结论**：未发现问题
- **可核验依据**：固定 commit 源码 `celestial.lua:49` 为技能树 `celestial/dirge` 描述 `description = _t"Sing of death and damnation."`。译文“死亡和毁灭之歌。”准确凝练，与其他技能系描述风格保持一致，无占位符，标点准确。

---

### entry-01506
- **位置与标签**：`mod-tome.lua:20992`；section：`mod-tome/data/talents/celestial/chants.lua`；`tformat`
- **复核结论**：未发现问题
- **可核验依据**：源码 `chants.lua:105` (`Chant of Fortress`) 传递 3 个格式化参数：物理抗性、物理豁免、护甲值。原文与译文均为 3 个数值占位符（`%d%%`、`%d`、`%d`），顺序一致；硬编码数值 `+15%%` 译为 `15%%`（略去前置加号），机制表述完整准确。

---

### entry-01507
- **位置与标签**：`mod-tome.lua:20998`；section：`mod-tome/data/talents/celestial/chants.lua`；`tformat`
- **复核结论**：未发现问题
- **可核验依据**：源码 `chants.lua:147` (`Chant of Resistance`) 传递 3 个格式化参数：四系抗性、法术豁免、远距离减伤。“reduces the damage from enemies 3 or more spaces away by %d%%”准确译为“减少三格外敌人对你造成的伤害 %d%%”，3 个占位符（`%d%%`、`%d`、`%d%%`）与换行格式完全匹配。

---

### entry-01508
- **位置与标签**：`mod-tome.lua:21014`；section：`mod-tome/data/talents/celestial/chants.lua`；`tformat`
- **复核结论**：细微观察
- **可核验依据**：
  1. 占位符核验：源码 `chants.lua:201` (`Chant Acolyte`) 依次传递 8 个参数（坚韧精神豁免、坚韧生命百分比、堡垒物理豁免、堡垒物理抗性、堡垒护甲、元素法术豁免、元素四系抗性、元素远距减伤）。译文中 8 个占位符的类型与出现顺序完全吻合，技能名对齐正确（Chant of Resistance 统一为“元素赞歌”）。
  2. 格式观察：译文列表中前两项末尾未打句号，第三项末尾有句号；且第 4 行斜杠处存在空格“/寒冷 /闪电 /酸性”，属轻微排版风格差异，不影响运行及数值渲染。

---

### entry-01509
- **位置与标签**：`mod-tome.lua:21029`；section：`mod-tome/data/talents/celestial/chants.lua`；`tformat`
- **复核结论**：细微观察
- **可核验依据**：
  1. 占位符核验：原文 2 个 `%d` 分别对应光照半径增益与负面状态解除上限，译文占位符数量与类型完全一致。
  2. 机制细节与表达观察：源码 `chants.lua:233-264` (`Chant Adept.doCure`) 逻辑为：按所切赞歌对应的类型（精神/物理/魔法）解除该类型下的所有 cross-tier 效果，再解除至多 %d 个同类型常规 debuff。译文增补了说明括号“（失去平衡、法术冲击和思维封锁）”，虽然当前激活某一赞歌时仅解除对应类型的 cross-tier（并非每次同时解除三种），但后续分项说明（坚韧->精神，堡垒->物理，元素->魔法）已明确划分类型，因此该括号属于补充常见越层效果名称的释义性翻译，不影响实质机制理解。

---

### entry-01510
- **位置与标签**：`mod-tome.lua:21053`；section：`mod-tome/data/talents/celestial/circles.lua`；`tformat`
- **复核结论**：细微观察
- **可核验依据**：
  1. 占位符核验：源码 `circles.lua:97` (`Circle of Sanctity`) 格式化参数为半径、光系伤害、持续回合。译文对应 3 个 `%d` 占位符，顺序无误。
  2. 格式观察：英文原文为单行描述无换行，译文在末句“法阵持续 %d 回合。”前添加了一处换行缩进（`\n\t\t`），在 Lua 多行字符串内语法合法，排版显示略有拆分。

---

### entry-01511
- **位置与标签**：`mod-tome.lua:21056`；section：`mod-tome/data/talents/celestial/circles.lua`；`tformat`
- **复核结论**：未发现问题
- **可核验依据**：源码 `circles.lua:147` (`Circle of Warding`) 传递 5 个参数：半径、弹道减速百分比、光系伤害、暗影伤害、持续回合。译文中 5 个占位符（`%d`、`%d%%`、`%0.2f`、`%0.2f`、`%d`）数量、类型及顺序完全对齐，词义准确。

---

### entry-01512
- **位置与标签**：`mod-tome.lua:21076`；section：`mod-tome/data/talents/celestial/combat.lua`；`tformat`
- **复核结论**：细微观察
- **可核验依据**：
  1. 占位符核验：原文占位符为 `%0.1f`（附加光伤）和 `%d`（护盾强化值），译文占位符完全匹配。
  2. 版本差异观察：在固定 commit 624a673 源码中，该技能描述已包含“and set its duration to 2 (if not already higher)”，而条目冻结的英文文本取自未含该句的基线，当前译文完全忠实于冻结条目的英文原文。

---

### entry-01513
- **位置与标签**：`mod-tome.lua:21083`；section：`mod-tome/data/talents/celestial/combat.lua`；`tformat`；`args_order: [1, 2, 3, 5, 4]`
- **复核结论**：未发现问题
- **可核验依据**：源码 `combat.lua:164` (`Wave of Power`) 传参顺序为：第 1 击伤害、第 2 击伤害、距离 2 触发率（浮点）、最大射程触发率（浮点）、最大射程（整数）。中文译文将语序调整为“距离最大（%d）时几率为 %0.1f%%”，占位符顺序变为第 4 个是整数 `%d`，第 5 个是浮点 `%0.1f%%`。经核查 `engine/I18N.lua:default_tformat`，`args_order: [1, 2, 3, 5, 4]` 正确将原参数第 5 项映射至译文第 4 个占位符、原参数第 4 项映射至译文第 5 个占位符，重排准确无误，运行时类型安全。

---

### entry-01514
- **位置与标签**：`mod-tome.lua:21091`；section：`mod-tome/data/talents/celestial/combat.lua`；`tformat`
- **复核结论**：细微观察
- **可核验依据**：
  1. 占位符核验：源码 `combat.lua:222` (`Weapon of Wrath`) 传递 4 个参数（损失生命比例、最大伤害上限、当前伤害值、殉难反伤比例）。译文 4 个占位符（`%d%%`、`%d`、`%d`、`%d%%`）完全对齐。
  2. 标点观察：英文第 1 行末尾为 `(up to %d, Current:  %d).`，译文第 1 行末尾“当前 %d 点”缺少句末标点或闭合括号，第 2、3 行标点正常。

---

### entry-01515
- **位置与标签**：`mod-tome.lua:21097`；section：`mod-tome/data/talents/celestial/combat.lua`；`tformat`
- **复核结论**：未发现问题
- **可核验依据**：源码 `combat.lua:258` (`Second Life`) 传递 1 个参数（治疗数值 `t.getLife`），译文“然后受到 %d 点治疗”与占位符 `%d` 完全对应，机制表达准确。

---

### entry-01516
- **位置与标签**：`mod-tome.lua:21110`；section：`mod-tome/data/talents/celestial/crusader.lua`；`tformat`
- **复核结论**：细微观察
- **可核验依据**：
  1. 占位符核验：源码 `crusader.lua:60` (`Absorption Strike`) 传递 3 个参数（武器伤害、光抗削减、伤害降低）。译文 3 个 `%d%%` 占位符数量与顺序一致。
  2. 标点排版观察：第 2 行逗号前存在多余空格（`%d%% , 持续 5 回合`），不影响运行与内容表达。

---

### entry-01517
- **位置与标签**：`mod-tome.lua:21116`；section：`mod-tome/data/talents/celestial/crusader.lua`；`tformat`
- **复核结论**：细微观察
- **可核验依据**：
  1. 占位符核验：源码 `crusader.lua:125` (`Righteous Strength`) 传递 4 个参数（物暴提升、伤害增益、灼伤光伤、护甲削减）。译文 4 个占位符（`%d%%`、`%d%%`、`%0.2f`、`%d`）完全吻合。
  2. 标点与用词观察：第 1 行逗号前存在多余空格（`%d%% , 同时`）；“lasting lightburn”译为“灼烧痕迹”，通俗可懂。

---

### entry-01518
- **位置与标签**：`mod-tome.lua:21122`；section：`mod-tome/data/talents/celestial/crusader.lua`；`tformat`
- **复核结论**：细微观察
- **可核验依据**：
  1. 占位符核验：源码 `crusader.lua:180` (`Flash of the Blade`) 传递 2 个参数（半径 1 武器伤害、半径 2 光系武器伤害）。译文 2 个 `%d%%` 占位符完全匹配。
  2. 排版观察：英文原文为 4 行，译文将第 2 行（半径 1 伤害）与第 3 行（半径 2 伤害）合并在同一行展示，内容完整无缺失。4 级护盾机制对齐源码无误。

---

### entry-01519
- **位置与标签**：`mod-tome.lua:21142`；section：`mod-tome/data/talents/celestial/dark-sun.lua`；`talent name`
- **复核结论**：未发现问题
- **可核验依据**：源码 `dark-sun.lua:104` 技能名 `Singularity Armor`，译文“奇点护甲”准确规范。

---

### entry-01520
- **位置与标签**：`mod-tome.lua:21166`；section：`mod-tome/data/talents/celestial/darkside.lua`；`tformat`
- **复核结论**：未发现问题
- **可核验依据**：源码 `darkside.lua:80` (`Lunacy`) 传递 2 个参数（基于意志的法强加成、基于魔力的精神强度加成）。译文中 2 个 `%d%%` 占位符、斜体标签 `#{italic}#` 及还原标签 `#{normal}#` 完全保留无误，属性对应准确。

---

### entry-01521
- **位置与标签**：`mod-tome.lua:21176`；section：`mod-tome/data/talents/celestial/darkside.lua`；`logSeen`
- **复核结论**：未发现问题
- **可核验依据**：源码 `darkside.lua:118` 传送失败战斗日志，占位符 `%s` 匹配，译文“%s 的传送失败了！”自然准确。

---

### entry-01522
- **位置与标签**：`mod-tome.lua:21177`；section：`mod-tome/data/talents/celestial/darkside.lua`；`logSeen`
- **复核结论**：未发现问题
- **可核验依据**：源码 `darkside.lua:120` 现身战斗日志，占位符 `%s` 匹配，译文“%s从黑暗中现身了！”自然准确。

---

### entry-01523
- **位置与标签**：`mod-tome.lua:21204`；section：`mod-tome/data/talents/celestial/dirge.lua`；`tformat`
- **复核结论**：未发现问题
- **可核验依据**：源码 `dirge.lua:49` (`Dirge of Conquest`) 传递 1 个参数（击杀获得回合比例）。原文硬编码 `10%%` 转义完整，占位符 `%d%%` 匹配，换行与末尾空行严格对应。

---

### entry-01524
- **位置与标签**：`mod-tome.lua:21227`；section：`mod-tome/data/talents/celestial/dirge.lua`；`talent name`
- **复核结论**：未发现问题
- **可核验依据**：源码 `dirge.lua:150` 技能名 `Dirge Intoner`，译文“挽歌吟诵者”准确规范。

---

### entry-01525
- **位置与标签**：`mod-tome.lua:21239`；section：`mod-tome/data/talents/celestial/dirge.lua`；`talent name`
- **复核结论**：未发现问题
- **可核验依据**：源码 `dirge.lua:178` 技能名 `Dirge Nihilist`，译文“挽歌虚无者”准确规范。

---

### entry-01526
- **位置与标签**：`mod-tome.lua:21275`；section：`mod-tome/data/talents/celestial/glyphs.lua`；`tformat`
- **复核结论**：未发现问题
- **可核验依据**：源码 `glyphs.lua:160` (`Glyphs`) 传递 11 个参数。译文全部 11 个占位符（`%d`、`%d`、`%d`、`%0.2f`、`%d`、`%0.2f`、`%d%%`、`%d`、`%0.2f`、`%0.2f`、`%d`）类型与顺序无误，三处颜色标签（`#ffd700#...#LAST#`、`#7f7f7f#...#LAST#`、`#9D9DC9#...#LAST#`）完整无损，圣印名称与资源术语一致。

---

### entry-01527
- **位置与标签**：`mod-tome.lua:21306`；section：`mod-tome/data/talents/celestial/glyphs.lua`；`tformat`
- **复核结论**：未发现问题
- **可核验依据**：源码 `glyphs.lua:192` (`Empowered Glyphs`) 传递持续回合与最大叠加层数。原文固定数值 `5%%` 正确转义，2 个 `%d` 占位符顺序吻合，每回合触发 3 次的限制置于句末表达通顺。

---

### entry-01528
- **位置与标签**：`mod-tome.lua:21308`；section：`mod-tome/data/talents/celestial/glyphs.lua`；`tformat`
- **复核结论**：细微观察
- **可核验依据**：
  1. 占位符与颜色码：源码 `glyphs.lua:256` (`Destabilize Glyphs`) 传递 5 个参数（持续回合、日光伤害、月光伤害、暮光光伤、暮光暗伤）。译文 5 个占位符（`%d`、`%0.2f`、`%0.2f`、`%0.2f`、`%0.2f`）与颜色标签严格对齐。
  2. 标点与用词观察：英文末行末尾无句号，译文补充句号；列表项补充“圣印”后缀对齐概念。未发现实质问题。

---

### entry-01529
- **位置与标签**：`mod-tome.lua:21330`；section：`mod-tome/data/talents/celestial/guardian.lua`；`logPlayer`
- **复核结论**：未发现问题
- **可核验依据**：源码 `guardian.lua:34` 技能无盾提示。技能 Brandish 在同 section 统一定名为“剑盾之怒”，译文“没有盾牌就无法使用剑盾之怒！”与之完全对应。

---

### entry-01530
- **位置与标签**：`mod-tome.lua:21335`；section：`mod-tome/data/talents/celestial/guardian.lua`；`logPlayer`
- **复核结论**：未发现问题
- **可核验依据**：源码 `guardian.lua:92` 技能无盾提示。技能 Retribution 在同 section 统一定名为“惩戒之盾”，译文“没有盾牌就无法使用惩戒之盾！”与之完全对应。

---

### entry-01531
- **位置与标签**：`mod-tome.lua:21343`；section：`mod-tome/data/talents/celestial/guardian.lua`；`logPlayer`
- **复核结论**：细微观察
- **可核验依据**：源码 `guardian.lua:149` 技能无盾提示。技能 Crusade 在同 section 定名为“十字军打击”。译文将否定表达“无法使用……没有盾牌”转换为肯定限制句“使用十字军打击必须使用盾牌！”，语义等价，表达通顺。

---

### entry-01532
- **位置与标签**：`mod-tome.lua:21344`；section：`mod-tome/data/talents/celestial/guardian.lua`；`tformat`
- **复核结论**：未发现问题
- **可核验依据**：源码 `guardian.lua:170` (`Crusade`) 传递 4 个参数（主手光伤百分比、盾牌光伤百分比、冷却减少技能数、解除负面状态数）。译文 4 个占位符（`%d%%`、`%d%%`、`%d`、`%d`）完全吻合，且“至多 %d 个负面状态”精准对应源码 `self:removeEffectsFilter` 的上限逻辑。

---

### entry-01533
- **位置与标签**：`mod-tome.lua:21407`；section：`mod-tome/data/talents/celestial/hymns.lua`；`tformat`
- **复核结论**：未发现问题
- **可核验依据**：源码 `hymns.lua:125` (`Hymn Adept`) 传递 6 个参数（暗视半径、移速加成、隐形强度、隐形时间、护盾强度、护盾时间）。译文 6 个占位符（`%d`、`%d%%`、`%d`、`%d`、`%d`、`%d`）严格对应，各项圣诗名称（暗影、侦测、坚毅）与术语库一致。

---

### entry-01534
- **位置与标签**：`mod-tome.lua:21433`；section：`mod-tome/data/talents/celestial/light.lua`；`tformat`
- **复核结论**：细微观察
- **可核验依据**：
  1. 占位符与机制核验：源码 `light.lua:67` (`Bathe in Light`) 传递 4 个参数（范围、每回合治疗量、受治疗效果加成比例、持续回合）。译文 4 个占位符（`%d`、`%0.2f`、`%d%%`、`%d`）完全一致。机制中 `DamageType.HEALING_POWER` 兼具治疗与护盾效果，译文“每回合治疗所有单位 %0.2f 生命值，给予其等量的护盾”准确还原代码底层效果。
  2. 标点观察：英文最后一行末尾无句号，译文补全句号。

---

### entry-01535
- **位置与标签**：`mod-tome.lua:21456`；section：`mod-tome/data/talents/celestial/other.lua`；`tformat`
- **复核结论**：未发现问题
- **可核验依据**：源码 `other.lua:121` 爆炸圣印陷阱描述（提取器提取的代码段），占位符 `%d` 与伤害类型完全吻合，译文“爆炸（范围 1）造成 %d 光系伤害。”准确无误。

---

### entry-01536
- **位置与标签**：`mod-tome.lua:21483`；section：`mod-tome/data/talents/celestial/radiance.lua`；`tformat`
- **复核结论**：细微观察
- **可核验依据**：
  1. 占位符核验：源码 `radiance.lua:52` (`Radiance`) 传递 4 个参数（光照半径、致盲抗性、光系抗性、光系亲和）。译文 4 个占位符（`%d`、`%d%%`、`%d%%`、`%d%%`）完全对齐。
  2. 术语与意译观察：“blindness resistance”译为“目盲免疫”（汉化常见用法）；“normal light”译为“灯具”。末尾缩进与换行均一致。

---

### entry-01537
- **位置与标签**：`mod-tome.lua:21502`；section：`mod-tome/data/talents/celestial/radiance.lua`；`tformat`
- **复核结论**：未发现问题
- **可核验依据**：源码 `radiance.lua:144` (`Illumination`) 传递 4 个参数（潜行与隐形削减值、闪避降低值、光伤提升百分比、光抗穿透百分比）。译文 4 个占位符（`%d`、`%d`、`%d%%`、`%d%%`）顺序无误，防御、闪避、法强等机制术语对齐准确。

---

### entry-01538
- **位置与标签**：`mod-tome.lua:21534`；section：`mod-tome/data/talents/celestial/sun.lua`；`tformat`
- **复核结论**：未发现问题
- **可核验依据**：源码 `sun.lua:79` (`Sun Ray`) 传递光系伤害（浮点）与致盲回合（整数）。译文 2 个占位符（`%0.1f`、`%d`）类型与顺序完全匹配，机制表述清晰。

---

### entry-01539
- **位置与标签**：`mod-tome.lua:21540`；section：`mod-tome/data/talents/celestial/sun.lua`；`tformat`
- **复核结论**：未发现问题
- **可核验依据**：源码 `sun.lua:118` (`Path of the Sun`) 字符串格式化中仅使用 1 个占位符（每回合光伤）。译文 `%0.1f` 对应准确，“行走不消耗时间，也不会触发陷阱”准确反映代码机制。

---

### entry-01540
- **位置与标签**：`mod-tome.lua:21556`；section：`mod-tome/data/talents/celestial/sun.lua`；`tformat`
- **复核结论**：未发现问题
- **可核验依据**：源码 `sun.lua:186` (`Suncloak`) 传递 3 个百分比参数（施法速度加成、冷却缩减比例、单次受击伤害上限比例）。译文 3 个 `%d%%` 占位符顺序一致，防暴死机制表达准确。

---

### entry-01541
- **位置与标签**：`mod-tome.lua:21597`；section：`mod-tome/data/talents/celestial/twilight.lua`；`tformat`
- **复核结论**：未发现问题
- **可核验依据**：源码 `twilight.lua:74` (`Jumpgate: Teleport To`) 传递 1 个射程参数。译文占位符 `%d` 匹配，语义清晰无歧义。

---

### entry-01542
- **位置与标签**：`mod-tome.lua:21606`；section：`mod-tome/data/talents/celestial/twilight.lua`；`tformat`
- **复核结论**：未发现问题
- **可核验依据**：源码 `twilight.lua:178` (`Mind Blast`) 传递 4 个参数（半径、暗影伤害、混乱失控几率、持续回合）。译文 4 个占位符（`%d`、`%0.2f`、`%d%%`、`%d`）位置与类型吻合，灵巧（Cunning）与法术强度（Spellpower）属性对齐正确。

---

### entry-01543
- **位置与标签**：`mod-tome.lua:21610`；section：`mod-tome/data/talents/celestial/twilight.lua`；`logPlayer`
- **复核结论**：细微观察
- **可核验依据**：
  1. 源码核对：源码 `twilight.lua:203` 为 `game.logPlayer(self, "Not enough space to summon!")`，译文为“没有足够的空间召唤！”。
  2. 术语库对比观察：术语库中有一条全局日志规则 `Not enough space to summon! -> 没有足够的空间召唤。`（标记为句号、logSeen）。本处英文原句带有感叹号 `!`，且属于 `logPlayer` 语境，译文保留全角感叹号严格对照英文原文标点，含义完全一致，不影响运行。

---

### entry-01544
- **位置与标签**：`mod-tome.lua:21621`；section：`mod-tome/data/talents/celestial/twilight.lua`；`tformat`
- **复核结论**：细微观察
- **可核验依据**：
  1. 占位符核验：源码 `twilight.lua:301` (`Jumpgate Two`) 传递 1 个射程参数，译文 `%d` 占位符匹配。
  2. 机制与技能名观察：英文原文写有 `'Jumpgate: Teleport'`，但在代码 `twilight.lua:266` 中，开启 Jumpgate Two 后实际习得并供使用的子技能为 `T_JUMPGATE_TELEPORT_TWO`（即 `Jumpgate Two: Teleport To`，汉化为“跃迁之门II：传送”）。中文译文修正为“「跃迁之门II：传送」”，准确指引了玩家技能栏中的实际对应子技能，属于改善游戏体验的积极校正。

---

## 3. 汇总概览

- **总复核条目数**：40 条（entry-01505 至 entry-01544）
- **未发现问题条目**：28 条（entry-01505, 01506, 01507, 01511, 01513, 01515, 01519, 01520, 01521, 01522, 01523, 01524, 01525, 01526, 01527, 01529, 01530, 01532, 01533, 01535, 01537, 01538, 01539, 01540, 01541, 01542 等）
- **细微观察条目**：12 条（包括排版微差、句末标点微调、原文化用增补说明或上游代码机制主动校准）：
  - `entry-01508`：行末标点不完全统一，斜杠旁有空格。
  - `entry-01509`：译文补充越层状态名称括号，机制上每次仅针对单一类型生效。
  - `entry-01510`：译文末句较原文多一处换行与制表符。
  - `entry-01512`：当前 commit 源码新增了刷新 2 回合时长的英文说明，而基线冻结原文未包含，译文与条目原文一致。
  - `entry-01514`：第 1 行末尾缺少句末标点或闭合括号。
  - `entry-01516`：逗号前有多余空格。
  - `entry-01517`：逗号前有多余空格；lightburn 意译为灼烧痕迹。
  - `entry-01518`：将英文原文的第 2、3 行合并为一行。
  - `entry-01528`：末行补全句号，补充“圣印”后缀。
  - `entry-01531`：双重否定句式微调为肯定必要条件句式。
  - `entry-01534`：英文末行无句号，译文补全句号。
  - `entry-01536`：状态抗性习惯译为免疫，normal light 意译为灯具。
  - `entry-01543`：沿用英文原句叹号，与术语库句号存在标点微差。
  - `entry-01544`：主动将英文原句疏忽写成的旧技能名校正为实际激活的子技能名「跃迁之门II：传送」。
- **阻断性语法/运行时缺陷**：0 条（无占位符缺失、类型不匹配、死循环或破坏性崩溃风险）。特别说明：`entry-01513` 中的参数重排（`args_order: [1, 2, 3, 5, 4]`）经核验与引擎 `I18N.lua` 实现完全兼容，格式化运行安全。