# batch-069：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-02148
位置：mod-tome.lua:27892；section：mod-tome/data/talents/psionic/slumber.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Enter a sleeping target's dreams for %d turns.  While in the Dreamscape, you'll encounter the target's invulnerable sleeping form as well as dream projections that it will spawn every other turn to defend its mind.
		Projections inflict 50%% less damage than the original, unless the target has Lucid Dreamer active.
		When the Dreamscape ends, for each projection destroyed, the target's life will be reduced by 10%% and it will be brainlocked for one turn.
		In the Dreamscape, your damage will be improved by %d%%.
		The damage bonus will improve with your Mindpower.
```
译文：
```text
进入某个睡眠状态目标的梦境中，持续 %d 回合。当你位于梦境空间中时，你将会遇到目标无敌的睡眠形态，每 2 回合它会制造出 1 个梦境守卫来保护它的心灵。
		除非目标激活了清晰梦境，否则梦境守卫造成的伤害比本体低 50%%。
		当梦境空间的效果结束时，你每摧毁一个梦境守卫，目标生命值会减少 10%%，并且受到持续 1 回合的思维封锁效果（可叠加）。
		在梦境空间中时，你的伤害会提高 %d%%。
		伤害增益受精神强度加成。
```

## entry-02149
位置：mod-tome.lua:27906；section：mod-tome/data/talents/psionic/solipsism.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You believe that your mind is the center of everything.  Permanently increases the amount of psi you gain per level by 5 and reduces your life rating (affects life at level up) by 50%% (one time only adjustment).
		You also have learned to overcome damage with your mind alone, and convert %d%% of all damage you receive into Psi damage and %d%% of your healing and life regen now recovers Psi instead of life.
		Converted Psi damage you take will be further reduced by %0.1f%% (%0.1f%% from character level with the remainder further reduced by %0.1f%% from talent level).
		The first talent point invested will also increase the amount of Psi you gain from Willpower by 0.5, but reduce the amount of life you gain from Constitution by 0.25.
		The first talent point also increases your solipsism threshold by 20%% (currently %d%%), reducing your global speed by 1%% for each percentage your current Psi falls below this threshold.
```
译文：
```text
你相信你的心灵是世间万物的中心。
		每级永久性增加你 5 点灵能值，并减少你 50%% 的生命成长（影响升级时的生命增益，但只在学习此技能时永久影响一次）
		同时你学会用心灵来承受伤害，转化 %d%% 生命削减为灵能值削减，并且 %d%% 的治疗值和回复值会转化为灵能值的增长。
		转化成的灵能值削减将进一步被减少 %0.1f%% （%0.1f%% 来自于人物等级，%0.1f%% 来自于技能等级。）
		学习此技能时，（高于基础值 10 的）每点意志会额外增加 0.5 点灵能值上限，而（高于基础值 10 的）每点体质会减少 0.25 点生命上限（若低于基础值 10 则增加生命上限）。
		学习此技能时，你的唯我临界点会增加 20 %%（当前 %d%%），你的灵能值每低于这个临界点 1 %%，你的所有速度减少 1 %%。
```

## entry-02150
位置：mod-tome.lua:27917；section：mod-tome/data/talents/psionic/solipsism.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You now substitute %d%% of your Mental Save for %d%% of your Physical and Spell Saves throws (so at 100%%, you would effectively use mental save for all saving throw rolls).
		The first talent point invested will also increase the amount of Psi you gain from Willpower by 0.5, but reduce the amount of life you gain from Constitution by 0.25.
		Learning this talent also increases your solipsism threshold by 10%% (currently %d%%).
```
译文：
```text
你现在使用 %d%% 精神豁免值来替代 %d%% 物理和法术豁免（即 100 %%时精神豁免完全替代所有豁免）。
		学习此技能时，（高于基础值 10 的）每点意志会额外增加 0.5 点灵能值上限，而（高于基础值 10 的）每点体质会减少 0.25 点生命上限（若低于基础值 10 则增加生命上限）。
		学习此技能也会增加你 10 %%唯我临界点（当前 %d%%）。
