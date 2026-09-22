### batch-021 文件哈希核验

- **文件路径**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-021.md`
- **预期 SHA-256**：`8b32123d11271163bfa7a72cd19a4732806e1f60869ae37623f5ed83a846e401`
- **实测 SHA-256**：`8b32123d11271163bfa7a72cd19a4732806e1f60869ae37623f5ed83a846e401`
- **核验结论**：哈希一致，通过。

---

### 本批复核环境与基准说明

- **源码基准**：ToME4 engine 固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63`（所有条目均来自 `mod-tome/` 路径，对照公开源码文件核验）。
- **译文终点**：commit `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`（对照 `mod-tome.lua` 同 section 上下文）。
- **覆盖范围**：`entry-00802` 至 `entry-00841`，共 40 条，逐条列出核验依据与结论。

---

### 逐条复核报告

#### entry-00802
- **位置**：`mod-tome.lua:9182`（`mod-tome/data/general/objects/boss-artifacts-far-east.lua`）
- **标签**：`logCombat`
- **原文**：`#GOLD#A bolt of lightning fires from #Source#'s bow, striking #Target#!`
- **译文**：`#GOLD#一道闪电从#Source#的弓中射出，击中了#Target#！`
- **结论**：未发现问题
- **依据**：源码 `who:logCombat(a, "#GOLD#A bolt of lightning fires from #Source#'s bow, striking #Target#!")`，战斗日志实体宏 `#Source#` 与 `#Target#`、颜色控制符 `#GOLD#` 均完整保留，标点转换正确，语意准确。

#### entry-00803
- **位置**：`mod-tome.lua:9187`（`mod-tome/data/general/objects/boss-artifacts-far-east.lua`）
- **标签**：`logSeen`
- **原文**：`%s releases an icy blast from %s %s!`
- **译文**：`%s从%s%s中释放出冰风！`
- **结论**：未发现问题
- **依据**：源码传参依次为角色名、代词 `who:his_her()`、物品名；译文占位符 `%s` 数量（3个）与顺序一致；“icy blast”译为“冰风”，与该装备主动技能描述 `chilling blast`（吹出冰风）保持行文风格一致，感叹号转换正确。

#### entry-00804
- **位置**：`mod-tome.lua:9191`（`mod-tome/data/general/objects/boss-artifacts-far-east.lua`）
- **标签**：`_t`
- **原文**：`The massive stone limb of the Rotting Titan, a mass of stone and rotting flesh. You think you can lift it, but it is very heavy.`
- **译文**：`腐化泰坦巨大的石质肢体，一大块石头与腐肉的混合体。你觉得自己举得动它，但它非常沉重。`
- **结论**：细微观察
- **依据**：装备描述准确通顺。微小观察：在 `rak-shor-pride/npcs.lua` 中该 NPC 实体的名称译为“腐烂泰坦”，此条描述译作“腐化泰坦”，专名存在细微出入，但结合后文“腐肉的混合体”语意完全清晰。

#### entry-00805
- **位置**：`mod-tome.lua:9194`（`mod-tome/data/general/objects/boss-artifacts-far-east.lua`）
- **标签**：`tformat`
- **原文**：`knock away other creatures within radius %d), dealing %0.2f to %0.2f physical damage (based on Strength) to each`
- **译文**：`击退半径 %d 的生物，造成 %0.2f 到 %0.2f 物理伤害（基于力量）。`
- **结论**：存在疑点
- **依据**：
  1. 原文在源码中存在笔误自带多余闭括号 `within radius %d)`，译文妥善处理并去除了孤立括号，格式化占位符 `%d` 与两个 `%0.2f` 顺序及数量一致；
  2. 但译文漏译了“within”（范围内）与“other”（其他），且“击退半径 %d 的生物”在中文语境下存在“体型半径为 %d 的生物”之歧义，建议更准确译作“击退半径 %d 范围内的其他生物”。

#### entry-00806
- **位置**：`mod-tome.lua:9195`（`mod-tome/data/general/objects/boss-artifacts-far-east.lua`）
- **标签**：`logSeen`
- **原文**：`%s slams %s %s into the ground, sending out a shockwave!`
- **译文**：`%s将%s%s砸入地面，释放冲击波！`
- **结论**：未发现问题
- **依据**：源码传参依次为角色名、代词、装备名；3 个 `%s` 占位符及顺序完整保留，感叹号转换正确，动作与效果表达准确。

