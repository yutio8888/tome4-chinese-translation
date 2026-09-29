# batch-006：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-00201
位置：mod-tome.lua:359；section：mod-tome/class/Actor.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You can not drop %s (plot item).
```
译文：
```text
你不能丢弃%s（剧情物品）。
```

## entry-00202
位置：mod-tome.lua:360；section：mod-tome/class/Actor.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You can not drop %s (tagged).
```
译文：
```text
你不能丢弃%s（已被标记）。
```

## entry-00203
位置：mod-tome.lua:368；section：mod-tome/class/Actor.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot change your equipment while sleeping!
```
译文：
```text
你不能在睡眠中切换装备！
```

## entry-00204
位置：mod-tome.lua:369；section：mod-tome/class/Actor.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You cannot change your equipment!
```
译文：
```text
你不能切换装备！
```

## entry-00205
位置：mod-tome.lua:375；section：mod-tome/class/Actor.lua；source_tag：_t；args_order：None；special：None

原文：
```text
When you close the inventory window, all items in the chest will be transmogrified.
```
译文：
```text
当你关闭物品栏的时候，所有在转化之盒里的物品都会被自动转化。
```

## entry-00206
位置：mod-tome.lua:378；section：mod-tome/class/Actor.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You can not use a tinker without the corresponding item.
```
译文：
```text
你不能在没有相关物品时使用配件。
```

## entry-00207
位置：mod-tome.lua:379；section：mod-tome/class/Actor.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
This item is not usable: %s.
```
译文：
```text
该物品不能使用：%s。
```

## entry-00208
位置：mod-tome.lua:380；section：mod-tome/class/Actor.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
This tinker can not be applied to this item.
```
译文：
```text
这个配件不能装在该物品上。
```

## entry-00209
位置：mod-tome.lua:381；section：mod-tome/class/Actor.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You already have a tinker on this item.
```
译文：
```text
这个物品上已经有了配件。
```

## entry-00210
位置：mod-tome.lua:382；section：mod-tome/class/Actor.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You attach %s to your %s.
```
译文：
```text
你将%s附着于%s。
```

## entry-00211
位置：mod-tome.lua:395；section：mod-tome/class/EscortRewards.lua；source_tag：_t；args_order：None；special：None

原文：
```text
%s, the lost warrior
```
译文：
```text
%s，迷路的战士
```

## entry-00212
位置：mod-tome.lua:398；section：mod-tome/class/EscortRewards.lua；source_tag：_t；args_order：None；special：None

原文：
```text
%s, the injured seer
```
译文：
```text
%s，受伤的先知
```

## entry-00213
位置：mod-tome.lua:400；section：mod-tome/class/EscortRewards.lua；source_tag：_t；args_order：None；special：None

原文：
```text
%s, the repented thief
```
译文：
```text
%s，忏悔的盗贼
```

## entry-00214
位置：mod-tome.lua:401；section：mod-tome/class/EscortRewards.lua；source_tag：_t；args_order：None；special：None

原文：
```text
%s, the lone alchemist
```
译文：
```text
%s，落单的炼金术师
```

## entry-00215
位置：mod-tome.lua:402；section：mod-tome/class/EscortRewards.lua；source_tag：_t；args_order：None；special：None

原文：
```text
%s, the lost sun paladin
```
译文：
```text
%s，迷路的太阳骑士
```

## entry-00216
位置：mod-tome.lua:403；section：mod-tome/class/EscortRewards.lua；source_tag：_t；args_order：None；special：None

原文：
```text
%s, the lost defiler
```
译文：
```text
%s，迷路的腐化者
```

## entry-00217
位置：mod-tome.lua:410；section：mod-tome/class/EscortRewards.lua；source_tag：_t；args_order：None；special：None

原文：
```text
%s, temporal explorer
```
译文：
```text
%s，时空旅行者
```

## entry-00218
位置：mod-tome.lua:412；section：mod-tome/class/EscortRewards.lua；source_tag：_t；args_order：None；special：None

原文：
```text
%s, the worried loremaster
```
译文：
```text
%s，担忧的贤者
```

## entry-00219
位置：mod-tome.lua:451；section：mod-tome/class/Game.lua；source_tag：_t；args_order：None；special：None

原文：
```text
<Scroll mode, press direction keys to scroll, press again to exit>
```
译文：
```text
<地图滚动模式，按方向键滚动地图，再次按键退出>
```

## entry-00220
位置：mod-tome.lua:462；section：mod-tome/class/Game.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
%s the %s %s
```
译文：
```text
%s，%s %s
```

## entry-00221
位置：mod-tome.lua:469；section：mod-tome/class/Game.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_RED#You may not change level without your own body!
```
译文：
```text
#LIGHT_RED#你只能用自己的身体离开地图！
```

## entry-00222
位置：mod-tome.lua:470；section：mod-tome/class/Game.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_RED#You may not leave the zone with this character!
```
译文：
```text
#LIGHT_RED#你不能用这个角色离开地图！
```

## entry-00223
位置：mod-tome.lua:471；section：mod-tome/class/Game.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_RED#You cannot escape your fate by leaving the level!
```
译文：
```text
#LIGHT_RED#你不能离开地图以求逃避命运！
```

## entry-00224
位置：mod-tome.lua:475；section：mod-tome/class/Game.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Debug the problem (move to the failed zone/level)
```
译文：
```text
调试问题（进入失败的地图/楼层）
```

