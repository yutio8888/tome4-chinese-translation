# batch-028：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-01084
位置：mod-tome.lua:12878；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
These brilliant voratun gauntlets shine with an almost otherworldly glow. Originally used in the spellhunt, they were often used to destroy arcane artifacts, ridding the world of their influence. Pride in the fulfillment of this ancient duty practically radiates from them.
```
译文：
```text
这件沃瑞钽臂铠闪耀着近乎超凡脱俗的光芒。它最初在魔法狩猎中使用，常被用于摧毁奥术类装备，以消除它们对世界的影响。履行这一古老职责的自豪，几乎从这件臂铠上散发出来。
```

## entry-01085
位置：mod-tome.lua:12879；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
attempt to destroy all magic effects and sustains on creatures in a radius %d cone (unnatural creatures are additionally dealt %0.2f arcane damage and stunned)
```
译文：
```text
在半径%d码弧形区域尝试驱散生物身上的魔法效果和魔法持续技能（至多两项；非自然生物还会额外受到%0.2f奥术伤害并被震慑）
```

## entry-01086
位置：mod-tome.lua:12880；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s unleashes antimagic forces from %s %s!
```
译文：
```text
%s从%s%s中放出反魔法力量！
```

## entry-01087
位置：mod-tome.lua:12881；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s's animating magic is disrupted by the burst of power!
```
译文：
```text
%s的活化魔法被爆发的力量干扰了！
```

## entry-01088
位置：mod-tome.lua:12884；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Destroy which item?
```
译文：
```text
摧毁哪一件物品？
```

## entry-01089
位置：mod-tome.lua:12885；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You crush the %s, and the gloves take on an illustrious shine!
```
译文：
```text
你摧毁了%s，手套开始发光！
```

## entry-01090
位置：mod-tome.lua:12889；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
Summertide
```
译文：
```text
炎华
```

## entry-01091
位置：mod-tome.lua:12893；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
send out a range %d beam, lighting its path and dealing %0.2f to %0.2f light damage (based on Willpower and Cunning)
```
译文：
```text
发射长度 %d 的射线，照亮路径，并造成 %0.2f 到 %0.2f 点光系伤害（基于意志和灵巧）
```

## entry-01092
位置：mod-tome.lua:12894；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s's %s flashes!
```
译文：
```text
%s的%s 闪光了！
```

## entry-01093
位置：mod-tome.lua:12899；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
flowing robe
```
译文：
```text
飘逸的法袍
```

## entry-01094
位置：mod-tome.lua:12902；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
bone-link chain
```
译文：
```text
骨节锁链
```

## entry-01095
位置：mod-tome.lua:12926；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
This lantern of pale white crystal holds a sphere of darkness, that yet emanates light. Everywhere it shines, darkness vanishes entirely.
```
译文：
```text
这个灰白色水晶制成的灯笼中盛着一颗黑暗之球，却仍放射着光芒。光之所在，黑暗尽除。
```

## entry-01096
位置：mod-tome.lua:12927；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Absorbs all darkness (power %d, based on Willpower and Cunning) within its light radius, increasing its own brightness. (current charge %d).
```
译文：
```text
在光照范围内吸收所有黑暗(强度 %d，基于意志和灵巧) 并增加亮度(当前增幅：%d)。
```

## entry-01097
位置：mod-tome.lua:12929；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
release absorbed darkness in a %d radius cone with a %d%% chance to blind (based on lite radius), dealing %0.2f darkness damage (based on Mindpower and charge)
```
译文：
```text
在%d码的锥形范围内释放吸收的黑暗，有 %d%% 几率致盲（基于光照半径），并造成 %0.2f 暗影伤害（基于精神强度和吸收量）
```

## entry-01098
位置：mod-tome.lua:12930；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s unshutters %s %s, unleashing a torrent of shadows!
```
译文：
```text
%s打开了%s%s，释放出一股暗影洪流！
```

## entry-01099
位置：mod-tome.lua:12932；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
ethereal blue lantern
```
译文：
```text
飘渺的蓝色灯笼
```