#### entry-00807
- **位置**：`mod-tome.lua:9212`（`mod-tome/data/general/objects/boss-artifacts-maj-eyal.lua`）
- **标签**：`_t`
- **原文**：`Winter Storm: `
- **译文**：`寒冰风暴： `
- **结论**：未发现问题
- **依据**：源码为拼接字符串前缀 `_t"Winter Storm: " .. (...)`，英文冒号后带 1 空格；译文使用全角冒号并保留末尾空格，与后续拼接的 `radius %d...` 衔接顺畅。

#### entry-00808
- **位置**：`mod-tome.lua:9215`（`mod-tome/data/general/objects/boss-artifacts-maj-eyal.lua`）
- **标签**：`tformat`
- **原文**：`Create a Winter Storm that gradually expands (from radius %d to radius %d), dealing %0.2f cold damage (based on Strength) to your enemies each turn and slowing their ability to act by 20%%.  Subsequent melee strikes will relocate the storm on top of your target and increase its duration.`
- **译文**：`制造不断扩张的寒冰风暴（从半径 %d 到半径 %d），每回合对敌人造成 %0.2f 寒冷伤害（基于力量）并减速 20%%。接下来的近战攻击将把风暴移至目标身上并延长持续时间。`
- **结论**：未发现问题
- **依据**：源码 `tformat` 依次传入 `special.radius`、`special.max_radius`、`dam`；译文占位符 `%d`、`%d`、`%0.2f` 及转义百分号 `20%%` 完全一致；伤害类型“cold（寒冷）”与属性“Strength（力量）”术语规范。

#### entry-00809
- **位置**：`mod-tome.lua:9238`（`mod-tome/data/general/objects/boss-artifacts-maj-eyal.lua`）
- **标签**：`_t`
- **原文**：`A pitch black ring, unadorned. It seems as though tendrils of darkness creep upon it.`
- **译文**：`一枚纯黑色的戒指，没有任何纹饰。似乎有黑暗的触须攀附其上。`
- **结论**：未发现问题
- **依据**：戒指 Nightsong（暗夜颂歌）背景描述，句式通顺，标点与分句对应准确。

#### entry-00810
- **位置**：`mod-tome.lua:9242`（`mod-tome/data/general/objects/boss-artifacts-maj-eyal.lua`）
- **标签**：`_t`
- **原文**：`A great helm that belonged to Garkul the Devourer, one of the greatest orcs ever to live.`
- **译文**：`这顶巨盔曾属于吞噬者加库尔，有史以来最伟大的兽人之一。`
- **结论**：未发现问题
- **依据**：“Garkul the Devourer”译为“吞噬者加库尔”，“orcs”译为“兽人”，专名符合全库规范。

#### entry-00811
- **位置**：`mod-tome.lua:9248`（`mod-tome/data/general/objects/boss-artifacts-maj-eyal.lua`）
- **标签**：`_t`
- **原文**：`large chunk of wood`
- **译文**：`一大块木头`
- **结论**：未发现问题
- **依据**：盾牌 Wrathroot's Barkwood（狂怒树精的树皮）的未鉴定名，简洁准确。

#### entry-00812
- **位置**：`mod-tome.lua:9251`（`mod-tome/data/general/objects/boss-artifacts-maj-eyal.lua`）
- **标签**：`entity subtype`
- **原文**：`red`
- **译文**：`红色`
- **结论**：未发现问题
- **依据**：宝石类物品 Petrified Wood（硅化木）定义的子类型属性 `subtype = "red"`，对应宝石分类“红色”，译法准确。

#### entry-00813
- **位置**：`mod-tome.lua:9253`（`mod-tome/data/general/objects/boss-artifacts-maj-eyal.lua`）
- **标签**：`_t`
- **原文**：`A piece of the scorched wood taken from the remains of Snaproot.`
- **译文**：`取自远古树精遗骸的一块烧焦的木头。`
- **结论**：未发现问题
- **依据**：“Snaproot”在 `old-forest/npcs.lua` 中译名为“远古树精”，掉落该硅化木宝石，专名对应完全一致，句意准确。

