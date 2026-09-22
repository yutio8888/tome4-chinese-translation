# batch-080 只读译文复核报告

- **工作区**：`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921`
- **复核批次**：`batch-080.md`（共 40 条：`entry-02572` 至 `entry-02611`）
- **文件校验**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-080.md` SHA-256 为 `a9eafab3804f68dc58012273a85f21aee52b6376451dcc80a3f087b8963f7d63`，核验一致。
- **源码依据**：ToME 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（`game/modules/tome/`）；译文语境基准 `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00:mod-tome.lua`。

---

### entry-02572
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-paladin_fallen.lua:23`。原文 `#LIGHT_GREEN#Fallen (Sun Paladin)` 译为 `#LIGHT_GREEN#堕落者（太阳骑士）`，职业进阶与职业名称均符合术语规范，开放颜色控制符 `#LIGHT_GREEN#` 保持原样无闭合缺失。

### entry-02573
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-psionic_mindslayer.lua:23`。原文 `Mindslayer (Psionic)` 译为 `心灵杀手（灵能系）`，职业分类与系别名称规范，颜色码 `#LIGHT_GREEN#` 正确。

### entry-02574
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-psionic_mindslayer.lua:24`。颜色标记 `#LIGHT_GREEN#心灵杀手#WHITE#` 与 `#YELLOW#...#WHITE#` 成对闭合完整，空行和换行结构对应完整；机制描述中将护盾/光环的 “spiking them in great bursts of power” 译为 “过载”，准确贴合心灵杀手护盾过载（Spike）技能机制。

### entry-02575
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-psionic_solipsist.lua:23`。原文 `Solipsist (Psionic)` 译为 `织梦者（灵能系）`，符合职业及系别统一术语，颜色码保留无误。

### entry-02576
- **状态**：细微观察
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-psionic_solipsist.lua:24`。
  1. 机制描述“Convert damage you take into Psi damage”译为“将你受到的伤害转化为灵能值损失”，准确体现唯我论扣除灵能代替扣血的机制；颜色码成对完整。
  2. 观察发现：原文倒数第二段首句为 `Solipsists use their mind to manipulate the world around them.`，译文重复了前一段首句的译法“织梦者利用思想和梦境的力量掌控身边的天地。”，将 `their mind` 译作“思想和梦境的力量”；此外正文解锁行“选择新的职业 #LIGHT_GREEN#织梦者#WHITE#”较其他解锁条目省略了冒号，列表最后一项带句号而前四项无句号。均不影响游戏机制理解。

### entry-02577
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-race_ogre.lua:24`。叙事中 `Allure Wars`（厄流战争）、`Spellhunt`（魔法狩猎）、`Conclave`（孔克雷夫）、`inscriptions`（刻印）、`runes and infusions`（纹身和符文）等专名与机制术语均准确对应，颜色控制符 `#LIGHT_GREEN#...#WHITE#` 与 `#YELLOW#...#WHITE#` 匹配完整。

### entry-02578
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-rogue_marauder.lua:23`。原文 `Marauder (Rogue)` 译为 `掠夺者（盗贼系）`，术语一致，颜色码完整。

### entry-02579
- **状态**：细微观察
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-rogue_marauder.lua:24`。
  1. 颜色标记 `#LIGHT_GREEN#掠夺者#WHITE#` 及 `#YELLOW#...#WHITE#` 匹配，核心机制描述完整准确。
  2. 观察发现：原文中 `Class features:#YELLOW#` 紧接在上一句末尾未换行，译文将其单独换行作为新行，视觉结构更整齐；正文中“选择新的职业 #LIGHT_GREEN#掠夺者#WHITE#”省略了冒号。

### entry-02580
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-rogue_poisons.lua:23`。原文 `New Talent Category: #LIGHT_GREEN#Poisons` 译为 `新的技能树：#LIGHT_GREEN#毒素系`，颜色码与技能分类术语准确。

### entry-02581
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-undead_ghoul.lua:24`。原文 `Ghoul (Undead)` 译为 `食尸鬼（不死亡灵）`，种族术语与颜色码准确。

### entry-02582
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-undead_ghoul.lua:25`。技能列表 `ghoulish leap, gnaw and retch` 译为 `食尸鬼跳跃、啃噬和腐秽呕吐`，与 `game/modules/tome/data/talents/undeads/ghoul.lua` 中技能在游戏翻译库中的实际显示名完全一致；颜色码与段落结构无误。

### entry-02583
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-undead_skeleton.lua:24`。原文 `Skeleton (Undead)` 译为 `骷髅（不死亡灵）`，种族术语准确，颜色码保留一致。

### entry-02584
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-undead_skeleton.lua:25`。技能列表 `bone armour, resilient bones, re-assemble` 译为 `骨质盔甲，弹力骨骼，重组`，各项抗性及无呼吸特性与游戏实际种族机制一致，颜色码成对闭合。

### entry-02585
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-wanderer.lua:23`。原文 `New Class: #LIGHT_GREEN#Wanderer` 译为 `新职业：#LIGHT_GREEN#流浪者`，颜色码与职业名一致。

