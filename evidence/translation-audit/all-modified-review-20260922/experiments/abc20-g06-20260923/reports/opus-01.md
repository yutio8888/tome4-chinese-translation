# entry-03373–entry-03412 复核报告（REVIEWER，translation_contextual_v1，自然语言实验旁路）

40 条都已独立复核。结果：21 条**存在问题**，7 条**仅建议**，12 条**未发现问题**，没有**待确认**。以下是审核观察，不是真值，也不声称 DONE_VERIFIED。

| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03373 | 存在问题 | C01、C02、C03；C04 仅建议 |
| entry-03374 | 存在问题 | C05、C06、C07；C08 仅建议 |
| entry-03375 | 存在问题 | C09 |
| entry-03376 | 仅建议 | C10 |
| entry-03377 | 存在问题 | C11、C12 |
| entry-03378 | 存在问题 | C13、C14、C15、C16、C17；C18 仅建议 |
| entry-03379 | 存在问题 | C19、C20、C21、C22 |
| entry-03380 | 仅建议 | C23、C24 |
| entry-03381 | 存在问题 | C25、C26；标记与片段数已核对无误 |
| entry-03382 | 存在问题 | C27、C28 |
| entry-03383 | 存在问题 | C29、C30；C31 仅建议 |
| entry-03384 | 存在问题 | C32、C33；C34 仅建议 |
| entry-03385 | 未发现问题 | 与邻近雕像名“乌尔罗格”一致 |
| entry-03386 | 未发现问题 | 语义、标记、署名齐全 |
| entry-03387 | 未发现问题 | 与邻近雕像名“克里尔·费扬”一致 |
| entry-03388 | 存在问题 | C35–C42；C43、C44 仅建议 |
| entry-03389 | 存在问题 | C45、C46、C47；C48 仅建议 |
| entry-03390 | 未发现问题 | 与邻近雕像名“里斯丰格”一致 |
| entry-03391 | 存在问题 | C49、C50 |
| entry-03392 | 存在问题 | C51、C52 |
| entry-03393 | 存在问题 | C53；C54 仅建议 |
| entry-03394 | 存在问题 | C55、C56；C57 仅建议 |
| entry-03395 | 仅建议 | C58（handler 译“主人”与邻近 context 一致，不计缺陷） |
| entry-03396 | 仅建议 | C59；机制与源码一致 |
| entry-03397 | 未发现问题 | brutality.lua:35-59 一致 |
| entry-03398 | 未发现问题 | brutality.lua:113 logSeen，%s 保留 |
| entry-03399 | 存在问题 | C60 |
| entry-03400 | 仅建议 | C61 |
| entry-03401 | 未发现问题 | demon-seeds.lua:271、292 一致 |
| entry-03402 | 存在问题 | C62 |
| entry-03403 | 未发现问题 | demon-seeds.lua:786-832 一致 |
| entry-03404 | 未发现问题 | demon-seeds.lua:834-851；timed_effects.lua:991-1001 |
| entry-03405 | 未发现问题 | demon-seeds.lua:853-871；各邪术的核心译名不在可读范围，不作判断 |
| entry-03406 | 未发现问题 | demon-seeds.lua:873-891 一致 |
| entry-03407 | 未发现问题 | demon-seeds.lua:1218-1245 一致 |
| entry-03408 | 未发现问题 | demonic-pact.lua:331-339，4 个参数顺序一致 |
| entry-03409 | 未发现问题 | demonic-pact.lua:417 |
| entry-03410 | 未发现问题 | demonic-pact.lua:426 |
| entry-03411 | 未发现问题 | demonic-pact.lua:426 |
| entry-03412 | 未发现问题 | demonic-pact.lua:555，%s／%d 顺序一致 |

说明：全部 40 条都属于 ashes-urhrok DLC。所用源码快照已按 source-access 核对哈希，但源码仓库和 commit 均未固定，DLC 目标版本适用性未确认。全部 15 条 tformat／logSeen／logPlayer 条目的格式符都逐一比对过。entry-03396 和 entry-03402 的格式符列表与原文不同：03396 删去了字面量 `100%%`，03402 只有一个 `%d`，只是位置调整。两处参数消费都正确。

