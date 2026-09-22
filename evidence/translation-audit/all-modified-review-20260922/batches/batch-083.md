# batch-083：40 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-02692
位置：mod-tome.lua:35896；section：mod-tome/data/timed_effects/mental.lua；source_tag：logSeen；args_order：None；special：None

原文：
```text
%s collapses.
```
译文：
```text
%s 倒下了。
```

## entry-02693
位置：mod-tome.lua:35922；section：mod-tome/data/timed_effects/mental.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#F53CBE##Target# moves reluctantly!
```
译文：
```text
#F53CBE##Target#移动变得迟缓！
```

## entry-02694
位置：mod-tome.lua:35928；section：mod-tome/data/timed_effects/mental.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The gloom has stunned the target, reducing damage by 50%%, putting 4 random talents on cooldown and reducing movement speed by 50%%.  While stunned talents cooldown twice as slow.
```
译文：
```text
目标被黑暗光环震慑，伤害降低 50%%，随机 4 个技能进入 CD，移动速度降低 50%%。在震慑时技能冷却速度变慢一倍。
```

## entry-02695
位置：mod-tome.lua:35929；section：mod-tome/data/timed_effects/mental.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#F53CBE##Target# is stunned with fear!
```
译文：
```text
#F53CBE##Target#被恐惧所震慑！
```

## entry-02696
位置：mod-tome.lua:35934；section：mod-tome/data/timed_effects/mental.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The gloom has confused the target, making it act randomly (%d%% chance) and unable to perform complex actions.
```
译文：
```text
目标因黑暗光环陷入混乱，使其随机行动（%d%% 概率）且不能完成复杂动作。
```

## entry-02697
位置：mod-tome.lua:35935；section：mod-tome/data/timed_effects/mental.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#F53CBE##Target# is lost in despair!
```
译文：
```text
#F53CBE##Target#在绝望中迷失！
```

## entry-02698
位置：mod-tome.lua:35938；section：mod-tome/data/timed_effects/mental.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#F53CBE##Target# is dismayed!
```
译文：
```text
#F53CBE##Target#陷入惊慌失措！
```

## entry-02699
位置：mod-tome.lua:35940；section：mod-tome/data/timed_effects/mental.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# overcomes the dismay
```
译文：
```text
#Target#从惊慌失措中恢复
```

## entry-02700
位置：mod-tome.lua:35945；section：mod-tome/data/timed_effects/mental.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Stalking %s. Bonus level %d: +%d accuracy, +%d%% melee damage, +%0.2f hate/turn prey was hit.
```
译文：
```text
追踪 %s. 等级 %d：+%d 命中，+%d%% 近战伤害，攻击目标时 +%0.2f 仇恨/回合。
```

## entry-02701
位置：mod-tome.lua:35946；section：mod-tome/data/timed_effects/mental.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Prey damage modifier: %d%%.
```
译文：
```text
猎捕伤害加成：%d%%。
```

## entry-02702
位置：mod-tome.lua:35951；section：mod-tome/data/timed_effects/mental.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Being stalked by %s. Stalker bonus level %d: +%d accuracy, +%d%% melee damage, +%0.2f hate/turn prey was hit.
```
译文：
```text
目标被 %s 追踪。追踪等级 %d：+%d 命中，+%d%% 近战伤害，击中目标时 +%0.2f 仇恨/回合。
```

## entry-02703
位置：mod-tome.lua:35952；section：mod-tome/data/timed_effects/mental.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
 Prey damage modifier: %d%%.
```
译文：
```text
 猎捕伤害加成：%d%%。
```

## entry-02704
位置：mod-tome.lua:35955；section：mod-tome/data/timed_effects/mental.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
 (spellpower: %d, mindpower: %d
```
译文：
```text
 (法术强度：%d，精神强度：%d
```

## entry-02705
位置：mod-tome.lua:35975；section：mod-tome/data/timed_effects/mental.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Harassed
```
译文：
```text
被骚扰
```

## entry-02706
位置：mod-tome.lua:35976；section：mod-tome/data/timed_effects/mental.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The target has been harassed by its stalker, reducing damage by %d%%.
```
译文：
```text
目标受到追踪者骚扰，伤害降低 %d%%。
```

## entry-02707
位置：mod-tome.lua:35977；section：mod-tome/data/timed_effects/mental.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# has been harassed.
```
译文：
```text
#Target#受到骚扰。
```

## entry-02708
位置：mod-tome.lua:35978；section：mod-tome/data/timed_effects/mental.lua；source_tag：_t；args_order：None；special：None

原文：
```text
+Harassed
```
译文：
```text
+被骚扰
```

## entry-02709
位置：mod-tome.lua:35979；section：mod-tome/data/timed_effects/mental.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# is no longer harassed.
```
译文：
```text
#Target#不再受到骚扰。
```

