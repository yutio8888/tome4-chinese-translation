# 修复窗口18：264批4条确认问题

Paseo MCP / schema5 translation_contextual_v2 implement；基线00c4861ad01d10d8a24d5e577fc6e6b308d412bc。用户2026-09-23授权持续推进审核与修复、提交与推送，无需逐批确认；有争议条目记pending待用户集中审阅。按审核/修复1:1节奏开窗。

唯一EXECUTOR仅修改mod-tome.lua中WORKSET的4个target及evidence/quality/repair-window-18-20260923/。不修改其他译文、术语库、规则、工具、旧证据；首次不修改handoff/catalog/migration；不stage/commit/push、不写.ai、不创建agent。保留既有无关未跟踪文件。

SOURCE-CLAIMS仅供实施，reviewer只读中性冻结输入和相关固定源码；不传宿主裁决。源码固定624a67329fe2ad440c5b344785a9c73fcf22ae63。source/source_tag/args_order/printf占位符/markup保持基线；LF/TAB 必须与原文逐处一致（Offhand Jab 要删除一处多余换行）。专名、技能名沿用本库现有译名（先在mod-tome.lua查证），不自行新造。

4条按契约选择full：REVIEW/full（codex/gpt-6-sol）与FINAL_REVIEW/full（claude/claude-opus-5-5）。max_cycles默认3；FINAL_REVIEW 中任何 ISSUE 都算失败，修复后必须先 RE_REVIEW 再 FINAL_REVIEW。每条按整句核对，不只改被点名处。LuaJIT全记录比较恰4个target变动；strict lint/claims、diff check、完整门禁/构建、DONE_VERIFIED。译文commit→queue→单次catalog/migration→证据发布commit→queue→push，然后继续审核265。

范围约束（每条都逐句对照原文，发现明显增删一并修正，不重写已忠实的句子）：
- “#Target# is being crushed.”（timed_effects/physical.lua:1501 CRUSHING_HOLD、1876 IMPLODING 的 on_gain，持续挤压，配对 on_lose 为挣脱）：改为“#Target#正被碾压。”一类进行态；#Target# 保持。
- 队友行为菜单 Standby（dialogs/orders/Behavior.lua:61；同族 Default/Melee/Ranged/Tank=默认/近战/远程/肉盾；选中后日志用 _t(item.set)，engine.lua standby=待命）：改为“待命”。
- Offhand Jab 说明（talents/techniques/dualweapon.lua:205，tformat）：首句写出以出其不意的徒手攻击替代通常的副手攻击（with a quick shift of your momentum / surprise / in place of your normal offhand attack）；第二行“This allows you to attack…”与“If the unarmed attack hits…”在同一行（原文 2 个 LF，行首 \t\t 保持），%d 顺序：主手伤害、徒手伤害、混乱强度、回合；“The chance to confuse increases with your Accuracy”保持含义。
- Z’quikzshl 日记（lore/misc.lua:768–778）：The other ingredients were trivial and in possession of my master = 其余材料都不难弄到，而且主人手里就有；最后一句 all he can manage is a corruption of his own name: Z’quikzshl = 他能挤出来的只有自己名字走了样的读音：兹基克茨（沿用本库 Z’quikzshl=兹基克茨）；同句代词统一为“他”（原文均 He）；Ruby of Eldoral 补出“红宝石”（Eldoral 沿用本库“艾德瑞尔”）；#{italic}#/#{bold}#/#{normal}# 与所有换行保持；其余逐句对照，只修明显错漏。

## f36a77c67030a4ae4a985497a95f1efd368e8e9b5215ff60a484473f5c279299

section: mod-tome/data/timed_effects/physical.lua
source_tag: _t

source: #Target# is being crushed.

target: #Target#被击碎。

确认依据：timed_effects/physical.lua:1501 CRUSHING_HOLD（grapple，long_desc 每回合受 %d 伤害）与 1876 IMPLODING（缓慢+每回合碾压伤害）的 on_gain 共用该消息，表示正在持续受压；现译“被击碎”表示已被打碎（完成态、毁坏），与持续挤压效果不符。改为“#Target#正被碾压。”。
与 surface 同向：physical.lua:1501/1876 CRUSHING_HOLD 与 IMPLODING 的 on_gain，持续挤压状态（配对 on_lose 为挣脱/摆脱），“被击碎”误述为已毁坏，改“正被碾压”。

## f3756e2f2d7f9cf289f5d069c1921b1c338a6f919c993b75ae50ed92f8b46de7

section: mod-tome/dialogs/orders/Behavior.lua
source_tag: _t

source: Standby

target: 乖乖站好

确认依据：dialogs/orders/Behavior.lua:57–61 队友行为菜单 Default/Melee/Ranged/Tank/Standby，同族现译 默认/近战/远程/肉盾；选中后 game.logPlayer 以 _t(item.set) 记录，engine.lua:98 standby=待命。菜单项“乖乖站好”与同族术语风格及选择后的日志“待命”不一致（resolvers.lua:947 standby 战术即原地待命）。改为“待命”。

## f3bf7c41d4567349f7f4e239a7d8a6af82f2c66ffa2bcd12f5b5db4e73fa1ecf

section: mod-tome/data/talents/techniques/dualweapon.lua
source_tag: tformat

