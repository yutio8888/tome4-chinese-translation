# 匿名源码核验与归并：40 条 / 101 项观察

你是本任务独立 REVIEWER。用户要求继续三模型实验并归并问题；本阶段依据源码核验，不参与参赛评分。参考是暂定模型裁决，非人工金标准。禁止寻找模型身份或读取来源映射、原始报告、STATE、其他实验目录。不得以多数票、重复次数、报告声称“已证实”替代证据。

唯一允许输入：本文件、同目录 INPUT.md、entries.json、context.lua、source-access.json、source-access.json 明确列出的冻结源码。先阅读INPUT统一判定规则；沿其限定调用链读取单文件。本体使用git show固定commit；DLC只能使用获准的哈希快照，不能把引擎commit套用于DLC，缺少目标版本适用证据则保留pending；无源码组件仅确认文本可证偏差。后续实验的临时文件已获用户授权，可用自己创建的任务专属临时目录；仓库只读，不创建子agent。

下方101项匿名观察按entry和文字排序，包括问题、建议及待确认。各观察C编号仅为原报告局部编号，不跨观察匹配；统一以O编号标识。保持原断言供核验但不采信。请逐项确认、否决、待确认或仅建议；同条同义缺陷合并为canonical D-ID，不同信息或机制错误拆开。注明翻译新增/沿袭上游。遇实质争议要核实双方论据和完整上下文，证据不足保留pending。缺陷边界应考虑完整界面语境，不把单词必然等同为排他机制断言；也不能因玩家猜得出或英文有同错就豁免。

同时独立检查全部40条，包括没有观察或全部观察被否决的条目，补充漏项。只依据INPUT/源码/语境，不能读取其他轮答案。

输出要求：三个Markdown表格，再补充必要解释与读取路径。
1. 恰好40行：entry-ID | 判定（OK/ISSUE/PENDING） | canonical D或P编号/简短依据。OK包括仅建议；有确认缺陷即ISSUE，即使附带pending；无确认但仍有疑点才PENDING。严格冻结顺序。
2. 确认缺陷表：D-ID（D01起） | entry-ID | 内容、归因及固定源码路径:行号/调用链证据。未决用P-ID另列，不混入D。每个D须实际核验。
3. 恰好101行：O-ID | 状态（confirmed/refuted/pending/advisory/mixed） | 命中D-ID（无则—） | 具体证据与理由。mixed须明确哪些部分confirmed、refuted、pending或advisory；不要把未命中的错误问题借用同条其他正确D。若仅有措辞问题则advisory。补充说明所有未决与主要分歧如何处理。

不要给模型排名或分数、不要修改译文，不宣称DONE_VERIFIED。列出实际读取的路径和额外单文件引入依据；未完成的机制核验如实记录。



## O001 | entry-03454

### C01 | entry-03454 | 仅建议
- 原文 "A demon with 3 arms … For experiment. Not for fun. Nope."，译文「长着三只手……不是娱乐，而是实验。」
- 句末调侃的 "Nope." 被略去，「三只手」在中文里有「扒手」的俗义。
- 事实（三条手臂、要切割你、目的是实验）都保留了，只是语气和措辞偏好，所以不计缺陷。
- 来源：searing-halls/npcs.lua:73，mutilator 的 desc。



## O002 | entry-03454

### C01 | entry-03454 | 存在问题

原文“**3 arms**”，译文“三只手”。`A/data/zones/searing-halls/npcs.lua:71–73` 将这句话用作恶魔的实体描述。*Arm* 指手臂，“三只手”只明确了手的数量，改变了描述的身体部位。状态：文本确认。



## O003 | entry-03454

### C01 | entry-03454 | 存在问题

原文：“3 arms”；译文：“三只手”。

这里直接描述恶魔的身体构造，原文计数对象是手臂，译文变成手，改变了明确的解剖部位。状态：**confirmed，文本事实错误**。证据：`A/data/zones/searing-halls/npcs.lua:73`，`mutilator.desc`。



## O004 | entry-03454

