# 冻结40条译文：统一复核规则 v3-source（临时文件与混合来源）

你是只读 REVIEWER。仅审本包 entry-03333–entry-03372 共40条。中文自然语言输出，不强制JSON。用户已明确允许临时文件：可在仓库外使用自己创建的任务专属临时目录（例如 mkdtemp(prefix="abc20-g05-20260923-")），保存/删除中间文件并报告路径；不得读取他人临时材料。仓库、冻结输入及译文保持只读，不创建子agent，不修复译文，不读取其他模型输出。以下任务约束对所有实验臂相同。

## 判断依据与范围

1. 原文/译文及身份以本包和 entries.json 为准；邻近译文仅来自同目录 context.lua。术语只用本包末尾子集；按 source_tag/category/语境匹配，existing 不是强制改名依据。不得读取当前翻译文件、其他实验文件、SPEC/STATE、历史报告或生产结论。
2. 游戏机制以可核验的实际源码行为为准。本体固定commit 624a67329fe2ad440c5b344785a9c73fcf22ae63；DLC使用source-access列明且哈希固定的公开快照，源码仓库/commit未固定，必须显式标注。DLC机制疑点可陈述快照内已证事实，但目标版本适用性缺口保留待确认，不将引擎commit套用DLC。缺源码的组件仅确认文本或格式直接可证的问题，机制依赖疑点待确认。英文、术语或旧译不能覆盖源码；沿袭上游的误述和翻译新增分开，不仅凭变量名猜机制。
3. 可读本INPUT、entries.json、context.lua、source-access.json及其中sections列明的本组sources文件。可在这些单文件内搜索。源码缺失已明确列在unavailable_components，不把其他组件同名代码当作它的证据。
4. 追调用链时，本体只能git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<明确相关的单文件path>；DLC只能读取source-access中dlc_additional_sources列明、哈希匹配的相关单文件。每个新增文件说明哪个已读调用/符号/require引入。禁止当前源码工作树、其他commit、整目录git grep/rg/find或历史审核查找；不能读取共享DLC快照中的locales等其他语言答案。证据不足写待确认。
5. 不把问题扩大为全局重命名或术语策略。格式结合实际显示/参数消费判断：保留source_tag、args_order、special；占位符、标记及段落/换行差异只有导致错误参数、错误显示或信息结构丢失时才算缺陷。合法排版和等价重排不算缺陷。

## 四类判定（按以下顺序合并一条内的多个claim）

- **存在问题**：至少一个有可核验证据的错误或遗漏，涉及事实、作用对象/所属关系、数量/条件/范围/时序、玩家操作、语义信息、明确适用的术语要求或运行时格式。轻微并不自动变为建议；必须解释具体哪项信息错误或丢失，不因可自行猜出原意便忽略。
- **待确认**：没有已证实问题，但有具体疑点因证据不足无法定论。指出缺哪项证据。不得把待确认当未发现问题。
- **仅建议**：没有上述问题或未决疑点，仅更自然的措辞、个人偏好、无损排版等；不得将建议计作缺陷。
- **未发现问题**：无上述三类事项。

一条同时有已证实问题和待确认claim，总判定为存在问题，但须分别列出各claim状态。若只有建议和未决claim，总判定为待确认。不同条目重复同一问题仍分别覆盖；同条重复表述不重复计claim。

## 输出

先给恰好40行的表格，列为“完整entry-ID | 四类判定 | claim编号或简短依据”。按冻结顺序，无漏项，不用“其余通过”。随后按claim编号列出原文/译文必要短引、问题具体内容、状态、源码路径:行号/函数及消费逻辑（纯语义判断可给明确语境证据）。对建议简述其为何仅属偏好；无需大段重抄整个输入。不要给修改方案。每个问题、建议或待确认观察使用单独标题：### C01 | entry-03333 | 存在问题（ID递增，替换为实际条目和状态）；不同缺陷尽量分开，方便后续无损归并。

最后列实际读取的所有路径与版本、额外源码路径的调用链来源、是否有无法核验或越界；如发生越界如实报告。禁止查找模型比较结果或给自己打分。你输出的是审核观察，不是真值，不宣称DONE_VERIFIED。


## entry-03333
位置：tome-addon-dev.lua:122；section：tome-addon-dev/superload/mod/dialogs/debug/AddonDeveloper.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Addon MD5: #LIGHT_BLUE#%s#LAST# (this was copied to your clipboard).
However you should'nt need that anymore, you can upload your addon directly from here.
```
译文：
```text
插件 MD5: #LIGHT_BLUE#%s#LAST#（已复制到剪贴板）。
不过你应该不需要它了，你可以直接在这里上传。
```

## entry-03334
位置：tome-addon-dev.lua:186；section：tome-addon-dev/superload/mod/dialogs/debug/ExampleAddonMaker.lua；source_tag：tformat；args_order：None；special：None

原文：
```text

ToME4 is about to relaunch and change locale to %s, proceed?
```
译文：
```text

ToME4 即将重启并切换语言到 %s，确定？
```

## entry-03335
位置：tome-addon-dev.lua:198；section：tome-addon-dev/superload/mod/dialogs/debug/ReleaseTranslation.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Choose the addon you want to copy translation file to.
```
译文：
```text
选择你想要将翻译文件拷贝去的插件。
```

## entry-03336
位置：tome-ashes-urhrok.lua:7；section：tome-ashes-urhrok/data/achievements/all.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Activated all 23 different kinds of demon statues.
```
译文：
```text
启动全部23个不同的恶魔雕像。
```

## entry-03337
位置：tome-ashes-urhrok.lua:17；section：tome-ashes-urhrok/data/achievements/all.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Kill all the three demons that are on Eyal since before the Spellblaze: Shasshhiy'Kaish, Kryl'Feijan and Walrog.
```
译文：
```text
杀死三个在魔法大爆炸前就来到埃亚尔的古老恶魔：莎西·凯希、克里尔·费扬和乌尔罗格。
```

## entry-03338
位置：tome-ashes-urhrok.lua:20；section：tome-ashes-urhrok/data/achievements/all.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_GREEN#Kryl-Feijan#LAST#
```
译文：
```text
#LIGHT_GREEN#克里尔·费扬#LAST#
```

## entry-03339
位置：tome-ashes-urhrok.lua:21；section：tome-ashes-urhrok/data/achievements/all.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Kryl-Feijan
```
译文：
```text
克里尔·费扬
```

## entry-03340
位置：tome-ashes-urhrok.lua:34；section：tome-ashes-urhrok/data/birth/corrupted.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * +4 Strength, +0 Dexterity, +2 Constitution
```
译文：
```text
#LIGHT_BLUE# * +4 力量，+0 敏捷，+2 体质
```

## entry-03341
位置：tome-ashes-urhrok.lua:35；section：tome-ashes-urhrok/data/birth/corrupted.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * +2 Magic, +0 Willpower, +1 Cunning
```
译文：
```text
#LIGHT_BLUE# * +2 魔法，+0 意志，+1 灵巧
```

## entry-03342
位置：tome-ashes-urhrok.lua:36；section：tome-ashes-urhrok/data/birth/corrupted.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Life per level:#LIGHT_BLUE# +3
```
译文：
```text
#GOLD#每等级生命加值：#LIGHT_BLUE# +3
```

## entry-03343
位置：tome-ashes-urhrok.lua:42；section：tome-ashes-urhrok/data/birth/corrupted.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * +3 Strength, +0 Dexterity, +2 Constitution
```
译文：
```text
#LIGHT_BLUE# * +3 力量，+0 敏捷，+2 体质
```

