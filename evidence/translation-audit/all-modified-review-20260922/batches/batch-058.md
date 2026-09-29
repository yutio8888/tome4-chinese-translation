# batch-058：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-01706
位置：mod-tome.lua:23297；section：mod-tome/data/talents/cunning/called-shots.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your mastery of called shots is unparalleled. and you gain %d%% bonus critical chance and %d%% critical damage with your Called Shots Talents. At rank 3 the cooldowns of all of your Called Shots Talents are reduced by 2 each. At rank 5 you gain %d%% Physical resistance penetration with all Called Shot attacks.
```
译文：
```text
你对射击的掌握程度无与伦比。你的精准射击系技能获得 %d%% 额外暴击几率和 %d%% 额外暴击伤害。
		在第 3 级时，所有精准射击系技能冷却时间降低两回合。
		在第 5 级时，你的精准射击技能获得 %d%% 物理抗性穿透。
```

## entry-01707
位置：mod-tome.lua:23306；section：mod-tome/data/talents/cunning/cunning.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Allows the user to enter stealth.
```
译文：
```text
使你的角色进入潜行。
```

## entry-01708
位置：mod-tome.lua:23308；section：mod-tome/data/talents/cunning/cunning.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The knowledge of trap laying and assorted trickeries.
```
译文：
```text
关于布设陷阱与各式诡计的知识。
```

## entry-01709
位置：mod-tome.lua:23310；section：mod-tome/data/talents/cunning/cunning.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Collection of known traps.
```
译文：
```text
学会制造各种功能的陷阱。
```

## entry-01710
位置：mod-tome.lua:23312；section：mod-tome/data/talents/cunning/cunning.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The knowledge of poisons and how to apply them to 'good' effects.
```
译文：
```text
关于毒物的知识，以及如何用它们取得“良好”的效果。
```

## entry-01711
位置：mod-tome.lua:23313；section：mod-tome/data/talents/cunning/cunning.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Collection of known poisons.
```
译文：
```text
制造各种不同毒素。
```

## entry-01712
位置：mod-tome.lua:23315；section：mod-tome/data/talents/cunning/cunning.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Teaches various talents to cripple your foes.
```
译文：
```text
使你学会令你目标致残的技能。
```

## entry-01713
位置：mod-tome.lua:23317；section：mod-tome/data/talents/cunning/cunning.lua；source_tag：_t；args_order：None；special：None

原文：
```text
How to make your foes feel the pain.
```
译文：
```text
让你的对手尝尝什么是真正的痛苦……
```

## entry-01714
位置：mod-tome.lua:23319；section：mod-tome/data/talents/cunning/cunning.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Blending magic and shadows.
```
译文：
```text
融合魔法与阴影。
```

## entry-01715
位置：mod-tome.lua:23323；section：mod-tome/data/talents/cunning/cunning.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The knowledge of the dangers of the world, and how to best avoid them.
```
译文：
```text
让你认识到世界中的各种危险，并学会如何有效避免它们。
```

## entry-01716
位置：mod-tome.lua:23325；section：mod-tome/data/talents/cunning/cunning.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Tactical combat abilities.
```
译文：
```text
战斗中使用的策略技巧。
```

## entry-01717
位置：mod-tome.lua:23327；section：mod-tome/data/talents/cunning/cunning.lua；source_tag：_t；args_order：None；special：None

原文：
```text
The use of ungentlemanly techniques.
```
译文：
```text
街头格斗中使用的卑劣技巧。
```

## entry-01718
位置：mod-tome.lua:23329；section：mod-tome/data/talents/cunning/cunning.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Create and use cunning tools.
```
译文：
```text
制造并使用工具。
```

## entry-01719
位置：mod-tome.lua:23333；section：mod-tome/data/talents/cunning/cunning.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Inflict maximum pain to specific places on your enemies.
```
译文：
```text
对敌人身上的特定部位施加极致的痛苦。
```