### C01 | entry-03454 | 存在问题
- **原文短引**：`For experiment. Not for fun. Nope.`
- **译文短引**：`不是娱乐，而是实验。`
- **问题具体内容**：句末独立的断言短句 `Nope.`（“才怪 / 绝非如此 / 绝无玩笑”）在译文中被完全漏译。原文通过短促的四个句子片段构成了鲜明的黑色幽默语气，漏译导致原作者特有的调侃与确认语气丢失。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/zones/searing-halls/npcs.lua:73`（DLC公开快照，源码commit未固定），作为 `mutilator`（恶魔切割者）的 NPC 实体描述（`desc`）显示给玩家查看。



## O005 | entry-03454

### C02 | entry-03454 | 仅建议
- **原文短引**：`A demon with 3 arms`
- **译文短引**：`一个长着三只手的恶魔`
- **建议内容**：`3 arms` 译为“三只手”，在中文俗语中容易引起“扒手/窃贼”的不必要联想。建议使用“三条手臂”以更清晰准确地表现其变异解剖结构。此项仅属用词偏好，不影响事实理解。
- **状态**：仅建议



## O006 | entry-03454

### C02 | entry-03454 | 存在问题

原文“**mutilate you**”，译文“切割你”。同一实体描述中的 *mutilate* 表示严重伤残、毁损身体；“切割”仅表示切开动作，丢失伤残程度。证据同 `A/data/zones/searing-halls/npcs.lua:73`。状态：文本确认。



## O007 | entry-03454

### C02 | entry-03454 | 存在问题

原文：“ready to mutilate you”；译文：“准备切割你”。

原文表达使人残缺、残毁的行为结果；译文仅说明切割这一动作，同时将方式限定为切割，未保留残毁含义。状态：**confirmed，语义损失**。证据：同文件第 72、73 行，生物名称与实验性残害描述共同限定语境。



## O008 | entry-03455

### C02 | entry-03455 | 存在问题（术语）
- "Many in Maj'Eyal" 译成「在马基埃亚尔」。
- 术语快照中 Maj'Eyal 为 preferred「马基·埃亚尔」，notes 写明维护者已于 2026-08-25 裁定，「马基埃亚尔」已被取代。
- 这是专名，不受 source_tag 差异影响，属于明确适用的术语要求。
- 来源：init.lua:28。



## O009 | entry-03455

### C03 | entry-03455 | 存在问题

原文两处均为“**Fearscape**”；译文在开头写“恐惧空间”，介绍新地区时写“恶魔空间”。同一段 DLC 介绍把同一地点呈现为两个名称，削弱了指代关系。见 `A/init.lua:28、33` 及冻结译文；术语子集也记录了“恶魔空间”，但此项依据是**本条内部不一致**，并非仅凭 `existing` 状态强制改名。状态：文本确认。



## O010 | entry-03455

### C03 | entry-03455 | 存在问题

原文：“fighting against overwhelming odds”；译文：“与势不可挡的敌人战斗”。

原文描述己方处于压倒性劣势的战斗局面；译文转为敌人本身势不可挡的属性。前后文反复强调敌群和成群对手，不能将这种局面信息完全等同于敌人强大。状态：**confirmed，关系与语义偏移**。证据：`A/init.lua:31`。



## O011 | entry-03455

### C03 | entry-03455 | 存在问题
- **原文短引**：`Many in Maj'Eyal have heard of "demons"`
- **译文短引**：`在马基埃亚尔，很多人都曾听闻“恶魔”的大名`
- **问题具体内容**：译文使用了旧称 `马基埃亚尔`。根据术语快照明确规定，`Maj'Eyal` 的统一规范译名为 `马基·埃亚尔`（`T.PN.WORLD`，places，preferred，规则注记：“维护者于 2026-08-25 裁定采用‘马基·埃亚尔’；‘马基埃亚尔’已被取代”）。译文直接违反了明确适用的首选术语要求。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/init.lua:28`（DLC公开快照，源码commit未固定），作为 DLC 的描述（`description`）展示在游戏模组与 DLC 选择列表中。



## O012 | entry-03455

### C03 | entry-03455 | 存在问题（同一专名两译）
- 第一段 "Their Fearscape" 译成「恐惧空间」；Features 第 3 项 "the plains of the Fearscape" 译成「恶魔空间的平原」。
- 同一个专名在同一条目里用了两个名字，读者会以为是两个不同地点，所指的同一性丢失。
- 至于应该统一成哪个名字，属于术语策略：快照中 fearscape＝恶魔空间 只是 existing，context.lua:12 另有「恐惧空间」。这里不就此下结论，只判定条目内部不一致。
- 来源：init.lua:28、33。



## O013 | entry-03455

### C04 | entry-03455 | 存在问题

原文“barrier … crack **under their scrutiny**”，译文“在他们的**破坏**下开始破碎”。原文说屏障在恶魔的审视、探究下出现裂缝；译文改成了明确的主动破坏行为。见 `A/init.lua:28`。状态：文本确认。



## O014 | entry-03455

### C04 | entry-03455 | 存在问题

原文：“feeding on the flames and suffering … to stay alive”；译文：“吸收周围的火焰和痛苦，将任何敌人迅速化为灰烬”。

译文保留吸收和杀敌，却遗漏吸收这些力量用于维持自身生存的目的。状态：**confirmed，文本信息遗漏**。

证据：`A/init.lua:31`。快照中的补充机制证据为 `A/data/timed_effects.lua:179` 的 `CURSED_FLAMES.on_timeout`：调用 `eff.src:heal(eff.heal)`，随后恢复活力；该快照确有向来源提供治疗的消费逻辑，但其目标版本适用性未固定。



## O015 | entry-03455

### C04 | entry-03455 | 存在问题
- **原文短引**：`call forth a squad of Fire Imps to pelt your enemies to death`
- **译文短引**：`召唤火焰恶魔将敌人烧成灰烬`
- **问题具体内容**：
  1. 生物/召唤物类型误译：`Fire Imps` 是游戏内明确的怪物与恶魔使者召唤仆从“火焰小鬼”（Imp 在 ToME4 中恒为“小鬼”，如水小鬼、火小鬼，不同于大恶魔 Demon）。译为“火焰恶魔”混淆了恶魔阶级与召唤物实际实体类别。
  2. 战术动作曲解：`pelt your enemies to death while they exhaust themselves on your impenetrable defenses`（在敌人耗尽体力于你坚不可摧的防御前，召唤小鬼小队不断投掷火弹将他们砸死/风筝击毙）被随意偏离转写为“将敌人烧成灰烬”，丢失了防御反击配合持续骚扰的战术描述特征。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/init.lua:32`（DLC公开快照，源码commit未固定），恶魔使者职业特性说明。



## O016 | entry-03455

### C04 | entry-03455 | 存在问题（语义改写）
- "crack under their scrutiny" 译成「在他们的破坏下开始破碎」。
- scrutiny 是「审视、窥探」，被改写成主动「破坏」，原文措辞的信息改变了。
- 来源：init.lua:28。



## O017 | entry-03455

### C05 | entry-03455 | 存在问题

原文“survive the **ensuing stresses**”，译文“在恶魔的**拷问**中存活”。前者泛指随后承受的压力或折磨，后者限定为恶魔施加拷问；原文这一处没有给出该限定。见 `A/init.lua:28`。状态：文本确认。



## O018 | entry-03455

### C05 | entry-03455 | 存在问题

原文：“a squad of Fire Imps”；译文：“召唤火焰恶魔”。

原文明确是一队特定种类的小恶魔；译文泛化为火焰恶魔，遗漏小队规模及具体生物类别。状态：**confirmed，数量与对象信息遗漏**，不依赖强制专名译法。证据：`A/init.lua:32`；`A+/data/talents/corruptions/demonic-pact.lua:27`、第 314 行另可确认快照中存在独立的 `fire imp` 种子类型。



## O019 | entry-03455

### C05 | entry-03455 | 存在问题
- **原文短引**：`Their Fearscape floats far above the skies` vs `plains of the Fearscape`
- **译文短引**：`他们的恐惧空间高浮于天幕之上` vs `恶魔空间的平原`
- **问题具体内容**：同一文本内对专有位面名称 `Fearscape` 的翻译自相矛盾。第 1 段译为 `恐惧空间`，特性第 3 点却译为 `恶魔空间`。依据术语快照，`fearscape` 的统一译名为 `恶魔空间`（`T.NARRATIVE.LORE`，narrative，existing dlc）。同一文本内部译名不一致破坏了专名统一性。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/init.lua:28, 33`（DLC公开快照，源码commit未固定），DLC 背景叙事与新区域介绍。



## O020 | entry-03455

### C05 | entry-03455 | 存在问题（遗漏）
- Doombringer 一项的 "feeding on the flames and suffering of their surroundings **to stay alive** while quickly reducing **any group** …" 译成「随后吸收周围的火焰和痛苦，将任何敌人迅速化为灰烬」。
- 吸收火焰与痛苦是「为了维持生存」，这一目的被删，玩法定位信息丢失；"any group" 也缩成了「任何敌人」。
- 属于文本层面可直接证明的遗漏，没有追具体技能机制。
- 来源：init.lua:31。



## O021 | entry-03455

### C06 | entry-03455 | 存在问题

原文“fighting against **overwhelming odds**”，译文“与**势不可挡的敌人**战斗”。原文强调寡不敌众或胜算悬殊；译文把悬殊局势说成敌人本身不可阻挡。见 `A/init.lua:31`。状态：文本确认。



## O022 | entry-03455

### C06 | entry-03455 | 存在问题
- **原文短引**：`As the barrier between our worlds begins to crack under their scrutiny`
- **译文短引**：`隔绝两端世界的屏障，在他们的破坏下开始破碎`
- **问题具体内容**：原文 `under their scrutiny` 意为在恶魔持续的严密窥探/审视之下，裂隙悄然产生。译文误译为 `在他们的破坏下`，曲解了原句中恶魔尚未全面突破、仅凭窥视与法术试探便引起裂痕的悬疑紧张氛围。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/init.lua:28`（DLC公开快照，源码commit未固定），世界背景说明。



## O023 | entry-03455

