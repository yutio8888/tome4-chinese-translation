### batch-012 译文复核报告

#### 1. 前置核验与环境确认
- **batch-012 文件哈希核验**：
  - 目标路径：`evidence/translation-audit/all-modified-review-20260922/batches/batch-012.md`
  - 预期 SHA-256：`1d9583537b865634b2a99042a71836b4018914bd71204fbf36fd8b3e5f84c067`
  - 实际计算 SHA-256：`1d9583537b865634b2a99042a71836b4018914bd71204fbf36fd8b3e5f84c067`
  - 校验结果：**一致（MATCH）**
- **源码与语境接入依据**：
  - 涉及组件均为游戏核心模块 `mod-tome`，依据 `source-access.json` 规则映射至公开源码目录 `/workspace/t-engine4/game/modules/tome/`，并通过 `git show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<path>` 读取固定 commit 源码进行核验。本批不包含 DLC 或第三方 addon 条目。
  - 译文语境基准固定于提交 `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`。

---

#### 2. 逐条复核意见（entry-00441 至 entry-00480）

---

### entry-00441
- **位置**：`mod-tome.lua:2852`
- **section**：`mod-tome/data/achievements/quests.lua`
- **原文**：`Experienced and completed all the dreams in the Dogroth Caldera.`
- **译文**：`经历并完成达格罗斯火山的全部梦境。`
- **结论**：**未发现问题**
- **可核验依据**：固定源码 `data/achievements/quests.lua:ALL_DREAMS` 描述成就条件。术语快照核对 `Dogroth Caldera` 对应 `达格罗斯火山`，句意准确，标点完整。

---

### entry-00442
- **位置**：`mod-tome.lua:2862`
- **section**：`mod-tome/data/achievements/talents.lua`
- **原文**：`Unlocked Archmage class and did over one million fire damage (with any item/talent/class).`
- **译文**：`解锁元素法师职业并造成超过100万火焰伤害（使用任意物品/技能/职业）。`
- **结论**：**未发现问题**
- **可核验依据**：固定源码 `data/achievements/talents.lua:PYROMANCER` 成就描述。`Archmage` 对应职业 `元素法师`，`fire damage` 对应 `火焰伤害`，括号与标点对应无误。

---

### entry-00443
- **位置**：`mod-tome.lua:2864`
- **section**：`mod-tome/data/achievements/talents.lua`
- **原文**：`Unlocked Archmage class and did over one million cold damage (with any item/talent/class).`
- **译文**：`解锁元素法师职业并造成超过100万冰冷伤害（使用任意物品/技能/职业）。`
- **结论**：**细微观察**
- **可核验依据**：固定源码 `data/achievements/talents.lua:CRYOMANCER` 在 `data/damage_types.lua` 中的 `DamageType.COLD` 触发（`world:gainAchievement("CRYOMANCER", src, realdam)`）。在 ToME 规范中，该伤害类型注册名为 `_t("cold", "damage type")` -> `寒冷`，术语快照亦标明 `cold -> 寒冷 (damage type)`。此处译为“冰冷伤害”（对比 entry-00442 的“火焰伤害”）虽不影响游戏理解，但与系统伤害类型统一名称“寒冷伤害”存在细微不一致（全库中“寒冷伤害”占 61 处，“冰冷伤害”占 10 处）。

---

### entry-00444
- **位置**：`mod-tome.lua:2868`
- **section**：`mod-tome/data/achievements/talents.lua`
- **原文**：`Removed 89 beneficial effects from enemies via Disintegration.`
- **译文**：`使用裂解清除敌人身上的89个增益效果。`
- **结论**：**未发现问题**
- **可核验依据**：固定源码 `data/talents/chronomancy/matter.lua` 中技能名为 `Disintegration`，对应中文译名 `裂解`；数量 `89` 及清除增益效果对应准确，句末标点对应。

---

### entry-00445
- **位置**：`mod-tome.lua:2878`
- **section**：`mod-tome/data/birth/classes/adventurer.lua`
- **原文**：`#LIGHT_BLUE# * +2 Strength, +2 Dexterity, +2 Constitution`
- **译文**：`#LIGHT_BLUE# * +2 力量，+2 敏捷，+2 体质`
- **结论**：**未发现问题**
- **可核验依据**：固定源码冒险家（Adventurer）属性加成文本。三项主属性 `力量`、`敏捷`、`体质` 符合术语规范，前置颜色代码 `#LIGHT_BLUE#` 与符号、数值均完全保留。