---

### C01 | entry-03373 | 存在问题
- **原文**："a prime location for carrying out covert operations"
- **译文**："成为我们的藏身的主要根据地"
- **问题**：“开展秘密行动”被改成了“藏身根据地”，行动这层信息丢失。
- **证据**：纯语义判断；demon.lua:308-309（water imp 雕像）。

### C02 | entry-03373 | 存在问题
- **原文**："As our scouts and servants beneath the seas"
- **译文**："作为我们在海里的使者"
- **问题**：“侦察兵与仆从”被改成“使者”，职能变了。下文还说它们在收集情报，与侦察身份相呼应。

### C03 | entry-03373 | 存在问题
- **原文**："Remember to pay tribute to the Water Imp"
- **译文**："请记得随时为小水怪们奉上礼物"
- **问题**：pay tribute to 在这里是“致敬、缅怀”，译成“奉上礼物”改变了行为含义。下文说的是不要遗忘它们的牺牲，属于致敬语境。

### C04 | entry-03373 | 仅建议
- **原文**："retain use of their hands"
- **译文**："依旧使用双手作战"
- **说明**：多了“作战”，但不影响整句论点，只是措辞偏好。

### C05 | entry-03374 | 存在问题
- **原文**："study new magical spells for our arsenal"
- **译文**："学习兵工厂新的魔法"
- **问题**：arsenal 在这里指“法术储备”，被误解成实体“兵工厂”，作用对象错了。

### C06 | entry-03374 | 存在问题
- **原文**："focus on making new constructs from scratch"
- **译文**："专心学习新的构架体"
- **问题**：“从零制造”被改成“学习”，动作错了，和本句三方分工的对比（研究法术／强化身体／制造构造体）也对不上。

### C07 | entry-03374 | 存在问题
- **原文**："the warrior onyx known as Quasits are very much machines, made with bolstered muscles without losing the clever minds they come from.  As eager as they are brilliant, Quasits are well-disciplined…"
- **译文**："尽管仍是血肉之躯，玛瑙战士——或者说夸塞魔——有着钢铁般的纪律和强大的近战能力"
- **问题**：丢失了四项信息：“本质上近乎机器”“强化的肌肉”“保留原有的聪明头脑”“热忱与聪慧并重”。“钢铁般的纪律”是新增内容。

### C08 | entry-03374 | 仅建议
- **现象**：children of onyx 在本条译作“玛瑙色的孩子们”“玛瑙战士”，本批 03379、03383、03388、03389 用的是“缟玛瑙之子”。
- **说明**：context.lua 中两种写法都有（缟玛瑙 10 处，玛瑙色 3 处），读者仍能认出指称，属于统一性偏好，不扩大为全局改名。

### C09 | entry-03375 | 存在问题
- **原文**："Although no less aggressive than their younger counterparts, wretch titans generally have a much higher survival rate"
- **译文**："他们不比酸液树魔杀伤力小"
- **问题**：aggressive（好斗、冲锋性）被改成“杀伤力”。原句的逻辑是“同样好斗却更能活下来”，改成杀伤力后这层对比不成立。

### C10 | entry-03376 | 仅建议
- **原文**："rather intelligent for a beast"
- **译文**："比野兽更有智力"
- **说明**：译文略有“不算野兽”的歧义，“尽数我们为战争作出的牺牲”用词也生硬。整体语义没有丢失。

### C11 | entry-03377 | 存在问题
- **原文**："a good example of the devious designs the Sher'Tul had in mind"
- **译文**："夏·图尔人制造或者改变埃亚尔种族的一个绝妙的例子"
- **问题**：“阴险的用心（devious designs）”丢失，还新增了褒义的“绝妙”，评价方向反了。

