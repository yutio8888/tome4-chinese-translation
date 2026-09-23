section "mod-tome/dialogs/LevelupDialog.lua"

t("Levelup: %s, level %s", "升级：%s，等级 %s", "tformat")
t("Finish", "完成", "_t")
t("Do you accept changes?", "你确认接受更改吗？", "_t")
t("Impossible", "不可能", "_t")
t("You cannot learn this talent(s): ", "你无法学习该技能：", "_t")
t([[#LIGHT_BLUE#Warning: You have increased some of your statistics or talent. Talent(s) actually sustained: 
 %s If these are dependent on one of the stats you changed, you need to re-use them for the changes to take effect.]], [[#LIGHT_BLUE#警告：你改变了你的某些技能或属性。你目前开启的持续技能：
 %s 如果其中某些技能和你改变的属性点相关，你需要重新使用该技能来使新的属性生效。]], "_t")
t("#LIGHT_RED#Requirements for %s not met, prodigy not learnt.", "#LIGHT_RED#未满足学习%s的条件，觉醒技学习失败了。", "log")
t("Not enough stat points", "属性点不足", "_t")
t("You have no stat points left!", "你的属性点不足！", "_t")
t("Stat is at the maximum for your level", "该属性已达到当前等级上限", "_t")
t("You cannot increase this stat further until next level!", "在升级之前，你无法再次提升这项属性！", "_t")
t("Stat is at the maximum", "该属性已达到上限", "_t")
t("You cannot increase this stat further!", "你不能继续提升该属性！", "_t")
t("You cannot take out more points!", "你不能取出更多点数！", "_t")
t("unknown", "未知", "_t")
t("not enough stat", "属性值不足", "_t")
t("class", "职业", "_t")
t("generic", "通用", "_t")
t("Not enough %s talent points", "%s技能点不足", "tformat")
t("You have no %s talent points left!", "你没有足够的%s技能点！", "tformat")
t("Cannot learn talent", "无法学习技能", "_t")
t("Prerequisites not met!", "技能学习条件未满足！", "_t")
t("Already known", "已学会", "_t")
t("You already fully know this talent!", "你已完全掌握此技能！", "_t")
t("You do not know this talent!", "你还没学会这个技能！", "_t")
t("Impossible here", "不能在这里这么做", "_t")
t("You must be out of combat or in a quiet place like a #{bold}#town#{normal}# to unlearn this talent.", "你只能在战斗外或在 #{bold}#城市#{normal}# 这样安全的地方遗忘这个技能。", "_t")
t("You cannot unlearn this talent!", "你不能遗忘这个技能！", "_t")
t("You cannot unlearn this talent because of talent(s): ", "由于以下技能，你不能遗忘这个技能：", "_t")
t("You can only improve a category mastery once!", "你只能提升一次技能类别掌握度！", "_t")
t("Not enough talent category points", "技能树解锁点不足", "_t")
t("You have no category points left!", "你的技能树解锁点不够！", "_t")
t("Too low level", "等级太低", "_t")
t("This talent tree only provides talents starting at level %d. Learning it now would be useless.", "这个技能树只提供 %d 级以上才能学习的技能。现在学习这个技能树是没有意义的。", "tformat")
t("You cannot unlearn this category!", "你不能遗忘该技能树！", "_t")
t("You do not know this category!", "你没有学会该技能树！", "_t")
t("You cannot unlearn this category because of: %s", "由于以下技能，你无法遗忘该技能树：%s", "tformat")
t([[Stats points left: #00FF00#%d#LAST#
Category points left: #00FF00#%d#LAST#
Class talent points left: #00FF00#%d#LAST#
Generic talent points left: #00FF00#%d#LAST#]], [[属性点剩余：#00FF00#%d#LAST#
技能树解锁点剩余：#00FF00#%d#LAST#
职业技能点剩余：#00FF00#%d#LAST#
通用技能点剩余：#00FF00#%d#LAST#]], "_t")
t([[Stat points allow you to increase your core stats.
Each level you gain 3 new stat points to use.

You may only increase stats to a natural maximum of 60 or lower (relative to your level).]], [[属性点可以提高你的基础属性。
人物等级每升一级可以获得 3 点自由分配。

每项属性基础值上限为 60 点。加点不能超过这个上限，另外属性上限也受你的人物等级限制。]], "_t")
t([[Class talent points allow you to learn new class talents or improve them.
Class talents are core to your class and can not be learnt by training.

Each level you gain 1 new class point to use.
Each five levels you gain one more.
]], [[职业技能点可以让你学习新的或者提升已学习的职业技能。
职业技能是你所选择职业的核心技能，不能从训练师处学到。

人物等级每升一级可以获得 1 点职业技能点。
此外每 5 级可以额外获得 1 点职业技能点。
]], "_t")
t([[Generic talent points allow you to learn new generic talents or improve them.
Generic talents comes from your class, your race or various outside training you can get during your adventures.

Each level you gain 1 new generic point to use.
Each five levels you gain one less.
]], [[通用技能点可以让你学习新的或者提升已学习的通用技能。
通用技能可以是你选择职业或种族自身拥有，或者在你的冒险生涯中习得。

通常人物等级每升一级可以获得 1 点通用技能点。
不过每 5 级时不能获得。
]], "_t")
t([[Talent category points allow you to either:
- learn a new talent (class or generic) category
- improve a known talent category efficiency by 0.2
- learn a new inscription slot (up to a maximum of 5, learning it is automatic when using an inscription)

You gain a new point at level 10, 20 and 34.
Some races or items may increase them as well.]], [[技能树解锁点有以下作用：
- 解锁职业或通用技能树
- 提升已解锁技能树的精通度，每点提升 0.2
- 解锁新的刻印位（最多 5 个，你使用刻印时会自动消耗点数解锁）

你会在人物等级达到 10、20 和 34 级时各获得 1 个点数。
某些种族和物品可以获得额外的点数。]], "_t")
t([[Prodigies are special talents that only the most powerful of characters can attain.
All of them require at least 50 in a core stat and many also have more special demands. You can learn a new prodigy at level 25 and 42.]], [[觉醒技是角色足够强大时才能获得的特殊技能。
所有觉醒技都要求某项核心属性达到 50 点，其中许多还有更特殊的额外要求。
你可以在人物等级达到 25 级和 42 级时各获得一个觉醒技能点。]], "_t")
t("You can use a category point to unlock a new inscription slot (up to 5 slots).", "你可以消耗 1 个技能树解锁点来解锁一个新的刻印位（最多 5 个）。", "_t")
t("Prodigies", "觉醒技", "_t")
t("Inscriptions", "刻印", "_t")
t("You have learnt all the inscription slots you could.", "你已经解锁了所有的刻印位。", "_t")
t("You can learn %d new slot(s). Do you wish to buy one with one category point?", "您可以解锁 %d 个新的刻印位。你希望用 1 个技能树点数解锁 1 个刻印位吗？", "tformat")
t("Category points: %s", "技能树解锁点：%s", "tformat")
t("You can still learn %d new slot(s) but you need a category point.", "你还可以学习 %d 个新的刻印位，但你需要一个技能树点数。", "tformat")
t("Stats: %s", "属性：%s", "tformat")
t("Class points: %s", "职业点：%s", "tformat")
t("Generic points: %s", "通用点：%s", "tformat")
t("Hide unlearnt categories", "隐藏没有学会的技能树", "_t")
t("Current value: ", "当前值：", "_t")
t("Base value: ", "基础值：", "_t")
t("Stat gives:", "属性提供：", "_t")
t("Max life: ", "最大生命：", "_t")
t("Physical save: ", "物理豁免：", "_t")
t("Healing mod: ", "治疗系数：", "_t")
t("Max mana: ", "最大法力值：", "_t")
t("Max stamina: ", "最大体力值：", "_t")
t("Max psi: ", "最大灵能值：", "_t")
t("Mindpower: ", "精神强度：", "_t")
t("Mental save: ", "精神豁免：", "_t")
t("Spell save: ", "法术豁免：", "_t")
t("Physical power: ", "物理强度：", "_t")
t("Max encumbrance: ", "最大负重：", "_t")
t("Crit. chance: ", "暴击率：", "_t")
t("Accuracy: ", "命中：", "_t")
t("Spellpower: ", "法术强度：", "_t")
t("Defense: ", "闪避：", "_t")
t("Ranged defense: ", "远程闪避：", "_t")
t("Shrug off criticals chance: ", "暴击摆脱率：", "_t")
t("Class powers:", "职业能力：", "_t")
t("Talent Category", "技能树", "_t")
t([[A talent category contains talents you may learn. You gain a talent category point at level 10, 20 and 34. You may also find trainers or artifacts that allow you to learn more.
A talent category point can be used either to learn a new category or increase the mastery of a known one.]], "一个技能树包含你可以学习的技能。你会在 10、20 和 34 级时各获得一个技能树点数，也可以找到训练师或神器来学习更多。\n每一点技能树点数可以用来学习一个新的技能树，或者提升一个已知技能树的熟练度。", "_t")
t("Generic talent tree", "通用技能树", "_t")
t("A generic talent allows you to perform various utility actions and improve your character. It represents a skill anybody can learn (should you find a trainer for it). You gain one point every level (except every 5th level). You may also find trainers or artifacts that allow you to learn more.", "通用技能让你能够执行各种实用动作并强化角色。它代表任何人都能学习的技能（只要能找到训练师）。你每升 1 级获得一点通用技能点（每第 5 级除外），也可以通过训练师或神器获得更多。", "_t")
t("Class talent tree", "职业技能树", "_t")
t("A class talent allows you to perform new combat moves, cast spells, and improve your character. It represents the core function of your class. You gain one point every level and two every 5th level. You may also find trainers or artifacts that allow you to learn more.", "职业技能让你能够施展新的战斗招式、施放法术并强化角色。它代表你职业的核心功能。你每升 1 级获得一点职业技能点，每第 5 级获得两点，也可以通过训练师或神器获得更多。", "_t")
t("This talent was recently learnt; you can still unlearn it.", "你刚在此技能上加点，你还可以遗忘它。", "_t")
t("The last %d %s talents you learnt are always unlearnable.", "你最近学习的 %d 个%s技能始终可以遗忘。", "tformat")
t(" generic", " 通用", "_t")
t(" class", " 职业", "_t")
t("This talent can alter the world in a permanent way; as such, you can never unlearn it once known.", "本技能会永久性的影响这个游戏世界，所以学习之后无法移除。", "_t")
t("This talent was recently learnt; you can still unlearn it if you are out of combat or in a quiet area like a #{bold}#town#{normal}#.", "你刚在此技能上加点，你还可以在战斗外或者#{bold}#城市#{normal}#这样安全的地方遗忘它。", "_t")
t("Current talent level: ", "当前技能等级： ", "_t")
t(" (%+0.1f bonus level)", " (%+0.1f 额外等级)", "tformat")
t("<Press 'x' to swap to simple display>", "<按 X 键切换简单显示>", "_t")
t("First talent level: ", "第一级技能等级： ", "_t")
t("Next talent level", "下一技能等级", "_t")
t("<Press 'x' to swap to advanced display>", "<按 X 键切换进阶显示>", "_t")

------------------------------------------------

section "mod-tome/dialogs/PartySendItem.lua"

t("Give item to a party member", "把物品交给队伍成员", "_t")
t("%s cannot receive items while asleep!", "%s不能在睡眠中接收物品！", "log")
t("%s cannot transfer items while asleep!", "%s不能在睡眠中转移物品", "log")
t("You give %s to %s.", "你把%s交给了%s。", "log")
t(" #YELLOW#[SLEEPING]#LAST#", " #YELLOW#[睡眠中]#LAST#", "_t")
t(" #YELLOW#[NO ROOM]#LAST#", " #YELLOW#[没有空间]#LAST#", "_t")

------------------------------------------------

section "mod-tome/dialogs/QuestPopup.lua"

t("#LIGHT_GREEN#New#LAST# Quest!", "#LIGHT_GREEN#新#LAST# 任务！", "_t")
t("Quest #AQUAMARINE#Updated!", "任务 #AQUAMARINE#更新了！", "_t")
t("Quest #LIGHT_GREEN#Completed!", "任务 #LIGHT_GREEN#已完成！", "_t")
t("Quest #LIGHT_GREEN#Done!", "任务 #LIGHT_GREEN#完成！", "_t")
t("Quest #CIMSON#Failed!", "任务 #CIMSON#失败了！", "_t")
t("#ANTIQUE_WHITE#Quest: #AQUAMARINE#%s", "#ANTIQUE_WHITE#任务：#AQUAMARINE#%s", "tformat")
t("#ANTIQUE_WHITE#(See your Journal for further details or click here)", "#ANTIQUE_WHITE#（点击此处或者打开任务面板查看详情）", "_t")

------------------------------------------------

section "mod-tome/dialogs/SentientWeapon.lua"

t("Points left: #00FF00#%d#WHITE#", "剩余点数：#00FF00#%d#WHITE#", "_t")
t([[Keyboard: #00FF00#up key/down key#FFFFFF# to select a stat; #00FF00#right key#FFFFFF# to increase stat; #00FF00#left key#FFFFFF# to decrease a stat.
Mouse: #00FF00#Left click#FFFFFF# to increase a stat; #00FF00#right click#FFFFFF# to decrease a stat.
]], [[键盘：#00FF00#上/下键#FFFFFF#选择属性，#00FF00#右键#FFFFFF#增加属性，#00FF00#左键#FFFFFF#降低属性。
鼠标：#00FF00#左键点击#FFFFFF#增加属性，#00FF00#右键点击#FFFFFF#降低属性。
]], "_t")
t("Stat", "属性值", "_t")
t("Value", "数值", "_t")
t("Spellpower", "法术强度", "_t")
t("Spellcrit", "法术暴击", "_t")
t("Not enough stat points", "属性点不足", "_t")
t("You have no stat points left!", "你的属性点不足！", "_t")
t("Stat is at the maximum", "该属性已达到上限", "_t")
t("You can not increase this stat further!", "你无法进一步提升此项属性！", "_t")
t("Impossible", "不可能", "_t")
t("You cannot take out more points!", "你不能取出更多点数！", "_t")
t("Stats points left: #00FF00#%s", "剩余属性点：#00FF00#%s", "tformat")
t("Strength", "力量", "_t")
t("Dexterity", "敏捷", "_t")
t("Magic", "魔力", "_t")
t("Willpower", "意志", "_t")
t("Cunning", "灵巧", "_t")
t("Constitution", "体质", "_t")

------------------------------------------------

section "mod-tome/dialogs/ShowIngredients.lua"

t("Ingredients collected", "搜集到的材料", "_t")
t("Ingredient", "材料", "_t")
t("Category", "分类", "_t")
t("Quantity", "数量", "_t")
t([[#GOLD#Category:#AQUAMARINE# %s
#GOLD#Ingredient:#0080FF# %s
#GOLD#Quantity:#0080FF# %s
#GOLD#Text:#ANTIQUE_WHITE# %s]], [[#GOLD#分类：#AQUAMARINE# %s
#GOLD#材料：#0080FF# %s
#GOLD#数量：#0080FF# %s
#GOLD#描述：#ANTIQUE_WHITE# %s]], "tformat")

------------------------------------------------

section "mod-tome/dialogs/ShowLore.lua"

t("Lore", "手札", "_t")
t("Search: ", "搜索：", "_t")
t("Category", "分类", "_t")
t([[#GOLD#Category:#AQUAMARINE# %s
#GOLD#Found as:#0080FF# %s
#GOLD#Text:#ANTIQUE_WHITE# %s]], [[#GOLD#分类：#AQUAMARINE# %s
#GOLD#发现于：#0080FF# %s
#GOLD#文本：#ANTIQUE_WHITE# %s]], "tformat")
-- untranslated text
--[==[
t("", "", "_t")
--]==]


------------------------------------------------

section "mod-tome/dialogs/ShowStore.lua"

t("Inventory", "物品栏", "_t")
t("Category", "分类", "_t")
t("Price", "价格", "_t")
t("Store", "商店", "_t")
t(" (pays up to %0.2f gold, Your Gold: %0.2f)", " (最多付款 %0.2f 金币，你的金币：%0.2f)", "tformat")
-- untranslated text
--[==[
t("", "", "_t")
--]==]


------------------------------------------------

section "mod-tome/dialogs/TrapsSelect.lua"

t("Select Traps", "选择陷阱", "_t")
t("Select traps to prepare:", "选择需要准备的陷阱：", "_t")
t("starting trap selection dialog", "开始选择陷阱", "log")
t(" (replacing instant trigger)", " （替换瞬间启动机关）", "_t")
t(" (primed trigger)", " （即爆启动机关）", "_t")
t(" (prepared)", " （准备完毕）", "_t")
t(" (preparing)", " （准备中）", "_t")
t(" (dismantling)", " （分解中）", "_t")
t(" (need more skill)", " （需要更多技能）", "_t")
t("%s) Tier %d: %s%s", "%s) 等级 %d：%s%s", "tformat")
t("#LIGHT_BLUE#You cannot prepare this trap: %s.", "#LIGHT_BLUE#你不能准备这个陷阱：%s。", "logPlayer")
t("#LIGHT_BLUE#You need more skill to prepare this trap.", "#LIGHT_BLUE#你的技能等级不足，无法准备这个陷阱。", "logPlayer")
t("#LIGHT_BLUE#Preparing trap with normal trigger.", "#LIGHT_BLUE#准备了常规触发的陷阱。", "logPlayer")
t("Accept these selections", "确认选择", "_t")
t("#LIGHT_BLUE#You cannot prepare more than %d traps.", "#LIGHT_BLUE#你不能准备多于%d个陷阱。", "logPlayer")
-- untranslated text
--[==[
t([[#GOLD#%s#LAST#
%s]], [[#GOLD#%s#LAST#
%s]], "tformat")
t(" (%s)", " (%s)", "tformat")
--]==]


------------------------------------------------

section "mod-tome/dialogs/UberTalent.lua"

t("Prodigies: %s", "觉醒技：%s", "tformat")
t([[#LIGHT_GREEN#Number available: %d#LAST#
Prodigies are special talents that only the most powerful of characters can attain.%s
All of them require at least 50 in a core stat and many also have more special demands. You can learn a new prodigy at level 25 and 42.]], [[#LIGHT_GREEN#当前可用觉醒技能点：%d#LAST#
觉醒技是角色足够强大时才能获得的特殊技能。%s
所有觉醒技都要求某项核心属性达到 50 点，其中许多还有更特殊的额外要求。
你可以在人物等级达到25级和42级时各获得一个觉醒技能点。]], "_t")
t("\
Evolutions are special prodigies specific to a class or race. Only one evolution can be choosen, if any are available at all.", "\
进阶是特殊的觉醒技，只有特定职业种族才能学习。即使有多项进阶可能，每名角色最多只能选择一项进阶。", "_t")
t("#{bold}##GOLD#Prodigies#{normal}#", "#{bold}##GOLD#觉醒技#{normal}#", "_t")
t("#{bold}##LIGHT_STEEL_BLUE#Evolutions#{normal}#", "#{bold}##LIGHT_STEEL_BLUE#进阶#{normal}#", "_t")

------------------------------------------------

section "mod-tome/dialogs/UnlockDialog.lua"

t("#VIOLET#Option unlocked: %s", "#VIOLET#游戏选项已解锁：%s", "logPlayer")
t("Option unlocked: %s", "选项已解锁：%s", "tformat")

------------------------------------------------

section "mod-tome/dialogs/UseItemDialog.lua"

t("Impossible", "不可能", "_t")
t("You must wear this object to use it!", "你必须装备这件物品才能使用它！", "_t")
t("Drop how many?", "丢下多少？", "_t")
t("1 to %d", "1 到 %d", "tformat")
t("Attach to item", "附加到物品", "_t")
t("You do not have any equipped items that it can be attached to.", "你没有已装备的、可供它附加的物品。", "_t")
t("Select which item to attach it to:", "选择要附加到哪个物品：", "_t")
t("Really %s %s", "真的要 %s %s", "tformat")
t("Tag object (tagged objects can not be destroyed or dropped)", "标记物品（被标记的物品无法丢下或摧毁）", "_t")
t("Tag:", "标记：", "_t")
t("Identify", "鉴定", "_t")
t("Move to normal inventory", "移动到普通物品栏", "_t")
t("Use", "使用", "_t")
t("Wield/Wear", "装备/穿戴", "_t")
t("Take off", "脱下", "_t")
t("Detach from item", "从物品上解除附加", "_t")
t("Detach tinker", "移除插件", "_t")
t("Drop", "丢下", "_t")
t("Transfer to party", "转交给队伍成员", "_t")
t("%s now", "现在%s", "tformat")
t("Link item in chat", "在聊天中链接这个物品", "_t")
t("Lua inspect", "Lua 检查", "_t")
t("Tag", "标记", "_t")
t("Untag", "解除标记", "_t")

------------------------------------------------

section "mod-tome/dialogs/WandererSeed.lua"

t("Wanderer Options", "流浪者选项", "_t")
t([[Welcome, wandering one! The Wanderer class uses a randomly selected set of talent trees.
You can now choose how this set is selected:]], [[欢迎，流浪者！流浪者职业具有随机的技能树。
现在你将选择随机模式：]], "_t")
t("Simply make a random set of trees, this is the default option. If you want to share it with friends, you will find the seed in the character's sheet later on.", "完全随机，这也是默认选项。稍后你可以在角色面板中找到随机种子以分享给朋友。", "_t")
t("If an other player gave you a seed to play, you can enter it here. Do note that while a seed will always work, you will only get the same talents set if you use the same DLC/addons.", "如果其他玩家给你随机种子，可以在此输入。注意，种子总是会生效，但只有使用相同的DLC/插件，你才能获得相同的技能组合。", "_t")
t("Play!", "开始游戏！", "_t")
t("#{bold}##ANTIQUE_WHITE#Random#{normal}##LAST#", "#{bold}##ANTIQUE_WHITE#随机模式#{normal}##LAST#", "_t")
t("#{bold}##ANTIQUE_WHITE#Seed#{normal}##LAST#", "#{bold}##ANTIQUE_WHITE#种子模式#{normal}##LAST#", "_t")
t("Wanderer Seed", "流浪者随机种子", "_t")
t("The wanderer seed you used was generated for a different set of DLC/addons. Your character will still work fine but you may not have the same talent set as the person that shared the seed with you.", "你使用的随机种子和你开启的DLC/插件不匹配。你的角色仍然可以游玩，但可能不会拥有和分享种子的玩家相同的技能树组合。", "_t")

------------------------------------------------

section "mod-tome/dialogs/debug/AdvanceActor.lua"

t("DEBUG -- Levelup Actor: [%s] %s", "调试模式 -- 升级角色：[%s] %s", "tformat")
t([[Levelup an actor.
Optionally set Stat levels, learn all talents possible, and gain points to spend on Levelup. 
The actor is backed up before changes are made.  (Use the "Restore" button to recover.)
]], [[升级角色
可以自动设置相应的属性值，尽可能学习所有技能，并获得升级所得到的属性点。
这个角色会在更新前被备份，按“恢复”按钮可以恢复备份。
]], "_t")
t(" Advance to Level: ", " 升级到等级： ", "_t")
t("Restore: %s (v%d)", "恢复：%s (v%d)", "tformat")
t("Restore: none", "恢复：无", "_t")
t("#LIGHT_BLUE#Restoring [%s]%s from backup version %d", "#LIGHT_BLUE#恢复 [%s]%s（来自备份版本 %d）", "log")
t("Gain points for stats, talents, and prodigies (unlimited respec)", "获得属性点，技能点和觉醒点（无限次重置）", "_t")
t(" Force all BASE stats to: ", " 设置所有基础属性为： ", "_t")
t(" Force all BONUS stats to: ", " 设置所有额外属性为： ", "_t")
t("Learn Talents ", "学习技能 ", "_t")
t("Unlock & Learn all available talents to level: ", "解锁并学习所有的技能到等级： ", "_t")
t("maximum allowed", "最高等级", "_t")
t("Ignore requirements", "无视技能需求", "_t")
t("Force all talent mastery levels to (0.1-5.0): ", "将所有技能树系数设置到 (0.1-5.0): ", "_t")
t("no change", "不变", "_t")
t("Unlock all talent types (slow)", "解锁所有技能树（缓慢）", "_t")
t("Accept", "接受", "_t")
t("Cancel", "取消", "_t")
t("#LIGHT_BLUE#AdvanceActor inputs: %s", "#LIGHT_BLUE#升级角色 输入：%s", "log")
t("%s #GOLD#Forcing all Base Stats to %s", "%s #GOLD#正在将所有基础属性值设置为 %s", "log")
t("%s #GOLD#Resetting all talents_types_mastery to %s", "%s #GOLD#正在将所有技能树系数重置为 %s", "log")
t("%s #GOLD#Unlocking All Talent Types", "%s #GOLD#正在解锁所有技能树", "log")
t("#GOLD#Checking %s Talents (%s)", "#GOLD#检查 %s 技能 (%s)", "log")
t("#LIGHT_BLUE#Talent %s learned to level %d", "#LIGHT_BLUE#技能 %s 学习到等级 %d", "log")
t("%s #GOLD#Forcing all Bonus Stats to %s", "%s #GOLD#将所有额外属性值设置为 %s", "log")
t("%d stat point(s)", "%d 属性点", "tformat")
t("%d class talent point(s)", "%d 职业技能点", "tformat")
t("%d generic talent point(s)", "%d 通用技能点", "tformat")
t("%d category point(s)", "%d 大系点", "tformat")
t("#ORCHID#%d prodigy point(s)#LAST#", "#ORCHID#%d 觉醒点#LAST#", "tformat")
t("#LIGHT_BLUE#%s has %s to spend", "#LIGHT_BLUE#%s 有 %s 可以使用", "log")
t(", and ", ", 和 ", "_t")
-- untranslated text
--[==[
t("", "", "_t")
t("#LIGHT_BLUE#%s -- %s", "#LIGHT_BLUE#%s -- %s", "log")
--]==]


------------------------------------------------

section "mod-tome/dialogs/debug/AlterFaction.lua"

t("DEBUG -- Alter Faction", "调试模式 -- 切换阵营", "_t")
t("Alter: %s", "改变：%s", "tformat")
t("Alter to which state:", "改变到什么状态：", "_t")
t("friendly", "友善", "_t")
t("neutral", "中立", "_t")
t("hostile", "敌对", "_t")

------------------------------------------------

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