## entry-01720
位置：mod-tome.lua:23340；section：mod-tome/data/talents/cunning/dirty.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You make a low blow against a sensitive point on the target, dealing %d%% unarmed damage. If your attack hits, the target is left reeling and vulnerable, reducing their physical save by %d and their stun, blind, confusion and pin immunities to 50%% of normal for %d turns.
This effect bypasses saves.
```
译文：
```text
你攻击目标的敏感部位，造成 %d%% 徒手伤害。如果攻击命中，目标身受重创，物理豁免减少 %d，震慑、致盲、混乱、定身免疫降低为原来的 50%%，持续 %d 回合。
该效果无视豁免。
```

## entry-01721
位置：mod-tome.lua:23352；section：mod-tome/data/talents/cunning/dirty.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Throw a cloud of blinding dust in a radius %d cone. Enemies within will be blinded, as well as having their accuracy reduced by %d and movement speed decreased by %d%% for %d turns.
		The chance to inflict these effects increase with your Accuracy.
```
译文：
```text
撒出致盲粉，致盲前方 %d 格锥形范围内的敌人。受影响的敌人命中减少 %d，移动速度减少 %d%%，持续 %d 回合。
		效果成功率受命中加成。
```

## entry-01722
位置：mod-tome.lua:23356；section：mod-tome/data/talents/cunning/dirty.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#CRIMSON#%s's %s was extended!#LAST#
```
译文：
```text
#CRIMSON#%s的%s被延长了！#LAST#
```

## entry-01723
位置：mod-tome.lua:23357；section：mod-tome/data/talents/cunning/dirty.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#CRIMSON#%s's %s was stripped!#LAST#
```
译文：
```text
#CRIMSON#%s的%s被解除了！#LAST#
```

## entry-01724
位置：mod-tome.lua:23358；section：mod-tome/data/talents/cunning/dirty.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#CRIMSON#%s's %s was disrupted!#LAST#
```
译文：
```text
#CRIMSON#%s的%s被干扰了！#LAST#
```

## entry-01725
位置：mod-tome.lua:23387；section：mod-tome/data/talents/cunning/poisons.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the vile poison!
```
译文：
```text
%s抵抗了邪恶毒素！
```

## entry-01726
位置：mod-tome.lua:23427；section：mod-tome/data/talents/cunning/poisons.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You strike your target with your melee or ranged weapon, doing %d%% weapon damage as nature and inflicting additional effects based on your active vile poisons:
		
		%s
		Learning this talent in addition to the Throwing Knives talent allows you to learn the Venomous Throw talent, which can be used to throw poisoned daggers at your foes, but is put on cooldown when this talent is used.
		
```
译文：
```text
使用近战或远程武器攻击目标，造成相当于 %d%% 武器伤害的自然伤害，并根据你当前激活的邪恶毒素附加额外效果：

		%s
		同时学会本技能和飞刀投掷技能后，你可以学会剧毒飞刀技能，用淬毒匕首攻击敌人；使用本技能时，剧毒飞刀也会进入冷却。
		
```

## entry-01727
位置：mod-tome.lua:23437；section：mod-tome/data/talents/cunning/poisons.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Enhances your Deadly Poison with a numbing agent, causing the poison to reduce all damage the target deals by %d%%.
```
译文：
```text
为你的致命剧毒加入麻痹成分，使该毒素令目标造成的所有伤害降低 %d%%。
```

## entry-01728
位置：mod-tome.lua:23439；section：mod-tome/data/talents/cunning/poisons.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Enhances your Deadly Poison with an insidious agent, causing it to reduce the healing taken by enemies by %d%%.
```
译文：
```text
以阴险成分强化你的致命毒素，中毒目标受到的治疗效果减少 %d%%。
```

## entry-01729
位置：mod-tome.lua:23441；section：mod-tome/data/talents/cunning/poisons.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Enhances your Deadly Poison with a crippling agent, giving enemies a %d%% chance on using a talent to fail and lose a turn.
```
译文：
```text
以致残成分强化你的致命毒素，中毒目标每次使用技能都有 %d%% 概率失败并流失 1 回合时间。
```

