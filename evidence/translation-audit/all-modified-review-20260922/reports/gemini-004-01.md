# batch-004 译文复核报告

- **复核批次**：batch-004（条目范围：`entry-00121` 至 `entry-00160`，共 40 条）
- **冻结文件哈希核验**：
  - 路径：`evidence/translation-audit/all-modified-review-20260922/batches/batch-004.md`
  - 预期 SHA-256：`7f402096d61e853d3b74f1a62c44e84784c81af8cfd530222cb6b5044c926dfe`
  - 实测 SHA-256：`7f402096d61e853d3b74f1a62c44e84784c81af8cfd530222cb6b5044c926dfe`（**核验一致**）
- **参考基准**：
  - 引擎与核心模块公开源码固定 commit：`624a67329fe2ad440c5b344785a9c73fcf22ae63`（`/workspace/t-engine4`）
  - 译文终点基准 commit：`7c38a53b88a1c80d7d9b209f84c518ae9f6eac00`
  - DLC 参照说明：涉及官方 DLC（Ashes of Urh'Rok, Embers of Rage, Forgotten Cults）对照时，来源未固定（unpinned）。

---

## 逐条复核详情

### entry-00121
- **位置**：`engine.lua:1953`（section: `engine/modules/boot/dialogs/ProfileSteamRegister.lua`）
- **原文**：`Username or Email already taken, please select an other one.`
- **译文**：`用户名或邮件地址已被使用，请选择其他用户名或邮件地址。`
- **复核结论**：**未发现问题**
- **依据**：源码对应固定 commit 下 `ProfileSteamRegister.lua:89` 的注册冲突弹窗文本；语义准确，标点完整，无占位符或格式标签。

### entry-00122
- **位置**：`engine.lua:1969`（section: `engine/modules/boot/dialogs/UpdateAll.lua`）
- **原文**：`There was an error while downloading:\n`
- **译文**：`下载时发生错误：\n`
- **复核结论**：**未发现问题**
- **依据**：源码对应 `UpdateAll.lua:152` 中追加具体报错的提示前缀；冒号与换行符完全保留。

### entry-00123
- **位置**：`engine.lua:1998`（section: `engine/modules/boot/init.lua`）
- **原文**：`Bootmenu!\n`
- **译文**：`启动菜单！\n`
- **复核结论**：**未发现问题**
- **依据**：源码对应 `boot/init.lua:30` 的 `description` 描述；感叹号与换行符匹配。

### entry-00124
- **位置**：`mod-boot.lua:5`（section: `mod-boot/class/Game.lua`）
- **原文**：
  ```text
  #GOLD#"Tales of Maj'Eyal"#WHITE# is the main game, you can also install more addons or modules by going to https://te4.org/

  When inside a module remember you can press Escape to bring up a menu to change keybindings, resolution and other module specific options.

  Remember that in most roguelikes death is usually permanent so be careful!

  Now go and have some fun!
  ```
- **译文**：
  ```text
  #GOLD#马基·埃亚尔的传说#WHITE# 是主游戏，你也可以在 https://te4.org/ 下载到更多游戏插件和游戏模组。

  在游戏模组内，你可以按 Esc 键打开菜单，改变按键绑定，游戏分辨率和其他和模组有关的设置。

  请记住，在大部分Roguelike游戏里，角色的死亡都是永久的，请小心！

  玩的开心！
  ```
- **复核结论**：**细微观察**
- **依据**：颜色代码 `#GOLD#` / `#WHITE#` 匹配；换行与 URL 保留完好；“马基·埃亚尔”符合 preferred 术语。末句“玩的开心！”中助词“的”按现代汉语语法更推荐使用“得”（“玩得开心！”），属轻微语感瑕疵，不影响语义理解。

### entry-00125
- **位置**：`mod-boot.lua:31`（section: `mod-boot/class/Game.lua`）
- **原文**：
  ```text
  Oops! Either you activated safe mode manually or the game detected it did not start correctly last time and thus you are in #LIGHT_GREEN#safe mode#WHITE#.
  Safe Mode disabled all graphical options and sets a low FPS. It is not advisable to play this way (as it will be very painful and ugly).

  Please go to the Video Options and try enabling/disabling options and then restarting until you do not get this message.
  A usual problem is shaders and thus should be your first target to disable.
  ```