### C06 | entry-03455 | 存在问题（机制表述偏差）
- "Demons have persistent health, making them a little more precious than disposable … skeletons or summoner beasts" 译成「恶魔具有更持久的生命值，比死灵法师易碎的骷髅……更加珍贵」。
- persistent health 是「生命值会保留、不会重置」，被改成了比较级「更持久」，读起来像是恶魔血更厚或更耐打。
- disposable（用完即弃）译成「易碎」，原句「可保留 vs 一次性」的对比逻辑随之丢失。
- 文本层面可证。恶魔血量保留的实际实现不在本次允许读取的调用链上，具体机制未核验。
- 来源：init.lua:32。



## O024 | entry-03455

### C06 | entry-03455 | 待确认

原文：“Demons have persistent health”；译文：“恶魔具有更持久的生命值”。

疑点是将跨次召唤保留生命状态，表述为生命值更加持久、更加耐用。

快照证据：`A+/data/talents/corruptions/demonic-pact.lua:326` 的 `availableDemonSeed` 返回种子中已有的恶魔对象及当前生命值；`Bind Demon.action` 在第 788–815 行取该对象并传给 `setupDemonSummon`。后者位于 `A+/data/talents/corruptions/corruptions.lua:93`，没有将生命值重置为满值。复活分支另在 `demonic-pact.lua:935` 将生命设为最大生命的 15%。

状态：**pending**。快照内支持“生命状态保留”的解释；仍缺该 DLC 快照与目标版本的绑定证据，不能将此机制判断提升为目标版本已确认缺陷。



## O025 | entry-03455

### C07 | entry-03455 | 存在问题

原文“**demon-cursed minotaur**”，译文“恶魔牛头人”。译文未传达牛头人**受到恶魔诅咒**的关系，读者会将其理解为恶魔种类。见 `A/init.lua:32`。状态：文本确认。



## O026 | entry-03455

### C07 | entry-03455 | 存在问题

原文：“disposable necromancer skeletons”；译文：“死灵法师易碎的骷髅”。

`disposable` 说明可消耗、用后可替换的性质；“易碎”说明承伤脆弱。译文把资源管理上的比较改成了耐久性比较。状态：**confirmed，比较依据改变**。证据：`A/init.lua:32`，该句紧接恶魔生命状态与复活说明。



## O027 | entry-03455

### C07 | entry-03455 | 存在问题（删限定）
- "Shalore who've taken to the demonic alterations **especially well**" 译成「那些被恶魔的力量所改变的永恒精灵」。
- 删掉「适应得尤为好」后，范围从「改造中表现特别好的一部分永恒精灵」扩大成了「所有被改变的永恒精灵」。
- 来源：init.lua:35。



## O028 | entry-03455

### C08 | entry-03455 | 存在问题

原文“a **squad of Fire Imps**”，译文“火焰恶魔”。*Imp* 的具体种类和 *squad* 的成队数量均消失，只剩宽泛的恶魔称呼。见 `A/init.lua:32`；已读的 `A/overload/mod/class/DemonologistsDLC.lua:105–109` 也明确使用 `fire imp` 名称。状态：文本及快照内名称确认。



## O029 | entry-03455

### C08 | entry-03455 | 存在问题

原文：“Shalore who've taken to the demonic alterations especially well”；译文：“那些被恶魔的力量所改变的永恒精灵”。

译文仅保留受到改造，遗漏这些精灵尤其适应恶魔改造的限定条件，扩大了这段种族说明所指人群。状态：**confirmed，限定信息遗漏**。证据：`A/init.lua:35`。



## O030 | entry-03455

### C08 | entry-03455 | 存在问题（语义）
- "assault your enemies' minds to leave them unsteady in combat" 译成「攻击敌人的精神，使他们难以为继」。
- unsteady 是「站不稳、失衡」，「难以为继」是「无法持续下去」，效果描述的含义改变了。
- 来源：init.lua:35。



## O031 | entry-03455

### C09 | entry-03455 | 存在问题

原文：“their metaphorical skulls”；译文：“他们的头骨”。

原文明示头骨是比喻性的战绩展示，译文删除这一性质，成为将敌人头骨悬挂到个人页面的直接陈述。状态：**confirmed，语义限定遗漏**。证据：`A/init.lua:40`，该项明确介绍成就和个人资料页。



## O032 | entry-03455

### C09 | entry-03455 | 存在问题

同句原文“**pelt your enemies to death**”，译文“将敌人**烧成灰烬**”。原文描述连续投射攻击，译文改成燃尽的结果，改变了攻击方式的呈现。见 `A/init.lua:32`。状态：文本确认；不据此推断实际伤害类型。



## O033 | entry-03455

### C09 | entry-03455 | 存在问题（所属关系颠倒）
- "Conquer the worst **Urh'Rok's forces** can throw at you" 译成「战胜乌鲁洛克最强大的敌人」。
- 原意是乌鲁洛克的部队派来对付你的最强者；中文「乌鲁洛克最强大的敌人」会读成「与乌鲁洛克为敌的人」，所属关系反了。
- 另外 "metaphorical skulls" 的 metaphorical 被删，译文成了字面上「悬挂头骨」。
- 来源：init.lua:40。



## O034 | entry-03455

### C10 | entry-03455 | 仅建议

原文：“all-new art”；译文：“全新的艺术”。

游戏地区介绍中，这一表达具有明显直译感。不过上下文仍能将它理解为地区的视觉艺术内容，没有足够证据认定具体功能或事实被改变。状态：**advisory，仅自然度意见**。证据：`A/init.lua:33`。



## O035 | entry-03455

### C10 | entry-03455 | 仅建议
- "a squad of Fire Imps" 译成泛称「火焰恶魔」，也没译出 "a squad"。快照里没有 Fire Imp 的术语，无法认定为术语违例。
- "always wanted" 译成「会想要」，时态有偏移，但不影响信息。
- 牛头人先用「它」后用「他」，代词不一致。
- 以上都属措辞或一致性偏好。



## O036 | entry-03455

### C10 | entry-03455 | 待确认

原文“Demons have **persistent health**”，译文“恶魔具有**更持久的生命值**”。译文易被读成恶魔生命值更多或更耐打；原文更像指生命状态能够持续保留。已读 `A/data/talents/corruptions/corruptions.lua:93–106` 的 `setupDemonSummon` 会复用恶魔对象并清除 `dead`，但所读调用链尚不足以确认完整的生命值保存、死亡和再召唤规则；DLC 目标版本也未固定。状态：待确认，缺召唤对象存取与再次召唤时生命值处理的完整调用证据。



## O037 | entry-03455

### C11 | entry-03455 | 存在问题

原文“**metaphorical skulls** from your profile page”，译文“将他们的**头骨悬挂**在个人页面上”。原文特意说明“头骨”是比喻；译文呈现为字面展示物，改变了成就陈列的含义。见 `A/init.lua:40`。状态：文本确认。



## O038 | entry-03456

### C11 | entry-03456 | 存在问题

原文：“As you recover … splits … memories flood your mind”；译文：“当你醒来后……和主大陆分离的焦土……记忆渐渐涌来”。