## entry-01730
位置：mod-tome.lua:23443；section：mod-tome/data/talents/cunning/poisons.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Enhances your Deadly Poison with a leeching agent, causing it to heal you for %d%% of the damage it does to its target.
```
译文：
```text
以吸血成分强化你的致命毒素，使其对目标造成的伤害按 %d%% 转化为对你的治疗。
```

## entry-01731
位置：mod-tome.lua:23445；section：mod-tome/data/talents/cunning/poisons.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Enhances your Deadly Poison with a volatile agent, causing the poison to deal %d%% increased damage to the victim and damage all of your enemies adjacent to it for 50%%.
```
译文：
```text
用易爆制剂强化你的致命毒素，使毒素对中毒者造成额外 %d%% 伤害，并以中毒目标为中心对其相邻的所有敌人造成毒素伤害的 50%%。
```

## entry-01732
位置：mod-tome.lua:23449；section：mod-tome/data/talents/cunning/poisons.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Enhance your Deadly Poison with a stoning agent.  Whenever you apply Deadly Poison, you afflict your target with an additional earth-based poison that inflicts %d nature damage per turn (stacking up to %d damage per turn) for %d turns.
		After either %d turns or the poison has run its course (<100%% chance, see effect description), the target will be turned to stone for %d turns.
		The damage scales with your Cunning.
```
译文：
```text
在你的武器上涂上石化毒素，额外造成每轮 %d 点自然伤害（可叠加至 %d），持续 %d 回合。
		%d 回合后或者毒素效果结束后（几率小于100%%，请参见效果介绍），目标将被石化 %d 回合。
		受灵巧影响，伤害按比例加成。
```

## entry-01733
位置：mod-tome.lua:23462；section：mod-tome/data/talents/cunning/scoundrel.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your melee and ranged attacks inflict distracting wounds that reduce the target’s critical strike multiplier by %d%% for 5 turns. 
In addition, your attacks have a %d%% chance to inflict a painful wound that causes them to forget a random talent for %d turns.  The last effect cannot occur more than once per turn per target.
		
```
译文：
```text
你的近战和远程攻击制造的伤口会使敌人分心，使目标的暴击系数减少 %d%%，持续 5 回合。
		此外，你的攻击还有 %d%% 的几率造成痛苦的创伤，使敌人随机遗忘一项技能，持续 %d 回合。这一效果对每个目标每回合最多触发一次。
```

## entry-01734
位置：mod-tome.lua:23468；section：mod-tome/data/talents/cunning/scoundrel.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your abilities in sowing confusion and chaos have reached their peak.  Whenever a foe attempts to apply a detrimental physical effect to you, they have a %d%% chance to fail. If there is an adjacent enemy to you, you misdirect your foe into applying it to them at %d%% duration.
You gain %d defense.
The chance to apply status effects increases with your Accuracy and the Defense with your Cunning.
```
译文：
```text
你制造混乱的技巧已趋于巅峰。
		敌人试图对你施加物理负面状态时，有 %d%% 几率失败。此外，如果相邻格有敌人，这一效果将会被转移到这个敌人身上，持续时间变为 %d%%。
		你获得 %d 闪避。
		施加负面状态几率受命中影响。
		闪避加成受灵巧影响。
```

## entry-01735
位置：mod-tome.lua:23490；section：mod-tome/data/talents/cunning/shadow-magic.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Channel raw magical energy into your melee attacks; each blow you land will do an additional %.2f darkness damage.
		The damage will improve with your Spellpower.
```
译文：
```text
将原始的魔法能量灌注到你的近战攻击中，你每次成功命中都会额外造成 %.2f 暗影伤害。
		伤害受法术强度加成。
```

## entry-01736
位置：mod-tome.lua:23494；section：mod-tome/data/talents/cunning/shadow-magic.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your preparations give you greater magical capabilities. You gain a bonus to Spellpower equal to %d%% of your Cunning (Current bonus: %d).
```
译文：
```text
你的充分准备提高了你的魔法运用能力。增加相当于你 %d%% 灵巧的法术强度。目前的法术强度加成：%d。
```

## entry-01737
位置：mod-tome.lua:23503；section：mod-tome/data/talents/cunning/shadow-magic.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
You do not have line of sight.
```
译文：
```text
你没有视线。
```

