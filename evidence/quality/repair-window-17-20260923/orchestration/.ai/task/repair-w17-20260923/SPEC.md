# 修复窗口17：263批5条确认问题

Paseo MCP / schema5 translation_contextual_v2 implement；基线2a4b1c3d1aa9b835f2161c6d0ac1bd83b3834108。用户2026-09-23授权持续推进审核与修复、提交与推送，无需逐批确认；有争议条目记pending待用户集中审阅。按审核/修复1:1节奏开窗。

唯一EXECUTOR仅修改mod-tome.lua中WORKSET的5个target及evidence/quality/repair-window-17-20260923/。不修改其他译文、术语库、规则、工具、旧证据；首次不修改handoff/catalog/migration；不stage/commit/push、不写.ai、不创建agent。保留既有无关未跟踪文件。

SOURCE-CLAIMS仅供实施，reviewer只读中性冻结输入和相关固定源码；不传宿主裁决。源码固定624a67329fe2ad440c5b344785a9c73fcf22ae63。source/source_tag/args_order/printf占位符/markup保持基线；LF/TAB 必须与原文逐处一致（本窗口两条要删除多余换行）。专名、技能名沿用本库现有译名（先在mod-tome.lua查证），不自行新造。

5条按契约选择full：REVIEW/full（codex/gpt-6-sol）与FINAL_REVIEW/full（claude/claude-opus-5-5）。max_cycles默认3；FINAL_REVIEW 中任何 ISSUE 都算失败，修复后必须先 RE_REVIEW 再 FINAL_REVIEW。每条按整句核对，不只改被点名处。LuaJIT全记录比较恰5个target变动；strict lint/claims、diff check、完整门禁/构建、DONE_VERIFIED。译文commit→queue→单次catalog/migration→证据发布commit→queue→push，然后继续审核264。

范围约束（每条都逐句对照原文，发现明显增删一并修正，不重写已忠实的句子）：
- 猎头者挑战播报（class/GameState.lua:3669，say）：You claim the head of %s 为“取下了 %s 的首级”一类；giving pause to all foes on the level 指令关卡内敌人迟疑（实现为以你为目标的敌人全部 setTarget() 失去锁定，3671–3675），不得写成“被暂停/冻结”；#ORCHID# 与 %s 保持。
- Exploit Weakness 说明（talents/cunning/tactical.lua:171，tformat）：Each time you hit an opponent with a melee attack 必须写出“近战攻击命中”（Combat.lua:975 仅近战流程触发）；其余逐句对照；原文结尾的 \n\t\t 恢复。
- 单项效果抵抗提示（class/interface/TooltipsData.lua:438）：标题 Effect resistance chance 为“效果抵抗几率”一类，正文为“表示你完全抵抗该特定效果的几率”；不得与上一条 Status resistance（状态免疫）混同或泛化为全部状态异常；#GOLD#…#LAST# 与末尾换行保持。
- 教程完成文本（texts/tutorial/done.lua:20–31）：删除译文在“不\n会”“(你也可以\n根据”“还存\n在”处插入的硬换行，使 LF 数与段落位置和原文完全一致（原文 11 个 LF）；其余逐句对照。
- 思维形态说明（talents/psionic/thought-forms.lua:507–510，tformat）：LF 与 \t\t 行首缩进与原文完全一致（原文 3 个 LF：三句分别在第一行、等级列表整句为第二行、范围句第三行、最后一句第四行，不得把等级列表拆成三行）；warrior/defender 沿用本库“战士/盾战士”（Thought-Form: Warrior=思维形态：战士），不得写“狂战士”；mighty/powerful/strong 不得改写成“大师/精英”；距离单位沿用本库“码”。

## f277b46e7f315b0f0cf6cc0c8429e7772f11050d0405de4a84f197e681b0cba2

section: mod-tome/class/GameState.lua
source_tag: say

source: #ORCHID#You claim the head of %s, giving pause to all foes on the level.

target: #ORCHID#你杀死了 %s，楼层上所有的敌人都被暂停了。

确认依据：class/GameState.lua:3669–3675 猎头者挑战：击杀目标后 bignews 播报，随后遍历关卡实体，凡以玩家为 ai_target 的敌人 setTarget() 清除目标（“other enemies pause, untarget player”）；giving pause 意为令敌人迟疑、失去对你的锁定，现译“楼层上所有的敌人都被暂停了”误述为暂停/冻结；claim the head of 译“杀死了”丢失“取下首级”。整条修复。

## f2b2afecaf9b406b4e16fe70ea531f9eff43b3afe927d07705718d424ee5aeb8

section: mod-tome/data/talents/cunning/tactical.lua
source_tag: tformat

source: Systematically find the weaknesses in your opponents' physical resists, at the cost of 10%% of your physical damage.  Each time you hit an opponent with a melee attack, you reduce their physical resistance by 5%%, up to a maximum of %d%%.
		

target: 感知对手的物理弱点，代价是你减少 10%% 物理伤害。每次你击中对手时，你会减少它们 5%% 物理伤害抗性，最多减少 %d%%。

确认依据：talents/cunning/tactical.lua:171 Exploit Weakness：Combat.lua:975 仅在近战攻击命中（attackTargetWith 的 hitted 分支）时调用 do_weakness；现译“每次你击中对手时”删去 with a melee attack 限定，远程/法术命中也读作会触发（删限定词缺陷类）。另原文结尾 
		 未保留。整条修复。
与 surface 同向：Combat.lua:975 Exploit Weakness 只在近战攻击命中流程中触发，现译删去 with a melee attack 限定。整条修复（含结尾 \n\t\t）。

## f2d8717e52063cdc50c2878f0b77090b02de36be04eb819137e4c12fc1d0ae42

section: mod-tome/class/interface/TooltipsData.lua
source_tag: _t

source: #GOLD#Effect resistance chance#LAST#
This represents your chance to completely resist this specific effect.


target: #GOLD#状态异常免疫几率#LAST#
表示你完全免疫状态异常的几率。


确认依据：class/interface/TooltipsData.lua:438 TOOLTIP_SPECIFIC_IMMUNE，CharacterSheet.lua:1298/1307 作为各单项免疫（无专属提示时）的回退提示；原文“完全抵抗这一特定效果的几率”，现译标题“状态异常免疫几率”与正文“完全免疫状态异常的几率”泛化为全部状态异常，且与上一条 Status resistance（状态免疫）混同。整条修复。
与 surface 同向：TOOLTIP_SPECIFIC_IMMUNE 为单项免疫行的回退提示（CharacterSheet.lua:1298/1307），应为“完全抵抗该特定效果的几率”，标题勿与 Status resistance 混同。

## f30327e69ff63cfcd23683b56cd58db5f07ea2989ca040b3bc04d4e017d8dcdb

section: mod-tome/data/texts/tutorial/done.lua
source_tag: _t

source: #GOLD#Congratulations !#WHITE#

You have completed this small tutorial, and should now know the basics of ToME4. You are ready to step forward into the world to find glory, treasures and be mercilessly slaughtered by hordes of creatures you thought you could handle!
During this tutorial some creatures were adjusted to the need of the teachings, beware, in the real world trolls are not usually this nice!

If you need a reminder of which key does what, you can access the game menu by pressing #GOLD#Escape#WHITE# and checking the key binds (you can also adjust them to your needs).

As this is probably your first time with the game you will find there is a limited number of races and classes available to play, many many more do exist but you will unlock them while playing.

Now go boldly and remember: #GOLD#Have fun!#WHITE#
Press Escape, save & exit and create a new character!


target: #GOLD#恭喜你！#WHITE#

你完成了这个简单教程，应该已经了解 ToME4 的基础。现在你已准备好踏入这个世界，寻找荣耀与财富，并被一群你自以为能对付的怪物无情屠杀！
在教程中，一些生物为了配合教学进行了调整；记住，在真实世界里，巨魔通常不
会这么友善！

如果你想知道快捷键的功能，你可以按 #GOLD#Esc#WHITE#键进入游戏菜单检查按键设定(你也可以
根据你的需要改变设置)。