- **译文**：
  ```text
  糟糕！如果你不是手动开启了安全模式的话，那么说明，游戏检测到上一次启动时发生错误，目前游戏已进入#LIGHT_GREEN#安全模式#WHITE#。
  在安全模式下，所有图形选项都被关闭，FPS被设置为很低。不建议在这种情况下进行游戏（游戏画面会变得很难看）。

  请你进入游戏视频选项，尝试启用或禁用各项选项并重启游戏，直到不再弹出此消息。
  常见的问题一般是由着色器引发的，你可以先尝试关闭这些选项。
  ```
- **复核结论**：**未发现问题**
- **依据**：源码对应安全模式弹窗提示；颜色标签 `#LIGHT_GREEN#` / `#WHITE#` 位置正确，段落换行与括号保留完整，排查说明翻译准确。

### entry-00126
- **位置**：`mod-boot.lua:42`（section: `mod-boot/class/Game.lua`）
- **原文**：
  ```text
  Oops! It seems like you have the same addon/dlc installed twice.
  This is unsupported and would make many things explode. Please remove one of the copies.

  Addon name: #YELLOW#%s#LAST#

  Check out the following folder on your computer:
  %s
  %s

  ```
- **译文**：
  ```text
  糟糕！好像你安装了多份同一个插件/DLC。
  这种情况不被支持的，会引发很多BUG。请你移除掉多余的文件。

  插件名称：#YELLOW#%s#LAST#

  请你检查你电脑里的以下文件夹：
  %s
  %s

  ```
- **复核结论**：**细微观察**
- **依据**：源码为 `Game.lua:233` 处的格式化字符串调用，3 个 `%s` 占位符、颜色标记 `#YELLOW#%s#LAST#` 及多行换行均准确对应。第二句“这种情况不被支持的”略缺谓语助词“是”（建议“这种情况是不被支持的”），不影响实际运行与理解。

### entry-00127
- **位置**：`mod-boot.lua:59`（section: `mod-boot/class/Game.lua`）
- **原文**：`Updating addon: #LIGHT_GREEN#%s`
- **译文**：`正在更新插件：#LIGHT_GREEN#%s`
- **复核结论**：**未发现问题**
- **依据**：源码对应 `Game.lua:309` 插件下载进度标题；占位符 `%s` 及颜色代码 `#LIGHT_GREEN#` 完整匹配。

### entry-00128
- **位置**：`mod-boot.lua:63`（section: `mod-boot/class/Game.lua`）
- **原文**：
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
- **译文**：
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
- **复核结论**：**细微观察**
- **依据**：列表格式、颜色代码与富文本样式标记（`#{bold}#`、`#{normal}#`）完整无缺；“马基·埃亚尔”遵循 preferred 规范。第 6 个列表项中将 donator 译为“赞助者”（以及“捐助”），术语快照 line 679 记录“Donator 捐赠者 preferred core（聊天徽章与成就名称统一为‘捐赠者’；不写作‘捐助者’）”，此处表述属口语化扩展，建议后续注意用词统一。

### entry-00129
- **位置**：`mod-boot.lua:98`（section: `mod-boot/class/Game.lua`）
- **原文**：`Registering...`
- **译文**：`正在注册…`
- **复核结论**：**未发现问题**
- **依据**：省略号转化为中文标准省略号 `…`，语义准确。

### entry-00130
- **位置**：`mod-boot.lua:103`（section: `mod-boot/class/Game.lua`）
- **原文**：`Creation failed: %s (you may also register on https://te4.org/)`
- **译文**：`创建失败：%s（你也可以在 https://te4.org/ 网站上注册）`
- **复核结论**：**未发现问题**
- **依据**：占位符 `%s`、全角冒号及括号格式正确，URL 完整保留。

### entry-00131
- **位置**：`mod-boot.lua:123`（section: `mod-boot/data/damage_types.lua`）
- **原文**：`Kill!`
- **译文**：`击杀！`
- **复核结论**：**未发现问题**
- **依据**：源码对应 `damage_types.lua:28` 飘字提示，感叹号与词义匹配。

