# batch-126：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-03953
位置：tome-orcs.lua:5416；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Fires your ammo at an enemy in range %d for %d%% weapon damage.  If this tinker is made of voratun you will fire an additional shot.
			This shot is a ranged melee attack but will use the ranged procs of your ammo as well.
```
译文：
```text
向在 %d 码范围内的一个敌人开火造成 %d%% 的武器伤害。如果手炮是由沃瑞钽钢制作的，你能多一次额外的射击。射击是远程攻击将会触发弹药特效。
```

## entry-03954
位置：tome-orcs.lua:5419；section：tome-orcs/data/talents/steam/other.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Not enough space to summon!
```
译文：
```text
没有足够的空间召唤！
```

## entry-03955
位置：tome-orcs.lua:5422；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Quickly create a psionic-enhanced metal contraption that lures all your foes to it and reflects %d%% of the damage it takes to its attackers.
		The contraption will have %d life and last 5 turns.
		Damage, life, resists, and armor scale with your Steampower.
```
译文：
```text
快速制造一个灵能强化的金属装置，吸引所有敌人攻击它，并将其所受伤害的 %d%% 反弹给攻击者。
该装置拥有 %d 点生命值，持续 5 回合。
其伤害、生命值、抗性和护甲随你的蒸汽强度提升。
```

## entry-03956
位置：tome-orcs.lua:5437；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Activate the pistons to crush your target for %d turns and dealing %d%% unarmed melee damage.
		While the target is held it can not move and its armour and defense are reduced by %d.
		#{italic}#Crush their bones!#{normal}#
```
译文：
```text
激活活塞碾压你的目标 %d 回合，并造成 %d%% 的徒手伤害。
被碾压的目标会被定身，且其护甲和闪避减少 %d。
#{italic}#压碎他们的骨头 !#{normal}#
```

## entry-03957
位置：tome-orcs.lua:5444；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Grab the target and pull them towards you, striking for %d%% unarmed melee damage, and if you hit, pinning them for %d turns.
```
译文：
```text
抓住目标把目标向你拉拢，造成 %d%% 的徒手伤害，如果命中，目标定身 %d 回合。
```

## entry-03958
位置：tome-orcs.lua:5470；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You fire a cone of blighted needles, hitting everything in a frontal cone of radius %d for %0.2f physical damage.
		Each creature hit has a %d%% chance of being infected by a random disease, doing %0.2f blight damage and reducing either Constitution, Strength or Dexterity by %d for 20 turns.
		The damage and disease effects increase with your Steampower.
```
译文：
```text
你射出一片枯萎的针，打击 %d 码锥形范围内的目标，造成 %0.2f 的物理伤害。
每个命中目标都有 %d%% 几率感染一种随机疾病，造成 %0.2f 枯萎伤害同时降低体质，力量或敏捷 %d 点持续 20 回合。
		伤害和疾病效果受蒸汽强度加成。
```

## entry-03959
位置：tome-orcs.lua:5476；section：tome-orcs/data/talents/steam/other.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s shreds through sandwalls!
```
译文：
```text
%s 挖开沙墙！
```

## entry-03960
位置：tome-orcs.lua:5483；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Throw a cone of healing with radius %d, healing other mechanical creatures (steam spiders) for %d.
		The healing will increase with your Steampower.
```
译文：
```text
释放一片锥形半径 %d 码的修理器，修复机械生物（蒸汽蜘蛛）%d 生命值。
　　治疗量受蒸汽强度加成。
```

## entry-03961
位置：tome-orcs.lua:5486；section：tome-orcs/data/talents/steam/other.lua；source_tag：talent name；args_order：None；special：None

原文：
```text
Arcane Disruption Wave
```
译文：
```text
奥术干扰波
```

## entry-03962
位置：tome-orcs.lua:5492；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Shatters the mind of your victim, giving you full control over its actions for 6 turns.
		When the effect ends, you pull out your mind and the victim's body collapses, dead.
		This effect does not work on rares, bosses, or undead.
		.
