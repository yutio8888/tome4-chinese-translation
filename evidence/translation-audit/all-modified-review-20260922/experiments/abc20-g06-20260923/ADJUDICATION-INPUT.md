# 匿名源码核验与归并：40 条 / 181 项观察

你是本任务独立 REVIEWER。用户要求继续三模型实验并归并问题；本阶段依据源码核验，不参与参赛评分。参考是暂定模型裁决，非人工金标准。禁止寻找模型身份或读取来源映射、原始报告、STATE、其他实验目录。不得以多数票、重复次数、报告声称“已证实”替代证据。

唯一允许输入：本文件、同目录 INPUT.md、entries.json、context.lua、source-access.json、source-access.json 明确列出的冻结源码。先阅读INPUT统一判定规则；沿其限定调用链读取单文件。本体使用git show固定commit；DLC只能使用获准的哈希快照，不能把引擎commit套用于DLC，缺少目标版本适用证据则保留pending；无源码组件仅确认文本可证偏差。后续实验的临时文件已获用户授权，可用自己创建的任务专属临时目录；仓库只读，不创建子agent。

下方181项匿名观察按entry和文字排序，包括问题、建议及待确认。各观察C编号仅为原报告局部编号，不跨观察匹配；统一以O编号标识。保持原断言供核验但不采信。请逐项确认、否决、待确认或仅建议；同条同义缺陷合并为canonical D-ID，不同信息或机制错误拆开。注明翻译新增/沿袭上游。遇实质争议要核实双方论据和完整上下文，证据不足保留pending。缺陷边界应考虑完整界面语境，不把单词必然等同为排他机制断言；也不能因玩家猜得出或英文有同错就豁免。

同时独立检查全部40条，包括没有观察或全部观察被否决的条目，补充漏项。只依据INPUT/源码/语境，不能读取其他轮答案。

输出要求：三个Markdown表格，再补充必要解释与读取路径。
1. 恰好40行：entry-ID | 判定（OK/ISSUE/PENDING） | canonical D或P编号/简短依据。OK包括仅建议；有确认缺陷即ISSUE，即使附带pending；无确认但仍有疑点才PENDING。严格冻结顺序。
2. 确认缺陷表：D-ID（D01起） | entry-ID | 内容、归因及固定源码路径:行号/调用链证据。未决用P-ID另列，不混入D。每个D须实际核验。
3. 恰好181行：O-ID | 状态（confirmed/refuted/pending/advisory/mixed） | 命中D-ID（无则—） | 具体证据与理由。mixed须明确哪些部分confirmed、refuted、pending或advisory；不要把未命中的错误问题借用同条其他正确D。若仅有措辞问题则advisory。补充说明所有未决与主要分歧如何处理。

不要给模型排名或分数、不要修改译文，不宣称DONE_VERIFIED。列出实际读取的路径和额外单文件引入依据；未完成的机制核验如实记录。



## O001 | entry-03373

### C01 | entry-03373 | 存在问题

原文“retain use of their hands”只说明保留双手的使用能力；译文“依旧使用双手作战”增加了作战用途。牺牲其他能力而保留手部能力的身体改造描述，被限定为战斗行为。证据：`L:309`。



## O002 | entry-03373

### C01 | entry-03373 | 存在问题

原文的「covert operations」和「scouts and servants」分别是秘密行动、侦察员与仆役；译文的「藏身的主要根据地」「使者」遗漏了行动及侦察职责。证据：L:309。



## O003 | entry-03373

### C01 | entry-03373 | 存在问题
- **原文**："a prime location for carrying out covert operations"
- **译文**："成为我们的藏身的主要根据地"
- **问题**：“开展秘密行动”被改成了“藏身根据地”，行动这层信息丢失。
- **证据**：纯语义判断；demon.lua:308-309（water imp 雕像）。



## O004 | entry-03373