原文将恢复、地块分裂和记忆猛然涌回写成同时发生的转折；译文变成醒来后发现分离已经完成，记忆再逐渐恢复。改变了事件时序和记忆恢复的速度。状态：**confirmed，叙事时序偏移**。证据：`A/overload/data/texts/intro-ashes-urhrok.lua:27`。这是冻结叙述本身可证的差异，不据此推断实际地图生成时序。



## O039 | entry-03456

### C11 | entry-03456 | 存在问题（时序与状态改写）
- "As you recover, and your platform of searing earth splits from the main continent" 译成「当你醒来后，你发现你身处一处和主大陆分离的焦土」。
- 原文是「你恢复过来时，脚下平台正在从大陆分裂出去」，是正在发生的事件；译文改成了「醒来后发现已经分离」的既成状态。
- recover 译成「醒来」，还额外引入了原文没有的昏迷。
- 来源：intro-ashes-urhrok.lua:28。



## O040 | entry-03456

### C12 | entry-03456 | 存在问题

原文“your **handler**”，译文“你的‘**主人**’”。这里的人负责带领、看管玩家；“主人”增添了所有权关系。见 `A/overload/data/texts/intro-ashes-urhrok.lua:25`。状态：文本确认。



## O041 | entry-03456

### C12 | entry-03456 | 存在问题（遗漏）
- "floating in the void **between worlds**" 译成「漂浮在虚空中的燃烧大陆」。
- 「世界之间」这个方位信息被删。
- 来源：intro-ashes-urhrok.lua:23。



## O042 | entry-03456

### C13 | entry-03456 | 仅建议
- "cause the most pain" 译成「更大的痛苦」，最高级变成了比较级。
- handler 加引号译作「主人」属于合法的风格处理。



## O043 | entry-03456

### C13 | entry-03456 | 存在问题

原文说陨石“**lands near you**”，并使看管者当场死亡；译文说“它落在你身边，**砸死**了你的‘主人’”。“砸死”指定直接撞击致死，而原文仅给出附近着陆、冲击波及死亡，没有指定直接砸中。见 `A/overload/data/texts/intro-ashes-urhrok.lua:25`。状态：文本确认。



## O044 | entry-03457

### C14 | entry-03457 | 待确认
- "Corruptor (Demonologist)" 译成「堕落系（恶魔使者）」，而术语快照中 Corruptor＝腐化者（birth descriptor name，existing）。
- existing 不是强制要求。待确认的是：游戏里建角界面实际显示的职业大类名是否为「腐化者」。如果是，这个解锁标题就和界面名不一致。
- 缺少的证据：该职业描述符的实际显示译名。这属于当前翻译文件，按规则不能读取。
- 来源：unlock-corrupter_demonologist.lua:20。



## O045 | entry-03458

### C07 | entry-03458 | 存在问题
- **原文短引**：`they have created many dark cults to spread fear and terror.`
- **译文短引**：`并通过黑暗仪式来传播不安与恐慌。`
- **问题具体内容**：原文 `created many dark cults`（建立了许多黑暗教派 / 创立了多个邪教组织）被严重曲解为 `通过黑暗仪式`。译文将核心实体名词 `cults`（教派/邪教）错译为“仪式”（rituals），且将谓语动作 `created`（建立/创立）丢失篡改为状语“通过”，丢失了恶魔在埃亚尔大陆扶植黑暗教派势力的核心叙事背景。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/overload/data/texts/unlock-corrupter_demonologist.lua:22`（DLC公开快照，源码commit未固定），恶魔使者职业解锁说明正文。



## O046 | entry-03458

### C08 | entry-03458 | 存在问题
- **原文短引**：`- Summon and control demons to do your binding.`
- **译文短引**：`- 召唤并控制恶魔`
- **问题具体内容**：原文职业特性第 3 项句末的目的状语 `to do your binding`（履行你的契约 / 听从你的役使差遣）在译文中被直接截断漏译。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/overload/data/texts/unlock-corrupter_demonologist.lua:29`（DLC公开快照，源码commit未固定），职业特性条目列表。



## O047 | entry-03458

### C09 | entry-03458 | 存在问题
- **原文短引**：`Corruptors are spellcasters, ranged attackers using magic.`
- **译文短引**：`堕落系是施法职业，能使用魔法攻击敌人。`
- **问题具体内容**：原文 `ranged attackers using magic`（使用魔法的远程攻击者）中，明确战斗距离特性的定位词 `ranged`（远程）在译文中被漏译，仅泛化为“能使用魔法攻击敌人”。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/overload/data/texts/unlock-corrupter_demonologist.lua:26`（DLC公开快照，源码commit未固定），职业定位概括。



## O048 | entry-03458

### C12 | entry-03458 | 存在问题

原文：“created many dark cults”；译文：“通过黑暗仪式”。

原文讲建立多个黑暗教团，译文讲举行仪式；组织被换成活动，“建立多个组织”的事实也随之消失。状态：**confirmed，对象与行为错误**。证据：`A/overload/data/texts/unlock-corrupter_demonologist.lua:22`。



## O049 | entry-03458

### C13 | entry-03458 | 待确认

原文：“It does not regenerate, and can only be stolen from your foes”；译文：“不会自己回复，而必须从你的目标身上偷取”。

这项疑点主要**沿袭上游的绝对化说明**，不能归因于翻译新增。

固定本体 `game/modules/tome/class/Actor.lua:254` 将默认 `vim_regen` 设为 0，但第 602 行仍调用资源恢复；`game/modules/tome/data/resources.lua:147` 将活力绑定到 `vim_regen`。`ActorResource.lua:201` 的 `regenResources` 按恢复字段增加资源。DLC 快照的 `A+/data/talents/corruptions/demonic-pact.lua:214`、第 231 行则向特定戒指种子效果提供正的 `vim_regen`。

状态：**pending**。默认不恢复与任何情况下都不能恢复并不相同；快照存在例外，但目标 DLC 版本绑定缺失，故保留机制适用性待确认。



## O050 | entry-03458

### C14 | entry-03458 | 存在问题

原文“created many **dark cults**”，译文“通过**黑暗仪式**”。组织被换成仪式，且原文的“建立多个”信息消失。见 `A/overload/data/texts/unlock-corrupter_demonologist.lua:22`。状态：文本确认。



## O051 | entry-03458

### C15 | entry-03458 | 存在问题

原文“use ‘vim’ to power their **special abilities**”，译文“使用活力值来施放他们的**法术**”。“特殊能力”涵盖范围比“法术”宽；译文无依据地限定能力类型。见 `A/overload/data/texts/unlock-corrupter_demonologist.lua:34`。状态：文本确认。



## O052 | entry-03458

### C15 | entry-03458 | 存在问题（误译）
- "they have **created many dark cults** to spread fear and terror" 译成「并通过黑暗仪式来传播不安与恐慌」。
- cults（邪教组织）被译成「仪式」，「创建了许多」这层信息也丢了。
- 来源：unlock-corrupter_demonologist.lua:22。



## O053 | entry-03458

### C16 | entry-03458 | 存在问题

原文活力“can only be stolen from your **foes**”，译文“必须从你的**目标**身上偷取”。“目标”不限定敌对关系，放宽了来源范围。见 `A/overload/data/texts/unlock-corrupter_demonologist.lua:35`。状态：文本确认；不据此断言所有活力获取机制。



## O054 | entry-03458

### C16 | entry-03458 | 存在问题（遗漏）
- "Corruptors are spellcasters, **ranged** attackers using magic." 译成「堕落系是施法职业，能使用魔法攻击敌人。」
- 「远程」这个定位属性被删。
- 来源：unlock-corrupter_demonologist.lua:27。



## O055 | entry-03458

### C17 | entry-03458 | 待确认
- 与 C14 相同：Corruptor 译成「堕落系」，与术语「腐化者」不同，同样缺实际 UI 显示名的证据。



## O056 | entry-03458

### C18 | entry-03458 | 仅建议
- 同一条内先用「堕落系」、后用「堕落者」。
- "Infect" 译成「注射」，「恶魔之种」和「恶魔种子」两种说法混用。
- "to do your binding"（上游原文就把 bidding 打成了 binding）没有译出，但「控制」已表达从属关系。
- 前三行由单换行改成了空行分段，属于合法排版，不影响显示结构。



## O057 | entry-03460

### C10 | entry-03460 | 存在问题
- **原文短引**：`- Instant cast phase door`
- **译文短引**：`- 使用加速技能，瞬间穿梭空间`
- **问题具体内容**：
  1. 机制理解严重错误：`Instant cast` 在 ToME4 引擎中专指不占用行动回合的瞬发特性（即 `no_energy = true`），译文将其曲解为“使用加速技能”，生造出了一个不存在的加速增益动作。
  2. 核心技能名称被改写丢失：`phase door`（相位之门）是游戏中标准的短距离传送技能（术语快照：`Phase Door` -> `相位之门`，`T.GAME.TALENT`）。魔化精灵的首个种族天赋 `Haste of the Doomed` 实际机制正是一个具有瞬发特性的定向短距离相位之门（DLC快照 `data/talents/misc/races.lua:42-43`：`is_teleport = true, no_energy = true`）。译文将“瞬发相位之门”错误翻译为“使用加速技能，瞬间穿梭空间”，造成严重机制误导。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/overload/data/texts/unlock-race_doomelf.lua:28`（DLC公开快照，源码commit未固定；关联 `data/talents/misc/races.lua:36-44`）。



