# batch-121：1 条冻结译文

全程只读。输出中文自然语言，不要求 JSON。逐条写编号及「未发现问题」或疑点、证据。不可用空泛的“其余通过”替代编号覆盖。允许使用编号列表或表格。只审当前包条目；禁止读历史审核意见。

用户明确指定主代理只记录推进；Gemini 发现疑点后交 Codex/Sol 交叉核验，禁止写入或自动修复。

源码读取：见 ../source-access.json。engine/boot/tome 必须 git show 固定 commit，DLC 使用冻结目录但标注来源未固定。可沿相关调用链查看该固定版本公开源码，尤其属性的最终消费逻辑；不得凭英文或属性名推断机制。允许读取当前包涉及的同 section 译文作为上下文，仓库译文已固定在 7c38a53；不得读取其他审核记录。

术语按 source_tag/category/语境适用；不能以术语覆盖源码。

## entry-03866
位置：tome-orcs.lua:2959；section：tome-orcs/data/lore/pocket-time.lua；source_tag：_t；args_order：None；special：None

原文：
```text
<? Lore.init_pocket_time_data() ?>Once upon a time, there was a Halfling alchemist by the name of <?=Lore.pocket_time_winner.name?>.  Alongside her trusty golem, she marched into the Trollmire, disposing of all foes in her path; when she encountered Prox, though, and he bent down to roar mere inches from her face, well inside a bomb's blast radius, she panicked and pulled a vial off her belt--

Once upon a time, there was a Dwarven berserker by the name of <?=Lore.pocket_time_winner.name?>.  Fleeing through the halls of Reknor as his friend was cut down by Orcish warriors, he ran face-first into a couple of them and--

Once upon a time, there was a Cornac rogue by the name of <?=Lore.pocket_time_winner.name?>.  His traps made short work of Prox, but when Bill the Stone Troll tossed him around his lair, he lost his bearings and stepped on--

Once upon a time--

Once upon a time, there was a great hero, a Dwarven Stone-Warden by the name of <?=Lore.pocket_time_winner.name?>, who began her adventure swearing incomprehensibly about unfairness before shrugging and continuing onward.  She escaped from Reknor with her closest companion, used her natural powers to purge the Deep Bellow and The Maze of the corrupting forces therein, rescued a strange new creature called a "yeek" from the clutches of the murderous Subject Z, and even shrugged off boulders thrown at her by the giants of Daikara as she inexorably pushed forward, slaying so many threats that had harmed so many people before her.  She uncovered the long-lost Conclave Vault and put the last of the original Ogres to rest, rescued a damsel from the clutches of the Sect of Kryl-Feijan, and finally found herself standing at the gates of the tower of Dreadfell, her skills honed by her trials and laden with exotic equipment found in her travels.  Climbing through the waves of shambling undead, she finally faced The Master head-on, when a skeletal warrior struck her from behind.  A stunning blow from its warhammer struck her right where she'd applied a wild infusion, the only one she had.  Dazed and stumbling, trying to invoke its power, she only became lucid when a terrible cold crept up her limbs, encasing her in ice--

Once upon a time, there was a Thalore summoner by the name of <?=Lore.pocket_time_winner.name?>, who began her adventure right next to a snake that was unnaturally skilled with temporal magic--

Once upon a time, there was a terrible villain, an Ogre reaver by the name of <?=Lore.pocket_time_winner.name?>, who found himself fascinated by the corrupted crystalline structures of the Spellblaze Caverns.  He first drowned a Last Hope guard in the dead of night to steal her enchanted ring, then began to leave a trail of destruction throughout the land, feeding on the strength of those hewn with his battleaxe or impaled with his longsword, and growing ever more powerful with every death he caused.  He joined the cause of the Grand Corruptor in an assault on Zigur to ensure that nothing could stop his arcane plagues from spreading, then took the Heart of the Sandworm Queen to Spellblaze-tainted lands to pervert its natural blessing into a blighted font of suffering.  He sat and watched as a cult sacrificed a maiden to summon their demonic master just so he could kill it himself, and salivated at the prospect of traveling to the Far East and seeing four armies' worth of Orcs broken and bleeding, tumors and boils spreading across their skin as the life slowly left their eyes.  The finest soldiers of Vor Pride could do nothing to prevent him from raiding their armory, but one crippled and diseased Orc pulled himself up against its sealed doors and begged him not to open them; he simply laughed before crushing his skull under his boot as he walked toward it, then kicked the door down, only to feel his bone armor disintegrate under a storm of breath attacks from an army of unspeakably powerful multi-hued wyrms.  Even <?=Lore.pocket_time_winner.name?> knew when he had to flee from a fight, and clenched his fist as he charged his Phase Door rune; when the blinding flash of light cleared, he found himself mere inches from--

Once upon a time, there was a Doomelf by the name of <?=Lore.pocket_time_winner.name?>, freed from demonic mind-control by a lucky meteor strike, who set out to use her new-found powers to escape the orbital hell on which she was trapped.  Investigators and mutilators, designed for torturing captives but far too frail for direct combat, fell under her infernal blade nearly as easily as the unaltered Children of Ruby who had few skills outside clerical work, and soon she began to feel that the demonic magic she had been imbued with may have made her nearly unstoppable.  When a demonic statue called out to her, she thought nothing of trying to absorb more of its power, barely even noticing when the statue called forth a Champion of Urh'Rok--

Once upon a time, there was a Shalore Adventurer by the name of <?=Lore.pocket_time_winner.name?>, who was quite certain of what he was doing.  He'd learned an extremely uncommon set of abilities - great talent with unarmed martial arts, some psychic potential to swing a staff in the air while leaving his hands free, stone magic that used his punches as a focus to blast foes with a hailstorm of earthen missiles - and once he had enough practice to master a few of these, he started effortlessly destroying any foe he faced... until he encountered the Weirdling Beast.  The battle was intense, and soon, both were on the verge of death, on opposite sides of the fortress's foyer; the Adventurer knew he couldn't afford to rush in close to finish the beast off, so he launched a pair of earthen missiles at it instead.  However, the moment they left his hands, he felt the grip of hard bone around his waist, legs, and back, pulling him at an incomprehensible speed into the Weirdling Beast's grasp.  Perhaps <?=Lore.pocket_time_winner.name?> could have survived an ensuing fistfight, but he had been pulled faster than his own missiles could fly, and now he found himself between the stony projectiles and their original target--

Once upon a time, a great spirit put down its pen and closed its notebook, sighing in frustration.
```
译文：
```text
<? Lore.init_pocket_time_data() ?>从前，有个半身人炼金术师叫做<?=Lore.pocket_time_winner.name?>。和她可靠的傀儡一起，她向巨魔沼泽前进，把挡住她的敌人消灭殆尽；不过当她遇到了普洛克斯时，他弯下腰来在离她脸几英寸的地方大吼，正好在炸弹的爆炸范围之内，她慌张起来把一个炼金瓶从腰带上拽开————

从前，有个矮人狂战士名叫<?=Lore.pocket_time_winner.name?>。在瑞库纳的大厅逃离时，在他的朋友被兽人战士砍倒后，他直接向几个兽人正面冲去，然后————

从前，有个科纳克人盗贼名叫<?=Lore.pocket_time_winner.name?>。他的陷阱很快解决了普洛克斯，但当岩石巨魔比尔在他的巢穴里把他扔了出去，他失去平衡踩在了————

从前————

从前，有个大英雄，一个矮人岩石守卫名叫<?=Lore.pocket_time_winner.name?>，在开始她的旅程时发表了一番关于不公平的费解的话，然后耸肩继续前进。她与最亲近的同伴一道从瑞库纳逃离，使用了她的自然能力清除了深渊咆哮与迷宫里的堕落之力，从嗜杀的实验体Z的魔掌中拯救了一个奇怪的叫做“夺心魔”的新生物，甚至在势不可挡地推进时，甩开了岱卡拉的巨人向她扔去的巨石，消灭了伤害了以往许多人的威胁。她发现了失落的孔克雷夫地下实验室，让最后几个最初被造出来的食人魔安息，从克里尔·费扬邪教徒的魔掌中救出了一个姑娘，最终站在了恐惧王座的塔门前，技艺百经锤炼，满载旅程中找到的各种珍奇装备。她一边往上爬，一边与一波波蹒跚的不死生物而战，她终于见到了吸血鬼领主迎面而来。这是，一个骷髅战士从后袭来。当她想用她仅有的那一个狂暴纹身时，它的战锤挥击震慑了她。当她因震慑而失去平衡，想要激活纹身的力量，一阵可怕的寒流涌遍了她的四肢，把她包裹在冰块之中时，她才清醒过来————

从前，有个自然精灵召唤师叫做<?=Lore.pocket_time_winner.name?>, 在一条蛇旁开始了旅程，这条蛇不自然地精通时间魔法————

从前，有个可怕的恶棍，一个食人魔收割者叫做<?=Lore.pocket_time_winner.name?>，他发现自己为魔法大爆炸影响的山洞中被污染的晶体结构着迷。他首先在夜深人静之时淹死了一个最后的希望的守卫，偷走了她的附魔戒指，然后在大陆上一路留下他毁灭的轨迹，吸取着被他双手斧砍死或被他的长剑穿透的对手的力量，在造成一场场死亡的同时变得更强大。他参与了大腐化者的事业来袭击伊格，来确保没人能阻止他的奥术瘟疫散播，之后把沙虫女王的心脏带到魔法大爆炸污染的土地上，来把它的自然祝福腐化成一种枯萎的苦难力量。他对一个邪教献祭少女来召唤他们的恶魔主人袖手旁观，这样他能亲自杀死它。他旅行到远东，看到四支兽人大军溃散而流血，肿块和疮遍布他们的皮肤，同时生命缓慢地从眼中流失而垂涎不已。沃尔部落最好的战士对于他劫掠兵器库而无可奈何，但一个瘸腿而病弱的兽人堵在封印的门前求他别打开；他只是大笑，走向门，踩过兽人的头，在靴子下碾碎，之后把门踢倒，突然感觉到他的骨盾在一群无可言喻地强大的七彩龙的吐息风暴中解体。即使是<?=Lore.pocket_time_winner.name?>也知道什么时候该从战斗中逃跑，在激活相位门符文的同时握紧了拳头；当刺眼的闪光消失时，他发现自己几英寸外就是————

从前，有个魔化精灵叫<?=Lore.pocket_time_winner.name?>，由于一个好运天降的落星从恶魔的心灵控制中解脱，出发去用她新得到的力量来从她被困住的轨道地狱中逃脱。那些调查员和切割者是被设计来折磨囚徒，他们对于近身战斗来说过于脆弱，在她的烈火之刃面前，几乎就像是那些未被转变的，除了文书工作外没什么技能的红宝石之子那样轻松倒下，很快，她开始感觉她体内被灌注的恶魔魔法说不定已让她接近无敌。当她看到一个恶魔雕像时，她除了想吸收更多力量外没想别的，根本没注意到雕像召唤了一个乌鲁洛克的精英卫兵————


从前，有个永恒精灵冒险者叫<?=Lore.pocket_time_winner.name?>，他对于自己在做什么非常确信。他学会了一套相当不寻常的能力————了不起的空手武术天赋，一种在空中挥动法杖的心灵潜能，用拳击触发的石系魔法来用暴风般的石弹来击退敌人们————一旦他在这些方面都有了一些实战经验，他开始秒杀所有遇到的敌人……直到他遇到了异形触手。战斗非常激烈，不一会儿，双方都在死亡的边缘上，位于要塞前厅的两端；冒险者知道他没法冲上前近距离解决那野兽，因此他取而代之地向它发射了一双石弹。然而，当石弹从手中离开时，他感到坚硬的骨爪紧紧环绕腰、腿和后背，以一种无可理喻的速度把他拖入异形触手的手掌心。或许<?=Lore.pocket_time_winner.name?>可能会在接下来的近身拳击中活下来，但他被拖动的速度快于石弹的飞行，现在他发现自己处在这些石制投射物和他们原来的目标之间————

从前，一个伟大的灵魂放下了它的笔，合上了它的笔记本，沮丧地叹气。
```