## entry-01100
位置：mod-tome.lua:12935；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Not enough space to summon!
```
译文：
```text
没有足够的空间召唤！
```

## entry-01101
位置：mod-tome.lua:12938；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# releases an icy whisp from %s %s!
```
译文：
```text
#Source#从%s%s中放出寒冷鬼火！
```

## entry-01102
位置：mod-tome.lua:12949；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#Source# uses %s to summon a natural guardian!
```
译文：
```text
#Source#使用%s召唤自然守卫者！
```

## entry-01103
位置：mod-tome.lua:12950；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
Cloth of Dreams
```
译文：
```text
梦幻披风
```

## entry-01104
位置：mod-tome.lua:12956；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
release a radius %d burst of void energy at up to range %d, dealing %0.2f temporal and %0.2f darkness damage (based on Magic)
```
译文：
```text
释放一片半径 %d 的虚空能量爆发，最远可及 %d 码距离，造成 %0.2f 时空和 %0.2f 暗影伤害。（基于魔法）
```

## entry-01105
位置：mod-tome.lua:12957；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s siphons space and time into %s %s!
```
译文：
```text
%s将时空吸收入%s%s！
```

## entry-01106
位置：mod-tome.lua:12968；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You find yourself constantly fighting an urge to handle this strange pouch of shot.
```
译文：
```text
你发现自己在不断抵抗摆弄这袋奇异弹丸的冲动。
```

## entry-01107
位置：mod-tome.lua:12994；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Casts lasers on spellcast when worn or imbued.
```
译文：
```text
当装备或镶嵌时，施放法术时附加激光。
```

## entry-01108
位置：mod-tome.lua:13004；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s merges with %s %s!
```
译文：
```text
%s与%s%s合并！
```

## entry-01109
位置：mod-tome.lua:13006；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
This small wooden ring has a single green stem wrapped around it. Thin leaves still seem to be growing from it.
```
译文：
```text
这枚小巧的木戒上缠绕着一根绿色的茎，纤薄的叶片似乎仍在从中生长。
```

## entry-01110
位置：mod-tome.lua:13010；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
This thick cloak is incredibly tough, yet bends and flows with ease.
```
译文：
```text
这件厚重的斗篷坚韧异常，却依然能轻松地弯折垂流。
```

## entry-01111
位置：mod-tome.lua:13022；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
This hourglass of otherworldly crystal appears to be filled with countless tiny gemstones in place of sand. As they fall, you feel the flow of time change around you.
```
译文：
```text
这只异界水晶制成的沙漏里装载着无数细小的宝石，用以代替沙子。当它们落下时，你能感受到你周围时间的流动发生变化。
```

## entry-01112
位置：mod-tome.lua:13028；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#GOLD#The sands slowly begin falling towards %s.
```
译文：
```text
#GOLD#沙子慢慢流向%s。
```

## entry-01113
位置：mod-tome.lua:13045；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
This smooth green crystal flows with a light green slime in its core. Droplets occasionally form on its surface, tufts of grass growing quickly on the ground where they fall.
```
译文：
```text
光滑的绿色晶体，内部流动着浅绿色的黏液。偶尔有液滴在其表面凝结，滴落处的地面很快长出几簇青草。
```

## entry-01114
位置：mod-tome.lua:13079；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
This rugged jacket is the subject of many a rural legend.
Some say it was fashioned by an adventurous mage turned rogue, in times before the Spellblaze, but was since lost.
All manner of shady gamblers have since claimed to have worn it at one point or another. To fail, but live, is what it means to be untouchable, they said.
```
译文：
```text
这件破旧的夹克是许多乡村传说的主角。
有人说，在魔法大爆炸之前的年代，一位转行盗贼的冒险法师制作了它，但此后便遗失了。
形形色色的神秘赌徒都声称自己曾穿过它。他们说，失败却活下来，这就是“不可触及”的含义。
```

## entry-01116
位置：mod-tome.lua:13089；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
This green robe is engraved with icons showing clouds and swirling winds. Its original owner, a powerful mage named Proccala, was often revered for both his great benevolence and his intense power when it proved necessary.
```
译文：
```text
这件绿色长袍上刻有云朵和旋风的图案。它最初的主人，大法师普偌卡拉，因其善行和力量被人们敬畏。
```