### C12 | entry-03377 | 存在问题
- **原文**："horned beast-men"
- **译文**："长角的兽人"
- **问题**：术语快照中 Orc 固定为“兽人”（T.PN.RACE）。这里用“兽人”指米诺陶，会被读成“长角的兽人（orc）”，与已登记的种族名冲突。

### C13 | entry-03378 | 存在问题
- **原文**："the most straightforward of our competitions for the spectator, but those competing have a huge variety of possible divisions"
- **译文**："对我们的观众来说最为熟悉的比赛，然而有些人不知道的是……"
- **问题**：“最直观易懂”被改成“最熟悉”；“有些人不知道的是”为新增；原句“观众看着简单、参赛者分组繁多”的对比丢失。

### C14 | entry-03378 | 存在问题
- **原文**："based on the maximum amount of energy consumed by their entrants since (and including) birth"
- **译文**："来自于选手从出生开始所消耗的能量"
- **问题**：删掉了“最大值／上限”。分组依据的是能耗上限（类似体重级别），删除后分组标准就变了。

### C15 | entry-03378 | 存在问题
- **原文**："a difficult-to-navigate forest of pillars"
- **译文**："复杂迷宫"
- **问题**：赛场类型从“石柱林”变成了“迷宫”。

### C16 | entry-03378 | 存在问题
- **原文**："while performing adequately in the less-direct ones"
- **译文**："在其他复杂的环境下也有相当出色的表现"
- **问题**：“表现尚可”被夸大成“相当出色”，程度不符。

### C17 | entry-03378 | 存在问题
- **原文**："with a sustainable amount of energy-input"
- **译文**："通过很少的能量"
- **问题**：“可持续的能量投入”被改成“很少的能量”，程度信息错了。

### C18 | entry-03378 | 仅建议
- **原文**："a few fleeting moments of terror before their utter annihilation"
- **译文**："瞬间就会被……彻底歼灭"
- **说明**：丢了“短暂的恐惧”这层渲染，但“迅速歼灭”的主干保留了，属于修辞层面。

### C19 | entry-03379 | 存在问题
- **原文**："as such, he cannot spend time or effort making equipment"
- **译文**："他或许没有足够的时间和精力"
- **问题**：确定的“不能”被弱化成推测的“或许”，情态变了。

### C20 | entry-03379 | 存在问题
- **原文**："built for raw strength at the expense of speed and energy-efficient creation"
- **译文**："以牺牲一定行动速度和能量燃率的代价"
- **问题**：原文说的是“造出它们的能量效率”（即制造成本更高），译文变成了意义不明的“能量燃率”，好像在说运行能耗。另外“一定”也是新增的。

### C21 | entry-03379 | 存在问题
- **原文**："heating raw metal with their magic until it is workable, then pounding it into their shape"
- **译文**："用魔法熔炼，然后将其导入模具中"
- **问题**：“用锤锻打成型”被改成“浇铸入模”，和本条“巨锤锻造”的核心设定矛盾。

### C22 | entry-03379 | 存在问题
- **原文**："every single swing produces several pieces of usable equipment"
- **译文**："一击就能瞬间制造出数个装备零件"
- **问题**：“几件可用的成品装备”被改成“装备零件”，产出性质错了。

### C23 | entry-03380 | 仅建议
- **原文**："Thanks to numerous contacts we have on Eyal's surface, ranging from easily-duped natives to our own scouting teams"
- **译文**："源于我们对埃亚尔大陆的多次接触"
- **说明**：contacts 原指“人脉、联络人”，译成“多次接触”，但后半句的列举让读者仍能理解。

### C24 | entry-03380 | 仅建议
- **现象**：
  - "ends up mortally wounded" 译作“当场惨死”；
  - "try to preserve" 译作“曾经试图”；
  - "'tormentors'" 译作“敌人”。
- **说明**：细节有偏移，但“俘虏死后被拼接再利用、被导向攻击同胞”的主线和反讽基本保留。

