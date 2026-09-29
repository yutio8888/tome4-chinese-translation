# batch-002：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-00041
位置：engine.lua:1029；section：engine/engine/dialogs/VideoOptions.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Request a specific origin point for the game window.
This point corresponds to where the upper left corner of the window will be located.
Useful when dealing with multiple monitors and borderless windows.

The default origin is (0,0).

Note: This value will automatically revert after ten seconds if not confirmed by the user.#WHITE#
```
译文：
```text
设置游戏窗口的原点。
这个点表示窗口左上角所在的位置。
这一选项用于在使用无边框窗口或者多显示器的场合。

默认原点：(0,0)。

注意：如果用户在十秒后不进行确认，这一数值将会自动恢复原值#WHITE#
```

## entry-00042
位置：engine.lua:1067；section：engine/engine/dialogs/microtxn/MTXMain.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Welcome!

I am #{italic}##ANTIQUE_WHITE#DarkGod#LAST##{normal}#, the creator of the game and before you go on your merry way I wish to take a few seconds of your time to explain why there are microtransactions in the game.

Before you run off in terror let me put it plainly: I am very #{bold}#firmly #CRIMSON#against#LAST# pay2win#{normal}# things so rest assured I will not add this kind of stuff.

So why put microtransactions? Tales of Maj'Eyal is a cheap/free game and has no subscription required to play. It is my baby and I love it; I plan to work on it for many years to come (as I do since 2009!) but for it to be viable I must ensure a steady stream of income as this is sadly the state of the world we live in.

As for what kind of purchases are/will be available:
- #GOLD#Cosmetics#LAST#: in addition to the existing racial cosmetics & item shimmers available in the game you can get new packs of purely cosmetic items & skins to look even more dapper!
- #GOLD#Pay2DIE#LAST#: Tired of your character? End it with style!
- #GOLD#Vault space#LAST#: For those that donated they can turn all those "useless" donations into even more online vault slots.
- #GOLD#Community events#LAST#: A few online events are automatically and randomly triggered by the server. With those options you can force one of them to trigger; bonus point they trigger for the whole server so everybody online benefits from them each time!

I hope I've convinced you of my non-evil intentions (ironic for a DarkGod I know ;)). I must say feel dirty doing microtransactions even as benign as those but I want to find all the ways I can to ensure the game's future.
Thanks, and have fun!
```
译文：
```text
欢迎！

我是游戏的制造者 #{italic}##ANTIQUE_WHITE#DarkGod#LAST##{normal}#。在愉快的探险开始之前，我希望占用短暂的时间向你解释游戏内购的存在意义。

请不要听到“内购”就惊慌逃跑，听完我的解释再做选择：我本人 #{bold}# 坚决 #CRIMSON#反对#LAST# 氪金胜利 #{normal}#，因此我保证绝不会做这种事情。

那么，为什么要加入内购呢？马基·埃亚尔的传说是一款便宜/免费的游戏，也不需要会员订阅。它就像我的孩子一样；我非常爱它，并计划为之长久工作（从2009年开始我就一直这么干了！）。但是，为了生存，我仍然需要在现实世界中取得必要的收入。

目前，我提供了以下几种内购项：
- #GOLD#时装#LAST#：在目前游戏内已有的种族、物品时装外，你可以获得更多时装效果，让你看起来更靓！
- #GOLD#氪金速死#LAST#：已经不想玩这个角色了吗？用这个选项来迎接一个帅气的终结吧！
- #GOLD#额外共享装备格#LAST#：对于捐赠者而言，可以把那些“无用”的捐赠换成更多在线共享装备格。
- #GOLD#社区事件#LAST#：服务器会自动触发部分在线事件，而你可以强制让服务器触发特定事件。当然，当前在线的所有玩家都会收到该事件！

我希望这些能说服你，我并没有什么邪恶的想法（虽然我名为DarkGod）。我不得不说，内购这种事情让我感觉很龌龊，即使上面这些选项都不影响游戏内容，但为了游戏的未来，我必须想尽办法。
感谢你看到这里，去享受游戏吧！
```