## entry-01117
位置：mod-tome.lua:13105；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Forget the moons, the starry sky,
The warm and greeting sheen of sun,
The rays of light will never reach inside,
The heart which wishes that it be unseen.
```
译文：
```text
忘却明月，忘却星空，
忘却那温暖相迎的日辉；
光线永远照不进
那颗但愿不被看见的心。
```

## entry-01118
位置：mod-tome.lua:13120；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
This impossibly cold chain of frost-coated metal radiates a strange and imposing aura.
```
译文：
```text
这不可思议的金属链覆盖着极度寒霜，向外放射出诡异而强大的光环能量。
```

## entry-01119
位置：mod-tome.lua:13124；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The blade of this sword seems to have been forged of a mixture of voratun and stralite, resulting in a blend of swirling light and darkness.
```
译文：
```text
这柄长剑似乎是用沃瑞钽和斯莱特混合制成，光与暗在不断旋转交融。
```

## entry-01120
位置：mod-tome.lua:13125；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
release a burst of light and dark damage (scales with Magic)
```
译文：
```text
爆发光明和黑暗伤害（受魔法加成）
```

## entry-01121
位置：mod-tome.lua:13136；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
25% chance to strike the target again.
```
译文：
```text
25%几率再次攻击。
```

## entry-01122
位置：mod-tome.lua:13143；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Enter a Rampage (Shared cooldown).
```
译文：
```text
进入暴走（共享冷却时间）。
```

## entry-01123
位置：mod-tome.lua:13150；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
These cracked boots are caked with a thick layer of mud. It isn't clear who they previously belonged to, but they've clearly seen extensive use.
```
译文：
```text
这双裂纹遍布的靴子上糊着厚厚一层泥浆。不清楚它以前属于谁，但显然经历过大量的使用。
```

## entry-01124
位置：mod-tome.lua:13151；section：mod-tome/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
boost movement speed by 300% for up to 5 turns (or until you perform a non-movement action)
```
译文：
```text
增加移动速度300%，最多持续五回合。（任何非移动行动会打断这个效果）
```

## 相关术语快照
```tsv
Crush	压碎	T.GAME.TALENT	talents	talent name	existing	core	
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Mindpower	精神强度	T.GAME.STAT	combat	tformat	preferred	multi	技能与物品机制说明中的精神强度属性；与 Willpower“意志”区分
Name	名称	T.UI.LABEL	ui	_t	preferred	global	界面标签（17 处）
Not enough space to summon!	没有足够的空间召唤。	T.RUNTIME.LOG	combat	logSeen	preferred	global	召唤失败日志（22 处）
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Rogue	盗贼	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Spellhunt	魔法狩猎	T.PN.WORLD	places	_t	preferred	global	黄昏纪对法师的迫害事件；与 Spellblaze“魔法大爆炸”区分
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Willpower	意志	T.GAME.STAT	combat	stat name	existing	global	
antimagic	反魔法	T.GAME.EFFECT	combat	effect subtype	existing	global	
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blind	致盲	T.GAME.EFFECT	combat	effect subtype	existing	global	
cold	寒冷	T.GAME.DAMAGE	combat	damage type	existing	core	
cold	寒冷	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
natural	自然	T.GAME.ENTITY	creatures	entity type	preferred	core	自然类陷阱的实体类型；entity keyword 语境可指“自然主义者”
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
spellblaze	魔法大爆炸	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
spellblaze	魔法大爆炸	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与世界事件的其他标签区分
spellblaze	魔法大爆炸	T.PN.WORLD	places	effect subtype	existing	core	
stone	石化	T.GAME.EFFECT	combat	_t	preferred	core	状态免疫面板 Stoning Resistance；与石化毒素（nature 伤害变体）同词根
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stralite	斯莱特	T.GAME.ENTITY	items	nil	preferred	global	高阶金属材质名；统一装备全名、材质短名、材料块及叙事引用，不使用少数旧条目的“蓝皓石”
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
temporal	时空	T.GAME.DAMAGE	combat	damage type	existing	core	
temporal	时空	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
voratun	沃瑞钽	T.GAME.ENTITY	items	entity subtype	preferred	global	最高级金属材料（22 处）；与 iron 铁、steel 钢并列
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