### C25 | entry-03381 | 存在问题
- **原文片段**："…arness their fear and suspici…"（harness）
- **译文**："卸下他们的恐惧和怀"
- **问题**：harness 是“利用”，被译成“卸下”，词义相反。
- **格式核验**：原文与译文各有 10 个 `#927e64#`、10 个 `#LAST#`，`#{italic}#`／`#{bold}#`／`#{normal}#` 序列一致。全角波浪线约为原文数量的一半，显示宽度相当，不构成格式缺陷。

### C26 | entry-03381 | 存在问题
- **原文片段**："…king them a val…" / "…tion to our intel-gathering camps. Redee…"（making them a valuable addition to…）
- **译文**："给他们一个…" / "…息提供给了我们的情报机构。为了偿…"
- **问题**：“使其成为情报营地的宝贵补充”被重构成“给他们一个……信息提供给情报机构”，残片对应的语义错了。

### C27 | entry-03382 | 存在问题
- **原文**："will occasionally emit a shade of one of our fallen citizens"
- **译文**："附近经常徘徊着我们牺牲同胞的灵魂"
- **问题**：频率从“偶尔”变成“经常”，动作从“从门中涌出”变成“在附近徘徊”。

### C28 | entry-03382 | 存在问题
- **原文**："warped to insanity by its transit"
- **译文**："被折磨地几近疯狂"
- **问题**：原文是已经发疯，译文变成“几近疯狂”，程度降低了。“smelling of Mal'Rok's ashes”译作“被灰烬所环绕”也有轻微偏移。

### C29 | entry-03383 | 存在问题
- **原文**："he's been reverse-engineering the Sher'Tul portals"
- **译文**："他正在反向驱动夏·图尔的传送门"
- **问题**：“逆向工程／逆向解析”被译成“反向驱动”，意思变成了让传送门反向运行。同批 03384 用的是正确的“逆向解析”。

### C30 | entry-03383 | 存在问题
- **原文**："work his skills into a mass-producible artifact"
- **译文**："将他的技术融入工艺品并量产化"
- **问题**：这里 artifact 指能赋予传送能力的魔法造物，“工艺品”是装饰性手工品，物品性质错了。

### C31 | entry-03383 | 仅建议
- **现象**：“之一—缟玛瑙之子德瑞宝——”，前半用单个破折号，后半用双破折号。
- **说明**：属于标点规范问题，不影响信息。

### C32 | entry-03384 | 存在问题
- **原文**："all of them appear with nearly every shred of their essence drained"
- **译文**："他们的每一丝生命精华已被汲取殆尽"
- **问题**：删掉了 nearly，“几乎耗尽”变成“完全耗尽”，与后句“陷于死亡边缘（仍活着）”相矛盾。

### C33 | entry-03384 | 存在问题
- **原文**："the frequent cases of internal bleeding and the rare occasion of them appearing with a rewired nervous system"
- **译文**："又或者是神经网络重接导致……的情况"
- **问题**：保留了“常见”，却删掉了“罕见”，原文“常见 vs 罕见”的频率对比丢失。

### C34 | entry-03384 | 仅建议
- **现象**：正文写“莎西·凯希”，本条所属雕像标题（demon.lua:420；context.lua:315）写“恶魔雕像：莎西凯希”。
- **说明**：只差间隔号，指称不变，属于统一性问题，不扩大为全局改名。

### C35 | entry-03388 | 存在问题
- **原文**："such savages that had barely escaped feudalism"
- **译文**："还没脱离封建社会的野蛮人"
- **问题**：“刚刚勉强脱离”被改成“尚未脱离”，事实反转。

### C36 | entry-03388 | 存在问题
- **原文**："an enraged horde of peasants, provoked by our unfortunate choice of disguises"
- **译文**："大量的无知难民"
- **问题**：“农民”变成“难民”，行动主体错了；“愤怒的”也丢了。

