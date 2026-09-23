# 修复窗口20：266批7条确认问题

Paseo MCP / schema5 translation_contextual_v2 implement；基线3e3ca17d8fb944389d02303df8e0748bf83717ec。用户2026-09-23授权持续推进审核与修复、提交与推送，无需逐批确认；有争议条目记pending待用户集中审阅。按审核/修复1:1节奏开窗。

唯一EXECUTOR仅修改mod-tome.lua中WORKSET的7个target及evidence/quality/repair-window-20-20260923/。不修改其他译文、术语库、规则、工具、旧证据；首次不修改handoff/catalog/migration；不stage/commit/push、不写.ai、不创建agent。保留既有无关未跟踪文件。

SOURCE-CLAIMS仅供实施，reviewer只读中性冻结输入和相关固定源码；不传宿主裁决。源码固定624a67329fe2ad440c5b344785a9c73fcf22ae63。source/source_tag/args_order/printf占位符/%%/markup保持基线；LF/TAB 必须与原文逐处一致。专名、技能名沿用本库现有译名（先在mod-tome.lua查证），不自行新造。

7条按契约选择full：REVIEW/full（codex/gpt-6-sol）与FINAL_REVIEW/full（claude/claude-opus-5-5）。max_cycles默认3；FINAL_REVIEW 中任何 ISSUE 都算失败，修复后必须先 RE_REVIEW 再 FINAL_REVIEW。每条按整句核对，不只改被点名处。LuaJIT全记录比较恰7个target变动；strict lint/claims、diff check、完整门禁/构建、DONE_VERIFIED。译文commit→queue→单次catalog/migration→证据发布commit→queue→push，然后继续审核267。

范围约束（每条都逐句对照原文，发现明显增删一并修正，不重写已忠实的句子）：
- 念力核心（Telekinetic Core）desc（general/objects/world-artifacts.lua:5016）：This heavy torque appears to draw nearby matter towards it. 保留“似乎”推测语气，不增“所有”；wielder 无被动牵引（仅主动 use_talent 念力牵引），写成“这副沉重的项圈似乎会把附近的物体吸向自己。”一类。
- 邪眼 desc（general/npcs/horror.lua:264）：bloodshot 为“布满血丝/充血”（本库同族 a bloodshot eye=充血的眼球），不是“带血的”。
- Utterly Destroyed 说明（talents/spells/death.lua:241–242，tformat）：creature 译“生物”（callbackOnKill/callbackOnSummonKill 对任何被杀生物触发），不要缩成“敌人”；the thrill of the death 为击杀/死亡带来的快感，不是“渴望死亡”；%0.1f、%d、50%% 顺序与第二行行首 \t\t 保持。
- 离线模式说明（dialogs/GameOptions.lua:664–680 起的长文本）：Version checks: Addons will not be checked for new versions. 为“版本检查：不再检查插件是否有新版本。”一类（上一条已说明仍可手动安装）；其余各行逐句对照，只修明显错漏；#{bold}#/#{normal}#/#CRIMSON# 等标记、所有换行与空行保持。
- 时空法术类别说明（talents/spells/spells.lua:32）：The school of time manipulation. 为名词短语“操控时间的法术学派。”一类；同族 Conveyance 等其他类别说明不在本窗口范围。
- 成就名 Savior of the damsels in distress（achievements/quests.lua:267，MELINDA_SAVED：从 Kryl-Feijan 墓穴的可怕命运中救出 Melinda）：damsel in distress 为“落难少女”，写成“落难少女拯救者”一类，不是“迷路”。
- 蛛毒魔棒未鉴定名 poison dripping wand（zones/ardhungol/objects.lua:43，BASE_ROD，巨型蜘蛛獠牙雕成）：wand 沿用本库“魔杖”（entity subtype wand=魔杖），写成“滴着毒液的魔杖”一类，不是“枝条”。

## f58a8172afcac3ee54724029a89988aa3975dcabb34eb6db66961bc00cbd89eb

section: mod-tome/data/general/objects/world-artifacts.lua
source_tag: _t

source: This heavy torque appears to draw nearby matter towards it.

