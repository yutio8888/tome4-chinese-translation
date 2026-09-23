# 修复窗口13：259批4条确认问题

Paseo MCP / schema5 translation_contextual_v2 implement；基线dd2b44df7db0ba069b6d750f88bd58669c8ab9fe。用户2026-09-23授权持续推进审核与修复、提交与推送，无需逐批确认；有争议条目记pending待用户集中审阅。按审核/修复1:1节奏开窗。

唯一EXECUTOR仅修改mod-tome.lua中WORKSET的4个target及evidence/quality/repair-window-13-20260923/。不修改其他译文、术语库、规则、工具、旧证据；首次不修改handoff/catalog/migration；不stage/commit/push、不写.ai、不创建agent。保留既有无关未跟踪文件。

SOURCE-CLAIMS仅供实施，reviewer只读中性冻结输入和相关固定源码；不传宿主裁决。源码固定624a67329fe2ad440c5b344785a9c73fcf22ae63。source/source_tag/args_order/printf占位符/markup/LF/TAB全部保持基线。

4条按契约选择full：REVIEW/full（codex/gpt-6-sol）与FINAL_REVIEW/full（claude/claude-opus-5-5）。max_cycles默认3；FINAL_REVIEW 若失败，修复后必须先 RE_REVIEW 再 FINAL_REVIEW。每条按整句核对，不只改被点名处。LuaJIT全记录比较恰4个target变动；strict lint/claims、diff check、完整门禁/构建、DONE_VERIFIED。译文commit→queue→单次catalog/migration→证据发布commit→queue→push，然后继续审核260。

范围约束：
- Self-Judgement 流血死亡信息（special_death_msg，拼在名字后）：well-deserved death 是“罪有应得的死”，不得写“死得其所”；如“因失血过多而死，罪有应得”一类，保持简短。
- Body of Stone 描述：transform your flesh into stone 为“化为石头”；you may not move, and any forced movement will end the effect 须保留 forced（强制位移才结束效果，Actor.lua:1486）；“Reduces the cooldown of … by %d%%” 为按百分比缩减冷却，不得写“回合数”；其余各行逐句对照，占位符数量与顺序、TAB 缩进与换行保持基线。
- 魔杖类型描述：made by powerful Alchemists and Archmagi to store spells——写明由强大的炼金术师和大法师制造、用于储存法术；Anybody can use them 为“任何人都可以用它释放其中的法术”一类。
- Crushing Hold：global action speed 用术语“全局速度”（terminology/combat.tsv:137 preferred），如“降低目标 %d%% 全局速度”；首句补 apply to every grapple（每次抓取），保持 #RED# 标记，删去 #RED# 后多出的空格以对齐原文“#RED#Talent Level 1”（原文 #RED# 后无空格）；等级行用“技能等级 N”或维持既有“等级 N”均可，但三行一致。

## ee3d073a2c9024bf0a974df77795c89fc8e9977304e69ff347378004d95854d1

section: mod-tome/data/timed_effects/other.lua
source_tag: _t

source: died a well-deserved death by exsanguination

target: 因失血过多而死，死得其所

确认依据：timed_effects/other.lua:4184 Self-Judgement 流血致死的 special_death_msg：well-deserved death 意为“罪有应得的死”，译文“死得其所”（死得有价值）语义评价相反。改“因失血过多而死，罪有应得”一类；不涉及死亡描述词表的增添意象问题。

## ee646924bb32857001e8cb881dc72f6ba79c70b0712b0ea50699baa11ef6e159

section: mod-tome/data/talents/spells/stone.lua
source_tag: tformat

source: You root yourself into the earth, and transform your flesh into stone.  While this spell is sustained, you may not move, and any forced movement will end the effect.
		Your stone form and your affinity with the earth while the spell is active has the following effects:
		* Reduces the cooldown of Earthen Missiles, Pulverizing Auger, Earthquake, and Mudslide by %d%%.
		* Grants %d%% Fire Resistance, %d%% Lightning Resistance, %d%% Acid Resistance, and %d%% Stun Resistance.
		Resistances scale with your Spellpower.

target: 你将自己扎根于土壤并使你的肉体融入石头。
		当此技能被激活时你不能移动并且任何移动会打断此技能效果。
		当此技能激活时，受你的石化形态和土壤相关影响，会产生以下效果：
		* 减少岩石飞弹、粉碎钻击、地震和山崩地裂冷却时间回合数：%d%%
		* 获得 %d%% 火焰抗性，%d%% 闪电抗性，%d%% 酸性抗性和 %d%% 震慑抵抗。
		受法术强度影响，抗性按比例加成。

确认依据：talents/spells/stone.lua:79–132 Body of Stone：transform your flesh into stone 译成“融入石头”偏义；“Reduces the cooldown … by %d%%” 译为“冷却时间回合数：%d%%”把百分比缩减写成回合数（getCooldownReduction 为百分比，cd_recution=cdr*cooldown/100）。移动打断部分：never_move 下仅可能被强制移动，Actor.lua:1486 任一 moved 即关闭，译文“任何移动会打断”功能等价，但宜随整句修回“任何强制移动都会终止此效果”。整句修复。
与 surface 同向的独立语境复核：stone.lua activate 设 never_move，Actor.lua:1486 仅在实际发生移动（只能是强制位移）时 forceUseTalent 关闭 Body of Stone；译文删 forced 易让人以为尝试移动即结束。随整句修复（化为石头、强制位移、冷却缩减百分比）。

## ee7affcb576ec9570085b729563ced5da745a971dd3cbb42ce573f47cbc08f6f

section: mod-tome/data/general/objects/wands.lua
source_tag: _t

source: Magical wands are made by powerful Alchemists and Archmagi to store spells. Anybody can use them to release the spells.

target: 魔杖被炼金术师和大法师用来储存法术。任何人可以用它来释放储存的法术。

确认依据：general/objects/wands.lua:30 魔杖类型描述：made by powerful Alchemists and Archmagi to store spells，译文“被炼金术师和大法师用来储存法术”漏 made（制造者）与 powerful，改写为使用者，信息错位。改“魔杖由强大的炼金术师和大法师制造，用来储存法术。任何人都可以用它释放其中的法术。”一类。

## eea3b16de500ec86097d123eb5e29ef9d0214c71d34a8fd0f509c5db758a51ba

section: mod-tome/data/talents/techniques/grappling.lua
source_tag: tformat

source: Enhances your grapples with additional effects. All additional effects will apply to every grapple with no additional save or resist check.
		#RED#Talent Level 1:  Reduces physical power by %d
		Talent Level 3:  Silences
		Talent Level 5:  Reduces global action speed by %d%%

target: 增强你的抓取，获得额外效果，所有效果不需通过其他豁免或抵抗鉴定。
		#RED# 等级 1：减少 %d 物理强度
		等级 3：沉默
		等级 5：目标减速 %d%%

确认依据：techniques/grappling.lua:120–147 Crushing Hold：slow 经 startGrapple 合并为抓取附加效果，GRAPPLED 效果以 global_speed_add -eff.slow 实现（physical.lua:1475）；“Reduces global action speed” 译为“目标减速”丢失机制名，冻结术语 combat.tsv:137 global action speed=全局速度（preferred，tformat）。与 contextual 同向，宿主由 advisory 改判 confirmed 一级术语缺陷；随整句补“每次抓取”，并修 #RED# 后多余空格。
与 surface 同向：GRAPPLED 以 global_speed_add -eff.slow 实现（physical.lua:1475），冻结术语 combat.tsv:137 global action speed=全局速度（preferred）；“目标减速”丢机制名。改“降低目标 %d%% 全局速度”一类。
