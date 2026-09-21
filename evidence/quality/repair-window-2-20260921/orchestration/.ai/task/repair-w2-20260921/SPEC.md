# 修复窗口2：批243的五条译文

模式：implement；change_class=standard；Paseo MCP；translation_contextual_v2 schema 5。

授权：用户要求读取 handoff 接手推进翻译审核，每批完成后推送。依交接先收口窗口2，再开审核244。

允许任务内容写入：mod-tome.lua 中以下五个 source 的 target，及 evidence/quality/repair-window-2-20260921/ 下本窗口核验证据；最终交接允许 handoff.md。现阶段只实施五条 target 与本窗口证据，不修改 handoff，后续宿主另给确定状态。

禁止：不改 source/source_tag/args_order/special/占位符/markup/换行序列；不改术语库、其他条目、规则、检查器、旧证据。SCOPE 的 section 仅为来源锚点，不扩大编辑面。RW1-SIB-01/02 和 Archmage 均不在本范围。

新 preflight：.artifacts/i18n/repair-window/window2-20260921-preflight-2.json，必须真实成功且以此为准，旧 workset 只用于前置只读准备。

固定来源：commit:624a67329fe2ad440c5b344785a9c73fcf22ae63；宿主已按 git 对象读取 SOURCE-ANCHORS.json。所有目标均为 tome，无 DLC。

任务前 tracked diff 为空，既有 untracked 见 BASELINE-status.txt，不得删除或纳入提交。

验收：五条 target 实际修复；全条语义完整；LuaJIT 加载前后只改变允许 target，其他记录完全一致；strict lint、差异空白、占位符/markup/newline 不变量；源码值流证据（%d duration；%d%% crit mitigation；%d%% immunity）；独立 REVIEW 和 FINAL_REVIEW；完整 ci-gates（含构建）；DONE_VERIFIED；译文/证据双提交及两次 queue rebuild、单次 catalog/migration，最后 push。

EXECUTOR 不 stage/commit、不写 .ai，不调度 child。


## de6a65ed2bf9694bcff086b4d961aeeffa14868f69aeb11d997a75a84d71e421

section: mod-tome/init.lua

source_tag: init.lua load_tips

source: In the Age of Pyre the giant golem Atamathon was built with the sole purpose of stopping the orcish leader Garkul the Devourer. The golem was single-handedly destroyed by the orc, who then slaughtered an army of thousands before the demonic fighter was finally slain.

当前 target: 在烈火纪，人们建造了巨型傀儡阿塔玛森以对抗兽人首领吞噬者加库尔所领导的兽人军队。加库尔不仅孤身一人亲自干掉了傀儡王，在他倒下之前，还单枪匹马斩杀了上千人的部队。


## de83a721c1a9495beac993ede15beb5c703bd06d906eee24febc902d799c26d7

section: mod-tome/data/general/objects/world-artifacts.lua

source_tag: _t

source: These gloves make you feel rock steady! These magical gloves feel really soft to the touch from the inside. On the outside, magical stones create a rough surface that is constantly shifting. When you brace yourself, a magical ray of earth energy seems to automatically bind them to the ground, granting you increased stability.

当前 target: 这副手套让你觉得坚如磐石！这双充满魔力的手套从里面摸起来无比松软。在其外，魔法石创造了一个不断转动的粗糙表面。当你振作精神，一束包含大地能量的魔法射线会将它自动扎根在地面上，赋予你更高的稳定性。


## de87dbd2517ed4a4264e7b26a3e43784a1c4a845521a6f2584062d624ec33e8d

section: mod-tome/data/talents/gifts/summon-advanced.lua

source_tag: tformat

source: For %d turn(s), you have 100%% chance that your summons appear as a wild version.
		Each turn the chance disminishes.
		Wild creatures have one more talent/power than the base versions:
		- Ritch Flamespitter: Can fly in the air, spitting its Flamespit past creatures in the path of its target
		- Hydra: Can concentrate its breath into spits when allies would be caught in a breath, instead spitting a bolt
		- Rimebark: Can grab foes, pulling them into range of its ice storm
		- Fire Drake: Can emit a powerful roar to silence its foes
		- War Hound: Can rage, inreasing its critical chance and gaining armour penetration
		- Jelly: Can split into an additional jelly upon taking a large hit (jellies formed by splitting do not count against your summon cap)
		- Minotaur: Can rush toward its target
		- Stone Golem: Can disarm its foes
		- Turtle: Can force all foes in a radius into melee range
		- Spider: Can project an insidious poison at its foes, reducing their healing
		This talent requires Master Summoner to be active to be used.
		Effects scale with levels in summon talents.

