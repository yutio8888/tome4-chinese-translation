# batch-077：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-02470
位置：mod-tome.lua:31329；section：mod-tome/data/talents/uber/cun.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s surges with #1133F3#icy#LAST# power!
```
译文：
```text
%s涌起#1133F3#冰霜#LAST#能量的狂潮！
```

## entry-02471
位置：mod-tome.lua:31330；section：mod-tome/data/talents/uber/cun.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s surges with #ROYAL_BLUE#lightning#LAST# power!
```
译文：
```text
%s涌起#ROYAL_BLUE#闪电#LAST#能量的狂潮！
```

## entry-02472
位置：mod-tome.lua:31331；section：mod-tome/data/talents/uber/cun.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s surges with #YELLOW#light#LAST# power!
```
译文：
```text
%s涌起#YELLOW#光系#LAST#能量的狂潮！
```

## entry-02473
位置：mod-tome.lua:31332；section：mod-tome/data/talents/uber/cun.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s surges with #LIGHT_GREEN#natural#LAST# power!
```
译文：
```text
%s涌起#LIGHT_GREEN#自然#LAST#能量的狂潮！
```

## entry-02474
位置：mod-tome.lua:31333；section：mod-tome/data/talents/uber/cun.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Surround yourself with an elemental aura that stores damage you deal.
		Whenever you have stored %d damage of one type you unleash a powerful blast at a random enemy dealing %d damage of that type in radius %d and granting you one of the following effects:

		Physical:		Cleanses 1 physical debuff and grant immunity to physical debuffs for 2 turns.
		#PURPLE#Arcane:#LAST#		Increases your mind and spell action speeds by 30%% for 3 turns.
		#LIGHT_RED#Fire:#LAST#		Increases all damage dealt by %d%% for 3 turns.
		#1133F3#Cold:#LAST#		Turns your skin into ice for 3 turns increasing armor by %d and dealing %d ice damage to attackers.
		#ROYAL_BLUE#Lightning:#LAST#	Increases your movement speed by %d%% for 2 turns.
		#YELLOW#Light:#LAST#		Reduces all cooldowns by 20%% for 3 turns.
		#LIGHT_GREEN#Nature:#LAST#		Cleanses 1 magical debuff and grant immunity to magical debuffs for 2 turns.

		Each effect can only happen once per 10 player turns.  This does not count as a typical cooldown.
		The damage and some effect powers increase with your Cunning and the threshold with your level.
		%s
```
译文：
```text
你被元素光环笼罩，存储你造成的元素伤害。
		当你积累的某类伤害达到 %d 时，你会向一个随机的敌人发射一次强力的爆炸，造成 %d 的该类型伤害，爆炸半径 %d 码，并对你自己附加以下的附加效果：

		物理：清除 1 个物理负面特效并给予 2 回合物理负面特效豁免。
		#PURPLE#奥术 :#LAST# 增加你的精神和施法速度 30%%，持续 3 回合。
		#LIGHT_RED#火焰 :#LAST# 增加你所造成的所有伤害 %d%%，持续 3 回合。
		#1133F3#寒冷 :#LAST# 将你的皮肤变成冰，增加护甲 %d，对攻击者造成 %d 冰冻伤害，持续 3 回合
		#ROYAL_BLUE#闪电 :#LAST# 你的移动速度提升 %d%%，持续 2 回合。
		#YELLOW#光系 :#LAST# 技能冷却时间减少 20%%，持续 3 回合。
		#LIGHT_GREEN#自然 :#LAST# 清除 1 个魔法负面特效并给予 2 回合魔法负面特效豁免。

		同种效果最多每 10 回合触发一次。这不是普通的技能冷却。
		伤害和效果强度受灵巧值加成，伤害阈值受等级加成。
		%s
```

## entry-02475
位置：mod-tome.lua:31387；section：mod-tome/data/talents/uber/cun.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Have sided with the Assassin Lord
```
译文：
```text
与刺客领主同流合污
```

## entry-02476
位置：mod-tome.lua:31404；section：mod-tome/data/talents/uber/dex.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Flexible Combat
```
译文：
```text
灵活格斗
```

## entry-02477
位置：mod-tome.lua:31422；section：mod-tome/data/talents/uber/dex.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You like to keep your most precious tools always at hand. This talent lets you prepare up to 4 items in advance (outside of combat).
		Then at a moment's notice you can use any of them as if they were worn.
		In addition swapping equipment sets (default q key) takes no time.
```
译文：
```text
你喜欢将最有用的工具常备手边。该技能允许你在战斗外准备最多4件工具。
		你可以随时使用它们，如同已装备一样。
		此外，切换装备组（默认 Q 键）不再消耗回合。
```