#### entry-00814
- **位置**：`mod-tome.lua:9259`（`mod-tome/data/general/objects/boss-artifacts-maj-eyal.lua`）
- **标签**：`logSeen`
- **原文**：`Crystals splinter off of %s's %s and animate!`
- **译文**：`%s的%s上的水晶碎片活动了起来！`
- **结论**：未发现问题
- **依据**：源码传参为角色名与法杖名，2 个 `%s` 占位符位置与从属关系处理得当，感叹号转换正确。

#### entry-00815
- **位置**：`mod-tome.lua:9276`（`mod-tome/data/general/objects/boss-artifacts-maj-eyal.lua`）
- **标签**：`logPlayer`
- **原文**：`You need an enemy nearby to summon!`
- **译文**：`需要旁边有一个敌人才能召唤！`
- **结论**：未发现问题
- **依据**：召唤吸血鬼仆从失败提示，感叹号与语意完整对应。

#### entry-00816
- **位置**：`mod-tome.lua:9277`（`mod-tome/data/general/objects/boss-artifacts-maj-eyal.lua`）
- **标签**：`logPlayer`
- **原文**：`Not enough space to summon!`
- **译文**：`没有足够的空间召唤！`
- **结论**：未发现问题
- **依据**：源码为 `game.logPlayer(who, "Not enough space to summon!")`，带感叹号，译文忠实保留全角感叹号与句意（术语快照中含带句号的 logSeen 版本，本条以对应固定源码的标点为准）。

#### entry-00817
- **位置**：`mod-tome.lua:9322`（`mod-tome/data/general/objects/boss-artifacts-maj-eyal.lua`）
- **标签**：`logCombat`
- **原文**：`#Source# aims %s %s at #target#!`
- **译文**：`#Source#用%s%s瞄准了#target#！`
- **结论**：未发现问题
- **依据**：源码 `who:logCombat(..., "#Source# aims %s %s at #target#!", who:his_her(), self:getName(...))`，实体标记 `#Source#`、`#target#`（原小写）完全吻合，2 个 `%s` 占位符保留，感叹号转换规范。

#### entry-00818
- **位置**：`mod-tome.lua:9329`（`mod-tome/data/general/objects/boss-artifacts-maj-eyal.lua`）
- **标签**：`_t`
- **原文**：`A huge tooth taken from the Mouth, in the Deep Bellow.`
- **译文**：`一颗取自深渊咆哮中巨口的巨大牙齿。`
- **结论**：未发现问题
- **依据**：“the Mouth”对应深渊咆哮 Boss“巨口”，“Deep Bellow”对应地名“深渊咆哮”，地名与 Boss 名均准确对应。

#### entry-00819
- **位置**：`mod-tome.lua:9331`（`mod-tome/data/general/objects/boss-artifacts-maj-eyal.lua`）
- **标签**：`_t`
- **原文**：`pair of painful-looking boots`
- **译文**：`看着就疼的靴子`
- **结论**：未发现问题
- **依据**：重靴 The Warped Boots（扭曲之靴）的未鉴定名，口吻传神，表达自然。

#### entry-00820
- **位置**：`mod-tome.lua:9332`（`mod-tome/data/general/objects/boss-artifacts-maj-eyal.lua`）
- **标签**：`_t`
- **原文**：`These blackened boots have lost all vestiges of any former glory they might have had. Now, they are a testament to the corruption of the Deep Bellow, and its power.`
- **译文**：`这些被玷污的靴子已经丧失了它们以前的荣耀，现在，它们只能作为深渊咆哮的存在以及腐蚀力量的证明。`
- **结论**：存在疑点
- **依据**：
  1. 原文为“a testament to the corruption of the Deep Bellow, and its power”，结构为证明“深渊咆哮的腐化（堕落）”与“其力量”；译文作“深渊咆哮的存在以及腐蚀力量的证明”，无端增译了原文中不存在的“的存在”，并把“corruption”与“power”糅合成“腐蚀力量”，造成原文句法结构与语意移位；
  2. 原文“blackened boots”为发黑/熏黑的靴子，被意译为“被玷污的靴子”。