target: 这副沉重的项圈将周围的所有物体拉向它。

确认依据：general/objects/world-artifacts.lua:5010 Telekinetic Core desc：This heavy torque appears to draw nearby matter towards it——“似乎”吸引附近物质；该物品被动并不牵引物体（仅 use_talent T_PSIONIC_PULL 主动使用），现译“将周围的所有物体拉向它”删去 appears 并增“所有”，把外观描述说成确定的机制。整条修复。
与 surface 同向：world-artifacts.lua:5002–5022 Telekinetic Core 的 wielder 无被动牵引，仅 use_talent T_PSIONIC_PULL 主动使用；现译删 appears 并增“所有”，把外观描述写成确定的被动效果。整条修复。

## f5928e33316fa455cae001b918290d8ac971a759be6ec5081c38c3baa9606184

section: mod-tome/data/general/npcs/horror.lua
source_tag: _t

source: A small bloodshot eye floats here.

target: 一只带血的小眼睛漂浮在这里。

确认依据：general/npcs/horror.lua:264 eldritch eye desc：bloodshot eye 为“充血/布满血丝的眼睛”（本库同族 a bloodshot eye=充血的眼球、Small and bloodshot=小而充血）；现译“带血的小眼睛”误作沾血。整条修复。
与 surface 同向：horror.lua:264 bloodshot 为“布满血丝/充血”，现译“带血的”误作沾血。整条修复。

## f5d4f8ef890c28cd90cd1022f602d757efedb53fc5422e446de4eef0e01c1571

section: mod-tome/data/talents/spells/death.lua
source_tag: tformat

source: Whenever a creature is killed by yourself or a minion you feast on its essence, gaining %0.1f mana.
		At level 3 the thrill of the death invigorates you, granting a movement speed bonus of 50%% for %d turns.

target: 每当你或你的随从杀死一个敌人，你吞噬它的精华，获得 %0.1f 法力值。
		技能等级 3 时，对死亡的渴望还会激励你，让你获得 50%% 移动速度加成，持续 %d 回合。

确认依据：talents/spells/death.lua:241–242：At level 3 the thrill of the death invigorates you（击杀触发 EFF_DEATH_RUSH）指杀戮/死亡带来的快感；现译“对死亡的渴望”意为渴求死亡，语义相反。整条修复，%0.1f/%d/50%% 与 \n\t\t 保持。
与 surface 同向，并补充：death.lua:229–234 callbackOnKill/callbackOnSummonKill 对任何被杀生物触发，原文为 creature，现译缩为“敌人”。整条修复：thrill of the death 译为击杀/死亡带来的快感，creature 译为“生物”。

## f5f90d5b06df70f3bbbc22c37c682688c33eb0b3f1d565300f278099f856bc8f

section: mod-tome/dialogs/GameOptions.lua
source_tag: _t

source: Disables all connectivity to the network.
This includes, but is not limited to:
- Player profiles: You will not be able to login, register
- Characters vault: You will not be able to upload any character to the online vault to show your glory
- Item's Vault: You will not be able to access the online item's vault, this includes both storing and retrieving items.
- Ingame chat: The ingame chat requires to connect to the server to talk to other players, this will not be possible.
- Purchaser / Donator benefits: The base game being free, the only way to give donators their bonuses fairly is to check their online profile. This will thus be disabled.
- Easy addons downloading & installation: You will not be able to see ingame the list of available addons, nor to one-click install them. You may still do so manually.
- Version checks: Addons will not be checked for new versions.
- Discord: If you use Discord Rich Presence integration this will also be disabled by this setting.
- Ingame game news: The main menu will stop showing you info about new updates to the game.

Note that this setting only affects the game itself. If you use the game launcher, whose sole purpose is to make sure the game is up to date, it will still do so.
If you do not want that, simply run the game directly: the #{bold}#only#{normal}# use of the launcher is to update the game.

#{bold}##CRIMSON#This is an extremely restrictive setting. It is recommended you only activate it if you have no other choice as it will remove many fun and acclaimed features.
A full exit and restart of the game is neccessary to apply this setting.#{normal}#