## entry-02478
位置：mod-tome.lua:31429；section：mod-tome/data/talents/uber/dex.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You spin madly, generating a sharp gust of wind with your weapons that deals 320%% weapon damage to all targets within radius 4 and disarms them for 4 turns.
```
译文：
```text
你挥动武器疯狂旋转，产生剑刃风暴，对 4 码范围内所有目标造成 320%% 的武器伤害，并缴械它们 4 回合。
```

## entry-02479
位置：mod-tome.lua:31430；section：mod-tome/data/talents/uber/dex.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Windtouched Speed
```
译文：
```text
疾风之速
```

## entry-02480
位置：mod-tome.lua:31449；section：mod-tome/data/talents/uber/dex.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You fire a shot straight at your enemy's vital areas, wounding them terribly.
		Enemies hit by this shot will take 450%% weapon damage and will be stunned and crippled (losing 50%% physical, magical and mental attack speeds) for five turns due to the devastating impact of the shot.
		The stun and cripple chances increase with your Accuracy.
```
译文：
```text
你对着目标要害射出一发，使目标受到重创。
		受到攻击的敌人将会承受 450%% 武器伤害，并且由于受到重创，还会被震慑和残废（减少 50%% 攻击、施法和精神速度）5 回合。
		震慑和残废几率受命中加成。
```

## entry-02481
位置：mod-tome.lua:31463；section：mod-tome/data/talents/uber/mag.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You gain 25%% absolute damage resistance and 25%% all damage penetration.  Each time you are struck by a weapon these bonuses are reduced by 5%% but fully recovered after 8 turns.
			Additionally, you gain 70%% of the highest of your Magic or Dexterity stat as defense (%d)
```
译文：
```text
你获得 25%% 绝对伤害抗性，25%% 全体伤害抗性穿透。
			每当你被武器攻击的时候，这两项加成各减少 5%%，8 回合后完全恢复。
			此外，你将获得相当于你魔力和敏捷中最高的一项  70%% 的闪避值 (%d)
```

## entry-02482
位置：mod-tome.lua:31470；section：mod-tome/data/talents/uber/mag.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You manifest a thin layer of aether all around you. 
		Any time you are the target of a dispel effect the aether strengthens around you, protecting you from the dispel and any further ones for 6 turns and unsustaining this spell.
		While undisturbed the layer of aether provides you with 40 raw spellpower.
```
译文：
```text
你在身边形成薄薄的一层以太。
		每当你成为解除效果的目标时，以太便会在你周围强化，使你免受该次解除以及此后 6 回合内的任何解除，并同时终止本持续法术。
		只要不受干扰，这层以太便为你提供 40 点原始法术强度。
```

## entry-02483
位置：mod-tome.lua:31477；section：mod-tome/data/talents/uber/mag.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your study of arcane forces has let you develop a new way of applying your aptitude for trapping and poisons.

		You gain 1.0 mastery in the Cunning/Poisons and Cunning/Trapping talent trees.
		Your Venomous Strike talent cooldown is reduced by 3.
		Your Lure talent cooldown is reduced by 5.

		You learn the following talents:
%s
```
译文：
```text
通过对奥术之力的研究，你找到了运用自己陷阱与毒药天赋的新方式。

你在灵巧/毒药系和灵巧/陷阱系技能树上获得 1.0 系数。
		你的毒素爆发技能冷却时间减少 3。
		你的诱饵技能冷却时间减少 5。

		你将习得以下技能：
%s
```

## entry-02484
位置：mod-tome.lua:31492；section：mod-tome/data/talents/uber/mag.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Arcane Might
```
译文：
```text
奥术伟力
```

## entry-02485
位置：mod-tome.lua:31493；section：mod-tome/data/talents/uber/mag.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You have learned to harness your latent arcane powers, channeling them through your weapon.
		This has the following effects:
		Equipped weapons are treated as having an additional 50%% Magic modifier;
		Your raw Physical Power is increased by 100%% of your raw Spellpower;
		Your physical critical chance is increased by 25%% of your bonus spell critical chance.
```
译文：
```text
你学会如何利用自己潜在的奥术力量，将它们注入你的武器。
		这一技能具有以下效果：
		所有武器均有额外的 50%% 魔法加成。
		你的基础物理强度增加等同于 100%% 基础法强的数值。
		你的物理暴击率增加等同于 25%% 额外法术暴击率的数值。
```