## entry-00043
位置：engine.lua:1102；section：engine/engine/dialogs/microtxn/ShowPurchasable.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{italic}##UMBER#Bonus vault slots from this order: #ROYAL_BLUE#%d#{normal}#
```
译文：
```text
#{italic}##UMBER#这项购买提供的额外在线仓库空间：#ROYAL_BLUE#%d#{normal}#
```

## entry-00044
位置：engine.lua:1107；section：engine/engine/dialogs/microtxn/ShowPurchasable.lua；source_tag：_t；args_order：None；special：None

原文：
```text
For every donations you've ever made you have earned voratun coins. These can be spent purchasing expansions or options on the online store. This is the amount you have left, if your purchase total is below this number you'll instantly get your purchase validated, if not you'll need to donate some more first.
#GOLD##{italic}#Thanks for your support, every little bit helps the game survive for years on!#{normal}#
```
译文：
```text
你历次所做的每一笔捐赠，都为你赚取了沃瑞钽硬币，可以用于购买扩展DLC或者在线商店的商品。这是你当前可用的硬币，如果购买价格在这以下，你可以立刻获得商品，否则你需要进行更多的捐赠。
#GOLD##{italic}#感谢你的支持，每一分钱都让这游戏更加持久！#{normal}#
```

## entry-00045
位置：engine.lua:1111；section：engine/engine/dialogs/microtxn/ShowPurchasable.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#YELLOW#-- connecting to server... --
```
译文：
```text
#YELLOW#-- 正在连接到服务器… --
```

## entry-00046
位置：engine.lua:1119；section：engine/engine/dialogs/microtxn/ShowPurchasable.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Let's do it! (Opens in your browser)
```
译文：
```text
开始吧！（在浏览器中打开）
```

## entry-00047
位置：engine.lua:1126；section：engine/engine/dialogs/microtxn/ShowPurchasable.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
  (%d items in cart, %s)
```
译文：
```text
  (购物车中有%d件物品，%s)
```

## entry-00048
位置：engine.lua:1132；section：engine/engine/dialogs/microtxn/ShowPurchasable.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Shimmer pack installed!
```
译文：
```text
时装包安装成功！
```

## entry-00049
位置：engine.lua:1133；section：engine/engine/dialogs/microtxn/ShowPurchasable.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Could not dynamically link addon to current character, maybe the installation weng wrong.
You can fix that by manually downloading the addon from https://te4.org/ and placing it in game/addons/ folder.
```
译文：
```text
无法自动将插件链接至当前角色，可能安装失败了。
你可以在 https://te4.org/ 手动下载该插件并放置于 game/addons/ 目录下来解决这个问题。
```

## entry-00050
位置：engine.lua:1136；section：engine/engine/dialogs/microtxn/ShowPurchasable.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Downloading cosmetic pack: #LIGHT_GREEN#%s
```
译文：
```text
时装包下载中：#LIGHT_GREEN#%s
```

## entry-00051
位置：engine.lua:1138；section：engine/engine/dialogs/microtxn/ShowPurchasable.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
- #{bold}##ROYAL_BLUE#%s #SLATE#x%d#WHITE##{normal}#: You can now trigger it whenever you are ready.
```
译文：
```text
- #{bold}##ROYAL_BLUE#%s #SLATE#x%d#WHITE##{normal}#：准备好的时候就可以触发它。
```

## entry-00052
位置：engine.lua:1139；section：engine/engine/dialogs/microtxn/ShowPurchasable.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
- #{bold}##ROYAL_BLUE#%s #SLATE#x%d#WHITE##{normal}#: Your available vault space has increased.
```
译文：
```text
- #{bold}##ROYAL_BLUE#%s #SLATE#x%d#WHITE##{normal}#：你可用的在线共享装备空间增加了。
```

## entry-00053
位置：engine.lua:1162；section：engine/engine/dialogs/microtxn/ShowPurchasable.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{bold}##GOLD#Once per Character#WHITE##{normal}#: This event can only be received #{bold}#once per character#{normal}#. Usualy because it adds a new zone or effect to the game that would not make sense to duplicate.
```
译文：
```text
#{bold}##GOLD#每角色限一次#WHITE##{normal}#：这个事件 #{bold}#每名角色只能接收一次#{normal}#。通常是因为它添加了新地城或者其他游戏内不能重复添加的效果。
```