---

### entry-00446
- **位置**：`mod-tome.lua:2879`
- **section**：`mod-tome/data/birth/classes/adventurer.lua`
- **原文**：`#LIGHT_BLUE# * +2 Magic, +2 Willpower, +2 Cunning`
- **译文**：`#LIGHT_BLUE# * +2 魔力，+2 意志，+2 灵巧`
- **结论**：**未发现问题**
- **可核验依据**：三项属性 `魔力`、`意志`、`灵巧` 符合术语规范，格式控制符 `#LIGHT_BLUE#` 与数值均准确保留。

---

### entry-00447
- **位置**：`mod-tome.lua:2880`
- **section**：`mod-tome/data/birth/classes/adventurer.lua`
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# +0`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# +0`
- **结论**：**未发现问题**
- **可核验依据**：角色描述面板生命成长固定格式标签。`#GOLD#` 与 `#LIGHT_BLUE#` 颜色标记、冒号及数值 `+0` 匹配一致。

---

### entry-00448
- **位置**：`mod-tome.lua:2886`
- **section**：`mod-tome/data/birth/classes/adventurer.lua`
- **原文**：`#{bold}##GOLD#This is a bonus class for the chaotically inclined. It is by no means balanced, fun or winnable, it is most of all #{italic}#RANDOM#{bold}#.#WHITE##{normal}#`
- **译文**：`#{bold}##GOLD#这是倾向混乱的奖励职业。显然，他并不平衡，也不保证有趣或者能通关。一切为了 #{italic}#随机#{bold}#。#WHITE##{normal}#`
- **结论**：**细微观察**
- **可核验依据**：
  1. 格式码 `#{bold}##GOLD#` 与 `#{italic}#...#{bold}#.#WHITE##{normal}#` 完整对称。
  2. 译文中“显然，他并不平衡”使用男性人称代词“他”指代“职业（class）”，按中文规范指代物或抽象概念宜使用“它”。
  3. 原文“it is most of all RANDOM”意为“最重要的是/首要特点是随机”，译文“一切为了 随机”语义稍显翻译腔/过度引申，但不影响核心语义传达。

---

### entry-00449
- **位置**：`mod-tome.lua:2888`
- **section**：`mod-tome/data/birth/classes/adventurer.lua`
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# +2`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# +2`
- **结论**：**未发现问题**
- **可核验依据**：流浪者（Wanderer）生命成长数值 `+2`，颜色标记 `#GOLD#` 与 `#LIGHT_BLUE#` 保留完整。

---

### entry-00450
- **位置**：`mod-tome.lua:2889`
- **section**：`mod-tome/data/birth/classes/adventurer.lua`
- **原文**：`#GOLD#As you level up you learn the talent tree: #LIGHT_BLUE#%s`
- **译文**：`#GOLD#在你升级的同时，你学会了新的技能树：#LIGHT_BLUE#%s`
- **结论**：**未发现问题**
- **可核验依据**：固定源码 `adventurer.lua:randventurerLearn` 调用 `game.bignews:say(90, "#GOLD#As you level up you learn the talent tree: #LIGHT_BLUE#%s", tostring(name))`。占位符 `%s` 及其前导颜色码 `#LIGHT_BLUE#` 顺序与位置正确无误。

---

### entry-00451
- **位置**：`mod-tome.lua:2909`
- **section**：`mod-tome/data/birth/classes/afflicted.lua`
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# +2`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# +2`
- **结论**：**未发现问题**
- **可核验依据**：痛苦系（Cursed）生命成长标签，颜色标记与数值 `+2` 准确对应。

---

### entry-00452
- **位置**：`mod-tome.lua:2913`
- **section**：`mod-tome/data/birth/classes/afflicted.lua`
- **原文**：`Stripped of their magic by the dark forces that once served them, they have learned to harness the hatred that burns in their minds.`
- **译文**：`被那些曾经侍奉他们的黑暗力量夺去魔法的他们，开始学习如何驱使他们心头燃烧的憎恨的力量。`
- **结论**：**未发现问题**
- **可核验依据**：固定源码末日使者（Doomed）职业背景描述。句子句式虽稍有长句翻译痕迹，但忠实表达了“黑暗力量夺去其魔法、转而驾驭心头憎恨”的设定。

---