## entry-02486
位置：mod-tome.lua:31503；section：mod-tome/data/talents/uber/mag.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Have cast over 1000 spells and visited a zone outside of time
```
译文：
```text
曾释放过 1000 个以上的法术并且进入过时间之外的区域。
```

## entry-02487
位置：mod-tome.lua:31504；section：mod-tome/data/talents/uber/mag.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You can wrap temporal threads around you, assuming the form of a telugoroth for 10 turns.
		While in this form you gain pinning, bleeding, blindness and stun immunity, 30%% temporal resistance, your temporal damage bonus is set to your current highest damage bonus + 30%%, 50%% of the damage you deal becomes temporal, and you gain 20%% temporal resistance penetration.
		You also are able to cast anomalies: Anomaly Rearrange, Anomaly Temporal Storm, Anomaly Flawed Design, Anomaly Gravity Pull and Anomaly Wormhole.
```
译文：
```text
你可以扭曲周围的时间线，转换成时空元素“泰鲁戈洛斯”形态，持续 10 回合。
		在这种形态中，你对定身、流血、致盲、震慑免疫，获得 30%% 时空抗性和 20%% 的时空抗性穿透。
		你造成的伤害的 50%% 转化为时空伤害。
		同时，你的时空伤害增益等于你所有类型的伤害增益中的最大值，此外，还增加 30%% 额外时空伤害增益。
		你在时空形态下能释放以下异常：异常：重排，异常：时空风暴，异常：不完美设计，异常：重力井和异常：虫洞。
```

## entry-02488
位置：mod-tome.lua:31512；section：mod-tome/data/talents/uber/mag.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Have summoned at least 100 creatures. More permanent summons may count as more than 1.
```
译文：
```text
曾召唤了 100 个以上的召唤生物。更为持久的召唤物可能会被计为多于 1 个。
```

## entry-02489
位置：mod-tome.lua:31513；section：mod-tome/data/talents/uber/mag.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You infuse blighted energies into all of your summons, granting them Bone Shield (level 3) and a bonus to Spellpower equal to your Magic.
		Your Wilder Summons and Necrotic Minions will gain special corrupted talents (level 3), other summons will gain 10%% Blight damage conversion and Virulent Disease (level 3).
		#GREEN#Wilder Summons:#LAST#
		- War Hound: Gnaw
		- Jelly: Curse of Defencelessness
		- Minotaur: Ruin
		- Golem: Acid Blood
		- Ritch: Life Tap
		- Hydra: Blood Spray
		- Rimebark: Poison Storm
		- Fire Drake: Flame of Urh’Rok
		- Turtle: Elemental Discord
		- Spider: Blood Grasp
		#GREY#Necrotic Minions:#LAST#
		- Skeleton Mages: Bone Spear
		- Skeleton Archers: Bone Spike
		- Skeleton Warriors: Ruin
		- Bone Giants: Bone Spike and Ruin
		- Ghouls: Virulent Disease
		- Dread: Slumber
		%s
		
```
译文：
```text
你把枯萎能量灌注进你的召唤生物中，让他们获得白骨护盾（等级 3），并获得相当于你魔力值的法术强度加成。
		你的自然召唤和死灵随从将会得到特殊的枯萎技能（等级 3），其他的召唤物将会获得 10%% 枯萎伤害转换，并获得剧毒瘟疫（等级 3）。
		#GREEN#自然召唤：#LAST#
		- 战争猎犬：啃噬
		- 果冻怪：无防备诅咒
		- 米诺陶：毁伤
		- 岩石傀儡：酸性血液
		- 喷火里奇：生命分流
		- 九头蛇：鲜血喷射
		- 雾凇：剧毒风暴
		- 火龙：乌鲁洛克之焰
		- 乌龟：元素狂乱
		- 蜘蛛：鲜血支配
		#GREY#死灵随从：#LAST#
		- 骷髅法师：白骨之矛
		- 骷髅弓箭手：白骨尖刺
		- 骷髅战士：毁伤
		- 骨巨人：白骨尖刺和 毁伤
		- 食尸鬼：剧毒瘟疫
		- 梦魇：沉睡
		%s
		
```

