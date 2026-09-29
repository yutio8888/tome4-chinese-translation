# batch-013 只读译文复核报告

## 一、批次与基准核验

- **批次文件**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-013.md`
- **文件哈希校验**：SHA-256 计算结果为 `27ef1130aaebaac8e316f01325f3f73a1007de2c626f03099008b12ce78f2b07`，与冻结要求完全一致。
- **条目范围**：`entry-00481` 至 `entry-00520`，共 40 条，已实现逐条全覆盖核查。
- **源码参考基准**：
  - 公开引擎与本体源码来自固定 commit：`624a67329fe2ad440c5b344785a9c73fcf22ae63`（通过 `git show` 读取 `/workspace/t-engine4` 对应路径）。
  - 译文终点基准：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`。
  - 本批涉及文件均为本体 `mod-tome` 涉及的职业及种族诞生描述文件（`data/birth/classes/`、`data/birth/descriptors.lua`、`data/birth/races/`），未涉及 DLC 内容。

---

## 二、逐条复核详情（共 40 条）

### entry-00481
- **位置**：`mod-tome.lua:3077`（对应源码 `game/modules/tome/data/birth/classes/rogue.lua:53`）
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# +0`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# +0`
- **复核结论**：未发现问题
- **核验依据**：颜色代码 `#GOLD#` 与 `#LIGHT_BLUE#` 保留完整，数值 `+0` 匹配；对应盗贼（Rogue）生命成长设定，全库此类模板格式一致。

### entry-00482
- **位置**：`mod-tome.lua:3093`（对应源码 `game/modules/tome/data/birth/classes/rogue.lua:226`）
- **原文**：`Fleet of foot and strong of throw, overwhelming every foe, from afar we counter, strike and thud, in the chaos'd skirmish spilling blood.`
- **译文**：`脚程轻捷，投掷有力，压倒每一个敌人；我们自远处反击、痛打、重创，在混乱的遭遇战中溅洒鲜血。`
- **复核结论**：未发现问题
- **核验依据**：散兵（Skirmisher）解锁诗歌韵文，译文节奏工整，分句与分号对应原文四音步结构，词义完整传达。

### entry-00483
- **位置**：`mod-tome.lua:3117`（对应源码 `game/modules/tome/data/birth/classes/warrior.lua:60`）
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# +3`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# +3`
- **复核结论**：未发现问题
- **核验依据**：狂战士（Berserker）生命成长修正，源码 `copy_add.life_rating = 3`，颜色标签及数值完全匹配。

### entry-00484
- **位置**：`mod-tome.lua:3123`（对应源码 `game/modules/tome/data/birth/classes/warrior.lua:118`）
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# +6`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# +6`
- **复核结论**：未发现问题
- **核验依据**：盾战士（Bulwark）生命成长修正，源码 `copy_add.life_rating = 6`，颜色标签及数值完全匹配。

### entry-00485
- **位置**：`mod-tome.lua:3127`（对应源码 `game/modules/tome/data/birth/classes/warrior.lua:174`）
- **原文**：`Archers can become good with either longbows or slings.`
- **译文**：`弓箭手可以专精于长弓或投石索。`
- **复核结论**：未发现问题
- **核验依据**：弓箭手（Archer）职业机制说明，长弓（longbows）与投石索（slings）术语与游戏内武器子类完全对应。

### entry-00486
- **位置**：`mod-tome.lua:3128`（对应源码 `game/modules/tome/data/birth/classes/warrior.lua:175`）
- **原文**：`Their most important stats are: Dexterity and Strength (when using bows) or Cunning (when using slings)`
- **译文**：`他们最重要的属性是：敏捷和力量（装备弓时）或灵巧（装备投石索）`
- **复核结论**：细微观察
- **核验依据**：属性名（敏捷、力量、灵巧）符合术语表规范。但前半句为“（装备弓时）”，后半句“（装备投石索）”脱落了“时”字，括号内结构不对称；且原文两处均为“when using”，译为“装备”略有词义轻微偏移（弓箭手发射时区分武器类型），但不影响玩家实际理解。

### entry-00487
- **位置**：`mod-tome.lua:3131`（对应源码 `game/modules/tome/data/birth/classes/warrior.lua:178`）
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# +0`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# +0`
- **复核结论**：未发现问题
- **核验依据**：弓箭手生命成长设定，颜色标签与数值 `+0` 匹配。