```

## entry-02151
位置：mod-tome.lua:27923；section：mod-tome/data/talents/psionic/solipsism.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
For every percent that your Psi pool exceeds %d%%, you gain 1%% global speed (up to a maximum of %+d%%).
		The first talent point invested will also increase the amount of Psi you gain from Willpower by 0.5, but reduce the amount of life you gain from Constitution by 0.25 and will increase your solipsism threshold by 10%% (currently %d%%).
```
译文：
```text
当你的灵能值超过 %d%% 时，每超过 1%% 你增加 1%% 全局速度（最大值 %+d%%）。
		学习此技能时，每点意志使灵能值上限额外增加 0.5 点，每点体质使生命上限减少 0.25 点，并增加 10%% 唯我临界点（当前 %d%%）。
```

## entry-02152
位置：mod-tome.lua:27927；section：mod-tome/data/talents/psionic/solipsism.lua；source_tag：delayedLogMessage；args_order：None；special：None

原文：
```text
#TAN##Source# mentally dismisses some damage!
```
译文：
```text
#TAN##Source#精神上豁免了部分伤害！
```

## entry-02153
位置：mod-tome.lua:27929；section：mod-tome/data/talents/psionic/solipsism.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Each time you take damage, you roll %d%% of your mental save against it.  A successful saving throw can crit and will reduce the damage by at least 50%%.
		The first talent point invested will also increase the amount of Psi you gain from Willpower by 0.5, but reduce the amount of life you gain from Constitution by 0.25.
		The first talent point also increases your solipsism threshold by 10%% (currently %d%%).
```
译文：
```text
每当你受到伤害时，你会使用 %d%% 精神豁免来鉴定。鉴定时精神豁免可能暴击，至少减少 50%% 的伤害。
		学习此技能时，（高于基础值 10 的）每点意志会额外增加 0.5 点灵能值上限，而（高于基础值 10 的）每点体质会减少 0.25 点生命上限（若低于基础值 10 则增加生命上限）。
		学习此技能也会增加你 10 %%唯我临界点（当前 %d%%）。
```

## entry-02154
位置：mod-tome.lua:27976；section：mod-tome/data/talents/psionic/thermal-mastery.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Within radius %d, transfer heat from a group of enemies bodies to their equipment, freezing them to the floor while the excess heat disables their weapons and armor.
		Those afflicted will be dealt %0.1f Cold and %0.1f Fire damage, and be pinned (Frozen Feet) and disarmed for %d turns.
		Targets suffering both types of damage will also have have their Armour and saves reduced by %d.
		The chance to apply the effects and the duration increase with your Mindpower.
```
译文：
```text
在半径 %d 范围内，将一群敌人身上的热量转移到他们的装备上，把敌人冻僵在地面，多余的热量则令他们无法使用武器和盔甲。
		造成 %0.1f 寒冷伤害和 %0.1f 火焰伤害，并对敌人施加定身（冻足）和缴械状态，持续 %d 回合。
		受到两种伤害影响的单位也会降低 %d 护甲和豁免。
		施加状态的几率和持续时间受精神强度加成。
```

## entry-02155
位置：mod-tome.lua:27997；section：mod-tome/data/talents/psionic/thought-forms.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Not enough space to summon!
```
译文：
```text
没有足够的空间召唤！
```

## entry-02156
位置：mod-tome.lua:27999；section：mod-tome/data/talents/psionic/thought-forms.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A thought-forged bowman.  It appears ready for battle.
```
译文：
```text
一位精神体弓箭手。他时刻准备着战斗。
```

## entry-02157
位置：mod-tome.lua:28000；section：mod-tome/data/talents/psionic/thought-forms.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Forge a bowman, clad in leather armor, from your thoughts.  The bowman learns Bow Mastery, Combat Accuracy, Steady Shot, Crippling Shot, and Rapid Shot as it levels up, and has +%d Strength, +%d Dexterity, and +%d Constitution.
		Activating this talent will put all other thought-forms on cooldown.
		The stat bonuses will improve with your Mindpower.