## entry-01738
位置：mod-tome.lua:23504；section：mod-tome/data/talents/cunning/shadow-magic.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
The spell fizzles!
```
译文：
```text
法术失败了！
```

## entry-01739
位置：mod-tome.lua:23518；section：mod-tome/data/talents/cunning/stealth.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
 (range %d in an unlit grid)
```
译文：
```text
 (在黑暗地格范围为 %d)
```

## entry-01740
位置：mod-tome.lua:23519；section：mod-tome/data/talents/cunning/stealth.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Enters stealth mode (power %d, based on Cunning), making you harder to detect.
		If successful (re-checked each turn), enemies will not know exactly where you are, or may not notice you at all.
		Stealth reduces your light radius to 0, increases your infravision by 3, and will not work with heavy or massive armours.
		You cannot enter stealth if there are foes in sight within range %d%s.
		Any non-instant, non-movement action will break stealth if not otherwise specified.

		Enemies uncertain of your location will still make educated guesses at it.
		While stealthed, enemies cannot share information about your location with each other and will be delayed in telling their allies that you exist at all.
```
译文：
```text
进入潜行模式（潜行点数 %d，基于灵巧），让你更难被侦测到。
		如果成功（每回合都重新检查），敌人将不会知道你在哪里，或者根本不会注意到你。
		潜行将光照半径减小至 0，增加3点夜视能力，并且不能在装备重甲或板甲时使用。
		如果敌人在半径 %d %s 内，你不能进入潜行。
		除非特别说明，任何非瞬间非移动技能均会打破潜行。

		即使不知道你位置的敌人，仍然会猜测你可能在的位置。
		潜行时，敌人无法彼此分享有关你所在位置的信息，并且会延迟向盟友通报你的存在。
```

## entry-01741
位置：mod-tome.lua:23535；section：mod-tome/data/talents/cunning/stealth.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You know how to make the most out of being unseen.
		When striking from stealth, your attacks are automatically critical if the target does not notice you just before you land it.  (Spell and mind attacks critically strike even if the target notices you.)
		Your critical multiplier against targets that cannot see you is increased by up to %d%%. (You must be able to see your target and the bonus is reduced from its full value at range 3 to 0 at range 10.)
		Also, after exiting stealth for any reason, the critical multiplier persists for %d turns (with no range limitation).
```
译文：
```text
你充分发挥潜行优势。
		潜行状态下攻击时，如果直到命中前你的目标都没有发现你，你的攻击将自动暴击。（即使目标注意到你，你的法术和精神攻击也会暴击。）
		对于看不见你的目标，暴击伤害增加 %d%%。（你必须能够看到你的目标，并且伤害奖励随距离降低：3 格内保持满额，到 10 格时降低为 0）。
		此外，由于任何原因脱离潜行后，暴击伤害奖励会持续存在 %d 回合（不受范围限制）。
```

## entry-01742
位置：mod-tome.lua:23557；section：mod-tome/data/talents/cunning/survival.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You notice the small things others do not notice, allowing you to "see" creatures in a %d radius even outside of light radius.
		This is not telepathy, however, and it is still limited to line of sight.
		Also, your attention to detail increases stealth detection and invisibility detection by %d, and you gain the ability to detect traps (+%d detect 'power').
		The detection abilities improve with Cunning.
```
译文：
```text
你注意到他人注意不到的细节，甚至能在阴影区域“看到”怪物，%d 码半径范围。
		注意此能力不属于心灵感应，仍然受到视野的限制。
		同时你的细致观察使你侦察潜行和隐身的能力增加 %d，使你发现周围的陷阱的能力增加 %d。
		上述侦测能力均受灵巧加成。