### entry-00488
- **位置**：`mod-tome.lua:3135`（对应源码 `game/modules/tome/data/birth/classes/warrior.lua:234`）
- **原文**：`They can cast spells from a limited selection but have the unique capacity to 'channel' their attack spells through their melee attacks.`
- **译文**：`他们能施展一些有限的法术，并且独有将攻击法术「导引」进近战攻击的能力。`
- **复核结论**：未发现问题
- **核验依据**：准确描述奥术之刃核心机制 `Arcane Combat`（将法术导引附着于近战普通攻击并触发），引号保留中文角引号「导引」，语法流畅。

### entry-00489
- **位置**：`mod-tome.lua:3136`（对应源码 `game/modules/tome/data/birth/classes/warrior.lua:235`）
- **原文**：`They are adept with two-handed weapons, for the sheer destruction they can bring.`
- **译文**：`他们擅长使用双手武器，造成最大的伤害。`
- **复核结论**：细微观察
- **核验依据**：“for the sheer destruction they can bring”意译为“造成最大的伤害”，相较原文偏向平铺直叙与泛化（字面意为追求双手武器带来的纯粹破坏力/毁灭），但符合奥术之刃双手重击构筑语境，无机制错误。

### entry-00490
- **位置**：`mod-tome.lua:3140`（对应源码 `game/modules/tome/data/birth/classes/warrior.lua:269`）
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# +2`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# +2`
- **复核结论**：未发现问题
- **核验依据**：奥术之刃生命成长修正，源码 `copy_add.life_rating = 2`，标签与数值无误。

### entry-00491
- **位置**：`mod-tome.lua:3142`（对应源码 `game/modules/tome/data/birth/classes/warrior.lua:315`）
- **原文**：`Though you may fight alone against many, destined to fight till you die, still you do not relent. In a ring of blood you learn that a pair of fists can face the world.`
- **译文**：`纵使你独自一人面对千军万马，注定战至最后一刻，你依然绝不退缩。在鲜血之环中，你学会了一双拳头就足以面对整个世界。`
- **复核结论**：未发现问题
- **核验依据**：格斗家（Brawler）解锁描述，鲜血之环（Ring of Blood）为对应解锁世界事件，语义与背景高度契合。

### entry-00492
- **位置**：`mod-tome.lua:3145`（对应源码 `game/modules/tome/data/birth/classes/warrior.lua:318`）
- **原文**：`Whether a pit-fighter, a boxer, or just an amateur practitioner, the Brawler's skills are still handy today.`
- **译文**：`无论是一个职业拳手还是个业余的门外汉，格斗技能直到现在仍然十分有用。`
- **复核结论**：存在疑点
- **核验依据**：
  1. 原文并列列出三类人：“a pit-fighter（角斗士/地下格斗者）”、“a boxer（拳击手）”、“an amateur practitioner（业余练习者/研习者）”。
  2. 译文“无论是一个职业拳手还是个业余的门外汉”漏译了“pit-fighter”（斗坑格斗者/角斗士，这正是游戏内鲜血之环等斗兽场格斗的核心背景），并疑似将 boxer 与 pit-fighter 概括合并为“职业拳手”。
  3. 将“amateur practitioner”译为“业余的门外汉”存在严重词义歪曲：practitioner 是实际研习/修习某种技能的从业者或研习者；“门外汉”指完全不通此道的局外人（layman），含义直接相悖，与后文“格斗家的技能”产生逻辑矛盾。

### entry-00493
- **位置**：`mod-tome.lua:3167`（对应源码 `game/modules/tome/data/birth/classes/wilder.lua:62`）
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# +0`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# +0`
- **复核结论**：未发现问题
- **核验依据**：召唤师（Summoner）生命成长修正，标签与数值完全匹配。

### entry-00494
- **位置**：`mod-tome.lua:3168`（对应源码 `game/modules/tome/data/birth/classes/wilder.lua:70`）
- **原文**：`Max summons: %d`
- **译文**：`最大召唤数：%d`
- **复核结论**：未发现问题
- **核验依据**：召唤师属性计算文本格式串，占位符 `%d` 正确保留，术语规范。

### entry-00495
- **位置**：`mod-tome.lua:3170`（对应源码 `game/modules/tome/data/birth/classes/wilder.lua:94`）
- **原文**：`Sleek, majestic, powerful... In the path of dragons we walk, and their breath is our breath. See their beating hearts with your eyes and taste their majesty between your teeth.`
- **译文**：`矫健、雄壮、强大……我们行走在巨龙之道上，它们的吐息便是我们的吐息。用你的双眼凝视它们跳动的心脏，在你的齿间品味它们的威严。`
- **复核结论**：未发现问题
- **核验依据**：龙战士解锁描述，省略号转为中文标准省略号，修辞与文风典雅贴切。