```
译文：
```text
粉碎你的受害者的内心，给你完全控制其行为 6 回合。
　　当效果结束时，你抽出了自己的思维，受害者的身体会崩溃，死亡。
　　稀有怪、boss、亡灵不受控制。
```

## entry-03963
位置：tome-orcs.lua:5508；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Throw a handful of dust that rapidly oxidises, releasing a blinding light.
		Creatures in a cone of radius %d are blinded for %d turns.
		The blindness effect is applied with your Steampower.
```
译文：
```text
扔一把尘土，迅速氧化，释放出眩目的光芒。
		致盲锥形半径 %d 码内的生物 %d 回合。
		致盲强度受蒸汽强度加成。
```

## entry-03964
位置：tome-orcs.lua:5515；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Throw a handful of dust that is very itchy to touch.
		Creatures in a cone of radius %d are itchy for %d turns, causing them to fail talents %d%% of the time.
		The itchiness effect is applied with your Steampower.
```
译文：
```text
释放一把痒痒粉。
		锥形半径 %d 码内的生物 %d 回合内很痒，导致它们释放技能 %d%% 几率失败。
		致痒强度受蒸汽强度加成。
```

## entry-03965
位置：tome-orcs.lua:5521；section：tome-orcs/data/talents/steam/other.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the explosion!
```
译文：
```text
%s 抵抗了爆炸！
```

## entry-03966
位置：tome-orcs.lua:5522；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Throw a grenade at your foes, dealing %0.2f physical damage in radius %d.
		Creatures hit will also be stunned for %d turns.
		The stun effect is applied with your Steampower.
```
译文：
```text
向你的敌人投掷手榴弹，造成 %0.2f 物理伤害，半径 %d 码。
　　目标也会震慑 %d 回合。
　　震慑强度受蒸汽强度加成。
```

## entry-03967
位置：tome-orcs.lua:5552；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You fire a special explosive shot with your steamgun(s) at a spot within range.
		When each shot reaches its target, it does normal steamgun damage and explodes within radius %d, which does %0.2f physical damage.
		This talent does not use ammo as it is the ammo.
```
译文：
```text
你使用蒸汽枪在射程内制造一场特殊的爆炸。
　　当每一个弹片击中它的目标，造成正常蒸汽枪伤害和半径 %d 码内的爆炸，造成 %0.2f 的物理伤害，
　　这个技能不使用弹药。
```

## entry-03968
位置：tome-orcs.lua:5573；section：tome-orcs/data/talents/steam/other.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s is knocked back!
```
译文：
```text
%s 被击退！
```

## entry-03969
位置：tome-orcs.lua:5593；section：tome-orcs/data/talents/steam/other.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s resists the pull!
```
译文：
```text
%s抵抗了拖动！
```

## entry-03970
位置：tome-orcs.lua:5594；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You fire a special hook shot with your steamgun(s) at a target creature or location.
		If you target a creature, they are pulled up to %d tiles towards you.
		If you target an empty tile, you are pulled up to %d tiles towards it.
		This talent does not use ammo as it is the ammo.
```
译文：
```text
你使用蒸汽枪发射特殊弹药打击目标或某处
如果你的目标是一个生物，他们被拉向你 %d 码
如果你的目标是一个空地，你会被拉向空地 %d 码
这个技能不使用弹药。
```

## entry-03971
位置：tome-orcs.lua:5610；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You fire a special voltaic shot with your steamgun(s) at a target for 100%% weapon damage as lightning.
		The shot will release powerful electrical currents at up to %d nearby enemies. 
		Each bolt does %0.2f lightning damage.
		This talent does not use ammo as it is the ammo.
		Bolt damage scales with Steampower.
```
译文：
```text
你使用蒸汽枪发射特殊弹药打击目标造成 100%% 闪电武器伤害。
这将释放强大的电流，打击周围 %d 的敌人。
每个闪电球造成 %0.2f 的闪电伤害
这个技能不使用弹药
闪电球伤害受蒸汽强度加成。
```

## entry-03972
位置：tome-orcs.lua:5628；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You fire a special botanical shot with your steamgun(s) at a target for 100%% weapon damage as nature.
		The shot will release spores which grow into Nourishing Moss in a radius of %d for %d turns.
		Each turn the moss deals %0.2f nature damage to each foe within its radius.
		This moss has vampiric properties and heals the user for %d%% of the damage done.
		This talent does not use ammo as it is the ammo.
		Moss damage scales with Steampower.
