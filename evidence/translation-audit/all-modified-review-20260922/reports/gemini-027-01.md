# 译文复核报告：batch-027（条目 entry-01044 至 entry-01083）

### 校验与复核基准
- **文件校验**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-027.md`
  - 冻结 SHA-256：`c6c624aa2e0cad73afb092a3e864270122003ae0343681a9ca8257298e9d75c4`（核对一致）
- **公开源码基准**：
  - engine / tome 固定 commit：`624a67329fe2ad440c5b344785a9c73fcf22ae63`
  - 源码路径：`game/modules/tome/data/general/objects/world-artifacts.lua`
- **译文版本基准**：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`（`mod-tome.lua` 行 12679 ～ 12876）

---

### 逐条复核详情（共 40 条）

#### entry-01044
- **位置**：`mod-tome.lua:12679`（`SCALE_MAIL_KROLTAR`）
- **原文**：`A heavy shirt of scale mail constructed from the remains of Kroltar, whose armour was like tenfold shields.`
- **译文**：`一件用库洛塔的遗骸打造的厚重鳞甲，他的护甲坚如十重盾牌。`
- **复核结论**：未发现问题
- **可核验依据**：源码第 1775 行。无占位符或格式标记；“whose armour was like tenfold shields”引用经典典故，译文“他的护甲坚如十重盾牌”表意准确，标点完整对应。

#### entry-01045
- **位置**：`mod-tome.lua:12690`（`URESLAK_FEMUR`）
- **原文**：`a strangely colored bone`
- **译文**：`一根颜色奇异的骨头`
- **复核结论**：未发现问题
- **可核验依据**：源码第 1885 行未鉴定名（`unided_name`）。译文直截准确，无特殊格式。

#### entry-01046
- **位置**：`mod-tome.lua:12692`（`URESLAK_FEMUR`）
- **原文**：`10% chance to shimmer to a different hue and gain powers`
- **译文**：`10% 几率闪烁变换成不同色调并获得相应能力`
- **复核结论**：未发现问题
- **可核验依据**：源码第 1900 行 `special_on_hit.desc`。机制为命中时 10% 几率随机切换骨杖的元素形态（火/冰/电/毒/群星/奥术）并赋予对应属性加成。译文与游戏机制完全一致。

#### entry-01047
- **位置**：`mod-tome.lua:12694`（`URESLAK_FEMUR`）
- **原文**：`#GOLD#Ureslak's Femur glows and shimmers!`
- **译文**：`#GOLD#乌尔斯拉克的股骨发出闪光！`
- **复核结论**：未发现问题
- **可核验依据**：源码第 1911 行 `game.logSeen`。颜色标记 `#GOLD#` 正确保留，感叹号匹配；译文将“glows and shimmers”整合译为“发出闪光”，语义在日志语境中通顺达意。

#### entry-01048
- **位置**：`mod-tome.lua:12706`（`URESLAK_CLOAK`）
- **原文**：`, or `
- **译文**：`或 `
- **复核结论**：未发现问题
- **可核验依据**：源码第 1989 行，用于 `table.concatNice` 构建抗性列表的末尾连接符。中文语境省略前置逗号、保留后置空格符合中文排版习惯。

#### entry-01049
- **位置**：`mod-tome.lua:12707`（`URESLAK_CLOAK`）
- **原文**：`%s empowers %s %s!`
- **译文**：`%s充能了%s%s！`
- **复核结论**：未发现问题
- **可核验依据**：源码第 1994 行 `game.logSeen(who, "%s empowers %s %s!", who:getName():capitalize(), who:his_her(), self:getName(...))`。三个 `%s` 分别接收角色名、物主代词、带颜色物品名，译文占位符数量、类型及排列顺序完全匹配。

#### entry-01050
- **位置**：`mod-tome.lua:12716`（`ART_PAIR_TWSWORD`）
- **原文**：`Sword of Potential Futures`
- **译文**：`可能未来之剑`
- **复核结论**：未发现问题
- **可核验依据**：源码第 2050 行物品实体名。与配对匕首“往昔之匕（Dagger of the Past）”双关呼应，译名准确。

