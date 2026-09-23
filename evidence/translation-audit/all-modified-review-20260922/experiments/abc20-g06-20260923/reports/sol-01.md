40 条身份已与 entries.json 核对，引用的 DLC 源文件哈希也与 source-access 一致。复核已完成；我正在整理逐条判定和证据，避免把上游原文本身的表述当成译文新增错误。
---

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03373 | 存在问题 | C01、C02 |
| entry-03374 | 存在问题 | C03、C04 |
| entry-03375 | 存在问题 | C05 |
| entry-03376 | 存在问题 | C06 |
| entry-03377 | 存在问题 | C07 |
| entry-03378 | 存在问题 | C08–C11 |
| entry-03379 | 存在问题 | C12–C14 |
| entry-03380 | 存在问题 | C15、C16 |
| entry-03381 | 未发现问题 | 可辨文字与遮蔽结构保留 |
| entry-03382 | 存在问题 | C17 |
| entry-03383 | 存在问题 | C18 |
| entry-03384 | 存在问题 | C19 |
| entry-03385 | 未发现问题 | 名称语义相符 |
| entry-03386 | 未发现问题 | 留言语义相符 |
| entry-03387 | 未发现问题 | 名称语义相符 |
| entry-03388 | 存在问题 | C20–C24 |
| entry-03389 | 存在问题 | C25 |
| entry-03390 | 未发现问题 | 名称语义相符 |
| entry-03391 | 存在问题 | C26、C27 |
| entry-03392 | 存在问题 | C28 |
| entry-03393 | 存在问题 | C29 |
| entry-03394 | 存在问题 | C30–C32 |
| entry-03395 | 未发现问题 | 任务叙述的主要事件保留 |
| entry-03396 | 未发现问题 | 暗影效果与参数相符 |
| entry-03397 | 未发现问题 | 两次攻击、吸血与活力条件相符 |
| entry-03398 | 未发现问题 | 战斗日志语义相符 |
| entry-03399 | 未发现问题 | 酸池、自伤、抗性与亲和效果相符 |
| entry-03400 | 未发现问题 | 充能数与菜单用途相符 |
| entry-03401 | 未发现问题 | 护盾数值与反射比例相符 |
| entry-03402 | 存在问题 | C33 |
| entry-03403 | 未发现问题 | 敌我伤害及恶魔治疗条件相符 |
| entry-03404 | 未发现问题 | 触发、持续时间及亲和数值相符 |
| entry-03405 | 未发现问题 | 格挡触发与邪术列表相符 |
| entry-03406 | 未发现问题 | 近战触发与诅咒列表相符 |
| entry-03407 | 未发现问题 | 疾病效果与参数相符 |
| entry-03408 | 未发现问题 | 名称、生命及等级参数相符 |
| entry-03409 | 未发现问题 | 物品描述语义相符 |
| entry-03410 | 未发现问题 | 状态参数相符 |
| entry-03411 | 未发现问题 | 死亡与不可召唤状态相符 |
| entry-03412 | 未发现问题 | 活力注入、升级及治疗语义相符 |

以下源码行号使用冻结包内的路径缩写：**L**＝[demon.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua)，**D**＝[demon-seeds.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/demon-seeds.lua)，**E**＝[timed_effects.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/ashes-urhrok/tome-ashes-urhrok/data/timed_effects.lua)。L 中的雕像文字作为 lore 内容直接显示；下列叙事判断据此比较原文与译文。

### C01 | entry-03373 | 存在问题

原文的「covert operations」和「scouts and servants」分别是秘密行动、侦察员与仆役；译文的「藏身的主要根据地」「使者」遗漏了行动及侦察职责。证据：L:309。

### C02 | entry-03373 | 存在问题

「pay tribute」在此承接铭记牺牲和贡献，译成「奉上礼物」变成具体赠礼行为。证据：L:309。

### C03 | entry-03374 | 存在问题

「holding the front lines against the hordes of Eyal」说明抵御埃亚尔大军；「奋战在埃亚尔边界前线」改写了地点，且未交代对抗对象。证据：L:316。

### C04 | entry-03374 | 存在问题

夸塞魔「very much machines」，肌肉被强化而保留聪明头脑；译文改述为「钢铁般的纪律和强大的近战能力」，丢失其制造方式与身体、心智能力的关系。证据：L:316。

### C05 | entry-03375 | 存在问题

「no less aggressive」比较的是攻击性；「不比酸液树魔杀伤力小」改成了杀伤力比较。证据：L:342。

### C06 | entry-03376 | 存在问题

三分之二人口的范围包括拥有多雷格、与其同住、**或仅与其共事**的人；「在生活中都有一只多雷格陪伴」把这些关系合并成生活陪伴。证据：L:349。

### C07 | entry-03377 | 存在问题

叙述者称夏·图尔的设计「devious」；「绝妙的例子」抹去了其狡诈、险恶的评价。证据：L:356。

### C08 | entry-03378 | 存在问题

赛制按出生以来消耗能量的**最高额度**分组，另一赛场是「forest of pillars」；译文只说消耗能量，并将柱林写成「复杂迷宫」。两处赛制条件均改变。证据：L:370。

### C09 | entry-03378 | 存在问题

造物在间接战斗组「performing adequately」，译成「相当出色」提高了其表现等级。证据：L:370。

### C10 | entry-03378 | 存在问题

制造方法使用「sustainable amount of energy-input」，即能持续承担的投入；「通过很少的能量」改成了绝对耗能很低。证据：L:370。

### C11 | entry-03378 | 存在问题

原文说埃亚尔在彻底毁灭前还会经历短暂恐惧；「瞬间……彻底歼灭」删去了这段时序与恐惧体验。证据：L:370。

### C12 | entry-03379 | 存在问题