### entry-00453
- **位置**：`mod-tome.lua:2914`
- **section**：`mod-tome/data/birth/classes/afflicted.lua`
- **原文**：`Only time will tell if they can choose a new path or are doomed forever.`
- **译文**：`只有时间会证明他们能否选择一条新的道路，还是永远为厄运所缚。`
- **结论**：**未发现问题**
- **可核验依据**：固定源码末日使者背景描述。原文末尾“doomed forever”双关其职业名称，译文以“永远为厄运所缚”处理得当。

---

### entry-00454
- **位置**：`mod-tome.lua:2920`
- **section**：`mod-tome/data/birth/classes/afflicted.lua`
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# +0`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# +0`
- **结论**：**未发现问题**
- **可核验依据**：末日使者生命成长标签，颜色代码与数值 `+0` 匹配一致。

---

### entry-00455
- **位置**：`mod-tome.lua:2932`
- **section**：`mod-tome/data/birth/classes/celestial.lua`
- **原文**：`Their way of life is well represented by their motto 'The Sun is our giver, our purity, our essence. We carry the light into dark places, and against our strength none shall pass.'`
- **译文**：`他们的生活方式集中体现在他们的座右铭中：太阳是我们的赐予者、我们的纯洁、我们的本质。我们为黑暗带去光明，任何反抗我们的力量都休想通过。`
- **结论**：**细微观察**
- **可核验依据**：固定源码太阳骑士（Sun Paladin）座右铭描述。原文单引号 `'...'` 译文中转换为冒号引出无引号；原文末句“and against our strength none shall pass”核心含义为“在我们的力量面前/面对我们的力量，无人得以通过”，译文“任何反抗我们的力量都休想通过”将 strength 意译成了反抗力量的宾语主体，略有曲解，但不脱离誓言基调。

---

### entry-00456
- **位置**：`mod-tome.lua:2939`
- **section**：`mod-tome/data/birth/classes/celestial.lua`
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# +2`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# +2`
- **结论**：**未发现问题**
- **可核验依据**：太阳骑士生命成长标签，格式与数值 `+2` 匹配一致。

---

### entry-00457
- **位置**：`mod-tome.lua:2941`
- **section**：`mod-tome/data/birth/classes/celestial.lua`
- **原文**：`The balance of the heavens' powers is a daunting task. Mighty are those that stand in the twilight places, wielding both light and darkness in their mind.`
- **译文**：`平衡天空的力量是一件令人望而生畏的任务。强大的是那些驻足于暮光之境的人，心中同时驾驭着光明与黑暗的力量。`
- **结论**：**未发现问题**
- **可核验依据**：安诺瑞希尔（Anorithil）未解锁提示。“twilight places”译为“暮光之境”，“light and darkness”译为“光明与黑暗”，术语与语境准确对应。

---

### entry-00458
- **位置**：`mod-tome.lua:2943`
- **section**：`mod-tome/data/birth/classes/celestial.lua`
- **原文**：`Their way of life is well represented by their motto 'We stand betwixt the Sun and Moon, where light and darkness meet. In the grey twilight we seek our destiny.'`
- **译文**：`他们的生活方式集中体现在他们的座右铭中：我们站在太阳与月亮之间，光暗交替之界。在灰色的黎明中寻找我们的使命。`
- **结论**：**存在疑点**
- **可核验依据**：
  1. 原文为“In the grey twilight we seek our destiny.”，译文作“在灰色的黎明中寻找我们的使命。”将 `twilight` 译为了“黎明”（黎明英文为 dawn）。
  2. 安诺瑞希尔职业核心设定为平衡日与月、光与暗（“where light and darkness meet”），其专属核心技能树即为 `celestial/twilight`（暮光）。在前一条 entry-00457 中，同一文件将“twilight places”正确译为“暮光之境”。
  3. 将 twilight 译为“黎明”既违背天文词义，又与该职业“日落月升、光暗交织之暮色”的核心意象及前文译名相冲突。建议校对为“暮光/微光/暮色”。

---

### entry-00459
- **位置**：`mod-tome.lua:2949`
- **section**：`mod-tome/data/birth/classes/celestial.lua`
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# +0`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# +0`
- **结论**：**未发现问题**
- **可核验依据**：安诺瑞希尔生命成长标签，颜色代码与数值 `+0` 匹配一致。

---

