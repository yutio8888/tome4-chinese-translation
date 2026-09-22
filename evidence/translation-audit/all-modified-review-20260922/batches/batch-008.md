# batch-008：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-00281
位置：mod-tome.lua:963；section：mod-tome/class/Object.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Learn shield attack talent or enable 'Always show shield combat' to see combat stats.
```
译文：
```text
学习盾牌攻击技能，或者开启 '强制显示盾牌战斗数据' 选项来查看战斗数据。
```

## entry-00282
位置：mod-tome.lua:984；section：mod-tome/class/Object.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Talent level: %+d %s.
```
译文：
```text
技能等级：%+d %s。
```

## entry-00283
位置：mod-tome.lua:985；section：mod-tome/class/Object.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Talent level: %s.
```
译文：
```text
技能等级：%s。
```

## entry-00284
位置：mod-tome.lua:986；section：mod-tome/class/Object.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Talent on hit(spell): %s (%d%% chance level %d).
```
译文：
```text
技能（法术）命中后释放：%s (%d%% 几率等级 %d)。
```

## entry-00285
位置：mod-tome.lua:987；section：mod-tome/class/Object.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Talent on hit(nature): %s (%d%% chance level %d).
```
译文：
```text
技能（自然）命中后释放：%s (%d%% 几率等级 %d)。
```

## entry-00286
位置：mod-tome.lua:988；section：mod-tome/class/Object.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Talent on hit(mindpower): %s (%d%% chance level %d).
```
译文：
```text
技能（精神）命中后释放：%s (%d%% 几率等级 %d)。
```

## entry-00287
位置：mod-tome.lua:1005；section：mod-tome/class/Object.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
%d out of %d/%d.
```
译文：
```text
%d，总计%d/%d。
```

## entry-00288
位置：mod-tome.lua:1031；section：mod-tome/class/Object.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
This object's appearance was changed to %s
```
译文：
```text
这个物品的外观被改变为 %s。
```

## entry-00289
位置：mod-tome.lua:1032；section：mod-tome/class/Object.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Press <control> to compare
```
译文：
```text
按住 Ctrl 键比较
```

## entry-00290
位置：mod-tome.lua:1048；section：mod-tome/class/Party.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#MOCCASIN#Character control switched to %s.
```
译文：
```text
#MOCCASIN#角色切换至 %s。
```

## entry-00291
位置：mod-tome.lua:1058；section：mod-tome/class/Party.lua；source_tag：log；args_order：None；special：None

原文：
```text
%s is dismissed!
```
译文：
```text
%s 被遣散了！
```

## entry-00292
位置：mod-tome.lua:1063；section：mod-tome/class/Party.lua；source_tag：_t；args_order：None；special：None

原文：
```text
close
```
译文：
```text
较近了
```

## entry-00293
位置：mod-tome.lua:1079；section：mod-tome/class/Player.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Level change (%s)!
```
译文：
```text
地图切换 (%s)！
```

## entry-00294
位置：mod-tome.lua:1086；section：mod-tome/class/Player.lua；source_tag：_t；args_order：None；special：None

原文：
```text
LOW HEALTH!
```
译文：
```text
生命值低！
```

## entry-00295
位置：mod-tome.lua:1093；section：mod-tome/class/Player.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Automatic use of talent %s #DARK_RED#skipped#LAST#: cooldown too low (%d).
```
译文：
```text
%s 的自动施法被#DARK_RED#跳过#LAST#了：冷却时间太低(%d)。
```

## entry-00296
位置：mod-tome.lua:1097；section：mod-tome/class/Player.lua；source_tag：_t；args_order：None；special：None

原文：
```text
losing breath!
```
译文：
```text
窒息！
```

## entry-00297
位置：mod-tome.lua:1098；section：mod-tome/class/Player.lua；source_tag：_t；args_order：None；special：None

原文：
```text
losing health!
```
译文：
```text
生命值下降！
```

## entry-00298
位置：mod-tome.lua:1115；section：mod-tome/class/Player.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Your antimagic disrupts %s.
```
译文：
```text
你的反魔法技能打断了 %s。
```

## entry-00299
位置：mod-tome.lua:1116；section：mod-tome/class/Player.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your antimagic disrupts %s.
```
译文：
```text
你的反魔法技能打断了 %s。
```

## entry-00300
位置：mod-tome.lua:1123；section：mod-tome/class/Player.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You use the %s on the pedestal. There is a distant 'clonk' sound.
```
译文：
```text
你在基座上使用了 %s。你听到远处传来一声“咔嗒”声。
```

## entry-00301
位置：mod-tome.lua:1124；section：mod-tome/class/Player.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_RED#%s briefly catches sight of you!
```
译文：
```text
#LIGHT_RED#%s 短暂地瞥见了你！
```

## entry-00302
位置：mod-tome.lua:1132；section：mod-tome/class/Player.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#Accepted quest '%s'!#WHITE#(Press 'j' to see the quest log)
```
译文：
```text
#LIGHT_GREEN#接受了任务“%s”！#WHITE#（按 J 键查看任务日志）
```

## entry-00303
位置：mod-tome.lua:1133；section：mod-tome/class/Player.lua；source_tag：saySimple；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#Accepted quest '%s'!
```
译文：
```text
#LIGHT_GREEN#接受了任务“%s”！
```