### C01 | entry-03373 | 存在问题
- **原文短引**：`As our scouts and servants beneath the seas, water imps forego the fire-slinging abilities...`
- **译文短引**：`作为我们在海里的使者，小水怪们放弃了同胞们使用火焰的能力...`
- **问题具体内容**：原文中的“scouts and servants”（侦察兵与仆役）被误译并合并为“使者”。水魔婴在海中的职责是水下侦察与伺候/劳役（对应末尾其在“gathering intelligence”收集情报与建立基地方面的贡献），译为“使者”（emissary/messenger）丢失了关键职能信息与语境因果呼应。
- **状态**：存在问题
- **证据与消费逻辑**：源码路径 [`dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:309`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua#L309)（快照哈希 `d3adada58124ab822393a43a8ec21060a5d465bfca69ff02d4b46df31b92e142`，DLC来源未固定），该段作为恶魔雕像背景 lore，定义了水魔婴作为水下渗透侦察单位的兵种职能。

---



## O005 | entry-03373

### C02 | entry-03373 | 存在问题

「pay tribute」在此承接铭记牺牲和贡献，译成「奉上礼物」变成具体赠礼行为。证据：L:309。



## O006 | entry-03373

### C02 | entry-03373 | 存在问题

原文“carrying out covert operations”“our scouts and servants”描述秘密行动及侦察、服务职责；译文“藏身的主要根据地”“海里的使者”分别变成藏身地点和使者身份。末句虽保留收集情报，仍未完整保留这些具体职责。证据：`L:309`。



## O007 | entry-03373

### C02 | entry-03373 | 存在问题
- **原文**："As our scouts and servants beneath the seas"
- **译文**："作为我们在海里的使者"
- **问题**：“侦察兵与仆从”被改成“使者”，职能变了。下文还说它们在收集情报，与侦察身份相呼应。



## O008 | entry-03373

### C02 | entry-03373 | 存在问题
- **原文短引**：`Remember to pay tribute to the Water Imp whenever you can; since they do not fight alongside our land-based forces, it's all too easy to forget the selfless sacrifices they've made...`
- **译文短引**：`请记得随时为小水怪们奉上礼物，不能因为他们没有同大家在地表作战，就轻易遗忘他们做出的无私牺牲...`
- **问题具体内容**：固定习语“pay tribute to”（向……致敬、缅怀、颂扬其功绩）被曲解误译为“奉上礼物”。恶魔纪念碑文号召恶魔同胞向未在地表并肩作战的水魔婴表达敬意与铭记其牺牲，译为送实体礼物完全背离了铭文纪念致敬的语境与逻辑。
- **状态**：存在问题
- **证据与消费逻辑**：语境证据见 [`demon.lua:309`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua#L309)，后半句紧承“it's all too easy to forget the selfless sacrifices they've made”，语义重心在“缅怀/铭记致敬”而非赠送物质礼品。

---



## O009 | entry-03373

### C03 | entry-03373 | 存在问题

原文“too dangerous to perform on our own soil”指不宜在己方本土进行的危险实验；译文“对于我们的土壤来说过于危险”把实验地点限制改成土壤受害对象。证据：`L:309`，同句列举海洋基地的用途。



## O010 | entry-03373

### C03 | entry-03373 | 存在问题
- **原文**："Remember to pay tribute to the Water Imp"
- **译文**："请记得随时为小水怪们奉上礼物"
- **问题**：pay tribute to 在这里是“致敬、缅怀”，译成“奉上礼物”改变了行为含义。下文说的是不要遗忘它们的牺牲，属于致敬语境。



## O011 | entry-03373

### C04 | entry-03373 | 仅建议
- **原文**："retain use of their hands"
- **译文**："依旧使用双手作战"
- **说明**：多了“作战”，但不影响整句论点，只是措辞偏好。



## O012 | entry-03374

### C03 | entry-03374 | 存在问题

「holding the front lines against the hordes of Eyal」说明抵御埃亚尔大军；「奋战在埃亚尔边界前线」改写了地点，且未交代对抗对象。证据：L:316。



## O013 | entry-03374

### C03 | entry-03374 | 存在问题
- **原文短引**：`the children of onyx focus on making new constructs from scratch, lashing flesh, magic, and steel together into towering creations...`
- **译文短引**：`而玛瑙色的孩子们专心学习新的构架体，将魔法、血肉和钢铁融为一体...`
- **问题具体内容**：“focus on making new constructs from scratch”被误译为“专心学习新的构架体”。原文对照前文红宝石之子 study 魔法、绿翡翠之子 study 肉体改造，指出玛瑙之子专注于“从零开始制造新的构装体”，译文把“making”（制造）误译为“学习”，且漏译“from scratch”（从零开始/白手起家），严重失真。
- **状态**：存在问题
- **证据与消费逻辑**：源码路径 [`demon.lua:316`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua#L316)，此处阐述玛瑙恶魔作为工程师种族从零制造血肉机械构装体的核心设定。

---



## O014 | entry-03374

### C04 | entry-03374 | 存在问题

原文“holding the front lines against the hordes of Eyal”说明抵御埃亚尔军众、坚守前线；译文“奋战在埃亚尔边界前线”新增地理边界，并遗漏抵御对象。证据：`L:316`。



## O015 | entry-03374

### C04 | entry-03374 | 存在问题

夸塞魔「very much machines」，肌肉被强化而保留聪明头脑；译文改述为「钢铁般的纪律和强大的近战能力」，丢失其制造方式与身体、心智能力的关系。证据：L:316。



## O016 | entry-03374

### C04 | entry-03374 | 存在问题
- **原文短引**：`Though they are mostly flesh, the warrior onyx known as Quasits are very much machines, made with bolstered muscles without losing the clever minds they come from.  As eager as they are brilliant, Quasits are well-disciplined and capable in combat...`
- **译文短引**：`尽管仍是血肉之躯，玛瑙战士——或者说夸塞魔——有着钢铁般的纪律和强大的近战能力...`
- **问题具体内容**：整整大半句核心设定严重漏译。原文中紧随转折后的“are very much machines, made with bolstered muscles without losing the clever minds they come from. As eager as they are brilliant”（在很大程度上宛如机器，强化了肌肉的同时并未丧失其源自种族的聪慧头脑；他们既充满热忱又聪慧过人）被整段丢弃，导致夸塞魔“血肉机械构装、增强肌肉却保留玛瑙族智力、兼具热忱与聪慧”的描述完全丢失。
- **状态**：存在问题
- **证据与消费逻辑**：源码路径 [`demon.lua:316`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua#L316)，该句是连接上文制造工艺与下文纪律特性的核心定性说明。

---



## O017 | entry-03374

### C05 | entry-03374 | 存在问题

原文“study new magical spells for our arsenal”是研究新法术以扩充己方武备；译文“学习兵工厂新的魔法”把用途关系改成法术属于兵工厂，并将研究改成学习。证据：`L:316`。



## O018 | entry-03374

### C05 | entry-03374 | 存在问题
- **原文**："study new magical spells for our arsenal"
- **译文**："学习兵工厂新的魔法"
- **问题**：arsenal 在这里指“法术储备”，被误解成实体“兵工厂”，作用对象错了。



## O019 | entry-03374

### C05 | entry-03374 | 存在问题
- **原文短引**：`...with Forge-Giant-produced armor bolted onto their skin at "birth."`
- **译文短引**：`...一“出生”就身着锻造巨人亲制的护甲。`
- **问题具体内容**：“bolted onto their skin”（用螺栓钉在/固定在皮肤上）被弱化误译为普通的“身着”。恶魔工厂在流水线半成熟体“出生”时将锻造巨人打造的装甲直接用螺栓钉入肉体的冷酷改造设定丢失。
- **状态**：存在问题
- **证据与消费逻辑**：源码路径 [`demon.lua:316`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua#L316)。

---



## O020 | entry-03374

### C06 | entry-03374 | 存在问题

原文“making new constructs from scratch”描述从零制造构装体，后接组成高大造物的过程；译文“专心学习新的构架体”遗漏制造行为和从零创造的含义。这一判断不依赖强制采用某个术语译名。证据：`L:316`。



## O021 | entry-03374

### C06 | entry-03374 | 存在问题
- **原文**："focus on making new constructs from scratch"
- **译文**："专心学习新的构架体"
- **问题**：“从零制造”被改成“学习”，动作错了，和本句三方分工的对比（研究法术／强化身体／制造构造体）也对不上。



## O022 | entry-03374

### C07 | entry-03374 | 存在问题

原文护甲在“出生”时“bolted onto their skin”；译文仅说“一‘出生’就身着……护甲”，遗漏护甲被固定到皮肤上的身体构造信息。证据：`L:316`。



## O023 | entry-03374

### C07 | entry-03374 | 存在问题
- **原文**："the warrior onyx known as Quasits are very much machines, made with bolstered muscles without losing the clever minds they come from.  As eager as they are brilliant, Quasits are well-disciplined…"
- **译文**："尽管仍是血肉之躯，玛瑙战士——或者说夸塞魔——有着钢铁般的纪律和强大的近战能力"
- **问题**：丢失了四项信息：“本质上近乎机器”“强化的肌肉”“保留原有的聪明头脑”“热忱与聪慧并重”。“钢铁般的纪律”是新增内容。



## O024 | entry-03374

### C08 | entry-03374 | 仅建议
- **现象**：children of onyx 在本条译作“玛瑙色的孩子们”“玛瑙战士”，本批 03379、03383、03388、03389 用的是“缟玛瑙之子”。
- **说明**：context.lua 中两种写法都有（缟玛瑙 10 处，玛瑙色 3 处），读者仍能认出指称，属于统一性偏好，不扩大为全局改名。



## O025 | entry-03374

### C08 | entry-03374 | 存在问题

原文明确说明夸塞魔虽主要由血肉组成，却近似机器，拥有强化肌肉，并保留原有聪明头脑；译文直接转为“钢铁般的纪律和强大的近战能力”，遗漏这组制造结果与智力保留信息。证据：`L:316`。



## O026 | entry-03375

### C05 | entry-03375 | 存在问题

「no less aggressive」比较的是攻击性；「不比酸液树魔杀伤力小」改成了杀伤力比较。证据：L:342。



## O027 | entry-03375

### C06 | entry-03375 | 存在问题
- **原文短引**：`Although no less aggressive than their younger counterparts, wretch titans generally have a much higher survival rate...`
- **译文短引**：`他们不比酸液树魔杀伤力小，同时生存率要高得多...`
- **问题具体内容**：“no less aggressive”（凶猛好斗、攻击性丝毫不减）被误译为“不比……杀伤力小”。上文已明确比喻树魔是箭矢、泰坦是抛石机巨石并造成毁灭性破坏，泰坦破坏力本就远大于幼体树魔；此处对比的是其性格攻击性（虽体型巨大、生存率高，但凶悍激进的攻击性与幼体无异）。译为“杀伤力”导致逻辑违和与词义扭曲。
- **状态**：存在问题
- **证据与消费逻辑**：源码路径 [`demon.lua:342`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua#L342)。

---



## O028 | entry-03375

### C09 | entry-03375 | 存在问题

原文“no less aggressive”比较的是攻击性；译文“不比酸液树魔杀伤力小”比较伤害能力。随后有关力量和体型的说明不能使这两种属性等价。证据：`L:342`。



## O029 | entry-03375

### C09 | entry-03375 | 存在问题
- **原文**："Although no less aggressive than their younger counterparts, wretch titans generally have a much higher survival rate"
- **译文**："他们不比酸液树魔杀伤力小"
- **问题**：aggressive（好斗、冲锋性）被改成“杀伤力”。原句的逻辑是“同样好斗却更能活下来”，改成杀伤力后这层对比不成立。



## O030 | entry-03376

### C06 | entry-03376 | 存在问题

三分之二人口的范围包括拥有多雷格、与其同住、**或仅与其共事**的人；「在生活中都有一只多雷格陪伴」把这些关系合并成生活陪伴。证据：L:349。



## O031 | entry-03376

### C10 | entry-03376 | 仅建议
- **原文**："rather intelligent for a beast"
- **译文**："比野兽更有智力"
- **说明**：译文略有“不算野兽”的歧义，“尽数我们为战争作出的牺牲”用词也生硬。整体语义没有丢失。



## O032 | entry-03376

### C10 | entry-03376 | 存在问题

原文“rather intelligent for a beast”是在野兽这一类别内评价其聪明；译文“比野兽更有智力”改成与野兽整体比较，改变了比较范围。证据：`L:349`。



## O033 | entry-03376

### C11 | entry-03376 | 存在问题

原文只说失去温柔伙伴可能“troubles us the most”；译文增加“可能是最大、也是最困扰我们的一项”，额外认定它是最大的战争牺牲。最令人困扰不等于牺牲规模最大。证据：`L:349`。



## O034 | entry-03377

### C07 | entry-03377 | 存在问题

叙述者称夏·图尔的设计「devious」；「绝妙的例子」抹去了其狡诈、险恶的评价。证据：L:356。



## O035 | entry-03377

### C11 | entry-03377 | 存在问题
- **原文**："a good example of the devious designs the Sher'Tul had in mind"
- **译文**："夏·图尔人制造或者改变埃亚尔种族的一个绝妙的例子"
- **问题**：“阴险的用心（devious designs）”丢失，还新增了褒义的“绝妙”，评价方向反了。



## O036 | entry-03377

### C12 | entry-03377 | 存在问题

原文将米诺陶作为夏·图尔“devious designs”的例子，包含对其创造意图阴险、诡诈的评价；译文仅称制造或改变种族的“绝妙的例子”，丢失这一态度信息。证据：`L:356`。



## O037 | entry-03377

### C12 | entry-03377 | 存在问题
- **原文**："horned beast-men"
- **译文**："长角的兽人"
- **问题**：术语快照中 Orc 固定为“兽人”（T.PN.RACE）。这里用“兽人”指米诺陶，会被读成“长角的兽人（orc）”，与已登记的种族名冲突。



## O038 | entry-03378

### C07 | entry-03378 | 存在问题
- **原文短引**：`In the high-energy divisions, those competing are typically not born in the conventional manner, usually being constructs made by a team performing a collaborative effort.`
- **译文短引**：`在最高能量的组别，那些挑战者并不是正常出生的天才，而是在各个比赛有关的研究团队团结合作，精心设计的产物。`
- **问题具体内容**：“not born in the conventional manner”（不是以常规方式出生）被无中生有脑补增译出“天才”二字（“并不是正常出生的天才”），扭曲了原文单纯指代人造构装生物非自然胎生的说明。
- **状态**：存在问题
- **证据与消费逻辑**：源码路径 [`demon.lua:370`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua#L370)。

---



## O039 | entry-03378

### C08 | entry-03378 | 存在问题

赛制按出生以来消耗能量的**最高额度**分组，另一赛场是「forest of pillars」；译文只说消耗能量，并将柱林写成「复杂迷宫」。两处赛制条件均改变。证据：L:370。



## O040 | entry-03378

### C08 | entry-03378 | 存在问题
- **原文短引**：`Once they arrive on the surface, Eyal will experience a few fleeting moments of terror before their utter annihilation.`
- **译文短引**：`只要他们组成的军队成批到达埃亚尔，那些弱小的生物瞬间就会被他们强大的力量彻底歼灭。`
- **问题具体内容**：结句关键信息严重篡改丢失。原文意为“一旦他们抵达地表，埃亚尔将在被彻底歼灭前经历短暂的恐惧”，译文将埃亚尔体验短暂恐惧的主谓结构全部抹去，臆造增添“成批到达”、“那些弱小的生物”、“被强大的力量”等原文完全不存在的词句，信息结构严重失真。
- **状态**：存在问题
- **证据与消费逻辑**：源码路径 [`demon.lua:370`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua#L370)。

---



## O041 | entry-03378

### C09 | entry-03378 | 存在问题

造物在间接战斗组「performing adequately」，译成「相当出色」提高了其表现等级。证据：L:370。



## O042 | entry-03378

### C10 | entry-03378 | 存在问题

制造方法使用「sustainable amount of energy-input」，即能持续承担的投入；「通过很少的能量」改成了绝对耗能很低。证据：L:370。



## O043 | entry-03378

### C11 | entry-03378 | 存在问题

原文说埃亚尔在彻底毁灭前还会经历短暂恐惧；「瞬间……彻底歼灭」删去了这段时序与恐惧体验。证据：L:370。



## O044 | entry-03378

### C13 | entry-03378 | 存在问题

原文“most straightforward … for the spectator”说明比赛最直观、易于观众理解；译文“最为熟悉”改成观众熟悉程度，且增加“有些人不知道”的叙述。证据：`L:370`。



## O045 | entry-03378

### C13 | entry-03378 | 存在问题
- **原文**："the most straightforward of our competitions for the spectator, but those competing have a huge variety of possible divisions"
- **译文**："对我们的观众来说最为熟悉的比赛，然而有些人不知道的是……"
- **问题**：“最直观易懂”被改成“最熟悉”；“有些人不知道的是”为新增；原句“观众看着简单、参赛者分组繁多”的对比丢失。



## O046 | entry-03378

### C14 | entry-03378 | 存在问题

原文组别依据包含“maximum”及“since (and including) birth”；译文“从出生开始所消耗的能量”未保留能量上限与出生本身也计入的限定。对于工厂制造的参赛造物，出生投入与出生后消耗并不等价。证据：`L:370`，后文紧接参赛者制造方式。



## O047 | entry-03378

### C14 | entry-03378 | 存在问题
- **原文**："based on the maximum amount of energy consumed by their entrants since (and including) birth"
- **译文**："来自于选手从出生开始所消耗的能量"
- **问题**：删掉了“最大值／上限”。分组依据的是能耗上限（类似体重级别），删除后分组标准就变了。



## O048 | entry-03378

### C15 | entry-03378 | 存在问题

原文场地是难以穿行的“forest of pillars”；译文改为“复杂迷宫”，遗漏密集柱林这一场地结构。证据：`L:370`。



## O049 | entry-03378

### C15 | entry-03378 | 存在问题
- **原文**："a difficult-to-navigate forest of pillars"
- **译文**："复杂迷宫"
- **问题**：赛场类型从“石柱林”变成了“迷宫”。



## O050 | entry-03378

### C16 | entry-03378 | 存在问题

原文说高能组参赛者“typically”不按常规出生，“usually”由团队制造；译文改为“最高能量”的组别，并无条件断言参赛者都是团队产物，还增加“天才”。组别范围与通常成立的限定均被改变。证据：`L:370`。



## O051 | entry-03378

### C16 | entry-03378 | 存在问题
- **原文**："while performing adequately in the less-direct ones"
- **译文**："在其他复杂的环境下也有相当出色的表现"
- **问题**：“表现尚可”被夸大成“相当出色”，程度不符。



## O052 | entry-03378

### C17 | entry-03378 | 存在问题

原文在非直接战斗组别“performing adequately”；译文“有相当出色的表现”明显提高评价等级，削弱了其主要优势在开放场地正面战斗的对比。证据：`L:370`。



## O053 | entry-03378

### C17 | entry-03378 | 存在问题
- **原文**："with a sustainable amount of energy-input"
- **译文**："通过很少的能量"
- **问题**：“可持续的能量投入”被改成“很少的能量”，程度信息错了。



## O054 | entry-03378

### C18 | entry-03378 | 仅建议
- **原文**："a few fleeting moments of terror before their utter annihilation"
- **译文**："瞬间就会被……彻底歼灭"
- **说明**：丢了“短暂的恐惧”这层渲染，但“迅速歼灭”的主干保留了，属于修辞层面。



## O055 | entry-03378

### C18 | entry-03378 | 存在问题

原文制造所需能量为“a sustainable amount”；译文“很少的能量”把可持续承担的投入改成绝对低投入。证据：`L:370`。



## O056 | entry-03378

### C19 | entry-03378 | 存在问题

原文成为军队骨干有“once mass-production is in order”的前提；译文直接宣布将成为中流砥柱，遗漏量产准备就绪这一条件。末句“成批到达”描述部署，不能替代生产条件。证据：`L:370`。



## O057 | entry-03378

### C20 | entry-03378 | 存在问题

原文明确描写彻底毁灭前短暂的恐惧时刻；译文只说弱小生物瞬间被歼灭，遗漏这一先恐惧、后毁灭的叙事过程。证据：`L:370`。



## O058 | entry-03379

### C09 | entry-03379 | 存在问题
- **原文短引**：`...heating raw metal with their magic until it is workable, then pounding it into their shape, automatically imbuing the resulting armor and weaponry with Urh'Rok's blessing.`
- **译文短引**：`...将金属的原材料用魔法熔炼，然后将其导入模具中，自动锻造成注入了乌鲁洛克的祝福的魔钢武器和护甲。`
- **问题具体内容**：“pounding it into their shape”（挥舞巨锤捶打/锻打成形）被脑补误译为“将其导入模具中”；且脑补添加了原文没有的“魔钢”。锻造巨人手持神赐巨锤日夜捶击锻打（pounding），浇铸进模具与挥锤锻打工艺相反，破坏了巨人之锤挥舞敲击的叙事机制。
- **状态**：存在问题
- **证据与消费逻辑**：源码路径 [`demon.lua:377`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua#L377)，后文紧接“every single swing produces several pieces of usable equipment”（每一次挥锤敲击产出多件装备），证明其为挥锤锻打机制。

---



## O059 | entry-03379

### C10 | entry-03379 | 存在问题
- **原文短引**：`Thanks to an assortment of detachable heads for these hammers, every single swing produces several pieces of usable equipment.`
- **译文短引**：`在各种可拆卸的锤头的帮助下，只要一击就能瞬间制造出数个装备零件。`
- **问题具体内容**：“several pieces of usable equipment”（数件可用装备，如护甲与武器成品）被降格误译为“数个装备零件”。巨人之锤一击能直接锻造出整件成品装备，译成零件削弱了神迹与生产力描述，并与后文“bolstering the rest of our forces with blessed equipment”（以受祝福的装备武装全军）脱节。
- **状态**：存在问题
- **证据与消费逻辑**：源码路径 [`demon.lua:377`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua#L377)。

---



## O060 | entry-03379

### C12 | entry-03379 | 存在问题

原文明确说只有声称乌鲁洛克力量「无限」才算夸大；译文称「没有什么词语比‘无穷无尽’更加合适」，把唯一的夸大说法当成准确描述。证据：L:377。



## O061 | entry-03379

### C13 | entry-03379 | 存在问题

锻造巨人的设计牺牲的是速度和**制造时的能量效率**；「行动速度和能量燃率」把制造成本改写为能量燃烧速率。证据：L:377。



## O062 | entry-03379

### C14 | entry-03379 | 存在问题

原文是把金属加热至可加工后用锤敲出形状，且每一锤产出数件可用装备；「导入模具」「装备零件」改写了工艺和产物。证据：L:377。



## O063 | entry-03379

### C19 | entry-03379 | 存在问题
- **原文**："as such, he cannot spend time or effort making equipment"
- **译文**："他或许没有足够的时间和精力"
- **问题**：确定的“不能”被弱化成推测的“或许”，情态变了。



## O064 | entry-03379

### C20 | entry-03379 | 存在问题
- **原文**："built for raw strength at the expense of speed and energy-efficient creation"
- **译文**："以牺牲一定行动速度和能量燃率的代价"
- **问题**：原文说的是“造出它们的能量效率”（即制造成本更高），译文变成了意义不明的“能量燃率”，好像在说运行能耗。另外“一定”也是新增的。



## O065 | entry-03379

### C21 | entry-03379 | 存在问题

原文“cannot be overstated, except by claiming it to be infinite”明确把“无限”排除在合理形容之外；译文却说没有比“无穷无尽”更合适的形容，意义反转。证据：`L:377`。



## O066 | entry-03379

### C21 | entry-03379 | 存在问题
- **原文**："heating raw metal with their magic until it is workable, then pounding it into their shape"
- **译文**："用魔法熔炼，然后将其导入模具中"
- **问题**：“用锤锻打成型”被改成“浇铸入模”，和本条“巨锤锻造”的核心设定矛盾。



## O067 | entry-03379

### C22 | entry-03379 | 存在问题

原文“he cannot spend time or effort”明确表示无法亲自制造军队装备；译文“他或许没有足够的时间和精力”将确定限制变成猜测。证据：`L:377`。



## O068 | entry-03379

### C22 | entry-03379 | 存在问题
- **原文**："every single swing produces several pieces of usable equipment"
- **译文**："一击就能瞬间制造出数个装备零件"
- **问题**：“几件可用的成品装备”被改成“装备零件”，产出性质错了。



## O069 | entry-03379

### C23 | entry-03379 | 存在问题

原文牺牲的是“energy-efficient creation”，即制造这些改造体的能量效率；译文“能量燃率”改成未说明的能量燃烧指标，丢失制造阶段的限定。证据：`L:377`。



## O070 | entry-03379

### C24 | entry-03379 | 存在问题

原文是加热金属至可加工，再锤打成形；译文写成熔炼后导入模具，并增加“魔钢”材质。加工方式和材料信息均发生变化。证据：`L:377`，巨锤及可拆卸锤头说明也支持锻打语境。



## O071 | entry-03379

### C25 | entry-03379 | 存在问题

原文每次挥锤产生数件“usable equipment”；译文“数个装备零件”把可用成品改为部件。证据：`L:377`。



## O072 | entry-03380

### C15 | entry-03380 | 存在问题

俘虏因事故「mortally wounded」是受了致命伤；「当场惨死」提前宣告死亡，改变后文利用其身体与生命精华的时序。证据：L:384。



## O073 | entry-03380

### C16 | entry-03380 | 存在问题

被操纵的造物向自以为的「tormentors」报复；「自己眼中的‘敌人’」丢失了施虐者这一认知及引号的讽刺作用。证据：L:384。



## O074 | entry-03380

### C23 | entry-03380 | 仅建议
- **原文**："Thanks to numerous contacts we have on Eyal's surface, ranging from easily-duped natives to our own scouting teams"
- **译文**："源于我们对埃亚尔大陆的多次接触"
- **说明**：contacts 原指“人脉、联络人”，译成“多次接触”，但后半句的列举让读者仍能理解。



## O075 | entry-03380

### C24 | entry-03380 | 仅建议
- **现象**：
  - "ends up mortally wounded" 译作“当场惨死”；
  - "try to preserve" 译作“曾经试图”；
  - "'tormentors'" 译作“敌人”。
- **说明**：细节有偏移，但“俘虏死后被拼接再利用、被导向攻击同胞”的主线和反讽基本保留。



## O076 | entry-03380

### C26 | entry-03380 | 存在问题

原文“contacts … ranging from … natives to … scouting teams”指己方在地表的联系人或联系网络；译文“对埃亚尔大陆的多次接触”改为接触次数，丢失取得俘虏的人员渠道。证据：`L:384`。



## O077 | entry-03380

### C27 | entry-03380 | 存在问题

原文俘虏“ends up mortally wounded”，随后说明不让其以死亡逃脱；译文提前写成“当场惨死”，改变死亡时点，并削弱后续阻止死亡解脱的因果关系。证据：`L:384`。



## O078 | entry-03380

### C28 | entry-03380 | 存在问题

原文被攻击者在拼合生物眼中是“tormentors”；译文仅为“敌人”，遗漏复仇认知被转移后，将原同胞视作折磨者的具体信息。证据：`L:384`，前句明确提到重定向复仇本能。



## O079 | entry-03381

### C11 | entry-03381 | 存在问题
- **原文短引**：`#927e64#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#LAST#arness their fear and suspici#927e64#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#LAST#`
- **译文短引**：`#927e64#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～#LAST#卸下他们的恐惧和怀#927e64#～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～#LAST#`
- **问题具体内容**：“[h]arness their fear and suspici[on]”（利用/驾驭他们的恐惧与猜疑）被严重误译为“卸下他们的恐惧和怀”。恶魔在转化多瑟顿刺客时是利用吸收被捕者的负面情感，而非“卸下”释怀，词义产生完全相反的颠倒。
- **状态**：存在问题
- **证据与消费逻辑**：源码路径 [`demon.lua:393`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua#L393)。残卷词根 `arness` 明显对应 `harness`。

---



## O080 | entry-03381

### C12 | entry-03381 | 存在问题
- **原文短引**：`...#LAST#king them a val#927e64#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#LAST#tion to our intel-gathering camps.`
- **译文短引**：`...#LAST#给他们一个#927e64#～～～～～～～～～～～～～～~#LAST#息提供给了我们的情报机构。`
- **问题具体内容**：“[ma]king them a val[uable addition] to our intel-gathering camps”（使他们成为我们情报搜集营地的宝贵补充）中，`king them a val` 被误解断句为“给他们一个”。`king` 是 `making` 的词尾，`val` 是 `valuable` 的词头，译为“给他们一个”完全破坏了残卷语法与语义。
- **状态**：存在问题
- **证据与消费逻辑**：源码路径 [`demon.lua:393`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua#L393)。

---



## O081 | entry-03381

### C25 | entry-03381 | 存在问题
- **原文片段**："…arness their fear and suspici…"（harness）
- **译文**："卸下他们的恐惧和怀"
- **问题**：harness 是“利用”，被译成“卸下”，词义相反。
- **格式核验**：原文与译文各有 10 个 `#927e64#`、10 个 `#LAST#`，`#{italic}#`／`#{bold}#`／`#{normal}#` 序列一致。全角波浪线约为原文数量的一半，显示宽度相当，不构成格式缺陷。



## O082 | entry-03381

### C26 | entry-03381 | 存在问题
- **原文片段**："…king them a val…" / "…tion to our intel-gathering camps. Redee…"（making them a valuable addition to…）
- **译文**："给他们一个…" / "…息提供给了我们的情报机构。为了偿…"
- **问题**：“使其成为情报营地的宝贵补充”被重构成“给他们一个……信息提供给情报机构”，残片对应的语义错了。



## O083 | entry-03381

### C29 | entry-03381 | 存在问题

可见原文残片“arness their fear and suspici…”对应利用、驾驭恐惧与猜疑；译文“卸下他们的恐惧和怀…”变成解除这些情绪。遮蔽文本不要求补全，但仍应保留可辨残片的方向。证据：`L:393`。未将波浪线宽度变化判为格式缺陷。



## O084 | entry-03382

### C13 | entry-03382 | 存在问题
- **原文短引**：`...will occasionally emit a shade of one of our fallen citizens, imbued by some of Urh'Rok's power...`
- **译文短引**：`...附近经常徘徊着我们牺牲同胞的灵魂——即使是那些已经关闭的传送门也不例外。`
- **问题具体内容**：“occasionally emit a shade of one of our fallen citizens”（偶尔会吐出/喷射出一个牺牲同胞的幽魂）被误译为“附近经常徘徊着……灵魂”。频率从“occasionally”（偶尔）篡改为“经常”；产生机制从传送门喷出幽魂（即毁灭女妖 Ruin Banshee 的生成机制）篡改为“在附近徘徊”，严重失真。
- **状态**：存在问题
- **证据与消费逻辑**：源码路径 [`demon.lua:404`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua#L404)，本雕像 lore 所解释的正是毁灭女妖如何在埃亚尔传送门被动现身。

---



## O085 | entry-03382

### C17 | entry-03382 | 存在问题

原文是传送门**偶尔放出**亡者阴影，包括已彻底停用的门；译文说阴影「经常徘徊」在门附近，改变出现频率和发生方式。证据：L:404。



## O086 | entry-03382

### C27 | entry-03382 | 存在问题
- **原文**："will occasionally emit a shade of one of our fallen citizens"
- **译文**："附近经常徘徊着我们牺牲同胞的灵魂"
- **问题**：频率从“偶尔”变成“经常”，动作从“从门中涌出”变成“在附近徘徊”。



## O087 | entry-03382

### C28 | entry-03382 | 存在问题
- **原文**："warped to insanity by its transit"
- **译文**："被折磨地几近疯狂"
- **问题**：原文是已经发疯，译文变成“几近疯狂”，程度降低了。“smelling of Mal'Rok's ashes”译作“被灰烬所环绕”也有轻微偏移。



## O088 | entry-03382

### C30 | entry-03382 | 存在问题

原文传送门“occasionally emit a shade”；译文改为传送门附近“经常徘徊着”灵魂，同时改变发生频率及出现方式。证据：`L:404`。



## O089 | entry-03382

### C31 | entry-03382 | 存在问题

原文“warped to insanity”表示已被扭曲至疯狂；译文“几近疯狂”改成尚未达到疯狂。证据：`L:404`。



## O090 | entry-03382

### C32 | entry-03382 | 存在问题

原文“smelling of Mal'Rok's ashes”是带有灰烬气味；译文“被玛·洛克的灰烬所环绕”改为实体灰烬围绕的视觉现象。证据：`L:404`。



## O091 | entry-03383

### C14 | entry-03383 | 仅建议
- **原文短引**：`...work his skills into a mass-producible artifact... reverse-engineering the Sher'Tul portals...`
- **译文短引**：`...将他的技术融入工艺品并量产化... 反向驱动夏·图尔的传送门...`
- **问题具体内容**：“artifact”在奇幻魔导语境下一般指魔导器或神器，译为“工艺品”偏向手工艺品；“reverse-engineering”译为“反向驱动”略偏生硬（一般为逆向工程/反向解析）。但由于原句意思尚能理解且无事实断裂，仅属用词偏好。
- **状态**：仅建议
- **证据与消费逻辑**：源码路径 [`demon.lua:414`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua#L414)。

---



## O092 | entry-03383

### C18 | entry-03383 | 存在问题

德瑞宝被传正在「reverse-engineering」传送门，即研究、逆向解析；「反向驱动」指反方向操作，技术行为不同。证据：L:414。



## O093 | entry-03383

### C29 | entry-03383 | 存在问题
- **原文**："he's been reverse-engineering the Sher'Tul portals"
- **译文**："他正在反向驱动夏·图尔的传送门"
- **问题**：“逆向工程／逆向解析”被译成“反向驱动”，意思变成了让传送门反向运行。同批 03384 用的是正确的“逆向解析”。



## O094 | entry-03383

### C30 | entry-03383 | 存在问题
- **原文**："work his skills into a mass-producible artifact"
- **译文**："将他的技术融入工艺品并量产化"
- **问题**：这里 artifact 指能赋予传送能力的魔法造物，“工艺品”是装饰性手工品，物品性质错了。



## O095 | entry-03383

### C31 | entry-03383 | 仅建议
- **现象**：“之一—缟玛瑙之子德瑞宝——”，前半用单个破折号，后半用双破折号。
- **说明**：属于标点规范问题，不影响信息。



## O096 | entry-03383

### C33 | entry-03383 | 存在问题

原文“reverse-engineering the Sher'Tul portals”指逆向研究传送门技术；译文“反向驱动……传送门”改成反方向运行设备。证据：`L:414`，上下文是学者研究、量产传送能力的工作。



## O097 | entry-03384

### C19 | entry-03384 | 存在问题

神经系统被重接、以痛为乐是「rare occasion」；译文仅写「又或者是……情况」，丢失其罕见程度。证据：L:421。



## O098 | entry-03384

### C32 | entry-03384 | 存在问题
- **原文**："all of them appear with nearly every shred of their essence drained"
- **译文**："他们的每一丝生命精华已被汲取殆尽"
- **问题**：删掉了 nearly，“几乎耗尽”变成“完全耗尽”，与后句“陷于死亡边缘（仍活着）”相矛盾。



## O099 | entry-03384

### C33 | entry-03384 | 存在问题
- **原文**："the frequent cases of internal bleeding and the rare occasion of them appearing with a rewired nervous system"
- **译文**："又或者是神经网络重接导致……的情况"
- **问题**：保留了“常见”，却删掉了“罕见”，原文“常见 vs 罕见”的频率对比丢失。



## O100 | entry-03384

### C34 | entry-03384 | 仅建议
- **现象**：正文写“莎西·凯希”，本条所属雕像标题（demon.lua:420；context.lua:315）写“恶魔雕像：莎西凯希”。
- **说明**：只差间隔号，指称不变，属于统一性问题，不扩大为全局改名。



## O101 | entry-03384

### C34 | entry-03384 | 存在问题

原文将神经系统重接、把疼痛当快乐的现象限定为“rare occasion”；译文保留体内出血“常见”，却删除后一现象罕见的限定，丢失两类受试者情况的频率对比。证据：`L:421`。



## O102 | entry-03388

### C15 | entry-03388 | 存在问题
- **原文短引**：`I could have fought back, but I kept telling myself only to lash out once I was sure my life was in danger...`
- **译文短引**：`我本可以反击，然而我一直忍耐，想着只要在真正有性命之虞的时候抽身逃走就行...`
- **问题具体内容**：“only to lash out once I was sure my life was in danger”（告诫自己只有确信生命受到威胁时才出手痛击/猛烈反击）被严重误译为“只要在真正有性命之虞的时候抽身逃走就行”。将痛下杀手猛烈反击（lash out）曲解为消极逃跑，与下文莎西·凯希最终狂怒施展死灵禁咒反杀全场的情绪与行动逻辑产生直接冲突。
- **状态**：存在问题
- **证据与消费逻辑**：语境证据见 [`demon.lua:452`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua#L452)。

---



## O103 | entry-03388

### C16 | entry-03388 | 存在问题
- **原文短引**：`...when the "demons" are dripping acid into your eyes, then growing them back with more nerve endings than before so you can feel the pain more acutely...`
- **译文短引**：`...当“恶魔们”将酸液滴入你的眼球，再将它放回神经更加密集的地方去，于是你会感到更加剧烈的痛苦。`
- **问题具体内容**：“growing them back with more nerve endings than before”（让眼球重新生长出来，并带有比以往更多的神经末梢）被严重误译为“再将它放回神经更加密集的地方去”。将用黑魔法让被酸液溶解的眼球重新再生并密集增生神经末梢的残酷酷刑，荒谬曲解为“把眼球放回某个地方”，语义严重失真崩塌。
- **状态**：存在问题
- **证据与消费逻辑**：语境证据见 [`demon.lua:458`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua#L458)。

---



## O104 | entry-03388

### C20 | entry-03388 | 存在问题

「had barely escaped feudalism」指刚刚脱离封建制度；「还没脱离封建社会」把状态反转。证据：L:448。



## O105 | entry-03388

### C21 | entry-03388 | 存在问题

袭击者是愤怒的「peasants」；「无知难民」把农民改成了难民。证据：L:450。



## O106 | entry-03388

### C22 | entry-03388 | 存在问题

叙述者决定只有确信生命受威胁才会「lash out」反击；「抽身逃走」改成逃跑，改变她当时的行动界限。证据：L:452。



## O107 | entry-03388

### C23 | entry-03388 | 存在问题

「Even if I wanted to」是假设即便自己想阻止入侵也做不到；「尽管我很想这么做」肯定了她想阻止入侵的意愿。证据：L:458。



## O108 | entry-03388

### C24 | entry-03388 | 存在问题

恶魔会把受酸液损伤的眼睛「growing them back with more nerve endings」重新长出；「再将它放回神经更加密集的地方」误成移动眼睛的位置。证据：L:458。



## O109 | entry-03388

### C35 | entry-03388 | 存在问题

原文说被刮去的文字谈论“his accomplishments … and his mysterious disappearance”，未称其为本人自述；译文“一个博物学者喋喋不休地讲述他的成就和……失踪”将博物学者变成叙述者。证据：`L:446`及雕像说明语境。



## O110 | entry-03388

### C35 | entry-03388 | 存在问题
- **原文**："such savages that had barely escaped feudalism"
- **译文**："还没脱离封建社会的野蛮人"
- **问题**：“刚刚勉强脱离”被改成“尚未脱离”，事实反转。



## O111 | entry-03388

### C36 | entry-03388 | 存在问题

原文“had barely escaped feudalism”表示刚刚或勉强脱离封建制；译文“还没脱离封建社会”否定了脱离这一事实。证据：`L:448`。



## O112 | entry-03388

### C36 | entry-03388 | 存在问题
- **原文**："an enraged horde of peasants, provoked by our unfortunate choice of disguises"
- **译文**："大量的无知难民"
- **问题**：“农民”变成“难民”，行动主体错了；“愤怒的”也丢了。



## O113 | entry-03388

### C37 | entry-03388 | 存在问题

原文围攻者是“peasants”；译文“大量的无知难民”把农民身份改为难民。灾难发生并不能直接证明这些人具有难民身份。证据：`L:450`。



## O114 | entry-03388

### C37 | entry-03388 | 存在问题
- **原文**："I kept telling myself only to lash out once I was sure my life was in danger"
- **译文**："只要在真正有性命之虞的时候抽身逃走就行"
- **问题**：“出手反击”被改成“抽身逃走”，行为反了，与前句“I could have fought back”也脱节。



## O115 | entry-03388

### C38 | entry-03388 | 存在问题

原文叙述者告诫自己仅在确认生命危险后“lash out”；译文改为有性命之虞时“抽身逃走”。克制反击与准备逃跑是不同的行动选择。证据：`L:452`。



## O116 | entry-03388

### C38 | entry-03388 | 存在问题
- **原文**："Their reasons are somewhat inaccurate, but make no mistake: you deserve the fate they have lined up for you."
- **译文**："他们的理由是——或许不准确，但是我没有说错——“他们所安排的命运是你们应得的”。"
- **问题**：原文是说话人（S）自己的判断：“他们的理由不太准确，但你们确实罪有应得”。译文把“你们罪有应得”加引号，当成了“他们的理由”的内容，归属和逻辑结构都错了。



## O117 | entry-03388

### C39 | entry-03388 | 存在问题

原文“only now did I use it”强调此前未使用、此刻才使用禁咒；译文“也只有在那时我使用了这个咒语”变成仅那一次使用。后文继续猎取居民生命精华，也使这一唯一时点限制与叙事不符。证据：`L:454`、`L:456`。



## O118 | entry-03388

### C39 | entry-03388 | 存在问题
- **原文**："Even if I wanted to, neither I nor anything else in the universe could stop their invasion"
- **译文**："我或者宇宙中任何事物都没法阻止他们的侵略，尽管我很想这么做。"
- **问题**：原文是假设“即便我想”（她实际并不想），译文变成“尽管我很想”，说话人立场反了。



## O119 | entry-03388

### C40 | entry-03388 | 存在问题

原文“Even if I wanted to”是假设自己想阻止入侵；译文“尽管我很想这么做”断言她确实想阻止。人物动机被改变，且与后文帮助世界灭亡的宣言冲突。证据：`L:458`、`L:460`。



## O120 | entry-03388

### C40 | entry-03388 | 存在问题
- **原文**："dripping acid into your eyes, then growing them back with more nerve endings than before"
- **译文**："再将它放回神经更加密集的地方去"
- **问题**：“重新长出神经末梢更多的眼睛”被误译成“放回神经密集处”，动作和结果都错了。



## O121 | entry-03388

### C41 | entry-03388 | 存在问题

原文眼睛被酸液毁坏后重新长出，并具有更多神经末梢；译文“再将它放回神经更加密集的地方”变成移动、放回眼球，改变折磨方式与疼痛增强原因。证据：`L:458`。



## O122 | entry-03388

### C41 | entry-03388 | 存在问题
- **原文**："Countless others have agreed to this deal in the millenia before you were even born"
- **译文**："在你们诞生千年之前"
- **问题**：“你们出生前的数千年间（持续）”被改成“你们出生前一千年（时点）”，时序和跨度错了。



## O123 | entry-03388

### C42 | entry-03388 | 存在问题

原文承诺“nearly-equal pleasure”；译文“等量的快乐”删除近似限定，把接近等量的许诺变成精确等量。证据：`L:458`。



## O124 | entry-03388

### C42 | entry-03388 | 存在问题
- **原文**："you will feel nearly-equal pleasure"
- **译文**："你们会感到等量的快乐"
- **问题**：删掉了限定词 nearly，“近乎等量”变成“等量”，承诺的程度被说满了。



## O125 | entry-03388

### C43 | entry-03388 | 仅建议
- **现象**："even the armies of Mal'Rok" 译作“哪怕乌鲁洛克的军队”，把世界名换成了神名。
- **说明**：两者在语境中指同一支军队，读者不会误解。“agonizing”译作“可悲”也略弱。



## O126 | entry-03388

### C44 | entry-03388 | 仅建议
- **现象**：“the Fearscape”译作“恐惧空间”；术语快照有 fearscape→恶魔空间（newLore category，existing），context.lua 第 212 行也用“恶魔空间”。
- **说明**：source_tag 与类别不同，existing 不构成强制要求，只记统一性建议。



## O127 | entry-03389

### C17 | entry-03389 | 存在问题
- **原文短引**：`With a form and weapons granted by our Father, and a mind given his direct, enthusiastic approval, Khulmanar is considered to be the avatar of Urh'Rok...`
- **译文短引**：`拥有我们的父所赐予的武器与躯壳，精神受到父的指引，库马纳被视作乌鲁洛克的化身...`
- **问题具体内容**：“and a mind given his direct, enthusiastic approval”（其战术智慧得到了父亲直接且热烈的赞同与认可）被误译为“精神受到父的指引”。前文反复强调库马纳是以全族最卓越的战术头脑赢得神明赞赏，神明并未接管或指引其意志，而是热情认可其智慧。
- **状态**：存在问题
- **证据与消费逻辑**：源码路径 [`demon.lua:471`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua#L471)。

---



## O128 | entry-03389

### C18 | entry-03389 | 存在问题
- **原文短引**：`...inspiration of Urh'Rok... Khulmanar... avatar of Urh'Rok... Divine Tournament of Tactics`
- **译文短引**：`...在乌尔洛克的命令和鼓动下... 库马纳被乌鲁洛克亲自召见... 神圣战术竞标赛...`
- **问题具体内容**：同条段落内核心主神译名分裂：首句写“乌尔洛克”，后文两处写“乌鲁洛克”；此外，“神圣战术锦标赛”出现严重形近错别字“神圣战术竞标赛”（Tournament 误写为商业竞标）。
- **状态**：存在问题
- **证据与消费逻辑**：文本内部前后冲突，见 [`demon.lua:471`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua#L471)。

---



## O129 | entry-03389

### C25 | entry-03389 | 存在问题

库马纳的才智获得乌鲁洛克「direct, enthusiastic approval」；「精神受到父的指引」把认可改成了精神指导。证据：L:471。



## O130 | entry-03389

### C43 | entry-03389 | 存在问题

原文“a mind given his direct, enthusiastic approval”说明库马纳的才智得到乌鲁洛克亲自、热情认可；译文“精神受到父的指引”改为精神受其引导，遗漏认可关系。证据：`L:471`。



## O131 | entry-03389

### C45 | entry-03389 | 存在问题
- **原文**："under the command and inspiration of Urh'Rok"
- **译文**："在乌尔洛克的命令和鼓动下"
- **问题**：同条后文和本批其他条目都写“乌鲁洛克”。本条所属雕像标题（demon.lua:470；context.lua:380）是“库马纳，乌鲁洛克将军”。同一专名在同一条内出现两种写法。



## O132 | entry-03389

### C46 | entry-03389 | 存在问题
- **原文**："the Divine Tournament of Tactics"
- **译文**："神圣战术竞标赛"
- **问题**：“竞标”是招投标的意思，属于错字，改变了赛事名称的含义。本条前文和 03378 都写作“锦标赛”。



## O133 | entry-03389

### C47 | entry-03389 | 存在问题
- **原文**："a mind given his direct, enthusiastic approval"
- **译文**："精神受到父的指引"
- **问题**：“心智获得父亲直接而热情的认可”被改成“受父指引”，关系性质从“认可”变成了“引导”。



## O134 | entry-03389

### C48 | entry-03389 | 仅建议
- **现象**：
  - "salvation from the dust mages" 译作“被从尘埃法师的控制之下解放”，“控制”为新增；
  - "physical endurance" 译作“物理耐受”，用词生硬；
  - "the little energy he's not using" 丢了 little。
- **说明**：均不改变主干信息。



## O135 | entry-03391

### C19 | entry-03391 | 存在问题
- **原文短引**：`Saying that the consequences of failure were too awful to risk inflicting on other test subjects, he entered the portal himself...`
- **译文短引**：`由于他说实施其他实验的失败后果太过危险，他独自一人进入了传送门...`
- **问题具体内容**：“risk inflicting on other test subjects”（冒着加诸于其他受试对象身上的风险）被误译为“实施其他实验”。里斯丰格之所以亲自冒险穿越不稳定的传送门，是因为不忍拿其他同胞或生物充当活体受试者（因此文末称颂其无私奉献）；译为“实施其他实验太过危险”彻底抹除了“受试者”关键信息并曲解了人物动机。
- **状态**：存在问题
- **证据与消费逻辑**：语境证据见 [`demon.lua:478`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua#L478)。

---



## O136 | entry-03391

### C26 | entry-03391 | 存在问题

里斯丰格找到的是一座「intact」的完好传送门；「未被人使用过」描述使用历史，原文没有这个事实。证据：L:478。



## O137 | entry-03391

### C27 | entry-03391 | 存在问题

他亲自测试，是因为失败后果太可怕，不愿让**其他受试者承受**；译文的「实施其他实验的失败后果太过危险」丢失受试者和亲自承担风险的原因。证据：L:478。



## O138 | entry-03391

### C44 | entry-03391 | 存在问题

原文里斯丰格找到“an intact”传送门；译文“一个未被人使用过的”把完好状态改为使用历史。证据：`L:478`。



## O139 | entry-03391

### C45 | entry-03391 | 存在问题

原文不愿把失败后果施加给“other test subjects”，因此亲自试验；译文“实施其他实验的失败后果太过危险”改成其他实验危险，遗漏保护其他受试者的伦理动机。证据：`L:478`，末句专门赞扬其无私奉献。



## O140 | entry-03391

### C49 | entry-03391 | 存在问题
- **原文**："he recovered an intact one"
- **译文**："他早已找到了一个未被人使用过的"
- **问题**：“完好无损”被改成“未被使用过”，属性错了。“早已”也是新增。



## O141 | entry-03391

### C50 | entry-03391 | 存在问题
- **原文**："Saying that the consequences of failure were too awful to risk inflicting on other test subjects, he entered the portal himself"
- **译文**："由于他说实施其他实验的失败后果太过危险"
- **问题**：原意是“不忍让其他受试者承担失败后果”，是他亲身冒险的无私动机。译文变成“其他实验的失败后果危险”，对象和动机都错了。



## O142 | entry-03392

### C20 | entry-03392 | 存在问题
- **原文短引**：`Rogroth generates countless essence-less seeds from within its frame, then embeds them in nearby living beings...`
- **译文短引**：`洛格罗斯在这个构造中留下了无数没有精华的种子，并将这些种子嵌入附近的生物中...`
- **问题具体内容**：“generates ... from within its frame”（从自身机体内源源不断产生）被误译为“在这个构造中留下了”。洛格罗斯（噬魂者）本身即是玛瑙族打造的机体（chassis），其功能是在体内生成种子并植入活物；译文将其篡改为在某个外部构造中留下种子，机体机制与主客体关系混乱。
- **状态**：存在问题
- **证据与消费逻辑**：源码路径 [`demon.lua:485`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua#L485) 与 [`demonic-pact.lua:276`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/demonic-pact.lua#L276)。

---



## O143 | entry-03392

### C21 | entry-03392 | 存在问题
- **原文短引**：`...the children of emerald have developed a prototype of this form of magic...`
- **译文短引**：`...绿翡翠之子研究出了这种魔法的原形...`
- **问题具体内容**：“prototype”出现错别字“原形”（应为“原型”）。原形指本来面目，原型指初始样品模型。
- **状态**：存在问题
- **证据与消费逻辑**：文本字面错误，见 [`demon.lua:485`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua#L485)。

---



## O144 | entry-03392

### C28 | entry-03392 | 存在问题

洛格罗斯从体内结构**不断生成**无生命精华的种子；「在这个构造中留下了无数……种子」变成预先存放。证据：L:485。



## O145 | entry-03392

### C46 | entry-03392 | 存在问题

原文洛格罗斯“generates countless … seeds from within its frame”，是在体内生产种子；译文“在这个构造中留下了无数……种子”变成放置、留存种子，遗漏生产能力。证据：`L:485`，后文继续讨论其生产能力尚未完善。



## O146 | entry-03392

### C47 | entry-03392 | 存在问题

原文就地形成入侵军队需要“some decisive early skirmishes”；译文“只需要早期的小规模战斗”遗漏战斗具有决定性这一限定，降低了设想成立的条件。证据：`L:485`。



## O147 | entry-03392

### C51 | entry-03392 | 存在问题
- **原文**："Rogroth generates countless essence-less seeds"
- **译文**："洛格罗斯在这个构造中……"
- **问题**：本条正是雕像“Rogroth, Eater of Souls”的铭文（demon.lua:484-485），标题译作“罗格洛斯·灵魂吞噬者”（context.lua:384）。正文写成“洛格罗斯”，同一弹窗里标题与正文名称不一致。



## O148 | entry-03392

### C52 | entry-03392 | 存在问题
- **原文**："developed a prototype of this form of magic"
- **译文**："研究出了这种魔法的原形"
- **问题**：“原形”是本来面目的意思，“原型”才是 prototype，错字改变了词义。



## O149 | entry-03393

### C29 | entry-03393 | 存在问题

枯萎化达莱奇通常必须立刻「put down」，即处死或消灭，以免造成损害；「压制」只表示暂时制服。证据：L:492。



## O150 | entry-03393

### C48 | entry-03393 | 存在问题

原文失控的枯萎达莱奇通常必须“immediately put down”，在此生物处置语境中指杀死；译文“立刻被压制”只表达控制、镇压，未保留处死措施。证据：`L:492`，前文说明其可能摧毁制造者，后文以可控样本为例外。



## O151 | entry-03393

### C53 | entry-03393 | 存在问题
- **原文**："usually a blighted daelach has to be immediately put down"
- **译文**："一个枯萎化的达莱奇必须立刻被压制"
- **问题**：删掉了 usually，“通常”变成“一律”；put down（处决、销毁）被译成“压制”，处置方式错了。



## O152 | entry-03393

### C54 | entry-03393 | 仅建议
- **现象**："almost entirely made of magic" 译作“纯粹魔法生物”；同一段内“它／他”指代混用（“他的火焰风暴”“他的实际效果”）。
- **说明**：主旨（高魔法构成导致不稳定）不变。



## O153 | entry-03394

### C22 | entry-03394 | 存在问题
- **原文短引**：`While we have not yet found a way to reverse-engineer these spells to protect our standard troops from disintegration...`
- **译文短引**：`我们还没有找到反制这些咒语的方法来保护我们的军队免于溃散。`
- **问题具体内容**：“reverse-engineer these spells”（逆向破解并仿制利用这些引导流星的法术）被误译为“反制这些咒语”；“disintegration”（穿越护盾时的肉体解体/碎灭）被误译为“溃散”（routed）。恶魔意在学习仿制该法术以护送部队肉体穿越护盾，译为“反制”导致动机颠倒。
- **状态**：存在问题
- **证据与消费逻辑**：源码路径 [`demon.lua:499`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua#L499)。

---



## O154 | entry-03394

### C23 | entry-03394 | 存在问题
- **原文短引**：`...the shield shattered him as expected, but we had designed him to survive this, the fragments merging back into their completed form once he reached the surface.  It would seem, though, that ... he has been unable to start the second stage of this process, wherein he merges these fragments back into a completed form.`
- **译文短引**：`...不过我们的设计让它能够得以生存。碎片在到达埃亚尔之后重新融合到一起，组成完整形态。然而，或许是因为... 哈卡祖无法进行第二阶段——将碎片重组的阶段。`
- **问题具体内容**：将前句分词短语所表达的设计预期目标（原本设想碎片落地后自行重新融合），误译为已发生的既成事实（“碎片在到达埃亚尔之后重新融合到一起，组成完整形态”），导致与后一句“哈卡祖无法进行第二阶段——将碎片重组的阶段”直接在中文行文内产生无可调和的前后自相矛盾。
- **状态**：存在问题
- **证据与消费逻辑**：源码路径 [`demon.lua:499`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua#L499)。

---



## O155 | entry-03394

### C30 | entry-03394 | 存在问题

尚未找到的是逆向解析召唤陨石的法术、借其保护部队的方法；「反制这些咒语」改成了对抗法术。证据：L:499。



## O156 | entry-03394

### C31 | entry-03394 | 存在问题

陨石会裂成大小**可预测**的碎块；「若干大块」改写碎块尺寸，并漏掉可预测性。证据：L:499。



## O157 | entry-03394

### C32 | entry-03394 | 存在问题

到达地表后重组是哈卡祖的**设计目标**，后文明确说它至今无法启动这一步；「碎片……重新融合到一起，组成完整形态」误称重组已经发生。证据：L:499。



## O158 | entry-03394

### C49 | entry-03394 | 存在问题

原文陨石被分成“predictably-sized chunks”；译文“若干大块”遗漏碎块大小可预测这一特征，并增加“大”的判断。证据：`L:499`。



## O159 | entry-03394

### C50 | entry-03394 | 存在问题

原文“reverse-engineer these spells”是研究并复现法术，以保护己方军队；译文“反制这些咒语”变成对抗、克制法术。证据：`L:499`，目的为利用通过护盾的方法，而非抵消这些法术。



## O160 | entry-03394

### C51 | entry-03394 | 存在问题

原文“too sturdy”指石质躯体过于坚固；译文“太过顽固”通常指性情执拗，改变无法重组的物理原因。证据：`L:499`，另一候选原因是护盾附加反魔法包层。



## O161 | entry-03394

### C52 | entry-03394 | 存在问题

原文将落地后碎片重组置于设计说明中，紧接着说明此阶段未能启动；译文独立断言“碎片在到达埃亚尔之后重新融合到一起，组成完整形态”，随后又说无法重组，形成实际已完成与尚未完成的矛盾。证据：`L:499`。



## O162 | entry-03394

### C55 | entry-03394 | 存在问题
- **原文**："we have not yet found a way to reverse-engineer these spells to protect our standard troops"
- **译文**："还没有找到反制这些咒语的方法"
- **问题**：目的是“逆向复制”这些法术，让己方部队穿过护盾，译成“反制”后目的反了。



## O163 | entry-03394

### C56 | entry-03394 | 存在问题
- **原文**："protect our standard troops from disintegration"
- **译文**："免于溃散"
- **问题**：disintegration 是物理解体（与本条“护盾将其撕碎”对应），“溃散”是军队崩溃的意思，语义错了。



## O164 | entry-03394

### C57 | entry-03394 | 仅建议
- **现象**："we made him to be too sturdy" 译作“制造的太过顽固”。
- **说明**：“顽固”偏指性格，这里“坚固”更贴切；读者仍可理解为“太结实”，按措辞偏好处理。



## O165 | entry-03395

### C53 | entry-03395 | 存在问题

原文大陆漂浮于“the void between worlds”；译文仅保留“虚空”，遗漏世界之间这一位置关系。证据：`quests/start-ashes.lua:23`。这是叙事位置遗漏，不是对地图实现的额外推断。



## O166 | entry-03395

### C54 | entry-03395 | 存在问题

原文“but not without destroying the crystal”把摧毁水晶作为逃离前必须完成的事；译文“同时别忘了”未保留明确先后要求。冻结邻近任务说明也写明离开前必须摧毁，否则仍会被追踪。证据：`quests/start-ashes.lua:27`、`:38`。此处确认的是任务指示信息遗漏，不断言游戏一定禁止提前离开。



## O167 | entry-03395

### C58 | entry-03395 | 仅建议
- **原文**："As you recover, and your platform of searing earth splits from the main continent, your old memories flood your mind"
- **译文**："当你醒来后，你发现你身处一个和主大陆分离的平台，而你旧时的记忆渐渐涌来"
- **说明**：丢了“灼热土地”，平台分离从正在发生的事件变成了既成状态，“flood”译作“渐渐”也不贴切。核心事实（平台已与大陆分离、记忆恢复）都在。
- **handler 的处理**：译作“主人”加引号，与邻近 context（context.lua 第 139、150 行）一致，不计缺陷。
- **证据**：start-ashes.lua:22-28。



## O168 | entry-03396

### C24 | entry-03396 | 仅建议
- **原文短引**：`While transformed you are invisible (power %d), convert 100%% of all damage done to darkness...`
- **译文短引**：`不祥黑影状态下你处于隐形（强度 %d）造成的所有伤害转化为暗影伤害...`
- **问题具体内容**：隐形强度数值括号后缺失逗号，行文读作“隐形（强度 %d）造成的所有伤害”，产生轻微语句粘连。但占位符与机制完整，仅属标点断句偏好建议。
- **状态**：仅建议
- **证据与消费逻辑**：源码路径 [`dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/black-magic.lua:146`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/black-magic.lua#L146)。

---



## O169 | entry-03396

### C55 | entry-03396 | 仅建议

译文“处于隐形（强度 %d）造成的所有伤害……”在两个分句之间缺乏明显停顿，阅读稍显拥挤。但隐形和伤害转换仍可辨认，两个 `%d` 的消费对应也正确，因此仅属可读性建议。

原文的“100%%”改为中文“所有”仍表达全部转换，不构成占位符丢失。证据：`black-magic.lua:146`至其 `tformat` 调用；`timed_effects.lua:1014`、`:1015`。



## O170 | entry-03396

### C56 | entry-03396 | 待确认

原文“equal to your highest”与译文“相当于你最高……”一致；但源码组合显示，并非严格相等：

- DLC `timed_effects.lua:1016`、`:1017`向两个 `auto_highest` 属性写入数值 `1`。
- 固定本体 `Combat.lua:2339`、`:2376`分别返回最高值加上该属性值。

因此，在这组源码组合下会额外增加一个百分点，而非只取最高值。这是沿袭英文的机制疑点，不是译文新增错误。待确认项是该未固定 commit 的 DLC 快照与目标版本的对应关系。



## O171 | entry-03396

### C59 | entry-03396 | 仅建议
- **现象**：“你处于隐形（强度 %d）造成的所有伤害转化为暗影伤害”，括号后缺逗号，可能读成“隐形造成的伤害”。
- **机制核验**：black-magic.lua:146-149 的 info 与 action（:130-137，按层数设定持续回合）一致；timed_effects.lua:1013-1017 为 100% 伤害转为暗影，auto_highest_inc_damage／auto_highest_resists_pen 施加于暗影。译文“相当于你最高伤害加成和抗性穿透”正确。删掉字面量 `100%%`、改写为“所有伤害”不影响参数消费。



## O172 | entry-03399

### C57 | entry-03399 | 存在问题

原文“in radius 4 around you”明确酸池以施法者为中心；译文“在半径 4 的范围内制造”遗漏中心位置。括号“包括自己”说明受伤对象，不能完整替代施放中心限制。

证据：`demon-seeds.lua:214`的 `addEffect` 使用 `self.x, self.y`，`:217`传入半径；`:225`给自己施加抗性与亲和效果。中心遗漏由原文直接确认；源码证据仅代表已核验的 DLC 快照。



## O173 | entry-03399

### C60 | entry-03399 | 存在问题
- **原文**："You spawn a pool of acid in radius 4 around you"
- **译文**："在半径 4 的范围内制造持续 %d 回合的酸池"
- **问题**：丢了“以你为中心（around you）”这一位置信息。该技能定义了 `range = 4` 和 `requires_target = true`（demon-seeds.lua:205-206），但 action 实际以 `self.x, self.y` 为中心生成地图效果（:213-216）。缺少位置信息时，“半径 4 的范围内”容易被读成射程 4 的指定点施放。
- **其余部分**：40% 抗性和亲和数值与 timed_effects.lua:559-571 一致。



## O174 | entry-03400

### C61 | entry-03400 | 仅建议
- **现象**：“选择%s次充能的用途”，这里的 charges 是可储存的充能数（demon-seeds.lua:247-257），用量词“次”不够贴切。
- **说明**：参数 `p.charges` 由 tformat %s 正确消费，信息无损。



## O175 | entry-03402

### C25 | entry-03402 | 存在问题
- **原文短引**：`While the effect last your Strength and Magic stats are increased by 10%% of your shield block value.`
- **译文短引**：`你利用盾牌来强化自身，力量和魔法增加 10%% 格挡值，持续 %d 回合。`
- **问题具体内容**：技能机制描述严重歧义与颠倒。源码逻辑是为玩家自身增加力量和魔力属性点，提升数值为盾牌格挡值的 10%（Strength/Magic += block * 0.1）。译文表述为“力量和魔法增加 10%% 格挡值”，宾语变成了格挡值，极易被玩家理解为“力量和魔力使格挡值增加 10%”或“增加 10% 的格挡值”，完全歪曲了属性收益机制。
- **状态**：存在问题
- **证据与消费逻辑**：源码路径 [`dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/demon-seeds.lua:704-710`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/demon-seeds.lua#L704-L710)：
  ```lua
  local block = self:combatShieldBlock()
  self:setEffect(self.EFF_DEMON_SEED_ARMOURED_LEVIATHAN, t.getDuration(self, t), {power=block*0.1})
  ```
  该状态在 timed_effects 中将 `power` 加成至施法者的 `str` 与 `mag` 属性，绝非增加盾牌格挡值。

---



## O176 | entry-03402

### C33 | entry-03402 | 存在问题

技能提升 Strength 与 **Magic 属性**，译文把后者写作「魔法」。冻结术语子集的 Magic 属性为「魔力」；快照实现也将增益写入 `Stats.STAT_MAG`，并非提高法术本身。证据：D:700–710 的技能说明与效果调用、E:630–643 的 `inc_stats` 消费逻辑。

**读取与边界。** 实际读取了冻结包的 [INPUT.md](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/INPUT.md)、[entries.json](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/entries.json)、[context.lua](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/context.lua)、[source-access.json](/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/source-access.json)，以及其中六个 `sections` 对应的 DLC 源文件：`data/lore/demon.lua`、`data/quests/start-ashes.lua`、`data/talents/corruptions/{black-magic,brutality,demon-seeds,demonic-pact}.lua`。这六个文件的 SHA-256 均与 `source-access.json` 相符。唯一额外读取的源码是哈希相符的 E；调用链来源为 `black-magic.lua` 的 `EFF_OMINOUS_SHADOW`，以及 `demon-seeds.lua` 的 `EFF_ACIDIC_BATH`、`EFF_DEMON_SEED_ARMOURED_LEVIATHAN`、`EFF_DEMON_SEED_PAIN_AFFINITY`。

DLC 快照的源码仓库与 commit 未固定，因此其机制证据只证明该快照内的行为，目标版本适用性未核验。没有读取其他报告、其他模型输出或越界材料；没有创建临时文件或修改仓库。本结果是审核观察，不宣称生产 `DONE_VERIFIED`。


## O177 | entry-03402

### C62 | entry-03402 | 存在问题
- **原文**："your Strength and Magic stats are increased by 10%% of your shield block value"
- **译文**："力量和魔法增加 10%% 格挡值"
- **问题**：源码提升的是属性 STAT_MAG／STAT_STR（timed_effects.lua:630-641 `inc_stats`；demon-seeds.lua:703 `power=block*0.1`）。术语快照中 Magic／mag 这一属性名都登记为“魔力”（T.GAME.STAT，existing，反映语料现状）。译成“魔法”后，指称的属性名与面板属性不一致。
- **状态说明**：状态是 existing，但这里原文明确写的是 stats，属性指称错误。
- **其他**：两行合并为一行、`%d` 移到句尾，都不影响参数消费。

---



## O178 | entry-03403

### C58 | entry-03403 | 待确认

原文“Demons … will instead be healed”与译文“恶魔不会被伤害，而会被治疗”均未说明例外。

DLC `demon-seeds.lua:810`使用 `DamageType.DEMONFIRE`；固定本体 `damage_types.lua:2600`要求目标具有 `demon` 属性且没有 `fiery_torment`，才在下一行治疗，否则转入火焰伤害分支。

可确认所读本体实现存在这一条件，但尚未核实该状态在目标 DLC 组合中的实际可达性，且 DLC 版本来源未固定。因此保留待确认，归因为沿袭英文的范围概括，而非中文独有错误。



## O179 | entry-03404

### C26 | entry-03404 | 仅建议
- **原文短引**：`...increasing all damage affinity by 15%%.`
- **译文短引**：`...在 2 回合内提升全体伤害亲和 15%%。`
- **问题具体内容**：“all damage affinity”（全属性伤害亲和 / 对所有伤害类型的伤害吸收百分比）被直译为“全体伤害亲和”。在中文语境下“全体”通常修饰生物目标群体，容易使人误以为是光环类全体队友增益，建议表述为全类型伤害亲和或所有伤害亲和。因其本质系直译生硬（translationese），机制数值消费无误，归为仅建议。
- **状态**：仅建议
- **证据与消费逻辑**：源码路径 [`demon-seeds.lua:843`](file:///home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g06-20260923/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/talents/corruptions/demon-seeds.lua#L843)，底层赋予的是 `EFF_DEMON_SEED_PAIN_AFFINITY` 个人 buff。

---



## O180 | entry-03404

### C59 | entry-03404 | 仅建议

“全体伤害亲和”不如明确指向全部伤害类型的表达自然，但句子主语仍是“你”，并未明确承诺全队或其他生物获得效果，不据此判为作用对象错误。

证据：`demon-seeds.lua:843`只向自身施加效果；`timed_effects.lua:999`增加自身 `damage_affinity.all`。此观察仅属措辞可读性建议，不据术语快照中的 existing 条目要求改名。



## O181 | entry-03407

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