## entry-03344
位置：tome-ashes-urhrok.lua:44；section：tome-ashes-urhrok/data/birth/corrupted.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Life per level:#LIGHT_BLUE# +2
```
译文：
```text
#GOLD#每等级生命加值：#LIGHT_BLUE# +2
```

## entry-03345
位置：tome-ashes-urhrok.lua:50；section：tome-ashes-urhrok/data/birth/doomelf.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The demons of Mal'Rok would never bless you!
Three could tell them of the horrors elves wrought.
One rages and torments in deep oceans blue,
one fights for the third with the cultists she taught.
Silence these beings, maintain your deception,
and then you may witness a new elf's conception...
```
译文：
```text
玛·洛克的恶魔绝不会对你施以祝福！
三者可以诉说精灵所带来的恐怖
之一在无尽的深海中永远咆哮
之一召集邪徒为复活另一者而战
静默他们的声音，隐藏你的踪影
新的精灵终将诞生…
```

## entry-03346
位置：tome-ashes-urhrok.lua:65；section：tome-ashes-urhrok/data/birth/doomelf.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * -2 Strength, +1 Dexterity, +1 Constitution
```
译文：
```text
#LIGHT_BLUE# * -2 力量，+1 敏捷，+1 体质
```

## entry-03347
位置：tome-ashes-urhrok.lua:66；section：tome-ashes-urhrok/data/birth/doomelf.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#LIGHT_BLUE# * +3 Magic, +2 Willpower, +0 Cunning
```
译文：
```text
#LIGHT_BLUE# * +3 魔法，+2 意志，+0 灵巧
```

## entry-03348
位置：tome-ashes-urhrok.lua:67；section：tome-ashes-urhrok/data/birth/doomelf.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Life per level:#LIGHT_BLUE# 9
```
译文：
```text
#GOLD#每等级生命加值：#LIGHT_BLUE# 9
```

## entry-03349
位置：tome-ashes-urhrok.lua:68；section：tome-ashes-urhrok/data/birth/doomelf.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#GOLD#Experience penalty:#LIGHT_BLUE# 12%
```
译文：
```text
#GOLD#经验惩罚：#LIGHT_BLUE# 12%
```

## entry-03350
位置：tome-ashes-urhrok.lua:119；section：tome-ashes-urhrok/data/general/grids/demon_statues.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Kryl-Feijan
```
译文：
```text
克里尔·费扬
```

## entry-03351
位置：tome-ashes-urhrok.lua:167；section：tome-ashes-urhrok/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Your Obliterating Smash can destroy walls.
```
译文：
```text
你的歼灭挥斩能摧毁墙壁。
```

## entry-03352
位置：tome-ashes-urhrok.lua:171；section：tome-ashes-urhrok/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
All enemies in radius 2 take 20 fire damage each turn and healing you for 10% of the damage dealt.
```
译文：
```text
附近2码范围的敌人每回合受到20火焰伤害。你受到10%伤害值的治疗。
```

## entry-03353
位置：tome-ashes-urhrok.lua:187；section：tome-ashes-urhrok/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Status resistances shift over time to match the statuses you are being hit by.
```
译文：
```text
依据你中的负面状态改变你的状态免疫。
```

## entry-03354
位置：tome-ashes-urhrok.lua:200；section：tome-ashes-urhrok/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Can be unequipped, can't be rerolled.
```
译文：
```text
能解除装备，不能重置。
```

## entry-03355
位置：tome-ashes-urhrok.lua:201；section：tome-ashes-urhrok/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Can be unequipped or rerolled.
```
译文：
```text
能解除装备或重置。
```

## entry-03356
位置：tome-ashes-urhrok.lua:214；section：tome-ashes-urhrok/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Increases all saves by your Shadow Power.
```
译文：
```text
每点“阴影强度”增加1点全豁免。
```

## entry-03357
位置：tome-ashes-urhrok.lua:218；section：tome-ashes-urhrok/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Grants spellpower equal to your Shadow Power.
```
译文：
```text
每点“阴影强度”增加1点法术强度。
```

## entry-03358
位置：tome-ashes-urhrok.lua:222；section：tome-ashes-urhrok/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Increases all damage penetration by 1% for each point of your Shadow Power.
```
译文：
```text
每点“阴影强度”增加1%抗性穿透。
```

## entry-03359
位置：tome-ashes-urhrok.lua:226；section：tome-ashes-urhrok/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Grants 2.5% movement speed for each point of Shadow Power.
```
译文：
```text
每点“阴影强度”增加2.5%移动速度。
```

## entry-03360
位置：tome-ashes-urhrok.lua:230；section：tome-ashes-urhrok/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Grants spell-crit equal to half of your Shadow Power.
```
译文：
```text
每点“阴影强度”增加0.5%法术暴击率。
```

## entry-03361
位置：tome-ashes-urhrok.lua:233；section：tome-ashes-urhrok/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
"Wreckage all about you. Is there anything left inside?"
```
译文：
```text
己身若残，何物能存？
```

## entry-03362
位置：tome-ashes-urhrok.lua:234；section：tome-ashes-urhrok/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Grants physical power equal to your Shadow Power.
```
译文：
```text
每点“阴影强度”增加1点物理强度。
```

## entry-03363
位置：tome-ashes-urhrok.lua:238；section：tome-ashes-urhrok/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Increases all damage by 1% for each point of your Shadow Power.
```
译文：
```text
每点“阴影强度”增加1%全体伤害加成。
```

