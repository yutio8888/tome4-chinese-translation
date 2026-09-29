# batch-003：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-00081
位置：engine.lua:1313；section：engine/engine/interface/PlayerRun.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
You don't see how to get there...
```
译文：
```text
你不知道怎么到达那里…
```

## entry-00082
位置：engine.lua:1320；section：engine/engine/interface/PlayerRun.lua；source_tag：log；args_order：None；special：None

原文：
```text
Ran for %d turns (stop reason: %s).
```
译文：
```text
奔跑了%d回合（中断原因：%s）。
```

## entry-00083
位置：engine.lua:1325；section：engine/engine/interface/WorldAchievements.lua；source_tag：log；args_order：None；special：None

原文：
```text
#%s#Personal New Achievement: %s!
```
译文：
```text
#%s#个人新成就：%s！
```

## entry-00084
位置：engine.lua:1326；section：engine/engine/interface/WorldAchievements.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Personal New Achievement: #%s#%s
```
译文：
```text
个人新成就：#%s#%s
```

## entry-00085
位置：engine.lua:1327；section：engine/engine/interface/WorldAchievements.lua；source_tag：log；args_order：None；special：None

原文：
```text
#%s#New Achievement: %s!
```
译文：
```text
#%s#新成就：%s！
```

## entry-00086
位置：engine.lua:1328；section：engine/engine/interface/WorldAchievements.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
New Achievement: #%s#%s
```
译文：
```text
新成就：#%s#%s
```

## entry-00087
位置：engine.lua:1388；section：engine/engine/ui/WebView.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Are you sure you want to install this addon: #LIGHT_GREEN##{bold}#%s#{normal}##LAST# ?
```
译文：
```text
你确认要安装这个插件吗：#LIGHT_GREEN##{bold}#%s#{normal}##LAST#？
```

## entry-00088
位置：engine.lua:1390；section：engine/engine/ui/WebView.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Are you sure you want to install this module: #LIGHT_GREEN##{bold}#%s#{normal}##LAST#?
```
译文：
```text
你确认要安装这个模组吗：#LIGHT_GREEN##{bold}#%s#{normal}##LAST#？
```

## entry-00089
位置：engine.lua:1393；section：engine/engine/ui/WebView.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Game installed!
```
译文：
```text
游戏安装完成！
```

## entry-00090
位置：engine.lua:1420；section：engine/modules/boot/class/Game.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#"Tales of Maj'Eyal"#WHITE# is the main game, you can also install more addons or modules by going to https://te4.org/

When inside a module remember you can press Escape to bring up a menu to change keybindings, resolution and other module specific options.

Remember that in most roguelikes death is usually permanent so be careful!

Now go and have some fun!
```
译文：
```text
#GOLD#马基·埃亚尔的传说#WHITE# 是主游戏，你也可以在 https://te4.org/ 下载到更多游戏插件和游戏模组。

在游戏模组内，你可以按 Esc 键打开菜单，改变按键绑定，游戏分辨率和其他和模组有关的设置。

请记住，在大部分Roguelike游戏里，角色的死亡都是永久的，请小心！

玩的开心！
```

## entry-00091
位置：engine.lua:1446；section：engine/modules/boot/class/Game.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Oops! Either you activated safe mode manually or the game detected it did not start correctly last time and thus you are in #LIGHT_GREEN#safe mode#WHITE#.
Safe Mode disabled all graphical options and sets a low FPS. It is not advisable to play this way (as it will be very painful and ugly).

Please go to the Video Options and try enabling/disabling options and then restarting until you do not get this message.
A usual problem is shaders and thus should be your first target to disable.
```
译文：
```text
糟糕！如果你不是手动开启了安全模式的话，那么说明，游戏检测到上一次启动时发生错误，目前游戏已进入#LIGHT_GREEN#安全模式#WHITE#。
在安全模式下，所有图形选项都被关闭，FPS被设置为很低。不建议在这种情况下进行游戏（游戏画面会变得很难看）。

请你进入游戏视频选项，尝试启用或禁用各项选项并重启游戏，直到不再弹出此消息。
常见的问题一般是由着色器引发的，你可以先尝试关闭这些选项。
```