```
译文：
```text
你从脑海里召唤出一位身穿皮甲的精神体弓箭手。当精神体弓箭手到达对应等级时可习得弓术掌握、强化命中、稳固射击、致残射击和急速射击，并且可增加 %d 点力量、%d 点敏捷和 %d 体质。
		激活此技能会使其他思维形态技能进入冷却。
		属性增益受精神强度加成。
```

## entry-02158
位置：mod-tome.lua:28005；section：mod-tome/data/talents/psionic/thought-forms.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Thought-Form: Warrior
```
译文：
```text
思维形态：战士
```

## entry-02159
位置：mod-tome.lua:28006；section：mod-tome/data/talents/psionic/thought-forms.lua；source_tag：_t；args_order：None；special：None

原文：
```text
thought-forged warrior
```
译文：
```text
精神体战士
```

## entry-02160
位置：mod-tome.lua:28007；section：mod-tome/data/talents/psionic/thought-forms.lua；source_tag：_t；args_order：None；special：None

原文：
```text
A thought-forged warrior wielding a massive battle-axe and clad in heavy armor.  It appears ready for battle.
```
译文：
```text
一位手持巨型战斧、身穿重甲的精神体战士。他时刻准备着战斗。
```

## entry-02161
位置：mod-tome.lua:28008；section：mod-tome/data/talents/psionic/thought-forms.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Forge a warrior wielding a battle-axe from your thoughts.  The warrior learns Weapon Mastery, Combat Accuracy, Berserker, Death Dance, and Rush as it levels up, and has +%d Strength, +%d Dexterity, and +%d Constitution.
		Activating this talent will put all other thought-forms on cooldown.
		The stat bonuses will improve with your Mindpower.
```
译文：
```text
你从脑海里召唤出一位手持战斧的精神体战士。当精神体战士到达对应等级时可习得武器掌握、强化命中、嗜血、死亡之舞和冲锋，并且可增加 %d 点力量、%d 点敏捷和 %d 体质。
		激活此技能会使其他思维形态技能进入冷却。
		属性增益受精神强度加成。
```

## entry-02162
位置：mod-tome.lua:28016；section：mod-tome/data/talents/psionic/thought-forms.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Forge a defender wielding a sword and shield from your thoughts.  The solider learns Armor Training, Weapon Mastery, Combat Accuracy, Shield Pummel, and Shield Wall as it levels up, and has +%d Strength, +%d Dexterity, and +%d Constitution.
		Activating this talent will put all other thought-forms on cooldown.
		The stat bonuses will improve with your Mindpower.
```
译文：
```text
你从脑海里召唤出一位手持剑盾的精神体盾战士。当精神体盾战士到达对应等级时可习得护甲掌握、武器掌握、强化命中、盾牌连击和盾墙，并且可增加 %d 点力量、%d 点敏捷和 %d 体质。
		激活此技能会使其他思维形态技能进入冷却。
		属性增益受精神强度加成。
```

## entry-02163
位置：mod-tome.lua:28022；section：mod-tome/data/talents/psionic/thought-forms.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Forge a guardian from your thoughts alone.  Your guardian's primary stat will be improved by %d, its two secondary stats by %d, and it will have Magic, Cunning, and Willpower equal to your own.
		At talent level one, you may forge a mighty bowman clad in leather armor; at level three a powerful warrior wielding a two-handed weapon; and at level five a strong defender using a sword and shield.
		Thought forms can only be maintained up to a range of %d, and will rematerialize next to you if this range is exceeded.
		Only one thought-form may be active at a time, and the stat bonuses will improve with your Mindpower.
