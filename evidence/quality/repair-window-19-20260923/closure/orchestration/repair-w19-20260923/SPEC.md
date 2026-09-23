# 修复窗口19：265批4条确认问题

Paseo MCP / schema5 translation_contextual_v2 implement；基线e4a010965a779bce7f2a19c3bea0534abcad6ac1。用户2026-09-23授权持续推进审核与修复、提交与推送，无需逐批确认；有争议条目记pending待用户集中审阅。按审核/修复1:1节奏开窗。

唯一EXECUTOR仅修改mod-tome.lua中WORKSET的4个target及evidence/quality/repair-window-19-20260923/。不修改其他译文、术语库、规则、工具、旧证据；首次不修改handoff/catalog/migration；不stage/commit/push、不写.ai、不创建agent。保留既有无关未跟踪文件。

SOURCE-CLAIMS仅供实施，reviewer只读中性冻结输入和相关固定源码；不传宿主裁决。源码固定624a67329fe2ad440c5b344785a9c73fcf22ae63。source/source_tag/args_order/printf占位符/markup保持基线；LF/TAB 必须与原文逐处一致（念动弓第二行行首3个TAB；Burrow 第三行用 \n\t\t 不用空格）。专名、技能名沿用本库现有译名（先在mod-tome.lua查证），不自行新造。

4条按契约选择full：REVIEW/full（codex/gpt-6-sol）与FINAL_REVIEW/full（claude/claude-opus-5-5）。max_cycles默认3；FINAL_REVIEW 中任何 ISSUE 都算失败，修复后必须先 RE_REVIEW 再 FINAL_REVIEW。每条按整句核对，不只改被点名处。LuaJIT全记录比较恰4个target变动；strict lint/claims、diff check、完整门禁/构建、DONE_VERIFIED。译文commit→queue→单次catalog/migration→证据发布commit→queue→push，然后继续审核266。

范围约束（每条都逐句对照原文，发现明显增删一并修正，不重写已忠实的句子）：
- 念动弓说明（talents/psionic/psi-archery.lua:238–245，tformat）：It will automatically attack a target each turn for %d turns 写出“每回合”；uses Willpower in place of Strength and Cunning in place of Dexterity to determine attack and damage 写出“攻击与伤害”；第二行行首 3 个 TAB，其余行 2 个 TAB，与原文逐处一致。
- Burrow 说明（talents/gifts/sand-drake.lua:163–166，tformat）：四行均以 \n\t\t 分隔（现译第三行用了空格）；burrow into earthen walls 写出“土质墙壁”一类；%d 顺序保持。
- Nightshade 陷阱 short_info（talents/cunning/traps.lua:2210，tformat）：触发时施加震慑与中毒（EFF_STUNNED 与 EFF_POISONED 各 4 回合，中毒每回合 %0.1f 自然伤害）；写成“造成 %0.1f 自然伤害，并使目标震慑且中毒（每回合 %0.1f 自然伤害），持续 4 回合”一类，让 4 回合同时覆盖震慑与中毒。
- 野蛮种族记载（lore/misc.lua:497；本条是 mod-tome.lua 中 section "mod-tome/load.lua" 下的那一行，不是 lore/misc 段的那一行——两行 source 相同，游戏中后写覆盖，本行实际生效；只改 WORKSET 指定的这一行）：首句 No text would be complete without at least a brief note of… 为“任何著述都少不了对……的简要记述”；infest 为“肆虐/盘踞”；more advanced form of speech 为“更发达的言语能力”（不要写成速度，且不与后半句“移动迅速”重复）；towards the end of the Age of Pyre 写出“末期”；Records of them exist only from the last few hundred years 为“近几百年”；some become wreathed in flames, others release hideous acids or belching clouds of darkness 为“有的被火焰环绕，有的释放可怕的酸液或喷吐黑暗之云”。可参考同 source 的 lore/misc 段那一行（其较新译文已改正多数问题），但须逐句对照原文，不照搬其“更为敏捷的速度”增译。专名（科兹拉克、马提普、德斯镇、巨魔沼泽、岱卡拉、马基·埃亚尔、永恒精灵、黄昏纪、烈火纪）沿用本库现有译名。

## f4754d3cfb3fe41979a96ea2fa4fad855be7ec6539af94a434ed0dd221cc4ebe