### entry-00460
- **位置**：`mod-tome.lua:2955`
- **section**：`mod-tome/data/birth/classes/chronomancer.lua`
- **原文**：`Some do not walk upon the straight road others follow. Seek the hidden paths outside the normal course of life.`
- **译文**：`有些人并不走他人遵循的坦途。去寻觅常规生命轨迹之外的那些隐秘路径。`
- **结论**：**未发现问题**
- **可核验依据**：时空系（Chronomancer）解锁提示，对应玩家脱离常规路径寻找时空异常的探索设定，译文达意自然。

---

### entry-00461
- **位置**：`mod-tome.lua:2968`
- **section**：`mod-tome/data/birth/classes/chronomancer.lua`
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# +0`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# +0`
- **结论**：**未发现问题**
- **可核验依据**：悖论法师（Paradox Mage）生命成长标签，颜色代码与数值 `+0` 匹配一致。

---

### entry-00462
- **位置**：`mod-tome.lua:2970`
- **section**：`mod-tome/data/birth/classes/chronomancer.lua`
- **原文**：`We preserve the past to protect the future. The hands of time are guarded by the arms of war.`
- **译文**：`我们守护过去，以护佑未来。时间之手由战争之臂守卫。`
- **结论**：**未发现问题**
- **可核验依据**：时空守卫（Temporal Warden）解锁提示。原文中“hands of time”（表针/时间之手）与“arms of war”（兵刃/战争之臂）的双关对比在译文中工整重现。

---

### entry-00463
- **位置**：`mod-tome.lua:2976`
- **section**：`mod-tome/data/birth/classes/chronomancer.lua`
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# +2`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# +2`
- **结论**：**未发现问题**
- **可核验依据**：时空守卫生命成长标签，颜色代码与数值 `+2` 匹配一致。

---

### entry-00464
- **位置**：`mod-tome.lua:2982`
- **section**：`mod-tome/data/birth/classes/corrupted.lua`
- **原文**：`Dark thoughts, black bloods, vile deeds... Those who spill their brethren's blood will find its power.`
- **译文**：`黑暗的思想、黑色的血液、卑鄙的行为……那些倾洒同族之血的人，将发现血的力量。`
- **结论**：**未发现问题**
- **可核验依据**：堕落系（Defiler）解锁提示，省略号 `……` 与句末标点准确，语义贴合残害同族解锁腐化机制的设定。

---

### entry-00465
- **位置**：`mod-tome.lua:2986`
- **section**：`mod-tome/data/birth/classes/corrupted.lua`
- **原文**：`Reavers are terrible foes, charging their enemies with a weapon in each hand.`
- **译文**：`收割者是可怕的对手，他们双手各持一把武器向敌人发起冲锋。`
- **结论**：**未发现问题**
- **可核验依据**：收割者（Reaver）职业描述。术语 `Reaver -> 收割者` 匹配，双持冲锋设定表述准确。

---

### entry-00466
- **位置**：`mod-tome.lua:2987`
- **section**：`mod-tome/data/birth/classes/corrupted.lua`
- **原文**：`They can harness the blight of evil, infecting their foes with terrible contagious diseases while crushing their skulls with devastating combat techniques.`
- **译文**：`他们可以驾驭邪恶的枯萎术，一边将恐怖的传染病散布给敌人，一边以毁灭性的战斗技巧击碎他们的头颅。`
- **结论**：**未发现问题**
- **可核验依据**：固定源码收割者技能树对应 `corruption/plague`（疾病/传染病）与近战技能。术语 `blight -> 枯萎`、`technique -> 技巧` 符合规范。

---

### entry-00467
- **位置**：`mod-tome.lua:2992`
- **section**：`mod-tome/data/birth/classes/corrupted.lua`
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# +2`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# +2`
- **结论**：**未发现问题**
- **可核验依据**：收割者生命成长标签。源码中 `desc` 字符串为 `+2`（虽然底层 `copy_add.life_rating = 1`，但英文字符串本身为 `+2`），译文严格忠实于源字符串与颜色标记。

---

### entry-00468
- **位置**：`mod-tome.lua:2994`
- **section**：`mod-tome/data/birth/classes/corrupted.lua`
- **原文**：`Blight and depravity hold the greatest powers. Accept temptation and become one with corruption.`
- **译文**：`枯萎与堕落蕴藏着最强大的力量。接受诱惑，与腐化融为一体吧。`
- **结论**：**未发现问题**
- **可核验依据**：腐化者（Corruptor）解锁提示。术语 `Blight -> 枯萎`、`depravity -> 堕落`、`corruption -> 腐化` 契合语境，标点正确。

