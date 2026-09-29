# batch-097：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-03252
位置：mod-tome.lua:42572；section：mod-tome/dialogs/debug/CreateItem.lua；source_tag：log；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#OBJECT:#LAST# %s%s: #LIGHT_BLUE#[%s] %s {%s, slot %s} at (%s, %s)#LAST#
```
译文：
```text
#LIGHT_BLUE#物品：#LAST# %s%s: #LIGHT_BLUE#[%s] %s {%s，槽位 %s} 位于 (%s, %s)#LAST#
```

## entry-03253
位置：mod-tome.lua:42613；section：mod-tome/dialogs/debug/DebugMain.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Remove all (non-party) creatures or kill them for the player (awards experience and drops loot)?
```
译文：
```text
移除所有（队伍外）的生物，还是替玩家将其击杀（给予经验并掉落战利品）？
```

## entry-03254
位置：mod-tome.lua:42645；section：mod-tome/dialogs/debug/Endgamify.lua；source_tag：log；args_order：None；special：None

原文：
```text
#ORANGE# Create Object: Unable to load all objects from file %s:#GREY#
 %s
```
译文：
```text
#ORANGE# 创建物品：无法读取文件%s的所有物品：#GREY#
 %s
```

## entry-03255
位置：mod-tome.lua:42658；section：mod-tome/dialogs/debug/PlotTalent.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Values plot for: %s (mastery %0.1f)
```
译文：
```text
技能数值属性表：%s (技能树系数 %0.1f)
```

## entry-03256
位置：mod-tome.lua:42659；section：mod-tome/dialogs/debug/PlotTalent.lua；source_tag：_t；args_order：None；special：None

原文：
```text
TL: 
```
译文：
```text
技能等级： 
```

## entry-03257
位置：mod-tome.lua:42664；section：mod-tome/dialogs/debug/RandomActor.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#(From %s, line %s):#LAST#
```
译文：
```text
#LIGHT_GREEN#(来自 %s，第%s行):#LAST#
```