### C37 | entry-03388 | 存在问题
- **原文**："I kept telling myself only to lash out once I was sure my life was in danger"
- **译文**："只要在真正有性命之虞的时候抽身逃走就行"
- **问题**：“出手反击”被改成“抽身逃走”，行为反了，与前句“I could have fought back”也脱节。

### C38 | entry-03388 | 存在问题
- **原文**："Their reasons are somewhat inaccurate, but make no mistake: you deserve the fate they have lined up for you."
- **译文**："他们的理由是——或许不准确，但是我没有说错——“他们所安排的命运是你们应得的”。"
- **问题**：原文是说话人（S）自己的判断：“他们的理由不太准确，但你们确实罪有应得”。译文把“你们罪有应得”加引号，当成了“他们的理由”的内容，归属和逻辑结构都错了。

### C39 | entry-03388 | 存在问题
- **原文**："Even if I wanted to, neither I nor anything else in the universe could stop their invasion"
- **译文**："我或者宇宙中任何事物都没法阻止他们的侵略，尽管我很想这么做。"
- **问题**：原文是假设“即便我想”（她实际并不想），译文变成“尽管我很想”，说话人立场反了。

### C40 | entry-03388 | 存在问题
- **原文**："dripping acid into your eyes, then growing them back with more nerve endings than before"
- **译文**："再将它放回神经更加密集的地方去"
- **问题**：“重新长出神经末梢更多的眼睛”被误译成“放回神经密集处”，动作和结果都错了。

### C41 | entry-03388 | 存在问题
- **原文**："Countless others have agreed to this deal in the millenia before you were even born"
- **译文**："在你们诞生千年之前"
- **问题**：“你们出生前的数千年间（持续）”被改成“你们出生前一千年（时点）”，时序和跨度错了。

### C42 | entry-03388 | 存在问题
- **原文**："you will feel nearly-equal pleasure"
- **译文**："你们会感到等量的快乐"
- **问题**：删掉了限定词 nearly，“近乎等量”变成“等量”，承诺的程度被说满了。

### C43 | entry-03388 | 仅建议
- **现象**："even the armies of Mal'Rok" 译作“哪怕乌鲁洛克的军队”，把世界名换成了神名。
- **说明**：两者在语境中指同一支军队，读者不会误解。“agonizing”译作“可悲”也略弱。

### C44 | entry-03388 | 仅建议
- **现象**：“the Fearscape”译作“恐惧空间”；术语快照有 fearscape→恶魔空间（newLore category，existing），context.lua 第 212 行也用“恶魔空间”。
- **说明**：source_tag 与类别不同，existing 不构成强制要求，只记统一性建议。

### C45 | entry-03389 | 存在问题
- **原文**："under the command and inspiration of Urh'Rok"
- **译文**："在乌尔洛克的命令和鼓动下"
- **问题**：同条后文和本批其他条目都写“乌鲁洛克”。本条所属雕像标题（demon.lua:470；context.lua:380）是“库马纳，乌鲁洛克将军”。同一专名在同一条内出现两种写法。

### C46 | entry-03389 | 存在问题
- **原文**："the Divine Tournament of Tactics"
- **译文**："神圣战术竞标赛"
- **问题**：“竞标”是招投标的意思，属于错字，改变了赛事名称的含义。本条前文和 03378 都写作“锦标赛”。

### C47 | entry-03389 | 存在问题
- **原文**："a mind given his direct, enthusiastic approval"
- **译文**："精神受到父的指引"
- **问题**：“心智获得父亲直接而热情的认可”被改成“受父指引”，关系性质从“认可”变成了“引导”。

### C48 | entry-03389 | 仅建议
- **现象**：
  - "salvation from the dust mages" 译作“被从尘埃法师的控制之下解放”，“控制”为新增；
  - "physical endurance" 译作“物理耐受”，用词生硬；
  - "the little energy he's not using" 丢了 little。
- **说明**：均不改变主干信息。

### C49 | entry-03391 | 存在问题
- **原文**："he recovered an intact one"
- **译文**："他早已找到了一个未被人使用过的"
- **问题**：“完好无损”被改成“未被使用过”，属性错了。“早已”也是新增。

