# batch-005：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-00161
位置：mod-example_realtime.lua:19；section：mod-example_realtime/class/Game.lua；source_tag：log；args_order：None；special：None

原文：
```text
Saving game...
```
译文：
```text
保存游戏…
```

## entry-00162
位置：mod-example_realtime.lua:25；section：mod-example_realtime/class/Player.lua；source_tag：_t；args_order：None；special：None

原文：
```text
LOW HEALTH!
```
译文：
```text
生命值低！
```

## entry-00163
位置：mod-example_realtime.lua:44；section：mod-example_realtime/data/damage_types.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Kill!
```
译文：
```text
击杀！
```

## entry-00164
位置：mod-tome.lua:103；section：mod-tome/class/Actor.lua；source_tag：log；args_order：None；special：None

原文：
```text
#VIOLET#Following build order %s; increasing %s by 1.
```
译文：
```text
#VIOLET#遵循加点顺序%s;增加一点%s。
```

## entry-00165
位置：mod-tome.lua:104；section：mod-tome/class/Actor.lua；source_tag：log；args_order：None；special：None

原文：
```text
#VIOLET#Following build order %s; learning talent category %s.
```
译文：
```text
#VIOLET#遵循加点顺序%s;学会技能树%s。
```

## entry-00166
位置：mod-tome.lua:105；section：mod-tome/class/Actor.lua；source_tag：log；args_order：None；special：None

原文：
```text
#VIOLET#Following build order %s; learning talent %s.
```
译文：
```text
#VIOLET#遵循加点顺序%s;学会技能%s。
```

## entry-00167
位置：mod-tome.lua:111；section：mod-tome/class/Actor.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#CADET_BLUE#You notice a trap (%s)!
```
译文：
```text
#CADET_BLUE#你发现了一个陷阱（%s）！
```

## entry-00168
位置：mod-tome.lua:136；section：mod-tome/class/Actor.lua；source_tag：_t；args_order：None；special：None

原文：
```text
INVULNERABLE!
```
译文：
```text
无敌！
```

## entry-00169
位置：mod-tome.lua:138；section：mod-tome/class/Actor.lua；source_tag：tformat；args_order：None；special：None

原文：
```text

Mana:  %s%d / %d#LAST#
```
译文：
```text

法力值：%s%d / %d#LAST#
```

## entry-00170
位置：mod-tome.lua:140；section：mod-tome/class/Actor.lua；source_tag：tformat；args_order：None；special：None

原文：
```text

Vim:  %s%d / %d#LAST#
```
译文：
```text

活力值：%s%d / %d#LAST#
```

## entry-00171
位置：mod-tome.lua:142；section：mod-tome/class/Actor.lua；source_tag：tformat；args_order：None；special：None

原文：
```text

Positive:  %s%d / %d#LAST#
```
译文：
```text

正能量值：%s%d / %d#LAST#
```

## entry-00172
位置：mod-tome.lua:144；section：mod-tome/class/Actor.lua；source_tag：tformat；args_order：None；special：None

原文：
```text

Negative:  %s%d / %d#LAST#
```
译文：
```text

负能量值：%s%d / %d#LAST#
```

## entry-00173
位置：mod-tome.lua:148；section：mod-tome/class/Actor.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
#ffa0ff#Predator: +%d acc, +%d apr#LAST#
```
译文：
```text
#ffa0ff#猎杀者：+%d 命中，+%d 护甲穿透#LAST#
```

## entry-00174
位置：mod-tome.lua:162；section：mod-tome/class/Actor.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#Main:#LAST#%s
```
译文：
```text
#LIGHT_BLUE#主手：#LAST#%s
```

## entry-00175
位置：mod-tome.lua:163；section：mod-tome/class/Actor.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#Off :#LAST#%s
```
译文：
```text
#LIGHT_BLUE#副手：#LAST#%s
```

## entry-00176
位置：mod-tome.lua:164；section：mod-tome/class/Actor.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#Psi :#LAST#%s
```
译文：
```text
#LIGHT_BLUE#灵能：#LAST#%s
```

## entry-00177
位置：mod-tome.lua:165；section：mod-tome/class/Actor.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#Ammo:#LAST#%s
```
译文：
```text
#LIGHT_BLUE#弹药：#LAST#%s
```

## entry-00178
位置：mod-tome.lua:166；section：mod-tome/class/Actor.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#Unarmed:#LAST#%s
```
译文：
```text
#LIGHT_BLUE#徒手：#LAST#%s
```