## O058 | entry-03460

### C11 | entry-03460 | 存在问题
- **原文短引**：`thus have earned the right to make #LIGHT_GREEN#Doomelf#WHITE# characters.`
- **译文短引**：`#LIGHT_GREEN#魔化精灵#WHITE# 应运而生。`
- **问题具体内容**：原文直接陈述玩家达成的机制解锁结果——“从而获得了创建魔化精灵角色的资格”。译文将其过度文学化修饰为“魔化精灵应运而生”，丢弃了通知玩家获得新建角色资格的核心机制信息。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/overload/data/texts/unlock-race_doomelf.lua:24`（DLC公开快照，源码commit未固定），种族解锁成就与建卡资格提示。



## O059 | entry-03460

### C14 | entry-03460 | 存在问题

原文：“earned the right to make … characters”；译文：“魔化精灵应运而生”。

原文明示玩家取得创建该种族角色的权限；译文变成种族由此产生的叙述，遗漏了这段解锁通知最直接的玩家操作信息。状态：**confirmed，解锁结果遗漏**。证据：`A/overload/data/texts/unlock-race_doomelf.lua:20`、第 24 行，标题和正文共同构成种族解锁通知。



## O060 | entry-03460

### C15 | entry-03460 | 待确认

原文：“Instant cast phase door”；译文：“使用加速技能，瞬间穿梭空间”。

疑点在于“加速技能”可能被理解为提高行动或移动速度，而原文强调瞬发位移。

`A+/data/talents/misc/races.lua:35` 的 `Haste of the Doomed` 设置 `no_energy=true`；`action` 在第 68 行执行 `teleportRandom`，第 73 行附加防御和抗性效果，同回合第二次使用在第 82 行扣除行动能量。这个快照中的对应技能并未提供速度增益。

状态：**pending**。快照内支持上述机制区分；仍缺 DLC 目标版本绑定，不能只凭名称 `Haste` 或此快照断言目标版本的技能分类。



## O061 | entry-03460

### C17 | entry-03460 | 存在问题

原文仅说在 Fearscape 的“**rigorous training**”磨砺了能力；译文增添“恶魔空间的**烈火**和严格训练”。烈火作为磨砺原因并未出现在该句。见 `A/overload/data/texts/unlock-race_doomelf.lua:22`。状态：文本确认。



## O062 | entry-03460

### C18 | entry-03460 | 存在问题

原文“have **earned the right to make** Doomelf characters”，译文“魔化精灵**应运而生**”。玩家获得创建该种族角色的权限，被改成种族由此出现，改变了叙述对象和解锁结果。见 `A/overload/data/texts/unlock-race_doomelf.lua:24`。状态：文本确认。



## O063 | entry-03460

### C19 | entry-03460 | 存在问题（解锁信息丢失）
- "and thus **have earned the right to make Doomelf characters**" 译成「……#LIGHT_GREEN#魔化精灵#WHITE# 应运而生」。
- 原文告诉玩家的关键信息是「你现在可以创建魔化精灵角色」，译文改成了叙事性的「应运而生」，玩家读不出自己解锁了可选种族。
- 来源：unlock-race_doomelf.lua:24。



## O064 | entry-03460

### C20 | entry-03460 | 存在问题（技能信息失真）
- "Instant cast phase door" 译成「使用加速技能，瞬间穿梭空间」。
- instant cast 指施放不耗时，译文读起来更像传送过程本身是瞬间的。
- phase door（术语快照：相位之门，短距离随机传送）的名称没有出现。
- 「加速技能」是原文没有的内容。它是否在暗指某个种族技能名，属于待确认子项：技能定义不在本文件的调用链上，没有读取。
- 来源：unlock-race_doomelf.lua:27。



## O065 | entry-03460

### C21 | entry-03460 | 存在问题（增译）
- "honed by their rigorous training on the Fearscape" 译成「恶魔空间的烈火和严格训练磨砺了……」。
- 增加了「烈火」这个原文没有的成因。
- 来源：unlock-race_doomelf.lua:22。



## O066 | entry-03460

### C22 | entry-03460 | 待确认
- "could have told the demons the truth" 译成「恶魔们将无法了解到**有关埃亚尔大陆的**真相」。
- 译文限定了真相的内容，原文没有写明。
- 缺少的证据：相关背景文本。它不在本条源文件的调用链上。



## O067 | entry-03460

### C23 | entry-03460 | 待确认
- "Can **increase** detrimental effects and **reduce** beneficial ones on their foes" 译成「延长……缩短……」。
- 译文把「增强/削弱」具体化成了持续时间。
- 缺少的证据：魔化精灵种族技能的实现。birth/doomelf.lua 虽在补充快照中，但本文本文件没有引用任何符号引入它，按规则没有读取。



## O068 | entry-03464

### C12 | entry-03464 | 存在问题
- **原文短引**：`#LIGHT_BLUE# * +3 Magic, +0 Willpower, +0 Cunning`
- **译文短引**：`#LIGHT_BLUE# * +3 魔法，+0 意志，+0 灵巧`
- **问题具体内容**：在人物创建界面属性修正列表（`_t"#GOLD#Stat modifiers:"`）中，基础核心属性 `Magic` 必须依照六大战斗属性标准术语统一译为 `魔力`（术语快照：`Magic` -> `魔力`，`T.GAME.STAT`；短名 `mag` -> `魔力`）。译文将其误译为 `魔法`（混淆了属性 Magic 与法术/魔法类别 Magic），违背明确适用的战斗属性术语规范。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/cults/tome-cults/data/birth/demented.lua:83`（DLC公开快照，源码commit未固定），迷乱系职业创建界面属性加值展示。



## O069 | entry-03464

### C16 | entry-03464 | 仅建议

原文：“+3 Magic”；译文：“+3 魔法”。

这里明确是六项属性中的一项。术语子集记录“Magic／魔力”，但状态为 `existing`，且标签为 `stat name`，本条为 `_t`，不足以据此判定强制术语违规。状态：**advisory，仅属性命名一致性意见**。证据：`C/data/birth/demented.lua:81` 的属性标题、第 83 行说明和第 87 行 `mag=3`。



## O070 | entry-03464

### C24 | entry-03464 | 仅建议
- "+3 Magic" 译成「魔法」，术语快照中 Magic（stat name）＝魔力，但状态是 existing。
- 同组的 context.lua:404/414 等处都一致用「魔法」，属于全库术语策略，不在单条范围内判定为缺陷。



## O071 | entry-03465

### C17 | entry-03465 | 待确认

原文：“Life per level: +3”；译文：“每等级生命加值：+3”。

`C/data/birth/demented.lua:122` 实际增加 `life_rating=3`。固定本体 `Actor.lua:4020` 的升级逻辑还会调用 `getRankLifeAdjust`；该函数在第 1851 行依据等级和阶级缩放输入。因此，`+3` 并不普遍等于实际每级额外增加 3 点最大生命。

状态：**pending，上游标签精度疑点**。译文沿袭原文；目标 DLC 快照适用性未固定。



## O072 | entry-03466

### C18 | entry-03466 | 待确认

原文：“Life per level: -4”；译文：“每等级生命加值：-4”。

`C/data/birth/demented.lua:175` 修改的是 `life_rating=-4`，随后仍经过固定本体 `Actor.lua:4020` 的生命成长计算，不能普遍解释为每级直接少 4 点最大生命。

状态：**pending，上游标签精度疑点**。不是翻译新增数值错误；缺 DLC 目标版本绑定。



## O073 | entry-03468

### C13 | entry-03468 | 存在问题
- **原文短引**：`#LIGHT_BLUE# * +2 Magic, -1 Willpower, +0 Cunning`
- **译文短引**：`#LIGHT_BLUE# * +2 魔法，-1 意志，+0 灵巧`
- **问题具体内容**：同 C12。在抓狂矮人（Drem）种族属性修正列表中，基础战斗属性 `Magic` 被错误译为 `魔法` 而非规范术语 `魔力`（`T.GAME.STAT`）。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/cults/tome-cults/data/birth/drem.lua:33`（DLC公开快照，源码commit未固定），Drem 种族属性加值展示。



## O074 | entry-03468

### C19 | entry-03468 | 仅建议

原文：“+2 Magic”；译文：“+2 魔法”。

属性数值及其所指没有改变。与子集中的“魔力”存在命名差异，但该记录为 `existing`，不构成强制改名依据。状态：**advisory，仅一致性意见**。证据：`C/data/birth/drem.lua:31`、第 33 行及第 37 行 `inc_stats.mag=2`。



## O075 | entry-03468

### C25 | entry-03468 | 仅建议
- 同 C24（drem.lua:33）。



## O076 | entry-03469

### C20 | entry-03469 | 待确认

原文：“Life per level: 12”；译文：“每等级生命加值：12”。

`C/data/birth/drem.lua:51` 设置的是基础 `life_rating=12`；固定本体 `Actor.lua:1851`、第 4020 行仍对其作等级与阶级调整，并非所有等级都固定增加 12 点最大生命。

状态：**pending，上游标签精度疑点**。数值转录正确，机制适用性缺 DLC 目标版本绑定。



## O077 | entry-03472

### C14 | entry-03472 | 存在问题
- **原文短引**：`#LIGHT_BLUE# * -2 Magic, +2 Willpower, +0 Cunning`
- **译文短引**：`#LIGHT_BLUE# * -2 魔法，+2 意志，+0 灵巧`
- **问题具体内容**：同 C12、C13。在克罗格（Krog）种族属性修正列表中，基础战斗属性 `Magic` 被错误译为 `魔法` 而非规范术语 `魔力`（`T.GAME.STAT`）。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/cults/tome-cults/data/birth/krog.lua:33`（DLC公开快照，源码commit未固定），Krog 种族属性加值展示。



## O078 | entry-03472

### C21 | entry-03472 | 仅建议

原文：“-2 Magic”；译文：“-2 魔法”。

六属性列表的对象和数值明确，负号完整。与术语子集 existing 记录的区别仅作为命名一致性意见，不判强制术语错误。状态：**advisory**。证据：`C/data/birth/krog.lua:31`、第 33 行及第 38 行 `inc_stats.mag=-2`。



## O079 | entry-03472

### C26 | entry-03472 | 仅建议
- 同 C24（krog.lua:33）。



## O080 | entry-03473

### C22 | entry-03473 | 待确认

原文：“Life per level: 13”；译文：“每等级生命加值：13”。

`C/data/birth/krog.lua:55` 设置 `life_rating=13`。实际消费者仍是固定本体 `Actor.lua:4020` 及 `getRankLifeAdjust`，不能将 13 当作所有等级固定的生命增量。该 DLC 文件第 34 行的注释也明确指出上游标签应称 life rating；结论依据是实际计算，并非仅凭注释。

状态：**pending，上游标签精度疑点**。目标 DLC 版本适用性尚未绑定。



## O081 | entry-03475

### C15 | entry-03475 | 存在问题
- **原文短引**：`Oh, I suddenly feel like I have potential to grow.`
- **译文短引**：`哦，我觉得我的潜能增长了。`
- **问题具体内容**：
  1. 遗漏表即时时序的副词：原文 `suddenly`（突然）未予翻译。该对话分支是玩家选择赠予 NPC 属性点（`[Offer her stat increases.]`）后 NPC 的即时反应，“突然感到”体现了属性提升生效的当下感。
  2. 语义轻度偏离：`have potential to grow`（有了成长的潜力/潜能）表示具备了后续成长的空间，译文转写为“潜能增长了”，在表意重点上略有偏移。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/cults/tome-cults/data/chats/godfeaster-malyu-escaped.lua:73`（DLC公开快照，源码commit未固定），救出玛露（Malyu）后的对话节点。