---

### entry-00469
- **位置**：`mod-tome.lua:3001`
- **section**：`mod-tome/data/birth/classes/corrupted.lua`
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# +0`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# +0`
- **结论**：**未发现问题**
- **可核验依据**：腐化者生命成长标签，颜色代码与数值 `+0` 匹配一致。

---

### entry-00470
- **位置**：`mod-tome.lua:3007`
- **section**：`mod-tome/data/birth/classes/mage.lua`
- **原文**：`Mages are the wielders of arcane powers, able to cast powerful spells of destruction or to heal their wounds with nothing but a thought.`
- **译文**：`法师们用奥术魔法来武装自己，只要一闪念就能够释放破坏性的法术或者治疗自己。`
- **结论**：**未发现问题**
- **可核验依据**：法师系（Mage）类别概括描述。`arcane powers` 对应 `奥术魔法/力量`，语义表达顺畅。

---

### entry-00471
- **位置**：`mod-tome.lua:3011`
- **section**：`mod-tome/data/birth/classes/mage.lua`
- **原文**：`They do not use the forbidden arcane arts practised by the mages of old - such perverters of nature have been shunned or actively hunted down since the Spellblaze.`
- **译文**：`他们不使用古代法师所施行的被禁止的奥术——自魔法大爆炸以来，这些扭曲自然的人一直被排斥甚至遭到追捕。`
- **结论**：**未发现问题**
- **可核验依据**：炼金术士（Alchemist）描述。术语快照核对 `Spellblaze -> 魔法大爆炸`、`arcane -> 奥术`、`nature -> 自然`，破折号 `——` 转换规范。

---

### entry-00472
- **位置**：`mod-tome.lua:3018`
- **section**：`mod-tome/data/birth/classes/mage.lua`
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# -1`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# -1`
- **结论**：**未发现问题**
- **可核验依据**：炼金术士生命成长标签，负数数值 `-1` 与颜色标记保留完整。

---

### entry-00473
- **位置**：`mod-tome.lua:3025`
- **section**：`mod-tome/data/birth/classes/mage.lua`
- **原文**：`Most Archmagi have been trained in the secret town of Angolwen and possess a unique spell to teleport to it directly.`
- **译文**：`大多数元素法师在一个名叫安格利文的秘密小镇接受训练，并拥有一个直接传送到那里的独特技能。`
- **结论**：**未发现问题**
- **可核验依据**：固定源码元素法师描述。术语快照严格核对 `Angolwen -> 安格利文`（维护者裁定规范，取代旧称安格列文）、`Archmage -> 元素法师`，设定机制对应技能 `T_TELEPORT_ANGOLWEN`，翻译准确。

---

### entry-00474
- **位置**：`mod-tome.lua:3029`
- **section**：`mod-tome/data/birth/classes/mage.lua`
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# -4`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# -4`
- **结论**：**未发现问题**
- **可核验依据**：元素法师生命成长标签，负数数值 `-4` 与颜色标记保留完整。

---

### entry-00475
- **位置**：`mod-tome.lua:3034`
- **section**：`mod-tome/data/birth/classes/mage.lua`
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# -3`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# -3`
- **结论**：**未发现问题**
- **可核验依据**：死灵法师（Necromancer）生命成长标签，负数数值 `-3` 与颜色标记保留完整。

---

### entry-00476
- **位置**：`mod-tome.lua:3046`
- **section**：`mod-tome/data/birth/classes/psionic.lua`
- **原文**：`Weakness of flesh can be overcome by mental prowess. Find the way and fight for the way to open the key to your mind.`
- **译文**：`肉体的软弱可以被精神的强大所克服。寻找道路，并为之奋战，以打开通往你精神世界的钥匙。`
- **结论**：**细微观察**
- **可核验依据**：
  1. 固定源码中该句为灵能系（Psionic）职业类别的未解锁提示文本（`locked_desc`）。在游戏设定中，解锁灵能系的方法是在霍夫灵废墟（Ruined Halfling Complex）中协助拯救伊克族维网行者（Yeek Wayist）。
  2. 英文中“Find the way and fight for the way”是一语双关的线索，既指“寻找道路/方法”，又暗指伊克族的社会与信仰核心“维网（The Way）”（术语快照收录 `The Way -> 维网`）。译文将其直译为“寻找道路，并为之奋战”，使得向玩家提示“维网”阵营的指引线索失落。
  3. 后半句“open the key to your mind”被翻译为“以打开通往你精神世界的钥匙”，在汉语搭配上存在“打开……钥匙”的动宾不搭配问题（通常为“找到……的钥匙”或“用钥匙打开……大门”）。