### entry-00132
- **位置**：`mod-boot.lua:168`（section: `mod-boot/data/general/npcs/canine.lua`）
- **原文**：`Lean, mean, and shaggy, it stares at you with hungry eyes.`
- **译文**：`它精瘦、凶悍、皮毛蓬松，正用饥饿的眼神盯着你。`
- **复核结论**：**未发现问题**
- **依据**：NPC 描述文本，译文流畅准确，标点完整。

### entry-00133
- **位置**：`mod-boot.lua:181`（section: `mod-boot/data/general/npcs/skeleton.lua`）
- **原文**：`degenerated skeleton warrior`
- **译文**：`退化骷髅战士`
- **复核结论**：**未发现问题**
- **依据**：NPC 实体名称，符合 `skeleton -> 骷髅`、`warrior -> 战士` 的既有术语。

### entry-00134
- **位置**：`mod-boot.lua:192`（section: `mod-boot/data/general/npcs/troll.lua`）
- **原文**：`Green-skinned and ugly, this massive humanoid glares at you, clenching wart-covered green fists.`
- **译文**：`这只绿皮丑陋的庞大人形生物正盯着你，同时它握紧了满是疣的绿色拳头。`
- **复核结论**：**未发现问题**
- **依据**：巨魔描述文本，结构与语义翻译准确无误。

### entry-00135
- **位置**：`mod-boot.lua:198`（section: `mod-boot/data/general/npcs/troll.lua`）
- **原文**：`A large and athletic troll with an extremely tough and warty hide.`
- **译文**：`一只高大且强壮的巨魔，皮肤异常坚韧且长满疣。`
- **复核结论**：**未发现问题**
- **依据**：`troll -> 巨魔`，表意忠实原句。

### entry-00136
- **位置**：`mod-boot.lua:208`（section: `mod-boot/data/talents.lua`）
- **原文**：`Flame`
- **译文**：`火焰`
- **复核结论**：**存在疑点**
- **依据**：
  - 术语快照 line 683 明确记录：`Flame 火球术 T.GAME.TALENT talents talent name existing core`。此处译文使用了“火焰”，存在直观分歧。
  - 查证固定源码 `game/engines/default/modules/boot/data/talents.lua:86`，该技能投射物为 bolt（火焰弹/火流，非范围火球），且全库现有翻译（包括 `engine.lua:1623`、`mod-boot.lua:208` 以及 `mod-tome.lua:28848` 法术技能 Flame）均一致译为“火焰”，而真正的火球技能（如 Fireflash）在游戏中译为“爆裂火球”。
  - 此疑点为术语库条目（`Flame -> 火球术`）与游戏内实际机制及通用译名（`火焰`）之间的记录冲突，需由维护者核准是否订正术语库或调整译名。

### entry-00137
- **位置**：`mod-boot.lua:233`（section: `mod-boot/dialogs/Addons.lua`）
- **原文**：`You can get new addons at #LIGHT_BLUE##{underline}#Te4.org Addons#{normal}#`
- **译文**：`在以下位置可以获得新的插件：#LIGHT_BLUE##{underline}#Te4.org 插件页面#{normal}#`
- **复核结论**：**未发现问题**
- **依据**：源码对应插件列表底部的超链接文本，富文本标记与样式完整闭合。

### entry-00138
- **位置**：`mod-boot.lua:259`（section: `mod-boot/dialogs/Credits.lua`）
- **原文**：`Expert Shaders Design`
- **译文**：`着色器设计专家`
- **复核结论**：**未发现问题**
- **依据**：制作人员名单职位头衔，翻译准确规范。