## entry-03364
位置：tome-ashes-urhrok.lua:242；section：tome-ashes-urhrok/data/general/objects/world-artifacts.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Increases all resists by 0.4% for each point of your Shadow Power.
```
译文：
```text
每点“阴影强度”增加0.4%全体抗性。
```

## entry-03365
位置：tome-ashes-urhrok.lua:261；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
(You see here a pile of strange tablets, all piled up in a nice, orderly stack.  You remove the top one, and study it; your finger slips across a square in one corner, and strange sentences start playing through your mind. You struggle to make sense of the unfamiliar words and concepts in your thoughts.)

Many #{italic}##FIREBRICK#[moon-craters]#{normal}##LAST# after he #{italic}##FIREBRICK#[planted]#{normal}##LAST# us and #{italic}##FIREBRICK#[retired]#{normal}##LAST#, the #{italic}##FIREBRICK#[Father]#{normal}##LAST# awoke from his #{italic}##FIREBRICK#[cocoon]#{normal}##LAST# to see us #{italic}##FIREBRICK#[rattling]#{normal}##LAST#. He was shocked at our #{italic}##FIREBRICK#[wilted]#{normal}##LAST# state, asking us why we #{italic}##FIREBRICK#[rattled]#{normal}##LAST#; we told him about the #{italic}##FIREBRICK#[shaking]#{normal}##LAST# we had to suffer through, the way the planet was #{italic}##FIREBRICK#[jammed up]#{normal}##LAST# and how although our #{italic}##FIREBRICK#[peas in a pod]#{normal}##LAST# had #{italic}##FIREBRICK#[plugged the leaks]#{normal}##LAST# to keep the #{italic}##FIREBRICK#[beads]#{normal}##LAST# from #{italic}##FIREBRICK#[falling out]#{normal}##LAST#, the #{italic}##FIREBRICK#[brooms]#{normal}##LAST# kept sweeping our #{italic}##FIREBRICK#[dust bunnies]#{normal}##LAST# away, and there wasn't enough empty room to keep the #{italic}##FIREBRICK#[beads]#{normal}##LAST# from #{italic}##FIREBRICK#[cracking]#{normal}##LAST#.

(There is a larger square on the tablet here; you press your hand to it, and suddenly you see a desert planet, ravaged by constant dust-storms. You feel the futility of a short, greenish thing as he looks on his ruined crops; you feel the wrath of a red-skinned humanoid as he rushes at a large horde of small, onyx creatures, a sword in one hand and a fireball in the other. The images disappear as you remove your hand.)

#{italic}##FIREBRICK#[Father]#{normal}##LAST# gave us his #{italic}##FIREBRICK#[tools]#{normal}##LAST#, and after we #{italic}##FIREBRICK#[tripped the janitors?]#{normal}##LAST# he had us #{italic}##FIREBRICK#[shake gently?]#{normal}##LAST#, but instead of #{italic}##FIREBRICK#[rattling]#{normal}##LAST# we were #{italic}##FIREBRICK#[making music]#{normal}##LAST#, only #{italic}##FIREBRICK#[cracking]#{normal}##LAST# the #{italic}##FIREBRICK#[beads]#{normal}##LAST# that made us #{italic}##FIREBRICK#[out of tune]#{normal}##LAST#; our #{italic}##FIREBRICK#[beads]#{normal}##LAST# grew stronger, learned how to use #{italic}##FIREBRICK#[tools]#{normal}##LAST# of different #{italic}##FIREBRICK#[colors]#{normal}##LAST# than what the #{italic}##FIREBRICK#[Father]#{normal}##LAST# gave us. The #{italic}##FIREBRICK#[Father]#{normal}##LAST# loved to #{italic}##FIREBRICK#[hear our music]#{normal}##LAST#, and we were grateful he was there to #{italic}##FIREBRICK#[compose]#{normal}##LAST# for us when we needed; soon we were #{italic}##FIREBRICK#[writing our own music]#{normal}##LAST# and didn't need to #{italic}##FIREBRICK#[rattle]#{normal}##LAST# anymore, and the #{italic}##FIREBRICK#[Father]#{normal}##LAST# #{italic}##FIREBRICK#[retired]#{normal}##LAST#.

(Another larger square. You see a wonderful, loving #{italic}##FIREBRICK#[Father]#{normal}##LAST# descending on the planet, desert turning to lush forest with his touch; you worship him with your green and onyx and ruby brethren, all different shapes and sizes, united for the first time in appreciating all the good he's done for you. For the first time in ages, you know where your next meal is coming from, and you need not fear others killing you for your farmland, nor the dust storms. He holds the corpses of some reclusive earth-mages in his hand, the source of the storms; you would be angry at them, but you can only feel happiness for the future to come. You and your brethren start competing in an organized fashion, occasionally in fights again, but even when you die you know it's for the good of the planet; an age later, you and your brethren are smarter, stronger, and far happier than before, living in paradise. You remove your hand an instant later, and the feelings of worship and admiration drain from you.)

Eventually, the #{italic}##FIREBRICK#[egg-weeds]#{normal}##LAST# came. We tried to #{italic}##FIREBRICK#[crack their beads]#{normal}##LAST# but nothing happened; they did not try to #{italic}##FIREBRICK#[crack]#{normal}##LAST# us but instead promised us even more wonderful #{italic}##FIREBRICK#[sheet music]#{normal}##LAST# than what our #{italic}##FIREBRICK#[Father]#{normal}##LAST# had given us, under the condition that we let them #{italic}##FIREBRICK#[shatter]#{normal}##LAST# him. We refused, but we reached a #{italic}##FIREBRICK#[nasty pod]#{normal}##LAST# together; we'd #{italic}##FIREBRICK#[mute? pot?]#{normal}##LAST# the #{italic}##FIREBRICK#[Father]#{normal}##LAST# with the #{italic}##FIREBRICK#[tools]#{normal}##LAST# he gave us, leaving him a #{italic}##FIREBRICK#[lazy carpenter]#{normal}##LAST# and proving our #{italic}##FIREBRICK#[pod was shut]#{normal}##LAST# with the #{italic}##FIREBRICK#[egg-weeds]#{normal}##LAST#. The #{italic}##FIREBRICK#[Father]#{normal}##LAST# wouldn't be #{italic}##FIREBRICK#[rattled or cracked]#{normal}##LAST# by this; he wouldn't even know. The #{italic}##FIREBRICK#[egg-weeds]#{normal}##LAST# were pleased, and #{italic}##FIREBRICK#[smeared]#{normal}##LAST# their #{italic}##FIREBRICK#[eggsuckers]#{normal}##LAST# on our planet, letting us trade with #{italic}##FIREBRICK#[pods from other plants]#{normal}##LAST# from all other kinds of #{italic}##FIREBRICK#[gardens]#{normal}##LAST#. We tasted new food, learned new #{italic}##FIREBRICK#[tools]#{normal}##LAST#, and some #{italic}##FIREBRICK#[fancy]#{normal}##LAST# types of new #{italic}##FIREBRICK#[beads]#{normal}##LAST# came to our #{italic}##FIREBRICK#[garden]#{normal}##LAST#. We felt a little #{italic}##FIREBRICK#[noise]#{normal}##LAST# about our #{italic}##FIREBRICK#[Father]#{normal}##LAST#, but he was not #{italic}##FIREBRICK#[noisy]#{normal}##LAST# and wouldn't #{italic}##FIREBRICK#[hear]#{normal}##LAST# any #{italic}##FIREBRICK#[sounds]#{normal}##LAST#. The #{italic}##FIREBRICK#[egg-weeds]#{normal}##LAST# acted as our #{italic}##FIREBRICK#[pod peas]#{normal}##LAST#, and we treated them with great #{italic}##FIREBRICK#[listening]#{normal}##LAST#, even as they #{italic}##FIREBRICK#[slipped from the pod]#{normal}##LAST# and we could no longer #{italic}##FIREBRICK#[attend each other's concerts]#{normal}##LAST#.

(You touch the panel on the next page. A creature appears before you, stepping out of a massive fortress - it has an egg-shaped body, and limbs like four #{italic}##FIREBRICK#[tendril-weeds]#{normal}##LAST#. You hate this thing with all your being, although you know you did not at the time. They say they want the #{italic}##FIREBRICK#[Father]#{normal}##LAST# dead, and can offer you great magic and technology in return; you loathe to consider the idea, but their fortresses and weapons make you wonder if their offer is truly optional. You consider waking #{italic}##FIREBRICK#[Father]#{normal}##LAST# to ask him for help, but worry that even he could not stand up to the #{italic}##FIREBRICK#[egg-weeds]#{normal}##LAST#; ultimately you decided to seal him in his sleep, leaving him harmless but unharmed, unconscious until further intervention. The #{italic}##FIREBRICK#[egg-weeds]#{normal}##LAST# begrudgingly accept this resolution, and keep up their end of the bargain. They give you strange, powerful artifacts, and build portals on your world that let you pass through to strange worlds, more incredible and beautiful than you could possibly imagine, and filled with other races who've been given these gifts and seek to trade. You taste new foods, learn new magic, hear new music, and discover more beauty than you have in your entire history. If not for the pangs of guilt, life could not be better. Only when you remove your hand and the images start clearing from your mind do you recognize the "egg-weeds" as the Sher'Tul.)

Then, there was great #{italic}##FIREBRICK#[noise]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It got #{italic}##FIREBRICK#[louder]#{normal}##LAST#. It was #{italic}##FIREBRICK#[eardrum-bursting]#{normal}##LAST#.

(There is another panel. You dare not touch it, but as you reach to put it away, a finger briefly brushes across it. Starvation, burning, suffocation, misery, fury, and sheer agony rage across your mind for what you know to be a tenth of a second, but feels like half a minute. Your ears are still ringing as you move on to the next square.)

The #{italic}##FIREBRICK#[eggsuckers]#{normal}##LAST# were a trap, a #{italic}##FIREBRICK#[discord]#{normal}##LAST# planted by the #{italic}##FIREBRICK#[egg-weeds]#{normal}##LAST# to #{italic}##FIREBRICK#[crack]#{normal}##LAST# us all, and only cause #{italic}##FIREBRICK#[hairline fracture]#{normal}##LAST# to their own #{italic}##FIREBRICK#[garden]#{normal}##LAST#. Their #{italic}##FIREBRICK#[wrong note]#{normal}##LAST# turned our planet to #{italic}##FIREBRICK#[cacophony]#{normal}##LAST#, and nearly all of us #{italic}##FIREBRICK#[fell out of the pod]#{normal}##LAST#. The #{italic}##FIREBRICK#[apple was peeled]#{normal}##LAST# and a fragment of our #{italic}##FIREBRICK#[shell]#{normal}##LAST# floated in the #{italic}##FIREBRICK#[ocean]#{normal}##LAST#. Our #{italic}##FIREBRICK#[handymen]#{normal}##LAST# acted quickly to give the #{italic}##FIREBRICK#[peel]#{normal}##LAST# and our #{italic}##FIREBRICK#[garden]#{normal}##LAST# #{italic}##FIREBRICK#[tempo]#{normal}##LAST#, and would have failed had the #{italic}##FIREBRICK#[noise]#{normal}##LAST# not woken up #{italic}##FIREBRICK#[Father]#{normal}##LAST#.

We were sorry. We were so sorry. Our #{italic}##FIREBRICK#[pod]#{normal}##LAST# was #{italic}##FIREBRICK#[rotten]#{normal}##LAST# and we knew it; we should never have #{italic}##FIREBRICK#[planted it]#{normal}##LAST#. Father forgave us for our #{italic}##FIREBRICK#[spoiled barrel]#{normal}##LAST# and #{italic}##FIREBRICK#[fertilized our garden]#{normal}##LAST#; it was still burning and #{italic}##FIREBRICK#[salted]#{normal}##LAST#, but by #{italic}##FIREBRICK#[breaking out the toolbox]#{normal}##LAST# we could still #{italic}##FIREBRICK#[plant seeds]#{normal}##LAST# on it. We could not #{italic}##FIREBRICK#[bloom]#{normal}##LAST# but we could #{italic}##FIREBRICK#[hold a note, just one note]#{normal}##LAST#. #{italic}##FIREBRICK#[Father]#{normal}##LAST# is still devoting all his will to #{italic}##FIREBRICK#[nailing our garden together]#{normal}##LAST#; it will #{italic}##FIREBRICK#[splinter and wilt]#{normal}##LAST# if he stopped for even a second. Bless the #{italic}##FIREBRICK#[Father]#{normal}##LAST# in his altruism. Bless the #{italic}##FIREBRICK#[Father]#{normal}##LAST#. We are so sorry.

(You unsteadily touch your palm to the next panel. You stand on a charred, bubbling cliff, and see a black, star-dotted expanse above and below you. Your feet are constantly searing; the mages could give you oxygen and convert ambient magic into caloric energy, but they couldn't undo the terrible magical flames that rage on the blown-off continent, or the eternal pyre of your former planet. Nearly everyone you know is dead, and your scryers tell you the home of the #{italic}##FIREBRICK#[egg-weeds]#{normal}##LAST# has suffered only minor damage; all the others you've contacted through portals were blown apart instantly. Your home only survives from the constant effort and concentration of #{italic}##FIREBRICK#[Father]#{normal}##LAST#, who is exerting every bit of magic he can to keep the shattered fragments from spinning off into the void. There is no part of you that does not feel deep regret; you would commit suicide if you did not hope there was a way you could apologize to #{italic}##FIREBRICK#[Father]#{normal}##LAST#, work as tirelessly and selflessly as he is. The regret drains as your hand leaves the panel.)

We asked #{italic}##FIREBRICK#[Father]#{normal}##LAST# what #{italic}##FIREBRICK#[song to sing]#{normal}##LAST# to #{italic}##FIREBRICK#[make him dance]#{normal}##LAST# again. He told us: #{italic}##FIREBRICK#[rattle]#{normal}##LAST# the #{italic}##FIREBRICK#[egg-weeds]#{normal}##LAST# until their every last #{italic}##FIREBRICK#[bead falls out]#{normal}##LAST#. We know our #{italic}##FIREBRICK#[orchestra hall]#{normal}##LAST#, and we will #{italic}##FIREBRICK#[crash the party]#{normal}##LAST#. For our sake, giving us a new #{italic}##FIREBRICK#[garden]#{normal}##LAST# to replace the one the #{italic}##FIREBRICK#[egg-weeds]#{normal}##LAST# or their #{italic}##FIREBRICK#[sprouts]#{normal}##LAST# stole from us. For #{italic}##FIREBRICK#[Father]#{normal}##LAST#'s sake, to let him #{italic}##FIREBRICK#[retire]#{normal}##LAST# again once we're #{italic}##FIREBRICK#[planted]#{normal}##LAST# once more. For everyone's sake, to avenge the #{italic}##FIREBRICK#[spilled beads]#{normal}##LAST# from the #{italic}##FIREBRICK#[brushfire]#{normal}##LAST# and bring #{italic}##FIREBRICK#[silence]#{normal}##LAST# from the #{italic}##FIREBRICK#[egg-weeds]#{normal}##LAST# and any #{italic}##FIREBRICK#[weeds]#{normal}##LAST# they #{italic}##FIREBRICK#[planted]#{normal}##LAST#.

(There is another panel. You touch it briefly. You hate yourself. You hate Eyal. You hate the Sher'Tul. You hate anything and everything around you. You want to destroy it, letting the souls of trillions know that justice has been done. You want to purge not just the Sher'Tul, but anything that has ever been close to them. Elves. Halflings. Orcs. Humans. All could carry their taint. All survived, while everything else that used a portal burned. If there is even a possibility that a single Sher'Tul remains on Eyal, it must be purged in blighted fire. Justice has to be done to Eyal. You remain angry at nothing in particular for ten minutes after you remove your hand.)

#{italic}##FIREBRICK#[Father]#{normal}##LAST# helped our #{italic}##FIREBRICK#[carpenters]#{normal}##LAST# make #{italic}##FIREBRICK#[power tools]#{normal}##LAST#, forms of his blessed #{italic}##FIREBRICK#[fix-it wrenches]#{normal}##LAST# which could transform us to #{italic}##FIREBRICK#[shake harder]#{normal}##LAST#. The #{italic}##FIREBRICK#[peas]#{normal}##LAST# dripped with acid, the #{italic}##FIREBRICK#[beets]#{normal}##LAST# gained tremendous speed, the #{italic}##FIREBRICK#[peppers]#{normal}##LAST# fused their hands with #{italic}##FIREBRICK#[noisy dirt]#{normal}##LAST# to sling it at those who originally #{italic}##FIREBRICK#[made the racket]#{normal}##LAST#. The #{italic}##FIREBRICK#[blooming]#{normal}##LAST# is a little #{italic}##FIREBRICK#[noisy]#{normal}##LAST#, but nothing compared to the #{italic}##FIREBRICK#[egg-weeds' screech]#{normal}##LAST#. We will either #{italic}##FIREBRICK#[be a handyman]#{normal}##LAST# or #{italic}##FIREBRICK#[wilt in the sun]#{normal}##LAST#. Press the next panel to #{italic}##FIREBRICK#[grab a toolbox]#{normal}##LAST#. Be a #{italic}##FIREBRICK#[handyman]#{normal}##LAST#.

(You know all too well what this next panel does, and memories of being chained and bound while a wretchling presses it to your forehead flash through your mind. Despite a fading compulsion, no force in Eyal could convince you to touch the panel.)

```
译文：
```text
（你看到这里有一堆奇怪的石板，码成了整整齐齐的一摞。你取下最上面的一块，仔细研究起来；手指无意间滑过一角的方格，奇怪的句子便开始在你脑海中回响。你努力理解思绪中那些陌生的词语和概念。）

许多个#{italic}##FIREBRICK#[月面环形山]#{normal}##LAST#过去了；在他#{italic}##FIREBRICK#[播种]#{normal}##LAST#我们并#{italic}##FIREBRICK#[退休]#{normal}##LAST#之后，#{italic}##FIREBRICK#[父亲]#{normal}##LAST#从他的#{italic}##FIREBRICK#[茧]#{normal}##LAST#中醒来，看见我们正在#{italic}##FIREBRICK#[嘎啦作响]#{normal}##LAST#。他震惊于我们#{italic}##FIREBRICK#[枯萎]#{normal}##LAST#的模样，问我们为何#{italic}##FIREBRICK#[嘎啦作响]#{normal}##LAST#；我们告诉他，我们不得不忍受怎样的#{italic}##FIREBRICK#[摇晃]#{normal}##LAST#，这颗星球又是如何被#{italic}##FIREBRICK#[塞住]#{normal}##LAST#的。虽然我们那些#{italic}##FIREBRICK#[同荚之豆]#{normal}##LAST#已经#{italic}##FIREBRICK#[堵住漏洞]#{normal}##LAST#，不让#{italic}##FIREBRICK#[珠子]#{normal}##LAST##{italic}##FIREBRICK#[掉出去]#{normal}##LAST#，可#{italic}##FIREBRICK#[扫帚]#{normal}##LAST#仍不断把我们的#{italic}##FIREBRICK#[尘兔]#{normal}##LAST#扫走，而空余的地方又不够多，无法阻止#{italic}##FIREBRICK#[珠子]#{normal}##LAST##{italic}##FIREBRICK#[开裂]#{normal}##LAST#。

（石板上这里有一个更大的方格；你把手按上去，眼前突然出现一颗饱受连绵沙尘暴蹂躏的荒漠星球。一个矮小的绿皮生物望着毁掉的庄稼，你感受到他的无力；一个红皮人形生物一手持剑、一手托着火球，冲向一大群矮小的缟玛瑙色生物，你感受到他的暴怒。你一移开手，这些影像便消失了。）

#{italic}##FIREBRICK#[父亲]#{normal}##LAST#把他的#{italic}##FIREBRICK#[工具]#{normal}##LAST#交给了我们；在我们#{italic}##FIREBRICK#[绊倒清洁工？]#{normal}##LAST#之后，他让我们#{italic}##FIREBRICK#[轻轻摇晃？]#{normal}##LAST#。然而，我们没有#{italic}##FIREBRICK#[嘎啦作响]#{normal}##LAST#，而是在#{italic}##FIREBRICK#[奏乐]#{normal}##LAST#，只#{italic}##FIREBRICK#[敲裂]#{normal}##LAST#那些#{italic}##FIREBRICK#[珠子]#{normal}##LAST#，也就是令我们#{italic}##FIREBRICK#[走调]#{normal}##LAST#的珠子；我们的#{italic}##FIREBRICK#[珠子]#{normal}##LAST#变得更加强壮，还学会了使用各种#{italic}##FIREBRICK#[工具]#{normal}##LAST#，其#{italic}##FIREBRICK#[颜色]#{normal}##LAST#不同于#{italic}##FIREBRICK#[父亲]#{normal}##LAST#给我们的工具。#{italic}##FIREBRICK#[父亲]#{normal}##LAST#喜欢#{italic}##FIREBRICK#[聆听我们的音乐]#{normal}##LAST#；每当我们需要时，他都会为我们#{italic}##FIREBRICK#[作曲]#{normal}##LAST#，对此我们感激不尽。不久，我们便能#{italic}##FIREBRICK#[谱写自己的音乐]#{normal}##LAST#，再也不必#{italic}##FIREBRICK#[嘎啦作响]#{normal}##LAST#，于是#{italic}##FIREBRICK#[父亲]#{normal}##LAST##{italic}##FIREBRICK#[退休]#{normal}##LAST#了。

（又一个更大的方格。你看见一位慈爱而美好的#{italic}##FIREBRICK#[父亲]#{normal}##LAST#降临在星球上，他所触之处，荒漠化作葱郁森林；你与绿色、缟玛瑙色和红宝石色的同胞一同崇拜着他。你们形态各异、大小不一，却第一次团结起来，感激他为你们做下的一切善举。许多年来，你第一次知道下一顿饭从何而来，也不必再害怕别人为了农田杀死你，更不必惧怕沙尘暴。他手中握着几名隐居土系法师的尸体，正是他们制造了风暴；你本应憎恨他们，心中却只剩对未来的喜悦。你和同胞们开始以有组织的方式相互竞争，偶尔也再度交战，但即便死去，你也知道那是为了星球的福祉；一个时代过去，你和同胞们比从前更聪明、更强壮，也快乐得多，生活在乐园之中。一瞬之后，你移开了手，崇拜与敬仰之情随之从心中退去。）

终于，#{italic}##FIREBRICK#[蛋形杂草]#{normal}##LAST#来了。我们试着#{italic}##FIREBRICK#[敲裂他们的珠子]#{normal}##LAST#，却毫无作用；他们没有试图#{italic}##FIREBRICK#[敲裂]#{normal}##LAST#我们，反而许诺给我们更美妙的#{italic}##FIREBRICK#[乐谱]#{normal}##LAST#，胜过#{italic}##FIREBRICK#[父亲]#{normal}##LAST#所赐的一切，条件是让他们把他#{italic}##FIREBRICK#[摔碎]#{normal}##LAST#。我们拒绝了，但还是同他们结成了一个#{italic}##FIREBRICK#[坏豆荚]#{normal}##LAST#：我们会#{italic}##FIREBRICK#[消音？栽盆？]#{normal}##LAST#那位#{italic}##FIREBRICK#[父亲]#{normal}##LAST#，用他交给我们的#{italic}##FIREBRICK#[工具]#{normal}##LAST#使他变成一个#{italic}##FIREBRICK#[懒木匠]#{normal}##LAST#，以此向#{italic}##FIREBRICK#[蛋形杂草]#{normal}##LAST#证明我们同他们之间的#{italic}##FIREBRICK#[豆荚已经封闭]#{normal}##LAST#。#{italic}##FIREBRICK#[父亲]#{normal}##LAST#不会因此被#{italic}##FIREBRICK#[摇响或敲裂]#{normal}##LAST#；他甚至什么都不会知道。#{italic}##FIREBRICK#[蛋形杂草]#{normal}##LAST#很满意，便#{italic}##FIREBRICK#[涂抹]#{normal}##LAST#他们的#{italic}##FIREBRICK#[吸蛋器]#{normal}##LAST#到我们的星球上，使我们得以同#{italic}##FIREBRICK#[其他植物的豆荚]#{normal}##LAST#贸易；那些豆荚来自各种各样的#{italic}##FIREBRICK#[花园]#{normal}##LAST#。我们尝到了新食物，学会了新#{italic}##FIREBRICK#[工具]#{normal}##LAST#，还有一些#{italic}##FIREBRICK#[花哨]#{normal}##LAST#的新型#{italic}##FIREBRICK#[珠子]#{normal}##LAST#来到我们的#{italic}##FIREBRICK#[花园]#{normal}##LAST#。提起#{italic}##FIREBRICK#[父亲]#{normal}##LAST#，我们感到了一点#{italic}##FIREBRICK#[噪声]#{normal}##LAST#，但他并不#{italic}##FIREBRICK#[吵闹]#{normal}##LAST#，也不会#{italic}##FIREBRICK#[听见]#{normal}##LAST#任何#{italic}##FIREBRICK#[声响]#{normal}##LAST#。#{italic}##FIREBRICK#[蛋形杂草]#{normal}##LAST#充当了我们的#{italic}##FIREBRICK#[荚中豆]#{normal}##LAST#，我们以极大的#{italic}##FIREBRICK#[聆听]#{normal}##LAST#对待他们；即使他们后来#{italic}##FIREBRICK#[滑出豆荚]#{normal}##LAST#，我们再也无法#{italic}##FIREBRICK#[参加彼此的音乐会]#{normal}##LAST#，也是如此。

（你触碰下一页上的面板。一个生物从一座巨大的堡垒中走出来，出现在你面前——它有着蛋形的身体，四肢则像四根#{italic}##FIREBRICK#[藤蔓杂草]#{normal}##LAST#。你打心底憎恨这东西，尽管你知道自己当时并不憎恨它。他们说想要#{italic}##FIREBRICK#[父亲]#{normal}##LAST#死，并愿以强大的魔法和技术作为回报；你厌恶得不愿考虑这个提议，可他们的堡垒和武器让你不禁怀疑，这提议是否真能拒绝。你考虑唤醒#{italic}##FIREBRICK#[父亲]#{normal}##LAST#向他求助，却又担心即便是他，也无法抵挡#{italic}##FIREBRICK#[蛋形杂草]#{normal}##LAST#；最终，你决定将他封在沉睡中，让他无力反抗却不受伤害，保持昏迷，直至将来有人介入。#{italic}##FIREBRICK#[蛋形杂草]#{normal}##LAST#勉强接受了这个解决办法，并履行了交易中他们应尽的一方。他们送给你们奇异而强大的神器，又在你们的世界建起传送门，让你们得以前往陌生的世界；那些世界远比你所能想象的更加不可思议、更加美丽，其中还有其他获赠这些礼物、希望进行贸易的种族。你品尝新食物，学习新魔法，聆听新音乐，发现了整个文明史上前所未见的美。若不是心中阵阵愧疚，生活简直不可能更美好。直到你移开手、影像开始从脑海消退，才认出这些“蛋形杂草”就是夏·图尔。）

随后响起了巨大的#{italic}##FIREBRICK#[噪声]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。声音变得#{italic}##FIREBRICK#[更响]#{normal}##LAST#。最后，那声音变得#{italic}##FIREBRICK#[震耳膜裂]#{normal}##LAST#。

（这里还有一块面板。你不敢触碰，可就在你伸手准备把石板收起来时，一根手指从上面轻轻擦过。饥饿、灼烧、窒息、悲惨、狂怒和纯粹的剧痛在你脑中肆虐；你知道这只持续了十分之一秒，感觉却像足足半分钟。走向下一个方格时，你的耳朵仍嗡嗡作响。）

那些#{italic}##FIREBRICK#[吸蛋器]#{normal}##LAST#是陷阱，是一曲#{italic}##FIREBRICK#[不和谐音]#{normal}##LAST#，由#{italic}##FIREBRICK#[蛋形杂草]#{normal}##LAST#埋下，意图#{italic}##FIREBRICK#[敲裂]#{normal}##LAST#我们所有人，却只给他们自己的星球造成一道#{italic}##FIREBRICK#[发丝裂纹]#{normal}##LAST#，伤及他们的#{italic}##FIREBRICK#[花园]#{normal}##LAST#。他们的#{italic}##FIREBRICK#[错音]#{normal}##LAST#把我们的星球化作#{italic}##FIREBRICK#[嘈杂合奏]#{normal}##LAST#，我们几乎全都#{italic}##FIREBRICK#[掉出了豆荚]#{normal}##LAST#。#{italic}##FIREBRICK#[苹果被削了皮]#{normal}##LAST#，我们#{italic}##FIREBRICK#[外壳]#{normal}##LAST#的一块碎片漂浮在#{italic}##FIREBRICK#[海洋]#{normal}##LAST#中。我们的#{italic}##FIREBRICK#[杂务工]#{normal}##LAST#迅速行动起来，让#{italic}##FIREBRICK#[果皮]#{normal}##LAST#和我们的#{italic}##FIREBRICK#[花园]#{normal}##LAST#保持#{italic}##FIREBRICK#[节拍]#{normal}##LAST#；若不是那阵#{italic}##FIREBRICK#[噪声]#{normal}##LAST#唤醒了#{italic}##FIREBRICK#[父亲]#{normal}##LAST#，他们本会功亏一篑。

我们很抱歉。我们真的非常抱歉。我们的#{italic}##FIREBRICK#[豆荚]#{normal}##LAST#已经#{italic}##FIREBRICK#[腐烂]#{normal}##LAST#，我们心知肚明；当初根本不该#{italic}##FIREBRICK#[种下它]#{normal}##LAST#。父亲宽恕了我们的#{italic}##FIREBRICK#[坏掉的一桶]#{normal}##LAST#，并#{italic}##FIREBRICK#[给我们的花园施肥]#{normal}##LAST#；花园仍在燃烧，也依旧#{italic}##FIREBRICK#[盐碱化]#{normal}##LAST#，但只要#{italic}##FIREBRICK#[搬出工具箱]#{normal}##LAST#，我们仍能在上面#{italic}##FIREBRICK#[播下种子]#{normal}##LAST#。我们无法#{italic}##FIREBRICK#[绽放]#{normal}##LAST#，却还能#{italic}##FIREBRICK#[维持一个音符，仅仅一个音符]#{normal}##LAST#。#{italic}##FIREBRICK#[父亲]#{normal}##LAST#仍在倾注全部意志，#{italic}##FIREBRICK#[把我们的花园钉在一起]#{normal}##LAST#；他哪怕停下一秒，它都会#{italic}##FIREBRICK#[碎裂枯萎]#{normal}##LAST#。愿无私的#{italic}##FIREBRICK#[父亲]#{normal}##LAST#蒙福。愿#{italic}##FIREBRICK#[父亲]#{normal}##LAST#蒙福。我们真的非常抱歉。

（你摇摇晃晃地把手掌按在下一块面板上。你站在一处焦黑、冒泡的悬崖上，上下两方都是点缀着星辰的漆黑虚空。双脚时刻经受灼烧；法师们能为你提供氧气，把环境中的魔力转化为热量能量，却无法熄灭那片被炸飞的大陆上肆虐的可怕魔法火焰，也无法扑灭你昔日星球那座永恒的火葬堆。你认识的人几乎全死了，而占卜师告诉你，#{italic}##FIREBRICK#[蛋形杂草]#{normal}##LAST#的家园只受了轻微损伤；至于你们通过传送门联系过的其他世界，全都在一瞬间四分五裂。你们的家园之所以尚存，全靠#{italic}##FIREBRICK#[父亲]#{normal}##LAST#不间断的努力与专注；他正使出每一分魔力，阻止破碎的大地旋入虚空。你心中每一处都充满深切悔恨；若非仍盼望能有机会向#{italic}##FIREBRICK#[父亲]#{normal}##LAST#道歉，像他一样不知疲倦、无私无我地工作，你早已自尽。手离开面板时，悔恨也随之退去。）

我们问#{italic}##FIREBRICK#[父亲]#{normal}##LAST#，该#{italic}##FIREBRICK#[唱哪首歌]#{normal}##LAST#才能#{italic}##FIREBRICK#[令他起舞]#{normal}##LAST#。他告诉我们：#{italic}##FIREBRICK#[摇响]#{normal}##LAST#那些#{italic}##FIREBRICK#[蛋形杂草]#{normal}##LAST#，直到他们最后一颗#{italic}##FIREBRICK#[珠子掉出来]#{normal}##LAST#。我们熟悉自己的#{italic}##FIREBRICK#[乐团大厅]#{normal}##LAST#，也必将#{italic}##FIREBRICK#[闯进派对]#{normal}##LAST#。为了我们自己——夺回一座新的#{italic}##FIREBRICK#[花园]#{normal}##LAST#，补偿#{italic}##FIREBRICK#[蛋形杂草]#{normal}##LAST#或他们的#{italic}##FIREBRICK#[嫩芽]#{normal}##LAST#从我们手中偷走的那一座。为了#{italic}##FIREBRICK#[父亲]#{normal}##LAST#——让他再次#{italic}##FIREBRICK#[退休]#{normal}##LAST#，等我们又一次#{italic}##FIREBRICK#[栽种]#{normal}##LAST#下去。为了所有人——替#{italic}##FIREBRICK#[洒落的珠子]#{normal}##LAST#复仇，那些珠子洒落在#{italic}##FIREBRICK#[灌木火]#{normal}##LAST#之中；带来#{italic}##FIREBRICK#[寂静]#{normal}##LAST#，终结#{italic}##FIREBRICK#[蛋形杂草]#{normal}##LAST#以及他们#{italic}##FIREBRICK#[栽种]#{normal}##LAST#的每一株#{italic}##FIREBRICK#[杂草]#{normal}##LAST#。

（这里还有一块面板。你短暂地触碰了它。你恨自己。你恨埃亚尔。你恨夏·图尔。你恨身边的一切。你想摧毁一切，让数万亿亡魂知道正义已经得到伸张。你不只想肃清夏·图尔，还想肃清任何曾与他们亲近的东西。精灵。半身人。兽人。人类。任何一族都可能携带他们的污秽。其他所有使用传送门的种族都被烧死了，唯独这些种族活了下来。只要埃亚尔上仍有哪怕一个夏·图尔存在的可能，这里就必须被枯萎之火彻底净化。必须对埃亚尔执行正义。移开手后，你仍莫名其妙地愤怒了整整十分钟。）

#{italic}##FIREBRICK#[父亲]#{normal}##LAST#帮助我们的#{italic}##FIREBRICK#[木匠]#{normal}##LAST#打造出#{italic}##FIREBRICK#[动力工具]#{normal}##LAST#；这些是他赐福的#{italic}##FIREBRICK#[维修扳手]#{normal}##LAST#的不同形态，能改造我们，使我们#{italic}##FIREBRICK#[摇晃得更猛烈]#{normal}##LAST#。#{italic}##FIREBRICK#[豌豆]#{normal}##LAST#滴淌着酸液，#{italic}##FIREBRICK#[甜菜]#{normal}##LAST#获得了惊人的速度，#{italic}##FIREBRICK#[辣椒]#{normal}##LAST#则把双手同#{italic}##FIREBRICK#[吵闹的泥土]#{normal}##LAST#融为一体，再将泥土射向最初#{italic}##FIREBRICK#[制造喧闹]#{normal}##LAST#的那些家伙。#{italic}##FIREBRICK#[开花]#{normal}##LAST#过程有些#{italic}##FIREBRICK#[嘈杂]#{normal}##LAST#，但与#{italic}##FIREBRICK#[蛋形杂草的尖啸]#{normal}##LAST#相比根本不算什么。我们要么#{italic}##FIREBRICK#[成为杂务工]#{normal}##LAST#，要么#{italic}##FIREBRICK#[在阳光下枯萎]#{normal}##LAST#。按下下一块面板，#{italic}##FIREBRICK#[拿起工具箱]#{normal}##LAST#。成为一名#{italic}##FIREBRICK#[杂务工]#{normal}##LAST#。

（你太清楚下一块面板的作用了：遭锁链缠身、动弹不得时，一个猥琐小怪把它按上你额头的记忆在脑海中闪回。尽管那股强迫意志正在消退，埃亚尔也没有任何力量能说服你触碰这块面板。）
```