#### entry-01051
- **位置**：`mod-tome.lua:12718`（`ART_PAIR_TWSWORD`）
- **原文**：`Legend has it this blade is one of a pair: twin blades forged in the earliest of days of the Wardens. To an untrained wielder it is less than perfect; to a Warden, it represents the untapped potential of time.`
- **译文**：`传说这把长剑是一对兵器中的其中一个；这对兵器打造于时空守卫最初的年代。对于未经训练的持有者来说它还不是那么完善；对于时空守卫来说，它代表着时间尚未开发的潜能。`
- **复核结论**：未发现问题
- **可核验依据**：源码第 2054 行物品描述。Wardens 准确对应职业“时空守卫”，分号与句号断句对应准确，文意流畅。

#### entry-01052
- **位置**：`mod-tome.lua:12719`（`ART_PAIR_TWSWORD`）
- **原文**：`In the past there was a dagger with it.`
- **译文**：`过去有柄匕首和它成套。`
- **复核结论**：未发现问题
- **可核验依据**：源码第 2080 行 `set_desc`。用于提示配对副手匕首（Dagger of the Past），句意准确。

#### entry-01053
- **位置**：`mod-tome.lua:12726`（`ART_PAIR_TWDAG`）
- **原文**：`Potentially it would go with a sword in the future.`
- **译文**：`未来可能有把剑和它成套。`
- **复核结论**：未发现问题
- **可核验依据**：源码第 2128 行 `set_desc`。双关提示配对主手长剑（Sword of Potential Futures），传译准确。

#### entry-01054
- **位置**：`mod-tome.lua:12729`（`Stone Gauntlets of Harkor'Zun`）
- **原文**：`dark stone gauntlets`
- **译文**：`黑石臂铠`
- **复核结论**：未发现问题
- **可核验依据**：源码第 2161 行未鉴定名。gauntlets 对应“臂铠”，dark stone 译为“黑石”，符合规范。

#### entry-01055
- **位置**：`mod-tome.lua:12740`（`Quiver of the Sun`）
- **原文**：`This strange orange quiver is made of brass and etched with many bright red runes that glow and glitter in the light.  The arrows themselves appear to be solid shafts of blazing hot light, like rays of sunshine, hammered and forged into a solid state.`
- **译文**：`这个奇特的橙色箭壶由黄铜制成，在阳光下，你可以看到壶身铭刻着许多亮红色的发光符文。箭矢本身仿佛就是炽热光芒凝成的实体箭杆，如同阳光被锤炼锻造成了固态。`
- **复核结论**：未发现问题
- **可核验依据**：源码第 2243 行物品描述。无特殊控制符，叙述生动，文意完整。

#### entry-01056
- **位置**：`mod-tome.lua:12750`（`Blightstopper`）
- **原文**：`%s is purged of diseases!`
- **译文**：`%s 除去了疾病！`
- **复核结论**：未发现问题
- **可核验依据**：源码第 2415 行 `game.logSeen(who, "%s is purged of diseases!", who:getName():capitalize())`。`%s` 占位符与感叹号对应，机制为使用者被净化身上的疾病，语义清晰。

#### entry-01057
- **位置**：`mod-tome.lua:12758`（`Nexus of the Way`）
- **原文**：`The vast psionic force of the Way reverberates through this gemstone. With a single touch, you can sense overwhelming power, and hear countless thoughts.`
- **译文**：`维网的庞大灵能力量在这颗宝石之中回响。只需轻轻一触，你就能感受到压倒性的力量，听见无数的思绪。`
- **复核结论**：未发现问题
- **可核验依据**：源码第 2543 行物品描述。The Way 准确对应术语“维网”，psionic force 对应“灵能力量”，语句自然流畅。

#### entry-01058
- **位置**：`mod-tome.lua:12767`（`SET_SCEPTRE_LICH`）
- **原文**：`This sceptre, carved of ancient, blackened bone, holds a single gem of deep obsidian. You feel a dark power from deep within, looking to get out.`
- **译文**：`这根权杖以古老的焦黑骨骼雕刻而成，镶嵌着一颗深邃的黑曜石。你感受到内部深处有一股黑暗力量呼之欲出。`
- **复核结论**：未发现问题
- **可核验依据**：源码第 2643 行物品描述。“looking to get out”译为“呼之欲出”，传神贴切，标点对应。

