# 冻结40条译文：统一复核规则 v3-source（临时文件与混合来源）

你是只读 REVIEWER。仅审本包 entry-03773–entry-03812 共40条。中文自然语言输出，不强制JSON。用户已明确允许临时文件：可在仓库外使用自己创建的任务专属临时目录（例如 mkdtemp(prefix="abc20-g16-20260923-")），保存/删除中间文件并报告路径；不得读取他人临时材料。仓库、冻结输入及译文保持只读，不创建子agent，不修复译文，不读取其他模型输出。以下任务约束对所有实验臂相同。

## 判断依据与范围

1. 原文/译文及身份以本包和 entries.json 为准；邻近译文仅来自同目录 context.lua。术语只用本包末尾子集；按 source_tag/category/语境匹配，existing 不是强制改名依据。不得读取当前翻译文件、其他实验文件、SPEC/STATE、历史报告或生产结论。
2. 游戏机制以可核验的实际源码行为为准。本体固定commit 624a67329fe2ad440c5b344785a9c73fcf22ae63；DLC使用source-access列明且哈希固定的公开快照，源码仓库/commit未固定，必须显式标注。DLC机制疑点可陈述快照内已证事实，但目标版本适用性缺口保留待确认，不将引擎commit套用DLC。缺源码的组件仅确认文本或格式直接可证的问题，机制依赖疑点待确认。英文、术语或旧译不能覆盖源码；沿袭上游的误述和翻译新增分开，不仅凭变量名猜机制。
3. 可读本INPUT、entries.json、context.lua、source-access.json及其中sections列明的本组sources文件。可在这些单文件内搜索。源码缺失已明确列在unavailable_components，不把其他组件同名代码当作它的证据。
4. 追调用链时，本体只能git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<明确相关的单文件path>；DLC只能读取source-access中dlc_additional_sources列明、哈希匹配的相关单文件。每个新增文件说明哪个已读调用/符号/require引入。禁止当前源码工作树、其他commit、整目录git grep/rg/find或历史审核查找；不能读取共享DLC快照中的locales等其他语言答案。证据不足写待确认。
5. 不把问题扩大为全局重命名或术语策略。格式结合实际显示/参数消费判断：保留source_tag、args_order、special；占位符、标记及段落/换行差异只有导致错误参数、错误显示或信息结构丢失时才算缺陷。合法排版和等价重排不算缺陷。

## 四类判定（按以下顺序合并一条内的多个claim）

- **存在问题**：至少一个有可核验证据的错误或遗漏，涉及事实、作用对象/所属关系、数量/条件/范围/时序、玩家操作、语义信息、明确适用的术语要求或运行时格式。轻微并不自动变为建议；必须解释具体哪项信息错误或丢失，不因可自行猜出原意便忽略。
- **待确认**：没有已证实问题，但有具体疑点因证据不足无法定论。指出缺哪项证据。不得把待确认当未发现问题。
- **仅建议**：没有上述问题或未决疑点，仅更自然的措辞、个人偏好、无损排版等；不得将建议计作缺陷。
- **未发现问题**：无上述三类事项。

一条同时有已证实问题和待确认claim，总判定为存在问题，但须分别列出各claim状态。若只有建议和未决claim，总判定为待确认。不同条目重复同一问题仍分别覆盖；同条重复表述不重复计claim。

## 输出

先给恰好40行的表格，列为“完整entry-ID | 四类判定 | claim编号或简短依据”。按冻结顺序，无漏项，不用“其余通过”。随后按claim编号列出原文/译文必要短引、问题具体内容、状态、源码路径:行号/函数及消费逻辑（纯语义判断可给明确语境证据）。对建议简述其为何仅属偏好；无需大段重抄整个输入。不要给修改方案。每个问题、建议或待确认观察使用单独标题：### C01 | entry-03773 | 存在问题（ID递增，替换为实际条目和状态）；不同缺陷尽量分开，方便后续无损归并。

最后列实际读取的所有路径与版本、额外源码路径的调用链来源、是否有无法核验或越界；如发生越界如实报告。禁止查找模型比较结果或给自己打分。你输出的是审核观察，不是真值，不宣称DONE_VERIFIED。


## entry-03773
位置：tome-orcs.lua:993；section：tome-orcs/data/general/npcs/titan.lua；source_tag：_t；args_order：None；special：None

