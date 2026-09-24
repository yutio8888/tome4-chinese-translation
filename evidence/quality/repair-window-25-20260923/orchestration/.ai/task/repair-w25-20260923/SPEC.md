# 修复窗口25：271批8条确认问题

Paseo MCP / schema5 translation_contextual_v2 implement；基线ff0278e058d8e243c6ffb770c582d60e4d035d24。用户2026-09-23授权持续推进审核与修复、提交与推送，无需逐批确认；有争议条目记pending待用户集中审阅。按审核/修复1:1节奏开窗。

唯一EXECUTOR仅修改mod-tome.lua中WORKSET的8个target及evidence/quality/repair-window-25-20260923/。不修改其他译文、术语库、规则、工具、旧证据；首次不修改handoff/catalog/migration；不stage/commit/push、不写.ai、不创建agent。保留既有无关未跟踪文件。

SOURCE-CLAIMS仅供实施，reviewer只读中性冻结输入和相关固定源码；不传宿主裁决。源码固定624a67329fe2ad440c5b344785a9c73fcf22ae63。source/source_tag/args_order/printf占位符/%%/markup保持基线；LF/TAB 必须与原文逐处一致（多段条目逐行比对空行位置，不只看总数）。专名、技能名沿用本库现有译名（先在mod-tome.lua查证，并查同技能/同效果相邻条目已用译法），不自行新造。

8条按契约选择full：REVIEW/full（codex/gpt-6-sol）与FINAL_REVIEW/full（claude/claude-opus-5-5）。max_cycles默认3；FINAL_REVIEW 中任何 ISSUE 都算失败，修复后必须先 RE_REVIEW 再 FINAL_REVIEW。每条按整句核对，不只改被点名处；下列示例措辞仅为方向，落笔时仍须逐词对照原文。LuaJIT全记录比较恰8个target变动；strict lint/claims、diff check、完整门禁/构建、DONE_VERIFIED。译文commit→queue→单次catalog/migration→证据发布commit→queue→push，然后继续审核272。

范围约束（每条都逐句对照原文，发现明显增删一并修正，不重写已忠实的句子）：
- 疲劳圣印说明（talents/celestial/other.lua:420，tformat）：All enemies walking over the glyph——补“敌人”（陷阱只对敌对单位触发），不要写“所有经过的目标”；原文 1 个 \n\t\t 保持。
- 指令水晶球（亡灵）描述（general/objects/quest-artifacts.lua:177）：Dark visions fill your mind as you lift the orb.——“黑暗的幻象充满你的脑海”一类，不加“无尽”；第二句 It is cold to the touch. 保持。
- 血祭施法效果说明（timed_effects/magical.lua:2458）：Corruptions consume health instead of vim.——Corruptions 指堕落系法术（本库同类说法“堕落系法术”），不是“堕落者”；vim=活力值。
- 减速（Speed Sap）说明（talents/misc/npcs.lua:1653，tformat）：原文以 \n\t\t 结尾（1 个 LF、2 个 TAB），现译无，须在末尾补回；for three turns 持续三回合；%0.2f、30%% 保持。
- 摄魂剑·莫瑞格日志（general/objects/world-artifacts.lua:3642，tformat）：@Source@ taps the #SALMON#trapped soul#LAST# of %s, xmanifesting %s!——武器吞噬被杀者灵魂并反复使用其技能，灵魂未被释放：taps 是“汲取”，manifesting %s 是“显现/施展 %s”，不要“放出”“模仿”；第一个 %s 是被杀者名，第二个是技能名，两者先后顺序保持；@Source@、#SALMON#、#LAST# 保持（原文 xmanifesting 为上游笔误，按 manifesting 理解）。
- 第一滴血说明（talents/techniques/marksmanship.lua:57–68，tformat）：against these targets 仅对 90%% 以上生命的目标；(if capable of marking) 补“（若能标记）”；restore %0.1f stamina on hit 补“命中时”；技能名射击、稳固射击、爆头沿用本库；原文 1 个 \n（无 TAB）保持。
- 夏图尔壁画阿马克泰尔创世文本（lore/shertul.lua:40，#{italic}#…#{normal}#）：his might surpassed all else（力量凌驾万物）；the petty gods fled before his glory（伪神在其荣光前逃离，petty gods 按术语库保持“伪神”）；he made the Sun from his breath（以气息造出太阳）and held it above the world；All that this light touches shall be mine（光所照之处皆归我有），and this light shall touch all the world。标记保持。
- 盗匪日志（lore/misc.lua:656–662）：第二段 Only a matter of time until that nobleman catches wind and comes after us 是贵族迟早会听到风声来追杀（威胁），We were about to get more gold than we could count for his lassie back 是本来即将用他女儿换来数不清的金子；第三段 leave that idiot burnt on a stake 是把他绑在柱上烧死（不是“穿在柱子上”）；其余段落逐句对照；原文 3 处 \n\n 与第三段末尾空格前的写法保持 LF 结构。

