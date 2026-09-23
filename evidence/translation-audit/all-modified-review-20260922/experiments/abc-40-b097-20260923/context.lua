section "mod-tome/dialogs/debug/CreateItem.lua"

t("DEBUG -- Create Object", "调试 -- 创建物品", "_t")
t("Load from other zones ", "从其他地图读取 ", "_t")
t([[#ORANGE# Create Object: Unable to load all objects from file %s:#GREY#
 %s]], [[#ORANGE# 创建物品：无法读取文件%s的所有物品：#GREY#
 %s]], "log")
t("Generate examples (right-click refreshes) ", "创建样品（右键刷新） ", "_t")
t("#CRIMSON#==Resolved Example==#LAST#", "#CRIMSON#==解析样品==#LAST#", "_t")
t([[#LIGHT_BLUE#Object %s could not be generated or identified. Error:
%s]], [[#LIGHT_BLUE#物品%s无法被创建或鉴定。错误：
%s]], "log")
t("Object could not be resolved/identified.", "物品无法被解析或鉴定。", "_t")
t([[Error:
%s]], [[错误：
%s]], "tformat")
t("#LIGHT_BLUE#Could not add object to %s at (%d, %d)", "#LIGHT_BLUE#无法将物品添加到%s（位于(%d, %d)）", "log")
t("#LIGHT_BLUE#No creature to add object to at (%d, %d)", "#LIGHT_BLUE#在(%d, %d)上没有生物", "log")
t("#LIGHT_BLUE#No object to create", "#LIGHT_BLUE#没有可创建的物品", "log")
t("Place Object", "放置物品", "_t")
t("Place the object where?", "将物品放置到哪里？", "_t")
t("Inventory of %s%s", "%s%s的物品栏", "tformat")
t(" #LIGHT_GREEN#(player)#LAST#", " #LIGHT_GREEN#（玩家）#LAST#", "_t")
t("Drop @ (%s, %s)%s", "丢在 @ (%s, %s)%s", "tformat")
t("#LIGHT_BLUE#Dropped %s at (%d, %d)", "#LIGHT_BLUE#将%s丢在(%d, %d)", "log")
t("NPC Inventory", "NPC的物品栏", "tformat")
t("Cancel", "取消", "tformat")
t("#LIGHT_BLUE#OBJECT:#LAST# %s%s: #LIGHT_BLUE#[%s] %s {%s, slot %s} at (%s, %s)#LAST#", "#LIGHT_BLUE#物品：#LAST# %s%s: #LIGHT_BLUE#[%s] %s {%s，槽位 %s} 位于 (%s, %s)#LAST#", "log")
t("Number of items to make", "制作的物品数量", "_t")
t("Enter 1-100%s", "输入 1-100%s", "tformat")
t(", or 0 for the example item", ", 或输入0获得样品", "_t")
t("#LIGHT_BLUE# Creating %d items:", "#LIGHT_BLUE# 正在创建 %d 件物品：", "log")
t("Ego", "词缀", "_t")
t("Add an ego enhancement if possible?", "要添加词缀增强吗（如果可能的话）？", "_t")
t("#LIGHT_BLUE#Created %s", "#LIGHT_BLUE#已制造 %s", "log")
t("Greater Ego", "高级词缀", "_t")
t("Add a greater ego enhancement if possible?", "制作一个有高级词缀的物品么（假如可以的话）？", "_t")
t(" #GOLD#All Artifacts#LAST#", " #GOLD#所有神器#LAST#", "_t")
t("#LIGHT_BLUE#Creating All Artifacts.", "#LIGHT_BLUE#创建所有神器。", "log")
t("#LIGHT_BLUE#%d artifacts created.", "#LIGHT_BLUE#创建了%d个神器。", "log")
t(" #YELLOW#Random Object#LAST#", " #YELLOW#随机物品#LAST#", "_t")
-- untranslated text
--[==[
t("#GOLD#%s#LAST#", "#GOLD#%s#LAST#", "tformat")
--]==]