#### entry-00821
- **位置**：`mod-tome.lua:9339`（`mod-tome/data/general/objects/boss-artifacts-maj-eyal.lua`）
- **标签**：`_t`
- **原文**：
```text
Inch-thick stralite plates lock together with voratun joints. The whole suit looks impenetrable, but has clearly been subjected to terrible treatment - great dents and misshaping warps, and caustic fissures bored across the surface.
Though clearly a powerful piece, it must once have been much greater.
```
- **译文**：
```text
一英寸厚的斯莱特板甲，关节部分由沃瑞钽组成。整套铠甲看起来异常坚固，但是显然它有过非常可怕的经历——巨大的凹痕、扭曲的关节以及腐蚀的表面。
虽然这显然是一件强大的装备，但它曾经一定更为强大。
```
- **结论**：未发现问题
- **依据**：材质术语“stralite（斯莱特）”与“voratun（沃瑞钽）”严格符合术语库既定首选；破折号与换行分段完整保留，叙事行文流畅准确。

#### entry-00822
- **位置**：`mod-tome.lua:9354`（`mod-tome/data/general/objects/boss-artifacts-maj-eyal.lua`）
- **标签**：`_t`
- **原文**：
```text
A large hairy foot, very recognizably a halfling's, is strung on a piece of thick twine. In its decomposed state it's hard to tell how long ago it parted with its owner, but from what look like teeth marks around the ankle you get the impression that it wasn't given willingly.
It has been kept somewhat intact with layers of salt and clay, but in spite of this it's clear that nature is beginning to take its toll on the dead flesh. Some say the foot of a halfling brings luck to its bearer - right now the only thing you can be sure of is that it stinks.
```
- **译文**：
```text
一只用粗绳串起来的巨大毛脚，很显然这是一位半身人的。目前的状态，很难讲它多久以前被割了下来，但是从脚踝处的齿痕来看，应该不是出于自愿。
它靠着几层盐和粘土才勉强保持了一定程度的完整，但尽管如此，很明显大自然已经开始侵蚀这块早已死去的血肉。有人说，半身人的脚可以带来好运，但是现在唯一可确认的是——它臭死了。
```
- **结论**：未发现问题
- **依据**：半身人幸运脚背景描述，种族术语“halfling -> 半身人”准确；两段换行与破折号对应严密，语义传达生动。

#### entry-00823
- **位置**：`mod-tome.lua:9357`（`mod-tome/data/general/objects/boss-artifacts-maj-eyal.lua`）
- **标签**：`tformat`
- **原文**：
```text
Detects traps.
Removes (25%% chance) up to three stuns, pins, or dazes each turn%s
```
- **译文**：
```text
侦查陷阱。
每回合有 25%%几率解除至多3个震慑、定身或眩晕效果。%s
```
- **结论**：未发现问题
- **依据**：换行符 `\n` 一致；转义百分号 `25%%` 与后续格式化占位符 `%s`（用于接收冷却时间字串）保留完整；状态术语“stuns（震慑）”、“pins（定身）”、“dazes（眩晕）”与术语库完全吻合。

#### entry-00824
- **位置**：`mod-tome.lua:9368`（`mod-tome/data/general/objects/boss-artifacts-maj-eyal.lua`）
- **标签**：`logSeen`
- **原文**：`%s's %s sends out a blast of psionic energy!`
- **译文**：`%s的%s释放出灵能冲击波！`
- **结论**：未发现问题
- **依据**：源码传参角色名与装备名，2 个 `%s` 占位符保留且位置正确；术语“psionic -> 灵能”规范，感叹号转换正确。

#### entry-00825
- **位置**：`mod-tome.lua:9371`（`mod-tome/data/general/objects/boss-artifacts-maj-eyal.lua`）
- **标签**：`_t`
- **原文**：`This pair of fine mesh voratun gauntlets is covered with glyphs of power that spark with azure energy.  The metal is supple and light so as not to interfere with spell-casting.  When and where these gauntlets were forged is a mystery, but odds are the crafter knew a thing or two about magic.`
- **译文**：`这副细孔沃瑞钽臂铠被闪烁着蓝色能量的雕文所覆盖。这种金属柔软且轻盈，不会对施法造成阻碍。制造这副臂铠的时间和地点都是一个谜，但是可以确认的是，制造者对于魔法技术有一定的了解。`
- **结论**：未发现问题
- **依据**：材质术语“voratun -> 沃瑞钽”准确，未鉴定特征“fine mesh -> 细孔”前后一致，语意通顺。