## entry-02490
位置：mod-tome.lua:31567；section：mod-tome/data/talents/uber/mag.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your inner flame is strong. Each time that you receive a blow that would kill you, your body is wreathed in flames.
		The flames will cauterize the wound, fully absorbing all damage done this turn, but they will continue to burn for 8 turns.
		Each turn 10%% of the damage absorbed will be dealt by the flames. This will bypass resistance and affinity.
		Warning: this has a cooldown.
```
译文：
```text
你的心炎是如此强大。每当你受到足以致死的攻击时，你的身体都会被火焰环绕。
		火焰会烧灼伤口，完全吸收本回合受到的所有伤害，但会继续在你身上燃烧 8 回合。
		此后每回合，火焰会对你造成此前所吸收伤害的 10%%，且无视抗性和伤害亲和效果。
		警告：此技能有冷却时间。
```

## entry-02491
位置：mod-tome.lua:31588；section：mod-tome/data/talents/uber/mag.lua；source_tag：say；args_order：None；special：None

原文：
```text
#DARK_ORCHID#You are on your way to Lichdom. #{bold}#Your next death will finish the ritual.#{normal}#
```
译文：
```text
#DARK_ORCHID#你的巫妖转生之路已经到了最后的阶段。#{bold}#你下一次死亡的时候将会完成转化仪式。#{normal}#
```

## entry-02492
位置：mod-tome.lua:31589；section：mod-tome/data/talents/uber/mag.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
This is your true goal and the purpose of all necromancy - to become a powerful and everliving Lich!
		Once learnt, the next time you are killed, the arcane forces you unleash will be able to rebuild your body into the desired Lichform.
		Liches are immune to poisons, diseases, fear, cuts, stuns, do not need to breath and are 20%% resistant to cold and darkness.
		Liches also gain +12 Magic, Willpower and Cunning, 60%% chance to ignore critical hits, +4 life rating (not retroactive), +35 spell and mental saves and 7 mana regeneration.

		Liches gain a new racial tree with the following talents:
		- Neverending Unlife: A Lich body is extremely resilient, being able to go into negative life and when destroyed it can regenerate itself.
		- Frightening Presence: Your mere presence is enough to shatter the resolve of most, reducing their saves, damage and movement speed.
		- Doomed for Eternity: As a creature of doom and despair you now constantly spawn undead shadows around you.
		- Commander of the Dead: You are able to infuse all undead party members (including yourself) with un-natural power, increasing your physical and spellpower.
		
```
译文：
```text
这是你学习死灵法术的最终目标——成为强大而不死的巫妖！
		当你学习这一技能后，在你下一次被杀死的时候，你体内强大的奥术力量会重建你的身体，让你成为你梦寐以求的巫妖。
		巫妖免疫毒素、疾病、恐惧、流血、震慑，不需要呼吸，并获得 20%% 寒冷和黑暗抗性。
		巫妖同时获得 +12 魔力，意志和灵巧，60%% 暴击无视，+4 生命成长（不追加前面等级的生命值），+35 法术和精神豁免，获得 7 法力值恢复。

		巫妖会获得新的种族技能树，包含以下技能：
		- 不死之躯：巫妖的身体是极其难以摧毁的，它们的生命值可以降低到负数以下，且即使被杀死之后仍然可以复活。
		- 恐怖存在：你的恐怖存在足以粉碎大多数人的勇气，降低他们的豁免，伤害和移动速度。
		- 永恒毁灭：作为毁灭和绝望的使者，你现在不断地在你周围制造不死阴影。
		- 亡者领袖：你可以给所有不死族队友（包括你自己）注入非自然力量，增加它们的物理和法术强度。
		
```

## entry-02493
位置：mod-tome.lua:31613；section：mod-tome/data/talents/uber/mag.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Thaumaturgists have unlocked a deeper understanding of their spells, allowing them to combine the elements into new ways and to empower them.
		The spells Flame, Manathrust, Lightning, Pulverizing Auger and Ice Shards are permanently turned into 3-wide beams spells.
		In addition they have access to the unique Thaumaturgy class tree:
		- Orb of Thaumaturgy: a temporary orb that duplicates any beam spells that you cast
		- Multicaster: When casting a beam spell adds a chance to also cast an other archmage spell
		- Slipstream: Allows movement when casting beams
		- Elemental Array Burst: a powerful, multi-elemental beam spell that can inflict all elemental ailments and can not be resisted
		#CRIMSON#The fine spellcasting required for wide beams and all thaumaturgy spells can only happen while wearing cloth. Anything heavier will hinder the casting too much.