```
译文：
```text
你使用蒸汽枪发射特殊弹药打击目标造成 100%% 自然武器伤害。
将释放孢子生长成半径 %d 的苔藓 %d 回合。
每回合苔藓造成 %0.2f 自然伤害对半径内的每一个敌人。
这种苔藓有吸血特性，伤害的 %d%% 治愈使用者。
这个技能不使用弹药
苔藓伤害受蒸汽强度加成。
```

## entry-03973
位置：tome-orcs.lua:5649；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You fire a special toxic shot with your steamgun(s) at a target for 100%% weapon damage as blight.
		The shot will release heavy metals into the target, inflicting %0.2f blight damage per turn and reducing their global speed by %d%% for %d turns.
		This talent does not use ammo as it is the ammo.
		Toxin strength scales with Steampower.
```
译文：
```text
你使用蒸汽枪发射特殊弹药打击目标造成 100%% 枯萎武器伤害。
向目标释放重金属，造成每回合 %0.2f 枯萎伤害，并且降低整体速度 %d%% %d 回合。
这个技能不使用弹药。
枯萎伤害受蒸汽强度加成。
```

## entry-03974
位置：tome-orcs.lua:5667；section：tome-orcs/data/talents/steam/other.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Allows the use of Technomancy spells.
		Grants a magical steam reserve that regenerates %d steam per 10 mana spent.
		Grants Spellpower based on current steam level (currently %d; %d%% steam filled).
		Outside of combat, you relax and let your steam reserve slowly wither away.
		#{italic}#Metal Arcane Power!#{normal}#
```
译文：
```text
允许使用科技法术，
		获得一个魔法的蒸汽储备，每消耗10点法力值获得 %d 蒸汽。
		根据当前蒸汽等级获得法术强度（目前 %d；充满了 %d%% 蒸汽）
		在战斗外，你放松了控制，蒸汽储备会逐渐消退。
		#{italic}#金属奥术力量！#{normal}#
```

## entry-03975
位置：tome-orcs.lua:5702；section：tome-orcs/data/talents/steam/physics.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Increases the capacity of your steam tank by %d.
```
译文：
```text
增加你的蒸汽容量 %d。
```

## entry-03976
位置：tome-orcs.lua:5718；section：tome-orcs/data/talents/steam/psytech-gunnery.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Using psionic energies you overheat your shot, making it deal %d%% damage.
		If the shot hits a wet foe it will vaporize, removing the wet effect and dealing %0.2f fire damage in a radius 4.
```
译文：
```text
使用灵能加热子弹，造成 %d%% 武器伤害。
		子弹命中处于浸湿状态的目标时将气化，除去浸湿状态，在半径 4 范围内造成 %0.2f 火焰伤害。
```

## entry-03977
位置：tome-orcs.lua:5742；section：tome-orcs/data/talents/steam/sawmaiming.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You "gently" slam your saws into the wounds of a creature, dealing %d%% weapon damage and deepening the wounds.
		All bleeding wounds durations are increased by %d turns and the damage by %d%% (this may be done only once per bleeding effect).
		When this happens a gush of blood is projected in a narrow cone of radius 4, dealing %0.2f physical damage to all creatures.
		The power and damage improves with your Steampower.
		#{italic}#The marvels of technology, now at the service of true butchery!#{normal}#
```
译文：
```text
你 " 轻柔 " 地将链锯放在目标的伤口上，造成 %d%% 武器伤害并加深伤口。
		所有流血伤口持续时间增加 %d 回合，伤害增加 %d%% （每项流血最多触发一次）。
		效果触发时，血流将喷射而出，对 4 码锥形范围内所有生物造成 %0.2f 物理伤害。
		伤害受蒸汽强度加成。
		#{italic}#一切技术，皆为屠杀 !#{normal}#
```