```
译文：
```text
你从脑海里召唤出一位强大的守护者。
		你的守护者主属性会增加 %d，他的两项副属性会增加 %d，同时他的魔力、灵巧和意志属性等同于你的属性值。
		在等级 1 时，你会召唤出身着皮甲的弓箭手大师；
		在等级 3 时，你会召唤出手持双手武器的精英狂战士；
		在等级 5 时，你会召唤出手持剑盾的精英盾战士。
		精神体只能存在于 %d 码范围内，若超出此范围，则精神体会回到你身边。
		同一时间只能维持一种思维形态。
		属性增益受精神强度加成。
```

## entry-02164
位置：mod-tome.lua:28037；section：mod-tome/data/talents/psionic/thought-forms.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Take direct control of your active thought-form, improving its damage, attack speed, and maximum life by %d%%, but leaving your body a defenseless shell.
		At talent level 1, any Feedback your Thought-Forms gain will be given to you as well. At level 3, your Thought-Forms gain a bonus to all saves equal to your Mental Save. At level 5, they gain a bonus to all damage equal to your bonus mind damage.
		The secondary bonuses apply whether or not this talent is currently active.
		The life, damage, and speed bonus will improve with your Mindpower.
```
译文：
```text
直接控制当前的精神体，增加其 %d%% 伤害、攻速以及最大生命值，但你的身体会变成毫无防御的空壳。
		在等级 1 时，你的精神体所获得的任何反馈值也会传递给你。
		在等级 3 时，你的精神体会获得所有豁免的增益效果，数值等同你精神豁免的大小。
		在等级 5 时，它们会获得所有伤害加成，数值等同你的额外精神伤害。
		这些次级增益无论此技能是否激活均有效。
		上述生命、伤害与速度加成受精神强度加成。
```

## entry-02165
位置：mod-tome.lua:28047；section：mod-tome/data/talents/psionic/thought-forms.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You now gain %d%% mind speed while Thought-Form: Bowman is active, %d Mindpower while Thought-Form: Warrior is active, and %d%% resist all while Thought-Form: Defender is active. 
		These bonuses scale with your Mindpower.
```
译文：
```text
现在，当思维形态：弓箭手激活时，你提升 %d%% 精神速度；
		当思维形态：战士激活时，你提升 %d 精神强度；
		当思维形态：盾战士激活时，你提升 %d%% 全体伤害抗性。
		受精神强度影响，增益效果按比例加成。
```

## entry-02166
位置：mod-tome.lua:28057；section：mod-tome/data/talents/psionic/trance.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Activate to purge negative status effects (100%% chance for the first effect, -%d%% less chance for each subsequent effect).  While this talent is sustained all your saving throws are increased by %d.
		The chance to purge and saving throw bonus will scale with your mindpower.
		Only one trance may be active at a time.
```
译文：
```text
激活以清除负面状态（第一个状态 100%% 清除，此后每清除一个，几率再降低 %d%%）。当此技能激活时，你的所有豁免值增加 %d。
		受精神强度影响，净化几率和豁免增益按比例加成。
		同一时间只能维持一种入定。
```

## entry-02167
位置：mod-tome.lua:28075；section：mod-tome/data/talents/psionic/trance.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
When you wield or wear an item infused by psionic, nature, or arcane-disrupting forces you improve all values under its 'when wielded/worn' field %d%%.
		Note this doesn't change the item itself, but rather the effects it has on your person (the item description will not reflect the improved values).
```
译文：
```text
当你穿戴由灵能、自然或反魔力量灌注的装备时，你增加 %d%% "当使用或装备时："的增益属性。
		注意此技能不会改变装备属性，它的效果只作用于你自身（此技能的增益也不会在装备描述上反映出来）。
```

## entry-02168
位置：mod-tome.lua:28108；section：mod-tome/data/talents/psionic/voracity.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Increases your maximum energy by %d. You also gain %0.1f Psi for each kill and %0.1f Psi for each mind critical.
```
译文：
```text
增加灵能值上限 %d。每次杀死敌人获得 %0.1f 灵能值，每次精神暴击获得 %0.1f 灵能值。
```