## entry-00225
位置：mod-tome.lua:496；section：mod-tome/class/Game.lua；source_tag：logMessage；args_order：None；special：None

原文：
```text
#Source# hits #Target# for %s (#RED##{bold}#%0.0f#LAST##{normal}# total damage)%s.
```
译文：
```text
#Source#击中#Target#造成%s (#RED##{bold}#%0.0f#LAST##{normal}#合计伤害)%s。
```

## entry-00226
位置：mod-tome.lua:501；section：mod-tome/class/Game.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Kill (%d)!
```
译文：
```text
杀死 (%d)！
```

## entry-00227
位置：mod-tome.lua:503；section：mod-tome/class/Game.lua；source_tag：log；args_order：None；special：None

原文：
```text
Showing big healthbars and tactical borders.
```
译文：
```text
显示大血条+边框。
```

## entry-00228
位置：mod-tome.lua:504；section：mod-tome/class/Game.lua；source_tag：log；args_order：None；special：None

原文：
```text
Showing healthbars only.
```
译文：
```text
只显示血条信息。
```

## entry-00229
位置：mod-tome.lua:505；section：mod-tome/class/Game.lua；source_tag：log；args_order：None；special：None

原文：
```text
Showing no tactical information.
```
译文：
```text
不显示战术信息。
```

## entry-00230
位置：mod-tome.lua:506；section：mod-tome/class/Game.lua；source_tag：log；args_order：None；special：None

原文：
```text
Showing small healthbars and tactical borders.
```
译文：
```text
显示小血条+边框。
```

## entry-00231
位置：mod-tome.lua:510；section：mod-tome/class/Game.lua；source_tag：log；args_order：None；special：None

原文：
```text
You may not auto-explore with enemies in sight (%s to the %s%s)!
```
译文：
```text
当有敌人在视野里时，你不能自动探索！(%s 在 %s方%s)！
```

## entry-00232
位置：mod-tome.lua:532；section：mod-tome/class/Game.lua；source_tag：log；args_order：None；special：None

原文：
```text
Looking around... (direction keys to select interesting things, shift+direction keys to move freely)
```
译文：
```text
正在观察四周…（按方向键定位有趣的东西，按 Shift+方向键自由移动）
```

## entry-00233
位置：mod-tome.lua:533；section：mod-tome/class/Game.lua；source_tag：log；args_order：None；special：None

原文：
```text
Movement Mode: #LIGHT_GREEN#Default#LAST#.
```
译文：
```text
移动模式：#LIGHT_GREEN#默认#LAST#。
```

## entry-00234
位置：mod-tome.lua:534；section：mod-tome/class/Game.lua；source_tag：log；args_order：None；special：None

原文：
```text
Movement Mode: #LIGHT_RED#Passive#LAST#.
```
译文：
```text
移动模式：#LIGHT_RED#被动#LAST#。
```

## entry-00235
位置：mod-tome.lua:535；section：mod-tome/class/Game.lua；source_tag：log；args_order：None；special：None

原文：
```text
#GOLD#CHEAT MOVE ACTOR %s: ctrl+shift+alt+right click on an empty map spot to move it
```
译文：
```text
#GOLD#CHEAT MOVE ACTOR %s: Ctrl+Shift+Alt+右键点击地图上的空白位置来移动它
```

## entry-00236
位置：mod-tome.lua:540；section：mod-tome/class/Game.lua；source_tag：log；args_order：None；special：None

原文：
```text
Saving game...
```
译文：
```text
保存游戏…
```

## entry-00237
位置：mod-tome.lua:578；section：mod-tome/class/GameState.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Leave the level (to the next level) without killing a single creature. You will get #{italic}#two#{normal}# rewards.
```
译文：
```text
在不杀死任何怪物的情况下离开这一层（到达下一层）。你将得到#{italic}#两份#{normal}# 奖励。
```

## entry-00238
位置：mod-tome.lua:586；section：mod-tome/class/GameState.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Proceed directly to the next Infinite Dungeon level in less than %d turns (an exit is revealed on your map).
```
译文：
```text
在%d回合内到达无尽地下城的下一层（出口已标记在地图上）。
```

## entry-00239
位置：mod-tome.lua:587；section：mod-tome/class/GameState.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Turns left: #LIGHT_GREEN#%d
```
译文：
```text
剩余回合：#LIGHT_GREEN#%d
```

## entry-00240
位置：mod-tome.lua:588；section：mod-tome/class/GameState.lua；source_tag：log；args_order：None；special：None

原文：
```text

#ORCHID# Rush Hour: %s turns left!

```
译文：
```text

#ORCHID#决胜时刻：剩余%s回合！

```

## 相关术语快照
```tsv
Alchemist	炼金术师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Defiler	堕落系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Sun Paladin	太阳骑士	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Tinker	工匠系	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	
Warrior	战士系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“战士系”
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
infinite dungeon	无尽地下城	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
next level	前往下一层	T.GAME.ENTITY	places	entity name	preferred	global	楼梯/出口提示（19 处）
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
scroll	卷轴	T.GAME.ENTITY	items	entity type	existing	global	
sleep	睡眠	T.GAME.EFFECT	combat	effect subtype	existing	global	
tactic	战术	T.GAME.EFFECT	combat	effect subtype	existing	global	
tactical	战术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 tactic 同义的变体
temporal	时空	T.GAME.DAMAGE	combat	damage type	existing	core	
temporal	时空	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
tinker	蒸汽工具	T.GAME.ENTITY	items	entity type	existing	dlc	Embers of Rage 实体类型
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