## entry-03978
位置：tome-orcs.lua:5815；section：tome-orcs/data/talents/steam/steam.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Control your mindstar and infuse it with steamtech.
```
译文：
```text
掌握你的灵晶，并用蒸汽科技强化它。
```

## entry-03979
位置：tome-orcs.lua:5825；section：tome-orcs/data/talents/steam/steam.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Wield powerful steamtech tools of destruction.
```
译文：
```text
装备用来毁灭的强大蒸汽科技工具。
```

## entry-03980
位置：tome-orcs.lua:5835；section：tome-orcs/data/talents/steam/steam.lua；source_tag：log；args_order：None；special：None

原文：
```text
#VIOLET#EUREKA!
```
译文：
```text
#VIOLET#我发现了！
```

## entry-03981
位置：tome-orcs.lua:5836；section：tome-orcs/data/talents/steam/steam.lua；source_tag：saySimple；args_order：None；special：None

原文：
```text
#VIOLET#EUREKA!#WHITE# Schematic learnt: #LIGHT_BLUE#%s
```
译文：
```text
#VIOLET#我发现了！#WHITE# 已学习配方：#LIGHT_BLUE#%s
```

## entry-03982
位置：tome-orcs.lua:5838；section：tome-orcs/data/talents/steam/steam.lua；source_tag：_t；args_order：None；special：None

原文：
```text
 #LIGHT_BLUE#(known)#LAST#
```
译文：
```text
 #LIGHT_BLUE#（已学会）#LAST#
```

## entry-03983
位置：tome-orcs.lua:5839；section：tome-orcs/data/talents/steam/steam.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#{italic}#* ...perhaps more to discover...#{normal}#
```
译文：
```text
#{italic}#* ……可能还可以找到更多……#{normal}#
```

## entry-03984
位置：tome-orcs.lua:5853；section：tome-orcs/data/talents/steam/thoughts-of-iron.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Melding psionics with steamtech you create 5 mind drones at your sides that fly towards your target.
		If they encounter a creature they will latch on it and bore into its skull for 6 turns, disrupting its thoughts.
		Disrupted creatures have %d%% chances to fail to use talents and suffer a -%d%% reduction to fear and sleep immunity.
```
译文：
```text
将灵能和蒸汽科技结合，你在身边制造 5 只精神雄蜂飞向目标。
		雄蜂接触到生物时，将进入其大脑 6 回合，干扰思考能力。
		受影响的生物有 %d%% 几率使用技能失败，同时恐惧和睡眠免疫减少 %d%%。
```

## entry-03985
位置：tome-orcs.lua:5890；section：tome-orcs/data/talents/steam/turrets.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
Not enough space to summon!
```
译文：
```text
没有足够的空间召唤！
```

## entry-03986
位置：tome-orcs.lua:5902；section：tome-orcs/data/talents/steam/turrets.lua；source_tag：_t；args_order：None；special：None

原文：
```text
An automated turret equiped with a flamethrower.
```
译文：
```text
一个装备火焰喷射器的自动炮台。
```

## entry-03987
位置：tome-orcs.lua:5914；section：tome-orcs/data/talents/steam/turrets.lua；source_tag：_t；args_order：None；special：None

原文：
```text
An automated turret emitting a healing mist.
```
译文：
```text
一个可以喷射治疗迷雾的自动炮台。
```

## entry-03988
位置：tome-orcs.lua:5921；section：tome-orcs/data/talents/steam/turrets.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Upgrade the target turret, granting it %d%% increased maximum life and enhanced abilities based on type:
		Steamgun: Gains a second steamgun dealing %d%% damage, and every 3 turns will fire a rocket dealing %d%% steamgun damage as fire in radius 2.
		Flame: Increases damage by %d%%, range by %d, and every 3 turns will project a vortex of superheated air that drags targets within range %d towards the turret as well as dealing normal flamethrower damage.
		Medic: Increases healing on affected targets by %d%%, and has a %d%% chance to cleanse a negative effect each turn.
```
译文：
```text
升级目标炮台，使其获得 %d%% 最大生命值，并根据其类型，获得以下的特殊能力：
		蒸汽枪炮台：获得第二把造成 %d%% 伤害的蒸汽枪，每 3 回合会发射一枚火箭，在 2 码半径内造成 %d%% 火焰蒸汽枪伤害。
		火焰炮台：增加 %d%% 伤害和 %d 射程，每过 3 回合，会在 %d 码范围内喷出灼热蒸汽的漩涡，将所有敌人拉向炮台，并造成标准喷火伤害。
		医疗炮台：增加对目标的治疗量 %d%%，且每回合有 %d%% 几率清除目标身上一个负面效果。
```