#### entry-00826
- **位置**：`mod-tome.lua:9380`（`mod-tome/data/general/objects/boss-artifacts-maj-eyal.lua`）
- **标签**：`_t`
- **原文**：`clawed dragon-scale gloves`
- **译文**：`带爪的龙鳞手套`
- **结论**：未发现问题
- **依据**：手套 Wyrmbreath（龙之吐息）未鉴定名，翻译准确。

#### entry-00827
- **位置**：`mod-tome.lua:9401`（`mod-tome/data/general/objects/boss-artifacts.lua`）
- **标签**：`_t`
- **原文**：`Blackened with soot and covered in spikes, this battleaxe roars with the flames of the Fearscape. Given by Urh'Rok himself to his general, this powerful weapon can burn even the most resilient of foes.`
- **译文**：`这把双手斧被煤灰熏得漆黑，斧身布满尖刺，恶魔空间的烈焰在其上咆哮。它由乌鲁洛克亲手授予他的指挥官，这件强力武器甚至能烧穿最顽强的敌人。`
- **结论**：未发现问题
- **依据**：设定专名“Fearscape -> 恶魔空间”、“Urh'Rok -> 乌鲁洛克”严格符合术语库既定规则，行文生动流畅。

#### entry-00828
- **位置**：`mod-tome.lua:9408`（`mod-tome/data/general/objects/boss-artifacts.lua`）
- **标签**：`tformat`
- **原文**：`deals %d temporal damage and slows enemies in radius 6 of the target by %d%% based on Magic`
- **译文**：`造成 %d 时空伤害，并使目标周围 6 码范围内的敌人减速 %d%%（基于魔法）。`
- **结论**：未发现问题
- **依据**：源码传参为伤害值与减速百分比，占位符 `%d`、`%d%%` 数量与顺序一致；伤害类型“temporal -> 时空”准确。

#### entry-00829
- **位置**：`mod-tome.lua:9450`（`mod-tome/data/general/objects/brotherhood-artifacts.lua`）
- **标签**：`_t`
- **原文**：`vial of pink fluid`
- **译文**：`一瓶粉红色液体`
- **结论**：未发现问题
- **依据**：狡诈药剂未鉴定名，准确规范。

#### entry-00830
- **位置**：`mod-tome.lua:9456`（`mod-tome/data/general/objects/brotherhood-artifacts.lua`）
- **标签**：`_t`
- **原文**：`vial of green fluid`
- **译文**：`一瓶绿色液体`
- **结论**：未发现问题
- **依据**：闪避药剂未鉴定名，准确规范。

#### entry-00831
- **位置**：`mod-tome.lua:9461`（`mod-tome/data/general/objects/brotherhood-artifacts.lua`）
- **标签**：`_t`
- **原文**：`vial of red fluid`
- **译文**：`一瓶红色液体`
- **结论**：未发现问题
- **依据**：精准药剂未鉴定名，准确规范。

#### entry-00832
- **位置**：`mod-tome.lua:9466`（`mod-tome/data/general/objects/brotherhood-artifacts.lua`）
- **标签**：`_t`
- **原文**：`vial of cyan fluid`
- **译文**：`一瓶青色液体`
- **结论**：未发现问题
- **依据**：神秘药剂未鉴定名，准确规范。

#### entry-00833
- **位置**：`mod-tome.lua:9467`（`mod-tome/data/general/objects/brotherhood-artifacts.lua`）
- **标签**：`_t`
- **原文**：`A vial of glowing cyan fluid.`
- **译文**：`一瓶发光的青色液体。`
- **结论**：未发现问题
- **依据**：神秘药剂描述，标点与句意对应完整。

#### entry-00834
- **位置**：`mod-tome.lua:9471`（`mod-tome/data/general/objects/brotherhood-artifacts.lua`）
- **标签**：`_t`
- **原文**：`vial of grey fluid`
- **译文**：`一瓶灰色液体`
- **结论**：未发现问题
- **依据**：守护药剂未鉴定名，准确规范。

#### entry-00835
- **位置**：`mod-tome.lua:9476`（`mod-tome/data/general/objects/brotherhood-artifacts.lua`）
- **标签**：`_t`
- **原文**：`vial of maroon fluid`
- **译文**：`一瓶栗色液体`
- **结论**：未发现问题
- **依据**：掌握药剂未鉴定名，颜色“maroon -> 栗色”准确。