原文明确说只有声称乌鲁洛克力量「无限」才算夸大；译文称「没有什么词语比‘无穷无尽’更加合适」，把唯一的夸大说法当成准确描述。证据：L:377。

### C13 | entry-03379 | 存在问题

锻造巨人的设计牺牲的是速度和**制造时的能量效率**；「行动速度和能量燃率」把制造成本改写为能量燃烧速率。证据：L:377。

### C14 | entry-03379 | 存在问题

原文是把金属加热至可加工后用锤敲出形状，且每一锤产出数件可用装备；「导入模具」「装备零件」改写了工艺和产物。证据：L:377。

### C15 | entry-03380 | 存在问题

俘虏因事故「mortally wounded」是受了致命伤；「当场惨死」提前宣告死亡，改变后文利用其身体与生命精华的时序。证据：L:384。

### C16 | entry-03380 | 存在问题

被操纵的造物向自以为的「tormentors」报复；「自己眼中的‘敌人’」丢失了施虐者这一认知及引号的讽刺作用。证据：L:384。

### C17 | entry-03382 | 存在问题

原文是传送门**偶尔放出**亡者阴影，包括已彻底停用的门；译文说阴影「经常徘徊」在门附近，改变出现频率和发生方式。证据：L:404。

### C18 | entry-03383 | 存在问题

德瑞宝被传正在「reverse-engineering」传送门，即研究、逆向解析；「反向驱动」指反方向操作，技术行为不同。证据：L:414。

### C19 | entry-03384 | 存在问题

神经系统被重接、以痛为乐是「rare occasion」；译文仅写「又或者是……情况」，丢失其罕见程度。证据：L:421。

### C20 | entry-03388 | 存在问题

「had barely escaped feudalism」指刚刚脱离封建制度；「还没脱离封建社会」把状态反转。证据：L:448。

### C21 | entry-03388 | 存在问题

袭击者是愤怒的「peasants」；「无知难民」把农民改成了难民。证据：L:450。

### C22 | entry-03388 | 存在问题

叙述者决定只有确信生命受威胁才会「lash out」反击；「抽身逃走」改成逃跑，改变她当时的行动界限。证据：L:452。

### C23 | entry-03388 | 存在问题

「Even if I wanted to」是假设即便自己想阻止入侵也做不到；「尽管我很想这么做」肯定了她想阻止入侵的意愿。证据：L:458。

### C24 | entry-03388 | 存在问题

恶魔会把受酸液损伤的眼睛「growing them back with more nerve endings」重新长出；「再将它放回神经更加密集的地方」误成移动眼睛的位置。证据：L:458。

### C25 | entry-03389 | 存在问题

库马纳的才智获得乌鲁洛克「direct, enthusiastic approval」；「精神受到父的指引」把认可改成了精神指导。证据：L:471。

### C26 | entry-03391 | 存在问题

里斯丰格找到的是一座「intact」的完好传送门；「未被人使用过」描述使用历史，原文没有这个事实。证据：L:478。

### C27 | entry-03391 | 存在问题

他亲自测试，是因为失败后果太可怕，不愿让**其他受试者承受**；译文的「实施其他实验的失败后果太过危险」丢失受试者和亲自承担风险的原因。证据：L:478。

### C28 | entry-03392 | 存在问题

洛格罗斯从体内结构**不断生成**无生命精华的种子；「在这个构造中留下了无数……种子」变成预先存放。证据：L:485。

### C29 | entry-03393 | 存在问题

枯萎化达莱奇通常必须立刻「put down」，即处死或消灭，以免造成损害；「压制」只表示暂时制服。证据：L:492。

### C30 | entry-03394 | 存在问题

尚未找到的是逆向解析召唤陨石的法术、借其保护部队的方法；「反制这些咒语」改成了对抗法术。证据：L:499。

### C31 | entry-03394 | 存在问题

陨石会裂成大小**可预测**的碎块；「若干大块」改写碎块尺寸，并漏掉可预测性。证据：L:499。

### C32 | entry-03394 | 存在问题

到达地表后重组是哈卡祖的**设计目标**，后文明确说它至今无法启动这一步；「碎片……重新融合到一起，组成完整形态」误称重组已经发生。证据：L:499。

### C33 | entry-03402 | 存在问题

技能提升 Strength 与 **Magic 属性**，译文把后者写作「魔法」。冻结术语子集的 Magic 属性为「魔力」；快照实现也将增益写入 `Stats.STAT_MAG`，并非提高法术本身。证据：D:700–710 的技能说明与效果调用、E:630–643 的 `inc_stats` 消费逻辑。

**读取与边界。** 实际读取了冻结包的 [INPUT.md](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/INPUT.md)、[entries.json](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/entries.json)、[context.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/context.lua)、[source-access.json](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/source-access.json)，以及其中六个 `sections` 对应的 DLC 源文件：`data/lore/demon.lua`、`data/quests/start-ashes.lua`、`data/talents/corruptions/{black-magic,brutality,demon-seeds,demonic-pact}.lua`。这六个文件的 SHA-256 均与 `source-access.json` 相符。唯一额外读取的源码是哈希相符的 E；调用链来源为 `black-magic.lua` 的 `EFF_OMINOUS_SHADOW`，以及 `demon-seeds.lua` 的 `EFF_ACIDIC_BATH`、`EFF_DEMON_SEED_ARMOURED_LEVIATHAN`、`EFF_DEMON_SEED_PAIN_AFFINITY`。

DLC 快照的源码仓库与 commit 未固定，因此其机制证据只证明该快照内的行为，目标版本适用性未核验。没有读取其他报告、其他模型输出或越界材料；没有创建临时文件或修改仓库。本结果是审核观察，不宣称生产 `DONE_VERIFIED`。
