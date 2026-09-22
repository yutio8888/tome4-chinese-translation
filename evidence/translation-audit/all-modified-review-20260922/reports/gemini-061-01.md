# batch-061 译文复核报告

- **工作区**：`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921`
- **复核批次**：`evidence/translation-audit/all-modified-review-20260922/batches/batch-061.md`
- **批次文件 SHA-256 核验**：`45748343b37b4e5e2822fde6fbd4cfbdc9285bba87b59858d603b3599947df12`（核验通过）
- **覆盖条目**：`entry-01826` 至 `entry-01865`（共 40 条，逐条全量覆盖）
- **源码依据**：根据 `source-access.json`，本批全部条目均归属于 `mod-tome`，已通过 `git show` 对固定 Commit `624a67329fe2ad440c5b344785a9c73fcf22ae63:game/modules/tome/` 进行逐行核验；译文比对依据为 Commit `7c38a53b88a1c80d7d9b209f84c518ae9f6eac00:mod-tome.lua` 的上下文。

---

### entry-01826
- **位置**：`mod-tome.lua:24404`（`mod-tome/data/talents/cursed/punishments.lua`）
- **原文**：`Madness`
- **译文**：`疯狂`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/cursed/punishments.lua:311` 技能名定义为 `Madness`，译名与术语表（`madness -> 疯狂`）及游戏内 Cursed 惩罚系技能树一致，无占位符或特殊格式。

---

### entry-01827
- **位置**：`mod-tome.lua:24422`（`mod-tome/data/talents/cursed/rampage.lua`）
- **原文**：
  ```text
  You attack with mindless brutality. The first critical hit inflicted while rampaging increases the rampage duration by 1.
  		Rampage Bonus: Your physical damage increases by %d%%.
  		Rampage Bonus: Your Physical Save increases by %d and Mental Save increases by %d.
  ```
- **译文**：
  ```text
  使你的暴走更加无情，暴走状态下的第一次暴击可延长暴走效果 1 回合。
  		暴走加成：你的物理伤害增加 %d%%。
  		暴走加成：你的物理豁免增加 %d，精神豁免增加 %d。
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/cursed/rampage.lua:114` 格式化参数为 `tformat(physicalDamageChange, combatPhysResistChange, combatMentalResistChange)`。占位符 `%d%%`、`%d`、`%d` 数量及顺序与原文完全对应；缩进与制表符对齐；属性名词 `Physical Save`（物理豁免）、`Mental Save`（精神豁免）与术语库一致。首句“使你的暴走更加无情”对应技能名 `Brutality`（无情），语意流畅准确。

---

### entry-01828
- **位置**：`mod-tome.lua:24435`（`mod-tome/data/talents/cursed/rampage.lua`）
- **原文**：`#F53CBE#%s slams %s!`
- **译文**：`#F53CBE#%s 猛击了 %s！`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/cursed/rampage.lua:193` 调用 `game.logSeen(self, "#F53CBE#%s slams %s!", self:getName():capitalize(), target:getName())`，颜色标记 `#F53CBE#` 保持完整，参数顺序（攻击者、受击者）与动作逻辑完全一致。

---

### entry-01829
- **位置**：`mod-tome.lua:24437`（`mod-tome/data/talents/cursed/rampage.lua`）
- **原文**：`#F53CBE#Your rampage is invigorated by the collosal slam! (+1 duration)`
- **译文**：`#F53CBE#巨力猛击激发了你的暴走！（+1 持续时间）`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/cursed/rampage.lua:206` 调用 `game.logPlayer`，原文包含代码作者拼写笔误（`collosal`），译文正确转译其机制语义，颜色标记 `#F53CBE#` 及括号符号对齐保留。

---

### entry-01830
- **位置**：`mod-tome.lua:24447`（`mod-tome/data/talents/cursed/self-hatred.lua`）
- **原文**：
  ```text
  At the start of each turn, if you're bleeding, you gain %d hate.

  You can activate this talent to use your own life for power, bleeding yourself for a small portion of your maximum life (%0.2f damage) over the next 5 turns. This bleed cannot be resisted or removed, but can be reduced by Bloodstained.
  ```
- **译文**：
  ```text
  每回合开始时，如果你正在流血，你获得 %d 仇恨。

  你可以主动使用此技能，使用你的生命值换取力量，使你在5回合里受到最大生命值一小部分的流血伤害（%0.2f 伤害）。此流血效果不能被抵抗，无法被移除，但可以被血染系技能减少。
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/cursed/self-hatred.lua:60` 格式化参数为 `tformat(regen, damage)`，占位符 `%d` 与 `%0.2f` 正确对应；空行分段完整保留；末句 `Bloodstained` 经源码验证为技能树类别 `cursed/bloodstained`（其被动机制为每级减少 2% 流血伤害），译文译作“被血染系技能减少”符合实际机制；资源词 `hate`（仇恨）与术语一致。

---

### entry-01831
- **位置**：`mod-tome.lua:24473`（`mod-tome/data/talents/cursed/self-hatred.lua`）
- **原文**：`Self-Judgement`
- **译文**：`自我审判`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/cursed/self-hatred.lua:167` 定义技能名 `Self-Judgement`，译名准确规范。

---

### entry-01832
- **位置**：`mod-tome.lua:24474`（`mod-tome/data/talents/cursed/self-hatred.lua`）
- **原文**：`#CRIMSON##Target# suffers from %s from #Source#, mitigating the blow!#LAST#.`
- **译文**：`#CRIMSON##Target# 承受了来自#Source#的 %s，降低了伤害！#LAST#。`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/cursed/self-hatred.lua:192` 调用 `src:logCombat(self, ..., is_attk and _t"an attack" or _t"damage")`，根据 `Combat.lua:2839`，调用方 `src` 为攻击源，首个参数 `self` 为受击目标。译文“#Target# 承受了来自#Source#的 %s”与战斗日志主客体一致，占位符 `%s` 及颜色标记 `#CRIMSON#`、`#LAST#` 保持完整。