target: 禁止所有网络请求
包括但不仅限于：
- 用户信息：不能登录或者注册。
- 角色备份：不能在te4.org上保存你的角色信息（用来给其他人分享你的炫酷角色）。
- 物品仓库：不能访问你的在线物品仓库（包括存入和取回）。
- 游戏内聊天：游戏内聊天需要连接服务器才能与其他玩家交谈，这将无法使用。
- 购买者/捐赠者福利：基础游戏免费，公平发放捐赠者奖励的唯一途径是检查他们的在线档案，因此该功能将被禁用。
- 插件便捷下载与安装：你将无法在游戏内看到可用插件列表，也无法一键安装，但仍可手动安装。
- 插件版本更新：无法更新插件的版本。
- Discord：无法同步到Discord的实时状态。
- 游戏内新闻：主菜单将不再显示新闻。
注意这个设置只影响游戏本身。如果你使用游戏启动器，它的唯一目的就是确保游戏是最新的，因此它仍然会连接网络。
如果你不想这样，直接运行游戏即可。启动器#{bold}#只#{normal}#是用来更新游戏的。


#{bold}##CRIMSON#这是一个极端的选项。如果不是迫不得已，推荐你不要打开它，这会让你失去很多好用的功能和一些游戏体验。
应用这个选项必须退出重新进入游戏。#{normal}#

确认依据：dialogs/GameOptions.lua:672：Version checks: Addons will not be checked for new versions——只是不再检查插件新版本；现译“插件版本更新：无法更新插件的版本”误称插件不能更新（上一条明言仍可手动安装）。整条逐句核对后修复。
与 surface 同向：GameOptions.lua:672 Version checks 为不再检查插件新版本，现译“无法更新插件的版本”与上一条“仍可手动安装”矛盾。整条修复（其余各条 contextual 判一致）。

## f603e1fbc9c5fcc7b1df41a04254b66e5289160054dad1bc902356e2f04ee9e2

section: mod-tome/data/talents/spells/spells.lua
source_tag: _t

source: The school of time manipulation.

target: 学习操控时间。

确认依据：talents/spells/spells.lua:32 spell/temporal 类别说明 The school of time manipulation. 指操控时间的法术学派；现译“学习操控时间。”误作学习行为。整条修复（同族 Conveyance is the school of travel 现译“学习传送”属另一条，本批不扩）。
与 surface 同向：spells.lua:32 spell/temporal 类别说明是名词短语“操控时间的法术学派”，现译“学习操控时间。”误作动作。整条修复。

## f6060b573a570e17af892b2ecf917991b2c00828470098f1d3e08ab35791d76a

section: mod-tome/data/achievements/quests.lua
source_tag: achievement name

source: Savior of the damsels in distress

target: 迷路少女拯救者

确认依据：achievements/quests.lua:267 成就 Savior of the damsels in distress（MELINDA_SAVED：Saved Melinda from her terrible fate in the Crypt of Kryl-Feijan）；Melinda 是被邪教掳去献祭，不是迷路；damsel in distress 为“落难少女”，现译“迷路少女拯救者”误导。整条修复。
与 surface 同向：quests.lua:267–269 MELINDA_SAVED，damsels in distress 为“落难少女”，与迷路无关。整条修复。

## f62d40cfde7997845ae5616afa05939d61ee76acb37ad9d2549f140322df2bba

section: mod-tome/data/zones/ardhungol/objects.lua
source_tag: _t

source: poison dripping wand

target: 滴着毒液的枝条

确认依据：zones/ardhungol/objects.lua:43 Rod of Spydric Poison 未鉴定名 poison dripping wand；本库 wand 统一译“魔杖”（entity subtype wand=魔杖，榆木/白蜡/紫杉魔杖等），现译“枝条”不符物品类别。整条修复。
与 surface 同向：ardhungol/objects.lua:40–45 BASE_ROD，由巨型蜘蛛獠牙雕成；wand 本库统一“魔杖”（entity subtype wand=魔杖），现译“枝条”错。contextual 称冻结术语快照无 wand 条目，宿主以本库现行译名“魔杖”补足。整条修复。