------------------------------------------------

section "mod-tome/dialogs/debug/DebugMain.lua"

t("Debug/Cheat! It's BADDDD!", "调试/作弊！你又要做坏事了吧！", "_t")
t("#LIGHT_BLUE#God mode OFF", "#LIGHT_BLUE#天神模式关闭", "log")
t("#LIGHT_BLUE#God mode ON", "#LIGHT_BLUE#天神模式打开", "log")
t("#LIGHT_BLUE#Demi-God mode OFF", "#LIGHT_BLUE#半神模式关闭", "log")
t("#LIGHT_BLUE#Demi-God mode ON", "#LIGHT_BLUE#半神模式打开", "log")
t("#LIGHT_BLUE#Weakdamage mode OFF", "#LIGHT_BLUE#伤害减弱模式关闭", "log")
t("#LIGHT_BLUE#Weakdamage mode ON", "#LIGHT_BLUE#弱伤害模式：开启", "log")
t("#LIGHT_BLUE#Revealing Map.", "#LIGHT_BLUE#地图全开。", "log")
t("Zone: %s", "地图：%s", "tformat")
t("Level 1-%s", "楼层 1-%s", "tformat")
t("Kill or Remove", "杀死还是移除？", "_t")
t("Remove all (non-party) creatures or kill them for the player (awards experience and drops loot)?", "移除所有（队伍外）的生物，还是替玩家将其击杀（给予经验并掉落战利品）？", "_t")
t("#GREY#Removing [%s] %s at (%s, %s)", "#GREY#移除 [%s] %s 位于 (%s, %s)", "log")
t("#GREY#Killing [%s] %s at (%s, %s)", "#GREY#杀死[%s] %s位于(%s, %s)", "log")
t("#LIGHT_BLUE#%s %d creatures.", "#LIGHT_BLUE#%s %d 个生物。", "log")
t("Removed", "移除了", "_t")
t("Killed", "杀死了", "_t")
t("Remove", "移除", "_t")
t("Kill", "杀死", "_t")
t("Cancel", "取消", "_t")
t("Change Zone", "切换地图", "_t")
t("Change Level", "切换楼层", "_t")
t("Reveal all map", "地图全开", "_t")
t("Toggle Demi-Godmode", "切换半神模式", "_t")
t("Toggle Godmode", "切换天神模式", "_t")
t("Alter Faction", "改变阵营", "_t")
t("Summon a Creature", "召唤生物", "_t")
t("Create Items", "制造物品", "_t")
t("Create a Trap", "制造陷阱", "_t")
t("Grant/Alter Quests", "获得/改变任务", "_t")
t("Advance Player", "玩家升级", "_t")
t("Remove or Kill all creatures", "移除或杀死所有生物", "_t")
t("Give Sher'tul fortress energy", "获得夏·图尔堡垒能量", "_t")
t("Give all ingredients", "获得所有材料", "_t")
t("Weakdamage", "伤害减弱", "_t")
t("Spawn Event", "触发事件", "_t")
t("Endgamify", "游戏后期", "_t")
t("Reload/regenerate Zone and level", "重新加载/重新生成地图和楼层", "_t")
t("Automatically Clear Zones", "自动清图", "_t")

------------------------------------------------

section "mod-tome/dialogs/debug/Endgamify.lua"

t([[#ORANGE# Create Object: Unable to load all objects from file %s:#GREY#
 %s]], [[#ORANGE# 创建物品：无法读取文件%s的所有物品：#GREY#
 %s]], "log")
t("Failed to generate %s", "创建%s失败", "log")

------------------------------------------------

section "mod-tome/dialogs/debug/PlotTalent.lua"

t("Values plot for: %s (mastery %0.1f)", "技能数值属性表：%s (技能树系数 %0.1f)", "tformat")
t("TL: ", "技能等级： ", "_t")

------------------------------------------------