### entry-02586
- **状态**：细微观察
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-wanderer.lua:24`。
  1. 颜色码与排版格式：`#LIGHT_GREEN#流浪者#WHITE#` 成对无误；首句妥善处理了原文 DarkGod 英文原稿的语法笔误（`wanderer quite a lot`）。
  2. 观察发现：译文中 `#{bold}# 奖励 #{normal}#` 在格式标签内外均引入了空格，导致在游戏文本解析后“奖励”两端出现额外空格；另外“每升五级”与“每升10级”存在数字全角汉字与阿拉伯数字书写不一致。

### entry-02587
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-warrior_brawler.lua:23`。原文 `Brawler (Warrior)` 译为 `格斗家（战士系）`，符合职业分类术语，颜色码正确。

### entry-02588
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-warrior_brawler.lua:24`。机制末句中 “cannot perform their unarmed talents in massive armor” 译为 “身穿板甲时无法施展徒手技能”，准确对应格斗家徒手技能在代码中检测 `massive_armor` 禁用的机制；颜色码与换行均无误。

### entry-02589
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-wilder_oozemancer.lua:23`。原文 `Oozemancer (Wilder)` 译为 `软泥使（野性系）`，职业及系别术语统一，颜色码完整。

### entry-02590
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-wilder_oozemancer.lua:24`。失衡值（Equilibrium）、反魔（antimagic）、元素法师（archmagi）译法贴切，机制说明准确，颜色标签匹配完整。

### entry-02591
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-wilder_stone_warden.lua:23`。原文 `Stone Warden (Wilder)` 译为 `岩石守卫（野性系）`，术语一致，颜色码完整。

### entry-02592
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-wilder_stone_warden.lua:24`。双持盾牌、分身、岩石藤蔓及法力值（Mana）双能量机制描述与代码完全一致，颜色标签 `#LIGHT_GREEN#...#WHITE#` 及 `#YELLOW#...#WHITE#` 成对无误。

### entry-02593
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-wilder_summoner.lua:23`。原文 `Summoner (Wilder)` 译为 `召唤师（野性系）`，术语准确，颜色码完整。

### entry-02594
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-wilder_summoner.lua:24`。召唤盟友、直接控制（Possess 机制）以及失衡值描述完整，颜色标记闭合无误。

### entry-02595
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-wilder_wyrmic.lua:23`。原文 `Wyrmic (Wilder)` 译为 `龙战士（野性系）`，术语规范，颜色码一致。

### entry-02596
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-wilder_wyrmic.lua:24`。多系龙兽形态、吐息武器、失衡值与体力值双资源特性描述符合游戏机制，颜色控制符成对完整。

### entry-02597
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-yeek.lua:23`。原文 `Yeek` 译为 `夺心魔`，符合核心种族既定译名，颜色码保留。

### entry-02598
- **状态**：细微观察
- **可核验依据**：源码位于 `game/modules/tome/data/texts/unlock-yeek.lua:24`。
  1. 专名 `island of Rel`（瑞尔岛）、`Maj'Eyal`（马基·埃亚尔）、`Halfling nation of Nargol`（半身人国家纳格尔）、`The Way`（维网）、`Yeek Wayist`（夺心魔维网信徒）翻译准确，颜色标签闭合完整。
  2. 观察发现：原文第2行单句叙述在译文中被拆分为两小段，第3句补充了“在烈火纪元之前的漫长岁月里”这一衔接语，属于叙事性适度润色，不影响游戏事实。

### entry-02599
- **状态**：存在疑点
- **可核验依据**：源码位于 `game/modules/tome/data/timed_effects/floor.lua:51-64`。
  1. 格式占位符：4 个 `%+0.2f` 分别对应 `eff.power`（生命回复）、`eff.equilibrium`（失衡值回复）、`eff.stamina`（体力回复）和 `eff.psi`（灵能回复），顺序与格式完全正确。
  2. 疑点事实：原文末尾附带条件为 `(Only living creatures benefit.)`（仅活体生物受益），译文将其翻译为 `不死族无法获得此效果。`。经查阅固定 commit 源码 `game/modules/tome/class/Actor.lua:7045-7075`，判别机制为 `not self:checkClassification("living")`，其底层 `unliving` 明确定义为包含 `undead`（不死族）、`construct`（构装体/魔像）及 `crystal`（晶体生物）。译文将“仅活体生物受益”改写为“不死族无法获得此效果”，不仅丢失括号且变成否定句，而且排除了构装体等其他非活体生物，与底层机制事实不符。