也许这是你第一次玩这个游戏，你会发现可供游玩的种族和职业数量有限；游戏中还存
在许多其他种族和职业，你会在游戏过程中解锁它们。

现在，勇敢前进并记住：#GOLD#好好享受游戏的乐趣！#WHITE#
请按下 Esc 键，保存并退出游戏，建立一个新的角色吧！


确认依据：texts/tutorial/done.lua:20–31 教程完成文本：原文 11 个 LF，现译 14 个，在“不
会”“(你也可以
根据”“还存
在”处插入硬换行拆开词语（一级换行不变量）。整条修复，LF 与原文一致。
与 surface 同向：done.lua:20–31 无对应断行，现译在词中插入 3 处硬换行，违反换行不变量。

## f33c065ae56bb68f1a4146a8e6b75e23e7d1dab1bf0f7432472bc6f036e083a5

section: mod-tome/data/talents/psionic/thought-forms.lua
source_tag: tformat

source: Forge a guardian from your thoughts alone.  Your guardian's primary stat will be improved by %d, its two secondary stats by %d, and it will have Magic, Cunning, and Willpower equal to your own.
		At talent level one, you may forge a mighty bowman clad in leather armor; at level three a powerful warrior wielding a two-handed weapon; and at level five a strong defender using a sword and shield.
		Thought forms can only be maintained up to a range of %d, and will rematerialize next to you if this range is exceeded.
		Only one thought-form may be active at a time, and the stat bonuses will improve with your Mindpower.

target: 你从脑海里召唤出一位强大的守护者。
		你的守护者主属性会增加 %d，他的两项副属性会增加 %d，同时他的魔力、灵巧和意志属性等同于你的属性值。
		在等级 1 时，你会召唤出身着皮甲的弓箭手大师；
		在等级 3 时，你会召唤出手持双手武器的精英狂战士；
		在等级 5 时，你会召唤出手持剑盾的精英盾战士。
		精神体只能存在于 %d 码范围内，若超出此范围，则精神体会回到你身边。
		同一时间只能维持一种思维形态。
		属性增益受精神强度加成。

确认依据：talents/psionic/thought-forms.lua:507–510 Thought-Forms 说明：原文 3 个 LF，现译 7 个（首句后与三级列表处额外换行，一级换行不变量）；warrior 译“精英狂战士”与本库技能名 Thought-Form: Warrior=思维形态：战士、thought-forged warrior=精神体战士（27997–27998）不一致，且 mighty/powerful/strong 被改写为“大师/精英”。距离单位“码”为本库多数用法（%d 码 152 处），不是缺陷。整条修复，LF 与原文一致。