## entry-02169
位置：mod-tome.lua:28120；section：mod-tome/data/talents/spells/acid-alchemy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
While Acid Infusion is active, your bombs coat your golem in acid for %d turns when they hit it.
		While coated, any melee hit against your golem has a %d%% chance to trigger a radius 4 cone of acid towards the attacker that does %0.1f Acid damage to all caught inside. (This can only happen once per turn.)
		The effects increase with your talent level and with the Spellpower and damage modifiers of your golem.
```
译文：
```text
当你的酸性充能激活时，若你的炸弹击中了你的傀儡，酸液会覆盖傀儡 %d 回合。
		当傀儡被酸液覆盖时，任何命中傀儡的近战攻击有 %d%% 概率朝攻击者方向触发一次范围 4 的锥形酸液喷射，对波及范围内的所有单位造成 %0.1f 点酸性伤害（每回合至多一次）。
		效果受你的技能等级、法术强度和傀儡的伤害加成影响。
```

## entry-02170
位置：mod-tome.lua:28126；section：mod-tome/data/talents/spells/acid-alchemy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
A radius %d pool of acid spawns at the target location, doing %0.1f Acid damage each turn for %d turns.
		All creatures caught in the mire will also suffer a %d%% slowness effect.
		The damage will increase with your Spellpower.
```
译文：
```text
一小块酸液覆盖了目标地面，散落在半径 %d 的范围内，每回合造成 %0.1f 点酸性伤害，持续 %d 回合。
		受影响的生物同时会减速 %d%%。
		伤害受法术强度加成。
```

## entry-02171
位置：mod-tome.lua:28144；section：mod-tome/data/talents/spells/advanced-golemancy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You tap into your golem's life energies to replenish your own. Drains %d life.
```
译文：
```text
你汲取傀儡的生命能量来恢复自己。从傀儡身上吸取 %d 点生命。
```

## entry-02172
位置：mod-tome.lua:28146；section：mod-tome/data/talents/spells/advanced-golemancy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Insert a pair of gems into your golem, providing it with the gem bonuses and changing its melee attack damage type. You may remove the gems and insert different ones; this does not destroy the gems you remove.
		Gem level usable: %d
		Gem changing is done in the golem's inventory.
```
译文：
```text
在傀儡身上镶嵌 2 颗宝石，它可以得到宝石加成并改变近战攻击类型。你可以移除并镶嵌不同种类的宝石，移除行为不会破坏宝石。
		可用宝石等级：%d
		宝石的更换在傀儡的物品栏中进行。
```

## entry-02173
位置：mod-tome.lua:28159；section：mod-tome/data/talents/spells/advanced-golemancy.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Increases your golem's life, mana and stamina regeneration rates by %0.2f.
		At level 1, 3 and 5, the golem also gains a new rune slot.
		Even without this talent, Golems start with three rune slots.
```
译文：
```text
增加傀儡 %0.2f 生命、法力和耐力回复。
		在等级 1、3、5 时，傀儡会增加 1 个新的符文孔。
		即使没有此天赋，傀儡默认也有 3 个符文孔。
```

## entry-02174
位置：mod-tome.lua:28206；section：mod-tome/data/talents/spells/aether.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You focus the aether into a spinning beam of arcane energies, doing %0.2f arcane damage and having 25%% chance to silence the creatures it pierces.
		The beam will also damage its epicenter each turn for 10%% of the damage (but it will not silence).
		The beam spins with incredible speed (1600%%) and can only hit the same target up to 3 times inbetween their turns.
		The damage will increase with your Spellpower.
```
译文：
```text
你凝聚以太能量，释放出一道旋转的奥术光束，对被它穿透的生物造成 %0.2f 奥术伤害并且有 25 %%几率将其沉默。
		该光束每回合也会对中心点造成 10 %%的伤害（但是不会沉默目标）。
		该光束以难以置信的速度旋转（1600 %% 速度），对同一目标在其两个回合之间最多命中 3 次。
		伤害受法术强度加成。
```