#### entry-00836
- **位置**：`mod-tome.lua:9479`（`mod-tome/data/general/objects/brotherhood-artifacts.lua`）
- **标签**：`logPlayer`
- **原文**：`#00FF00#The elixir has greatly expanded your capacity for improving your mind and body.`
- **译文**：`#00FF00#药剂大大拓展了你提升身心的潜力。`
- **结论**：未发现问题
- **依据**：掌握药剂使用日志，颜色码 `#00FF00#` 正确保留，语意通顺。

#### entry-00837
- **位置**：`mod-tome.lua:9480`（`mod-tome/data/general/objects/brotherhood-artifacts.lua`）
- **标签**：`logPlayer`
- **原文**：`You have %d stat point(s) to spend. Press G to use them.`
- **译文**：`你有%d属性点。请按 G 键使用。`
- **结论**：未发现问题
- **依据**：源码传参属性点数 `who.unused_stats`，格式化占位符 `%d` 与快捷键 G 保留，句意完整。

#### entry-00838
- **位置**：`mod-tome.lua:9482`（`mod-tome/data/general/objects/brotherhood-artifacts.lua`）
- **标签**：`_t`
- **原文**：`vial of orange fluid`
- **译文**：`一瓶橙色液体`
- **结论**：未发现问题
- **依据**：爆炸药剂未鉴定名，准确规范。

#### entry-00839
- **位置**：`mod-tome.lua:9483`（`mod-tome/data/general/objects/brotherhood-artifacts.lua`）
- **标签**：`_t`
- **原文**：`A vial of churning orange fluid.`
- **译文**：`一瓶翻涌的橙色液体。`
- **结论**：未发现问题
- **依据**：爆炸药剂描述，动词翻译生动，句末标点一致。

#### entry-00840
- **位置**：`mod-tome.lua:9487`（`mod-tome/data/general/objects/brotherhood-artifacts.lua`）
- **标签**：`_t`
- **原文**：`vial of yellow fluid`
- **译文**：`黄色液体小瓶`
- **结论**：存在疑点
- **依据**：在同文件同批次的炼金兄弟会全套 10 种药剂未鉴定名中，其余 9 处完全统一采用“一瓶[颜色]液体”句式（如 entry-00829“一瓶粉红色液体”、entry-00830“一瓶绿色液体”、entry-00831“一瓶红色液体”、entry-00832“一瓶青色液体”、entry-00834“一瓶灰色液体”、entry-00835“一瓶栗色液体”、entry-00838“一瓶橙色液体”、下文 9493 行“一瓶透明液体”、9498 行“一瓶棕褐色液体”），唯独此处 entry-00840 采用反向定语结构“黄色液体小瓶”，严重破坏同系列未鉴定名排比一致性，建议统一为“一瓶黄色液体”。

#### entry-00841
- **位置**：`mod-tome.lua:9490`（`mod-tome/data/general/objects/brotherhood-artifacts.lua`）
- **标签**：`logPlayer`
- **原文**：`#00FF00#The elixir seems to have subtly repositioned your entire being within the fabric of reality!`
- **译文**：`#00FF00#这瓶炼金药剂似乎将你的整个存在在现实结构中微妙地重新定位了！`
- **结论**：未发现问题
- **依据**：幸运药剂使用日志，颜色标记 `#00FF00#` 保留完整，修辞还原准确，感叹号转换正确。

---

### 复核疑点汇总概览

| 条目编号 | 判定类别 | 核心疑点要点 |
| :--- | :--- | :--- |
| **entry-00804** | 细微观察 | 描述中的“腐化泰坦”与同库 NPC 实体名“腐烂泰坦”存在细微用词出入。 |
| **entry-00805** | 存在疑点 | 漏译“within”与“other”，“半径 %d 的生物”在中文语境下有体型半径歧义，宜作“击退半径 %d 范围内的其他生物”。 |
| **entry-00820** | 存在疑点 | 原文句法结构为深渊咆哮的腐化与其力量，译文增译“的存在”并发生句义糅合与移位；“blackened”被意译为“被玷污”。 |
| **entry-00840** | 存在疑点 | 破坏炼金兄弟会药剂系列未鉴定名的统一句式结构（同文件其余 9 处均为“一瓶[颜色]液体”，唯独此处作“黄色液体小瓶”）。 |