```
译文：
```text
奇术师是对元素法术有着深入理解的人，他们可以用新的方法融合元素，释放更强大的力量。
		火球术、奥术射线、闪电术、粉碎钻击和寒冰箭被永久转化为宽度为3的射线技能。
		此外，你获得独有的奇术师技能：
		- 奇术之球：召唤一个限时存在的球，可以复制你释放的射线类法术
		- 多重施法：当你释放射线类法术的时候，有一定几率追加释放一个其他的元素法师法术。
		- 能量滑流：释放射线类法术的时候可以移动。
		- 元素阵爆发：发射强力的多元素射线，可以施加所有元素异常状态，无法被元素抗性抵抗
		#CRIMSON#只有在身穿长袍的时候，才可以使用宽度为3的射线以及奇术技能。任何更重的护甲都会阻碍你的施法。
```

## entry-02494
位置：mod-tome.lua:31645；section：mod-tome/data/talents/uber/str.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You accurately jump to the target and deal 200%% weapon damage to all foes within radius 1 on impact as well as dazing them for 3 turns.
		When you jump you free yourself from any stun, daze and pinning effects.
```
译文：
```text
你跃向目标地点，对 1 码半径范围内的所有敌人造成 200%% 的武器伤害，并使它们眩晕 3 回合。
		落地后，你解除自身眩晕、定身和震慑效果。
```

## entry-02495
位置：mod-tome.lua:31655；section：mod-tome/data/talents/uber/str.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Massive Blow
```
译文：
```text
巨力重击
```

## entry-02496
位置：mod-tome.lua:31669；section：mod-tome/data/talents/uber/str.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
For 8 turns you gain the mass and power of a star, drawing all creatures within radius 5 toward you and dealing %0.2f fire, %0.2f light and %0.2f physical damage to all foes and reducing their damage dealt by 30%%.
		Foes closer to you take up to 150%% damage.
		The damage will increase with your Strength.
```
译文：
```text
你获得 8 回合的星之引力，将周围 5 码范围内的所有生物向你拉扯，并对所有敌人造成 %0.2f 火焰、%0.2f 光系和 %0.2f 物理伤害。他们所造成的伤害减少30%%。
		距离越近，敌人受到的伤害越高，最高为 150%%。
		伤害值受力量值加成。
```

## entry-02497
位置：mod-tome.lua:31676；section：mod-tome/data/talents/uber/str.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your strength is legendary; fatigue and physical exertion mean nothing to you.
		Your fatigue is permanently set to 0, carrying capacity increased by 500, and strength increased by 50 and you gain a size category.
```
译文：
```text
你是如此强壮，永不疲倦。
		疲劳值永久为 0 且负重上限增加 500 点。
		你增加 50 点力量并且体型 +1。
```

## entry-02498
位置：mod-tome.lua:31684；section：mod-tome/data/talents/uber/str.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You have sided with Slasul and helped him vanquish Ukllmswwik. You are now able to breathe underwater with ease.
		You have also learned to use tridents and other exotic weapons easily (talent level %d of Exotic Weapon Mastery), and can Spit Poison (talent level %d) as nagas do. These are bonus talent levels that increase with your character level.
		In addition, should Slasul still live, he may have a further reward for you as thanks...
```
译文：
```text
你站在萨拉苏尔一方并帮助他解决了乌克勒姆斯维奇。你现在可以轻松地在水下呼吸。
		同时，你能轻易学会如何使用三叉戟和其他特殊武器（获得 %d 级特殊武器掌握），并且可以像娜迦一样喷吐毒素（等级 %d）。这些是额外的技能等级，随人物等级增长。
		此外，若萨拉苏尔仍然存活，他还会送你一份大礼…
```

## entry-02499
位置：mod-tome.lua:31690；section：mod-tome/data/talents/uber/str.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
A strong body is key to a strong mind, and a strong mind can be powerful enough to make a strong body.
		This prodigy grants a Mindpower bonus equal to 60%% of your Strength.
		Additionally, you treat all weapons as having an additional 40%% Willpower modifier.
```
译文：
```text
强壮的身体才能承载强大的精神。而强大的精神却可以创造一个强壮的身体。
		获得相当于你 60%% 力量值的精神强度增益。
		此外，你的所有武器都会有额外的 40%% 意志修正加成。