## O082 | entry-03475

### C19 | entry-03475 | 仅建议

原文“I feel like I have **potential to grow**”，译文“我觉得我的**潜能增长了**”。后者更像潜能已经提高，前者更重成长空间；但该句紧接玩家选择提供属性增益的对话分支（`C/data/chats/godfeaster-malyu-escaped.lua:47–55、72–76`），两者在此均能表达获得成长机会。不足以判定为实质时序错误。状态：仅措辞建议。



## O083 | entry-03475

### C23 | entry-03475 | 仅建议

原文：“feel like I have potential to grow”；译文：“觉得我的潜能增长了”。

译文偏抽象，原文更着重于感到自己有继续成长的潜力。不过这是接受属性奖励后的感想，没有承诺具体数值或新的成长机制，当前语境下不足以认定玩法信息错误。状态：**advisory，仅表达重心与自然度意见**。证据：`C/data/chats/godfeaster-malyu-escaped.lua:53` 跳转 `stats`，第 73 行显示该回应。



## O084 | entry-03475

### C27 | entry-03475 | 仅建议
- "I suddenly feel like I have potential to grow." 译成「我觉得我的潜能增长了。」
- "suddenly" 被略去；「有成长潜力」变成「潜能增长了」，在给属性点的语境下（godfeaster-malyu-escaped.lua:52/72-73）含义基本一致。