### entry-00139
- **位置**：`mod-boot.lua:282`（section: `mod-boot/dialogs/FirstRun.lua`）
- **原文**：
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
- **译文**：
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
- **复核结论**：**细微观察**
- **依据**：
  - 样式标签 `#{bold}##CRIMSON#...#{normal}#` 配对完整。
  - 术语层面：第 5 条列表项中两处使用了“捐助者”（“购买者/捐助者福利”、“公平发放捐助者奖励”），术语快照 line 679 记录“Donator 捐赠者 preferred core（不写作‘捐助者’）”。
  - 文本层面：第 2 条列表中将 `Characters vault` 意译为“角色备份”（通常与“物品仓库”并列为“角色金库/仓库”），后半句意译扩写；末句“关闭后，可以通过游戏设置菜单的在线选项卡打开”对应原文网络禁用选项的重置说明，意思表述通顺。

### entry-00140
- **位置**：`mod-boot.lua:322`（section: `mod-boot/dialogs/LoadGame.lua`）
- **原文**：
  ```text
  #{bold}##GOLD#%s: %s#WHITE##{normal}#
  Game version: %d.%d.%d
  Requires addons: %s

  %s
  ```
- **译文**：
  ```text
  #{bold}##GOLD#%s：%s#WHITE##{normal}#
  游戏版本：%d.%d.%d
  需要的插件：%s

  %s
  ```
- **复核结论**：**未发现问题**
- **依据**：源码对应 `LoadGame.lua:118` 格式化构建；7 个格式占位符（`%s`, `%s`, `%d`, `%d`, `%d`, `%s`, `%s`）类型、顺序与个数完全一致，标签与换行匹配。

### entry-00141
- **位置**：`mod-boot.lua:340`（section: `mod-boot/dialogs/LoadGame.lua`）
- **原文**：`#LIGHT_RED#WARNING: #LAST#Loading a savefile while in developer mode will permanently invalidate it. Proceed?`
- **译文**：`#LIGHT_RED#警告：#LAST#在开发者模式下读取一个存档将会不可逆地将其标记为作弊存档。确定吗？`
- **复核结论**：**未发现问题**
- **依据**：源码对应 `LoadGame.lua:198`；开发者作弊模式会永久给存档置 `save.cheat = true`，译文解释机制准确；颜色标记与标点匹配。

### entry-00142
- **位置**：`mod-boot.lua:346`（section: `mod-boot/dialogs/LoadGame.lua`）
- **原文**：`Downloading old game data: #LIGHT_GREEN#`
- **译文**：`正在下载旧版游戏数据：#LIGHT_GREEN#`
- **复核结论**：**未发现问题**
- **依据**：末尾颜色标记 `#LIGHT_GREEN#` 用于为后续拼接的模组名着色，格式完全保留。

### entry-00143
- **位置**：`mod-boot.lua:347`（section: `mod-boot/dialogs/LoadGame.lua`）
- **原文**：`Old game data for %s correctly installed. You can now play.`
- **译文**：`%s 的旧版游戏数据已经安装成功了。你可以现在游玩了。`
- **复核结论**：**未发现问题**
- **依据**：占位符 `%s` 正常保留，句意完整。

### entry-00144
- **位置**：`mod-boot.lua:364`（section: `mod-boot/dialogs/MainMenu.lua`）
- **原文**：
  ```text
  #{bold}##GOLD#Ashes of Urh'Rok - Expansion#LAST##{normal}#
  #{italic}##ANTIQUE_WHITE#Many in Maj'Eyal have heard of "demons", sadistic creatures who appear seemingly from nowhere, leaving a trail of suffering and destruction wherever they go.#{normal}##LAST#

  #{bold}#Features#{normal}#:
  #LIGHT_UMBER#New class:#WHITE# Doombringers. These avatars of demonic destruction charge into battle with massive two-handed weapons, cutting swaths of firey devastation through hordes of opponents. Armed with flame magic and demonic strength, they delight in fighting against overwhelming odds
  #LIGHT_UMBER#New class:#WHITE# Demonologists. Bearing a shield and the magic of the Spellblaze itself, these melee-fighting casters can grow demonic seeds from their fallen enemies. Imbue these seeds onto your items to gain a wide array of new talents and passive benefits, and summon the demons within them to fight!
  #LIGHT_UMBER#New race:#WHITE# Doomelves. Shalore who've taken to the demonic alterations especially well, corrupting their typical abilities into a darker form.
  #LIGHT_UMBER#New artifacts, lore, zones, events...#WHITE# For your demonic delight!


  ```