#### entry-01059
- **位置**：`mod-tome.lua:12768`（`SET_SCEPTRE_LICH`）
- **原文**：`#LIGHT_BLUE#You feel the power of the sceptre flow over your undead form!`
- **译文**：`#LIGHT_BLUE#你感到权杖的力量流过你的亡灵之躯！`
- **复核结论**：未发现问题
- **可核验依据**：源码第 2668 行 `game.logPlayer`。`#LIGHT_BLUE#` 颜色标记完整保留，undead 译为“亡灵”，感叹号对应。

#### entry-01060
- **位置**：`mod-tome.lua:12772`（`Oozing Heart`）
- **原文**：`This mindstar oozes a thick, caustic liquid. Magic seems to die around it.`
- **译文**：`这只灵晶在不断的向外渗出粘稠的腐蚀性液体。魔法似乎消逝在它周围。`
- **复核结论**：未发现问题
- **可核验依据**：源码第 2714 行物品描述。mindstar 统一为“灵晶”，反魔机制表述准确。

#### entry-01061
- **位置**：`mod-tome.lua:12797`（`Emblem of Evasion`）
- **原文**：`gold coated emblem`
- **译文**：`镀金的徽记`
- **复核结论**：未发现问题
- **可核验依据**：源码第 2997 行未鉴定名。准确。

#### entry-01062
- **位置**：`mod-tome.lua:12801`（`Surefire`）
- **原文**：`This tightly strung bow appears to have been crafted by someone of considerable talent. When you pull the string, you feel incredible power behind it.`
- **译文**：`这把弓弦绷紧的弓看起来出自一位技艺高超者之手。当你拉动弓弦时，你能感受到蕴藏其中的惊人力量。`
- **复核结论**：未发现问题
- **可核验依据**：源码第 3016 行物品描述。语句流畅自然，标点对应。

#### entry-01063
- **位置**：`mod-tome.lua:12810`（`Stormlash`）
- **原文**：`The storm is on your side !`
- **译文**：`风暴协助了你！`
- **复核结论**：未发现问题
- **可核验依据**：源码第 3091 行暴击触发有益飓风效果时的日志。感叹号保留，语义准确。

#### entry-01064
- **位置**：`mod-tome.lua:12812`（`Stormlash`）
- **原文**：`strike an enemy within range %d (for 100%% weapon damage as lightning) and release a radius %d burst of electricity dealing %0.2f to %0.2f lightning damage (based on Magic and Dexterity)`
- **译文**：`攻击距离 %d 内的敌人，造成 100%% 闪电武器伤害并在半径 %d 内释放电弧，造成 %0.2f 到 %0.2f 点闪电伤害（基于魔法和敏捷）`
- **复核结论**：未发现问题
- **可核验依据**：源码第 3103 行主动技能描述。占位符包含 `%d`（射程）、`100%%`（武器伤害百分比）、`%d`（爆炸半径）、`%0.2f`（下限伤害）、`%0.2f`（上限伤害）。译文中 5 个占位符类型、顺序与转义完全一致，术语“闪电伤害”、“魔法和敏捷”正确。

#### entry-01065
- **位置**：`mod-tome.lua:12815`（`Focus Whip`）
- **原文**：`gemmed whip handle`
- **译文**：`镶有宝石的鞭柄`
- **复核结论**：未发现问题
- **可核验依据**：源码第 3137 行未鉴定名。准确。

#### entry-01066
- **位置**：`mod-tome.lua:12816`（`Focus Whip`）
- **原文**：`A small mindstar rests at top of this handle. As you touch it, a translucent cord appears, flicking with your will.`
- **译文**：`这只手柄上镶有一颗小小的灵晶。当你触摸它时，一根半透明的绳索浮现出来，随着你的意念抽动挥摆。`
- **复核结论**：未发现问题
- **可核验依据**：源码第 3139 行物品描述。灵晶及具现化灵能鞭细节传译准确。

#### entry-01067
- **位置**：`mod-tome.lua:12820`（`Focus Whip`）
- **原文**：`#Source# manifests a psychic assult with %s %s!`
- **译文**：`#Source#使用%s%s发动心灵攻击！`
- **复核结论**：未发现问题
- **可核验依据**：源码第 3172 行 `who:logCombat(target, "#Source# manifests a psychic assult with %s %s!", who:his_her(), self:getName(...))`。两处 `%s` 分别为物主代词与物品名，中文如“使用他的聚灵鞭发动心灵攻击！”，占位符与日志标签 `#Source#` 匹配无误。