## O085 | entry-03476

### C28 | entry-03476 | 仅建议
- "Fine, be that way. Good luck out there, though." 译成「好吧，就这样吧。祝你一路顺风。」
- 赌气的语气和 though 的转折略弱，信息没有丢失。
- 来源：godfeaster-malyu-escaped.lua:79-80，玩家选择什么都不给的分支。



## O086 | entry-03477

### C29 | entry-03477 | 仅建议
- "Who..what.. YES!" 译成「是谁…什么…对！我在里面！」
- 对上一句 "There's someone else in here?"（godfeaster-malyu.lua:31）的回应增补了「我在里面」，与语境一致，不改变信息。



## O087 | entry-03478

### C20 | entry-03478 | 存在问题

原文物品“**rolls** from the sack”，译文“**掉**了出来”。滚出的运动方式被改为掉落。事件在生成物品后显示该日志，见 `C/data/general/events/digestive-sack.lua:104–108`。状态：文本确认。



## O088 | entry-03478

### C24 | entry-03478 | 存在问题

原文：“An object rolls from the sack”；译文：“一个物品……掉了出来”。

原文明确描述滚出，译文改成掉出，丢失并替换了物品的运动方式。状态：**confirmed，轻微但可直接核验的动作语义错误**。

证据：`C/data/general/events/digestive-sack.lua:107` 放置物品，第 108 行显示此日志。代码没有另外提供足以证明译文是在纠正上游动画描述的证据。



## O089 | entry-03479

### C16 | entry-03479 | 仅建议
- **原文短引**：`#DARK_SEA_GREEN#A not yet digested foe burst out from the sack!`
- **译文短引**：`#DARK_SEA_GREEN#一个没有被完全消化的敌人从消化袋里掉了出来！`
- **建议内容**：原文动词短语为 `burst out from the sack`，表现尚未消化的强敌猛烈冲出、破囊而出的攻击性动态；译文使用“掉了出来”，动词表现力明显被弱化为被动掉落。但该句已准确传达“未被消化的敌人脱离消化袋出现”的事实，不构成事实误导，属修辞表现力提升建议。
- **状态**：仅建议



## O090 | entry-03479

### C21 | entry-03479 | 存在问题

原文敌人“**burst out** from the sack”，译文“**掉**了出来”。原文强调敌人猛然冲出，译文变为被动掉落；对应事件生成敌人后显示该日志，见 `C/data/general/events/digestive-sack.lua:109–117`。状态：文本确认。



## O091 | entry-03479

### C25 | entry-03479 | 存在问题

原文：“foe burst out”；译文：“敌人……掉了出来”。

原文描写敌人突然冲出，译文变成被动掉落，改变了出场动作及其突发性。状态：**confirmed，动作语义错误**。

证据：`C/data/general/events/digestive-sack.lua:109` 的守卫分支在附近放置敌方 actor，第 117 行显示此日志。它与上一条物品出现属于不同对象、不同动作的叙述。



## O092 | entry-03479

### C30 | entry-03479 | 存在问题（动作语义）
- "A not yet digested foe **burst out** from the sack!" 译成「……从消化袋里掉了出来！」
- 源码 digestive-sack.lua:109-117 会在附近空格加入活的 chest_guards（敌对单位）。「冲出」变成被动的「掉出」，同时「未完全消化的敌人掉出来」容易读成掉出一具残骸，失去了「活敌来袭」的提示。



## O093 | entry-03481

### C17 | entry-03481 | 仅建议
- **原文短引**：`You have already scavenged what you could understand and use.`
- **译文短引**：`你已经找遍了你能理解和使用的东西。`
- **建议内容**：原文 `scavenged what you could understand and use` 意为已将能理解和使用的物品搜刮带走。译文“找遍了你能理解和使用的东西”将搜刮对象误作了搜查范围，动宾搭配略显生硬（通常为“找遍了残骸”或“搜刮走了所有能用的物品”）。鉴于能正常传达残骸已无可搜刮物的游戏信息，属措辞润色建议。
- **状态**：仅建议



## O094 | entry-03481

### C22 | entry-03481 | 存在问题

原文“already **scavenged what you could understand and use**”，译文“已经**找遍了**你能理解和使用的东西”。原文表示已搜取得到可用之物，译文只表示搜索过；快照中 `searched_dwarf` 为真时显示此句，首次交互会将物品放入玩家库存，见 `C/data/general/events/space-dwarf-ship.lua:60–71`。状态：文本差异确认，快照行为为佐证；目标 DLC 版本的适用性仍未固定。



## O095 | entry-03481

### C26 | entry-03481 | 存在问题

原文：“already scavenged what you could understand and use”；译文：“已经找遍了你能理解和使用的东西”。

原文说明可利用物品已经搜取，译文只说明找过，未表达物品已经取得、此处可用资源已被搜取的结果。状态：**confirmed，完成结果遗漏**。

证据：`C/data/general/events/space-dwarf-ship.lua:62` 在 `searched_dwarf` 已设置时显示该消息；首次交互则在第 70 行通过 `addObject` 将物品加入背包，第 71 行设置该标记。快照中的消费逻辑与原文“已搜取”一致；文本遗漏本身不依赖 DLC 版本判定。

实际读取范围与版本如下。

本包根路径 `P`：

```text
/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g08-20260923
```

读取了以下冻结材料；40 条原文、译文及顺序已逐条核对一致：

```text
P/INPUT.md
P/entries.json
P/context.lua
P/source-access.json
```

读取了以下 21 个本组源码文件。每个文件均完成 SHA-256 校验，与 `source-access.json.files_sha256` 一致；均为 DLC 未固定仓库／commit 的快照：