- **译文**：
  ```text
  #{bold}##GOLD#乌鲁洛克之烬 - 游戏扩展包#LAST##{normal}#
  #{italic}##ANTIQUE_WHITE#很多马基埃亚尔的居民都曾经听说过“恶魔”的名字，它们是一群似乎凭空出现的暴虐生物，无论走到哪里都会带来痛苦和毁灭。#{normal}##LAST#

  #{bold}#扩展包特性#{normal}#:
  #LIGHT_UMBER#新职业：#WHITE# 毁灭使者。他们是恶魔毁灭力量的化身，手拿双手武器加入战斗，将敌人化为一片火海。他们的手中掌握着火焰的魔法和恶魔的力量，在与势不可挡的敌人战斗中寻求欢愉。
  #LIGHT_UMBER#新职业：#WHITE# 恶魔使者。这些近战施法者手拿盾牌，掌握魔法大爆炸本身的力量，可以从倒下的敌人身上培育出恶魔种子。将这些恶魔种子附魔到你的物品里，可以获得各种全新的技能和被动的能力，并召唤种子里的恶魔来加入战斗！
  #LIGHT_UMBER#新种族：#WHITE# 魔化精灵。那些被恶魔的力量所改变的永恒精灵，他们的种族能力被腐化成了黑暗的形态。
  #LIGHT_UMBER#更多新神器、新手札、新地图、新事件……#WHITE# 体验恶魔的欢愉吧！


  ```
- **复核结论**：**存在疑点**
- **依据**：
  - 第 2 段正文中出现“很多马基埃亚尔的居民”，缺少间隔号 `·`。
  - 术语快照 line 692 明确规定：`Maj'Eyal 马基·埃亚尔 T.PN.WORLD places _t preferred core（维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代）`。此处“马基埃亚尔”使用了已被明确淘汰的旧译，存在专名规范不一致缺陷。（注：Ashes of Urh'Rok DLC 来源未固定）。

### entry-00145
- **位置**：`mod-boot.lua:385`（section: `mod-boot/dialogs/MainMenu.lua`）
- **原文**：
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
- **译文**：
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
- **复核结论**：**存在疑点**
- **依据**：
  1. 专名术语冲突：原文第 2 段与第 5 段两次出现 `"Scourge from the West"`，译文均译为“西方灾星”。术语快照 line 702 明确规定：`Scourge from the West 西方天灾 T.PN.PERSON society _t preferred dlc（Embers of Rage 中的个体；统一为“西方天灾”，不写作“灾星”）`。译文“西方灾星”违背 preferred 规范。
  2. 职业术语不一致：原文 `Psyshots` 在此译为“念力射手”。术语快照 line 699 规定为 `Psyshot 灵能射手`；且在 Embers of Rage DLC（`tome-orcs.lua`）全篇（如职业选择界面、解锁文本等）该职业均固定译为“灵能射手”。（注：Embers of Rage DLC 来源未固定）。

### entry-00146
- **位置**：`mod-boot.lua:408`（section: `mod-boot/dialogs/MainMenu.lua`）
- **原文**：
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
- **译文**：
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
- **复核结论**：**存在疑点**
- **依据**：
  1. 职业名称不一致：原文 `Writhing Ones` 译为“扭动者”。术语快照 line 714 记录为 `Writhing One 蜿蜒怪人`，而 Cults DLC 翻译（`tome-cults.lua:35`）中出生职业描述实际采用译名 `蠕动者`。此处“扭动者”与两者均不一致，出现三方分歧。
  2. 地图译名冲突：原文 `Scourge Pits` 译为“瘟疫之穴”，而 Cults DLC 对应地图（`tome-cults.lua:3870`）中固定译为“天灾之穴”（如“通向天灾之穴的路”），“瘟疫”与“天灾”产生冲突。
  3. 另注：原文 `Nethergames` 属原作者笔误（实为恐魔怪物 `Nethergate`），译文正确纠正并译为“彼世之门”，此项处理符合游戏机制事实。（注：Forgotten Cults DLC 来源未固定）。