---

### entry-01833
- **位置**：`mod-tome.lua:24478`（`mod-tome/data/talents/cursed/self-hatred.lua`）
- **原文**：
  ```text
  Any direct damage that exceeds %d%% of your maximum life has the excess damage converted to a shallow wound that bleeds over the next %d turns. This bleed cannot be resisted or removed, but can be reduced by Bloodstained. Extremely powerful hits (more than %d%% of your max life) are not fully converted.

  #{italic}#You can't just die. That would be too easy.#{normal}#
  ```
- **译文**：
  ```text
  任何超过你最大生命 %d%% 的直接伤害中的额外部分会变成一道浅表伤口，在接下来的 %d 回合中造成流血伤害。此流血效果不能被抵抗或去除，但强度可以被血染系技能降低。极其强力的攻击（超过 %d%% 最大生命）无法被完全转化。

  #{italic}#你不能就这么死了。这太轻松了。#{normal}#
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/cursed/self-hatred.lua:203` 格式化参数为 `tformat(threshold, time, failThreshold)`，占位符 `%d%%`、`%d`、`%d%%` 数量与顺序完全对应；字体样式标记 `#{italic}#` 与 `#{normal}#` 配对完整；“Bloodstained”译作“血染系技能”与机制契合。

---

### entry-01834
- **位置**：`mod-tome.lua:24509`（`mod-tome/data/talents/cursed/shadows.lua`）
- **原文**：`Your hate is too low to call another shadow!`
- **译文**：`你的仇恨值不足，无法召唤阴影！`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/cursed/shadows.lua:409` 玩家提示文本，资源词 `hate` 译为“仇恨值”，符合术语表 preferred 规则。

---

### entry-01835
- **位置**：`mod-tome.lua:24511`（`mod-tome/data/talents/cursed/shadows.lua`）
- **原文**：
  ```text
  While this ability is active, you will continually call up to %d level %d shadows to aid you in battle. Each shadow costs 5 hate to summon. Shadows are weak combatants that can: Use Arcane Reconstruction to heal themselves (level %d), Blindside their opponents (level %d), and Phase Door from place to place.
  		Shadows ignore %d%% of the damage dealt to them by their master.
  ```
- **译文**：
  ```text
  当此技能激活时，你可以召唤 %d 个等级 %d 的阴影帮助你战斗。每个阴影需消耗 5 点仇恨值召唤。
  		阴影是脆弱的战士，它们能够：使用奥术重组治疗自己（等级 %d），使用闪电突袭攻击敌人（等级 %d），使用相位之门进行传送。
  		阴影无视主人对它们造成的 %d%% 伤害。
  ```
- **复核结论**：细微观察
- **可核验依据**：源码 `game/modules/tome/data/talents/cursed/shadows.lua:459` 格式化参数为 `tformat(maxShadows, level, healLevel, blindsideLevel, avoid_master_damage)`，5 个占位符 `%d`、`%d`、`%d`、`%d`、`%d%%` 顺序完全一致；技能引用名 `Arcane Reconstruction`（奥术重组）、`Blindside`（闪电突袭，符合术语表 preferred 规则）、`Phase Door`（相位之门）准确。细微观察在于原文“continually call up to %d”译为“你可以召唤 %d 个”，省略了“continually”（持续/自动，该技能在激活后每 10 回合在后台自动补充阴影）和“up to”（至多，受 `getMaxShadows` 限制为最多 1~4 个），但基础数值及核心技能说明完整。

---

### entry-01836
- **位置**：`mod-tome.lua:24516`（`mod-tome/data/talents/cursed/shadows.lua`）
- **原文**：
  ```text
  Instill hate in your shadows, strengthening their attacks. They gain %d%% extra Accuracy and %d%% extra damage. The fury of their attacks gives them the ability to try to Dominate their foes, increasing all damage taken by that foe for 4 turns (level %d, %d%% chance at range 1). They also gain the ability to Fade when hit, avoiding all damage until their next turn (%d turn cooldown).
  ```
- **译文**：
  ```text
  将仇恨注入你的阴影，强化他们的攻击。他们获得 %d%% 额外命中和 %d%% 额外伤害加成。
  		他们疯狂的攻击可以令他们支配对手，提高被支配目标所受到的所有伤害 4 回合（等级 %d，%d%% 几率 1 码范围）。
  		它们同时拥有消隐的能力，免疫所有伤害直到下一回合开始（%d 回合冷却时间）。
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/cursed/shadows.lua:517` 格式化参数为 `tformat(combatAtk, incDamage, dominateLevel, dominateChance, fadeCooldown)`，5 个占位符 `%d%%`、`%d%%`、`%d`、`%d%%`、`%d` 顺序无误；技能名 `Dominate`（支配）、`Fade`（消隐，符合术语表）准确。

---

### entry-01837
- **位置**：`mod-tome.lua:24520`（`mod-tome/data/talents/cursed/shadows.lua`）
- **原文**：
  ```text
  Infuse magic into your shadows to give them fearsome spells. Your shadows receive a bonus of %d to their Spellpower.
  		Your shadows can strike adjacent foes with Lightning (level %d, %d%% chance at range 1).
  		At level 3 your shadows can sear their enemies from a distance with Flames (level %d, %d%% chance at range 2 to 6).
  		At level 5 when your shadows are struck down they will attempt to Reform, becoming whole again (50%% chance).
  ```
- **译文**：
  ```text
  灌输魔力给你的阴影使它们学会可怕的法术。你的阴影获得 %d 点法术强度加成。
  		你的阴影可以用闪电术攻击附近的目标（等级 %d，%d%% 几率 1 码范围）。
  		等级 3 时你的阴影可以远距离使用火焰术灼烧你的敌人（等级 %d，%d%% 几率 2 到 6 码范围）。
  		等级 5 时你的阴影在被击倒时有一定几率重组并重新加入战斗（50%% 几率）。
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/cursed/shadows.lua:589` 格式化参数为 `tformat(spellpowerChange, lightningLevel, closeAttackSpellChance, flamesLevel, farAttackSpellChance)`，占位符 `%d`、`%d`、`%d%%`、`%d`、`%d%%` 与转义字面量 `50%%` 顺序完全一致；技能词 `Spellpower`（法术强度）、`Lightning`（闪电术）、`Flames`（火焰术）、`Reform`（重组）均准确对齐。

---

### entry-01838
- **位置**：`mod-tome.lua:24528`（`mod-tome/data/talents/cursed/shadows.lua`）
- **原文**：`#PINK#The shadows converge on #Target#!`
- **译文**：`#PINK#阴影被集中至 #Target#！`
- **复核结论**：细微观察
- **可核验依据**：源码 `game/modules/tome/data/talents/cursed/shadows.lua:652` 处于 `Focus Shadows` 技能对敌对目标施放时的进攻分支（`self:reactionToward(target) < 0`），指令所有阴影集火目标。译文“#PINK#阴影被集中至 #Target#！”颜色标记完整；但与 entry-01839 结合比对可见，进攻分支与防守分支被套用了完全相同的译文（详见 entry-01839）。