section: mod-tome/data/talents/psionic/psi-archery.lua
source_tag: tformat

source: You temporarily set aside a part of you mind to direct your telekinetically-wielded bow. It will automatically attack a target each turn for %d turns.
			The telekinetically-wielded bow uses Willpower in place of Strength and Cunning in place of Dexterity to determine attack and damage.
		Combat stats:
		Accuracy: %d
		Damage: %d
		APR: %d
		Crit: %0.2f
		Speed: %0.2f

target: 你暂时分出一部分精神去控制念动之弓。它会在 %d 回合内自动攻击1个目标。
		念动弓使用意志和灵巧来代替力量和敏捷决定攻击。
		战斗属性：
		命中：%d
		伤害：%d
		护甲穿透：%d
		暴击率：%0.2f
		攻击速度：%0.2f

确认依据：talents/psionic/psi-archery.lua:238–245 念动弓说明：uses Willpower in place of Strength and Cunning in place of Dexterity to determine attack and damage，现译“决定攻击”漏“伤害”（info 同时显示 combatDamage）；另原文第二行行首为 3 个 TAB，现译为 2 个（一级 TAB 不变量）。整条修复，LF/TAB 与原文逐处一致。
与 surface 同向：psi-archery.lua:238–245 attack a target each turn for %d turns 与 to determine attack and damage；现译漏“每回合”（读作整个持续期只攻击一次）与“伤害”，并少一个行首 TAB。整条修复。

## f4d315f2149baa7490569bbc71b3f14c4931c490889ae1e8fb85eeed4c5c9b5d

section: mod-tome/data/talents/gifts/sand-drake.lua
source_tag: tformat

source: Allows you to burrow into earthen walls for %d turns.
		Your powerful digging abilities also allow you to exploit and smash through enemy defensive weaknesses; You ignore %d of target armor and %d%% of enemy physical damage resistance while this is in effect.
		At Talent Level 5, this talent can be used instantly, and the cooldown will reduce with levels.
		Each point in sand drake talents also increases your physical resistance by 0.5%%.

target: 允许你钻进墙里，持续 %d 回合。
		你强大的挖掘能力让你能挖掘敌人的防御弱点；处于该状态下时你获得 %d 护甲穿透和 %d%% 物理抗性穿透。
     在技能等级 5 时，这个技能变成瞬间。冷却时间随技能等级升高而降低。
		每点土龙系的天赋可以使你增加物理抗性 0.5%%。

确认依据：talents/gifts/sand-drake.lua:155–167 Burrow 说明：原文四行均以 \n\t\t 分隔，现译第三行为“\n”加 5 个空格（一级 TAB 不变量）；burrow into earthen walls 漏“土质”限定。整条修复。

## f5651a163a271ec1f85b8fa30f051438e433501110c1e640ad4d13df34e0e4b7

section: mod-tome/data/talents/cunning/traps.lua
source_tag: tformat

source: Deals %0.1f nature damage, stuns and poisons for %0.1f nature/turn for 4 turns.

target: 造成 %0.1f 自然伤害，震慑且每回合造成 %0.1f 自然伤害，持续4 回合。

确认依据：talents/cunning/traps.lua:2182–2211 Nightshade trap short_info：触发时分别 setEffect EFF_STUNNED（canBe stun）与 EFF_POISONED（canBe poison，power=dam/10）；现译“震慑且每回合造成自然伤害”丢失“中毒”状态（中毒免疫可抵挡，可被解毒），机制描述不全。整条修复。
与 surface 同向：traps.lua:2188–2193 分别施加 EFF_STUNNED 与 EFF_POISONED（各 4 回合，各自受 canBe 判定）；现译漏“中毒”，“持续4回合”也只修饰伤害。整条修复，写明震慑与中毒均持续 4 回合。

## f56e57b65f02b9e8ca224b62b093ab11cefa9d7101b3e9459ecc25a7437cf8b8

section: mod-tome/load.lua
source_tag: _t