source: With a quick shift of your momentum, you execute a surprise unarmed strike in place of your normal offhand attack.
		This allows you to attack with your mainhand weapon for %d%% damage and unarmed for %d%% damage.  If the unarmed attack hits, the target is confused (%d%% power) for %d turns.
		The chance to confuse increases with your Accuracy.

target: 你迅速移动，用徒手攻击敌人。
		造成 %d%% 主手武器伤害，%d%% 徒手伤害。
		若徒手攻击命中，敌人将被混乱（%d%% 强度）%d 回合。
		混乱几率受命中加成。

确认依据：talents/techniques/dualweapon.lua:176–205 Offhand Jab：action 先主手 attackTargetWith，再以 barehand 徒手攻击，不使用副手武器；info 原文 in place of your normal offhand attack 与 surprise 被删，现译未说明以徒手攻击替代副手攻击。另原文 2 个 LF，现译在“徒手伤害。”后插入第 3 个换行（一级换行不变量）。整条修复，LF 与原文一致。
与 surface 同向：dualweapon.lua:176–205 Offhand Jab 以徒手突袭替代副手常规攻击（action 仅主手+barehand），现译删去替代关系与 surprise；并修正多出的第 3 个换行。

## f431fee2ffd961fecdeb4c05a240d52dc59c1201ea6d081aa237d22dcb21c418

section: mod-tome/data/lore/misc.lua
source_tag: _t

source: #{italic}#(The handwriting of this diary entry is poor at best. Whoever wrote this was in poor health.)

#{bold}#53rd Allure, Year 603 of the Age of Pyre#{normal}#

I have done it! My fool of a master said I was not ready for the rites of lichdom, that I would attract undue attention... what utter idiocy. Already I can feel the transformation taking place, and I am certain that this weakness will only be momentary. My master was foolish to leave the Grimoire of Mortality Transcended open and unattended! All I needed was a bone from a magical creature, and as luck would have it, I had found a skeletal corpse of a dragon not far from our tower. The other ingredients were trivial and in possession of my master... surely he will be astounded that I, Zilquick the Eternal, will have transcended mortality!

(Another entry is written beneath this one, in a much more elegant and controlled script.)

Zilquick the Eternal, hah! What an unbearable buffoon, and I am glad his pride was his undoing. The young fool used up the Ruby of Eldoral in creating his phylactery, however; I must acquire a new phylactery for myself. On the bright side, my incompetent apprentice did illustrate why a bone from a creature slain by my own hand is important: the dragon bone he chose had left to fester a mold infection, and the mold somehow infused itself with the bone's inherent magical properties, altering the magical composition of the spell. I do hope whoever finds this note shall kill this "lich" using the most painful means available, and shall deposit him someplace where he is sure to be found.
Oh, look. He is trying to harm me with spells, but all he can manage is a corruption of his own name: Z'quikzshl.

target: #{italic}#（这篇日记的字迹很差。写日记之人似乎健康状况不佳。）

#{bold}#烈火纪603年，厄流月53日#{normal}#

我完成了！我愚蠢的主人说我没有做巫妖的条件，我会引来不必要的关注……说什么蠢话。我已经感觉到了身上的变化，并且我确信这虚弱只是暂时的。我的主人竟然愚蠢到忘记合上《死亡转化禁书》！我需要的只是一根魔法生物的骨头，幸运的是，我在塔周围不远处找到了一具龙族的骨架。其他材料都太次，并且完全被主人所掌控……他肯定会震惊于我，不朽的兹基克，将会超越生死！

（这段文字下面还写着另一段记录，笔迹更加优雅工整。）

不朽的兹基克，哈！多么愚蠢的小丑。我很高兴他的骄傲最终毁掉了自己。然而讨厌的是，这个年轻的傻小子在制作他的命匣时用光了艾德瑞尔之石，所以我也必须为我自己做一只命匣。从好的一面来说，我那不成器的学徒从反面说明了为什么我们应该使用亲手杀死的生物的骨架作为死亡转化的道具：他所选择的那具龙骨正在发霉溃烂，并且附在上面的霉菌似乎利用了骨头内的魔法能量，改变了咒语的魔法组成。我真心希望任何发现这篇手稿的人能以最残忍的方式杀死这只“巫妖”并把他丢到一个肯定会被人找到的地方。
哦，看呐，它正在试图用法术攻击我，不过他所能做的只是拥有一个堕落的名字：兹基克茨。

确认依据：lore/misc.lua:768–778 Z’quikzshl 日记：The other ingredients were trivial and in possession of my master 意为其他材料易得且主人手中就有，现译“都太次，并且完全被主人所掌控”错译；末句 all he can manage is a corruption of his own name: Z’quikzshl 指他施法只能吐出自己名字的走样读音，现译“他所能做的只是拥有一个堕落的名字”错译；Ruby of Eldoral 现译“艾德瑞尔之石”丢失“红宝石”。整条修复，保留标记与换行。
与 surface 同向：lore/misc.lua:768–778 trivial 误译为“太次”、corruption of his own name 误译为“拥有一个堕落的名字”；另同句“它/他”混用（原文均 He）一并修正，Ruby of Eldoral 补“红宝石”。整条修复。