## entry-00179
位置：mod-tome.lua:167；section：mod-tome/class/Actor.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#Unarmed:#LAST#
```
译文：
```text
#LIGHT_BLUE#徒手：#LAST#
```

## entry-00180
位置：mod-tome.lua:179；section：mod-tome/class/Actor.lua；source_tag：delayedLogMessage；args_order：None；special：None

原文：
```text
#DARK_GREEN##Source# shares damage with %s oozes!
```
译文：
```text
#DARK_GREEN##Source#和%s软泥怪平分伤害！
```

## entry-00181
位置：mod-tome.lua:180；section：mod-tome/class/Actor.lua；source_tag：delayedLogMessage；args_order：None；special：None

原文：
```text
#CRIMSON##Source# teleports some damage to #Target#!
```
译文：
```text
#CRIMSON##Source#将部分伤害转移给#Target#！
```

## entry-00182
位置：mod-tome.lua:206；section：mod-tome/class/Actor.lua；source_tag：delayedLogMessage；args_order：None；special：None

原文：
```text
#CRIMSON##Source# steals life from #Target#!
```
译文：
```text
#CRIMSON##Source#从#Target#处偷取生命！
```

## entry-00183
位置：mod-tome.lua:214；section：mod-tome/class/Actor.lua；source_tag：_t；args_order：None；special：None

原文：
```text
RESURRECT!
```
译文：
```text
复活！
```

## entry-00184
位置：mod-tome.lua:225；section：mod-tome/class/Actor.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You have achieved #LIGHT_GREEN#level 50#WHITE#, congratulations!

This level is special, it granted you #LIGHT_GREEN#10#WHITE# more stat points, #LIGHT_GREEN#3#WHITE# more class talent points and #LIGHT_GREEN#3#WHITE# more generic talent points.
Now go forward boldly and triumph!
```
译文：
```text
你达到了#LIGHT_GREEN#等级 50#WHITE#，祝贺你！
这个等级很特殊，你可以得到额外的#LIGHT_GREEN#10#WHITE#点属性点，#LIGHT_GREEN#3#WHITE#点职业技能点和#LIGHT_GREEN#3#WHITE#点通用技能点。
现在，勇敢的向前并取得最终的胜利吧！
```

## entry-00185
位置：mod-tome.lua:232；section：mod-tome/class/Actor.lua；source_tag：log；args_order：None；special：None

原文：
```text
#00ffff#Welcome to level %d [%s].
```
译文：
```text
#00ffff#欢迎来到等级 %d [ %s ]。
```

## entry-00186
位置：mod-tome.lua:233；section：mod-tome/class/Actor.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Press p to use them.
```
译文：
```text
请按 P 键使用它们。
```

## entry-00187
位置：mod-tome.lua:234；section：mod-tome/class/Actor.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Select %s in the party list and press G to use them.
```
译文：
```text
请选择队伍里的%s，按 G 键使用它们。
```

## entry-00188
位置：mod-tome.lua:241；section：mod-tome/class/Actor.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#AQUAMARINE#You have gained one more life (%d remaining).
```
译文：
```text
#AQUAMARINE#你额外获得了一条命（剩余生命数：%d）。
```

## entry-00189
位置：mod-tome.lua:244；section：mod-tome/class/Actor.lua；source_tag：_t；args_order：None；special：None

原文：
```text
+ENCUMBERED!
```
译文：
```text
+超重！
```

## entry-00190
位置：mod-tome.lua:246；section：mod-tome/class/Actor.lua；source_tag：_t；args_order：None；special：None

原文：
```text
-ENCUMBERED!
```
译文：
```text
-超重！
```

## entry-00191
位置：mod-tome.lua:249；section：mod-tome/class/Actor.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s warps space-time to equip: %s.
```
译文：
```text
%s扭曲空间，切换武器至：%s。
```

## entry-00192
位置：mod-tome.lua:256；section：mod-tome/class/Actor.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#STEEL_BLUE#You've moved to another time thread.
```
译文：
```text
#STEEL_BLUE#你移动到了另一条时间线。
```

## entry-00193
位置：mod-tome.lua:258；section：mod-tome/class/Actor.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_RED#You feel the edges of spacetime begin to ripple and bend!
```
译文：
```text
#LIGHT_RED#你感到时空的边际开始弯曲振荡！
```

## entry-00194
位置：mod-tome.lua:261；section：mod-tome/class/Actor.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#Spacetime has calmed...  somewhat.
```
译文：
```text
#LIGHT_BLUE#时空稍微稳定了些……
```

## entry-00195
位置：mod-tome.lua:277；section：mod-tome/class/Actor.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You do not have enough %s to use %s.
```
译文：
```text
你没有足够的%s施展：%s。
```

## entry-00196
位置：mod-tome.lua:284；section：mod-tome/class/Actor.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s fumbles and fails to use %s, injuring %s!
```
译文：
```text
%s使用%s失败，还弄伤了%s！
```

## entry-00197
位置：mod-tome.lua:328；section：mod-tome/class/Actor.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
%s will now be used as often as possible automatically.
```
译文：
```text
%s将会尽可能多地自动使用。
```

## entry-00198
位置：mod-tome.lua:353；section：mod-tome/class/Actor.lua；source_tag：_t；args_order：None；special：None

原文：
```text
but fumbles!
```
译文：
```text
但是失败了！
```

## entry-00199
位置：mod-tome.lua:354；section：mod-tome/class/Actor.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
to the %s!
```
译文：
```text
到%s！
```

## entry-00200
位置：mod-tome.lua:358；section：mod-tome/class/Actor.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You can not drop items while sleeping.
```
译文：
```text
你不能在睡眠状态下丢弃物品。
```

## 相关术语快照
```tsv
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Psi	灵能值	T.GAME.RESOURCE	resources	_t	existing	core	
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Vim	活力值	T.GAME.RESOURCE	resources	_t	existing	core	
ammo	弹药	T.GAME.ENTITY	items	entity type	existing	core	
class	职业	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
sleep	睡眠	T.GAME.EFFECT	combat	effect subtype	existing	global	
steel	钢	T.GAME.ENTITY	items	entity subtype	preferred	global	二级金属材料（18 处）
teleport	传送	T.GAME.EFFECT	combat	effect subtype	existing	global	
trap	陷阱	T.GAME.ENTITY	items	entity name	preferred	global	陷阱实体（20 处）
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