## entry-00092
位置：engine.lua:1457；section：engine/modules/boot/class/Game.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Oops! It seems like you have the same addon/dlc installed twice.
This is unsupported and would make many things explode. Please remove one of the copies.

Addon name: #YELLOW#%s#LAST#

Check out the following folder on your computer:
%s
%s

```
译文：
```text
糟糕！好像你安装了多份同一个插件/DLC。
这种情况不被支持的，会引发很多BUG。请你移除掉多余的文件。

插件名称：#YELLOW#%s#LAST#

请你检查你电脑里的以下文件夹：
%s
%s

```

## entry-00093
位置：engine.lua:1474；section：engine/modules/boot/class/Game.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Updating addon: #LIGHT_GREEN#%s
```
译文：
```text
正在更新插件：#LIGHT_GREEN#%s
```

## entry-00094
位置：engine.lua:1478；section：engine/modules/boot/class/Game.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Welcome to #LIGHT_GREEN#Tales of Maj'Eyal#LAST#!

Before you can start dying in many innovative ways we need to ask you about online play.

This is a #{bold}#single player game#{normal}# but it also features many online features to enhance your gameplay and connect you to the community:
* Play from several computers without having to copy unlocks and achievements.
* Talk ingame to other fellow players, ask for advice, share your most memorable moments...
* Keep track of your kill count, deaths, most played classes...
* Cool statistics for to help sharpen your gameplay style
* Install official expansions and third-party addons directly from the game, hassle-free
* Access your purchaser / donator bonuses if you have bought the game or donated on https://te4.org/
* Help the game developers balance and refine the game

You will also have a user page on #LIGHT_BLUE#https://te4.org/#LAST# to show off to your friends.
This is all optional, you are not forced to use this feature at all, but the developer would thank you if you did as it will make balancing easier.
```
译文：
```text
欢迎来到#LIGHT_GREEN#马基·埃亚尔的传说#LAST#！

在你开始尝试这个游戏里无数有趣的死法之前，我们想问你一下有关在线游戏的事情。

马基·埃亚尔的传说是一个#{bold}#单人游戏#{normal}#，但也提供了丰富的在线功能，可以增强你的游戏体验，并让你和游戏社区建立联系：
* 在多台电脑上游玩，而不需要复制游戏解锁和成就。
* 与其他玩家在游戏内聊天，寻求建议，分享难忘的时刻…
* 记录你的击杀数量，死亡次数，以及玩得最多的职业…
* 用有趣的统计数据帮你打磨自己的游戏风格
* 在游戏里直接安装官方扩展包和第三方插件，免去手动安装的麻烦
* 如果你购买了游戏或是在 https://te4.org/ 上进行了捐助，你可以获得你的购买者/赞助者独享权益
* 帮助游戏开发者调整游戏平衡，让这个游戏变得更好。

你也会获得一个 #LIGHT_BLUE#https://te4.org/#LAST# 上的用户页面，可以用来向你的朋友炫耀。
这一切都是可选的，你可以自愿使用或者关闭这些功能。如果你愿意开启它们，开发者会感谢你的，因为这会让平衡调整变得更简单。
```

## entry-00095
位置：engine.lua:1513；section：engine/modules/boot/class/Game.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Registering...
```
译文：
```text
正在注册…
```