```

## entry-01743
位置：mod-tome.lua:23573；section：mod-tome/data/talents/cunning/survival.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You have an enhanced sense of self preservation, and your keen intuition allows you to sense dangers others miss.
		Your ability to detect traps is enhanced (+%d detect 'power').
		Critical attacks against you have %0.1f%% reduced bonus damage, and damage bonuses attackers gain against you for being unseen are reduced by %d%%.
		You also gain an additional chance (at your normal save %+d, effective) to resist detrimental status effects that can be resisted.
		The detection and additional save chance improve with Cunning.
```
译文：
```text
你拥有了更高级的自我保护感知力，敏锐的直觉让你察觉到他人会忽略的危险。
		你感知陷阱的能力提升了（+%d 点侦察强度）。
		对你发动的暴击，其暴击加成伤害降低 %0.1f%%；攻击者因未被你看见而获得的伤害加成倍率减小 %d%%。
		你获得一次机会重新抵抗未成功抵抗的负面效果，豁免为正常豁免 %+d。
		侦测点数和豁免随灵巧提升。
```

## entry-01744
位置：mod-tome.lua:23587；section：mod-tome/data/talents/cunning/survival.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You search a nearby grid for a hidden trap (%d detection 'power') and disarm it if possible (%d disarm 'power', based on your skill with %s).
		Disarming a trap requires at least a minimum skill level, and you must be able to enter the trap's grid to manipulate it, though you stay in your current location.  A failed attempt to disarm a trap may trigger it.
		Your skill improves with your your Cunning.
```
译文：
```text
你搜索周围地格的陷阱（%d 侦察强度），并尝试解除 (%d 解除强度，基于技能 %s)。
		解除陷阱有最低技能等级需求，且你必须能够移动到陷阱的所在格，尽管你仍然留在你的当前位置。
		解除陷阱失败可能会触发陷阱。
		解除能力随灵巧值提升。
```

## entry-01745
位置：mod-tome.lua:23623；section：mod-tome/data/talents/cunning/traps.lua；source_tag：_t；args_order：None；special：None

原文：
```text
There is already a trap there.
```
译文：
```text
这里已经有一个陷阱了。
```

## 相关术语快照
```tsv
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Physical Save	物理豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Physical Save 行；与 Spell Save 法术豁免、Mental Save 精神豁免并列
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
armours	护甲	T.GAME.ENTITY	items	nil	existing	core	复数实体类别
blind	致盲	T.GAME.EFFECT	combat	effect subtype	existing	global	
blinding	致盲	T.GAME.DAMAGE	combat	damage type	existing	global	
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
confusion	混乱	T.GAME.EFFECT	combat	effect subtype	existing	core	
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
disarm	缴械	T.GAME.EFFECT	combat	effect subtype	existing	global	
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
poison	毒素	T.GAME.DAMAGE	combat	damage type	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
sense	感知	T.GAME.EFFECT	combat	effect subtype	existing	global	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
stone	石化	T.GAME.EFFECT	combat	_t	preferred	core	状态免疫面板 Stoning Resistance；与石化毒素（nature 伤害变体）同词根
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
tactic	战术	T.GAME.EFFECT	combat	effect subtype	existing	global	
tactical	战术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 tactic 同义的变体
technique	技巧	T.GAME.EFFECT	combat	effect subtype	preferred	dlc	Orcs 效果类别，近战与射击效果（STRAFING 等）共用；talent category 语境仍译“格斗”；P0 审核确认
technique	格斗	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
throwing knives	飞刀	T.GAME.ENTITY	items	talent type	preferred	core	灵巧系远程投掷武器类别；在技能说明中与普通匕首 knives 并列
throwing knives	飞刀	T.GAME.ENTITY	items	tformat	preferred	core	技能机制说明中的投掷匕首；沿用飞刀类别名
trap	陷阱	T.GAME.ENTITY	items	entity name	preferred	global	陷阱实体（20 处）
void	虚空	T.GAME.ENTITY	creatures	entity type	existing	global	
void	虚空	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Cults of Entropy 技能树/技能类别名
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wound	创伤	T.GAME.EFFECT	combat	effect subtype	existing	global	
```