## entry-03989
位置：tome-orcs.lua:5931；section：tome-orcs/data/talents/steam/turrets.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Deploy a defensive emplacement around you, summoning 2 guardian turrets in adjacent tiles for %d turns. Guardian turrets redirect %d%% of all damage taken by other adjacent allies (other than fellow guardian turrets) to themselves, and each is armed with a powerful turret capable of firing piercing bullets.
			Guardian Turrets gain %0.2f ranks in Steamgun Mastery based on your Hunker Down talent level.
```
译文：
```text
进入守备模式，在身边召唤 2 个守卫炮台，持续 %d 回合。守卫炮台会将身边盟友（不包括其他守卫炮台）所受到所有伤害的 %d%% 转移到自己身上，并且它们装备有强力的电磁炮，可以发射贯穿敌人的子弹。
		守卫炮台具有 %0.2f 蒸汽枪精通技能，技能等级取决于你炮台守卫技能等级。
```

## entry-03990
位置：tome-orcs.lua:5951；section：tome-orcs/data/talents/uber/cun.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
You are adept at wreaking havoc onto your foes!
		Any time you deal damage to a creature you apply the Incoming Disasters effect for 20 turns.
		Each time you (or any others) would try to apply a cross-tier effect to this creature, you also try to apply the other two.
		In addition your physical, steam, spell and mind powers are increased by %d.
		The powers increase scales of your Cunning.
```
译文：
```text
你很擅长给你的敌人带来灾难！
		任何时候你对一个生物造成伤害，你会对它施加灾难临近效果，持续20回合。
		每次你（或任何其他目标）尝试对这个生物施加越层效果时，也将尝试施加其他两个越层效果。
		此外，你的物理，蒸汽，法术和精神强度增加 %d。
		强度增加值受灵巧值加成。
```