---

### entry-01839
- **位置**：`mod-tome.lua:24530`（`mod-tome/data/talents/cursed/shadows.lua`）
- **原文**：`#PINK#The shadows form around #Target#!`
- **译文**：`#PINK#阴影被集中至 #Target#！`
- **复核结论**：存在疑点
- **可核验依据**：源码 `game/modules/tome/data/talents/cursed/shadows.lua:669` 处于 `Focus Shadows` 对友方或自身施放的防守分支（`defend the target`），逻辑为阴影在友方周围组成防线（`e.ai_state.shadow_wall = true`）。原文在此处使用 `form around #Target#!`（阴影在 #Target# 周围成形/环绕护卫），但当前译文直接重复套用了进攻分支 entry-01838 的“#PINK#阴影被集中至 #Target#！”，未能表达“form around”在目标周围筑起防线的防守语义，且导致游戏日志中进攻与防守两种状态文字混淆无法区分。

---

### entry-01840
- **位置**：`mod-tome.lua:24543`（`mod-tome/data/talents/cursed/slaughter.lua`）
- **原文**：
  ```text
  You slash wildly at your target for %d%% (at 0 Hate) to %d%% (at 100+ Hate) damage.
  		At level 3, any wound you inflict with this carries a part of your curse, reducing the effectiveness of healing by %d%% for %d turns. The effect will stack.
  		The damage multiplier increases with your Strength.

  		This talent will also attack with your shield, if you have one equipped.
  ```
- **译文**：
  ```text
  野蛮的削砍你的目标造成 %d%% （0仇恨）至 %d%% （100+仇恨）伤害。
  		等级 3 时攻击附带诅咒，降低目标治疗效果 %d%% 持续 %d 回合，效果可叠加。
  		伤害比例受力量值加成。

  		如果你装备了盾牌，这一技能也会用你的盾牌攻击。
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/cursed/slaughter.lua:73` 格式化参数为 `tformat(t.getDamageMultiplier(self, t, 0) * 100, t.getDamageMultiplier(self, t, 100) * 100, -healFactorChange * 100, woundDuration)`，4 个占位符 `%d%%`、`%d%%`、`%d%%`、`%d` 顺序对齐；段落结构、缩进一致；属性 `Strength`（力量值）、`Hate`（仇恨）对齐规范。

---