## entry-02710
位置：mod-tome.lua:35980；section：mod-tome/data/timed_effects/mental.lua；source_tag：_t；args_order：None；special：None

原文：
```text
-Harassed
```
译文：
```text
-被骚扰
```

## entry-02711
位置：mod-tome.lua:36004；section：mod-tome/data/timed_effects/mental.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#F53CBE##Target# slows in the grip of madness!
```
译文：
```text
#F53CBE##Target#陷入疯狂之中速度减缓了！
```

## entry-02712
位置：mod-tome.lua:36012；section：mod-tome/data/timed_effects/mental.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Madness has confused the target, lowering mind resistance by %d%% and making it act randomly (%d%% chance)
```
译文：
```text
疯狂使目标混乱，降低目标 %d%% 精神抗性，使目标随机行动（%d%% 概率）。
```

## entry-02713
位置：mod-tome.lua:36083；section：mod-tome/data/timed_effects/mental.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The target erects a powerful kinetic shield capable of absorbing %d/%d physical%s or acid damage before it crumbles.
```
译文：
```text
目标施放一个念力护盾，在碎裂前吸收 %d/%d 物理%s或酸性伤害。
```

## entry-02714
位置：mod-tome.lua:36097；section：mod-tome/data/timed_effects/mental.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The target erects a powerful charged shield capable of absorbing %d/%d lightning%s or blight damage before it crumbles.
```
译文：
```text
目标施放一个充能护盾，在碎裂前吸收 %d/%d 闪电%s或枯萎伤害。
```

## entry-02715
位置：mod-tome.lua:36116；section：mod-tome/data/timed_effects/mental.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Decreases mind save by %d and increases mindpower by %d.
```
译文：
```text
降低精神豁免 %d 并增加精神强度 %d。
```

## entry-02716
位置：mod-tome.lua:36133；section：mod-tome/data/timed_effects/mental.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#F53CBE##Target# is plagued by inner demons!
```
译文：
```text
#F53CBE##Target#受心魔困扰！
```

## entry-02717
位置：mod-tome.lua:36158；section：mod-tome/data/timed_effects/mental.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Falls dead!
```
译文：
```text
死亡！
```

## entry-02718
位置：mod-tome.lua:36163；section：mod-tome/data/timed_effects/mental.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The thrill of combat improves the target's maximum life by %d%%, life regeneration by %0.2f, and stamina regeneration by %0.2f.
```
译文：
```text
目标被战斗激励提升生命上限 %d%%、提升生命回复 %0.2f、提升体力回复 %0.2f。
```

## entry-02719
位置：mod-tome.lua:36180；section：mod-tome/data/timed_effects/mental.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
Guarding against melee damage:  Will dismiss up to %d damage from the next %0.1f attack(s)%s.
```
译文：
```text
防御近战伤害：减少 %d 点伤害，剩余次数 %0.1f%s。
```

## entry-02720
位置：mod-tome.lua:36183；section：mod-tome/data/timed_effects/mental.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The target is rampaging! (+%d%% movement speed, +%d%% attack speed, +%d%% mind speed
```
译文：
```text
目标进入暴走状态！(+%d%% 移动速度，+%d%% 攻击速度，+%d%% 精神速度
```

## entry-02721
位置：mod-tome.lua:36184；section：mod-tome/data/timed_effects/mental.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
, +%d%% physical damage, +%d physical save, +%d mental save
```
译文：
```text
, +%d%% 物理伤害，+%d 物理豁免，+%d 精神豁免
```

## entry-02722
位置：mod-tome.lua:36193；section：mod-tome/data/timed_effects/mental.lua；source_tag：logPlayer；args_order：None；special：None

原文：
```text
#F53CBE#You feel your rampage slowing down. (-1 duration)
```
译文：
```text
#F53CBE#你感觉你的暴走正在消退。（-1持续时间）
```

## entry-02723
位置：mod-tome.lua:36231；section：mod-tome/data/timed_effects/mental.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The target is surrounded by a psychic field, absorbing 50%% of all damage (up to %d/%d).
```
译文：
```text
目标被灵能领域包围，吸收 50%% 所有伤害（最多 %d/%d）。
```