### entry-00496
- **位置**：`mod-tome.lua:3171`（对应源码 `game/modules/tome/data/birth/classes/wilder.lua:96`）
- **原文**：`Wyrmics are fighters who have learnt how to mimic some of the aspects of the dragons.`
- **译文**：`龙战士是学会模仿巨龙部分特质的战士。`
- **复核结论**：未发现问题
- **核验依据**：Wyrmic 统一译为“龙战士”，准确反映其学习龙系天赋的设定。

### entry-00497
- **位置**：`mod-tome.lua:3176`（对应源码 `game/modules/tome/data/birth/classes/wilder.lua:101`）
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# +2`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# +2`
- **复核结论**：未发现问题
- **核验依据**：龙战士生命成长修正，源码 `copy_add.life_rating = 2`，标签与数值完全匹配。

### entry-00498
- **位置**：`mod-tome.lua:3179`（对应源码 `game/modules/tome/data/birth/classes/wilder.lua:159`）
- **原文**：`Oozemancers separate themselves from normal civilisation so that they be more in harmony with Nature. Arcane force are reviled by them, and their natural attunement to the wilds lets them do battle with abusive magic-users on an equal footing.`
- **译文**：`软泥使将自己和正常文明割裂，让自己与自然更加和谐。他们憎恶奥术之力，而与生俱来的自然亲和让他们得以与滥用魔法者势均力敌地交战。`
- **复核结论**：未发现问题
- **核验依据**：软泥使（Oozemancer）反魔背景与自然亲和描述，概念传达准确。

### entry-00499
- **位置**：`mod-tome.lua:3183`（对应源码 `game/modules/tome/data/birth/classes/wilder.lua:164`）
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# -3`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# -3`
- **复核结论**：未发现问题
- **核验依据**：软泥使生命成长负修正，源码 `copy_add.life_rating = -3`，负号保留无误。

### entry-00500
- **位置**：`mod-tome.lua:3192`（对应源码 `game/modules/tome/data/birth/classes/wilder.lua:226`）
- **原文**：`Stone Wardens are dwarves trained in both the eldritch arts and the worship of nature.`
- **译文**：`岩石守卫是同时研习奥术技艺与自然崇拜的矮人。`
- **复核结论**：细微观察
- **核验依据**：原文词汇为“eldritch arts”，而生物分类与 Cults DLC 中 eldritch 统一译为“骇异”。但在岩石守卫的机制源码中（`power_source = {nature=true, arcane=true}`，法术树 `eldritch-shield` 等均造成奥术伤害，且前文诗歌与后文均直接阐述矮人调和“nature and arcane”），此处的 eldritch arts 实质即指其掌握的奥术/法术技艺。译者意译为“奥术技艺”准确契合机制，但字面未能保留 eldritch（怪异/秘术）的神秘风格色彩，属合理语境意译观察。

### entry-00501
- **位置**：`mod-tome.lua:3250`（对应源码 `game/modules/tome/data/birth/descriptors.lua:282`）
- **原文**：`Player is being hunted! Randomly all foes in a radius will get a feeling of where she/he is`
- **译文**：`玩家处于被捕猎的状态，随机地，一定半径内的所有敌人都会感知到你所在的位置。`
- **复核结论**：细微观察
- **核验依据**：
  1. 标点：原文独立短句“Player is being hunted!”带有感叹号，译文中弱化为逗号“玩家处于被捕猎的状态，随机地，...”。
  2. 人称：前半句采用第三人称“玩家”，后半句将“where she/he is”转译为第二人称“你所在的位置”，句内人称视角发生切换。机制描述（绝望难度专属天赋 `HUNTED_PLAYER` 效果）准确无误。

### entry-00502
- **位置**：`mod-tome.lua:3263`（对应源码 `game/modules/tome/data/birth/descriptors.lua:339`）
- **原文**：`Use it if you want normal playing conditions but do not feel ready for just one life.#{normal}#`
- **译文**：`如果你想要普通的游戏条件、但还没准备好一条命通关，就选择这个模式。#{normal}#`
- **复核结论**：未发现问题
- **核验依据**：冒险模式说明，格式标记 `#{normal}#` 完整闭合，顿号与逗号使用合理。