```

## entry-02500
位置：mod-tome.lua:31700；section：mod-tome/data/talents/uber/str.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
During your studies of celestial forces you came in contact with an entity far beyond Eyal: the living incarnation of a Star!
		By allying yourself with it you can gain its power!

		Grants multiple benefits:
		- The strength of your bond is so strong that you can now #GOLD#wield a two-handed weapon and a shield together#LAST#
		- 50%% of all damage you deal is converted to #GOLD#light damage#LAST#
		- #GOLD#Gravitic Effulgence#LAST#: whenever your Weapon of Light hits the damage is now a radius 2 sphere and all foes in range 5 are drawn to it. (You can toggle this effect)
		- The damage and chance to trigger of #GOLD#Searing Sight#LAST# is doubled
		- Whenever #GOLD#Sun's Vengeance#LAST# triggers the remaining cooldown of Judgement is reduced by 6.
		- If you also know #GOLD#Irresistible Sun#LAST#, it will set the fire and light resistances of those affected to 0%%

		#{italic}##GOLD#Will you bind yourself to the Distant Sun?#{normal}#
		
```
译文：
```text
在研习天体之力时，你接触到了距离埃亚尔大陆极其遥远的存在：一颗恒星的化身！
        与它结盟，你将获得它的力量。

        增益：
        - 你的力量如此强大，你可以#GOLD#同时装备双手武器和盾牌#LAST#
        - 50%% 伤害转化为 #GOLD#光系伤害#LAST#
        - #GOLD#光辉引力#LAST#：光明之刃变成半径2的球形伤害，且可以将5格范围内的敌人拉过来（你可以开关此效果）。
		- #GOLD#灼热之视#LAST# 的伤害和触发概率翻倍
        - #GOLD#阳光之怒#LAST# 触发时，裁决的剩余冷却时间减少6回合。
        - 若你也习得 #GOLD#无御之日#LAST#，它将使受影响者的光系和火焰伤害抗性降低为 0%%

		#{italic}##GOLD#你会同遥远的太阳联合吗？#{normal}#
		
```

## entry-02501
位置：mod-tome.lua:31772；section：mod-tome/data/talents/uber/wil.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Be lucky already (at least +5 luck)
```
译文：
```text
拥有大运气（至少有+5幸运属性）
```

## entry-02502
位置：mod-tome.lua:31779；section：mod-tome/data/talents/uber/wil.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Spell Feedback
```
译文：
```text
法术反馈
```

## entry-02503
位置：mod-tome.lua:31781；section：mod-tome/data/talents/uber/wil.lua；source_tag：logCombat；args_order：None；special：None

原文：
```text
#LIGHT_BLUE##Source# punishes #Target# for casting a spell!
```
译文：
```text
#LIGHT_BLUE##Source#惩罚了#Target#的施法！
```

## entry-02504
位置：mod-tome.lua:31782；section：mod-tome/data/talents/uber/wil.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your will is a shield against assaults from crazed arcane users.
		Each time that you take damage from a spell, you punish the spellcaster with %0.2f mind damage.
		Also, they will suffer a 35%% spell failure chance (with duration equal to the cooldown of the spell they used on you).
		Note: this talent has a cooldown.
```
译文：
```text
你的意志是对抗癫狂奥术使用者的盾牌。
		每当你受到法术造成的伤害，你会惩罚施法者，使其受到 %0.2f 的精神伤害。
		同时，它们在对你使用的技能进入冷却的回合中，会受到 35%% 法术失败率惩罚。
		注意：该技能有冷却时间。
```

## entry-02505
位置：mod-tome.lua:31855；section：mod-tome/data/talents/undeads/ghoul.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s #YELLOW_GREEN#VOMITS#LAST# on the ground!
```
译文：
```text
%s在地上#YELLOW_GREEN#呕吐#LAST#！
```

## entry-02506
位置：mod-tome.lua:31869；section：mod-tome/data/talents/undeads/ghoul.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Gnaw your target for %d%% damage.  If your attack hits, the target may be infected with Ghoul Rot for %d turns.
		Each turn, Ghoul Rot inflicts %0.2f blight damage.
		Targets suffering from Ghoul Rot rise as friendly ghouls when slain.
		Ghouls last for %d turns and can use Gnaw, Ghoulish Leap, Stun, and Rotting Disease.
		The blight damage scales with your Constitution.
```
译文：
```text
啃噬目标，造成 %d%% 伤害。如果你的攻击命中，目标可能感染食尸鬼腐烂疫病，持续 %d 回合。
		食尸鬼腐烂疫病每回合造成 %0.2f 枯萎伤害。
		目标被杀死时会变成为你作战的友方食尸鬼。
		食尸鬼傀儡持续 %d 回合，可以使用啃噬、食尸鬼跳跃、震慑和腐烂疫病。
		受体质影响，枯萎伤害按比例加成。