## entry-02175
位置：mod-tome.lua:28222；section：mod-tome/data/talents/spells/aether.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
#VIOLET#%s loses 50 mana from using a non-Arcane talent!#LAST#
```
译文：
```text
#VIOLET#%s 由于使用非奥术技能，流失了50点法力值！#LAST#
```

## entry-02176
位置：mod-tome.lua:28274；section：mod-tome/data/talents/spells/age-of-dusk.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You recall the age long gone where necromancers had free reign over the world.
		Increases all saves by %d, confusion and teleport resistances by %d%%.
		At level 5 any time you cross the 1 life threshold you become invulnerable for 1 turns.
```
译文：
```text
你回忆起久远的黄金时代，死灵法师自由支配这个世界。
		获得 %d 全体豁免，%d%% 混乱和传送抗性。
		技能等级 5 时，每当你穿越 1 生命值的界线，无敌 1 回合。
```

## entry-02177
位置：mod-tome.lua:28284；section：mod-tome/data/talents/spells/air.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Conjures up mana into a powerful beam of lightning, doing %0.2f to %0.2f damage (%0.2f average)
		The damage will increase with your Spellpower.
```
译文：
```text
用魔法召唤一次强力的闪电造成 %0.2f ～ %0.2f 伤害（平均 %0.2f）。
		伤害受法术强度加成。
```

## entry-02178
位置：mod-tome.lua:28302；section：mod-tome/data/talents/spells/air.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Conjures a furious, raging lightning storm with a radius of 6 that follows you as long as this spell is active.
		Each turn, a random lightning bolt will hit up to %d of your foes for 1.00 to %0.2f damage (%0.2f average) in a radius of 1.
		The damage will increase with your Spellpower.
```
译文：
```text
当此技能激活时，在 6 码半径范围内召唤一阵强烈的闪电风暴跟随你。
		每回合闪电风暴会随机伤害最多 %d 个敌方单位，对 1 码半径范围造成 1.00 ～ %0.2f 伤害（平均 %0.2f）。
		伤害受法术强度加成。
```

## entry-02179
位置：mod-tome.lua:28312；section：mod-tome/data/talents/spells/animus.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Each time you or your undead minions deal damage to a creature you apply Soul Leech to them.
		If a creature dies with this effect active, you steal its soul.
		Strong creatures and bosses are so overflowing with soul power that you steal a fragment of their soul every few turns:
		%s- rare: at most every %d turns
		%s- unique: at most every %d turns
		%s- boss: at most every %d turns
		%s- elite boss: at most every %d turns#WHITE#

		Also increases your maximum souls capacity by %d .
		
```
译文：
```text
每当你或你的不死随从对生物造成伤害，将会对其附加灵魂吸取效果。
		如果生物在灵魂吸取状态下死去，你将会偷取它的灵魂。
		强大的生物和 Boss 的灵魂力量如此强大，你可以每隔几个回合从它们的身上偷取一个灵魂：
		%s- 稀有：最多每 %d 回合偷取一个灵魂
		%s- 史诗：最多每 %d 回合偷取一个灵魂
		%s- Boss：最多每 %d 回合偷取一个灵魂
		%s- 精英Boss：最多每 %d 回合偷取一个灵魂#WHITE#

		此外，增加你的最大灵魂储量 %d。
		
```

## entry-02180
位置：mod-tome.lua:28332；section：mod-tome/data/talents/spells/animus.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Consume a soul whole to rebuild your body, healing you for %d and generating %d mana.
		If used below 1 life the surge increases your spellpower by %d for 10 turns.
		The heal and mana increases with your Spellpower.
```
译文：
```text
消耗一个灵魂，用来修复你的身体，恢复 %d 生命值，获得 %d 法力值。
		如果你当前生命值在 1 以下，这股力量还将会提升你的法术强度 %d，持续 10 回合。
		治疗量和法力值受法术强度加成。
```

## entry-02181
位置：mod-tome.lua:28344；section：mod-tome/data/talents/spells/animus.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You draw constant power from the souls you hold within your grasp.
		If you hold at least 2, your mana regeneration is increased by %0.1f per turn.
		If you hold at least 5, your spellpower is increased by %d.
		If you hold at least 8, all your resistances are increased by %d.