### entry-00503
- **位置**：`mod-tome.lua:3288`（对应源码 `game/modules/tome/data/birth/races/construct.lua:60`）
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# 13`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# 13`
- **复核结论**：未发现问题
- **核验依据**：符文傀儡（Runic Golem）种族生命成长设定，源码 `life_rating = 13`，标签与数值完全匹配。

### entry-00504
- **位置**：`mod-tome.lua:3289`（对应源码 `game/modules/tome/data/birth/races/construct.lua:61`）
- **原文**：`#GOLD#Experience penalty:#LIGHT_BLUE# 25%`
- **译文**：`#GOLD#经验惩罚：#LIGHT_BLUE# 25%`
- **复核结论**：未发现问题
- **核验依据**：符文傀儡经验惩罚设定，源码 `experience = 1.25`（即 +25%），标签与百分比完全匹配。

### entry-00505
- **位置**：`mod-tome.lua:3336`（对应源码 `game/modules/tome/data/birth/races/dwarf.lua:68`）
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# 14`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# 14`
- **复核结论**：未发现问题
- **核验依据**：矮人（Dwarf）种族生命成长，源码 `life_rating = 14`，格式无误。

### entry-00506
- **位置**：`mod-tome.lua:3337`（对应源码 `game/modules/tome/data/birth/races/dwarf.lua:69`）
- **原文**：`#GOLD#Experience penalty:#LIGHT_BLUE# 0%`
- **译文**：`#GOLD#经验惩罚：#LIGHT_BLUE# 0%`
- **复核结论**：未发现问题
- **核验依据**：矮人经验惩罚，数值为 0%，格式无误。

### entry-00507
- **位置**：`mod-tome.lua:3458`（对应源码 `game/modules/tome/data/birth/races/elf.lua:103`）
- **原文**：`Shaloren elves have close ties with the magic of the world, and produced in the past many great mages.`
- **译文**：`永恒精灵与这个世界的魔法有着很强的联系，曾一度出现过许多伟大的魔法师。`
- **复核结论**：未发现问题
- **核验依据**：永恒精灵（Shaloren / Shalore）与魔法渊源描述，术语符合规范。

### entry-00508
- **位置**：`mod-tome.lua:3464`（对应源码 `game/modules/tome/data/birth/races/elf.lua:109`）
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# 9`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# 9`
- **复核结论**：未发现问题
- **核验依据**：永恒精灵生命成长修正，标签与数值完全匹配。

### entry-00509
- **位置**：`mod-tome.lua:3465`（对应源码 `game/modules/tome/data/birth/races/elf.lua:110`）
- **原文**：`#GOLD#Experience penalty:#LIGHT_BLUE# 12%`
- **译文**：`#GOLD#经验惩罚：#LIGHT_BLUE# 12%`
- **复核结论**：未发现问题
- **核验依据**：文本忠实反映源码界面文本（虽然代码底层 `experience = 1.3` 为源码自身数值历史差异，但译文完全忠实于英文原文串）。

### entry-00510
- **位置**：`mod-tome.lua:3473`（对应源码 `game/modules/tome/data/birth/races/elf.lua:148`）
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# 11`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# 11`
- **复核结论**：未发现问题
- **核验依据**：自然精灵（Thalore）生命成长修正，数值与标签完全匹配。

### entry-00511
- **位置**：`mod-tome.lua:3474`（对应源码 `game/modules/tome/data/birth/races/elf.lua:149`）
- **原文**：`#GOLD#Experience penalty:#LIGHT_BLUE# 0%`
- **译文**：`#GOLD#经验惩罚：#LIGHT_BLUE# 0%`
- **复核结论**：未发现问题
- **核验依据**：自然精灵经验惩罚 0%，标签与数值匹配。

### entry-00512
- **位置**：`mod-tome.lua:3506`（对应源码 `game/modules/tome/data/birth/races/giant.lua:66`）
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# 13`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# 13`
- **复核结论**：未发现问题
- **核验依据**：食人魔（Ogre）生命成长修正，源码 `life_rating = 13`，匹配无误。

### entry-00513
- **位置**：`mod-tome.lua:3507`（对应源码 `game/modules/tome/data/birth/races/giant.lua:67`）
- **原文**：`#GOLD#Experience penalty:#LIGHT_BLUE# 15%`
- **译文**：`#GOLD#经验惩罚：#LIGHT_BLUE# 15%`
- **复核结论**：未发现问题
- **核验依据**：食人魔经验惩罚，源码 `experience = 1.15`，匹配无误。