## entry-03258
位置：mod-tome.lua:42666；section：mod-tome/dialogs/debug/RandomActor.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Randomly generate actors subject to a filter and/or create random bosses according to a data table.
Filters are interpreted by game.zone:checkFilter.
#ORANGE#Boss Data:#LAST# is interpreted by game.state:createRandomBoss, game.state:applyRandomClass, and Actor.levelupClass.
Generation is performed within the _G environment (used by the Lua Console) using the current zone's #LIGHT_GREEN#npc_list#LAST#.
Press #GOLD#'F1'#LAST# for help.
Mouse over controls for an actor preview (which may be further adjusted when placed on to the level).
(Press #GOLD#'L'#LAST# to lua inspect or #GOLD#'C'#LAST# to open the character sheet.)

The #LIGHT_BLUE#Base Filter#LAST# is used to filter the actor randomly generated.
```
译文：
```text
根据给定的筛选器随机生成角色，或/并根据给定的数据表生成随机Boss。
筛选器由game.zone:checkFilter处理。
#ORANGE#Boss数据：#LAST#由 game.state:createRandomBoss, game.state:applyRandomClass, 和 Actor.levelupClass处理。
生成过程在 _G 环境下进行（也是 Lua 控制台使用的环境），并使用当前地图的#LIGHT_GREEN#npc_list#LAST#。
请按#GOLD#'F1'#LAST#获得帮助。
鼠标移动查看角色预览（放置到楼层时可能会被进一步调整）。
（请按 #GOLD#'L'#LAST# 在Lua中检查，或按 #GOLD#'C'#LAST# 打开角色面板）

#LIGHT_BLUE#基础过滤器#LAST#用于过滤生成的随机角色。
```

## entry-03259
位置：mod-tome.lua:42684；section：mod-tome/dialogs/debug/RandomActor.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Current Base Actor: %s
```
译文：
```text
目前基础角色：%s
```

## entry-03260
位置：mod-tome.lua:42686；section：mod-tome/dialogs/debug/RandomActor.lua；source_tag：log；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# Current base actor: %s
```
译文：
```text
#LIGHT_BLUE# 目前基础角色：%s
```

## entry-03261
位置：mod-tome.lua:42691；section：mod-tome/dialogs/debug/RandomActor.lua；source_tag：log；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# Clear base actor: %s
```
译文：
```text
#LIGHT_BLUE# 清除基础角色：%s
```

## entry-03262
位置：mod-tome.lua:42692；section：mod-tome/dialogs/debug/RandomActor.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#Base Filter:#LAST# 
```
译文：
```text
#LIGHT_BLUE#基础筛选器：#LAST# 
```

## entry-03263
位置：mod-tome.lua:42693；section：mod-tome/dialogs/debug/RandomActor.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The #ORANGE#Boss Data#LAST# is used to transform the base actor into a random boss (which will use a random actor if needed).
```
译文：
```text
#ORANGE#Boss 数据#LAST#用于将基础角色转换成一个随机boss（如果需要的话，也可以用随机角色作为基础）。
```

## entry-03264
位置：mod-tome.lua:42694；section：mod-tome/dialogs/debug/RandomActor.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Current Boss Actor: %s
```
译文：
```text
目前Boss角色：%s
```

## entry-03265
位置：mod-tome.lua:42697；section：mod-tome/dialogs/debug/RandomActor.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#ORANGE#Boss Data:#LAST# 
```
译文：
```text
#ORANGE#Boss数据：#LAST# 
```

## entry-03266
位置：mod-tome.lua:42704；section：mod-tome/dialogs/debug/RandomActor.lua；source_tag：log；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#Bad filter for base actor: %s
```
译文：
```text
#LIGHT_BLUE#基础角色筛选器错误：%s
```

## entry-03267
位置：mod-tome.lua:42705；section：mod-tome/dialogs/debug/RandomActor.lua；source_tag：log；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#Could not generate a base actor with filter: %s
```
译文：
```text
#LIGHT_BLUE#无法使用以下筛选器生成基础角色：%s
```

## entry-03268
位置：mod-tome.lua:42706；section：mod-tome/dialogs/debug/RandomActor.lua；source_tag：log；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#Base actor could not be generated with filter [%s].
 Error:%s
```
译文：
```text
#LIGHT_BLUE#无法使用以下筛选器生成基础角色[%s]。
 错误：%s
```

## entry-03269
位置：mod-tome.lua:42709；section：mod-tome/dialogs/debug/RandomActor.lua；source_tag：log；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#Bad data for random boss actor: %s
```
译文：
```text
#LIGHT_BLUE#随机Boss数据错误：%s
```

## entry-03270
位置：mod-tome.lua:42710；section：mod-tome/dialogs/debug/RandomActor.lua；source_tag：log；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#Could not generate a base actor with data: %s
```
译文：
```text
#LIGHT_BLUE#无法使用以下数据生成基础角色：%s
```

## entry-03271
位置：mod-tome.lua:42718；section：mod-tome/dialogs/debug/RandomObject.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#(From %-10.60s, line: %s):#LAST#
```
译文：
```text
#LIGHT_GREEN#(来自 %-10.60s, 行数：%s):#LAST#
```

## entry-03272
位置：mod-tome.lua:42735；section：mod-tome/dialogs/debug/RandomObject.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Generate objects randomly subject to filters and create Random Artifacts.
Use "Generate" to create objects for preview and inspection.
Use "Add Object" to choose where to put the object and add it to the game.
(Mouse over controls for a preview of the generated object/working Actor. (Press #GOLD#'L'#LAST# to lua inspect.)
#SALMON#Resolvers#LAST# act on the working actor (default: player) to generate a SINGLE object.
They use the #LIGHT_GREEN#Random filter#LAST# as input unless noted otherwise and control object destination.
Filters are interpreted by ToME and engine entity/object generation functions (game.zone:checkFilter, etc.).
Interpretation of tables is within the _G environment (used by the Lua Console) using the current zone's #YELLOW_GREEN#object_list#LAST#.
Hotkeys: #GOLD#'F1'#LAST# :: context sensitive help, #GOLD#'C'#LAST# :: Working Character Sheet, #GOLD#'I'#LAST# :: Working Character Inventory.

```
译文：
```text
按筛选器随机生成物品，并创建随机神器。
使用“生成”按钮生成物品用于预览和检查。
使用“添加物品”按钮选择将物品放到哪里，并将其加入游戏。
将鼠标悬停在控件上，可以预览生成的物品/使用的角色（请按#GOLD#'L'#LAST#键进行 Lua 检查）。
#SALMON#解析器#LAST#作用于工作角色（默认：玩家），用于生成单个物品。
除非特别说明，它们使用#LIGHT_GREEN#随机筛选器#LAST#作为输入，并决定物品的去向。
筛选器由ToME游戏引擎的实体/物品处理函数解析(game.zone:checkFilter等)。
解析将会工作在_G环境下，这也是Lua控制台的工作环境，并使用当前地图的#YELLOW_GREEN#object_list#LAST#。
热键：#GOLD#'F1'#LAST# :: 查看帮助，#GOLD#'C'#LAST# :: 工作角色的角色面板，#GOLD#'I'#LAST# :: 工作角色的物品栏。

```

## entry-03273
位置：mod-tome.lua:42754；section：mod-tome/dialogs/debug/RandomObject.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The #LIGHT_GREEN#Random Filter#LAST# controls random generation of a normal object.
```
译文：
```text
#LIGHT_GREEN#随机筛选器#LAST#用于控制随机生成一个普通物品。
```

## entry-03274
位置：mod-tome.lua:42763；section：mod-tome/dialogs/debug/RandomObject.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#Random Filter:#LAST# 
```
译文：
```text
#LIGHT_GREEN#随机筛选器：#LAST# 
```

## entry-03275
位置：mod-tome.lua:42766；section：mod-tome/dialogs/debug/RandomObject.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#Base Filter:#LAST# 
```
译文：
```text
#LIGHT_BLUE#基础筛选器：#LAST# 
```

## entry-03276
位置：mod-tome.lua:42767；section：mod-tome/dialogs/debug/RandomObject.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
#SALMON#Resolver selected:#LAST# 
```
译文：
```text
#SALMON#选定的解析器：#LAST# 
```

## entry-03277
位置：mod-tome.lua:42776；section：mod-tome/dialogs/debug/RandomObject.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#ORANGE#Randart Data:#LAST# 
```
译文：
```text
#ORANGE#随机神器数据：#LAST# 
```

## entry-03278
位置：mod-tome.lua:42780；section：mod-tome/dialogs/debug/RandomObject.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Set working actor: [%s] %s
```
译文：
```text
设置工作角色：[%s] %s
```

## entry-03279
位置：mod-tome.lua:42781；section：mod-tome/dialogs/debug/RandomObject.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Set working actor: [%s] %s%s
```
译文：
```text
设置工作角色：[%s] %s%s
```

## entry-03280
位置：mod-tome.lua:42782；section：mod-tome/dialogs/debug/RandomObject.lua；source_tag：_t；args_order：None；special：None

原文：
```text
 #LIGHT_GREEN#(player)#LAST#
```
译文：
```text
 #LIGHT_GREEN#（玩家）#LAST#
```

## entry-03281
位置：mod-tome.lua:42789；section：mod-tome/dialogs/debug/RandomObject.lua；source_tag：log；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# Generate Random object using resolver: %s
```
译文：
```text
#LIGHT_BLUE# 使用解析器生成随机物品：%s
```

## entry-03282
位置：mod-tome.lua:42790；section：mod-tome/dialogs/debug/RandomObject.lua；source_tag：log；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# New random%s object: %s
```
译文：
```text
#LIGHT_BLUE# 新随机%s 物品：%s
```

## entry-03283
位置：mod-tome.lua:42791；section：mod-tome/dialogs/debug/RandomObject.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
 (resolver: %s)
```
译文：
```text
 (解析器：%s)
```

## entry-03284
位置：mod-tome.lua:42792；section：mod-tome/dialogs/debug/RandomObject.lua；source_tag：log；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#Could not generate a random object with filter: %s
```
译文：
```text
#LIGHT_BLUE#无法使用以下筛选器生成随机物品：%s
```

## entry-03285
位置：mod-tome.lua:42793；section：mod-tome/dialogs/debug/RandomObject.lua；source_tag：log；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#ERROR generating random object with filter [%s].
 Error: %s
```
译文：
```text
#LIGHT_BLUE#错误：使用该筛选器生成随机物品时发生错误[%s]。
 错误：%s
```

## entry-03286
位置：mod-tome.lua:42796；section：mod-tome/dialogs/debug/RandomObject.lua；source_tag：log；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#Could not generate a base object with filter: %s
```
译文：
```text
#LIGHT_BLUE#无法使用该筛选器生成基础物品：%s
```

## entry-03287
位置：mod-tome.lua:42797；section：mod-tome/dialogs/debug/RandomObject.lua；source_tag：log；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#ERROR generating base object with filter [%s].
 Error:%s
```
译文：
```text
#LIGHT_BLUE#错误：使用该筛选器生成基础物品时发生错误 [%s]。
 错误：%s
```

## entry-03288
位置：mod-tome.lua:42800；section：mod-tome/dialogs/debug/RandomObject.lua；source_tag：log；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#Could not generate a Randart with data: %s
```
译文：
```text
#LIGHT_BLUE#无法使用数据生成随机神器：%s
```

## entry-03289
位置：mod-tome.lua:42805；section：mod-tome/dialogs/debug/RandomObject.lua；source_tag：log；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#ERROR accepting object with resolver %s.
 Error:%s
```
译文：
```text
#LIGHT_BLUE#使用解析器%s接受物品时出错。
 错误：%s
```

## entry-03290
位置：mod-tome.lua:42808；section：mod-tome/dialogs/debug/RandomObject.lua；source_tag：log；args_order：None；special：None

原文：
```text
#LIGHT_BLUE#Working Actor set to [%s]%s at (%d, %d)
```
译文：
```text
#LIGHT_BLUE#将工作角色设置为[%s]%s 位于(%d, %d)
```

## entry-03291
位置：mod-tome.lua:42819；section：mod-tome/dialogs/debug/SummonCreature.lua；source_tag：log；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# no actor to place.
```
译文：
```text
#LIGHT_BLUE#没有待放置的角色。
```

## 相关术语快照
```tsv
Resolve	坚定意志	T.GAME.TALENT	talents	talent name	existing	core	反魔技能名；与同名临时效果及状态日志统一
class	职业	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
iron	铁	T.GAME.ENTITY	items	entity subtype	preferred	global	基础金属材料（22 处）
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
tome	书册	T.GAME.ENTITY	items	entity subtype	existing	global	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