### entry-01841
- **位置**：`mod-tome.lua:24567`（`mod-tome/data/talents/cursed/slaughter.lua`）
- **原文**：`Charge through your opponents, attacking anyone near your path for %d%% (at 0 Hate) to %d%% (at 100+ Hate) damage. %s opponents may be knocked away from your path. You can attack a maximum of %d times, and can hit targets along your path more than once.`
- **译文**：`冲过你的目标，途经的所有目标受到 %d%% （0仇恨）至 %d%% （100+仇恨）伤害。%s 体型的目标会被你弹开。你最多可以攻击 %d 次，并且你对路径上的敌人可造成不止 1 次攻击。`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/cursed/slaughter.lua:273` 格式化参数为 `tformat(..., size, maxAttackCount)`，其中 `%s` 传入体型描述字符串（`Small` / `Medium-sized` / `Big`），译文中译为“%s 体型的目标”结构吻合；占位符 `%d%%`、`%d%%`、`%s`、`%d` 顺序完全一致。

---

### entry-01842
- **位置**：`mod-tome.lua:24570`（`mod-tome/data/talents/cursed/slaughter.lua`）
- **原文**：
  ```text
  While active, every swing of your weapon strikes strikes other adjacent enemies for %d%% (at 0 hate) to %d%% (at 100 hate) physical damage. The recklessness of your attacks brings you bad luck (luck -3).
  		Cleave, Repel and Surge cannot be active simultaneously, and activating one will place the others in cooldown.
  		Cleave will deal 25%% additional damage while using a two-handed weapon.
  		The Cleave damage increases with your Strength.
  ```
- **译文**：
  ```text
  激活时，你的每次武器攻击都会同时攻击其他相邻敌人，造成 %d%% （0 仇恨值）到 %d%% （100 仇恨值）的物理伤害。如此不顾一切的杀戮会带给你厄运（幸运 -3）。
  		分裂攻击、无所畏惧和杀意涌动不能同时开启，并且激活一个也会使另外两个进入冷却。
  		当使用双手武器时，分裂攻击会造成 25%% 的额外伤害。
  		分裂攻击伤害受力量值加成。
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/cursed/slaughter.lua:388` 格式化参数为 `tformat(t.getDamageMultiplier(...) * 100, t.getDamageMultiplier(...) * 100)`，占位符 `%d%%`、`%d%%` 与转义字面量 `25%%` 正确对应；三个姿态技能名称引用 `Cleave`（分裂攻击）、`Repel`（无所畏惧）、`Surge`（杀意涌动）与全局技能译名完全一致；原文连字笔误“strikes strikes”被通顺纠正。

---

### entry-01843
- **位置**：`mod-tome.lua:24590`（`mod-tome/data/talents/cursed/strife.lua`）
- **原文**：
  ```text
  Your preternatural senses aid you in your hunt for the next victim. You sense foes in a radius of %0.1f. You will always sense a stalked victim in a radius of 10.
  		Also increases stealth detection by %d and invisibility detection by %d.
  		Stealth and invisibility detection improves with your Willpower
  ```
- **译文**：
  ```text
  你的超自然感官能帮助你搜寻下一个猎物。
  		你能感觉到 %0.1f 码半径范围内的敌人。
  		在 10 码半径范围内你总能看见被追踪的目标。
  		同时增加你的侦测潜行等级 %d，侦测隐形等级 %d。
  		侦测强度受意志加成。
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/cursed/strife.lua:103` 格式化参数为 `tformat(range, sense, sense)`，占位符 `%0.1f`、`%d`、`%d` 顺序完全一致；侦测属性与意志（Willpower）术语无误；首句分行清晰。

---

### entry-01844
- **位置**：`mod-tome.lua:24604`（`mod-tome/data/talents/cursed/strife.lua`）
- **原文**：
  ```text
  Rather than hide from the onslaught, you face down every threat. While active you have a %d%% chance of repelling a melee attack. The recklessness of your defense brings you bad luck (Luck -3).
  		Cleave, Repel and Surge cannot be active simultaneously, and activating one will place the others in cooldown.
  		Repel chance increases with your Strength and by 20%% when equipped with a shield.
  ```
- **译文**：
  ```text
  在猛烈的攻击面前，你选择直面威胁而不是躲藏。
  		当技能激活时，你有 %d%% 概率抵挡一次近程攻击。不顾一切的防御会带给你厄运（-3幸运）。
  		分裂攻击，无所畏惧和杀意涌动不能同时开启，并且激活其中一个也会使另外两个进入冷却。
  		抵挡概率受力量加成。
  		装备盾牌时，抵挡概率增加 20%%。
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/cursed/strife.lua:420` 格式化参数为 `tformat(chance)`，占位符 `%d%%` 及字面量 `20%%` 对应无误；技能名 `Cleave`、`Repel`、`Surge` 译名与 entry-01842 严格统一。

---

### entry-01845
- **位置**：`mod-tome.lua:24628`（`mod-tome/data/talents/gifts/antimagic.lua`）
- **原文**：
  ```text
  You stand in the way of magical damage. That which does not kill you will make you stronger.
  		When you are hit by hostile non-physical, non-mind damage you gain %d%% resistance to that element for 7 turns.
  		At talent level 3, the bonus resistance may apply to 3 elements, refreshing the duration with each element added.
  		Additionally, each time you take non-physical, non-mind damage, your equilibrium will decrease and stamina increase by %0.2f.
  		The effects will increase with the greater of your Mindpower or Physical power and the bonus resistance can be a mental crit.
  ```
- **译文**：
  ```text
  你选择了站在魔法的对立面。那些未能杀死你的磨难将使你更加强大。
  		每次你从敌对目标那里受到一种非物理、非精神伤害时，你能增加 %d%% 对该类型伤害的抗性，持续 7 回合。
  		在技能等级 3 时，你可以获得对 3 种类型的抗性，每增加一种类型时都会刷新持续时间。
  		此外，每当你被非物理，非精神伤害击中时，你会降低 %0.2f 失衡值并增加等量体力值。
  		技能效果受精神或物理强度较高者加成，抗性加成效果可以触发精神暴击。
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/gifts/antimagic.lua:51` 格式化参数为 `tformat(resist, regen)`，占位符 `%d%%`、`%0.2f` 顺序与位置正确；资源术语 `equilibrium`（失衡值）、`stamina`（体力值）、`Mindpower`（精神强度）、`Physical power`（物理强度）及 `mental crit`（精神暴击）完全符合术语表。

---

### entry-01846
- **位置**：`mod-tome.lua:24639`（`mod-tome/data/talents/gifts/antimagic.lua`）
- **原文**：
  ```text
  Let out a burst of sound that silences for %d turns all those affected in a radius of %d.
  		Each turn for %d turns the effected area will cause %0.2f manaburn damage to all creatures inside.
  		For each creature silenced your equilibrium is reduced by %d (up to 5 times).
  		The damage and apply power will increase with the greater of your Mindpower or Physical power.

  		Learning this talent will let your Nature damage and penetration bonuses apply to all Manaburn damage regardless of source.
  ```
- **译文**：
  ```text
  发出一阵音爆，使范围内所有目标沉默 %d 回合，范围半径 %d 格。
  		接下来 %d 回合内，受影响区域中的所有生物每回合受到 %0.2f 法力燃烧伤害。
  		每沉默一个生物，你的失衡值降低 %d，最多触发 5 次。
  		伤害和效果强度受精神强度与物理强度中较高者加成。

  		学会这个技能，也会让你的自然伤害加成和伤害穿透属性，对所有法力燃烧伤害生效，不管这一伤害的来源是什么。
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/gifts/antimagic.lua:107` 格式化参数为 `tformat(t.getduration(self,t), rad, t.getFloorDuration(self,t), t.getDamage(self, t), t.getEquiRegen(self, t))`，5 个占位符 `%d`、`%d`、`%d`、`%0.2f`、`%d` 顺序完全一致；`manaburn`（法力燃烧）与 `equilibrium`（失衡值）等术语准确。

---

### entry-01847
- **位置**：`mod-tome.lua:24652`（`mod-tome/data/talents/gifts/antimagic.lua`）
- **原文**：
  ```text
  Surround yourself with a shield that will absorb at most %d non-physical, non-mind element damage per attack.
  		Each time damage is absorbed by the shield, your equilibrium increases by 1 for every 30 points of damage and a standard Equilibrium check is made. If the check fails, the shield will crumble and Antimagic Shield will go on cooldown.
  		The damage the shield can absorb will increase with your Mindpower or Physical power (whichever is greater).
  ```
- **译文**：
  ```text
  给你增加一个护盾，每次被攻击吸收最多 %d 点非物理、非精神元素伤害。
  		每当护盾吸收伤害时，都会按每 30 点伤害增加 1 点失衡值，并进行一次失衡值鉴定；若鉴定失败，则护盾会破碎且技能会进入冷却状态。
  		护盾的最大伤害吸收值受精神或物理强度较高者加成。
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/gifts/antimagic.lua:164` 格式化参数为 `tformat(t.getMax(self, t))`，占位符 `%d` 准确；机制描述（吸收伤害增加失衡值并做失衡值鉴定）与源码 `on_damage` 逻辑一致。

---

### entry-01848
- **位置**：`mod-tome.lua:24658`（`mod-tome/data/talents/gifts/antimagic.lua`）
- **原文**：
  ```text

  #GREEN#Antimagic Adept:  #LAST#4 magical sustains from the target will be removed.
  ```
- **译文**：
  ```text

  #GREEN#反魔专家：#LAST#你的奥术对撞技能还会从目标身上移除 4 个持续魔法技能。
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/gifts/antimagic.lua:209` 中 `is_adept` 为插值至 `Mana Clash`（奥术对撞）描述中的字串。前导换行符、颜色代码 `#GREEN#`、`#LAST#` 均对齐保留；译文结合插入宿主语境增补主语，语义清晰精准。