## entry-00096
位置：engine.lua:1518；section：engine/modules/boot/class/Game.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Creation failed: %s (you may also register on https://te4.org/)
```
译文：
```text
创建失败：%s（你也可以在 https://te4.org/ 网站上注册）
```

## entry-00097
位置：engine.lua:1538；section：engine/modules/boot/data/damage_types.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Kill!
```
译文：
```text
击杀！
```

## entry-00098
位置：engine.lua:1583；section：engine/modules/boot/data/general/npcs/canine.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Lean, mean, and shaggy, it stares at you with hungry eyes.
```
译文：
```text
它精瘦、凶悍、皮毛蓬松，正用饥饿的眼神盯着你。
```

## entry-00099
位置：engine.lua:1596；section：engine/modules/boot/data/general/npcs/skeleton.lua；source_tag：entity name；args_order：None；special：None

原文：
```text
degenerated skeleton warrior
```
译文：
```text
退化骷髅战士
```

## entry-00100
位置：engine.lua:1607；section：engine/modules/boot/data/general/npcs/troll.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Green-skinned and ugly, this massive humanoid glares at you, clenching wart-covered green fists.
```
译文：
```text
这只绿皮丑陋的庞大人形生物正盯着你，同时它握紧了满是疣的绿色拳头。
```

## entry-00101
位置：engine.lua:1613；section：engine/modules/boot/data/general/npcs/troll.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A large and athletic troll with an extremely tough and warty hide.
```
译文：
```text
一只高大且强壮的巨魔，皮肤异常坚韧且长满疣。
```

## entry-00102
位置：engine.lua:1623；section：engine/modules/boot/data/talents.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Flame
```
译文：
```text
火焰
```

## entry-00103
位置：engine.lua:1648；section：engine/modules/boot/dialogs/Addons.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You can get new addons at #LIGHT_BLUE##{underline}#Te4.org Addons#{normal}#
```
译文：
```text
在以下位置可以获得新的插件：#LIGHT_BLUE##{underline}#Te4.org 插件页面#{normal}#
```

## entry-00104
位置：engine.lua:1674；section：engine/modules/boot/dialogs/Credits.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Expert Shaders Design
```
译文：
```text
着色器设计专家
```

## entry-00105
位置：engine.lua:1697；section：engine/modules/boot/dialogs/FirstRun.lua；source_tag：_t；args_order：None；special：None

原文：
```text
You are about to disable all connectivity to the network.
This includes, but is not limited to:
- Player profiles: You will not be able to login, register
- Characters vault: You will not be able to upload any character to the online vault to show your glory
- Item's Vault: You will not be able to access the online item's vault, this includes both storing and retrieving items.
- Ingame chat: The ingame chat requires to connect to the server to talk to other players, this will not be possible.
- Purchaser / Donator benefits: The base game being free, the only way to give donators their bonuses fairly is to check their online profile. This will thus be disabled.
- Easy addons downloading & installation: You will not be able to see ingame the list of available addons, nor to one-click install them. You may still do so manually.
- Version checks: Addons will not be checked for new versions.
- Discord: If you are a Discord user, Rich Presence integration will also be disabled by this setting.
- Ingame game news: The main menu will stop showing you info about new updates to the game.

#{bold}##CRIMSON#This is an extremely restrictive setting. It is recommended you only activate it if you have no other choice as it will remove many fun and acclaimed features.#{normal}#

If you disable this option you can always re-activate it in the Online category of the Game Options menu later on.
```
译文：
```text
即将禁止所有网络请求
包括但不仅限于：
- 用户信息：不能登录或者注册。
- 角色备份：不能在te4.org上保存你的角色信息（用来给其他人分享你的炫酷角色）。
- 物品仓库：不能访问你的在线物品仓库（包括存入和取回）。
- 游戏内聊天：游戏内聊天需要连接服务器才能与其他玩家交谈，这将无法使用。
- 购买者/捐助者福利：基础游戏免费，公平发放捐助者奖励的唯一途径是检查他们的在线档案，因此该功能将被禁用。
- 插件便捷下载与安装：你将无法在游戏内看到可用插件列表，也无法一键安装，但仍可手动安装。
- 插件版本检查：插件将不再检查新版本。
- Discord：如果你是 Discord 用户，此设置也会禁用 Rich Presence 集成。
- 游戏内新闻：主菜单将不再显示游戏更新信息。

#{bold}##CRIMSON#这是一个极端的选项。如果不是迫不得已，推荐你不要打开它，这会让你失去很多好用的功能和一些游戏体验。#{normal}#

关闭后，可以通过游戏设置菜单的在线选项卡打开。
```

## entry-00106
位置：engine.lua:1737；section：engine/modules/boot/dialogs/LoadGame.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
#{bold}##GOLD#%s: %s#WHITE##{normal}#
Game version: %d.%d.%d
Requires addons: %s

%s
```
译文：
```text
#{bold}##GOLD#%s：%s#WHITE##{normal}#
游戏版本：%d.%d.%d
需要的插件：%s

%s
```

## entry-00107
位置：engine.lua:1755；section：engine/modules/boot/dialogs/LoadGame.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_RED#WARNING: #LAST#Loading a savefile while in developer mode will permanently invalidate it. Proceed?
```
译文：
```text
#LIGHT_RED#警告：#LAST#在开发者模式下读取一个存档将会不可逆地将其标记为作弊存档。确定吗？
```

## entry-00108
位置：engine.lua:1761；section：engine/modules/boot/dialogs/LoadGame.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Downloading old game data: #LIGHT_GREEN#
```
译文：
```text
正在下载旧版游戏数据：#LIGHT_GREEN#
```

## entry-00109
位置：engine.lua:1762；section：engine/modules/boot/dialogs/LoadGame.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Old game data for %s correctly installed. You can now play.
```
译文：
```text
%s 的旧版游戏数据已经安装成功了。你可以现在游玩了。
```

## entry-00110
位置：engine.lua:1779；section：engine/modules/boot/dialogs/MainMenu.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{bold}##GOLD#Ashes of Urh'Rok - Expansion#LAST##{normal}#
#{italic}##ANTIQUE_WHITE#Many in Maj'Eyal have heard of "demons", sadistic creatures who appear seemingly from nowhere, leaving a trail of suffering and destruction wherever they go.#{normal}##LAST#

#{bold}#Features#{normal}#:
#LIGHT_UMBER#New class:#WHITE# Doombringers. These avatars of demonic destruction charge into battle with massive two-handed weapons, cutting swaths of firey devastation through hordes of opponents. Armed with flame magic and demonic strength, they delight in fighting against overwhelming odds
#LIGHT_UMBER#New class:#WHITE# Demonologists. Bearing a shield and the magic of the Spellblaze itself, these melee-fighting casters can grow demonic seeds from their fallen enemies. Imbue these seeds onto your items to gain a wide array of new talents and passive benefits, and summon the demons within them to fight!
#LIGHT_UMBER#New race:#WHITE# Doomelves. Shalore who've taken to the demonic alterations especially well, corrupting their typical abilities into a darker form.
#LIGHT_UMBER#New artifacts, lore, zones, events...#WHITE# For your demonic delight!


```
译文：
```text
#{bold}##GOLD#乌鲁洛克之烬 - 游戏扩展包#LAST##{normal}#
#{italic}##ANTIQUE_WHITE#很多马基埃亚尔的居民都曾经听说过“恶魔”的名字，它们是一群似乎凭空出现的暴虐生物，无论走到哪里都会带来痛苦和毁灭。#{normal}##LAST#

#{bold}#扩展包特性#{normal}#:
#LIGHT_UMBER#新职业：#WHITE# 毁灭使者。他们是恶魔毁灭力量的化身，手拿双手武器加入战斗，将敌人化为一片火海。他们的手中掌握着火焰的魔法和恶魔的力量，在与势不可挡的敌人战斗中寻求欢愉。
#LIGHT_UMBER#新职业：#WHITE# 恶魔使者。这些近战施法者手拿盾牌，掌握魔法大爆炸本身的力量，可以从倒下的敌人身上培育出恶魔种子。将这些恶魔种子附魔到你的物品里，可以获得各种全新的技能和被动的能力，并召唤种子里的恶魔来加入战斗！
#LIGHT_UMBER#新种族：#WHITE# 魔化精灵。那些被恶魔的力量所改变的永恒精灵，他们的种族能力被腐化成了黑暗的形态。
#LIGHT_UMBER#更多新神器、新手札、新地图、新事件……#WHITE# 体验恶魔的欢愉吧！


```

## entry-00111
位置：engine.lua:1800；section：engine/modules/boot/dialogs/MainMenu.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{bold}##GOLD#Embers of Rage - Expansion#LAST##{normal}#
#{italic}##ANTIQUE_WHITE#One year has passed since the one the Orcs call the "Scourge from the West" came and single-handedly crushed the Orc Prides of Grushnak, Vor, Gorbat, and Rak'Shor.  The Allied Kingdoms, now linked by farportal to their distant, long-lost Sunwall allies, have helped them conquer most of Var'Eyal.  The few remnants of the ravaged Prides are caged...  but one Pride remains.#{normal}##LAST#

#{bold}#Features#{normal}#:
#LIGHT_UMBER#A whole new campaign:#WHITE# Set one year after the events of the main game, the final destiny of the Orc Prides is up to you. Discover the Far East like you never knew it. 
#LIGHT_UMBER#New classes:#WHITE# Sawbutchers, Gunslingers, Psyshots, Annihilators and Technomanchers. Harness the power of steam to power deadly contraptions to lay waste to all those that oppose the Pride!  
#LIGHT_UMBER#New races:#WHITE# Orcs, Yetis, Whitehooves. Discover the orcs and their unlikely 'allies' as you try to save your Pride from the disasters caused by the one you call 'The Scourge from the West'.
#LIGHT_UMBER#Tinker system:#WHITE# Augment your items with powerful crafted tinkers. Attach rockets to your boots, gripping systems to your gloves and many more.
#LIGHT_UMBER#Salves:#WHITE# Bound to the tinker system, create powerful medical salves to inject into your skin, replacing the infusions§runes system.
#LIGHT_UMBER#A ton#WHITE# of artifacts, lore, zones, events... 


```
译文：
```text
#{bold}##GOLD#余烬怒火 - 游戏扩展包#LAST##{normal}#
#{italic}##ANTIQUE_WHITE#自从被兽人称为“西方灾星”的那个人，孤身一人粉碎了格鲁希纳克、沃尔、加伯特和拉克肖四大部落之后，已经过了一年的时间。联合王国现在已经通过远行传送门，和他们失落已久的盟友太阳堡垒建立了联系，帮助他们征服了瓦·埃亚尔大陆的近乎全境。被战火蹂躏的兽人部落的少数残余，现在都被联军关押在监狱里……但是，还有一个部落存活了下来。#{normal}##LAST#

#{bold}#扩展包特性#{normal}#:
#LIGHT_UMBER#全新战役：#WHITE# 故事发生在主游戏事件的一年之后，兽人部落的最终命运由你决定。去探索一个你从未认识过的远东大陆吧！
#LIGHT_UMBER#全新职业：#WHITE# 链锯屠夫，枪手，念力射手，歼灭者和科技法师。掌握蒸汽的力量，驱动致命的装置，用钢铁洪流粉碎那些胆敢反抗部落的人吧！
#LIGHT_UMBER#全新种族：#WHITE# 兽人，雪人，白蹄。了解兽人和他们那些出人意料的“盟友”，努力将你的部落从那个你们称为“西方灾星”的人所带来的灾难中拯救出来。
#LIGHT_UMBER#嵌件系统：#WHITE# 合成强大的嵌件，用于强化你的物品。包括给你的靴子安装火箭，给你的手套安装抓取系统，乃至许多更多的嵌件。
#LIGHT_UMBER#药剂系统：#WHITE# 在嵌件系统中，合成强大的医疗药剂，用于注入你的皮肤，替代原有的纹身和符文系统。
#LIGHT_UMBER#大量#WHITE# 全新神器、手札、地图和事件！


```

## entry-00112
位置：engine.lua:1823；section：engine/modules/boot/dialogs/MainMenu.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{bold}##GOLD#Forgotten Cults - Expansion#LAST##{normal}#
#{italic}##ANTIQUE_WHITE#Not all adventurers seek fortune, not all that defend the world have good deeds in mind. Lately the number of sightings of horrors have grown tremendously. People wander off the beaten paths only to be found years later, horribly mutated and partly insane, if they are found at all. It is becoming evident something is stirring deep below Maj'Eyal. That something is you.#{normal}##LAST#

#{bold}#Features#{normal}#:
#LIGHT_UMBER#New class:#WHITE# Writhing Ones. Give in to the corrupting forces and turn yourself gradually into an horror, summon horrors to do your bidding, shed your skin and melt your face to assault your foes. With your arm already turned into a tentacle, what creature can stop you?
#LIGHT_UMBER#New class:#WHITE# Cultists of Entropy. Using its insanity and control of entropic forces to unravel the normal laws of physic this caster class can turn healing into attacks and call upon the forces of the void to reduce its foes to dust.
#LIGHT_UMBER#New race:#WHITE# Drems. A corrupt subrace of dwarves, that somehow managed to keep a shred of sanity to not fully devolve into mindless horrors. They can enter a frenzy and even learn to summon horrors.
#LIGHT_UMBER#New race:#WHITE# Krogs. Ogres transformed by the very thing that should kill them. Their powerful attacks can stun their foes and they are so strong they can dual wield any one handed weapons.
#LIGHT_UMBER#Many new zones:#WHITE# Explore the Scourge Pits, fight your way out of a giant worm (don't ask how you get *in*), discover the wonders of the Occult Egress and many more strange and tentacle-filled zones!
#LIGHT_UMBER#New horrors:#WHITE# You liked radiant horrors? You'll love searing horrors! And Nethergames. And Entropic Shards. And ... more
#LIGHT_UMBER#Sick of your own head:#WHITE#  Replace it with a nice cozy horror!
#LIGHT_UMBER#A ton#WHITE# of artifacts, lore, events... 


```
译文：
```text
#{bold}##GOLD#禁忌邪教 - 游戏扩展包#LAST##{normal}#
#{italic}##ANTIQUE_WHITE#不是所有的冒险者都在寻求财富，也不是所有保卫世界的人都心存善念。最近，恐魔在大陆上出现的次数急剧增加。不断有人在偏僻的小路上失踪，有时几年后才被人发现，身体却遭受了恐怖的变异，神智也部分失常，也有时候再也无法寻到踪迹。很明显，在马基·埃亚尔的大地深处，有某种东西正在暗中活动。那种东西——就是你。#{normal}##LAST#

#{bold}#扩展包特性#{normal}#:
#LIGHT_UMBER#新职业：#WHITE# 扭动者。屈服于腐化的力量，让自己逐渐变成一只恐魔。你可以召唤恐魔在战斗中协助自己，褪去自己的皮肤，融化自己的脸庞，作为攻击的武器。当你的手臂也被转化成触手之后，还有什么敌人能阻挡你呢？
#LIGHT_UMBER#新职业：#WHITE# 熵教徒。这种法师职业使用疯狂的能力，掌控了熵的力量，颠覆了传统的物理定律。它们可以将治疗转换成伤害，并召唤虚空的力量，将敌人粉碎为尘土。
#LIGHT_UMBER#新种族：#WHITE# 德瑞姆。他们是矮人的一支腐化分支，但是因为某种原因，保持了一定程度的理性，而没有完全退化成无意识的恐魔。他们可以进入狂热状态，并学会召唤恐魔。
#LIGHT_UMBER#新种族：#WHITE# 克罗格。他们是被本该杀死他们的力量所转化的食人魔。他们强大的攻击可以震慑敌人，并且他们强壮的力量可以双持任何单手武器。
#LIGHT_UMBER#大量全新地图：#WHITE# 探索瘟疫之穴，在一只巨大蠕虫的身体内杀出一条血路(不要问我你是怎么*进来*的)，探索神秘的出口，以及更多奇异的，充满触手的地图！
#LIGHT_UMBER#新的恐魔：#WHITE# 你喜欢光芒恐魔吗？你一定会喜欢上灼光恐魔的！还有彼世之门，还有熵之碎片，还有其他更多怪物！
#LIGHT_UMBER#厌倦了你自己的头？#WHITE#  把它换成一个舒适惬意的恐魔吧！
#LIGHT_UMBER#大量#WHITE# 全新神器、手札、事件……


```

## entry-00113
位置：engine.lua:1864；section：engine/modules/boot/dialogs/MainMenu.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Steam client not found.
```
译文：
```text
找不到Steam客户端。
```

## entry-00114
位置：engine.lua:1911；section：engine/modules/boot/dialogs/ProfileLogin.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Accept to receive #{bold}#very infrequent#{normal}# (a few per year) mails about important game events from us.
```
译文：
```text
允许我们#{bold}#偶尔#{normal}#向你发送有关游戏重要新闻的邮件（每年最多只会有几封）。
```

## entry-00115
位置：engine.lua:1914；section：engine/modules/boot/dialogs/ProfileLogin.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Privacy Policy (opens in browser)
```
译文：
```text
隐私政策（用浏览器打开）
```

## entry-00116
位置：engine.lua:1929；section：engine/modules/boot/dialogs/ProfileSteamRegister.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Welcome to #GOLD#Tales of Maj'Eyal#LAST#.
To enjoy all the features the game has to offer it is #{bold}#highly#{normal}# recommended that you register your steam account.
Luckily this is very easy to do: you only require a profile name and optionally an email (we send very few email, maybe two a year at most).

```
译文：
```text
欢迎来到#GOLD#马基·埃亚尔的传说#LAST#。
为了享受游戏的全部功能，我们#{bold}#强烈#{normal}#推荐你注册你的Steam账户。
幸运的是，这非常容易：你只需要提供你的用户名，也可以提供你的邮箱（我们基本上不会给你发送邮件，每年最多发送一两份）。

```

## entry-00117
位置：engine.lua:1938；section：engine/modules/boot/dialogs/ProfileSteamRegister.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Accept to receive #{bold}#very infrequent#{normal}# (a few per year) mails about important game events from us.
```
译文：
```text
允许我们#{bold}#偶尔#{normal}#向你发送有关游戏重要新闻的邮件（每年最多只会有几封）。
```

## entry-00118
位置：engine.lua:1942；section：engine/modules/boot/dialogs/ProfileSteamRegister.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Privacy Policy (opens in browser)
```
译文：
```text
隐私政策（用浏览器打开）
```

## entry-00119
位置：engine.lua:1949；section：engine/modules/boot/dialogs/ProfileSteamRegister.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Registering...
```
译文：
```text
正在注册…
```

## entry-00120
位置：engine.lua:1951；section：engine/modules/boot/dialogs/ProfileSteamRegister.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Steam client not found.
```
译文：
```text
找不到Steam客户端。
```

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Allied Kingdoms	联合王国	T.PN.FACTION	society	nil	existing	core	
Annihilator	歼灭者	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	兽人战役职业
Ashes of Urh'Rok	乌鲁洛克之烬	T.NARRATIVE.LORE	narrative	newLore category	existing	dlc	Ashes of Urh'Rok 战役名称
Crush	压碎	T.GAME.TALENT	talents	talent name	existing	core	
Demonologist	恶魔使者	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	Ashes of Urh'Rok 职业
Donator	捐赠者	T.GAME.MISC	tech	_t	preferred	core	聊天徽章与成就名称统一为“捐赠者”；不写作“捐助者”
Doombringer	毁灭使者	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	Ashes of Urh'Rok 职业
Drem	德瑞姆	T.PN.RACE	creatures	birth descriptor name	existing	dlc	Cults of Entropy 种族
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Frenzy	狂热	T.GAME.TALENT	talents	talent name	existing	global	
Giant	巨人	T.PN.RACE	creatures	birth descriptor name	existing	core	巨人种族总称
Gunslinger	枪手	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	
Human	人类	T.PN.RACE	creatures	birth descriptor name	existing	core	
Insanity	疯狂值	T.GAME.RESOURCE	resources	_t	existing	dlc	Cults of Entropy 角色资源
Krog	克罗格	T.PN.RACE	creatures	birth descriptor name	existing	dlc	Cults of Entropy 种族
Luck	幸运	T.GAME.STAT	combat	stat name	existing	global	
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Maj'Eyal	马基·埃亚尔	T.PN.WORLD	places	_t	preferred	core	维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Name	名称	T.UI.LABEL	ui	_t	preferred	global	界面标签（17 处）
Occult Egress	神秘的出口	T.PN.PLACE	places	entity name	existing	core	
Ogre	食人魔	T.PN.RACE	creatures	birth descriptor name	existing	core	
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Orc Pride	兽人部落	T.PN.FACTION	society	nil	existing	core	
Psyshot	灵能射手	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	
Rogue	盗贼	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Sawbutcher	链锯屠夫	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	兽人战役职业
Scourge from the West	西方天灾	T.PN.PERSON	society	_t	preferred	dlc	Embers of Rage 中的个体（女性）；统一为“西方天灾”，不写作“灾星”
Shalore	永恒精灵	T.PN.RACE	creatures	nil	existing	core	
Skeleton	骷髅	T.PN.RACE	creatures	birth descriptor name	existing	core	
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Steam	蒸汽	T.GAME.RESOURCE	resources	_t	existing	dlc	Embers of Rage 角色资源
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Tinker	工匠系	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	
Vault	撑杆跳	T.GAME.TALENT	talents	talent name	existing	core	
Warrior	战士系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“战士系”
Whitehooves	白蹄	T.PN.FACTION	society	faction name	existing	dlc	Embers of Rage 阵营
Writhing One	蜿蜒怪人	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	Cults of Entropy 职业
Yeti	雪人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	兽人战役种族
assault	强袭	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
class	职业	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
demonic	恶魔	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
demonic strength	恶魔之力	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
doom	末日	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	Cults of Entropy 技能树/技能类别名；P1 审核确认
drem	德瑞姆	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
entropy	熵	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Cults of Entropy DLC 机制效果类型
entropy	熵	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
frenzy	狂乱	T.GAME.EFFECT	combat	effect subtype	existing	global	与技能名 Frenzy 的译法区分
giant	巨人	T.GAME.ENTITY	creatures	entity type	existing	global	
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
horror	恐怖	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Cults 恐怖/恐惧系效果类别（Putrescent Pustule、Horrific Display 等）；entity type 语境的“恐魔”保留；P0 审核确认
horror	恐魔	T.GAME.ENTITY	creatures	entity type	existing	global	
human	人类	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
humanoid	人形生物	T.GAME.ENTITY	creatures	entity type	existing	global	
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
infusion	充能	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	炼金术师为宝石炸弹注入元素力量的技能类型；区别于刻印物品 Infusion（纹身）
infusions	纹身	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
insanity	疯狂	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Cults of Entropy DLC 机制效果类型
krog	克罗格	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Cults of Entropy 实体子类型
krog	克罗格	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
nether	彼世	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
orc prides	兽人部落	T.NARRATIVE.LORE	narrative	newLore category	existing	dlc	与地点/阵营名称按 source_tag 区分
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
radiant horror	光芒恐魔	T.GAME.ENTITY	creatures	entity name	preferred	core	核心实体名称；与 1.8beta 的实体译法一致，描述性复数文本仍按语境处理
runes	符文	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
spellblaze	魔法大爆炸	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
spellblaze	魔法大爆炸	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与世界事件的其他标签区分
spellblaze	魔法大爆炸	T.PN.WORLD	places	effect subtype	existing	core	
steam	蒸汽	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Embers of Rage DLC 机制效果类型
steam	蒸汽	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	Embers of Rage 技能类别
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
sunwall	太阳堡垒	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
tinker	蒸汽工具	T.GAME.ENTITY	items	entity type	existing	dlc	Embers of Rage 实体类型
trap	陷阱	T.GAME.ENTITY	items	entity name	preferred	global	陷阱实体（20 处）
troll	巨魔	T.GAME.ENTITY	creatures	entity subtype	existing	global	
var'eyal	瓦·埃亚尔	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
whitehooves	白蹄	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
yeti	雪人	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
yeti	雪人	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
```