section "mod-tome/dialogs/debug/RandomActor.lua"

t("#LIGHT_GREEN#(From %s, line %s):#LAST#", "#LIGHT_GREEN#(来自 %s，第%s行):#LAST#", "tformat")
t("DEBUG -- Create Random Actor", "调试模式 -- 创建随机角色", "_t")
t([[Randomly generate actors subject to a filter and/or create random bosses according to a data table.
Filters are interpreted by game.zone:checkFilter.
#ORANGE#Boss Data:#LAST# is interpreted by game.state:createRandomBoss, game.state:applyRandomClass, and Actor.levelupClass.
Generation is performed within the _G environment (used by the Lua Console) using the current zone's #LIGHT_GREEN#npc_list#LAST#.
Press #GOLD#'F1'#LAST# for help.
Mouse over controls for an actor preview (which may be further adjusted when placed on to the level).
(Press #GOLD#'L'#LAST# to lua inspect or #GOLD#'C'#LAST# to open the character sheet.)

The #LIGHT_BLUE#Base Filter#LAST# is used to filter the actor randomly generated.]], [[根据给定的筛选器随机生成角色，或/并根据给定的数据表生成随机Boss。
筛选器由game.zone:checkFilter处理。
#ORANGE#Boss数据：#LAST#由 game.state:createRandomBoss, game.state:applyRandomClass, 和 Actor.levelupClass处理。
生成过程在 _G 环境下进行（也是 Lua 控制台使用的环境），并使用当前地图的#LIGHT_GREEN#npc_list#LAST#。
请按#GOLD#'F1'#LAST#获得帮助。
鼠标移动查看角色预览（放置到楼层时可能会被进一步调整）。
（请按 #GOLD#'L'#LAST# 在Lua中检查，或按 #GOLD#'C'#LAST# 打开角色面板）

#LIGHT_BLUE#基础过滤器#LAST#用于过滤生成的随机角色。]], "_t")
t("#GREY#None#LAST#", "#GREY#无#LAST#", "_t")
t("Current Base Actor: %s", "目前基础角色：%s", "tformat")
t("Generate", "生成", "_t")
t("#LIGHT_BLUE# Current base actor: %s", "#LIGHT_BLUE# 目前基础角色：%s", "log")
t("Place", "放置", "_t")
t("Default Filter", "默认筛选器", "_t")
t("#LIGHT_BLUE# Reset base filter", "#LIGHT_BLUE# 重设基础筛选器", "log")
t("Clear", "清除", "_t")
t("#LIGHT_BLUE# Clear base actor: %s", "#LIGHT_BLUE# 清除基础角色：%s", "log")
t("#LIGHT_BLUE#Base Filter:#LAST# ", "#LIGHT_BLUE#基础筛选器：#LAST# ", "_t")
t("The #ORANGE#Boss Data#LAST# is used to transform the base actor into a random boss (which will use a random actor if needed).", "#ORANGE#Boss 数据#LAST#用于将基础角色转换成一个随机boss（如果需要的话，也可以用随机角色作为基础）。", "_t")
t("Current Boss Actor: %s", "目前Boss角色：%s", "tformat")
t("Default Data", "默认数据", "_t")
t("#LIGHT_BLUE# Reset Randboss Data", "#LIGHT_BLUE# 重置Boss数据", "log")
t("#ORANGE#Boss Data:#LAST# ", "#ORANGE#Boss数据：#LAST# ", "_t")
t("Filter and Data Help", "筛选器和数据帮助", "_t")
t("#GREY#No Actor to Display#LAST#", "#GREY#没有待显示的角色#LAST#", "_t")
t("#LIGHT_BLUE#Inspect [%s]%s", "#LIGHT_BLUE#检查 [%s]%s", "log")
t("#LIGHT_BLUE#No actor to inspect", "#LIGHT_BLUE#没有待显示的角色", "log")
t("#LIGHT_BLUE#Lua Inspect [%s]%s", "#LIGHT_BLUE#Lua 检查 [%s]%s", "log")
t("#LIGHT_BLUE#No actor to Lua inspect", "#LIGHT_BLUE#没有待Lua检查的角色", "log")
t("#LIGHT_BLUE#Bad filter for base actor: %s", "#LIGHT_BLUE#基础角色筛选器错误：%s", "log")
t("#LIGHT_BLUE#Could not generate a base actor with filter: %s", "#LIGHT_BLUE#无法使用以下筛选器生成基础角色：%s", "log")
t([[#LIGHT_BLUE#Base actor could not be generated with filter [%s].
 Error:%s]], [[#LIGHT_BLUE#无法使用以下筛选器生成基础角色[%s]。
 错误：%s]], "log")
t("#LIGHT_BLUE#Bad data for random boss actor: %s", "#LIGHT_BLUE#随机Boss数据错误：%s", "log")
t("#LIGHT_BLUE#Could not generate a base actor with data: %s", "#LIGHT_BLUE#无法使用以下数据生成基础角色：%s", "log")
t([[#LIGHT_BLUE#ERROR: Random Boss could not be generated with data [%s].
 Error:%s]], [[#LIGHT_BLUE#错误：无法使用数据 [%s] 生成随机Boss。
错误：%s]], "log")

------------------------------------------------

section "mod-tome/dialogs/debug/RandomObject.lua"

t("#LIGHT_GREEN#(From %-10.60s, line: %s):#LAST#", "#LIGHT_GREEN#(来自 %-10.60s, 行数：%s):#LAST#", "tformat")
t("unknown", "未知", "_t")
t("None", "无", "_t")
t("Don't apply a resolver", "不使用解析器", "_t")
t("Equipment", "装备", "_t")
t("Object will be equipped if possible, otherwise added to main inventory", "物品将会尽可能被装备，否则会被加入物品栏。", "_t")
t("Inventory", "物品栏", "_t")
t("Object added to main inventory", "物品加入主要物品栏", "_t")
t("Drops", "掉落", "_t")
t("Object added to main inventory (dropped on death)", "物品加入主要物品栏，并在死亡时掉落", "_t")
t("Attach Tinker", "装载插件", "_t")
t("Tinker will be attached to a worn object", "插件将会被插到一个穿戴的物品上。", "_t")
t("Drop Randart (auto data)", "掉落随机神器（自动数据）", "_t")
t("Random Artifact (dropped on death) added to main inventory, uses the Base Object or Base Filter plus Randart Data as input", "随机神器（死亡后掉落）将会被加入到主要物品栏，使用基础物品或基础过滤器，加上随机神器数据作为输入。", "_t")
t("Drop Randart", "掉落随机神器", "_t")
t("Random Artifact (dropped on death) added to main inventory", "随机神器（死亡后掉落）将会被加入到主要物品栏", "_t")
t("DEBUG -- Create Random Object", "调试模式 -- 创建随机物品", "_t")
t([[Generate objects randomly subject to filters and create Random Artifacts.
Use "Generate" to create objects for preview and inspection.
Use "Add Object" to choose where to put the object and add it to the game.
(Mouse over controls for a preview of the generated object/working Actor. (Press #GOLD#'L'#LAST# to lua inspect.)
#SALMON#Resolvers#LAST# act on the working actor (default: player) to generate a SINGLE object.
They use the #LIGHT_GREEN#Random filter#LAST# as input unless noted otherwise and control object destination.
Filters are interpreted by ToME and engine entity/object generation functions (game.zone:checkFilter, etc.).
Interpretation of tables is within the _G environment (used by the Lua Console) using the current zone's #YELLOW_GREEN#object_list#LAST#.
Hotkeys: #GOLD#'F1'#LAST# :: context sensitive help, #GOLD#'C'#LAST# :: Working Character Sheet, #GOLD#'I'#LAST# :: Working Character Inventory.
]], [[按筛选器随机生成物品，并创建随机神器。
使用“生成”按钮生成物品用于预览和检查。
使用“添加物品”按钮选择将物品放到哪里，并将其加入游戏。
将鼠标悬停在控件上，可以预览生成的物品/使用的角色（请按#GOLD#'L'#LAST#键进行 Lua 检查）。
#SALMON#解析器#LAST#作用于工作角色（默认：玩家），用于生成单个物品。
除非特别说明，它们使用#LIGHT_GREEN#随机筛选器#LAST#作为输入，并决定物品的去向。
筛选器由ToME游戏引擎的实体/物品处理函数解析(game.zone:checkFilter等)。
解析将会工作在_G环境下，这也是Lua控制台的工作环境，并使用当前地图的#YELLOW_GREEN#object_list#LAST#。
热键：#GOLD#'F1'#LAST# :: 查看帮助，#GOLD#'C'#LAST# :: 工作角色的角色面板，#GOLD#'I'#LAST# :: 工作角色的物品栏。
]], "_t")
t("The #LIGHT_GREEN#Random Filter#LAST# controls random generation of a normal object.", "#LIGHT_GREEN#随机筛选器#LAST#用于控制随机生成一个普通物品。", "tformat")
t("#GREY#None#LAST#", "#GREY#无#LAST#", "_t")
t("%s: %s", "%s：%s", "tformat")
t("Object", "物品", "_t")
t("Generate", "生成", "_t")
t("Add Object", "添加物品", "_t")
t("Default Filter", "默认筛选器", "_t")
t("Clear Object", "清除物品", "_t")
t("#LIGHT_GREEN#Random Object#LAST#", "#LIGHT_GREEN#随机物品#LAST#", "_t")
t("#LIGHT_GREEN#Random Filter:#LAST# ", "#LIGHT_GREEN#随机筛选器：#LAST# ", "_t")
t("The #LIGHT_BLUE#Base Filter#LAST# is to generate a base object for building a Randart.", "#LIGHT_BLUE#基础筛选器#LAST#用于生成一个用来生成随机神器的基础物品。", "tformat")
t("#LIGHT_BLUE#Base Object#LAST#", "#LIGHT_BLUE#基础物品#LAST#", "_t")
t("#LIGHT_BLUE#Base Filter:#LAST# ", "#LIGHT_BLUE#基础筛选器：#LAST# ", "_t")
t("#SALMON#Resolver selected:#LAST# ", "#SALMON#选定的解析器：#LAST# ", "tformat")
t("An object resolver interprets additional filter fields to generate an object and determine where it will go.", "物品解析器解释附加的过滤字段以生成物品，并决定它将被放入何处。", "_t")
t("Dropdown text", "下拉文字", "_t")
t("No Tooltip", "没有提示", "_t")
t("Use this selector to choose which resolver to use", "使用这个选项选择想要使用的解析器。", "_t")
t([[#ORANGE#Randart Data#LAST# contains parameters used to generate a Randart (interpreted by game.state:generateRandart).
The #LIGHT_BLUE#Base Object#LAST# will be used if possible.]], [[#ORANGE#随机神器数据#LAST# 包含了用于生成随机神器的额外参数 (由game.state:generateRandart)解析。
如果可能，将会使用#LIGHT_BLUE#基础物品#LAST#作为基础。]], "tformat")
t("Default Data", "默认数据", "_t")
t("#ORANGE#Randart Data:#LAST# ", "#ORANGE#随机神器数据：#LAST# ", "_t")
t("#ORANGE#Randart#LAST#", "#ORANGE#随机神器#LAST#", "_t")
t("Show #GOLD#I#LAST#nventory", "显示#GOLD#[I]#LAST#物品栏", "_t")
t("Show #GOLD#C#LAST#haracter Sheet", "显示#GOLD#[C]#LAST#角色面板", "_t")
t("Set working actor: [%s] %s", "设置工作角色：[%s] %s", "tformat")
t("Set working actor: [%s] %s%s", "设置工作角色：[%s] %s%s", "tformat")
t(" #LIGHT_GREEN#(player)#LAST#", " #LIGHT_GREEN#（玩家）#LAST#", "_t")
t("#GREY#No Tooltip to Display#LAST#", "#GREY#没有待显示的提示#LAST#", "_t")
t("Filter/Data/Resolver Reference", "筛选器/数据/解析器文档", "_t")
t("#LIGHT_BLUE#Lua Inspect [%s] %s", "#LIGHT_BLUE#Lua 检查 [%s] %s", "log")
t("#LIGHT_BLUE#Nothing to Lua inspect", "#LIGHT_BLUE#没有用于Lua检查的物品", "log")
t("#LIGHT_BLUE#Bad %s: %s", "#LIGHT_BLUE#错误的%s: %s", "log")
t("table definition", "表定义", "_t")
t("#LIGHT_BLUE# Generate Random object using resolver: %s", "#LIGHT_BLUE# 使用解析器生成随机物品：%s", "log")
t("#LIGHT_BLUE# New random%s object: %s", "#LIGHT_BLUE# 新随机%s 物品：%s", "log")
t(" (resolver: %s)", " (解析器：%s)", "tformat")
t("#LIGHT_BLUE#Could not generate a random object with filter: %s", "#LIGHT_BLUE#无法使用以下筛选器生成随机物品：%s", "log")
t([[#LIGHT_BLUE#ERROR generating random object with filter [%s].
 Error: %s]], [[#LIGHT_BLUE#错误：使用该筛选器生成随机物品时发生错误[%s]。
 错误：%s]], "log")
t("#LIGHT_BLUE#Could not generate a base object with filter: %s", "#LIGHT_BLUE#无法使用该筛选器生成基础物品：%s", "log")
t([[#LIGHT_BLUE#ERROR generating base object with filter [%s].
 Error:%s]], [[#LIGHT_BLUE#错误：使用该筛选器生成基础物品时发生错误 [%s]。
 错误：%s]], "log")
t("#LIGHT_BLUE#Could not generate a Randart with data: %s", "#LIGHT_BLUE#无法使用数据生成随机神器：%s", "log")
t([[#LIGHT_BLUE#ERROR generating Randart with data [%s].
 Error:%s]], [[#LIGHT_BLUE#错误：使用数据 [%s] 生成随机神器时发生错误。
错误：%s]], "log")
t("#LIGHT_BLUE#No object to add", "#LIGHT_BLUE#没有待添加的物品", "log")
t([[#LIGHT_BLUE#ERROR accepting object with resolver %s.
 Error:%s]], [[#LIGHT_BLUE#使用解析器%s接受物品时出错。
 错误：%s]], "log")
t("#LIGHT_BLUE#Working Actor set to [%s]%s at (%d, %d)", "#LIGHT_BLUE#将工作角色设置为[%s]%s 位于(%d, %d)", "log")

------------------------------------------------

section "mod-tome/dialogs/debug/SummonCreature.lua"

t("DEBUG -- Summon Creature", "调试模式 -- 召唤生物", "_t")
t("#LIGHT_BLUE# no actor to place.", "#LIGHT_BLUE#没有待放置的角色。", "log")
t("#LIGHT_BLUE#Actor [%s]%s already occupies (%d, %d)", "#LIGHT_BLUE#角色[%s]%s已经占据了(%d, %d)", "log")
t("#LIGHT_BLUE#Added %s[%s]%s at (%d, %d)", "#LIGHT_BLUE#将%s[%s]%s添加到(%d, %d)", "log")
t("#YELLOW#Random Actor#LAST#", "#YELLOW#随机角色#LAST#", "_t")
t("#PINK#Test Dummy#LAST#", "#PINK#训练傀儡#LAST#", "_t")
t("Test Dummy", "训练傀儡", "_t")
t("Test dummy.", "训练傀儡。", "_t")

------------------------------------------------