```

## entry-02507
位置：mod-tome.lua:31896；section：mod-tome/data/talents/undeads/lich.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Your mere presence is terrying to any foes that dare stand against you.
		Every turn all foes in radius %d must make a mental save against your spellpower/physical power (whichever is highest) or become frightened (bypassing fear immunity), reducing all their saves by %d, all damage by %d%% and movement speed by %d%%.
		If they successfully resist, they are immune for %d turns.
```
译文：
```text
你的存在让任何胆敢对抗你的敌人的心中充满畏惧。
		每回合，半径 %d 码内的所有敌人必须使用精神豁免对抗你的法术强度/物理强度（取最高者），否则会被惊吓（无视恐惧免疫），他们的所有豁免降低 %d，所有伤害降低 %d%%，移动速度降低 %d%%。
		如果他们成功抵抗，他们可以免疫这一效果 %d 回合。
```

## entry-02508
位置：mod-tome.lua:31914；section：mod-tome/data/talents/undeads/lich.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You are so full with power that it overflows out of you whenever you cast a spell.
		Upon spell cast you have %d%% chances to boost the physical power, spellpower, mindpower and all saves of all friendly undeads in sight (including yourself) by %d for 4 turns.
```
译文：
```text
你的力量如此强大，每当你释放法术的时候，你的力量会喷涌而出。
		使用法术时，你有 %d%% 几率强化周围所有可见的友方不死生物（包括你自己），物理强度、法术强度、精神强度，所有豁免提升 %d，持续 4 回合。