---

### entry-01849
- **位置**：`mod-tome.lua:24660`（`mod-tome/data/talents/gifts/antimagic.lua`）
- **原文**：
  ```text
  Drain %d mana, %d vim, %d positive and negative energies from your target, triggering a chain reaction that explodes in a burst of arcane damage.
  		The damage done is equal to 100%% of the mana drained, 200%% of the vim drained, or 400%% of the positive or negative energy drained, whichever is higher. This effect is called a manaburn.
  		The effect will increase with your Mindpower or Physical power (whichever is greater).
  		%s
  ```
- **译文**：
  ```text
  从目标身上吸收 %d 点法力，%d 点活力，%d 点正负能量，并触发一次链式反应，引发一次奥术对撞。
  		奥术对撞造成相当于 100%% 吸收的法力值或 200%% 吸收的活力值或 400%% 吸收的正负能量的伤害，按最高值计算（称为法力燃烧）。
  		效果受精神或物理强度较高者加成。
  		%s
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/gifts/antimagic.lua:215` 格式化参数为 `tformat(mana, vim, positive, is_adept)`，占位符 `%d`、`%d`、`%d`、`%s` 及转义字面量 `100%%`、`200%%`、`400%%` 对应无误；各资源名称（法力、活力、正负能量）与机制名称（奥术对撞、法力燃烧）翻译标准统一。

---