## 相关术语快照
```tsv
Air	空气	T.GAME.RESOURCE	combat	_t	preferred	core	核心资源（resources.lua 定义 11 种之一）；面板 Air 行、空气容量/空气值语境统一
Alchemist	炼金术师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Berserker	狂战士	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Cornac	科纳克人	T.PN.RACE	creatures	birth descriptor name	existing	core	人类分支种族
Corruptor	腐化者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Crush	压碎	T.GAME.TALENT	talents	talent name	existing	core	
Doomelf	魔化精灵	T.PN.RACE	creatures	birth descriptor name	existing	dlc	Ashes of Urh'Rok 种族
Dread	噩灵	T.GAME.TALENT	talents	talent name	preferred	core	召唤物名称；与恐惧类普通文本区分
Dreadfell	恐惧王座	T.PN.PLACE	places	nil	existing	core	
Elf	精灵	T.PN.RACE	creatures	birth descriptor name	existing	core	精灵种族总称
Giant	巨人	T.PN.RACE	creatures	birth descriptor name	existing	core	巨人种族总称
Halfling	半身人	T.PN.RACE	creatures	birth descriptor name	existing	core	
Kick	踢	T.GAME.TALENT	talents	talent name	existing	global	
Last Hope	最后的希望	T.PN.PLACE	places	_t	existing	core	
Life	生命	T.GAME.RESOURCE	combat	_t	preferred	core	角色面板第一资源行；生命值语境统一用“生命值”，面板标签“生命”
Luck	幸运	T.GAME.STAT	combat	stat name	existing	global	
Magic	魔力	T.GAME.STAT	combat	stat name	existing	global	
Name	名称	T.UI.LABEL	ui	_t	preferred	global	界面标签（17 处）
Ogre	食人魔	T.PN.RACE	creatures	birth descriptor name	existing	core	
Orc	兽人	T.PN.RACE	creatures	birth descriptor name	existing	dlc	
Phase Door	相位之门	T.GAME.TALENT	talents	talent name	existing	core	
Reaver	收割者	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Rogue	盗贼	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Shalore	永恒精灵	T.PN.RACE	creatures	nil	existing	core	
Skin	皮肤	T.UI.LABEL	ui	birth facial category	existing	global	角色外观分类
Strength	力量	T.GAME.STAT	combat	stat name	existing	global	
Stunning Blow	震慑打击	T.GAME.TALENT	talents	talent name	existing	core	
Summon	召唤	T.UI.LABEL	ui	_t	preferred	global	召唤界面/技能按钮（18 处）；与召唤师职业名区分
Summoner	召唤师	T.GAME.CLASS	classes	birth descriptor name	existing	core	
Thalore	自然精灵	T.PN.RACE	creatures	nil	existing	core	
Trollmire	巨魔沼泽	T.PN.PLACE	places	_t	preferred	core	任务与地点叙述统一；troll 指巨魔，不是食人魔，与 narrative.tsv 的 trollmire→巨魔沼泽 一致；“Of trolls and damp caves”是任务标题，不作同名处理；2026-09-16 用户裁决，由 existing 升为 preferred
Undead	不死族	T.PN.RACE	creatures	nil	existing	core	
Vault	撑杆跳	T.GAME.TALENT	talents	talent name	existing	core	
Warrior	战士系	T.GAME.CLASS	classes	birth descriptor name	existing	core	职业描述中使用“战士系”
Yeek	夺心魔	T.PN.RACE	creatures	birth descriptor name	existing	core	
Zigur	伊格	T.PN.PLACE	places	nil	preferred	core	伊格兰斯教团的据点地名；与教团全称 Ziguranth「伊格兰斯」同源且紧密关联，但指称不同，见 society.tsv 的 Ziguranth 行。指地点时一律用「伊格」，不得写成「伊格兰斯」。
arcane	奥术	T.GAME.DAMAGE	combat	damage type	existing	global	
arcane	奥术	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
armor	护甲	T.GAME.ENTITY	items	entity type	existing	global	
assault	强袭	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Embers of Rage 技能树/技能类别名
bleed	流血	T.GAME.DAMAGE	combat	damage type	existing	core	
bleed	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blight	枯萎	T.GAME.DAMAGE	combat	damage type	existing	core	
blight	枯萎	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
blind	致盲	T.GAME.EFFECT	combat	effect subtype	existing	global	
blinding	致盲	T.GAME.DAMAGE	combat	damage type	existing	global	
book	书	T.GAME.ENTITY	items	entity type	existing	global	
cave	山洞	T.GAME.ENTITY	places	entity subtype	existing	global	
cold	寒冷	T.GAME.DAMAGE	combat	damage type	existing	core	
cold	寒冷	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
con	体质	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
corrupted	腐化	T.GAME.EFFECT	creatures	effect subtype	preferred	global	状态效果语境
corrupted	腐化	T.GAME.ENTITY	creatures	entity subtype	preferred	global	实体子类型语境
cut	流血	T.GAME.EFFECT	combat	effect subtype	existing	global	切割造成的流血效果
daikara	岱卡拉	T.NARRATIVE.LORE	narrative	newLore category	existing	core	
daze	眩晕	T.GAME.EFFECT	combat	effect subtype	preferred	global	与 stun=震慑 区分；daze/LIGHTNING_DAZE 表示眩晕效果，不等同于震慑
demon	恶魔	T.GAME.ENTITY	creatures	entity type	existing	global	
demonic	恶魔	T.GAME.EFFECT	combat	effect subtype	existing	dlc	Ashes of Urh'Rok DLC 机制效果类型
disease	疾病	T.GAME.EFFECT	combat	effect subtype	existing	core	
doom	末日	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	Cults of Entropy 技能树/技能类别名；P1 审核确认
doomelf	魔化精灵	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
dread	噩灵	T.GAME.ENTITY	creatures	entity name	preferred	core	Dread 召唤物实体
dread	惊骇	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	dlc	兽人战役 steam talent type；不是 Dread 召唤物名称
elf	精灵	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
giant	巨人	T.GAME.ENTITY	creatures	entity type	existing	global	
golem	傀儡	T.GAME.ENTITY	creatures	entity subtype	existing	global	
golem	傀儡	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
halfling	半身人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
ice	寒冰	T.GAME.DAMAGE	combat	damage type	existing	global	
infusion	充能	T.GAME.TALENT_CATEGORY	talents	talent type	preferred	core	炼金术师为宝石炸弹注入元素力量的技能类型；区别于刻印物品 Infusion（纹身）
light	光系	T.GAME.DAMAGE	combat	damage type	existing	core	与装备重量语境的“轻甲”区分
light	光系	T.GAME.EFFECT	combat	effect subtype	existing	global	与装备重量“轻甲”区分
light	轻甲	T.GAME.ENTITY	items	entity subtype	preferred	core	护甲材质子类（armor/light，45 处）与光元素/光球（elemental/orb/light，2 处）共享同一运行时键 （引擎 _t(subtype,entity subtype) 不带 type 参数）；按多数与物品分类 UI 裁决为“轻甲”，wisp 等光类实体提示显示“元素生物 / 轻甲”为已知局限
mag	魔力	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
mind	精神	T.GAME.DAMAGE	combat	damage type	existing	core	
multi-hued	多彩	T.GAME.ENTITY	creatures	entity subtype	preferred	global	实体生成修饰语；与 multihued entity subtype 的既有“多彩”统一，不使用名词性“混晶石”
natural	自然	T.GAME.ENTITY	creatures	entity type	preferred	core	自然类陷阱的实体类型；entity keyword 语境可指“自然主义者”
orc	兽人	T.GAME.ENTITY	creatures	entity subtype	existing	global	生物实体子类型
power	强度	T.GAME.EFFECT	combat	effect subtype	preferred	global	效果类别：physical power/spellpower 等强度增益，不是能量；entity keyword 语境仍译“能量”；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity keyword	preferred	core	物品词缀语境（of power 能量之）；与 effect subtype 的“强度”区分；P0 审核确认
power	能量	T.GAME.ENTITY	items	entity subtype	preferred	dlc	orcs 实体子类型语境；与 effect subtype 的“强度”区分；P0 审核确认
slow	减速	T.GAME.EFFECT	combat	effect subtype	existing	core	
speed	速度	T.GAME.EFFECT	combat	effect subtype	existing	global	
spell	法术	T.GAME.TALENT_CATEGORY	talents	talent category	existing	core	
spellblaze	魔法大爆炸	T.GAME.TALENT_CATEGORY	talents	talent type	existing	dlc	Ashes of Urh'Rok 技能树/技能类别名
spellblaze	魔法大爆炸	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与世界事件的其他标签区分
spellblaze	魔法大爆炸	T.PN.WORLD	places	effect subtype	existing	core	
staff	法杖	T.GAME.ENTITY	items	entity subtype	existing	global	
stone	石化	T.GAME.EFFECT	combat	_t	preferred	core	状态免疫面板 Stoning Resistance；与石化毒素（nature 伤害变体）同词根
str	力量	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
stun	震慑	T.GAME.EFFECT	combat	effect subtype	existing	core	
temporal	时空	T.GAME.DAMAGE	combat	damage type	existing	core	
temporal	时空	T.GAME.EFFECT	combat	effect subtype	existing	global	与 damage type 同名但语境不同
trap	陷阱	T.GAME.ENTITY	items	entity name	preferred	global	陷阱实体（20 处）
troll	巨魔	T.GAME.ENTITY	creatures	entity subtype	existing	global	
trollmire	巨魔沼泽	T.NARRATIVE.LORE	narrative	newLore category	preferred	core	与同类手札标题统一；troll 指巨魔，不是食人魔
undead	亡灵	T.GAME.ENTITY	creatures	entity type	existing	global	
undead	亡灵	T.GAME.TALENT_CATEGORY	talents	talent category	existing	global	
wil	意志	T.GAME.STAT	combat	stat short_name	existing	global	属性短名
wild infusion	野性纹身	T.GAME.ENTITY	items	entity name	preferred	core	物品实体名称；与 Wild infusion 技能名统一
zigur	伊格	T.NARRATIVE.LORE	narrative	newLore category	existing	core	与大写地点 Zigur 的源码标签区分
```