### C50 | entry-03391 | 存在问题
- **原文**："Saying that the consequences of failure were too awful to risk inflicting on other test subjects, he entered the portal himself"
- **译文**："由于他说实施其他实验的失败后果太过危险"
- **问题**：原意是“不忍让其他受试者承担失败后果”，是他亲身冒险的无私动机。译文变成“其他实验的失败后果危险”，对象和动机都错了。

### C51 | entry-03392 | 存在问题
- **原文**："Rogroth generates countless essence-less seeds"
- **译文**："洛格罗斯在这个构造中……"
- **问题**：本条正是雕像“Rogroth, Eater of Souls”的铭文（demon.lua:484-485），标题译作“罗格洛斯·灵魂吞噬者”（context.lua:384）。正文写成“洛格罗斯”，同一弹窗里标题与正文名称不一致。

### C52 | entry-03392 | 存在问题
- **原文**："developed a prototype of this form of magic"
- **译文**："研究出了这种魔法的原形"
- **问题**：“原形”是本来面目的意思，“原型”才是 prototype，错字改变了词义。

### C53 | entry-03393 | 存在问题
- **原文**："usually a blighted daelach has to be immediately put down"
- **译文**："一个枯萎化的达莱奇必须立刻被压制"
- **问题**：删掉了 usually，“通常”变成“一律”；put down（处决、销毁）被译成“压制”，处置方式错了。

### C54 | entry-03393 | 仅建议
- **现象**："almost entirely made of magic" 译作“纯粹魔法生物”；同一段内“它／他”指代混用（“他的火焰风暴”“他的实际效果”）。
- **说明**：主旨（高魔法构成导致不稳定）不变。

### C55 | entry-03394 | 存在问题
- **原文**："we have not yet found a way to reverse-engineer these spells to protect our standard troops"
- **译文**："还没有找到反制这些咒语的方法"
- **问题**：目的是“逆向复制”这些法术，让己方部队穿过护盾，译成“反制”后目的反了。

### C56 | entry-03394 | 存在问题
- **原文**："protect our standard troops from disintegration"
- **译文**："免于溃散"
- **问题**：disintegration 是物理解体（与本条“护盾将其撕碎”对应），“溃散”是军队崩溃的意思，语义错了。

### C57 | entry-03394 | 仅建议
- **现象**："we made him to be too sturdy" 译作“制造的太过顽固”。
- **说明**：“顽固”偏指性格，这里“坚固”更贴切；读者仍可理解为“太结实”，按措辞偏好处理。

### C58 | entry-03395 | 仅建议
- **原文**："As you recover, and your platform of searing earth splits from the main continent, your old memories flood your mind"
- **译文**："当你醒来后，你发现你身处一个和主大陆分离的平台，而你旧时的记忆渐渐涌来"
- **说明**：丢了“灼热土地”，平台分离从正在发生的事件变成了既成状态，“flood”译作“渐渐”也不贴切。核心事实（平台已与大陆分离、记忆恢复）都在。
- **handler 的处理**：译作“主人”加引号，与邻近 context（context.lua 第 139、150 行）一致，不计缺陷。
- **证据**：start-ashes.lua:22-28。

### C59 | entry-03396 | 仅建议
- **现象**：“你处于隐形（强度 %d）造成的所有伤害转化为暗影伤害”，括号后缺逗号，可能读成“隐形造成的伤害”。
- **机制核验**：black-magic.lua:146-149 的 info 与 action（:130-137，按层数设定持续回合）一致；timed_effects.lua:1013-1017 为 100% 伤害转为暗影，auto_highest_inc_damage／auto_highest_resists_pen 施加于暗影。译文“相当于你最高伤害加成和抗性穿透”正确。删掉字面量 `100%%`、改写为“所有伤害”不影响参数消费。