#### entry-01068
- **位置**：`mod-tome.lua:12825`（`Latafayn`）
- **原文**：`%s's %s lashes out in a flaming arc, intensifying the burning of %s enemies!`
- **译文**：`%s的%s划出一条烈焰的弧线，加速了%s个敌人身上的燃烧！`
- **复核结论**：存在疑点
- **可核验依据**：
  1. 查阅源码第 3244 行日志调用：
     `game.logSeen(who, "%s's %s lashes out in a flaming arc, intensifying the burning of %s enemies!", who:getName():capitalize(), self:getName({do_color = true, no_add_name = true}), who:his_her())`
  2. 第三个参数传入的是物主代词 `who:his_her()`（即“他的”或“她的”），代表“intensifying the burning of [his/her] enemies”（加剧其敌人身上的燃烧），而非敌人数量！
  3. 现有译文误将 `%s enemies` 当作敌人数量计数，翻译为“加速了`%s个敌人`身上的燃烧！”，导致运行时实际输出为：“……加速了**他的个敌人**身上的燃烧！”或“……加速了**她的个敌人**身上的燃烧！”，出现多余量词“个”和明显的语法硬伤。

#### entry-01069
- **位置**：`mod-tome.lua:12828`（`Robe of Force`）
- **原文**：`This thin cloth robe is surrounded by a pulsating shroud of telekinetic force.`
- **译文**：`这件薄薄的布袍被一层搏动的念动力护罩所包围。`
- **复核结论**：未发现问题
- **可核验依据**：源码第 3281 行物品描述。词义与标点准确对应。

#### entry-01070
- **位置**：`mod-tome.lua:12830`（`Robe of Force`）
- **原文**：`%s focuses a beam of force from %s %s!`
- **译文**：`%s从%s%s中发出动能射线！`
- **复核结论**：未发现问题
- **可核验依据**：源码第 3314 行 `game.logSeen(who, "%s focuses a beam of force from %s %s!", who:getName():capitalize(), who:his_her(), self:getName(...))`。三个 `%s` 顺序对应人物、物主代词和装备名，感叹号保留。

#### entry-01071
- **位置**：`mod-tome.lua:12836`（`Corpathus`）
- **原文**：`Thick straps encircle this blade. Jagged edges like teeth travel down the blade, bisecting it. It fights to overcome the straps, but lacks the strength.`
- **译文**：`厚重的革带紧缚着这把剑。锯齿般的锋刃沿着剑身纵贯而下，将其一分为二。它试图挣脱革带的束缚，但似乎缺乏足够的力量。`
- **复核结论**：未发现问题
- **可核验依据**：源码第 3399 行物品描述。叙述生动贴切，标点准确对应。

#### entry-01072
- **位置**：`mod-tome.lua:12844`（`Anmalice`）
- **原文**：`The eye on the hilt of this blade seems to glare at you, piercing your soul and mind. Tentacles surround the hilt, latching onto your hand.`
- **译文**：`这柄剑护手上的眼睛怒视着你，洞穿你的灵魂与心智。触须缠绕着剑柄，攀附在你的手上。`
- **复核结论**：未发现问题
- **可核验依据**：源码第 3500 行物品描述。翻译准确流畅，分句与标点对应。

#### entry-01073
- **位置**：`mod-tome.lua:12852`（`Morrigor`）
- **原文**：`jagged, segmented, sword`
- **译文**：`锯齿分节的剑`
- **复核结论**：未发现问题
- **可核验依据**：源码第 3595 行未鉴定名。准确。