source: No text would be complete without at least a brief note of some of the more brutish races which infest our world. These do not hold any civilised society of note, nor in general do they seem capable of any form of higher thought or culture, but they are still of interest to study for any who take delight in analysing beings of more primitive intellect.

 Trolls come in two main types - Kezrak and Moltep, or stone and forest trolls as they are colloquially known. Stone trolls infest many mountain chains to the north-east, and some have been known to wander further afield in search of food or to spread violence. They are generally over 8' high, with extremely pronounced muscular strength and a thick, solid hide which bears the appearance of coal or granite. Forest trolls are generally found in dense woods or swamps, with the Trollmire east of Derth being especially infamous. They have a more advanced form of speech than their mountain-dwelling cousins, and are known to move faster and wield more elaborate weapons, though their greenish hide is not as thick and their musculature less developed. All trolls have intensely fast metabolisms, capable of healing from grievous wounds within a matter of hours. At birth they measure just eight inches long, but within two years grow to full maturity, and rarely live beyond ten years old. They used to be considered little more than beasts, but towards the end of the Age of Pyre many were trained as fighters by the orcs, and were even taught the basics of language and certain battle tactics, making them much more dangerous. Though the orcs are gone their servants remain, and their remote breeding areas and intense birth rates have so far scampered attempts to eradicate them completely.

 Giants live mostly around the mountainous peaks surrounding the Daikara Pass. They vary greatly in size, but are normally at least 10' tall. They look somewhat like large, deformed humans, with swollen or distended facial features and much longer, swinging limbs. They live in nomadic tribes, moving from peak to peak with the seasons, feeding on wild deer and goats. They are usually peaceful creatures, only turning violent when their territory is encroached or their young are threatened. There are sometimes reports of giants coming to lowlands and stealing farm animals or attacking communities, but these are rare and normally isolated to particularly harsh winters. Giants seem to have no developed culture or language worth mentioning, but have been noted to show interactions of limited intelligence and to commune well in groups.

 Nagas were once believed to be mere myth, but reliable reports and even the capturing of dead physical samples has shown them to be real creatures. The upper half of their body is humanoid in form, with blonde hair and an extremely thin build, but the lower half is like that of a giant snake's tail. They stand around 6' tall on land, though their tails extend several feet further. They have been encountered off the eastern and south-eastern coasts of Maj'Eyal, which seems to indicate some exotic civilisation beneath the waves. Records of them exist only from the last few hundred years, and only more recently have they been interpreted as more than just the wild fantasies of inebriated sailors. They can breathe in air and underwater, possessing both lungs and gills, and have been reported to move with surprising speed on the ground. One might think them simply odd monsters, but they decorate themselves in jewellry and craft weapons and armour from materials found on the sea-bed, such as supple mail formed from layers of thick shark-hide. This would suggest an advanced culture, but communication with them so far has proved impossible. It is not known if they are capable of complex speech, but to date their only response to those who encounter them has been extreme violence, and fishermen in the east are always wary of coming across these vicious creatures.

 The origin of Demons is not wholly known, but it is clear that they are capable of intelligence and so I feel the need to describe them somewhat here. It is known that they can be summoned by certain magical rites, and minor demons were oft in the employ of evil sorcerers during the Age of Dusk. The main theory, which is supported by certain studies by Shaloren archmages, seems to indicate that they come from another world than our own, with connections formed through intense arcane energies. It must be a truly terrifying place to host such foul denizens. Demons vary immensely in appearance and power, as much as the creatures of our own world vary. They generally have blueish blood and metallic flesh and skin, which can oft react oddly with our atmosphere - some become wreathed in flames, others release hideous acids or belching clouds of darkness. All seem versed in magical abilities to some degree, and the strongest of them possess truly terrifying powers. Luckily they are exceptionally rare, and seem to be much less common in modern times since magic has fallen out of use.