### entry-02600
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/timed_effects/floor.lua:67`。`desc = "Spellblaze Scar"` 经 `floorEffect` 包装。译文 `魔法大爆炸伤痕` 与统一术语及上下文一致。

### entry-02601
- **状态**：存在疑点
- **可核验依据**：源码位于 `game/modules/tome/data/timed_effects/floor.lua:68-78`。
  1. 原文为 `The target is near a spellblaze scar, granting +25% spell critical chance, +10% fire and blight damage but critical spells will drain arcane forces.`，译文为 `目标接近魔法大爆炸伤痕，获得 25%法术暴击率，增加 10%火焰和枯萎伤害，但是法术暴击会消耗法力值。`。
  2. 机制核查：查看 `activate` 逻辑，法术暴击时触发的资源扣除实际包括：`mana_on_crit = -15`、`vim_on_crit = -10`、`paradox_on_crit = 20`、`positive_on_crit = -10`、`negative_on_crit = -10`。原文所指的 `arcane forces`（奥术能量/相关能量）是统称（涵盖法力、活力、悖论值、正能量与负能量）。译文将泛指的 `arcane forces` 窄化翻译为单一资源“法力值”（Mana），与实际机制严重脱节，会误导使用其他魔法能量的职业。

### entry-02602
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/timed_effects/floor.lua:81-87`。原文描述降低 60% 疾病抗性及 40% 几率感染疾病（每回合触发一次），数值、百分比及机制完全对应代码中 `disease_immune = -0.6` 与 `blighted_soil = 40`。

### entry-02603
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/timed_effects/floor.lua:107-116`。tformat 转义 `%`（`+20%%`）在原文与译文中均保留双百分号，`-%d` 正确对应单一参数 `eff.power`。

### entry-02604
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/timed_effects/magical.lua:60`。原文占位符 `%d%% (#RED#%d#LAST#)` 在译文中完整保留为 `%d%%（#RED#%d#LAST#）`，参数 1 为降低百分比，参数 2 为固定扣除点数，顺序及颜色控制符完全吻合。

### entry-02605
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/timed_effects/magical.lua:136`（`STONED` 效果的 `on_gain` 回调）。占位符 `#Target#` 与颜色标记 `#GREY#STONE#LAST#` -> `#GREY#石头#LAST#` 保留完整准确。

### entry-02606
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/timed_effects/magical.lua:374`（`STORMSHIELD` 效果的 `on_gain` 回调）。占位符 `#Target#` 正确保留，语义完全对应。

### entry-02607
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/timed_effects/magical.lua:391`。原文代码 `src:logCombat(self, "#BLUE##Target#'s stormshield is out of charges and dissipates!#LAST#.")`，译文保留了 `#BLUE#`、`#Target#` 及末尾嵌套标点 `！#LAST#。`，机制为风暴护盾阻挡次数耗尽，翻译准确。

### entry-02608
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/timed_effects/magical.lua:444`（`PURGING` 效果的 `on_lose` 回调）。原文有笔误 `#Target#'s is`，译文为 `#Target#不再被净化。`，占位符完好，语义准确。

### entry-02609
- **状态**：细微观察
- **可核验依据**：源码位于 `game/modules/tome/data/timed_effects/magical.lua:458`（`VIMSENSE_DETECT` 效果的 `long_desc`）。原文 `Improves senses, allowing the detection of unseen things.` 译为 `强化感知，可以看到看不到的东西。`。口语化程度略高，但准确表述了效果机制，无技术或机制缺陷。

### entry-02610
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/timed_effects/magical.lua:557`（`BANE_CONFUSED` 效果的 `long_desc`）。双参数 `%d%%`（混乱几率，对应 `eff.power`）与 `%0.2f`（暗影伤害，对应 `eff.dam`）顺序与格式严丝合缝，类型术语黑暗/暗影与混乱完全对应。

### entry-02611
- **状态**：未发现问题
- **可核验依据**：源码位于 `game/modules/tome/data/timed_effects/magical.lua:703`（`ARCANE_EYE_SEEN` 效果的 `long_desc`）。原文为状态描述，译文“一个奥术之眼正在观察着这个生物”符合其附着持续性效果的机制。

---

### 复核总结
- **核验范围**：全量 40 条（`entry-02572` 至 `entry-02611`），无遗漏。
- **存在疑点条目**（2 条）：
  - `entry-02599`：`floor.lua` 生命之泉尾句 `(Only living creatures benefit.)` 译为“不死族无法获得此效果。”，而源码底层 `checkClassification("living")` 实际包含构装体/魔像等非活体非亡灵生物，存在缩小限制范围且篡改句式的问题。
  - `entry-02601`：`floor.lua` 魔法大爆炸伤痕机制将暴击扣减各系奥术资源的 `arcane forces` 窄化错译为单一资源“法力值”（Mana），掩盖了其扣减活力、正负能量与增加悖论值的机制。
- **细微观察条目**（4 条）：
  - `entry-02576`：织梦者倒数第二段首句重复套用了前面的“思想和梦境的力量”译法，且正文缺少冒号。
  - `entry-02579`：掠夺者特点标题行格式增加换行，正文缺少冒号。
  - `entry-02586`：流浪者 `#{bold}# 奖励 #{normal}#` 标签内外存在多余空格，数字格式书写不统一。
  - `entry-02609`：活力感知描述用语略显口语化。