## fab2d8a942a284b81276cb30db491f20589a92acebf8170dbd33a6adddc57222

section: mod-tome/data/talents/celestial/other.lua
source_tag: tformat

source: You bind light in a glyph on the floor. All enemies walking over the glyph will be slowed by %d%% for 5 turns.
		The glyph is a hidden trap (%d detection and %d disarm power based on your Magic) and lasts for %d turns.

target: 你用光能在地上刻画圣印。所有经过的目标会减速 %d%%，持续 5 回合。
		圣印视为隐藏陷阱（%d 侦查强度，%d 点解除强度，基于魔法）持续 %d 回合。

确认依据：talents/celestial/other.lua:385–420（624a673）Glyph of Fatigue（疲劳圣印）：陷阱 canTrigger 仅在 who:reactionToward(summoner)<0（敌对）时触发；原文 All enemies walking over the glyph，现译“所有经过的目标”删去敌方限定（删限定词类，读作对任何经过者生效）。整条修复为“所有经过圣印的敌人”一类，其余逐句对照。
与 surface 同向：疲劳圣印陷阱 canTrigger 仅对敌对单位触发，现译“所有经过的目标”删去敌方限定。并入同条整句修复。

## fac87ff044dcfd8d35e72789dd64285dccfe2e548abe6521205cf8925f1047a4

section: mod-tome/data/general/objects/quest-artifacts.lua
source_tag: _t

source: Dark visions fill your mind as you lift the orb. It is cold to the touch.

target: 当你拿起这个水晶球时，无尽的黑暗扑面而来。这个球摸上去冰凉。

确认依据：general/objects/quest-artifacts.lua:177 Orb of Undeath（指令水晶球（亡灵））描述：Dark visions fill your mind as you lift the orb.——现译“无尽的黑暗扑面而来”丢了“幻象”“充满脑海”并增添“无尽”（一级 fidelity）。整条修复为“黑暗的幻象充满你的脑海”一类，第二句保持。
与 surface 同向：Dark visions fill your mind，现译丢“幻象/脑海”并增“无尽”。并入同条修复。

## fad7958eaa422b8d9d53eb490a80607d612b61ce184afb3d0cb1e1ae097f8632

section: mod-tome/data/timed_effects/magical.lua
source_tag: _t

source: Corruptions consume health instead of vim.

target: 堕落者消耗生命值来取代活力值。

确认依据：timed_effects/magical.lua:2456–2460 BLOODCASTING（血祭施法）效果说明：Corruptions consume health instead of vim.——Corruptions 指堕落系法术（本库同类说法“堕落系法术需要消耗…”），现译“堕落者”把法术误作施法者（一级 fidelity）。整条修复为“堕落系法术消耗生命值而非活力值”一类。
与 surface 同向并补充：Actor.lua:5580/5600 bloodcasting 属性改变堕落技能的活力消耗，Corruptions 指堕落系技能/法术，非施法者。并入同条修复。

## fae2367217e9ad3f2c4600823b78cd7c700e270df7f9ec30f3b4e7353aa88f28

section: mod-tome/data/talents/misc/npcs.lua
source_tag: tformat

source: Saps 30%% of the target's speed (increasing yours by the same amount) and inflicts %0.2f temporal damage for three turns.
		

target: 降低目标 30%% 速度，增加你等量的速度，并在 3 回合内造成 %0.2f 时空伤害。

确认依据：talents/misc/npcs.lua:1650–1655 Speed Sap（减速）说明（tformat）：原文以 \\n\\t\\t 结尾（1 个 LF、2 个 TAB），现译 0 个 LF（一级换行不变量，与既往裁决一致）。整条修复：末尾补回 \\n\\t\\t，其余逐句对照（for three turns 持续三回合）。

## fae9336cfe64b12bcb35426b508459203f8c93edb9ea5919fa75ba816741503c

section: mod-tome/data/general/objects/world-artifacts.lua
source_tag: tformat

source: @Source@ taps the #SALMON#trapped soul#LAST# of %s, xmanifesting %s!

target: @Source@放出了%s#SALMON#被束缚的灵魂#LAST#，模仿了%s！

确认依据：升级 surface advisory：world-artifacts.lua:3618–3645（624a673）Morrigor（摄魂剑·莫瑞格）special_on_kill 吞噬被杀者灵魂（日志 CONSUMES THE SOUL），取其一项技能作为 use_talent 并可反复充能使用，灵魂并未被放出；taps the trapped soul 是“汲取被困的灵魂”，manifesting %s 是“显现/施展 %s”。现译“放出了…被束缚的灵魂，模仿了%s”把汲取写成释放、施展写成模仿（一级机制）。整条修复，@Source@、#SALMON#…#LAST#、两个 %s 顺序保持（第一个为被杀者名，第二个为技能名）。

## fb0879a6f7942a8f6921e058b5ea72611279254880e329100ee7c4cc32240741

section: mod-tome/data/talents/techniques/marksmanship.lua
source_tag: tformat