target: 没有任何文字可以诠释那些影响我们世界的野蛮种族。他们没有任何文化遗留，也没有任何先进的智慧或文化，但是他们仍能激起大家研究原始种族的兴趣。

 巨魔主要分为两大类——科兹拉克和马提普，或者说岩石和森林巨魔，因为这更加通俗地为人所知。岩石巨魔生存与东北部的山脉地区，有些为了寻找食物和散播暴力甚至走到了更远的地方。他们通常超过8英尺高，有着强壮的肌肉和厚厚的煤黑色或花岗岩状的外观。森林巨魔生活在浓密的森林和沼泽中，在德斯镇东部的巨魔沼泽尤为臭名卓著。他们比岩石巨魔同胞有着更为敏捷的速度，并且以移动迅速和能够使用精工武器闻名，尽管他们泛绿的外皮没有那么厚实，肌肉也不如岩石巨魔发达。所有的巨魔有着快速的新陈代谢能力，再严重的伤口，恢复只要几个小时。据测量，他们在出生时只有8英寸长，但是在2年内他们就可以成长完全，并且很少有寿命超过10年的。他们一开始被认为仅比野兽好一点，然而在烈火纪时，他们被兽人当做战士般训练，甚至学习了一些基础语言和战术，使得他们更加危险。虽然兽人已经走了，但他们的仆人仍然存在，并且他们偏远的繁殖地和极高的出生率至今仍挫败着彻底根除他们的企图。

 巨人们通常住在岱卡拉周围的山峦中。他们在体型上有着很大的差异，但基本上不会低于10英尺高。他们看起来就像是具有浮肿面部特征和更长的四肢的放大人类。他们属于游牧部落，随着季节的变化，从一个山头迁移到另一个山头，以鹿和羊为食。他们通常是和善的生物，只有当他们的领土受到入侵或者他们的后辈受到威胁时才会变的具有攻击性。有报道称，巨人们有时会从山上下来，抢夺牧场的家畜或者攻击市民，但是这极其少见并且大多发生在极端的严冬。巨人们似乎没有值得一提的优越文化和语言，但是却向我们揭示了有限智慧的运用和团结一致的精神。

 娜迦曾被认为仅存于神话中，但是据可靠消息以及死亡的标本表明他们是真实存在的。他们的上半身是人形，有着金色的头发和苗条的身段，但是下半身却极像一只巨蛇的尾巴。他们大约身高6英尺，尽管他们的尾巴可能更长。他们在马基·埃亚尔的东岸和东南岸都有踪迹，这似乎表明波涛之下存在着某种异域文明。有关他们的记载只有近一百年的，并且越来越多的证据表明他们并不是喝醉水手们的幻觉。他们可以在水里和陆地上呼吸，同时拥有肺和鳃，并且据说在陆地上有着非常惊人的速度。有人可能认为它们只是特殊的怪物，但是他们会用海底找到的材料做成珠宝和武器装备自己，例如用鲨鱼皮制成的柔软锁甲。这表明了一种先进的文明，但是截至目前为止我们发现与他们沟通几乎是不可能的。现在还不知道他们是否有复杂的语言，但是他们目前的对外回复只是极端的暴力，并且东海的渔民们经常要提防碰上这些邪恶的生物。

 恶魔的起源尚未完全清楚，但是很显然他们具有某种智慧，所以我觉得有必要在此写下一段。众所周知，他们是由某种魔法仪式召唤而来，并且在黄昏纪时期，小恶魔们经常受雇于邪恶的巫师。最主要的理论，由永恒精灵魔导师们得出的，恶魔们似乎来自另一个世界，一个通过强烈的奥术能量与我们相连的世界。那必然是一个地狱般的地方才能容下如此多恐怖的生物。恶魔们在外观和能力上不尽相同，正如我们世界里的生物一样。他们通常有偏蓝的血液和金属化的血肉，可以表现出超乎我们想象的形态——有些绽放在火焰中，有的藏在酸雾里或是可怕的黑暗中。他们似乎都在某种程度上通晓魔法，并且他们之中最强者具有真正可怕的力量。幸运的是他们是非常罕见的种族，而且自从魔法淡出人们的视野后，出现的更加稀少了。

确认依据：lore/misc.lua:497 野蛮种族记载；该行位于 mod-tome.lua:43247 的 section "mod-tome/load.lua"（冻结 MISS：load.lua 无此串），但 I18N.lua:100–101/141–143 section 在游戏中不生效、t() 按 src+tag 后写覆盖，故此行覆盖 18126 行（lore/misc 段）成为实际生效译文。现译多处错误：首句误作“没有任何文字可以诠释”、infest 误作“影响”；more advanced form of speech 误作“更为敏捷的速度”；Records … only from the last few hundred years 误作“近一百年”；release hideous acids or belching clouds of darkness 误作“藏在酸雾里或黑暗中”。整条逐句修复（可参照 18126 行较新的译文，但须按原文核对，不照搬其“更为敏捷的速度”增译）。
与 surface 同向，并补充：towards the end of the Age of Pyre 现译“在烈火纪时”漏“末期”。连同首句、speech、few hundred years、demons release acids/darkness 一并整条逐句修复。
