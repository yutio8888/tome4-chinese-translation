| 完整entry-ID | 四类判定 | claim编号或简短依据 |
|---|---|---|
| entry-03373 | 存在问题 | C01–C03 |
| entry-03374 | 存在问题 | C04–C08 |
| entry-03375 | 存在问题 | C09 |
| entry-03376 | 存在问题 | C10–C11 |
| entry-03377 | 存在问题 | C12 |
| entry-03378 | 存在问题 | C13–C20 |
| entry-03379 | 存在问题 | C21–C25 |
| entry-03380 | 存在问题 | C26–C28 |
| entry-03381 | 存在问题 | C29 |
| entry-03382 | 存在问题 | C30–C32 |
| entry-03383 | 存在问题 | C33 |
| entry-03384 | 存在问题 | C34 |
| entry-03385 | 未发现问题 | 雕像名称与冻结邻近语境一致 |
| entry-03386 | 未发现问题 | 留言对象、存活信息及鼓励含义保留 |
| entry-03387 | 未发现问题 | 雕像名称与冻结邻近语境一致 |
| entry-03388 | 存在问题 | C35–C42 |
| entry-03389 | 存在问题 | C43 |
| entry-03390 | 未发现问题 | 雕像名称与冻结邻近语境一致 |
| entry-03391 | 存在问题 | C44–C45 |
| entry-03392 | 存在问题 | C46–C47 |
| entry-03393 | 存在问题 | C48 |
| entry-03394 | 存在问题 | C49–C52 |
| entry-03395 | 存在问题 | C53–C54 |
| entry-03396 | 待确认 | C55 仅建议；C56 待确认 |
| entry-03397 | 未发现问题 | 两次攻击、吸血比例、每次命中恢复量及参数对应保留 |
| entry-03398 | 未发现问题 | 抵抗抓取日志与触发分支一致 |
| entry-03399 | 存在问题 | C57 |
| entry-03400 | 未发现问题 | `%s` 消费当前充能数，用途选择含义保留 |
| entry-03401 | 未发现问题 | 护盾量与50%反射含义保留 |
| entry-03402 | 未发现问题 | 持续时间、两项属性及格挡值比例保留；重排不改变参数消费 |
| entry-03403 | 待确认 | C58 |
| entry-03404 | 仅建议 | C59 |
| entry-03405 | 未发现问题 | 格挡触发、随机邪术、技能等级及每回合上限保留 |
| entry-03406 | 未发现问题 | 近战攻击触发、几率、随机诅咒及每回合上限保留 |
| entry-03407 | 待确认 | C60 |
| entry-03408 | 未发现问题 | 名称、当前生命、最大生命、等级四项参数顺序正确 |
| entry-03409 | 未发现问题 | 物品描述含义保留 |
| entry-03410 | 未发现问题 | 状态字符串消费关系正确 |
| entry-03411 | 未发现问题 | 死亡与无法召唤含义保留 |
| entry-03412 | 未发现问题 | 活力注入、等级与治疗信息及颜色标记保留 |