```
译文：
```text
你从掌握的灵魂中持续汲取力量，根据当前灵魂数量获得以下效果：
		2 个以上：你的每回合法力值恢复速度增加 %0.1f。
		5 个以上：你的法术强度增加 %d。
		8 个以上：你的全体伤害抗性增加 %d%%。
```

## entry-02182
位置：mod-tome.lua:28378；section：mod-tome/data/talents/spells/arcane.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Surround yourself with arcane forces, disrupting any attempts to harm you by creating a shield of pure aether which can absorb %d damage.
		In combat, the mental focus required to maintain and monitor the shield is too much and you let it run on its own. In this state once the shield power is depleted it will start using your mana to absorb hits, at a ratio of %0.2f mana per damage.
		Whenever mana is used by the shield it stores a remnant of this energy (up to %d max). When the shield is deactivated any stored energy is released in a radius %d arcane storm that lasts 5 turns, dealing 20%% of the total stored damage each turn.
		Outside of combat the shield regenerates 10%% of its power each turn and stored energy quickly dissipates.
		Dropping below 50%% mana or reaching max energy storage will automatically deactivate this talent.
		The shield power improves with your Spellpower.
		The maximum energy storage is based on your total mana (ignoring sustained spells), with a limit at %d effective mana.

		Current shield power: %d
		Current stored energy: %d
```
译文：
```text
你的身边充满奥术力量，制造出一层能吸收 %d 伤害的护盾。
		在战斗中你无法集中精力持续维持这层护盾，一旦护盾值消耗归零，则会使用你的法力值来吸收伤害，比例为 %0.2f 法力值吸收一点伤害。
		每当法力值被该效果消耗时，护盾会储存一定能量（最多 %d）。当护盾关闭时，这些储存的能量将转化为在你身边 %d 格的奥术风暴，在5回合内每回合造成 20%% 总储存能量的伤害。
		战斗外该护盾每回合回复 10%%，同时储存的能量迅速消散。
		当你法力值下降到 50%% 以下，或者达到最大能量存储量，护盾会自动关闭。
		护盾值受法术强度加成。
		最大储存能量受原始法力值上限加成（无视已经启用的维持技能），在 %d 法力值的时候达到上限。

		当前护盾值：%d
		当前储能：%d
```

## entry-02183
位置：mod-tome.lua:28402；section：mod-tome/data/talents/spells/conveyance.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Select a target to teleport...
```
译文：
```text
选择目标传送…
```

## entry-02184
位置：mod-tome.lua:28403；section：mod-tome/data/talents/spells/conveyance.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
The spell fizzles!
```
译文：
```text
法术失败了！
```

## entry-02185
位置：mod-tome.lua:28404；section：mod-tome/data/talents/spells/conveyance.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Select a teleport location...
```
译文：
```text
选择传送位置…
```

## entry-02186
位置：mod-tome.lua:28405；section：mod-tome/data/talents/spells/conveyance.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
The targeted phase door fizzles and works randomly!
```
译文：
```text
相位之门定位失败了，变为随机传送！
```

## entry-02187
位置：mod-tome.lua:28406；section：mod-tome/data/talents/spells/conveyance.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Teleports you randomly within a small range of up to %d grids.
		At level 4, it allows you to specify which creature to teleport.
		At level 5, it allows you to choose the target area (radius %d).
		If the target area is not in line of sight, there is a chance the spell will partially fail and teleport the target randomly.
		The range will increase with your Spellpower.
```
译文：
```text
在 %d 码范围内随机传送你自己。
		在等级 4 时，你可以传送指定生物（怪物或被护送者）。
		在等级 5 时，你可以选择传送位置（半径 %d）。
		如果目标位置不在你的视线里，则法术有可能失败，变为随机传送。
		影响范围受法术强度加成。