当前 target: 你在 %d 回合内 100%% 召唤出一只野性模式的召唤兽。
		此概率每回合递减。
		野性召唤兽增加 1 个新的天赋：
		- 喷火里奇：可以在空中飞行，吐火不会被路径上的生物所阻挡。
		- 三头蛇：如果发现友军会被击中，则将吐息改为单体攻击。
		- 雾凇：可以抓取敌人，将它们拉进自己的冰风暴范围。
		- 火龙：可以用怒吼来沉默敌人
		- 战争猎犬：可以狂暴，增加它的暴击率和护甲穿透值
		- 果冻怪：可以在被攻击造成较大伤害的时候，分裂出一个果冻怪（分裂出的果冻怪不会占用你的召唤物上限）
		- 米诺陶：可以向目标冲锋
		- 岩石傀儡：可以缴械敌人。
		- 乌龟：可以嘲讽范围内敌人进入近战状态
		- 蜘蛛：可以向目标吐出剧毒，减少它们的治疗效果
		此技能只有在召唤精通激活时才能使用。
		技能效果受召唤物技能等级加成。


## de9af808fffcbe480b1c10f7948a421f6f7571f4015e5fa16557cc1cdc42fa85

section: mod-tome/data/talents/gifts/ooze.lua

source_tag: tformat

source: Your body's internal organs are indistinct, disguising your vital areas.
		You have a %d%% chance to shrug off all direct critical hits (physical, mental, spell).
		In addition you gain %d%% resistance to disease, poison, wounds and blindness.

当前 target: 你身体里的内脏全都融化在一起，隐藏了你的要害部位。
		你有 %d%% 几率摆脱任何（物理，精神，法术）暴击。
		你将额外获得 %d%% 的疾病、毒素、切割和目盲免疫。


## de9e666ad0b4d9f1774c91cd59a443c4bf424afe3f58e12961bad77bbdcb6336

section: mod-tome/data/general/objects/world-artifacts.lua

source_tag: _t

source: This wooden cup seems perpetually filled with a thick sap-like substance. Tasting it is exhilarating, and you feel intensely aware when you do so.

当前 target: 这个酒杯里装满了粘稠的物质，尝一口能提神醒脑。


## 宿主已核验的修复依据

1. 加库尔：sole purpose 指阻止首领本人；巨型傀儡不是傀儡王。保留最后 demonic fighter 的凶悍比喻，thousands 不缩成特定数字。

2. 手套：brace yourself 是稳住身体；shifting 不等于旋转；保留 seems，避免把风味文的射线写成额外运行机制。

3. Wild Summon：action 只赋 EFF_WILD_SUMMON，初始 chance=100，每回合乘0.66并取整；首行是召唤兽出现野性形态的概率，不是直接召出一只。乌龟野性附加 T_BATTLE_CALL，使目标移位；非基础 T_TAUNT。修正这两处并核对全条。

4. Anatomy：交接只补 direct 的方案不足。ooze.lua:254-270 → ignore_direct_crits → damage_types.lua:130-154 是按百分比削减额外暴击倍率，非 rng 概率；须以固定源码纠正英文过时描述。建议本句按实际含义“你受到的直接暴击（物理、精神、法术）的额外伤害降低 %d%%。”；不能说总伤害减少或概率免疫。原第三行 immunity 与字段吻合；首行不要增加解剖事实。宿主已撤回历史建议的概率解释，本窗口仅修此条，不全局扩展同类句。

5. 木杯：补回 wooden、seems perpetually、sap-like 与饮用时感官敏锐；不引入酒。

必须把修复前后、每条源码锚点、Anatomy 推翻旧概率解释、数值placeholder值流和不变量验证写入允许的受跟踪证据目录。源码事实与裁决区别清楚；不要声称 checker 或独立复审已完成。

## cycle 1 宿主补充裁决（HOST-CUT-01）
原先关于第三行“切割”已吻合的事实判断被固定源码/既有术语核验推翻。仅将 Anatomy 这条获准 target 的“疾病、毒素、切割和目盲免疫”改为“疾病、毒素、流血和目盲免疫”。依据 HOST-CUT-01.json 和 SOURCE-CUT-ANCHORS.json；没有新增可编辑 revision，没有术语库改动。旧冻结记录不修改。原“免疫”机制本身正确，修正的是状态名。