原文：
```text
One of the biggest titans you have seen yet, it is fully clad in deep black stralite full plate, charging menacingly towards you at a terrible pace.
```
译文：
```text
这是你迄今见过的最大泰坦之一，它身披一整套深黑色斯莱特板甲，正以骇人的速度向你猛冲而来。
```

## entry-03774
位置：tome-orcs.lua:1070；section：tome-orcs/data/general/objects/boss-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Fully heal yourself. (15 turn cooldown)
```
译文：
```text
完全治疗（15回合冷却）
```

## entry-03775
位置：tome-orcs.lua:1079；section：tome-orcs/data/general/objects/boss-artifacts.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# psychically dominates #target# through %s %s!
```
译文：
```text
#Source#使用%s%s精神控制#target#！
```

## entry-03776
位置：tome-orcs.lua:1086；section：tome-orcs/data/general/objects/boss-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A light staff covered in stralite and gems. It seems to reflect the light of the stars even in daylight.
```
译文：
```text
一把被斯莱特和宝石覆盖的轻型法杖。即使在白天，似乎也在反射着星星的光芒。
```

## entry-03777
位置：tome-orcs.lua:1114；section：tome-orcs/data/general/objects/generic-world-artifacts.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s quaffs the %s!
```
译文：
```text
%s 大口喝下 %s！
```

## entry-03778
位置：tome-orcs.lua:1116；section：tome-orcs/data/general/objects/generic-world-artifacts.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#CRIMSON#The Blood of Undeath strengthens your undead body (-60 maximum life, -140 minimum life).
```
译文：
```text
#CRIMSON#不死之血强化了你的不死之躯（-60最大生命值，-140生命值下限）。
```

## entry-03779
位置：tome-orcs.lua:1125；section：tome-orcs/data/general/objects/inscriptions.lua；source_tag：_t；args_order：None；special：None

原文：
```text
implant on your skin.
```
译文：
```text
植入到皮肤上。
```

## entry-03780
位置：tome-orcs.lua:1203；section：tome-orcs/data/general/objects/steamgun.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
stralite steamgun
```
译文：
```text
斯莱特蒸汽枪
```

## entry-03781
位置：tome-orcs.lua:1204；section：tome-orcs/data/general/objects/steamgun.lua；source_tag：entity short_name；args_order：None；special：None

原文：
```text
stralite
```
译文：
```text
斯莱特
```

## entry-03782
位置：tome-orcs.lua:1227；section：tome-orcs/data/general/objects/steamsaw.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
stralite steamsaw
```
译文：
```text
斯莱特蒸汽链锯
```

## entry-03783
位置：tome-orcs.lua:1228；section：tome-orcs/data/general/objects/steamsaw.lua；source_tag：entity short_name；args_order：None；special：None

原文：
```text
stralite
```
译文：
```text
斯莱特
```

## entry-03784
位置：tome-orcs.lua:1241；section：tome-orcs/data/general/objects/tinker.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Medical salve.
```
译文：
```text
医用药剂。
```

## entry-03785
位置：tome-orcs.lua:1255；section：tome-orcs/data/general/objects/tinkers/chemistry.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Infects targets with a stat reducing disease.
```
译文：
```text
使目标感染削减属性的疾病。
```

## entry-03786
位置：tome-orcs.lua:1258；section：tome-orcs/data/general/objects/tinkers/chemistry.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Deals cold damage and slows.
```
译文：
```text
造成寒冷伤害并减速。
```

## entry-03787
位置：tome-orcs.lua:1261；section：tome-orcs/data/general/objects/tinkers/chemistry.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Deals acid damage that also reduces armour.
```
译文：
```text
造成酸性伤害并降低护甲。
```

## entry-03788
位置：tome-orcs.lua:1277；section：tome-orcs/data/general/objects/tinkers/chemistry.lua；source_tag：_t；args_order：None；special：None

原文：
```text
On falling below 20% of your max life, releases a cloud of smoke, confusing nearby enemies and giving you stealth and a chance to avoid incoming damage for 5 turns.
```
译文：
```text
生命掉落至20%以下时，释放一阵烟雾，混乱周围生物，令你潜行并有一定几率免疫伤害，持续5回合。
```

## entry-03789
位置：tome-orcs.lua:1298；section：tome-orcs/data/general/objects/tinkers/electricity.lua；source_tag：_t；args_order：None；special：None

原文：
```text
stralite
```
译文：
```text
斯莱特
```

## entry-03790
位置：tome-orcs.lua:1313；section：tome-orcs/data/general/objects/tinkers/electricity.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# unleashes GALVANIC RETRIBUTION!
```
译文：
```text
#Source#引发了电力反击！
```