#### entry-01074
- **位置**：`mod-tome.lua:12857`（`Morrigor`）
- **原文**：`@Source@ taps the #SALMON#trapped soul#LAST# of %s, xmanifesting %s!`
- **译文**：`@Source@放出了%s#SALMON#被束缚的灵魂#LAST#，模仿了%s！`
- **复核结论**：细微观察
- **可核验依据**：
  1. 源码第 3644 行 `o.use_talent.message = ("@Source@ taps the #SALMON#trapped soul#LAST# of %s, xmanifesting %s!"):tformat(target:getName(), o.use_talent.name)`。
  2. 格式与标记：`@Source@`、`#SALMON#...#LAST#`、两处 `%s` 以及感叹号均正确对应，运行时能正常填充受害者名称与偷取技能名。
  3. 语义细节观察：莫瑞格剑机制为击杀敌人后将其灵魂吞噬拘禁并获得其主动技能；使用该技能时英文原文为“taps the trapped soul of %s, xmanifesting %s!”（调取引导受害者的被困之魂，展现出技能）。译文处理为“放出了……被束缚的灵魂，模仿了……”，其中“放出”容易在中文语境下误导为灵魂已解脱释放（实际仍在剑中拘禁），“xmanifesting”（显化/展现）处理为“模仿了”略偏。但因格式健全且大意通顺，归为细微观察。

#### entry-01075
- **位置**：`mod-tome.lua:12861`（`Hydra's Bite`）
- **原文**：`This three-headed stralite flail strikes with the power of a hydra. With each attack it lashes out, hitting everyone around you.`
- **译文**：`这把三头的斯莱特连枷，使用的是一只三头龙的力量。它的攻击可以伤害到周围的所有敌人。`
- **复核结论**：未发现问题
- **可核验依据**：源码第 3671 行物品描述。stralite 符合术语快照“斯莱特”；武器名 Hydra's Bite 译为“三头龙之牙”（因该连枷有 3 头且附带 3 种龙息），描述将 hydra 译为“三头龙”保持了一致性。

#### entry-01076
- **位置**：`mod-tome.lua:12862`（`Hydra's Bite`）
- **原文**：`hit up to two adjacent enemies`
- **译文**：`攻击你身边最多 2 个相邻敌人`
- **复核结论**：未发现问题
- **可核验依据**：源码第 3684 行 `special_on_hit.desc`。机制为攻击时对主目标之外额外至多 2 个相邻敌对目标造成打击，译文准确。

#### entry-01077
- **位置**：`mod-tome.lua:12863`（`Hydra's Bite`）
- **原文**：`#Source#'s three headed flail lashes at #Target#%s!`
- **译文**：`#Source#使用三头连枷打击#Target#%s！`
- **复核结论**：未发现问题
- **可核验依据**：源码第 3706 行双目标命中日志。`%s` 接收同文件 12864 行的 `(" and %s"):tformat(...)`（“和 %s”）。战斗日志标签 `#Source#`、`#Target#` 及占位符与感叹号完整匹配。

#### entry-01078
- **位置**：`mod-tome.lua:12865`（`Hydra's Bite`）
- **原文**：`#Source#'s three headed flail lashes at #Target#!`
- **译文**：`#Source#的三头连枷扫过了 #Target#！`
- **复核结论**：未发现问题
- **可核验依据**：源码第 3708 行单目标命中日志。标签与感叹号完整保留。（注：与 01077 相比句式从“使用……打击”变为“的三头连枷扫过了”，存在风格细微不一致，但完全不影响功能与阅读）。

#### entry-01079
- **位置**：`mod-tome.lua:12868`（`GAUNTLETS_SPELLHUNT` 基础形态）
- **原文**：`These once brilliant voratun gauntlets have fallen into a deep decay. Originally used in the spellhunt, they were often used to destroy arcane artifacts, curing the world of their influence.`
- **译文**：`这副曾经辉煌的沃瑞钽臂铠已经严重朽坏。它最初在魔法狩猎中使用，常被用于摧毁奥术类装备，以消除它们对世界的影响。`
- **复核结论**：未发现问题
- **可核验依据**：源码第 3723 行物品描述。voratun 对应“沃瑞钽”，spellhunt 对应“魔法狩猎”，arcane 对应“奥术”，完整忠实于原文。

#### entry-01080
- **位置**：`mod-tome.lua:12870`（`GAUNTLETS_SPELLHUNT`）
- **原文**：`#ORCHID#Your arcane equipment or powers conflict with the gauntlets!#LAST#`
- **译文**：`#ORCHID#你的奥术装备或能力和臂铠发生了冲突！#LAST#`
- **复核结论**：未发现问题
- **可核验依据**：源码第 3737 行装备冲突日志。`#ORCHID#` 与 `#LAST#` 颜色标记闭合完整，感叹号匹配，术语准确。