### entry-01850
- **位置**：`mod-tome.lua:24725`（`mod-tome/data/talents/gifts/cold-drake.lua`）
- **原文**：`@Source@ breathes ice!`
- **译文**：`@Source@呼出寒冰！`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/gifts/cold-drake.lua:217` 吐息战斗消息，标签 `@Source@` 保留完整，动词与伤害属性（ice 寒冰）翻译规范。

---

### entry-01851
- **位置**：`mod-tome.lua:24737`（`mod-tome/data/talents/gifts/corrosive-blades.lua`）
- **原文**：
  ```text
  Channel acid through your psiblades, extending their reach to create a beam doing %0.1f Acid damage (which can disarm them).
  		The damage increases with your Mindpower.
  ```
- **译文**：
  ```text
  在你的心灵利刃里充填酸性能量，延展攻击范围，形成一道射线，造成 %0.1f 点酸性缴械伤害。
  		伤害受精神强度加成。
  ```
- **复核结论**：细微观察
- **可核验依据**：源码 `game/modules/tome/data/talents/gifts/corrosive-blades.lua:48` 格式化参数为 `tformat(damDesc(self, DamageType.ACID, dam))`，占位符 `%0.1f` 一致；伤害受精神强度加成准确。细微观察在于原文为 `doing %0.1f Acid damage (which can disarm them)`（造成酸性伤害，可能缴械目标），译文浓缩为“造成 %0.1f 点酸性缴械伤害”；源码实际投射类型为 `DamageType.ACID_DISARM`，虽然浓缩但未造成机制歧义。

---

### entry-01852
- **位置**：`mod-tome.lua:24751`（`mod-tome/data/talents/gifts/corrosive-blades.lua`）
- **原文**：
  ```text
  You focus on a target zone of radius 2 to make up to %d corrosive seeds appear.
  		The first seed will appear at the center of the target zone, while others will appear at random spots.
  		Each seed lasts %d turns and will explode when a hostile creature walks over it, knocking the creature back and dealing %0.1f Acid damage within radius 1.
  		The damage will increase with your Mindpower.
  ```
- **译文**：
  ```text
  你集中精神于某块半径 2 的区域，制造至多 %d 个腐蚀之种。
  		第一个种子会产生于中心处，其他的会随机出现。
  		每个种子持续 %d 回合，当一个敌对生物走过腐蚀之种时，会在半径 1 的区域内引发一场爆炸，击退对方并造成 %0.1f 点酸性伤害。
  		伤害受精神强度加成。
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/gifts/corrosive-blades.lua:167` 格式化参数为 `tformat(nb, t.getDuration(self, t), damDesc(self, DamageType.ACID, dam))`，占位符 `%d`、`%d`、`%0.1f` 顺序与数量完全对应；机制说明与陷阱行为完全吻合。

---

### entry-01853
- **位置**：`mod-tome.lua:24759`（`mod-tome/data/talents/gifts/corrosive-blades.lua`）
- **原文**：
  ```text
  Surround yourself with natural forces, ignoring %d%% acid resistance of your targets.
  		In addition, the acid will nourish your bloated oozes, giving them an additional %0.1f life regeneration per turn.
  ```
- **译文**：
  ```text
  你的周围充满了自然力量，忽略目标 %d%% 的酸性伤害抗性。
  		同时酸性能量会治疗你的浮肿软泥怪，增加他们每回合 %0.1f 的生命回复。
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/gifts/corrosive-blades.lua:214` 格式化参数为 `tformat(ressistpen, regen)`，占位符 `%d%%` 与 `%0.1f` 对应准确；实体名称 `bloated oozes` 译为“浮肿软泥怪”，严格遵循术语表 preferred 规则（`bloated ooze -> 浮肿软泥怪`，不省略“软泥”）。

---

### entry-01854
- **位置**：`mod-tome.lua:24767`（`mod-tome/data/talents/gifts/dwarven-nature.lua`）
- **原文**：
  ```text
  Conjures %d missile-shaped rocks that you target individually at any target or targets in range.  Each missile deals %0.2f physical damage, and an additional %0.2f bleeding damage every turn for 5 turns.
  		At talent level 5, you can conjure one additional missile.
  		The damage will increase with your Spellpower.
  ```
- **译文**：
  ```text
  释放出 %d 个岩石飞弹，你可以为每个飞弹独立指定射程内的任意目标。每个飞弹造成 %0.2f 物理伤害和每回合 %0.2f 流血伤害，持续 5 回合。
  		在等级 5 时，你可以额外释放一个飞弹。
  		伤害受法术强度加成。
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/gifts/dwarven-nature.lua:67` 格式化参数为 `tformat(count, damDesc(self, DamageType.PHYSICAL, damage/2), damDesc(self, DamageType.PHYSICAL, damage/12))`，占位符 `%d`、`%0.2f`、`%0.2f` 数量与顺序完全对应；属性词 `Spellpower`（法术强度）符合术语表。

---

### entry-01855
- **位置**：`mod-tome.lua:24779`（`mod-tome/data/talents/gifts/dwarven-nature.lua`）
- **原文**：
  ```text
  Reach inside your dwarven core and summon your stone and crystaline halves to fight alongside you for %d turns.
  		Your Crystaline Half will attack your foes with earthen missiles.
  		Your Stone Half will taunt your foes to protect you.
  		This power can not be called upon while under the effect of Deeprock Form.
  		
  ```
- **译文**：
  ```text
  深入你的矮人血统，召唤岩石和水晶分身为你作战，持续 %d 回合。
  		水晶分身会使用岩石飞弹攻击敌人。
  		岩石分身会嘲讽敌人来保护你。
  		处于深岩形态时，该技能不能使用。
  		
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/gifts/dwarven-nature.lua:167` 格式化参数为 `tformat(t.getDuration(self, t))`，占位符 `%d` 对应无误；末尾空行与制表符缩进对齐完整；技能与实体名词（水晶分身、岩石分身、深岩形态）翻译规范一致。

---

### entry-01856
- **位置**：`mod-tome.lua:24819`（`mod-tome/data/talents/gifts/earthen-power.lua`）
- **原文**：
  ```text
  The first time you take damage each turn, you regenerate %d%% of the damage dealt as mana (up to a maximum of %0.2f) and %d%% as equilibrium (up to %0.2f).
  		Increases Physical Power by %d, increases damage done with shields by %d%%, and allows you to dual-wield shields.
  		Also, all of your melee attacks will perform a shield bash in addition to their normal effects.
  ```
- **译文**：
  ```text
  每回合第一次承受伤害时，你将 %d%% 的伤害转化为法力 (至多 %0.2f 点)，%d%% 的伤害转化为失衡值 (至多回复 %0.2f)。
  		增加物理强度 %d，增加盾牌伤害 %d%% , 并让你能够双持盾牌。
  		同时，你的近战攻击附带一次盾牌攻击。
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/gifts/earthen-power.lua:42` 格式化参数为 `tformat(100 * m, mm, 100 * e, em, damage, inc*100)`，6 个占位符 `%d%%`、`%0.2f`、`%d%%`、`%0.2f`、`%d`、`%d%%` 数量与顺序完全一致；术语 `Physical Power`（物理强度）、`mana`（法力）、`equilibrium`（失衡值）、`dual-wield shields`（双持盾牌）准确规范。

---

### entry-01857
- **位置**：`mod-tome.lua:24831`（`mod-tome/data/talents/gifts/earthen-power.lua`）
- **原文**：
  ```text
  Sharp shards of stone grow from your shields.
  		When you are hit in melee, you will get a free attack against the attacker with the shards doing %d%% shield damage (as Nature).
  		This effect can only happen once per turn and is not affected by counterstrike.
  ```
- **译文**：
  ```text
  尖锐的岩石碎片从盾牌生长出来。
  		每次你承受近战攻击时，你能利用这些碎片反击攻击者，造成 %d%% 自然盾牌伤害。
  		每回合只能反击一次，且不受反击（Counterstrike）状态影响。
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/gifts/earthen-power.lua:83` 格式化参数为 `tformat(self:combatTalentWeaponDamage(t, 0.4, 1) * 100)`，占位符 `%d%%` 正确对应；状态词 `counterstrike` 译为“反击（Counterstrike）”并带英文注记，准确消除与普通“反击”动作的歧义。

---

### entry-01858
- **位置**：`mod-tome.lua:24868`（`mod-tome/data/talents/gifts/earthen-vines.lua`）
- **原文**：
  ```text
  Merge with one of your stone vines, traversing it to emerge near an entangled creature (maximum range %d).
  		Merging with the stone is beneficial for you, healing %0.2f life (increases with Willpower).
  		This will not break Body of Stone.
  ```
- **译文**：
  ```text
  融入一条岩石藤蔓，穿行其中到达被缠绕的生物附近（最大射程 %d）。
  		融入岩石藤蔓会治疗你 %0.2f 点生命值（受意志加成）。
  		使用这个技能不会打破岩石身躯。
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/gifts/earthen-vines.lua:142` 格式化参数为 `tformat(self:getTalentRange(t), 100 + self:combatTalentStatDamage(t, "wil", 40, 630))`，占位符 `%d` 与 `%0.2f` 正确对应；技能名 `Body of Stone`（岩石身躯）及属性词 `Willpower`（意志）规范。

---

### entry-01859
- **位置**：`mod-tome.lua:24874`（`mod-tome/data/talents/gifts/earthen-vines.lua`）
- **原文**：
  ```text
  Merge your target (within range %d) with one of your stone vines that has seized it, forcing it to traverse the vine and reappear near you.
  		Merging with the stone is detrimental for the target, dealing %0.1f nature damage.
  		The damage will increases with your Willpower.
  ```
- **译文**：
  ```text
  将射程 %d 内已被你的岩石藤蔓抓住的目标与藤蔓融合，使其强制穿越藤蔓，重新出现在你身边。
  		与岩石融合的过程会对目标造成 %0.1f 自然伤害。
  		伤害受意志加成。
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/gifts/earthen-vines.lua:182` 格式化参数为 `tformat(self:getTalentRange(t), 80 + self:combatTalentStatDamage(t, "wil", 40, 330))`，占位符 `%d` 与 `%0.1f` 对应准确；自然伤害（nature damage）与意志（Willpower）翻译规范。

---

### entry-01860
- **位置**：`mod-tome.lua:24884`（`mod-tome/data/talents/gifts/eyals-fury.lua`）
- **原文**：
  ```text
  You focus the inexorable pull of nature against a single creature, eroding it and allowing it to be reclaimed by the cycle of life.
  		This deals %0.1f Nature and %0.1f Acid damage to the target, and is particularly devastating against undead and constructs, dealing %d%% more damage to them.
  		The damage increases with your Mindpower.
  ```
- **译文**：
  ```text
  你将自然无情的力量集中于某个目标上，腐蚀他并让他重归生命轮回。
  		造成 %0.1f 点自然伤害，%0.1f 点酸性伤害，对不死族和构装生物有 %d%% 伤害加成。
  		伤害受精神强度加成。
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/gifts/eyals-fury.lua:49` 格式化参数为 `tformat(damDesc(self, DamageType.NATURE, dam/2), damDesc(self, DamageType.ACID, dam/2), t.undeadBonus)`，占位符 `%0.1f`、`%0.1f`、`%d%%` 数量与顺序完全对应；种族实体词 `undead`（不死族）、`constructs`（构装生物）严格符合术语表标准译名。

---

### entry-01861
- **位置**：`mod-tome.lua:24890`（`mod-tome/data/talents/gifts/eyals-fury.lua`）
- **原文**：
  ```text
  Your devotion to nature has made your body more attuned to the natural world and resistant to unnatural energies.
  		You gain %d Spell save, %0.1f%% Arcane resistance, and %0.1f%% Nature damage affinity.
  		You defy arcane forces, so that any time you take damage from a spell, you restore %0.1f Equilibrium each turn for %d turns.
  		The effects increase with your Mindpower.
  ```
- **译文**：
  ```text
  你对自然的虔诚让你的身体更亲近自然世界，对非自然力量也更具抵抗力。
  		你获得 %d 点法术豁免，%0.1f%% 奥术抗性，以及 %0.1f%% 自然伤害亲和。
  		由于你和奥术力量对抗，每次你受到法术伤害时，你每回合回复 %0.1f 点失衡值，持续 %d 回合。
  		效果受精神强度加成。
  ```
- **复核结论**：细微观察
- **可核验依据**：源码 `game/modules/tome/data/talents/gifts/eyals-fury.lua:79` 格式化参数为 `tformat(t.getSave(self, t), t.getResist(self, t), t.getAffinity(self, t), t.getPower(self, t), t.getDuration(self, t))`，5 个占位符 `%d`、`%0.1f%%`、`%0.1f%%`、`%0.1f`、`%d` 顺序完全一致；术语 `Spell save`（法术豁免）、`Arcane resistance`（奥术抗性）、`Nature damage affinity`（自然伤害亲和）准确。细微观察在于第 3 行“restore %0.1f Equilibrium”译为“回复 %0.1f 点失衡值”：源码中实际效果为 `self:incEquilibrium(-eff.power)`（降低失衡值），中文直译英文的“回复”对自然系职业可能让部分新手玩家产生增加失衡值的误解（对比 entry-01863 中译作“使你的失衡值降低”更为明晰），但译文严格遵照英文原文，未算翻译错误。

---

### entry-01862
- **位置**：`mod-tome.lua:24899`（`mod-tome/data/talents/gifts/eyals-fury.lua`）
- **原文**：
  ```text
  You call upon the earth to create a blinding, corrosive cloud in an area of radius %d for %d turns.
  		Each turn, this cloud deals %0.1f acid damage to each foe with a 25%% chance to blind and a %d%% chance of burning away one magical sustain or beneficial magical effect.
  		The damage increases with your Mindpower.
  ```
- **译文**：
  ```text
  你召唤酸云覆盖半径 %d 的地面，持续 %d 回合。酸云具有腐蚀性，能致盲敌人。
  		每回合，酸云对每个敌人造成 %0.1f 点酸性伤害，25%% 几率致盲，同时有 %d%% 几率除去一个有益的魔法效果或魔法持续技能。
  		伤害受精神强度加成。
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/gifts/eyals-fury.lua:167` 格式化参数为 `tformat(self:getTalentRadius(t), t.getDuration(self, t), damDesc(self, DamageType.ACID, t.getDamage(self, t)), t.getChance(self, t))`，占位符 `%d`、`%d`、`%0.1f`、`25%%`、`%d%%` 数量与顺序完全对应；驱散逻辑描述（去除有益魔法效果或魔法持续技能）与代码 `removeEffect` 完全一致。

---

### entry-01863
- **位置**：`mod-tome.lua:24907`（`mod-tome/data/talents/gifts/eyals-fury.lua`）
- **原文**：
  ```text
  You draw deeply from your connection with nature to create a radius %d storm of natural forces around you for %d turns.
  		This storm moves with you and deals %0.1f Nature damage each turn to all foes it hits.
  		In addtion, it will drain up to %d Mana, %d Vim, %d Positive, and %d Negative energy from each enemy within it's area every turn, while you restore Equilibrium equal to 10%% of the amount drained.
  		The damage and drain increase with your Mindpower.
  ```
- **译文**：
  ```text
  你在自己周围半径 %d 的范围内制造自然力量风暴，持续 %d 回合。
  		风暴会跟随你移动，每回合对每个敌人造成 %0.1f 点自然伤害。
  		此外，每回合还会从范围内的每个敌人身上最多抽取 %d 点法力、%d 点活力、%d 点正能量和 %d 点负能量，同时使你的失衡值降低相当于所抽取能量的 10%%。
  		伤害和吸取量受精神强度加成。
  ```
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/gifts/eyals-fury.lua:234` 格式化参数为 `tformat(self:getTalentRadius(t), t.getDuration(self, t), damDesc(self, DamageType.NATURE, t.getDamage(self, t)), drain, drain/2, drain/4, drain/4)`，7 个数值占位符及转义 `10%%` 顺序无误；能量吸取与失衡值反哺机制（`eff.src:incEquilibrium(-drain/10)`）译为“使你的失衡值降低”清晰无误。

---

### entry-01864
- **位置**：`mod-tome.lua:24928`（`mod-tome/data/talents/gifts/fire-drake.lua`）
- **原文**：`@Source@ roars!`
- **译文**：`@Source@发出咆哮！`
- **复核结论**：未发现问题
- **可核验依据**：源码 `game/modules/tome/data/talents/gifts/fire-drake.lua:92` 中 `message = _t"@Source@ roars!"`，实体标签 `@Source@` 保留完整，战斗日志用词规范。

---

### entry-01865
- **位置**：`mod-tome.lua:24929`（`mod-tome/data/talents/gifts/