## entry-00054
位置：engine.lua:1163；section：engine/engine/dialogs/microtxn/ShowPurchasable.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{bold}##GOLD#Shimmer Pack#WHITE##{normal}#: Once purchased the game will automatically install the shimmer pack to your game and enable it for your current character too (you will still need to use the Mirror of Reflection to switch them on).
#LIGHT_GREEN#Bonus perk:#LAST# purchasing any shimmer pack will also give your characters a portable Mirror of Reflection to be able to change your appearance anywhere, anytime!
```
译文：
```text
#{bold}##GOLD#时装包#WHITE##{normal}#：购买后游戏会自动安装时装包，同时为当前角色自动开启。仍然需要使用反射之镜来切换。
#LIGHT_GREEN#额外福利：#LAST# 购买任何时装包后，你的角色自动获得便携式反射之镜，可以随时随地切换时装！
```

## entry-00055
位置：engine.lua:1166；section：engine/engine/dialogs/microtxn/ShowPurchasable.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{bold}##GOLD#UI Pack#WHITE##{normal}#: Once purchased the game will automatically install the UI pack to your game.
```
译文：
```text
#{bold}##GOLD#UI 组合包#WHITE##{normal}#：购买后游戏会自动安装UI组合包。
```

## entry-00056
位置：engine.lua:1173；section：engine/engine/dialogs/microtxn/UsePurchased.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#YELLOW#-- connecting to server... --
```
译文：
```text
#YELLOW#-- 正在连接到服务器… --
```

## entry-00057
位置：engine.lua:1176；section：engine/engine/dialogs/microtxn/UsePurchased.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Please use purchased options when not on the worldmap.
```
译文：
```text
请不要在世界地图上使用已购买的选项。
```

## entry-00058
位置：engine.lua:1178；section：engine/engine/dialogs/microtxn/UsePurchased.lua；source_tag：_t；args_order：None；special：None

原文：
```text
This option requires you to accept to receive events from the server.
Either you have the option currently disabled or you are playing a campaign that can not support these kind of events (mainly the Arena).
Make sure you have #GOLD##{bold}#Allow online events#WHITE##{normal}# in the #GOLD##{bold}#Online#WHITE##{normal}# section of the game options set to "all". You can set it back to your own setting once you have received the event.

```
译文：
```text
这一选项需要你同意接收服务器发来的事件。
可能是你当前关闭了这一选项，或者正在游玩不支持这类事件的战役（主要是竞技场）。
请确保在游戏设置的#GOLD##{bold}#在线#WHITE##{normal}#选项中将#GOLD##{bold}#允许在线事件#WHITE##{normal}# 设置为“全部”。收到事件之后，你可以把它改回你原本的设置。

```

## entry-00059
位置：engine.lua:1185；section：engine/engine/dialogs/microtxn/UsePurchased.lua；source_tag：_t；args_order：None；special：None

原文：
```text
This pack is already installed and in use for your character.
```
译文：
```text
这个包已经安装，并且正在你的角色上使用中。
```

## entry-00060
位置：engine.lua:1189；section：engine/engine/dialogs/microtxn/UsePurchased.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
There was an error from the server: %s
```
译文：
```text
服务器发生错误：%s
```

## entry-00061
位置：engine.lua:1198；section：engine/engine/interface/ActorInventory.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s picks up (%s.): %s%s.
```
译文：
```text
%s拾取了（%s）：%s%s。
```

## entry-00062
位置：engine.lua:1212；section：engine/engine/interface/ActorInventory.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s can not wear (%s): %s (%s).
```
译文：
```text
%s无法装备（%s）：%s（%s）。
```

## entry-00063
位置：engine.lua:1213；section：engine/engine/interface/ActorInventory.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s wears: %s.
```
译文：
```text
%s 装备了：%s。
```

## entry-00064
位置：engine.lua:1214；section：engine/engine/interface/ActorInventory.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s wears (offslot): %s.
```
译文：
```text
%s副手装备了：%s。
```

## entry-00065
位置：engine.lua:1215；section：engine/engine/interface/ActorInventory.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s wears (replacing %s): %s.
```
译文：
```text
%s装备（替换%s）了：%s。
```