### entry-00147
- **位置**：`mod-boot.lua:449`（section: `mod-boot/dialogs/MainMenu.lua`）
- **原文**：`Steam client not found.`
- **译文**：`找不到Steam客户端。`
- **复核结论**：**未发现问题**
- **依据**：源码对应主菜单无 Steam 运行环境时的弹窗，翻译准确。

### entry-00148
- **位置**：`mod-boot.lua:496`（section: `mod-boot/dialogs/ProfileLogin.lua`）
- **原文**：`Accept to receive #{bold}#very infrequent#{normal}# (a few per year) mails about important game events from us.`
- **译文**：`允许我们#{bold}#偶尔#{normal}#向你发送有关游戏重要新闻的邮件（每年最多只会有几封）。`
- **复核结论**：**未发现问题**
- **依据**：复选框标题文本；样式代码 `#{bold}#...#{normal}#` 及括号完整保留，语义精准。

### entry-00149
- **位置**：`mod-boot.lua:499`（section: `mod-boot/dialogs/ProfileLogin.lua`）
- **原文**：`Privacy Policy (opens in browser)`
- **译文**：`隐私政策（用浏览器打开）`
- **复核结论**：**未发现问题**
- **依据**：按钮文本，全角括号与文字准确对应。

### entry-00150
- **位置**：`mod-boot.lua:514`（section: `mod-boot/dialogs/ProfileSteamRegister.lua`）
- **原文**：
  ```text
  Welcome to #GOLD#Tales of Maj'Eyal#LAST#.
  To enjoy all the features the game has to offer it is #{bold}#highly#{normal}# recommended that you register your steam account.
  Luckily this is very easy to do: you only require a profile name and optionally an email (we send very few email, maybe two a year at most).

  ```
- **译文**：
  ```text
  欢迎来到#GOLD#马基·埃亚尔的传说#LAST#。
  为了享受游戏的全部功能，我们#{bold}#强烈#{normal}#推荐你注册你的Steam账户。
  幸运的是，这非常容易：你只需要提供你的用户名，也可以提供你的邮箱（我们基本上不会给你发送邮件，每年最多发送一两份）。

  ```
- **复核结论**：**未发现问题**
- **依据**：颜色代码 `#GOLD#...#LAST#`、富文本 `#{bold}#...#{normal}#` 及尾部换行完全保留；“马基·埃亚尔”遵循 preferred 规范。

### entry-00151
- **位置**：`mod-boot.lua:523`（section: `mod-boot/dialogs/ProfileSteamRegister.lua`）
- **原文**：`Accept to receive #{bold}#very infrequent#{normal}# (a few per year) mails about important game events from us.`
- **译文**：`允许我们#{bold}#偶尔#{normal}#向你发送有关游戏重要新闻的邮件（每年最多只会有几封）。`
- **复核结论**：**未发现问题**
- **依据**：与 entry-00148 内容完全一致，格式与样式代码完整。

### entry-00152
- **位置**：`mod-boot.lua:527`（section: `mod-boot/dialogs/ProfileSteamRegister.lua`）
- **原文**：`Privacy Policy (opens in browser)`
- **译文**：`隐私政策（用浏览器打开）`
- **复核结论**：**未发现问题**
- **依据**：与 entry-00149 内容完全一致，准确无误。

### entry-00153
- **位置**：`mod-boot.lua:534`（section: `mod-boot/dialogs/ProfileSteamRegister.lua`）
- **原文**：`Registering...`
- **译文**：`正在注册…`
- **复核结论**：**未发现问题**
- **依据**：等待弹窗标题，与 entry-00129 保持一致。

### entry-00154
- **位置**：`mod-boot.lua:536`（section: `mod-boot/dialogs/ProfileSteamRegister.lua`）
- **原文**：`Steam client not found.`
- **译文**：`找不到Steam客户端。`
- **复核结论**：**未发现问题**
- **依据**：与 entry-00147 内容一致，句式准确。