## entry-03791
位置：tome-orcs.lua:1315；section：tome-orcs/data/general/objects/tinkers/electricity.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Deals lightning damage and drains resources.
```
译文：
```text
造成闪电伤害，吸取资源。
```

## entry-03792
位置：tome-orcs.lua:1356；section：tome-orcs/data/general/objects/tinkers/explosive.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Boom.
```
译文：
```text
轰。
```

## entry-03793
位置：tome-orcs.lua:1378；section：tome-orcs/data/general/objects/tinkers/mechanical.lua；source_tag：_t；args_order：None；special：None

原文：
```text
stralite
```
译文：
```text
斯莱特
```

## entry-03794
位置：tome-orcs.lua:1403；section：tome-orcs/data/general/objects/tinkers/smith.lua；source_tag：_t；args_order：None；special：None

原文：
```text
stralite
```
译文：
```text
斯莱特
```

## entry-03795
位置：tome-orcs.lua:1448；section：tome-orcs/data/general/objects/tinkers/therapeutics.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
remove %d physical effects and grants a frost aura (%s cold, darkness and nature affinity)
```
译文：
```text
清除%d项物理负面效果并制造寒霜光环，获得%s寒冷、暗影和自然伤害亲和。
```

## entry-03796
位置：tome-orcs.lua:1450；section：tome-orcs/data/general/objects/tinkers/therapeutics.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
remove %d magical effects and grants a fiery aura (%s fire, light and lightning affinity)
```
译文：
```text
清除%d项魔法负面效果并制造烈火光环，获得%s火焰、光系和闪电伤害亲和。
```

## entry-03797
位置：tome-orcs.lua:1452；section：tome-orcs/data/general/objects/tinkers/therapeutics.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
remove %d mental effects and grants a water aura (%s blight, mind and acid affinity).
```
译文：
```text
清除%d项精神负面效果并制造静水光环，获得%s枯萎、精神和酸性伤害亲和。
```

## entry-03798
位置：tome-orcs.lua:1464；section：tome-orcs/data/general/objects/tinkers/therapeutics.lua；source_tag：_t；args_order：None；special：None

原文：
```text
(15 turn cooldown)
```
译文：
```text
（15回合冷却时间）
```

## entry-03799
位置：tome-orcs.lua:1499；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
These boots have a %d%% chance to fail to operate properly (reduced by Cunning).
```
译文：
```text
火箭靴有%d%%几率失败（随灵巧降低）。
```

## entry-03800
位置：tome-orcs.lua:1502；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# ignites %s %s, creating a #LIGHT_RED#blast of fire#LAST# that %s!
```
译文：
```text
#Source#点燃了%s%s，创造出一股#LIGHT_RED#火焰爆炸#LAST#%s！
```

## entry-03801
位置：tome-orcs.lua:1509；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：tformat；args_order：[1, 2, 3, 5, 4]；special：None

原文：
```text
fire a poisonous bolt out to range %d that deals %d nature damage and afflicts the target with crippling poison (%d%% fail chance) that deals %d addition nature damage over %d turns (damage based on Cunning)
```
译文：
```text
发射一支射程最远为 %d 码的毒箭，造成 %d 点自然伤害，并导致目标被致残毒素（%d%% 行动失败几率），在 %d 回合内造成 %d 点额外自然伤害（伤害受灵巧值加成）
```

## entry-03802
位置：tome-orcs.lua:1516；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# recoils from the shot.
```
译文：
```text
#Source#被反冲力击退。
```

## entry-03803
位置：tome-orcs.lua:1523；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
deal cold damage equal to 100 + the higher of your steam or spellpower, and attempt to freeze the target (20% chance).
```
译文：
```text
造成100+蒸汽强度或法术强度较高项的寒冷伤害，并有20%几率冰冻目标。
```

## entry-03804
位置：tome-orcs.lua:1531；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
"Have you ever looked at some guys and thought 'you know, I really wish they were on fire right now', but you didn't feel like walking all the way over there? Well, there's now a better way!"
```
译文：
```text
你是否曾经看到一些人并且想：“你知道吗，我真的想要烧死这些人”，但是你又不想大费周章，现在有了一个更加方便的方法！
```