## entry-03366
位置：tome-ashes-urhrok.lua:400；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{italic}#More memories rush into your mind...#{normal}#

"It's your lucky day, <?=player.name?>," your handler says as he leads you to a large, glowing crystal.  "You're too cooperative to stay in testing any longer.  Today, you're getting promoted to research assistant!"  You're nearly beside yourself with joy!  "Now, we'll need to do a short little process first.  Fireproofing wards here, loyalty reinforcement there, standard-issue alteration, but mostly just linking your consciousness to this," he says, pointing to the crystal.  "With this thing, everything you see, hear, smell, taste, or feel gets fed directly into this little ol' beauty.  Not just that, either - whereever you go, and whatever you think, we'll have it saved for future reference."  You're going to help them learn so much!  "Just step on the plate here, and hold your arms like this so I can get the bindings in place..."

That crystal.  That crystal is how they're keeping track of you, and it has most of what you helped them discover trapped within it.  If you break it, you'll be able to escape their notice for the first time since you arrived here, allowing you to get away without them finding you again, and as an added bonus you'll undo most of what you helped them accomplish.  You need to destroy it, then flee for your life!
```
译文：
```text
#{italic}#更多记忆涌入了你的脑海……#{normal}#

“记住，这是你的幸运日，<?=player.name?>，”你的“主人”带着你到一块巨大的闪耀水晶面前，“你非常合作，因此你将从一般实验中解放。现在你被提升为研究助理！”闻言，你欣喜若狂！“好了，现在我们需要先做一些事情。火焰防护在这，忠诚强化在那，标准化思维修改，呃，不过主要还是将你的意识链接到这里，”他一边说，一边指着水晶体，“有了这个，你看到的、听到的、嗅到的、尝到的、感觉到的全都能体现在这块美丽精巧的水晶里。不仅如此，不管你去哪，不管你想什么，都能记录下来，以供研究。”你突然发现自己能帮助他们研究如此之多！“站在那里别动，举起胳膊，这样我就能把它放好……”