#### entry-01081
- **位置**：`mod-tome.lua:12872`（`GAUNTLETS_SPELLHUNT` 2 级形态）
- **原文**：`These once brilliant voratun gauntlets appear heavily decayed. Originally used in the spellhunt, they were often used to destroy arcane artifacts, ridding the world of their influence.`
- **译文**：`这件沃瑞钽臂铠看起来十分破旧。它最初在魔法狩猎中使用，常被用于摧毁奥术类装备，以消除它们对世界的影响。`
- **复核结论**：存在疑点
- **可核验依据**：
  1. 源码第 3773 行。第一句原文为 `These once brilliant voratun gauntlets appear heavily decayed.`。
  2. 对比 entry-01079（1 级）：`These once brilliant voratun gauntlets have fallen into a deep decay.` -> 译为 `这副曾经辉煌的沃瑞钽臂铠已经严重朽坏。`。
  3. 在 entry-01081 中，原文明确保留了修饰成分 `once brilliant`（曾经辉煌的 / 曾经璀璨的），但译文完全遗漏了该短语，仅翻译为“这件沃瑞钽臂铠看起来十分破旧”，属于原文修饰成分缺失；且 `heavily decayed`（重度腐朽/严重朽坏）被大幅弱化为“十分破旧”，削弱了该神器随吞噬装备逐级修复（朽坏 -> 损伤 -> 磨损 -> 闪耀）的文本递进层次感。

#### entry-01082
- **位置**：`mod-tome.lua:12874`（`GAUNTLETS_SPELLHUNT` 3 级形态）
- **原文**：`These voratun gauntlets appear to have suffered considerable damage. Originally used in the spellhunt, they were often used to destroy arcane artifacts, ridding the world of their influence.`
- **译文**：`这件沃瑞钽臂铠曾经受到过可观的损伤。它最初在魔法狩猎中使用，常被用于摧毁奥术类装备，以消除它们对世界的影响。`
- **复核结论**：未发现问题
- **可核验依据**：源码第 3801 行物品描述。术语与句意完整准确，层次递进清晰。

#### entry-01083
- **位置**：`mod-tome.lua:12876`（`GAUNTLETS_SPELLHUNT` 4 级形态）
- **原文**：`These voratun gauntlets shine brightly beneath a thin layer of wear. Originally used in the spellhunt, they were often used to destroy arcane artifacts, ridding the world of their influence.`
- **译文**：`这件沃瑞钽臂铠虽然有一些使用痕迹，仍然闪耀着光芒。它最初在魔法狩猎中使用，常被用于摧毁奥术类装备，以消除它们对世界的影响。`
- **复核结论**：未发现问题
- **可核验依据**：源码第 3829 行物品描述。“shine brightly beneath a thin layer of wear”转化流畅贴切，标点与术语均准确无误。

---

### 疑点与观察汇总列表

| 条目编号 | 严重程度 | 涉及字段/机制 | 核心证据与简要说明 |
| :--- | :--- | :--- | :--- |
| **entry-01068** | **存在疑点** | `Latafayn` 日志占位符语义与格式 | 源码第 3244 行调用 `game.logSeen(who, ..., who:his_her())`，第三个参数是角色物主代词而非敌人数量。译文误译为 `%s个敌人`，运行时将拼接产生“他的个敌人”/“她的个敌人”语法硬伤。 |
| **entry-01081** | **存在疑点** | `GAUNTLETS_SPELLHUNT` 2 级描述漏译 | 原文 `These once brilliant voratun gauntlets appear heavily decayed.` 漏译了 `once brilliant`（曾经辉煌的），并将 `heavily decayed`（严重朽坏）弱化为“十分破旧”，破坏了神器逐级修复的文本递进体系。 |
| **entry-01074** | **细微观察** | `Morrigor` 偷取技能触发日志语义 | 原文 `taps the trapped soul of %s, xmanifesting %s!` 译为“放出了……被束缚的灵魂，模仿了……”，字面上与灵魂仍在剑中受困并被调取力量显化技能的机制设定略有出入，但控制标记健全。 |