## entry-03805
位置：tome-orcs.lua:1541；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s tosses %s %s!
```
译文：
```text
%s投掷了%s%s！
```

## entry-03806
位置：tome-orcs.lua:1547；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
On hitting with a mindstar, deal physical damage equal to your steampower in radius 1 around the target.
```
译文：
```text
用灵晶命中时，在半径1范围内造成等于蒸汽强度的物理伤害。
```

## entry-03807
位置：tome-orcs.lua:1551；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
(cooling down: %d turns)
```
译文：
```text
(冷却时间：%d 回合)
```

## entry-03808
位置：tome-orcs.lua:1557；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
strike the target with one of Mind Sear, Psychic Lobotomy, or Sunder Mind, at random.
```
译文：
```text
随机使用以下技能之一打击目标：心灵灼烧、心灵脑叶切除或碾碎心灵。
```

## entry-03809
位置：tome-orcs.lua:1560；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Through a combination of magic and airborne probes, these shots incite powerful bolts of lightning to strike your target from above, frying them and those around them!
```
译文：
```text
这些弹药通过魔法和探针从天空引导强力的闪电冲击你的目标，灼烧目标及周边的单位！
```

## entry-03810
位置：tome-orcs.lua:1565；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
release a burst of light dealing damage equal to your cunning plus your magic in a ball of radius 2. If the target is undead, the damage and radius are doubled.
```
译文：
```text
在半径2范围内造成等于灵巧加魔法的光明伤害。若目标为不死族，伤害和半径加倍。
```

## entry-03811
位置：tome-orcs.lua:1569；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Release a burst of shrapnel, dealing physical damage equal to your steampower in a cone from the target of radius 4.
```
译文：
```text
释放榴弹，在半径4锥形范围内造成等于蒸汽强度的物理伤害。
```

## entry-03812
位置：tome-orcs.lua:1585；section：tome-orcs/data/general/objects/world-artifacts.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# takes aim at #target# using %s!
```
译文：
```text
#Source#使用%s瞄准#target#！
```

## 相关术语快照
仅按source_tag/category/语境适用；existing不构成强制改名。
```tsv
source	target	category	domain	source_tag	status	scope	notes
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Lightning	闪电术	T.GAME.TALENT	talents	talent name	existing	core	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mind Sear	心灵灼烧	T.GAME.TALENT	talents	talent name	preferred	core	sear 指灼烧；技能机制虽为射线，名称不增译“光束”
Psychic Lobotomy	心灵脑叶切除	T.GAME.TALENT	talents	talent name	preferred	core	与技能日志中的 lobotomy 统一
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Steam	蒸汽	T.GAME.RESOURCE	resources	_t	existing	dlc	Embers of Rage 角色资源
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
The Way	维网	T.PN.FACTION	society	nil	existing	core	
Undead	不死族	T.PN.RACE	creatures	nil	existing	core	
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
affinity	伤害吸收	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
blight	枯萎	T.GAME.DAMAGE	combat	damage type	existing	core	
blight	枯萎	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
cold	寒冷	T.GAME.DAMAGE	combat	damage type	existing	core	
cold	寒冷	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
disease	疾病	T.GAME.EFFECT	combat	effect subtype	existing	core	
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
freeze	冰冻	T.GAME.DAMAGE	combat	damage type	existing	core	
galvanic	放电	T.GAME.DAMAGE	combat	damage type	existing	dlc	Embers of Rage DLC 伤害类型
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
lightning	闪电	T.GAME.DAMAGE	combat	damage type	existing	core	
lightning	闪电	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
poison	毒素	T.GAME.DAMAGE	combat	damage type	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
staff	法杖	T.GAME.ENTITY	items	entity subtype	existing	global	
steam	蒸汽	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Embers of Rage DLC 机制效果类型
steam	蒸汽	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	Embers of Rage 技能类别
steamgun	蒸汽枪	T.GAME.ENTITY	items	entity subtype	existing	dlc	
steamsaw	蒸汽链锯	T.GAME.ENTITY	items	entity subtype	existing	dlc	Embers of Rage 实体子类型
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stralite	斯莱特	T.GAME.ENTITY	items	nil	preferred	global	高阶金属材质名；统一装备全名、材质短名、材料块及叙事引用，不使用少数旧条目的“蓝皓石”
undead	亡灵	T.GAME.ENTITY	creatures	entity type	existing	global	
undead	亡灵	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
```