source: You take advantage of unwary foes (those at or above 90%% life). Against these targets, Shoot, Steady Shot and Headshot bleed targets for %d%% additional damage over 5 turns and have a 50%% increased chance to mark (if capable of marking).
In addition, your Steady Shot, Shoot and Headshot now restore %0.1f stamina on hit.

target: 你趁敌人尚未防备（90%% 血量以上）施展攻击，射击、稳固射击和爆头使敌人流血 5 回合造成额外 %d%% 伤害，标记概率增加 50%%。
此外，你的射击、稳固射击和爆头回复 %0.1f 体力。

确认依据：talents/techniques/marksmanship.lua:38–49 First Blood（第一滴血）；archery.lua:80–87 incStamina 位于 archery_onhit 回调，仅命中时回复体力。现译“回复 %0.1f 体力”删去 on hit（删限定词类），且漏 (if capable of marking)。整条修复：补“命中时”“（若能标记）”，其余逐句对照。
与 surface 同向并补充：archery.lua:64–77 标记判定仅在已学 Master Marksman 或有 mark_steady 时进行，(if capable of marking) 是真实条件；archery.lua:87 incStamina 位于 archery_onhit。两处限定都要补回。

## fb643ca9df6b45f4d8fccf7748e6c66d889cd668fcccb030929706f2d2c55766

section: mod-tome/data/lore/shertul.lua
source_tag: _t

source: #{italic}#'But AMAKTHEL came, and his might surpassed all else, and the petty gods fled before his glory. And he made the Sun from his breath and held it above the world and said, "All that this light touches shall be mine, and this light shall touch all the world.'#{normal}#

target: #{italic}#但阿马克泰尔来了，他的勇武震慑了众人，伪神们慑服于他的荣耀。他深呼吸后把太阳高举到了世界之上，说：“阳光所至，即我所至，这光芒将照亮全世界。”#{normal}#

确认依据：lore/shertul.lua（624a673）夏图尔壁画文本（阿马克泰尔创世）：the petty gods fled before his glory 是“逃离”，现译“慑服”；he made the Sun from his breath 是“以气息造出太阳”，现译“他深呼吸后把太阳高举”丢了创造；his might surpassed all else 译“震慑了众人”亦偏（一级 fidelity）。整条修复，#{italic}#/#{normal}# 保持。
与 surface 同向并补充：All that this light touches shall be mine 是“光所照之处皆归我有”，现译“阳光所至，即我所至”亦偏。并入同条整句修复（petty gods 保持“伪神”）。

## fb817eecf922f889b58208f1c1736399b82c752873b7f8a7e39037bc79b1ed40

section: mod-tome/data/lore/misc.lua
source_tag: _t

source: The best haul we ever got, gone. We could have been set for life, the most legendary outlaws in all the lands! Villages would tremble at the thought of us roaming the woods.

Only a matter of time until that nobleman catches wind and comes after us. We were about to get more gold than we could count for his lassie back, and that dirt farmer set her on fire. Of all the skullbrained things to do for fun!

Ordered my men to kill any who pass by and been running triple guard. We need all the time we can get before they come for us, can't let any word out. Once we find somewhere new, I'll leave that idiot burnt on a stake as tribute and hope we don't catch chase. 

I'm going to enjoy hearing his screams, a log on the pyre a gold he cost us. Nice and slow, need to make sure he doesn't die easy.

target: 我们费了九牛二虎之力才钓到大鱼，没了！我们本来可以因此扬名立万，成为被整个大陆传颂的不法之徒的传奇，我们的传说会在绿林中传颂，村庄会在我们的面前颤抖，现在全完了！

我们本来只要再等一些时间，让那位贵族听到风声之后过来找我们，就可以从那位大小姐身上榨取一大笔钱，结果那个土老帽村炮居然把她烧死了！这个傻逼还说是为了找乐子！

很好，叫我的人杀掉任何胆敢闯进来的人，守卫的密度增加三倍。我们需要尽可能在他们过来之前抓紧时间，绝对不能泄露任何消息。在我们找到新的藏身地之后，我要把那个蠢货穿在柱子上作为祭品，希望我们不会被他们抓到。

我要好好品尝他的哀嚎，他让我们每损失一枚金币，火堆上就多一根木柴。把这家伙文火慢烤，可别便宜他，让他死的太快了。

确认依据：lore/misc.lua:656 起盗匪日志：Only a matter of time until that nobleman catches wind and comes after us 是贵族迟早会追杀他们（威胁），We were about to get more gold … for his lassie back 是本来即将拿到赎金；现译合成“只要再等贵族听到风声过来找我们就可以榨取一大笔钱”，把威胁写成计划（一级 fidelity）。整条修复该段，其余段落逐句对照、3 处 \\n\\n 保持。
与 surface 同向并补充：第三段 leave that idiot burnt on a stake 是“绑在柱上烧死”，现译“穿在柱子上”（刺穿）与后文火刑不一致。并入同条修复。