## entry-03991
位置：tome-orcs.lua:5961；section：tome-orcs/data/talents/uber/cun.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Quaffed the Blood of Undeath, not already undead and not antimagic.
```
译文：
```text
喝下不死之血，不是不死族，也不是反魔。
```

## entry-03992
位置：tome-orcs.lua:5971；section：tome-orcs/data/talents/uber/cun.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Rak'Shor's Cunning (Skeleton)
```
译文：
```text
拉克·肖的狡诈（骷髅）
```

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Armour	护甲值	T.GAME.STAT	combat	_t	existing	core	英式拼写
Constitution	体质	T.GAME.STAT	combat	stat name	existing	global	
Crush	压碎	T.GAME.TALENT	talents	talent name	existing	core	
Cunning	灵巧	T.GAME.STAT	combat	stat name	existing	global	
Dexterity	敏捷	T.GAME.STAT	combat	stat name	existing	global	
Flame	火球术	T.GAME.TALENT	talents	talent name	existing	core	
Flamethrower	火焰喷射器	T.GAME.TALENT	talents	talent name	preferred	dlc	Embers of Rage 重装武器技能名；统一多个技能入口
Flamethrower	火焰喷射器	T.GAME.TALENT	talents	tformat	preferred	dlc	重装武器说明中的同名武器引用；与 talent name 保持一致
Global speed	全局速度	T.GAME.STAT	combat	_t	preferred	core	角色面板和教程中的全局行动速度；不写作“整体速度”或“全体速度”
Global speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	格式化状态说明中的句首机制名；与小写 global speed 统一
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Lightning	闪电术	T.GAME.TALENT	talents	talent name	existing	core	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Mana	法力值	T.GAME.RESOURCE	resources	_t	existing	core	
Not enough space to summon!	没有足够的空间召唤。	T.RUNTIME.LOG	combat	logSeen	preferred	global	召唤失败日志（22 处）
Psi	灵能值	T.GAME.RESOURCE	resources	_t	existing	core	
Psionic	灵能系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业类别名
Skeleton	骷髅	T.PN.RACE	creatures	birth descriptor name	existing	core	
Special	特殊	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Steam	蒸汽	T.GAME.RESOURCE	resources	_t	existing	dlc	Embers of Rage 角色资源
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Tinker	工匠系	T.GAME.CLASS	classes	birth descriptor name	existing	dlc	
Undead	不死族	T.PN.RACE	creatures	nil	existing	core	
ammo	弹药	T.GAME.ENTITY	items	entity type	existing	core	
antimagic	反魔法	T.GAME.EFFECT	combat	effect subtype	existing	global	
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
bleed	流血	T.GAME.DAMAGE	combat	damage type	existing	core	
bleed	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blight	枯萎	T.GAME.DAMAGE	combat	damage type	existing	core	
blight	枯萎	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blind	致盲	T.GAME.EFFECT	combat	effect subtype	existing	global	
blinding	致盲	T.GAME.DAMAGE	combat	damage type	existing	global	
cleanse	洁净	T.GAME.ENTITY	items	entity keyword	preferred	core	仅适用于核心装备 ego 的 keywords/short_key，与 cleansing keyword 同一 cohort；不约束动作、技能说明或其他语境
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cun	灵巧	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
dex	敏捷	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
disease	疾病	T.GAME.EFFECT	combat	effect subtype	existing	core	
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
fire	火焰	T.GAME.DAMAGE	combat	damage type	existing	core	
fire	火焰	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
global speed	全局速度	T.GAME.STAT	combat	_t	preferred	core	装备、技能和叙述中的全局行动速度机制；不写作“整体速度”
global speed	全局速度	T.GAME.STAT	combat	tformat	preferred	core	技能与状态说明中的全局行动速度机制；不写作“整体速度”或“全体速度”
heal	治疗	T.GAME.EFFECT	combat	effect subtype	existing	core	
healing	治疗	T.GAME.DAMAGE	combat	damage type	existing	global	治疗型伤害/效果类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
lightning	闪电	T.GAME.DAMAGE	combat	damage type	existing	core	
lightning	闪电	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mech	机械	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
mechanical	机械	T.GAME.ENTITY	creatures	entity type	existing	dlc	Embers of Rage 实体类型
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.DAMAGE	combat	damage type	existing	core	
nature	自然	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
other	其他	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
pin	定身	T.GAME.EFFECT	combat	effect subtype	existing	core	
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
psionic	灵能	T.GAME.EFFECT	combat	effect subtype	existing	global	
psionic	灵能	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
schematic	配方	T.GAME.ENTITY	items	nil	preferred	dlc	Embers of Rage 工匠物学习配方；统一实体子类型、说明、学习日志和配方物品名，不使用孤立的“设计图”
sleep	睡眠	T.GAME.EFFECT	combat	effect subtype	existing	global	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
steam	蒸汽	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Embers of Rage DLC 机制效果类型
steam	蒸汽	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	Embers of Rage 技能类别
steamgun	蒸汽枪	T.GAME.ENTITY	items	entity subtype	existing	dlc	
steamtech	蒸汽科技	T.GAME.ENTITY	creatures	entity subtype	existing	dlc	Embers of Rage 实体子类型
steamtech	蒸汽科技	T.GAME.TALENT_CATEGORY	talents	talent category	existing	dlc	
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
technomancy	科技法术	T.GAME.EFFECT	combat	effect subtype	existing	dlc	
tinker	蒸汽工具	T.GAME.ENTITY	items	entity type	existing	dlc	Embers of Rage 实体类型
trap	陷阱	T.GAME.ENTITY	items	entity name	preferred	global	陷阱实体（20 处）
turrets	炮台	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
undead	亡灵	T.GAME.ENTITY	creatures	entity type	existing	global	
undead	亡灵	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
voratun	沃瑞钽	T.GAME.ENTITY	items	entity subtype	preferred	global	最高级金属材料（22 处）；与 iron 铁、steel 钢并列
weapon	武器	T.GAME.ENTITY	items	entity type	existing	global	与复数 weapons 区分
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wound	创伤	T.GAME.EFFECT	combat	effect subtype	existing	global	
```