那块水晶，对，那就是他们追踪你的方式，同时也封存着你帮助他们取得的大部分发现。如果你摧毁了它，你就能避开他们的注意，逃出这里，不被他们发现，并抵消你帮助他们完成的大部分成果。你必须要摧毁它，然后逃跑！
```

## entry-03367
位置：tome-ashes-urhrok.lua:409；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
orbital base: battle plan (doombringer)
```
译文：
```text
轨道基地：战斗计划（毁灭使者）
```

## entry-03368
位置：tome-ashes-urhrok.lua:425；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
orbital base: battle plan (demonologist)
```
译文：
```text
轨道基地：战斗计划（恶魔使者）
```

## entry-03369
位置：tome-ashes-urhrok.lua:453；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
orbital base: battle plan (doomelf)
```
译文：
```text
轨道基地：战斗计划（魔化精灵）
```

## entry-03370
位置：tome-ashes-urhrok.lua:474；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
orbital base: battle info
```
译文：
```text
轨道基地：战斗情报
```

## entry-03371
位置：tome-ashes-urhrok.lua:491；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{italic}#This note is stained with what appear to be motorcycle tire-tracks.#{normal}#

#{bold}#URGENT:#{normal}#

Operation to secure <?=player.name?> failure.  Primary defense force routed by target's overwhelming badassery, secondary team presumed dead (reports inaudible over sound of face-melting guitar solos).  All is lost.  Totally worth it.  Highest priority is now isolating <?=player.name?>, building a stadium around <?=player:him_her()?>, and selling tickets to spectacle of badassery.  Blow all connectors, break platform off the continent, prepare pyrotechnics, and set up spotlights and speaker systems befo--

#{italic}#The last O trails off, a line leading from it to the end of the page like the pen was rapidly jerked away, then leads to a doodle depicting you, wielding a double-bladed katana and fighting a giant construct labelled "Ninja Atamathon."  Your badassery must have interrupted this demon's writing.#{normal}#

```
译文：
```text
#{italic}#这张便条被摩托车轮胎的痕迹弄脏了。#{normal}#

#{bold}#紧急事项：#{normal}#

对 <?=player.name?> 的保全监禁计划失败。主要防御力量被他的霸气侧漏吓退，应急部队推定已经死亡（报告的声音被吉他独奏的喧哗声盖住了）。虽然计划完全失败，但是这辈子值了。正在对 <?=player.name?> 启动最高优先级措施，为 <?=player:him_her()?> 建造一个体育场，让观众买票入场观看其霸气侧漏的情景。  关闭所有链接传送门，将所属的平台从大陆上分离，准备焰火，启动闪光灯和音响系统并——

#{italic}#最后一个字歪歪扭扭，一条墨水细线向下划去直到页面的底部，那是笔从手上滑落留下的痕迹。下方是一幅关于你的涂鸦，手里拿着武士刀，正在和“忍者王阿塔玛森”对战。看起来，你的霸气侧漏把这个恶魔吓尿了。#{normal}#

```

