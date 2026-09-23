# 修复窗口9（重跑 w9b）：255批5条确认问题

本任务取代 repair-w9-20260923（STOP_VERIFIED）。原任务内容已收敛（FINAL F3 5 OK/0 ISSUE，门禁17/17），但宿主在 FINAL_REVIEW 失败后直接进入下一轮 FINAL_REVIEW 而非 RE_REVIEW，v2 收敛结构无法通过 DONE 检查。本任务由唯一EXECUTOR逐字应用 .ai/task/repair-w9-20260923/FINAL-TARGETS.json 的5个最终 target，再按 REVIEW(0)/full→FINAL_REVIEW(1)/full 正确顺序独立复审；不再开任何修复轮，任一 confirmed finding 即交回用户。证据目录为 evidence/quality/repair-window-9-20260923/w9b/。

Paseo MCP / schema5 translation_contextual_v2 implement；基线c95647eb602b8a8dcb870422c84f4cb131b48c53。用户2026-09-23授权持续推进审核与修复、提交与推送，无需逐批确认；有争议条目记pending待用户集中审阅。本窗口因潜行说明的已确认机制缺陷提前修复。

唯一EXECUTOR仅修改mod-tome.lua中WORKSET的5个target及evidence/quality/repair-window-9-20260923/w9b/。不修改其他译文、术语库、规则、工具、旧证据；首次不修改handoff/catalog/migration；不stage/commit/push、不写.ai、不创建agent。保留既有无关未跟踪文件。

SOURCE-CLAIMS仅供实施，reviewer只读中性冻结输入和相关固定源码；不传宿主裁决。源码固定624a67329fe2ad440c5b344785a9c73fcf22ae63。source/source_tag/args_order/printf占位符/markup/TAB保持基线；LF除ea4c9e1c88须与原文一致（1个）外保持基线。

5条<4-lane阈值外但按契约选择full：REVIEW/full（codex/gpt-6-sol）与FINAL_REVIEW/full（claude/claude-opus-5-5），审核模型依用户2026-09-23指示。max_cycles默认3。LuaJIT全记录比较恰5个target变动；strict lint/claims、diff check、完整门禁/构建、DONE_VERIFIED。译文commit→queue→单次catalog/migration→证据发布commit→queue→push，然后继续审核256。

范围约束：高阶奇术师解锁文本只把Flame的“火球术”改为现行技能名“火焰”，寒冰箭等其余技能名不动；潜行说明只修“敌人在半径内”补足in sight（视野内/能看见你）及“技能”改为“行动”两处；runes active只改为体现“生效”；夏之眼只把“微光”改为明亮温暖的光；回归之杖描述修rod（魔杖/杖，不得用武器类“法杖”）、bend（扭曲）与raw（原始），物品名“回归之杖”不改。排除全部advisory（巫妖外观名、触手语气）、3条pending（yeek cunning、毒素风暴等概率、Matter is Energy）及其他已有blocked/repair。

## e9e627f60c131071a84d6a2ee2644e754f57692e5b2aa7f79b470b176e6e6968

section: mod-tome/data/texts/unlock-mage_thaumaturgist.lua
source_tag: _t

source: You have killed a boss by only using beam spells and nothing else, showing a deeper understanding of this type of spells.

You have unlocked the #LIGHT_GREEN#High Thaumaturgist class evolution#WHITE# for Archmages.

Features:
- #YELLOW#Wide Beams#WHITE#: Flame, Manathrust, Lightning, Pulverizing Auger and Ice Shards permanently become 3-wide beam spells.
- Access to the Thaumaturgy spell category containing the spells:
  - #YELLOW#Orb of Thaumaturgy#WHITE#: By placing a thaumaturgy orb on the ground you can duplicate all beam spells you cast.
  - #YELLOW#Multicaster#WHITE#: Casting beams becomes so easy for you that you can weave in random non-beam spells when you cast one.
  - #YELLOW#Slipstream#WHITE#: Flow through the battlefield with ease, when you cast a beam spell you can move one tile for free.
  - #YELLOW#Elemental Array Burst#WHITE#: The ultimate beam spell, the culmination of your deep understanding of magic. A 3-wide beam of pure thaumic energy that can never be resisted.


Class evolutions are selected as prodigies and grant new ways to build and expand your class and are only visible to the concerned class.


target: 你仅用射线法术、不使用其他技能杀死了一个boss，展示了你对这类法术的深入理解。

你解锁了元素法师的#LIGHT_GREEN#高阶奇术师#WHITE#职业进阶。

职业特性：
- #YELLOW#宽射线#WHITE#: 火球术，奥术射线，闪电术，粉碎钻击和寒冰箭永久成为宽度为3的射线技能。
- 获得奇术系技能，拥有以下能力：
  - #YELLOW#奇术之球#WHITE#: 在地上放置奇术之球，会复制你释放的射线类法术。
  - #YELLOW#多重施法#WHITE#: 你可以在释放射线类法术的同时交织释放随机非射线法术。
  - #YELLOW#能量滑流#WHITE#: 在战场上自由行动，当你使用射线类法术的时候可以不消耗回合移动一格。
  - #YELLOW#元素阵爆发#WHITE#: 终极射线法术，是你对魔法理解的精华。这一宽度为3的纯粹奇术能量永远无法被抵抗。


职业进阶是一种觉醒技，它们可以给予你新的方法来强化你的职业。只有相关的职业才能看到它们。