## entry-00066
位置：engine.lua:1223；section：engine/engine/interface/ActorLife.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s attacks %s.
```
译文：
```text
%s攻击了%s。
```

## entry-00067
位置：engine.lua:1228；section：engine/engine/interface/ActorTalents.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
%s is still on cooldown for %d turns.
```
译文：
```text
%s仍在冷却中，还需%d回合。
```

## entry-00068
位置：engine.lua:1230；section：engine/engine/interface/ActorTalents.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Use %s?
```
译文：
```text
使用%s？
```

## entry-00069
位置：engine.lua:1238；section：engine/engine/interface/ActorTalents.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
not enough stat: %s
```
译文：
```text
属性点不足：%s
```

## entry-00070
位置：engine.lua:1245；section：engine/engine/interface/ActorTalents.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
- Lower talents of the same category: %d
```
译文：
```text
- 同系低阶技能数：%d
```

## entry-00071
位置：engine.lua:1247；section：engine/engine/interface/ActorTalents.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
- Talent %s (not known)
```
译文：
```text
- 技能%s（未学习）
```

## entry-00072
位置：engine.lua:1260；section：engine/engine/interface/GameTargeting.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Tactical display disabled. Press shift+'t' to enable.
```
译文：
```text
战术视图关闭。请按 Shift+T 启用。
```

## entry-00073
位置：engine.lua:1265；section：engine/engine/interface/GameTargeting.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Tactical display enabled. Press shift+'t' to disable.
```
译文：
```text
战术视图启用。请按 Shift+T 关闭。
```

## entry-00074
位置：engine.lua:1271；section：engine/engine/interface/ObjectActivable.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
It can be used to %s, costing %d power out of %d/%d.
```
译文：
```text
可以用于 %s，消耗 %d 点能量（当前 %d/%d）。
```

## entry-00075
位置：engine.lua:1272；section：engine/engine/interface/ObjectActivable.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
It can be used to activate talent: %s (level %d).
```
译文：
```text
可以用于激活技能：%s (等级 %d)。
```

## entry-00076
位置：engine.lua:1273；section：engine/engine/interface/ObjectActivable.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
It can be used to activate talent: %s (level %d), costing %d power out of %d/%d.
```
译文：
```text
可以用于激活技能：%s（等级 %d），消耗 %d 点能量（当前 %d/%d）。
```

## entry-00077
位置：engine.lua:1281；section：engine/engine/interface/PlayerExplore.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You are exploring, press any key to stop.
```
译文：
```text
你正在自动探索，请按任意键停止。
```

## entry-00078
位置：engine.lua:1288；section：engine/engine/interface/PlayerHotkeys.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You may define a hotkey by pressing 'm' and following the instructions there.
```
译文：
```text
你可以按 M 键打开技能窗口，按其中的提示绑定快捷键。
```

## entry-00079
位置：engine.lua:1302；section：engine/engine/interface/PlayerRest.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
%s...
```
译文：
```text
%s中…
```

## entry-00080
位置：engine.lua:1304；section：engine/engine/interface/PlayerRest.lua；source_tag：log；args_order：None；special：None

原文：
```text
%s starts...
```
译文：
```text
%s开始了…
```

## 相关术语快照
```tsv
Maj'Eyal	马基·埃亚尔	T.PN.WORLD	places	_t	preferred	core	维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
The Arena	竞技场	T.NARRATIVE.ACHIEVEMENT	narrative	achievement name	existing	core	
The Arena	竞技场	T.UI.LABEL	ui	_t	existing	core	与成就名称同源但分类不同
The Way	维网	T.PN.FACTION	society	nil	existing	core	
Vault	撑杆跳	T.GAME.TALENT	talents	talent name	existing	core	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
iron	铁	T.GAME.ENTITY	items	entity subtype	preferred	global	基础金属材料（22 处）
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
sense	感知	T.GAME.EFFECT	combat	effect subtype	existing	global	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
tactic	战术	T.GAME.EFFECT	combat	effect subtype	existing	global	
tactical	战术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 tactic 同义的变体
voratun	沃瑞钽	T.GAME.ENTITY	items	entity subtype	preferred	global	最高级金属材料（22 处）；与 iron 铁、steel 钢并列
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