以下 `L` 指本组冻结源码 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua`；其他源码简称在末尾展开。所有“存在问题”均为本次复核的 confirmed 观察；叙事观察依据冻结文本直接判定，不据此断言额外游戏机制。DLC 快照哈希已核对，但其源码仓库、commit 与目标版本适用性未固定。

### C01 | entry-03373 | 存在问题

原文“retain use of their hands”只说明保留双手的使用能力；译文“依旧使用双手作战”增加了作战用途。牺牲其他能力而保留手部能力的身体改造描述，被限定为战斗行为。证据：`L:309`。

### C02 | entry-03373 | 存在问题

原文“carrying out covert operations”“our scouts and servants”描述秘密行动及侦察、服务职责；译文“藏身的主要根据地”“海里的使者”分别变成藏身地点和使者身份。末句虽保留收集情报，仍未完整保留这些具体职责。证据：`L:309`。

### C03 | entry-03373 | 存在问题

原文“too dangerous to perform on our own soil”指不宜在己方本土进行的危险实验；译文“对于我们的土壤来说过于危险”把实验地点限制改成土壤受害对象。证据：`L:309`，同句列举海洋基地的用途。

### C04 | entry-03374 | 存在问题

原文“holding the front lines against the hordes of Eyal”说明抵御埃亚尔军众、坚守前线；译文“奋战在埃亚尔边界前线”新增地理边界，并遗漏抵御对象。证据：`L:316`。

### C05 | entry-03374 | 存在问题

原文“study new magical spells for our arsenal”是研究新法术以扩充己方武备；译文“学习兵工厂新的魔法”把用途关系改成法术属于兵工厂，并将研究改成学习。证据：`L:316`。

### C06 | entry-03374 | 存在问题

原文“making new constructs from scratch”描述从零制造构装体，后接组成高大造物的过程；译文“专心学习新的构架体”遗漏制造行为和从零创造的含义。这一判断不依赖强制采用某个术语译名。证据：`L:316`。

### C07 | entry-03374 | 存在问题

原文护甲在“出生”时“bolted onto their skin”；译文仅说“一‘出生’就身着……护甲”，遗漏护甲被固定到皮肤上的身体构造信息。证据：`L:316`。

### C08 | entry-03374 | 存在问题

原文明确说明夸塞魔虽主要由血肉组成，却近似机器，拥有强化肌肉，并保留原有聪明头脑；译文直接转为“钢铁般的纪律和强大的近战能力”，遗漏这组制造结果与智力保留信息。证据：`L:316`。

### C09 | entry-03375 | 存在问题

原文“no less aggressive”比较的是攻击性；译文“不比酸液树魔杀伤力小”比较伤害能力。随后有关力量和体型的说明不能使这两种属性等价。证据：`L:342`。

### C10 | entry-03376 | 存在问题

原文“rather intelligent for a beast”是在野兽这一类别内评价其聪明；译文“比野兽更有智力”改成与野兽整体比较，改变了比较范围。证据：`L:349`。

### C11 | entry-03376 | 存在问题

原文只说失去温柔伙伴可能“troubles us the most”；译文增加“可能是最大、也是最困扰我们的一项”，额外认定它是最大的战争牺牲。最令人困扰不等于牺牲规模最大。证据：`L:349`。

### C12 | entry-03377 | 存在问题

原文将米诺陶作为夏·图尔“devious designs”的例子，包含对其创造意图阴险、诡诈的评价；译文仅称制造或改变种族的“绝妙的例子”，丢失这一态度信息。证据：`L:356`。

### C13 | entry-03378 | 存在问题

原文“most straightforward … for the spectator”说明比赛最直观、易于观众理解；译文“最为熟悉”改成观众熟悉程度，且增加“有些人不知道”的叙述。证据：`L:370`。

### C14 | entry-03378 | 存在问题

原文组别依据包含“maximum”及“since (and including) birth”；译文“从出生开始所消耗的能量”未保留能量上限与出生本身也计入的限定。对于工厂制造的参赛造物，出生投入与出生后消耗并不等价。证据：`L:370`，后文紧接参赛者制造方式。

### C15 | entry-03378 | 存在问题

原文场地是难以穿行的“forest of pillars”；译文改为“复杂迷宫”，遗漏密集柱林这一场地结构。证据：`L:370`。

### C16 | entry-03378 | 存在问题

原文说高能组参赛者“typically”不按常规出生，“usually”由团队制造；译文改为“最高能量”的组别，并无条件断言参赛者都是团队产物，还增加“天才”。组别范围与通常成立的限定均被改变。证据：`L:370`。

### C17 | entry-03378 | 存在问题

原文在非直接战斗组别“performing adequately”；译文“有相当出色的表现”明显提高评价等级，削弱了其主要优势在开放场地正面战斗的对比。证据：`L:370`。

### C18 | entry-03378 | 存在问题

原文制造所需能量为“a sustainable amount”；译文“很少的能量”把可持续承担的投入改成绝对低投入。证据：`L:370`。

### C19 | entry-03378 | 存在问题

原文成为军队骨干有“once mass-production is in order”的前提；译文直接宣布将成为中流砥柱，遗漏量产准备就绪这一条件。末句“成批到达”描述部署，不能替代生产条件。证据：`L:370`。

### C20 | entry-03378 | 存在问题

原文明确描写彻底毁灭前短暂的恐惧时刻；译文只说弱小生物瞬间被歼灭，遗漏这一先恐惧、后毁灭的叙事过程。证据：`L:370`。

### C21 | entry-03379 | 存在问题

原文“cannot be overstated, except by claiming it to be infinite”明确把“无限”排除在合理形容之外；译文却说没有比“无穷无尽”更合适的形容，意义反转。证据：`L:377`。

### C22 | entry-03379 | 存在问题

原文“he cannot spend time or effort”明确表示无法亲自制造军队装备；译文“他或许没有足够的时间和精力”将确定限制变成猜测。证据：`L:377`。

### C23 | entry-03379 | 存在问题

原文牺牲的是“energy-efficient creation”，即制造这些改造体的能量效率；译文“能量燃率”改成未说明的能量燃烧指标，丢失制造阶段的限定。证据：`L:377`。

### C24 | entry-03379 | 存在问题

原文是加热金属至可加工，再锤打成形；译文写成熔炼后导入模具，并增加“魔钢”材质。加工方式和材料信息均发生变化。证据：`L:377`，巨锤及可拆卸锤头说明也支持锻打语境。

### C25 | entry-03379 | 存在问题

原文每次挥锤产生数件“usable equipment”；译文“数个装备零件”把可用成品改为部件。证据：`L:377`。

### C26 | entry-03380 | 存在问题

原文“contacts … ranging from … natives to … scouting teams”指己方在地表的联系人或联系网络；译文“对埃亚尔大陆的多次接触”改为接触次数，丢失取得俘虏的人员渠道。证据：`L:384`。

### C27 | entry-03380 | 存在问题

原文俘虏“ends up mortally wounded”，随后说明不让其以死亡逃脱；译文提前写成“当场惨死”，改变死亡时点，并削弱后续阻止死亡解脱的因果关系。证据：`L:384`。

### C28 | entry-03380 | 存在问题

原文被攻击者在拼合生物眼中是“tormentors”；译文仅为“敌人”，遗漏复仇认知被转移后，将原同胞视作折磨者的具体信息。证据：`L:384`，前句明确提到重定向复仇本能。

### C29 | entry-03381 | 存在问题

可见原文残片“arness their fear and suspici…”对应利用、驾驭恐惧与猜疑；译文“卸下他们的恐惧和怀…”变成解除这些情绪。遮蔽文本不要求补全，但仍应保留可辨残片的方向。证据：`L:393`。未将波浪线宽度变化判为格式缺陷。

### C30 | entry-03382 | 存在问题

原文传送门“occasionally emit a shade”；译文改为传送门附近“经常徘徊着”灵魂，同时改变发生频率及出现方式。证据：`L:404`。

### C31 | entry-03382 | 存在问题

原文“warped to insanity”表示已被扭曲至疯狂；译文“几近疯狂”改成尚未达到疯狂。证据：`L:404`。

### C32 | entry-03382 | 存在问题

原文“smelling of Mal'Rok's ashes”是带有灰烬气味；译文“被玛·洛克的灰烬所环绕”改为实体灰烬围绕的视觉现象。证据：`L:404`。

### C33 | entry-03383 | 存在问题

原文“reverse-engineering the Sher'Tul portals”指逆向研究传送门技术；译文“反向驱动……传送门”改成反方向运行设备。证据：`L:414`，上下文是学者研究、量产传送能力的工作。

### C34 | entry-03384 | 存在问题

原文将神经系统重接、把疼痛当快乐的现象限定为“rare occasion”；译文保留体内出血“常见”，却删除后一现象罕见的限定，丢失两类受试者情况的频率对比。证据：`L:421`。

### C35 | entry-03388 | 存在问题

原文说被刮去的文字谈论“his accomplishments … and his mysterious disappearance”，未称其为本人自述；译文“一个博物学者喋喋不休地讲述他的成就和……失踪”将博物学者变成叙述者。证据：`L:446`及雕像说明语境。

### C36 | entry-03388 | 存在问题

原文“had barely escaped feudalism”表示刚刚或勉强脱离封建制；译文“还没脱离封建社会”否定了脱离这一事实。证据：`L:448`。

### C37 | entry-03388 | 存在问题

原文围攻者是“peasants”；译文“大量的无知难民”把农民身份改为难民。灾难发生并不能直接证明这些人具有难民身份。证据：`L:450`。

### C38 | entry-03388 | 存在问题

原文叙述者告诫自己仅在确认生命危险后“lash out”；译文改为有性命之虞时“抽身逃走”。克制反击与准备逃跑是不同的行动选择。证据：`L:452`。

### C39 | entry-03388 | 存在问题

原文“only now did I use it”强调此前未使用、此刻才使用禁咒；译文“也只有在那时我使用了这个咒语”变成仅那一次使用。后文继续猎取居民生命精华，也使这一唯一时点限制与叙事不符。证据：`L:454`、`L:456`。

### C40 | entry-03388 | 存在问题

原文“Even if I wanted to”是假设自己想阻止入侵；译文“尽管我很想这么做”断言她确实想阻止。人物动机被改变，且与后文帮助世界灭亡的宣言冲突。证据：`L:458`、`L:460`。

### C41 | entry-03388 | 存在问题

原文眼睛被酸液毁坏后重新长出，并具有更多神经末梢；译文“再将它放回神经更加密集的地方”变成移动、放回眼球，改变折磨方式与疼痛增强原因。证据：`L:458`。

### C42 | entry-03388 | 存在问题

原文承诺“nearly-equal pleasure”；译文“等量的快乐”删除近似限定，把接近等量的许诺变成精确等量。证据：`L:458`。

### C43 | entry-03389 | 存在问题

原文“a mind given his direct, enthusiastic approval”说明库马纳的才智得到乌鲁洛克亲自、热情认可；译文“精神受到父的指引”改为精神受其引导，遗漏认可关系。证据：`L:471`。

### C44 | entry-03391 | 存在问题

原文里斯丰格找到“an intact”传送门；译文“一个未被人使用过的”把完好状态改为使用历史。证据：`L:478`。

### C45 | entry-03391 | 存在问题

原文不愿把失败后果施加给“other test subjects”，因此亲自试验；译文“实施其他实验的失败后果太过危险”改成其他实验危险，遗漏保护其他受试者的伦理动机。证据：`L:478`，末句专门赞扬其无私奉献。

### C46 | entry-03392 | 存在问题

原文洛格罗斯“generates countless … seeds from within its frame”，是在体内生产种子；译文“在这个构造中留下了无数……种子”变成放置、留存种子，遗漏生产能力。证据：`L:485`，后文继续讨论其生产能力尚未完善。

### C47 | entry-03392 | 存在问题

原文就地形成入侵军队需要“some decisive early skirmishes”；译文“只需要早期的小规模战斗”遗漏战斗具有决定性这一限定，降低了设想成立的条件。证据：`L:485`。

### C48 | entry-03393 | 存在问题

原文失控的枯萎达莱奇通常必须“immediately put down”，在此生物处置语境中指杀死；译文“立刻被压制”只表达控制、镇压，未保留处死措施。证据：`L:492`，前文说明其可能摧毁制造者，后文以可控样本为例外。

### C49 | entry-03394 | 存在问题

原文陨石被分成“predictably-sized chunks”；译文“若干大块”遗漏碎块大小可预测这一特征，并增加“大”的判断。证据：`L:499`。

### C50 | entry-03394 | 存在问题

原文“reverse-engineer these spells”是研究并复现法术，以保护己方军队；译文“反制这些咒语”变成对抗、克制法术。证据：`L:499`，目的为利用通过护盾的方法，而非抵消这些法术。

### C51 | entry-03394 | 存在问题

原文“too sturdy”指石质躯体过于坚固；译文“太过顽固”通常指性情执拗，改变无法重组的物理原因。证据：`L:499`，另一候选原因是护盾附加反魔法包层。

### C52 | entry-03394 | 存在问题

原文将落地后碎片重组置于设计说明中，紧接着说明此阶段未能启动；译文独立断言“碎片在到达埃亚尔之后重新融合到一起，组成完整形态”，随后又说无法重组，形成实际已完成与尚未完成的矛盾。证据：`L:499`。

### C53 | entry-03395 | 存在问题

原文大陆漂浮于“the void between worlds”；译文仅保留“虚空”，遗漏世界之间这一位置关系。证据：`quests/start-ashes.lua:23`。这是叙事位置遗漏，不是对地图实现的额外推断。

### C54 | entry-03395 | 存在问题

原文“but not without destroying the crystal”把摧毁水晶作为逃离前必须完成的事；译文“同时别忘了”未保留明确先后要求。冻结邻近任务说明也写明离开前必须摧毁，否则仍会被追踪。证据：`quests/start-ashes.lua:27`、`:38`。此处确认的是任务指示信息遗漏，不断言游戏一定禁止提前离开。

### C55 | entry-03396 | 仅建议

译文“处于隐形（强度 %d）造成的所有伤害……”在两个分句之间缺乏明显停顿，阅读稍显拥挤。但隐形和伤害转换仍可辨认，两个 `%d` 的消费对应也正确，因此仅属可读性建议。

原文的“100%%”改为中文“所有”仍表达全部转换，不构成占位符丢失。证据：`black-magic.lua:146`至其 `tformat` 调用；`timed_effects.lua:1014`、`:1015`。

### C56 | entry-03396 | 待确认

原文“equal to your highest”与译文“相当于你最高……”一致；但源码组合显示，并非严格相等：

- DLC `timed_effects.lua:1016`、`:1017`向两个 `auto_highest` 属性写入数值 `1`。
- 固定本体 `Combat.lua:2339`、`:2376`分别返回最高值加上该属性值。

因此，在这组源码组合下会额外增加一个百分点，而非只取最高值。这是沿袭英文的机制疑点，不是译文新增错误。待确认项是该未固定 commit 的 DLC 快照与目标版本的对应关系。

### C57 | entry-03399 | 存在问题

原文“in radius 4 around you”明确酸池以施法者为中心；译文“在半径 4 的范围内制造”遗漏中心位置。括号“包括自己”说明受伤对象，不能完整替代施放中心限制。

证据：`demon-seeds.lua:214`的 `addEffect` 使用 `self.x, self.y`，`:217`传入半径；`:225`给自己施加抗性与亲和效果。中心遗漏由原文直接确认；源码证据仅代表已核验的 DLC 快照。

### C58 | entry-03403 | 待确认

原文“Demons … will instead be healed”与译文“恶魔不会被伤害，而会被治疗”均未说明例外。

DLC `demon-seeds.lua:810`使用 `DamageType.DEMONFIRE`；固定本体 `damage_types.lua:2600`要求目标具有 `demon` 属性且没有 `fiery_torment`，才在下一行治疗，否则转入火焰伤害分支。

可确认所读本体实现存在这一条件，但尚未核实该状态在目标 DLC 组合中的实际可达性，且 DLC 版本来源未固定。因此保留待确认，归因为沿袭英文的范围概括，而非中文独有错误。

### C59 | entry-03404 | 仅建议

“全体伤害亲和”不如明确指向全部伤害类型的表达自然，但句子主语仍是“你”，并未明确承诺全队或其他生物获得效果，不据此判为作用对象错误。

证据：`demon-seeds.lua:843`只向自身施加效果；`timed_effects.lua:999`增加自身 `damage_affinity.all`。此观察仅属措辞可读性建议，不据术语快照中的 existing 条目要求改名。

### C60 | entry-03407 | 待确认

原文“direct damage”与译文“直接伤害”一致，但所读调用链没有将触发限定于即时攻击伤害：

- DLC `demon-seeds.lua:1227`的回调检查几率、每回合标记及伤害来源的疾病免疫，没有检查持续伤害标记。
- 固定本体 `magical.lua:2253`的疾病 `on_timeout`通过枯萎 projector 造成每回合伤害。
- `damage_types.lua`的 `BLIGHT.projector`调用默认 projector；后者在`:536`调用 `callbackOnTakeDamage`，未因 `from_disease`排除此回调。

因此，持续疾病伤害也存在触发路径。这是英文已有的触发范围疑点；DLC 快照与目标版本对应关系尚未固定，最终适用性保留待确认。

实际读取与边界记录：

冻结包根目录 `P` 为：

`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923`

读取的冻结输入为以下完整路径展开项；40 条的 ID 顺序及全部 source、target 字符串已与 INPUT 对照一致：

| 路径 | SHA-256 |
|---|---|
| `P/INPUT.md` | `95ee9b12c74c7e034b839f792899fc910e574e84569c998c4d8d0238d6f1330c` |
| `P/entries.json` | `5ec766a71d0978588988e8b9b0f0bcdd5227841e5f17ea3bdb494323f9674725` |
| `P/context.lua` | `edd361ad2874ebedd5aa1c1804b72ef40e4675a7765a4ca3f43ba4678b846c9c` |
| `P/source-access.json` | `331874a77a82a63ff0601216ecb2317148097d7bc06091795c0b9468937939cc` |

本组源码根目录 `S = P/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data`。以下六个文件均读取并核对完整哈希，与 source-access 清单匹配：

- `S/lore/demon.lua`（上文 `L`）
- `S/quests/start-ashes.lua`
- `S/talents/corruptions/black-magic.lua`
- `S/talents/corruptions/brutality.lua`
- `S/talents/corruptions/demon-seeds.lua`
- `S/talents/corruptions/demonic-pact.lua`

额外 DLC 根目录 `A` 为清单明确许可的：

`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/ashes-urhrok`

额外读取：

| 路径 | 调用链来源及版本 |
|---|---|
| `A/tome-ashes-urhrok/data/timed_effects.lua` | 由已读技能中的 `EFF_OMINOUS_SHADOW`、`EFF_ACIDIC_BATH`、`EFF_DEMON_SEED_ARMOURED_LEVIATHAN`、`EFF_DEMON_SEED_PAIN_AFFINITY`引入；哈希 `eb183d02dba83a010aac5c7938cf590307b9f99a88de9b7222be7e58f4863f8d`，匹配 |
| `A/tome-ashes-urhrok/superload/mod/class/Actor.lua` | 沿 Actor 类及伤害回调核对允许的 DLC superload；哈希 `aac9ea24be23ed228353cad42b119ba56e83cdf9cc7333484ff98a0d440db346`，匹配 |

本体仅通过 `git -C /workspace/t-engine4 show 624a67329fe2ad440c5b344785a9c73fcf22ae63:<path>`读取以下四个单文件：

| 仓库内路径 | 调用链来源 |
|---|---|
| `game/modules/tome/data/damage_types.lua` | `DamageType.DEMONFIRE`、`DamageType.BLIGHT`及伤害转换消费 |
| `game/modules/tome/class/Actor.lua` | `callbackOnTakeDamage`注册与 Actor 方法调用 |
| `game/modules/tome/class/interface/Combat.lua` | Actor 的明确 `require`，以及已读 `combatGetDamageIncrease`、`combatGetResistPen`调用 |
| `game/modules/tome/data/timed_effects/magical.lua` | 已读 `EFF_WEAKNESS_DISEASE`；另在同文件查询 `FIERY_TORMENT`，未匹配定义 |

未读取其他报告、当前译文文件、SPEC/STATE、其他 commit 或当前源码工作树；未创建子 agent、临时文件或修改仓库。首次默认沙箱读取因挂载隔离错误未执行，随后获准的只读调用成功。未发生读取范围越界。

以上为独立审核观察，不是生产完成判定；C56、C58、C60 的证据缺口如上保留。