```

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Attack speed	攻击速度	T.GAME.STAT	combat	tformat	preferred	core	角色面板 Speeds/Attack Speed 行；与 Global speed 全局速度区分
Berserker	狂战士	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Constitution	体质	T.GAME.STAT	combat	stat name	existing	global	
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Death Dance	死亡之舞	T.GAME.TALENT	talents	talent name	existing	core	
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Global speed	全局速度	T.GAME.STAT	combat	_t	preferred	core	角色面板和教程中的全局行动速度；不写作“整体速度”或“全体速度”
Global speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	格式化状态说明中的句首机制名；与小写 global speed 统一
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Lightning	闪电术	T.GAME.TALENT	talents	talent name	existing	core	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Mental Save	精神豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Mental Save 行；与 Physical Save 物理豁免、Spell Save 法术豁免并列
Mindpower	精神强度	T.GAME.STAT	combat	tformat	preferred	multi	技能与物品机制说明中的精神强度属性；与 Willpower“意志”区分
Necromancer	死灵法师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Not enough space to summon!	没有足够的空间召唤。	T.RUNTIME.LOG	combat	logSeen	preferred	global	召唤失败日志（22 处）
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Phase Door	相位之门	T.GAME.TALENT	talents	talent name	existing	core	
Psi	灵能值	T.GAME.RESOURCE	resources	_t	existing	core	
Psionic	灵能系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Resistances	抗性	T.GAME.STAT	combat	_t	preferred	core	角色面板 Resistances base/cap 行；单系抗性为“X抗性”，全抗为 All Resists 全部抗性
Silence	沉默	T.GAME.TALENT	talents	talent name	existing	global	
Souls	灵魂	T.GAME.RESOURCE	combat	_t	preferred	core	死灵法师资源；Maximum souls 灵魂上限
Spell Save	法术豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Spell Save 行；与 Physical Save 物理豁免、Mental Save 精神豁免并列
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Stamina	体力值	T.GAME.RESOURCE	resources	_t	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Thought-Forms	思维形态	T.GAME.TALENT	talents	talent name	preferred	core	技能名及同系技能前缀统一
Thought-Forms	思维形态	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	灵能塑造的精神体技能类型；不使用“具象之弧”
Undead	不死族	T.PN.RACE	creatures	nil	existing	core	
Warrior	战士系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“战士系”
Willpower	意志	T.GAME.STAT	combat	stat name	existing	global	
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
cold	寒冷	T.GAME.DAMAGE	combat	damage type	existing	core	
cold	寒冷	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
confusion	混乱	T.GAME.EFFECT	combat	effect subtype	existing	core	
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
disarm	缴械	T.GAME.EFFECT	combat	effect subtype	existing	global	
dreamscape	梦境空间	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
global speed	全局速度	T.GAME.STAT	combat	_t	preferred	core	装备、技能和叙述中的全局行动速度机制；不写作“整体速度”
global speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	技能与状态说明中的全局行动速度机制；不写作“整体速度”或“全体速度”
golem	傀儡	T.GAME.ENTITY	creatures	entity subtype	existing	global	
golem	傀儡	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
infusion	充能	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	炼金术师为宝石炸弹注入元素力量的技能类型；区别于刻印物品 Infusion（纹身）
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
lightning	闪电	T.GAME.DAMAGE	combat	damage type	existing	core	
lightning	闪电	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
psionic	灵能	T.GAME.EFFECT	combat	effect subtype	existing	global	
psionic	灵能	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
regeneration	回复	T.GAME.EFFECT	combat	effect subtype	existing	global	
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
silence	沉默	T.GAME.EFFECT	combat	effect subtype	existing	core	
sleep	睡眠	T.GAME.EFFECT	combat	effect subtype	existing	global	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
teleport	传送	T.GAME.EFFECT	combat	effect subtype	existing	global	
trance	入定	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	灵能系技能类型；指专注的入定状态，不是幻想
undead	亡灵	T.GAME.ENTITY	creatures	entity type	existing	global	
undead	亡灵	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