## entry-02724
位置：mod-tome.lua:36246；section：mod-tome/data/timed_effects/mental.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target# is no longer gaining feedback.
```
译文：
```text
#Target#不再获取反馈值。
```

## entry-02725
位置：mod-tome.lua:36249；section：mod-tome/data/timed_effects/mental.lua；source_tag：tformat；args_order：[2, 1]；special：None

原文：
```text
The target's subconscious has focused, increasing Mind resistance penetration by +%d%% and turning its attention on %s.
```
译文：
```text
目标的潜意识集中在 %s，增加%d%%精神抗性穿透。
```

## entry-02726
位置：mod-tome.lua:36256；section：mod-tome/data/timed_effects/mental.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The target is asleep and unable to perform most actions.  Every %d damage it takes will reduce the duration of the effect by one turn.
```
译文：
```text
目标陷入睡眠，无法执行大多数行动，每受到 %d 伤害缩短 1 回合持续时间。
```

## entry-02727
位置：mod-tome.lua:36262；section：mod-tome/data/timed_effects/mental.lua；source_tag：tformat；args_order：None；special：None

原文：
```text
The target is in a deep sleep and unable to perform most actions.  Every %d damage it takes will reduce the duration of the effect by one turn.
```
译文：
```text
目标陷入沉睡，无法执行大多数行动，每受到 %d 伤害缩短 1 回合持续时间。
```

## entry-02728
位置：mod-tome.lua:36299；section：mod-tome/data/timed_effects/mental.lua；source_tag：_t；args_order：None；special：None

原文：
```text
#Target#'s focuses.
```
译文：
```text
#Target#集中了意志。
```

## entry-02729
位置：mod-tome.lua:36304；section：mod-tome/data/timed_effects/mental.lua；source_tag：_t；args_order：None；special：None

原文：
```text
Spell Feedback
```
译文：
```text
法术反馈
```

## entry-02730
位置：mod-tome.lua:36307；section：mod-tome/data/timed_effects/mental.lua；source_tag：_t；args_order：None；special：None

原文：
```text
+Spell Feedback
```
译文：
```text
+法术反馈
```

## entry-02731
位置：mod-tome.lua:36309；section：mod-tome/data/timed_effects/mental.lua；source_tag：_t；args_order：None；special：None

原文：
```text
-Spell Feedback
```
译文：
```text
-法术反馈
```

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Attack speed	攻击速度	T.GAME.STAT	combat	tformat	preferred	core	角色面板 Speeds/Attack Speed 行；与 Global speed 全局速度区分
Hate	仇恨值	T.GAME.RESOURCE	resources	nil	preferred	core	诅咒系职业资源；技能描述中统一不用“怒气”
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Lightning	闪电术	T.GAME.TALENT	talents	talent name	existing	core	
Mage	法师系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“法师系”
Mental Save	精神豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Mental Save 行；与 Physical Save 物理豁免、Spell Save 法术豁免并列
Mindpower	精神强度	T.GAME.STAT	combat	tformat	preferred	multi	技能与物品机制说明中的精神强度属性；与 Willpower“意志”区分
Mindpower: 	精神强度：	T.GAME.STAT	combat	_t	existing	core	源码标签包含尾随空格
Physical Save	物理豁免	T.GAME.STAT	combat	_t	preferred	core	角色面板 Physical Save 行；与 Spell Save 法术豁免、Mental Save 精神豁免并列
Spellpower	法术强度	T.GAME.STAT	combat	_t	existing	core	
Stamina	体力值	T.GAME.RESOURCE	resources	_t	existing	core	
acid	酸性	T.GAME.DAMAGE	combat	damage type	existing	core	
acid	酸性	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blight	枯萎	T.GAME.DAMAGE	combat	damage type	existing	core	
blight	枯萎	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
cooldown	冷却	T.GAME.EFFECT	combat	effect subtype	existing	global	
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
fear	恐惧	T.GAME.EFFECT	combat	effect subtype	existing	core	
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
lightning	闪电	T.GAME.DAMAGE	combat	damage type	existing	core	
lightning	闪电	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
madness	疯狂	T.GAME.EFFECT	combat	effect subtype	existing	global	
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.DAMAGE	combat	damage type	existing	core	
physical	物理	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
regeneration	回复	T.GAME.EFFECT	combat	effect subtype	existing	global	
resistance	抵抗	T.GAME.EFFECT	combat	effect subtype	existing	core	
shield	护盾	T.GAME.EFFECT	combat	effect subtype	existing	core	
sleep	睡眠	T.GAME.EFFECT	combat	effect subtype	existing	global	
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
```