### entry-00155
- **位置**：`mod-boot.lua:538`（section: `mod-boot/dialogs/ProfileSteamRegister.lua`）
- **原文**：`Username or Email already taken, please select an other one.`
- **译文**：`用户名或邮件地址已被使用，请选择其他用户名或邮件地址。`
- **复核结论**：**未发现问题**
- **依据**：与 entry-00121 内容完全一致，句意与标点正确。

### entry-00156
- **位置**：`mod-boot.lua:554`（section: `mod-boot/dialogs/UpdateAll.lua`）
- **原文**：`There was an error while downloading:\n`
- **译文**：`下载时发生错误：\n`
- **复核结论**：**未发现问题**
- **依据**：与 entry-00122 一致，冒号与末尾换行符准确保留。

### entry-00157
- **位置**：`mod-boot.lua:583`（section: `mod-boot/init.lua`）
- **原文**：`Bootmenu!\n`
- **译文**：`启动菜单！\n`
- **复核结论**：**未发现问题**
- **依据**：与 entry-00123 一致，感叹号与末尾换行符保留。

### entry-00158
- **位置**：`mod-example.lua:19`（section: `mod-example/class/Game.lua`）
- **原文**：`Saving game...`
- **译文**：`保存游戏…`
- **复核结论**：**未发现问题**
- **依据**：源码对应固定 commit 下 `game/modules/example/class/Game.lua:437` 的日志输出 `self.log("Saving game...")`；省略号规范转化，语义准确。

### entry-00159
- **位置**：`mod-example.lua:30`（section: `mod-example/class/Player.lua`）
- **原文**：`LOW HEALTH!`
- **译文**：`生命值低！`
- **复核结论**：**未发现问题**
- **依据**：源码对应 `game/modules/example/class/Player.lua:113` 的玩家低生命飘字提示 `_t"LOW HEALTH!"`；感叹号与词义匹配。

### entry-00160
- **位置**：`mod-example.lua:49`（section: `mod-example/data/damage_types.lua`）
- **原文**：`Kill!`
- **译文**：`击杀！`
- **复核结论**：**未发现问题**
- **依据**：源码对应 `game/modules/example/data/damage_types.lua:32` 的致死攻击飘字提示；感叹号与动词词义匹配。

---

## 疑点与细微观察汇总表

| 条目编号 | 判定类别 | 主要核验事实与分歧说明 |
| :--- | :--- | :--- |
| **entry-00124** | 细微观察 | 句末“玩的开心！”助词建议优化为“玩得开心！”；无破坏性错误。 |
| **entry-00126** | 细微观察 | “这种情况不被支持的”略缺谓语“是”（宜为“这种情况是不被支持的”）；3 个 `%s` 及高亮代码完整。 |
| **entry-00128** | 细微观察 | donator 译为“赞助者/捐助”，术语快照 line 679 记录“Donator 统一为‘捐赠者’，不写作‘捐助者’”。 |
| **entry-00136** | **存在疑点** | 译文“火焰”与术语快照 line 683 `Flame -> 火球术` 分歧；但固定源码机制为单体 bolt，全库当前实现亦统称为“火焰”，属术语表记录与库内实现冲突。 |
| **entry-00139** | 细微观察 | donator 译为“捐助者”（术语表推荐“捐赠者”）；`Characters vault` 意译为“角色备份”。 |
| **entry-00144** | **存在疑点** | 第 2 段出现“马基埃亚尔”，漏掉间隔号 `·`，违背术语快照 line 692 的 preferred 规范 `马基·埃亚尔`（注：Ashes DLC 来源未固定）。 |
| **entry-00145** | **存在疑点** | 1. 两次出现“西方灾星”，违背术语快照 line 702 preferred 规范 `西方天灾`（“不写作‘灾星’”）；<br>2. 职业名“念力射手”违背术语快照 line 699 及 DLC 既有统一定名 `灵能射手`（注：Orcs DLC 来源未固定）。 |
| **entry-00146** | **存在疑点** | 1. 职业名“扭动者”与术语快照 line 714 `蜿蜒怪人` 及 DLC 译名 `蠕动者` 三方冲突；<br>2. 地图名“瘟疫之穴”与 DLC 对应地图名 `天灾之穴` 冲突（注：Cults DLC 来源未固定）。 |