```text
P/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/timed_effects.lua
P/sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/zones/searing-halls/npcs.lua
P/sources/dlc/ashes-urhrok/tome-ashes-urhrok/init.lua
P/sources/dlc/ashes-urhrok/tome-ashes-urhrok/overload/data/texts/intro-ashes-urhrok.lua
P/sources/dlc/ashes-urhrok/tome-ashes-urhrok/overload/data/texts/unlock-corrupter_demonologist.lua
P/sources/dlc/ashes-urhrok/tome-ashes-urhrok/overload/data/texts/unlock-race_doomelf.lua
P/sources/dlc/ashes-urhrok/tome-ashes-urhrok/overload/mod/class/DemonologistsDLC.lua
P/sources/dlc/cults/tome-cults/data/achievements/all.lua
P/sources/dlc/cults/tome-cults/data/birth/demented.lua
P/sources/dlc/cults/tome-cults/data/birth/drem.lua
P/sources/dlc/cults/tome-cults/data/birth/krog.lua
P/sources/dlc/cults/tome-cults/data/chats/godfeaster-malyu-escaped.lua
P/sources/dlc/cults/tome-cults/data/chats/godfeaster-malyu.lua
P/sources/dlc/cults/tome-cults/data/general/events/digestive-sack.lua
P/sources/dlc/cults/tome-cults/data/general/events/space-dwarf-ship.lua
P/sources/dlc/cults/tome-cults/data/general/grids/fonts.lua
P/sources/dlc/cults/tome-cults/data/general/grids/fortress-multiverse.lua
P/sources/dlc/cults/tome-cults/data/general/grids/godfeaster.lua
P/sources/dlc/cults/tome-cults/data/general/grids/maggot.lua
P/sources/dlc/cults/tome-cults/data/general/grids/slimy_godfeaster.lua
P/sources/dlc/cults/tome-cults/data/general/npcs/blobs.lua
```

额外 DLC 源码根路径 `D`：

```text
/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/ashes-urhrok
```

以下文件均属于 `dlc_additional_sources` 白名单，且读取前核对哈希一致：

| 实际路径 | 已读引用来源 |
|---|---|
| `D/tome-ashes-urhrok/data/talents/misc/races.lua` | `DemonologistsDLC.hookLoad:34` 的显式加载。 |
| `D/tome-ashes-urhrok/data/talents/corruptions/corruptions.lua` | `DemonologistsDLC.hookLoad:35` 的显式加载。 |
| `D/tome-ashes-urhrok/data/birth/corrupted.lua` | `DemonologistsDLC.hookLoad:39` 的显式加载。 |
| `D/tome-ashes-urhrok/data/general/objects/world-artifacts.lua` | `DemonologistsDLC.hookEntityLoadList:47` 的显式加载；核对 Shadow Power 和手套描述。 |
| `D/tome-ashes-urhrok/data/talents/corruptions/demonic-pact.lua` | `corruptions.lua:153` 的显式加载；追踪种子召唤及生命保存。 |
| `D/tome-ashes-urhrok/data/talents/corruptions/wrath.lua` | `corruptions.lua:162` 的显式加载，以及神器引用的 `T_OBLITERATING_SMASH`。 |

本体只通过 `/workspace/t-engine4` 的 `git show` 读取以下单文件，版本均为 **`624a67329fe2ad440c5b344785a9c73fcf22ae63`**：

| 源码路径 | 调用链或符号来源 |
|---|---|
| `game/modules/tome/class/Actor.lua` | 出生定义的 `life_rating`、已读源码的 Actor 调用及活力恢复字段，追踪实际消费者。 |
| `game/modules/tome/class/Player.lua` | `Actor` 中的 `game.player` 与升级逻辑，核对玩家的继承及 `fixed_rating`。 |
| `game/modules/tome/class/interface/PlayerStats.lua` | `Player.lua:27`、第 46 行显式引用；检查生命成长方法是否被覆盖，未找到相应覆盖。 |
| `game/engines/default/engine/interface/ActorResource.lua` | `Actor.lua:31` 的 `require` 及第 602 行 `regenResources()`。 |
| `game/modules/tome/data/resources.lua` | 已读 `vim_regen` 与 `ActorResource.defineResource`，核对活力资源的具体绑定。 |

未读取其他报告、当前翻译文件、其他语言答案、SPEC／STATE 或当前源码工作树；未创建子 agent、临时文件或修改仓库。默认沙箱首次启动失败后，仅以获准的只读命令完成访问。无读取范围越界；未能核验的主要限制是 DLC 快照与目标版本的绑定。以上为独立审核观察，不是生产完成认证。


## O096 | entry-03488

### C32 | entry-03488 | 仅建议
- "You think you can open it." 译成「你觉得你可以打开它」，与原文一致，只是「你觉得」略口语化。
- 来源：godfeaster.lua:135 的 door_player_check。



## O097 | entry-03489

### C33 | entry-03489 | 仅建议
- 同 C32（maggot.lua:136）。



## O098 | entry-03490

### C34 | entry-03490 | 仅建议
- 同 C32（slimy_godfeaster.lua:135）。

> 更正：上表里 entry-03488/03489/03490 已按 C32–C34 标为「仅建议」。这三条其实只是同一个极轻的措辞偏好，也可以看作未发现问题。以表中「仅建议」为准，不影响缺陷计数。

---



## O099 | entry-03491

### C18 | entry-03491 | 存在问题
- **原文短引**：`A green oozing defence cell of the Maggot.`
- **译文短引**：`这团绿泥是巨大蛆虫的防御细胞。`
- **问题具体内容**：
  1. 状态修饰词漏译：`oozing`（渗液的 / 淌着黏液的）作为描述细胞生物体表特征的核心修饰语，在译文中被直接丢弃。
  2. 臆造实体称谓：原文核心为名词短语 `A green oozing defence cell`（一个渗液的绿色防御细胞），译文强行重组为判断句并凭空捏造了原文不存在的称谓“这团绿泥”（该 NPC 实体名为 plasmic disruptor，基础类型虽为 BLOB，但英文文本本身并无“泥/绿泥”词汇）。
- **状态**：已证实问题
- **源码与消费逻辑**：`sources/dlc/cults/tome-cults/data/general/npcs/blobs.lua:54`（DLC公开快照，源码commit未固定），等离子分裂细胞的怪物介绍。



## O100 | entry-03491

### C19 | entry-03491 | 仅建议
- **原文短引**：`of the Maggot`
- **译文短引**：`巨大蛆虫的`
- **建议内容**：`the Maggot` 在 Cults of Entropy 中为特定巨型异形区域/生物的专名（术语快照：`maggot` -> `蛆虫`，`T.GAME.ENTITY`，creatures，entity subtype）。译文增添修饰词译为“巨大蛆虫”，虽然符合其实体背景事实，但相比标准专名稍显随意，建议与实体专名保持一致。
- **状态**：仅建议

---



## O101 | entry-03491

### C31 | entry-03491 | 待确认
- "defence cell of **the Maggot**" 译成「巨大蛆虫的防御细胞」。
- the Maggot 首字母大写，是专指对象；译文加了「巨大」的描述。
- 缺少的证据：该专名（区域或生物）在游戏中的正式译名，不在允许材料内。
- 来源：blobs.lua:55。