### C60 | entry-03399 | 存在问题
- **原文**："You spawn a pool of acid in radius 4 around you"
- **译文**："在半径 4 的范围内制造持续 %d 回合的酸池"
- **问题**：丢了“以你为中心（around you）”这一位置信息。该技能定义了 `range = 4` 和 `requires_target = true`（demon-seeds.lua:205-206），但 action 实际以 `self.x, self.y` 为中心生成地图效果（:213-216）。缺少位置信息时，“半径 4 的范围内”容易被读成射程 4 的指定点施放。
- **其余部分**：40% 抗性和亲和数值与 timed_effects.lua:559-571 一致。

### C61 | entry-03400 | 仅建议
- **现象**：“选择%s次充能的用途”，这里的 charges 是可储存的充能数（demon-seeds.lua:247-257），用量词“次”不够贴切。
- **说明**：参数 `p.charges` 由 tformat %s 正确消费，信息无损。

### C62 | entry-03402 | 存在问题
- **原文**："your Strength and Magic stats are increased by 10%% of your shield block value"
- **译文**："力量和魔法增加 10%% 格挡值"
- **问题**：源码提升的是属性 STAT_MAG／STAT_STR（timed_effects.lua:630-641 `inc_stats`；demon-seeds.lua:703 `power=block*0.1`）。术语快照中 Magic／mag 这一属性名都登记为“魔力”（T.GAME.STAT，existing，反映语料现状）。译成“魔法”后，指称的属性名与面板属性不一致。
- **状态说明**：状态是 existing，但这里原文明确写的是 stats，属性指称错误。
- **其他**：两行合并为一行、`%d` 移到句尾，都不影响参数消费。

---

## 读取的路径、版本与越界情况

**冻结输入**：

实验目录为 `evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/`，读取了其中：
- `INPUT.md`
- `entries.json`（40 条；只读 source／target／line／source_tag 等字段）
- `context.lua`（用于专名与邻近译法检索）
- `source-access.json`

**条目源码**：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/` 下 6 个文件：
- `lore/demon.lua`
- `quests/start-ashes.lua`
- `talents/corruptions/black-magic.lua`
- `talents/corruptions/brutality.lua`
- `talents/corruptions/demon-seeds.lua`
- `talents/corruptions/demonic-pact.lua`

sha256 全部与 source-access 列明值一致。DLC 状态为 unpinned：源码仓库和 commit 均未固定，目标版本适用性待确认。

**额外 DLC 单文件**：`…/experiments/abc20-20260923/sources/ashes-urhrok/tome-ashes-urhrok/data/timed_effects.lua`
- sha256 `eb183d02…863f8d`，与 dlc_additional_sources 一致。
- 引入依据：
  - black-magic.lua:137 `self.EFF_OMINOUS_SHADOW`
  - demon-seeds.lua:225 `EFF_ACIDIC_BATH`
  - demon-seeds.lua:703 `EFF_DEMON_SEED_ARMOURED_LEVIATHAN`
  - demon-seeds.lua:843 `EFF_DEMON_SEED_PAIN_AFFINITY`
- 只按这几个效果名定位阅读。

**本体源码**：未使用。没有执行 `git show`，也没有读取 `/workspace/t-engine4` 工作树。

**无法核验**：
- 03405、03406 的各邪术和诅咒名在核心 talents 中，属于可读范围之外。只确认了与源码的等级参数和触发限制一致，没有判断译名。
- 03388 的“克里尔·费扬地宫”是区域名，没有核验。

**越界与边界说明**：
- 为列清单对实验目录执行过 `ls` 和 `wc -c`。输出里只出现了 SPEC／STATE／BASELINE 等文件的名称和字节数，没有查看或 cat 这些文件的内容。
- 对额外来源根目录执行过一次 `ls`，只看到顶层目录名。
- 没有读取 locales、其他报告、raw／dispatches、当前翻译文件，也没有读取其他模型的输出。

**临时文件**：没有创建任何临时目录或文件。仓库和冻结输入都没有修改。