### entry-00514
- **位置**：`mod-tome.lua:3595`（对应源码 `game/modules/tome/data/birth/races/halfling.lua:108`）
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# 12`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# 12`
- **复核结论**：未发现问题
- **核验依据**：半身人（Halfling）生命成长修正，源码 `life_rating = 12`，匹配无误。

### entry-00515
- **位置**：`mod-tome.lua:3596`（对应源码 `game/modules/tome/data/birth/races/halfling.lua:109`）
- **原文**：`#GOLD#Experience penalty:#LIGHT_BLUE# 10%`
- **译文**：`#GOLD#经验惩罚：#LIGHT_BLUE# 10%`
- **复核结论**：未发现问题
- **核验依据**：半身人经验惩罚，源码 `experience = 1.10`，匹配无误。

### entry-00516
- **位置**：`mod-tome.lua:3606`（对应源码 `game/modules/tome/data/birth/races/human.lua:26`）
- **原文**：`The Humans are one of the main races on Maj'Eyal, along with the Halflings. For many thousands of years they fought each other until events, and great people, unified all the Human and Halfling nations under one rule.`
- **译文**：`人类与半身人一起是马基·埃亚尔的主要种族，他们曾互相争战了几千年，直到历史的洪流与伟大的领袖将所有人类和半身人的国度统一在同一面旗帜之下。`
- **复核结论**：未发现问题
- **核验依据**：人类与联合王国背景描述。Maj'Eyal 准确使用裁定术语“马基·埃亚尔”，Halflings 准确使用“半身人”，“events, and great people”意译为“历史的洪流与伟大的领袖”，行文流畅且符合背景历史。

### entry-00517
- **位置**：`mod-tome.lua:3666`（对应源码 `game/modules/tome/data/birth/races/human.lua:139`）
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# 11`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# 11`
- **复核结论**：未发现问题
- **核验依据**：高等人类（Higher）生命成长修正，匹配无误。

### entry-00518
- **位置**：`mod-tome.lua:3667`（对应源码 `game/modules/tome/data/birth/races/human.lua:140`）
- **原文**：`#GOLD#Experience penalty:#LIGHT_BLUE# 0%`
- **译文**：`#GOLD#经验惩罚：#LIGHT_BLUE# 0%`
- **复核结论**：未发现问题
- **核验依据**：高等人类经验惩罚 0%，匹配无误。

### entry-00519
- **位置**：`mod-tome.lua:3673`（对应源码 `game/modules/tome/data/birth/races/human.lua:170`）
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# 10`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# 10`
- **复核结论**：未发现问题
- **核验依据**：科纳克人（Cornac）生命成长修正，匹配无误。

### entry-00520
- **位置**：`mod-tome.lua:3698`（对应源码 `game/modules/tome/data/birth/races/undead.lua:87`）
- **原文**：`Slow to shuffle, quick to bite, learn from master, rule the night!`
- **译文**：`蹒跚而行，利齿如刀，师从主人，统治黑夜！`
- **复核结论**：未发现问题
- **核验依据**：食尸鬼（Ghoul）解锁诗歌，译文采用四字对称句，音律押韵且完全传达原意。

---

## 三、疑点与观察汇总

1. **存在疑点（1 条）**：
   - **entry-00492**（格斗家背景）：原文明确并列列出“a pit-fighter（角斗士/地下格斗者）”、“a boxer（拳击手）”、“an amateur practitioner（业余研习者）”三种背景；译文漏译了斗坑格斗者“pit-fighter”（与游戏内鲜血之环地下拳赛剧情直接相关），且将“practitioner”（修习者）错译为相反概念“门外汉”。建议在后续阶段由主代理核实并交回修正（如：“无论是地下格斗者、拳击手，抑或仅仅是业余练习者…”）。

2. **细微观察（4 条）**：
   - **entry-00486**（弓箭手属性说明）：后半句括号内成“（装备投石索）”，遗漏了与前半句“（装备弓时）”对称的“时”字，略显不对称。
   - **entry-00489**（奥术之刃破坏力）：将“sheer destruction”略作泛化意译为“最大的伤害”，但符合语境，无机制问题。
   - **entry-00500**（岩石守卫技艺）：将“eldritch arts”根据职业机制意译为“奥术技艺”，符合实际 power_source 及法术类型，但字面脱离了 eldritch 词根。
   - **entry-00501**（绝望难度猎捕）：独立感叹句感叹号降格为逗号，且前半句“玩家”与后半句“你”发生句内人称视角切换，但机制说明准确。