## entry-00304
位置：mod-tome.lua:1134；section：mod-tome/class/Player.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#Quest '%s' status updated!#WHITE#(Press 'j' to see the quest log)
```
译文：
```text
#LIGHT_GREEN#任务“%s”状态已经更新！#WHITE#（按 J 键查看任务日志）
```

## entry-00305
位置：mod-tome.lua:1135；section：mod-tome/class/Player.lua；source_tag：saySimple；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#Quest '%s' updated!
```
译文：
```text
#LIGHT_GREEN#任务“%s”已更新！
```

## entry-00306
位置：mod-tome.lua:1136；section：mod-tome/class/Player.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#Quest '%s' completed!#WHITE#(Press 'j' to see the quest log)
```
译文：
```text
#LIGHT_GREEN#任务“%s”完成！#WHITE#（按 J 键查看任务日志）
```

## entry-00307
位置：mod-tome.lua:1137；section：mod-tome/class/Player.lua；source_tag：saySimple；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#Quest '%s' completed!
```
译文：
```text
#LIGHT_GREEN#任务“%s”已完成！
```

## entry-00308
位置：mod-tome.lua:1138；section：mod-tome/class/Player.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#Quest '%s' is done!#WHITE#(Press 'j' to see the quest log)
```
译文：
```text
#LIGHT_GREEN#任务“%s”完成！#WHITE#（按 J 键查看任务日志）
```

## entry-00309
位置：mod-tome.lua:1139；section：mod-tome/class/Player.lua；source_tag：saySimple；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#Quest '%s' done!
```
译文：
```text
#LIGHT_GREEN#任务“%s”已完成！
```

## entry-00310
位置：mod-tome.lua:1140；section：mod-tome/class/Player.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#LIGHT_RED#Quest '%s' is failed!#WHITE#(Press 'j' to see the quest log)
```
译文：
```text
#LIGHT_RED#任务“%s”失败！#WHITE#（按 J 键查看任务日志）
```

## entry-00311
位置：mod-tome.lua:1141；section：mod-tome/class/Player.lua；source_tag：saySimple；args_order：None；special：None

原文：
```text
#LIGHT_RED#Quest '%s' failed!
```
译文：
```text
#LIGHT_RED#任务“%s”失败了！
```

## entry-00312
位置：mod-tome.lua:1174；section：mod-tome/class/Store.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
This entity can not access inventories.
```
译文：
```text
该实体无法使用物品栏。
```

## entry-00313
位置：mod-tome.lua:1188；section：mod-tome/class/Trap.lua；source_tag：_t；args_order：None；special：None

原文：
```text
(beneficial)
```
译文：
```text
（有益）
```

## entry-00314
位置：mod-tome.lua:1189；section：mod-tome/class/Trap.lua；source_tag：_t；args_order：None；special：None

原文：
```text
(beneficial to enemies)
```
译文：
```text
（对敌人有益）
```

## entry-00315
位置：mod-tome.lua:1190；section：mod-tome/class/Trap.lua；source_tag：_t；args_order：None；special：None

原文：
```text
(safe)
```
译文：
```text
（安全）
```

## entry-00316
位置：mod-tome.lua:1201；section：mod-tome/class/Trap.lua；source_tag：_t；args_order：None；special：None

原文：
```text

#LIGHT_BLUE#Trap Description:#WHITE#

```
译文：
```text

#LIGHT_BLUE#陷阱说明：#WHITE#

```

## entry-00317
位置：mod-tome.lua:1213；section：mod-tome/class/Trap.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You set off the trap!
```
译文：
```text
你触发了陷阱！
```

## entry-00318
位置：mod-tome.lua:1223；section：mod-tome/class/Trap.lua；source_tag：log；args_order：None；special：None

原文：
```text
#CADET_BLUE#You %s a trap (%s).
```
译文：
```text
#CADET_BLUE#你%s了一个陷阱(%s)。
```

## entry-00319
位置：mod-tome.lua:1231；section：mod-tome/class/UserChatExtension.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
#ANTIQUE_WHITE#has linked an item: #WHITE# %s
```
译文：
```text
#ANTIQUE_WHITE#链接了一件物品：#WHITE# %s
```

## entry-00320
位置：mod-tome.lua:1232；section：mod-tome/class/UserChatExtension.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
#ANTIQUE_WHITE#has linked a creature: #WHITE# %s
```
译文：
```text
#ANTIQUE_WHITE#链接了一个生物：#WHITE# %s
```

## 相关术语快照
```tsv
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mindpower	精神强度	T.GAME.STAT	combat	tformat	preferred	multi	技能与物品机制说明中的精神强度属性；与 Willpower“意志”区分
antimagic	反魔法	T.GAME.EFFECT	combat	effect subtype	existing	global	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
trap	陷阱	T.GAME.ENTITY	items	entity name	preferred	global	陷阱实体（20 处）
```