---

### entry-00477
- **位置**：`mod-tome.lua:3049`
- **section**：`mod-tome/data/birth/classes/psionic.lua`
- **原文**：`A thought can inspire; a thought can kill. After centuries of oppression, years of imprisonment, a thought shall break us free and vengeance will strike from our darkest dreams.`
- **译文**：`思想可以鼓舞人，思想也能杀人。历经数个世纪的压迫、数年的囚禁，一个念头终将使我们挣脱束缚，而复仇将从我们最黑暗的梦境中降临。`
- **结论**：**未发现问题**
- **可核验依据**：心灵杀手（Mindslayer）未解锁提示，贴合伊克族历经数百年奴役后觉醒灵能挣脱囚禁的背景历史。语义、语气与标点匹配准确。

---

### entry-00478
- **位置**：`mod-tome.lua:3056`
- **section**：`mod-tome/data/birth/classes/psionic.lua`
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# -2`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# -2`
- **结论**：**未发现问题**
- **可核验依据**：心灵杀手生命成长标签，负数数值 `-2` 与颜色标记保留完整。

---

### entry-00479
- **位置**：`mod-tome.lua:3061`
- **section**：`mod-tome/data/birth/classes/psionic.lua`
- **原文**：`This knowledge comes with a heavy price and the Solipsist must guard his thoughts, lest he come to believe that the world exists only within his own mind.`
- **译文**：`使用此理论需要付出巨大的代价，织梦者必须对自己的思维有很强的控制力，否则他会渐渐相信这世界只存在于他自己的心智之中。`
- **结论**：**未发现问题**
- **可核验依据**：织梦者（Solipsist）背景描述。术语 `Solipsist -> 织梦者` 对应正确，对于“唯我论”哲学侵蚀心智的背景机制意译得当。

---

### entry-00480
- **位置**：`mod-tome.lua:3064`
- **section**：`mod-tome/data/birth/classes/psionic.lua`
- **原文**：`#GOLD#Life per level:#LIGHT_BLUE# -4 (*special*)`
- **译文**：`#GOLD#每等级生命加值：#LIGHT_BLUE# -4 (*特殊*)`
- **结论**：**未发现问题**
- **可核验依据**：固定源码中织梦者生命成长附带 `(*special*)` 注解（因为其机制通过核心技能将部分生命伤害转换为灵能值承受）。特殊标注 `(*特殊*)`、数值 `-4` 与颜色代码均完整匹配。

---

#### 3. 疑点与观察汇总清单

| 条目编号 | 类型 | 核心事实依据与现象 |
| :--- | :--- | :--- |
| **entry-00443** | 细微观察 | 原文 `cold damage` 译为 `冰冷伤害`。根据固定源码 `damage_types.lua`，该成就直接检测系统注册的 `cold` 伤害类型，规范译名应为 `寒冷`（寒冷伤害）。本条与规范伤害名称存在细微不一致。 |
| **entry-00448** | 细微观察 | 原文 `It is by no means balanced...` 指代职业（class），译文使用代词“他”；“most of all”意为“最重要的是/首要的是”，译文作“一切为了”。格式代码完全保留。 |
| **entry-00455** | 细微观察 | 原文“against our strength none shall pass”（面对我们的力量，无人得以通过）被译为“任何反抗我们的力量都休想通过”，对介词短语的语义理解略有偏差。英文单引号被替换为冒号引出。 |
| **entry-00458** | **存在疑点** | 原文“In the grey twilight we seek our destiny.”被误译为“在灰色的黎明中寻找我们的使命。”。`twilight`（暮光/微光/薄暮）被误译为黎明（dawn），与安诺瑞希尔平衡光暗的天文背景、专属技能树名称 `twilight` 及前文（entry-00457）中对“twilight places”的正确译法“暮光之境”产生实质冲突。 |
| **entry-00476** | 细微观察 | 原文“Find the way and fight for the way to open the key to your mind.”中，“the way”双关暗指灵能系解锁关键阵营“维网（The Way）”，直译为“寻找道路”使得双关解谜线索消失；且“打开通往……钥匙”存在中文动宾搭配瑕疵。 |