## entry-03372
位置：tome-ashes-urhrok.lua:514；section：tome-ashes-urhrok/data/lore/demon.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Behold, the humble wretchling, a testament to our devotion to our Father!  These children of emerald were among the first to alter themselves for our quest for vengeance, and managed an astounding degree of success.  With their bursts of blinding speed, overwhelming numbers, and skin that can release prodigious amounts of corrosive fluid, wretchlings can storm onto the battlefield and pounce on our foes one-by-one, dissolving the ground they walk on while leaving them helpless against our onslaught.  Wretchlings will readily give their lives in combat, serving as obstructions and shields while their acid and our casters do their work, and still remain the most populous of our species thanks to their incredible birth rates.  It is rare to see a wretchling survive to maturity, but make no mistake - every wretchling that fights does an incredible service to our cause.
```
译文：
```text
看着他，谦逊的酸液树魔，这是我们对父亲奉献一切的证明！这些绿翡翠的孩子们第一批同意改变自身以帮助复仇，同时取得了惊人的成功。极快的速度、庞大的数目以及能释放大量酸液的皮肤，酸液树魔能旋风般猛冲入战场，一个个扑住敌人，溶解土地，将无助的敌人暴露在我们的杀戮前。酸液树魔时刻准备着，怀着大无畏的牺牲精神，以肉体充当屏障，令酸液和法术能够发挥作用。尽管如此，在他们惊人的繁殖率下，他们仍是我们中数目最多的种族。我们很难见到一只酸液树魔活到成熟期，但请记住——每一只战斗过的酸液树魔都为我们的目标奉献了一切。
```

## 相关术语快照
仅按source_tag/category/语境适用；existing不构成强制改名。
```tsv
source	target	category	domain	source_tag	status	scope	notes
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
All Resists	全部抗性	T.GAME.STAT	combat	_t	preferred	core	角色面板 All Resists 行；对应 resists.all
Constitution	体质	T.GAME.STAT	combat	stat name	existing	global	
Construct	构装生物	T.PN.RACE	creatures	birth descriptor name	existing	core	构装生物种族
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Demonologist	恶魔使者	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	Ashes of Urh'Rok 职业
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Doombringer	毁灭使者	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	Ashes of Urh'Rok 职业
Doomelf	魔化精灵	T.PN.RACE	creatures	birth descriptor name	existing	dlc	Ashes of Urh'Rok 种族
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Giant	巨人	T.PN.RACE	creatures	birth descriptor name	existing	core	巨人种族总称
Halfling	半身人	T.PN.RACE	creatures	birth descriptor name	existing	core	
Hate	仇恨值	T.GAME.RESOURCE	resources	nil	preferred	core	诅咒系职业资源；技能描述中统一不用“怒气”
Human	人类	T.PN.RACE	creatures	birth descriptor name	existing	core	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Luck	幸运	T.GAME.STAT	combat	stat name	existing	global	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Name	名称	T.UI.LABEL	ui	_t	preferred	global	界面标签（17 处）
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Physical Power	物理强度	T.GAME.STAT	combat	tformat	preferred	core	角色面板物理强度；力量属性描述与技能效果统一用此译名
Resistances	抗性	T.GAME.STAT	combat	_t	preferred	core	角色面板 Resistances base/cap 行；单系抗性为“X抗性”，全抗为 All Resists 全部抗性
Retch	腐秽呕吐	T.GAME.TALENT	talents	talent name	preferred	core	食尸鬼种族技能；在地面制造呕吐区域，治疗不死族并伤害其他生物
Sher'Tul	夏·图尔	T.PN.RACE	creatures	nil	existing	core	
Silence	沉默	T.GAME.TALENT	talents	talent name	existing	global	
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Souls	灵魂	T.GAME.RESOURCE	combat	_t	preferred	core	死灵法师资源；Maximum souls 灵魂上限
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
The Way	维网	T.PN.FACTION	society	nil	existing	core	
Willpower	意志	T.GAME.STAT	combat	stat name	existing	global	
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blight	枯萎	T.GAME.DAMAGE	combat	damage type	existing	core	
blight	枯萎	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blind	致盲	T.GAME.EFFECT	combat	effect subtype	existing	global	
blinding	致盲	T.GAME.DAMAGE	combat	damage type	existing	global	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
construct	构装体	T.GAME.ENTITY	creatures	entity type	preferred	global	机械或魔法制造的生物实体类型；与种族 Construct“构装生物”区分，不作“机关”
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
doom	末日	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	Cults of Entropy 技能树/技能类别名；P1 审核确认
doomelf	魔化精灵	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
giant	巨人	T.GAME.ENTITY	creatures	entity type	existing	global	
halfling	半身人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
horror	恐怖	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Cults 恐怖/恐惧系效果类别（Putrescent Pustule、Horrific Display 等）；entity type 语境的“恐魔”保留；P0 审核确认
horror	恐魔	T.GAME.ENTITY	creatures	entity type	existing	global	
human	人类	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
humanoid	人形生物	T.GAME.ENTITY	creatures	entity type	existing	global	
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
race	种族技能	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
sense	感知	T.GAME.EFFECT	combat	effect subtype	existing	global	
sher'tul	夏·图尔	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
silence	沉默	T.GAME.EFFECT	combat	effect subtype	existing	core	
sleep	睡眠	T.GAME.EFFECT	combat	effect subtype	existing	global	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
spellblaze	魔法大爆炸	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
spellblaze	魔法大爆炸	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与世界事件的其他标签区分
spellblaze	魔法大爆炸	T.PN.WORLD	places	effect subtype	existing	core	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
tome	书册	T.GAME.ENTITY	items	entity subtype	existing	global	
trap	陷阱	T.GAME.ENTITY	items	entity name	preferred	global	陷阱实体（20 处）
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wrath	愤怒	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
```