```

## entry-02509
位置：mod-tome.lua:31930；section：mod-tome/data/talents/undeads/skeleton.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Reposition some of your bones, healing yourself for %d.
		At level 5, you will gain the ability to completely re-assemble your body should it be destroyed (can only be used once).
```
译文：
```text
重新组合你的骨头，治疗你 %d 点生命值。
		在等级 5 时你将会得到重塑自我的能力，被摧毁后可以原地满血复活（仅限 1 次）。
```

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Archer	弓箭手	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Archmage	元素法师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Attack speed	攻击速度	T.GAME.STAT	combat	tformat	preferred	core	角色面板 Speeds/Attack Speed 行；与 Global speed 全局速度区分
Celestial	天空系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Constitution	体质	T.GAME.STAT	combat	stat name	existing	global	
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Doomed	末日使者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Dread	噩灵	T.GAME.TALENT	talents	talent name	preferred	core	召唤物名称；与恐惧类普通文本区分
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Ghoul	食尸鬼	T.PN.RACE	creatures	birth descriptor name	existing	core	
Ghoulish Leap	定向跳跃	T.GAME.TALENT	talents	talent name	existing	core	
Giant	巨人	T.PN.RACE	creatures	birth descriptor name	existing	core	巨人种族总称
Gnaw	啃噬	T.GAME.TALENT	talents	talent name	preferred	core	食尸鬼近战技能及召唤物能力；与技能描述中的啃咬动作保持一致
Lich	巫妖	T.PN.RACE	creatures	birth descriptor name	existing	core	亡灵种族/形态
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Life Tap	生命分流	T.GAME.TALENT	talents	talent name	existing	core	
Lightning	闪电术	T.GAME.TALENT	talents	talent name	existing	core	
Luck	幸运	T.GAME.STAT	combat	stat name	existing	global	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Manathrust	奥术射线	T.GAME.TALENT	talents	talent name	existing	core	
Mental Save	精神豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Mental Save 行；与 Physical Save 物理豁免、Spell Save 法术豁免并列
Mindpower	精神强度	T.GAME.STAT	combat	tformat	preferred	multi	技能与物品机制说明中的精神强度属性；与 Willpower“意志”区分
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Physical Power	物理强度	T.GAME.STAT	combat	tformat	preferred	core	角色面板物理强度；力量属性描述与技能效果统一用此译名
Resistances	抗性	T.GAME.STAT	combat	_t	preferred	core	角色面板 Resistances base/cap 行；单系抗性为“X抗性”，全抗为 All Resists 全部抗性
Resolve	坚定意志	T.GAME.TALENT	talents	talent name	existing	core	反魔技能名；与同名临时效果及状态日志统一
Searing Sight	灼热之视	T.GAME.TALENT	talents	_t	preferred	core	灼热之视在职业进阶解锁文本中的引用
Searing Sight	灼热之视	T.GAME.TALENT	talents	talent name	preferred	core	光辉系技能；每回合灼烧光辉范围内敌人并可能使其眩晕且致盲，不写作“灼烧/灼热之矛”
Searing Sight	灼热之视	T.GAME.TALENT	talents	tformat	preferred	core	灼热之视在增益效果与职业进阶说明中的引用
Skeleton	骷髅	T.PN.RACE	creatures	birth descriptor name	existing	core	
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Slumber	沉睡	T.GAME.EFFECT	combat	_t	preferred	core	状态名；与同名技能统一
Slumber	沉睡	T.GAME.TALENT	talents	talent name	preferred	core	技能名；指睡眠状态，不是催眠动作
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Undead	不死族	T.PN.RACE	creatures	nil	existing	core	
Warrior	战士系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“战士系”
Wilder	野性系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Willpower	意志	T.GAME.STAT	combat	stat name	existing	global	
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
affinity	伤害吸收	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
assault	强袭	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
bleed	流血	T.GAME.DAMAGE	combat	damage type	existing	core	
bleed	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blight	枯萎	T.GAME.DAMAGE	combat	damage type	existing	core	
blight	枯萎	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blind	致盲	T.GAME.EFFECT	combat	effect subtype	existing	global	
celestial	天空	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
class	职业	T.GAME.TALENT_CATEGORY	talents	talent type	existing	core	
cleanse	洁净	T.GAME.ENTITY	items	entity keyword	preferred	core	仅适用于核心装备 ego 的 keywords/short_key，与 cleansing keyword 同一 cohort；不约束动作、技能说明或其他语境
cold	寒冷	T.GAME.DAMAGE	combat	damage type	existing	core	
cold	寒冷	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
corrupted	腐化	T.GAME.EFFECT	creatures	effect subtype	preferred	global	状态效果语境
corrupted	腐化	T.GAME.ENTITY	creatures	entity subtype	preferred	global	实体子类型语境
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
curse	诅咒	T.GAME.EFFECT	combat	effect subtype	existing	core	
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
darkness	暗影	T.GAME.DAMAGE	combat	damage type	existing	core	
darkness	暗影	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
daze	眩晕	T.GAME.EFFECT	combat	effect subtype	preferred	global	与 stun=震慑 区分；daze/LIGHTNING_DAZE 表示眩晕效果，不等同于震慑
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
disarm	缴械	T.GAME.EFFECT	combat	effect subtype	existing	global	
disease	疾病	T.GAME.EFFECT	combat	effect subtype	existing	core	
doom	末日	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	Cults of Entropy 技能树/技能类别名；P1 审核确认
dread	噩灵	T.GAME.ENTITY	creatures	entity name	preferred	core	Dread 召唤物实体
dread	惊骇	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	兽人战役 steam talent type；不是 Dread 召唤物名称
elemental	元素生物	T.GAME.ENTITY	creatures	entity type	preferred	global	entity type 统一为“元素生物”；entity keyword 与 effect subtype 保持“元素”
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
giant	巨人	T.GAME.ENTITY	creatures	entity type	existing	global	
golem	傀儡	T.GAME.ENTITY	creatures	entity subtype	existing	global	
golem	傀儡	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
gravity	重力	T.GAME.DAMAGE	combat	damage type	existing	core	
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
lightning	闪电	T.GAME.DAMAGE	combat	damage type	existing	core	
lightning	闪电	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
natural	自然	T.GAME.ENTITY	creatures	entity type	preferred	core	自然类陷阱的实体类型；entity keyword 语境可指“自然主义者”
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
poison	毒素	T.GAME.DAMAGE	combat	damage type	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
regeneration	回复	T.GAME.EFFECT	combat	effect subtype	existing	global	
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
ritch	里奇	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
ritual	仪式	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
slumber	沉睡	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	深度睡眠技能类型；与施加催眠的动作区分
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
temporal	时空	T.GAME.DAMAGE	combat	damage type	existing	core	
temporal	时空	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
trap	陷阱	T.GAME.ENTITY	items	entity name	preferred	global	陷阱实体（20 处）
undead	亡灵	T.GAME.ENTITY	creatures	entity type	existing	global	
undead	亡灵	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
weapons	武器	T.GAME.ENTITY	items	nil	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wound	创伤	T.GAME.EFFECT	combat	effect subtype	existing	global	
```