确认依据：spells/fire.lua:21 技能 Flame 的现行技能名译为“火焰”（mod-tome.lua talent name 行），高阶奇术师解锁文本写作“火球术”，与实际技能名不一致，确认为术语缺陷，改为“火焰”。同条 Ice Shards（water.lua:21）技能名现译即“寒冰箭”，与解锁文本一致，该部分驳回。

## ea047c36a0657e519501133b15798bef74ae09817c7773a8b199353147f7b53f

section: mod-tome/data/talents/cunning/stealth.lua
source_tag: tformat

source: Enters stealth mode (power %d, based on Cunning), making you harder to detect.
		If successful (re-checked each turn), enemies will not know exactly where you are, or may not notice you at all.
		Stealth reduces your light radius to 0, increases your infravision by 3, and will not work with heavy or massive armours.
		You cannot enter stealth if there are foes in sight within range %d%s.
		Any non-instant, non-movement action will break stealth if not otherwise specified.

		Enemies uncertain of your location will still make educated guesses at it.
		While stealthed, enemies cannot share information about your location with each other and will be delayed in telling their allies that you exist at all.

target: 进入潜行模式（潜行点数 %d，基于灵巧），让你更难被侦测到。
		如果成功（每回合都重新检查），敌人将不会知道你在哪里，或者根本不会注意到你。
		潜行将光照半径减小至 0，增加3点夜视能力，并且不能在装备重甲或板甲时使用。
		如果敌人在半径 %d %s 内，你不能进入潜行。
		除非特别说明，任何非瞬间非移动技能均会打破潜行。

		即使不知道你位置的敌人，仍然会猜测你可能在的位置。
		潜行时，敌人无法彼此分享有关你所在位置的信息，并且会延迟向盟友通报你的存在。

确认依据：潜行打破不限于技能：class/Actor.lua:6535 使用技能时 breakStealth，同时 interface/Combat.lua:121、258 攻击时、class/Object.lua:340 使用物品时也会打破潜行。原文 action 泛指行动，译文“技能”缩小了机制范围，确认修复为“行动”。
独立语境复核补充并经宿主核验：cunning/stealth.lua:24–36 stealthDetection 仅累计半径内敌对、未致盲且 act.fov.actors[self]（能看见你）的角色，原文 foes in sight within range 的 in sight 被译文“敌人在半径内”漏掉；action→技能的缩窄与 surface 键同一缺陷（Combat.lua:121/258、Object.lua:340 亦打破潜行）。确认整句有界修复两处。

## ea2d3aa57011e9743a3535843861954ee6eb75ef085b8d3ff18ff76f1e4cfa3a

section: mod-tome/data/talents/spells/necrosis.lua
source_tag: tformat

source: %d runes active

target: 有 %d 个符文

确认依据：spells/necrosis.lua:138 仅在 nb>0（无自然纹身、效果生效）时显示 ("%d runes active")，与另两分支“效果因……失效”对照。译文“有 %d 个符文”丢失“生效”这一对照要点，确认有界修复为“%d 个符文生效中”。

## ea36045fbab0929ca94dcd7a2f9dc421a790973db338e21d20c68b3e0ec38bfb

section: mod-tome/data/general/objects/world-artifacts.lua
source_tag: _t

source: This mindstar glows with a bright warm light, but seems somehow incomplete.

target: 这个灵晶散发着温暖的微光，但似乎有点残缺。

确认依据：general/objects/world-artifacts.lua:8068 灵晶描述 glows with a bright warm light；译文“温暖的微光”把 bright（明亮）反转为微弱，确认修复。
与 surface 键同一缺陷的独立语境复核：world-artifacts.lua:8068 bright warm light 被译作“微光”，语义相反，确认修复。

## ea4c9e1c8864a99ca4cc2ed45bc09fae542786feef2058485672125a1d8089da

section: mod-tome/data/general/objects/quest-artifacts.lua
source_tag: _t

source: This rod is made entirely of voratun, infused with raw magical energies that can bend space itself.
You have heard of such items before. They are very useful to adventurers, allowing faster travel.

target: 这个法杖通体用沃瑞钽打造，充满了可以撕裂空间的奥术能量。你以前曾听说过此类物品。它们对于冒险者的快速旅行非常有帮助。

确认依据：general/objects/quest-artifacts.lua:319 回归之杖描述 This rod…bend space itself。本库 rod 子类型译“魔杖”、物品名“回归之杖”，而“法杖”是 staff 武器类型的译名，译文“这个法杖”与物品类型冲突；bend（扭曲）被译成“撕裂”亦偏离。确认整句有界修复。
与 surface 键同一缺陷的独立语境复核：quest-artifacts.lua:319 bend space 被译作“撕裂空间”，raw magical energies 的“原始”亦未体现；与 surface 所指 rod→法杖 合并为整句有界修复。

## 最终 target 以 FINAL-TARGETS.json 为准

上文“范围约束”记录的是255批原始确认要点；原任务复审后另有裁决：解锁文本首句改为“不借助其他任何手段”且宽射线一行保持基线“火球术”（Flame 名称列 pending）、回归之杖恢复1个LF、潜行第二行与第六行保留 exactly/may/uncertain 限定。EXECUTOR 必须逐字应用 .ai/task/repair-w9-20260923/FINAL-TARGETS.json 中5个 final_target，不得自行改写。
