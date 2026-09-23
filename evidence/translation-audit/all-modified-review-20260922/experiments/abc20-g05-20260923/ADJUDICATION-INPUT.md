# 匿名源码核验与归并：40 条 / 74 项观察

你是本任务独立 REVIEWER。用户要求继续三模型实验并归并问题；本阶段依据源码核验，不参与参赛评分。参考是暂定模型裁决，非人工金标准。禁止寻找模型身份或读取来源映射、原始报告、STATE、其他实验目录。不得以多数票、重复次数、报告声称“已证实”替代证据。

唯一允许输入：本文件、同目录 INPUT.md、entries.json、context.lua、source-access.json、source-access.json 明确列出的冻结源码。先阅读INPUT统一判定规则；沿其限定调用链读取单文件。本体使用git show固定commit；DLC只能使用获准的哈希快照，不能把引擎commit套用于DLC，缺少目标版本适用证据则保留pending；无源码组件仅确认文本可证偏差。后续实验的临时文件已获用户授权，可用自己创建的任务专属临时目录；仓库只读，不创建子agent。

下方74项匿名观察按entry和文字排序，包括问题、建议及待确认。各观察C编号仅为原报告局部编号，不跨观察匹配；统一以O编号标识。保持原断言供核验但不采信。请逐项确认、否决、待确认或仅建议；同条同义缺陷合并为canonical D-ID，不同信息或机制错误拆开。注明翻译新增/沿袭上游。遇实质争议要核实双方论据和完整上下文，证据不足保留pending。缺陷边界应考虑完整界面语境，不把单词必然等同为排他机制断言；也不能因玩家猜得出或英文有同错就豁免。

同时独立检查全部40条，包括没有观察或全部观察被否决的条目，补充漏项。只依据INPUT/源码/语境，不能读取其他轮答案。

输出要求：三个Markdown表格，再补充必要解释与读取路径。
1. 恰好40行：entry-ID | 判定（OK/ISSUE/PENDING） | canonical D或P编号/简短依据。OK包括仅建议；有确认缺陷即ISSUE，即使附带pending；无确认但仍有疑点才PENDING。严格冻结顺序。
2. 确认缺陷表：D-ID（D01起） | entry-ID | 内容、归因及固定源码路径:行号/调用链证据。未决用P-ID另列，不混入D。每个D须实际核验。
3. 恰好74行：O-ID | 状态（confirmed/refuted/pending/advisory/mixed） | 命中D-ID（无则—） | 具体证据与理由。mixed须明确哪些部分confirmed、refuted、pending或advisory；不要把未命中的错误问题借用同条其他正确D。若仅有措辞问题则advisory。补充说明所有未决与主要分歧如何处理。

不要给模型排名或分数、不要修改译文，不宣称DONE_VERIFIED。列出实际读取的路径和额外单文件引入依据；未完成的机制核验如实记录。



## O001 | entry-03333

### C01 | entry-03333 | 存在问题

原文“upload **your addon** directly from here”译为“你可以直接在这里上传”，省去上传对象及“你的”所属关系。即使能从插件开发界面猜出对象，操作说明仍丢失了原文明确的信息。此项只据冻结原译文本判断；addon-dev 源码不可用。



## O002 | entry-03335

### C01 | entry-03335 | 仅建议

原文：“copy translation file to”；译文：“将翻译文件拷贝去的插件”。

“拷贝去的插件”略显生硬，但文件、操作和目的地关系均明确。`context.lua:95–106` 的插件选择及复制成功提示也支持这一理解。属于措辞偏好，无已证实信息损失。



## O003 | entry-03335

### C01 | entry-03335 | 仅建议
- **短引**：
  - 原文：`Choose the addon you want to copy translation file to.`
  - 译文：`选择你想要将翻译文件拷贝去的插件。`
- **问题说明**：译文“拷贝去的插件”带方言或口语色彩，介词与动词搭配略显生硬；但目标对象与操作含义准确完整，未造成歧义或信息丢失。
- **状态**：仅建议。
- **依据与语境**：所属组件 `addon-dev` 源码未提供（`unavailable`），纯文本语义核对。仅属措辞自然度与书面语润色偏好，不构成缺陷。



## O004 | entry-03335

### C02 | entry-03335 | 仅建议

“将翻译文件拷贝去的插件”能表达目标插件，“拷贝去”只是搭配不够自然；没有可证的信息错误。



## O005 | entry-03336

### C02 | entry-03336 | 仅建议
- **短引**：
  - 原文：`Activated all 23 different kinds of demon statues.`
  - 译文：`启动全部23个不同的恶魔雕像。`
- **问题说明**：原文为 "23 different kinds of demon statues"；在代码逻辑中，该成就统计的是23种恶魔雕像（`statue_kind = kind`）。中文译文使用了量词“个”（“23个不同的恶魔雕像”），虽然表达了23个各不相同，但从分类属性上看，量词“种”更符合 "different kinds" 的范畴概念。
- **状态**：仅建议。
- **依据与消费逻辑**：源码快照 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/general/grids/demon_statues.lua:22-59` 中定义了23个 `kind`，成就 `ASHES_ALL_STATUES` 统计该激活计数。译文对成就达成条件无实质误导，仅属量词精确度偏好。



## O006 | entry-03336

### C02 | entry-03336 | 待确认

原文：“all 23 different kinds”；译文：“全部23个不同的恶魔雕像”。

文本确有“种类”与“个体”计量差异，但快照实现不能支持直接把“必须覆盖23种”认定为正确机制：

- `D/data/achievements/all.lua:35–39` 的 `can_gain` 仅增加 `self.nb`，达到23即满足条件。
- `D/data/general/grids/demon_statues.lua:87–92` 只对当前雕像实例防止重复激活，调用 `world:gainAchievement` 时不传种类。
- `A/data/general/events/demon-statue.lua:25–35` 每次事件重新建立候选种类；移除已选种类只作用于本次事件。
- 本体 `game/engines/default/engine/interface/WorldAchievements.lua:131–146` 按成就保存计数数据并调用 `can_gain`，未增加种类去重。

快照内可证的是累计激活数量，英文的种类要求属于上游描述与实现的疑点，不能简单判成译文漏译机制。**缺少目标 DLC 版本来源及其实际实现，保留待确认。**



## O007 | entry-03341

### C03 | entry-03341 | 仅建议
- **短引**：
  - 原文：`#LIGHT_BLUE# * +2 Magic, +0 Willpower, +1 Cunning`
  - 译文：`#LIGHT_BLUE# * +2 魔法，+0 意志，+1 灵巧`
- **问题说明**：角色六大基础属性中的 Magic 在角色面板与通用术语中统一称为“魔力”；此处译文采用了“魔法”。因术语快照中 `Magic -> 魔力` 的 status 为 `existing`，依据规则 `existing不构成强制改名依据`，且玩家在属性修正列表中完全能够理解其指代魔力属性，故不列为缺陷。
- **状态**：仅建议。
- **依据与消费逻辑**：源码快照 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/birth/corrupted.lua:57`，属于创角面板描述文本，建议全库统一为“魔力”。



## O008 | entry-03341

### C07 | entry-03341 | 仅建议
- 译文“+2 魔法”；术语 Magic/mag 是“魔力”（stat name，existing）。
- 为什么只算建议：这条术语状态是 existing，不是强制改名依据。同文件的 Doombringer 描述也用“魔法”，属于一致性偏好。数值正确。



## O009 | entry-03345

### C01 | entry-03345 | 存在问题
- 原文：“Silence these beings, **maintain your deception**”；译文：“静默他们的声音，**隐藏你的踪影**”。
- 原文是“继续维持你的欺瞒”，译文改成了“藏好行踪”，“欺瞒”这层意思没了。
- 依据：doomelf.lua:26-31 的 `locked_desc` 是 Doomelf 种族的解锁提示诗。“三者可以向恶魔诉说精灵造成的恐怖”，所以要让三者噤声、把欺瞒维持下去。这是纯语义判断。



## O010 | entry-03345

### C02 | entry-03345 | 存在问题（影响较轻）
- 原文：“one fights for the third with the cultists **she taught**”；译文：“之一召集邪徒为复活另一者而战”。
- “她亲手教出的邪徒”被改成“召集邪徒”，丢了两点：这个恶魔是女性，而且邪教是她传授的。这两点正是用来辨认对象的提示。
- 依据：同文件的解锁条件是成就 The Old Ones（achievements/all.lua:85-107，击杀三者后 `setAllowedBuild("race_doomelf")`）。lore 条目里莎西·凯希以女性口吻自述，也与邪徒有关（见 context.lua:656-692 的上下文）。
- 另：“复活另一者”对应 “for the third”，属于 lore 支持的引申，不计。



## O011 | entry-03345

### C03 | entry-03345 | 存在问题

原文“one fights for the third **with the cultists she taught**”译为“召集邪徒**为复活另一者**而战”。译文加入原句未说明的“复活”目的，并丢失“她教导的邪徒”这一关系。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/birth/doomelf.lua:27–32`，`locked_desc`。



## O012 | entry-03345

### C03 | entry-03345 | 存在问题

原文：“One rages and torments”；译文：“之一……永远咆哮”。

译文保留了愤怒表现，却遗漏“折磨”这一行为，并新增永久持续的描述。证据为冻结诗歌及 `D/data/birth/doomelf.lua:29`；这是行为信息变化，不只是诗体取舍。状态：**confirmed，文本语义问题**。



## O013 | entry-03345

### C04 | entry-03345 | 存在问题

原文“**Silence these beings**”译为“静默**他们的声音**”，将处理三个存在本身改成处理声音。相邻成就要求杀死三名恶魔，达成后解锁 Doomelf；这里的解锁提示具有操作含义。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/birth/doomelf.lua:31–32`；`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/achievements/all.lua:84–107`，`ASHES_OLD_ONES.can_gain/on_gain`。



## O014 | entry-03345

### C04 | entry-03345 | 存在问题

原文：“with the cultists she taught”；译文：“召集邪徒”。

原文明确邪教徒受她教导；“召集”不能表达这一关系。`D/data/birth/doomelf.lua:30` 是直接证据。`D/data/lore/demon.lua:456–460` 支持组织追随者及恢复恋人的背景，因此不将“复活”单独判错；这里确认的是**教导关系遗漏**。

状态：**confirmed，文本语义问题**。



## O015 | entry-03345

### C04 | entry-03345 | 存在问题
- **短引**：
  - 原文：`One rages and torments in deep oceans blue, / one fights for the third with the cultists she taught.`
  - 译文：`之一在无尽的深海中永远咆哮 / 之一召集邪徒为复活另一者而战`
- **问题说明**：
  1. 第4句原文为 "with the cultists she taught"（带着她所传授/教导的邪教徒），体现了莎西·凯希传授信徒腐化知识并率领其战斗的师徒/从属关系；译文意译为“召集邪徒”，将定语从句 "she taught"（她所教导）完全遗漏。
  2. 第3句原文 "torments"（折磨/肆虐）未译出，意译加入了“无尽”与“永远”。
- **状态**：存在问题。
- **依据与消费逻辑**：源码快照 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/birth/doomelf.lua:27-32`（魔化精灵解锁诗歌）。诗中逐一对应被困埃亚尔的三大恶魔（深海的乌尔罗格、带领被其教导信徒的莎西·凯希，以及第三者克里尔·费扬）。遗漏 "she taught" 丢失了背景剧情中莎西·凯希与邪教徒的关系信息。



## O016 | entry-03345

### C05 | entry-03345 | 存在问题

原文“**maintain your deception**”译为“**隐藏你的踪影**”。维持伪装或欺骗与隐藏行踪不是同一行为。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/birth/doomelf.lua:31`，`locked_desc`。



## O017 | entry-03345

### C05 | entry-03345 | 存在问题

原文：“maintain your deception”；译文：“隐藏你的踪影”。

维持欺骗与掩藏行踪是不同目的。前文说明三者可能向恶魔揭露精灵造成的恐怖，灭口服务于继续蒙骗恶魔，而非避免被追踪。证据：`D/data/birth/doomelf.lua:27–32`。

状态：**confirmed，目的关系误译**。



## O018 | entry-03345

### C06 | entry-03345 | 存在问题

原文“**may witness** a new elf’s **conception**”译为“新的精灵**终将诞生**”：可能见证孕育变成必然出生，条件与阶段均改变。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/birth/doomelf.lua:32`，`locked_desc`。



## O019 | entry-03345

### C06 | entry-03345 | 存在问题

原文：“and then you may witness”；译文：“新的精灵终将诞生”。

原文说明完成前述行动后，玩家才可能见证诞生；译文变为诞生终将发生，丢失“之后才可能”及玩家见证的关系。证据：`D/data/birth/doomelf.lua:31–32`。

状态：**confirmed，条件和情态信息变化**。



## O020 | entry-03347

### C05 | entry-03347 | 仅建议
- **短引**：
  - 原文：`#LIGHT_BLUE# * +3 Magic, +2 Willpower, +0 Cunning`
  - 译文：`#LIGHT_BLUE# * +3 魔法，+2 意志，+0 灵巧`
- **问题说明**：同 C03，属性名 Magic 译为“魔法”，术语状态为 existing，不构成强制缺陷，建议与“魔力”统一。
- **状态**：仅建议。
- **依据与消费逻辑**：源码快照 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/birth/doomelf.lua:39`。



## O021 | entry-03347

### C08 | entry-03347 | 仅建议
- 同 C07（“+3 魔法”）。



## O022 | entry-03352

### C06 | entry-03352 | 仅建议
- **短引**：
  - 原文：`All enemies in radius 2 take 20 fire damage each turn and healing you for 10% of the damage dealt.`
  - 译文：`附近2码范围的敌人每回合受到20火焰伤害。你受到10%伤害值的治疗。`
- **问题说明**：后半句“你受到10%伤害值的治疗”略显生硬欧化，但作用对象（你）、数值比例（10%伤害）以及触发逻辑（治疗）完全准确。
- **状态**：仅建议。
- **依据与消费逻辑**：源码快照 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/general/objects/world-artifacts.lua:118, 142`（Fearfire Mantle）调用 `engine.DamageType.FIRE_DRAIN`，引擎固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63:game/modules/tome/data/damage_types.lua:1251` 确认其 `healfactor = 0.1`，机制数值与译文完全吻合。仅属语感偏好。



## O023 | entry-03353

### C03 | entry-03353 | 存在问题
- 原文：“Status resistances shift **over time** to match…”；译文：“依据你中的负面状态改变你的状态免疫。”
- 译文丢了“随时间逐渐”这个时序，读起来像一次性立即改变。
- 依据：world-artifacts.lua:315-400，Revenant 的 `act`。每次物品行动时，它检查身上现有的眩晕、混乱、定身、沉默效果；对每一种命中的状态，循环 5 次，每次从其他免疫各扣 0.01、转加到这一项。所以是渐进的转移。



## O024 | entry-03353

### C07 | entry-03353 | 存在问题

原文“resistances **shift over time**”译为“依据……改变……免疫”，漏掉逐渐调整的时序。快照中的装备 `act` 每次按当前状态从其他免疫值挪移小额数值，并非一次切换完成。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/general/objects/world-artifacts.lua:315–427`，`Revenant.act`。目标版本是否使用此未固定 DLC 快照待确认。



## O025 | entry-03353

### C07 | entry-03353 | 存在问题

原文：“shift over time”；译文：“依据……改变”。

译文遗漏抗性随时间调整的过程，仅保留按状态改变。`D/data/general/objects/world-artifacts.lua:322–427` 的 `act` 会读取当前效果，并在反复执行时逐步转移各项免疫数值；这支持英文时间信息确有意义。

“状态免疫”本身不判错：实际修改的正是 `confusion_immune`、`stun_immune` 等数值。状态：**confirmed，冻结文本的时间信息遗漏**；快照机制仅作支持，不外推目标版本。



## O026 | entry-03353

### C07 | entry-03353 | 存在问题
- **短引**：
  - 原文：`Status resistances shift over time to match the statuses you are being hit by.`
  - 译文：`依据你中的负面状态改变你的状态免疫。`
- **问题说明**：原文核心机制短语 "shift over time"（随时间推移逐渐转移/调整），译文“依据你中的负面状态改变你的状态免疫”完全遗漏了 "over time"（随时间推移/逐步）的时间维度修饰，容易让玩家误解为受到状态攻击时立刻全额变更免疫。
- **状态**：存在问题。
- **依据与消费逻辑**：源码快照 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/general/objects/world-artifacts.lua:315, 358-374`。装备每次 `act()` 时，若检测到角色身上存在对应负面状态，仅在 5 次循环中每次转移 0.01（即 1%）的特定状态免疫属性。该机制为明确的“随时间逐步调整”，遗漏 "over time" 导致时序机制信息缺失。



## O027 | entry-03358

### C04 | entry-03358 | 存在问题
- 原文：“Increases **all** damage penetration by 1%…”；译文：“每点“阴影强度”增加1%抗性穿透。”
- 译文丢了“全体（所有伤害类型）”这个范围。同组的 03363“全体伤害加成”、03364“全体抗性”都保留了“全体”。
- 依据：world-artifacts.lua:679-682，`self.wielder.resists_pen = {all = power}`。



## O028 | entry-03358

### C08 | entry-03358 | 存在问题

原文“**all** damage penetration”译为“抗性穿透”，未说明覆盖全部伤害类型。该装备写入的是穿透表的 `all` 项。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/general/objects/world-artifacts.lua:679–682`，`The Black Spike.on_obsidian_power_update`。目标版本适用性待确认。



## O029 | entry-03358

### C08 | entry-03358 | 存在问题
- **短引**：
  - 原文：`Increases all damage penetration by 1% for each point of your Shadow Power.`
  - 译文：`每点“阴影强度”增加1%抗性穿透。`
- **问题说明**：原文为 "all damage penetration"；译文仅写为“抗性穿透”，遗漏了关键范围限定词 "all"（全/全部）。在游戏中，抗性穿透有单系穿透（如火焰穿透、暗影穿透）与全伤害抗性穿透之分，缺少“全”导致作用范围不明确。
- **状态**：存在问题。
- **依据与消费逻辑**：源码快照 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/general/objects/world-artifacts.lua:679-681`（The Black Spike）。代码明确更新 `self.wielder.resists_pen = {all = power}`，作用于所有属性抗性穿透。同套装的 entry-03363 译有“全体伤害加成”，entry-03364 译有“全体抗性”，唯独本条遗漏了“全”。



## O030 | entry-03360

### C08 | entry-03360 | 待确认

原文：“equal to half”；译文：“每点……增加0.5%”。

`D/data/general/objects/world-artifacts.lua:731–732` 实际使用 `math.ceil(power / 2)`。戒指自身提供5点阴影强度（第725行），因此该状态下加成为3，而非2.5。

`A/superload/mod/class/Actor.lua:61–67` 将实际阴影强度传入更新函数并重新应用装备；本体 `game/modules/tome/class/interface/Combat.lua:1887–1890、2012–2025` 将该属性纳入暴击百分比并消费。

这是**英文与译文共同遗漏取整**，不是译文新增错误。快照行为已证，但目标 DLC 版本适用性未固定，故总状态为**待确认**。



## O031 | entry-03361

### C05 | entry-03361 | 存在问题
- 原文：“"Wreckage all about you. Is there anything left inside?"”；译文：“己身若残，何物能存？”
- 原文说残骸在“你四周”，并问（铠甲或你）“里面”还剩什么。译文把残骸移到“己身”，还加了一个原文没有的条件“若”，“inside”也丢了。残骸的所在从周围变成了自身，语义被改写。
- 依据：world-artifacts.lua:743，The Black Plate（重甲）的 `desc`。这是纯语义判断。



## O032 | entry-03361

### C09 | entry-03361 | 存在问题

原文“**Wreckage all about you. Is there anything left inside?**”描写周围残骸，并追问里面是否还有东西；译文“**己身若残，何物能存？**”改成自身残损后的存亡判断，丢失周围残骸与内外关系。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/general/objects/world-artifacts.lua:740–744`，`The Black Plate.desc`。



## O033 | entry-03361

### C09 | entry-03361 | 存在问题

原文：“Wreckage all about you. Is there anything left inside?”；译文：“己身若残，何物能存？”

原文以周围／包围自身的残破景象，追问内部是否仍有东西；译文改成“自身若残破”的假设，并泛问何物能够存留。外部与内部的对照、既存景象与疑问的关系均发生变化。

证据：`D/data/general/objects/world-artifacts.lua:737–743`，该句为黑之铠的物品描述。状态：**confirmed，意象关系和句意变化**，不以文风是否优美为依据。



## O034 | entry-03361

### C09 | entry-03361 | 存在问题
- **短引**：
  - 原文：`"Wreckage all about you. Is there anything left inside?"`
  - 译文：`己身若残，何物能存？`
- **问题说明**：原文 "Wreckage all about you" 中的 "about" 为空间介词（"all about you" 即 "all around you"，意为“四周/周遭各处尽是残骸”），描绘角色身穿重型铠甲、周遭化为一片废墟废土的客观外部场景，后句进而发问铠甲之内是否还有残留；译文误将空间介词 "about you" 理解为关于自身，将 "wreckage"（残骸废墟）意译为“若残”（若残破），严重曲解了原文的客观场景描写。
- **状态**：存在问题。
- **依据与消费逻辑**：源码快照 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/general/objects/world-artifacts.lua:743`（The Black Plate 描述）。黑石套装风格为冷酷极简描写，此处指周围全是毁灭的残骸，内部是否还有残存，属于语义层面的曲解。



## O035 | entry-03363

### C10 | entry-03363 | 存在问题

原文“**all damage**”是佩戴者所有类型的伤害；“**全体伤害加成**”易指全体成员的伤害加成，改变受益范围。效果实际写在本装备的 `wielder.inc_damage.all`。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/general/objects/world-artifacts.lua:813–816`，`The Black Maul.on_obsidian_power_update`。目标版本适用性待确认。



## O036 | entry-03364

### C06 | entry-03364 | 仅建议
- 译文“全体抗性”；术语快照里 All Resists 的首选译法是“全部抗性”（preferred，core，注明是角色面板行，对应 `resists.all`）。
- 为什么只算建议：这条术语针对本体面板标签，这里是 DLC 物品的描述句。“全体抗性”与同组 03363 的“全体伤害加成”风格一致，不构成错误。



## O037 | entry-03364

### C11 | entry-03364 | 存在问题

原文“**all resists**”对应佩戴者的 `resists.all`；“**全体抗性**”易表示全体成员的抗性，且冻结术语子集对这一属性给出“**全部抗性**”。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/general/objects/world-artifacts.lua:854–857`，`The Black Wall.on_obsidian_power_update`；`INPUT.md` 术语子集 `All Resists`。目标版本适用性待确认。



## O038 | entry-03365

### C09 | entry-03365 | 存在问题
- 最后一段原文：“while **a wretchling** presses it to your forehead”；译文：“一个**猥琐小怪**把它按上你额头”。
- wretchling 是 DLC 里一个具体的恶魔种类。同 DLC 其他地方都译作“酸液树魔”（context.lua:574 的 “demon statue: wretchling”，entry-03372）。译成“猥琐小怪”，读者就认不出是哪种恶魔，前文“豌豆滴淌着酸液”等改造描述也对不上号。
- 依据：demon.lua:291-296 的 lore id `ashes-urhrok-demon-statue-wretchling`。
- 格式方面：187 个方括号段和 34 个 [louder] 一一对应，标记计数和 16 段落结构都完整。原文结尾的换行在译文中没了，不影响显示，不计。



## O039 | entry-03365

### C10 | entry-03365 | 仅建议
- 原文：“only cause [hairline fracture] to their own [garden]”；译文：“却只给他们自己的**星球**造成一道[发丝裂纹]，伤及他们的[花园]”。
- 译文在方括号外加了“星球”作解释，提前揭开了“花园＝星球”这个谜底。
- 为什么只算建议：没丢失原文信息，只是加了原文刻意隐藏的解释。



## O040 | entry-03365

### C10 | entry-03365 | 存在问题

原文：“a wretchling”；译文：“一个猥琐小怪”。

这里指特定恶魔种类，译文变成泛称，丢失实施强制改造者的身份。`D/data/lore/demon.lua:60` 为直接原文；同文件第116–118行描述这种生物的酸液袭击，第294–295行明确以其为雕像介绍对象。冻结 `context.lua:203` 和 entry-03372 也将同一对象识别为“酸液树魔”。

这是**实体身份丢失**，不只是要求统一一个既有译名。状态：**confirmed**。此处位于正常叙事段落，不属于文中刻意误译的方括号隐喻。



## O041 | entry-03365

### C10 | entry-03365 | 存在问题
- **短引**：
  - 原文：`... memories of being chained and bound while a wretchling presses it to your forehead flash through your mind.`
  - 译文：`……遭锁链缠身、动弹不得时，一个猥琐小怪把它按上你额头的记忆在脑海中闪回。`
- **问题说明**：原文中将恶魔石板按在主角额头上的生物是 "a wretchling"；译文将其错译为“一个猥琐小怪”。在 ToME4 本体及本 DLC 全文（包括本条目第15段及 entry-03372）中，`wretchling` 均为固定恶魔生物种类“酸液树魔”（对应 emerald 之子改造的恶魔形态）。译作“猥琐小怪”破坏了专名统一性与世界观生物设定的严肃性。
- **状态**：存在问题。
- **依据与消费逻辑**：源码快照 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:261`（石板第16段）结合同文件第295行（entry-03372，`demon statue: wretchling` 译为“酸液树魔”）。此处属于实体专有名词误译。



## O042 | entry-03366

### C11 | entry-03366 | 存在问题

原文：“standard-issue alteration”；译文：“标准化思维修改”。

原文只说常规改造，没有限定为思维修改；译文额外指定了改造对象。上下文将防火、忠诚强化、改造和意识连接分别列举，不能由附近出现意识或忠诚就把一般改造限定为思维改造。

证据：`D/data/lore/demon.lua:135`。状态：**confirmed，译文新增范围限制**。



## O043 | entry-03366

### C11 | entry-03366 | 存在问题
- **短引**：
  - 原文：`"Just step on the plate here, and hold your arms like this so I can get the bindings in place..."`
  - 译文：`“站在那里别动，举起胳膊，这样我就能把它放好……”`
- **问题说明**：
  1. "Just step on the plate here"：看管人诱骗主角踩在特定装置踏板（plate）上，译文译为“站在那里别动”，遗漏了踏板/底板（plate）道具名词，且将指示代词 "here"（这里）错译为“那里”。
  2. "so I can get the bindings in place..."：看管人给主角套上拘束锁链（bindings，束缚具/拘束带），与前文“遭锁链缠身、动弹不得”呼应；译文误将复数名词 "bindings" 理解为代词“它”（误当成了放置水晶），译作“这样我就能把它放好”，彻底丢失了欺骗主角就擒并施加拘束的关键剧情动作。
- **状态**：存在问题。
- **依据与消费逻辑**：源码快照 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:400`。剧情中恶魔看管人以“晋升研究助理”为诱饵，诱导主角站上特定底板并伸开双臂，以便扣上束缚用具。译文遗漏 plate 并严重误译 bindings。



## O044 | entry-03366

### C11 | entry-03366 | 存在问题
- 原文：“loyalty reinforcement there, **standard-issue alteration**”；译文：“忠诚强化在那，**标准化思维修改**”。
- 原文是恶魔对身体、魔力的“标准改造”，译文加了“思维”，改造的对象变成了心智。
- 依据：同文件 demon.lua:146-199 的作战简报写到“Having been exposed to our alteration magic…”（doombringer）和“Our standard alterations have synergized with this Shalore's natural reactive magic”（doomelf，指改造后获得的相位传送能力）。可见 alteration 指的是能力或躯体改造。



## O045 | entry-03366

### C12 | entry-03366 | 存在问题

原文“**standard-issue alteration**”译为“**标准化思维修改**”，凭空限定为思维修改。同一冻结源码描述的标准改造还影响短距离传送和内脏避让，不能据此限缩为思维。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:135,189–191`，`training-recall2` 及 `tactics-doomelf` 的叙述。



## O046 | entry-03366

### C12 | entry-03366 | 存在问题

原文：“step on the plate here”；译文：“站在那里别动”。

原文要求踏上此处的平台／板面；译文变为在某处保持不动，遗漏具体承载物并改变动作。证据：`D/data/lore/demon.lua:135` 的连续操作指示。

状态：**confirmed，叙事动作信息变化**；这是回忆中的指示，不宣称它构成当前可操作任务。



## O047 | entry-03366

### C12 | entry-03366 | 存在问题
- 原文：“Just **step on the plate** here, and hold your arms like this so I can get **the bindings** in place...”；译文：“站在那里别动，举起胳膊，这样我就能把它放好……”
- 丢了“踏上底板”，也丢了“束缚／捆绑”，只剩一个指代不明的“它”。原文的反讽在于玩家欢天喜地地被绑上，这层信息没了。纯语义判断。



## O048 | entry-03366

### C13 | entry-03366 | 仅建议
- “your handler”译成“你的“主人””，开头还加了“记住，”。属于措辞增色，不影响事实，算偏好。



## O049 | entry-03366

### C13 | entry-03366 | 存在问题

原文“hold your arms like this so I can get the **bindings** in place”译为“举起胳膊，这样我就能把**它**放好”，省掉即将装上的束缚物，削弱这段记忆中受制于人的关键信息。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:133–137`，`training-recall2.lore`。



## O050 | entry-03366

### C13 | entry-03366 | 存在问题

原文：“get the bindings in place”；译文：“把它放好”。

“bindings”明确指束缚装置，译文只剩不明对象“它”，还可能被理解为前述水晶。由此丢失研究助理“晋升”实际伴随束缚的叙事信息。

证据：`D/data/lore/demon.lua:135`，紧接摆放手臂的指示。状态：**confirmed，对象及束缚动作遗漏**。



## O051 | entry-03371

### C12 | entry-03371 | 存在问题
- **短引**：
  - 原文：`... wielding a double-bladed katana and fighting a giant construct labelled "Ninja Atamathon." Your badassery must have interrupted this demon's writing.`
  - 译文：`……手里拿着武士刀，正在和“忍者王阿塔玛森”对战。看起来，你的霸气侧漏把这个恶魔吓尿了。`
- **问题说明**：
  1. "double-bladed katana" 中的 "double-bladed"（双刃/双头）漏译，仅译为“武士刀”。
  2. "fighting a giant construct labelled 'Ninja Atamathon.'" 中的实体类别 "giant construct"（巨型构装体）被彻底遗漏，直接抹去了阿塔玛森作为“构装体”的实体描述。
  3. "Your badassery must have interrupted this demon's writing."（一定是你的霸气打断了这个恶魔的书写），原文呼应便条结尾被拖出墨迹的断句 "befo--"；译文被随意替换为“把这个恶魔吓尿了”，完全丢失了“字迹被霸气当场打断”的画面解构关键语义。
- **状态**：存在问题。
- **依据与消费逻辑**：源码快照 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:491`。文本为恶搞风格的战斗汇报便条，"double-bladed katana"（致敬流行文化中夸张双刃武士刀）与 "giant construct"（构装体为游戏核心生物实体分类）均为具象设定描述，结尾亦与笔画拖断的视觉细节紧密扣合。



## O052 | entry-03371

### C14 | entry-03371 | 存在问题

原文“**Blow all connectors**”译为“**关闭所有链接传送门**”。前者要求炸断连接结构；与下一句“把平台从大陆分离”相连。译文改成关闭传送门，改变了命令对象及动作。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:226`，`tactics-failed-badass.lore`；普通版本的同一命令见该文件 `:210`。



## O053 | entry-03371

### C14 | entry-03371 | 存在问题

原文：“Highest priority is now isolating”；译文：“启动最高优先级措施”。

译文只保留优先级，未交代措施是隔离玩家。后面的体育场及平台分离描写不能替代这项明确行动目标。

证据：`D/data/lore/demon.lua:226`。状态：**confirmed，行动目标遗漏**。



## O054 | entry-03371

### C14 | entry-03371 | 存在问题
- 原文：“Highest priority is now **isolating** <?=player.name?>, building a stadium **around** <?=player:him_her()?>…”；译文：“正在对 <?=player.name?> 启动最高优先级措施，**为** <?=player:him_her()?> 建造一个体育场…”
- 首要任务“隔离玩家”被省掉；体育场“围住玩家”变成“为玩家建造”。原文“把目标关进体育场、卖票观看”的“围困”含义没了。
- 依据：对照 demon.lua:200-214 的普通版，那里的首要任务是 “containing … to prevent further damage”，本条是它的恶搞版。



## O055 | entry-03371

### C15 | entry-03371 | 存在问题

原文“the pen was rapidly **jerked away**”译为“笔**从手上滑落**”，把快速被扯开改成失手滑落，改变笔迹产生的动作。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:228`，`tactics-failed-badass.lore`。



## O056 | entry-03371

### C15 | entry-03371 | 存在问题

原文：“Blow all connectors”；译文：“关闭所有链接传送门”。

原文要求炸毁连接设施，译文变为关闭传送门，同时改变动作和对象。紧接的“break platform off the continent”提供物理连接／平台分离语境；本句没有将 connectors 指定为传送门。

证据：`D/data/lore/demon.lua:226`。状态：**confirmed，文本可证的动作和对象误译**；未据此推断地图中的具体执行脚本。



## O057 | entry-03371

### C15 | entry-03371 | 存在问题
- 原文：“**Blow** all connectors, break platform off the continent”；译文：“**关闭**所有链接**传送门**…”
- “炸毁”被弱化成“关闭”；connectors 被具体化成“传送门”，源码里没有这个依据。
- 依据：普通版 demon.lua:210 附近写着 “Blow all connectors, break platform of[f]…”，是断开平台的毁灭性指令。



## O058 | entry-03371

### C16 | entry-03371 | 存在问题

原文“**double-bladed katana**”仅译“武士刀”，丢失双刃特征。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:228`。



## O059 | entry-03371

### C16 | entry-03371 | 存在问题

原文：“spotlights”；译文：“闪光灯”。

体育场演出布置中的聚光照明被改为闪光灯，两者照明方式不同。证据：`D/data/lore/demon.lua:226`，与焰火、音响系统并列的舞台布置语境。

状态：**confirmed，对象误译**。



## O060 | entry-03371

### C16 | entry-03371 | 存在问题
- 原文：“like the pen was **rapidly jerked away** … Your badassery must have **interrupted this demon's writing**.”
- 译文：“那是笔从手上**滑落**留下的痕迹…看起来，你的霸气侧漏把这个恶魔**吓尿了**。”
- “笔被猛地扯开”变成了“滑落”；结论“你打断了它的书写”被改写成“吓尿了”。便条中断的原因，也就是玩家闯入打断，这层信息丢了。
- 依据：普通版结尾是 “You must have interrupted this demon's writing.”，本条是在它基础上的变体。



## O061 | entry-03371

### C17 | entry-03371 | 存在问题

原文对手是标作“Ninja Atamathon”的“**giant construct**”；译文仅作“**忍者王阿塔玛森**”，漏掉巨型构装体身份，并加入原文没有的“王”。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:228`；`INPUT.md` 术语子集对构装实体给出“构装体”。



## O062 | entry-03371

### C17 | entry-03371 | 存在问题

原文：“double-bladed katana”；译文：“武士刀”。

译文遗漏“双刃”的武器特征。该特征是涂鸦刻意夸张的内容，不能由普通武士刀自动表达。证据：`D/data/lore/demon.lua:228`。

状态：**confirmed，描述信息遗漏**。



## O063 | entry-03371

### C17 | entry-03371 | 存在问题
- 原文：“wielding a **double-bladed** katana and fighting a **giant construct** labelled "Ninja Atamathon."”；译文：“手里拿着武士刀，正在和“忍者王阿塔玛森”对战。”
- 丢了“双刃”和“巨型构装体”，还丢了“标着……字样”这层关系。纯语义判断。



## O064 | entry-03371

### C18 | entry-03371 | 存在问题

原文“Your badassery must have **interrupted this demon’s writing**”译为“你的霸气侧漏把这个恶魔**吓尿了**”。原文能确定的是书写被打断；译文删去这一事件并加入惊吓反应。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:228`。



## O065 | entry-03371

### C18 | entry-03371 | 存在问题

原文：“a giant construct labelled ‘Ninja Atamathon’”；译文：“‘忍者王阿塔玛森’”。

译文遗漏对手是巨大构装体这一实体描述，并新增“王”的身份。即使读者认识阿塔玛森，也不能以背景知识替代本句明示的信息。

证据：`D/data/lore/demon.lua:228`。状态：**confirmed，实体特征遗漏及身份增译**；不涉及全局专名调整。



## O066 | entry-03371

### C18 | entry-03371 | 存在问题
- 原文：“routed by **target's** overwhelming badassery”，不分性别；译文：“被**他的**霸气侧漏吓退”。
- 这里写死了男性代词。本条后文用 `<?=player:him_her()?>` 按玩家性别动态生成，所以女性角色看到的会是“他的”，指代错误。



## O067 | entry-03371

### C19 | entry-03371 | 仅建议
- 原文：“stained with **what appear to be** motorcycle tire-tracks”；译文：“被摩托车轮胎的痕迹弄脏了”。
- “看上去像”这层保留语气丢了。这是风味文本，不涉及机制，算偏好。



## O068 | entry-03371

### C19 | entry-03371 | 存在问题

原文：“like the pen was rapidly jerked away”；译文：“那是笔从手上滑落留下的痕迹”。

原文根据笔迹推测笔被猛然扯开；译文将其确定为笔从手中滑落。动作原因与证据确定程度均改变。

证据：`D/data/lore/demon.lua:228`。状态：**confirmed，动作及推测语气变化**。将末尾字母改称“最后一个字”属于本地化适配，不另计缺陷。



## O069 | entry-03371

### C20 | entry-03371 | 存在问题

原文：“must have interrupted this demon's writing”；译文：“把这个恶魔吓尿了”。

原文推断玩家的霸气打断恶魔写作；译文变成惊恐失禁，遗漏被打断的写作行为，并增加不同事件。幽默语体可以调整，但这里改变了叙述内容。

证据：`D/data/lore/demon.lua:228`。状态：**confirmed，事件替换**。



## O070 | entry-03372

### C13 | entry-03372 | 存在问题
- **短引**：
  - 原文：`... serving as obstructions and shields while their acid and our casters do their work ...`
  - 译文：`……以肉体充当屏障，令酸液和法术能够发挥作用……`
- **问题说明**：原文中并列的两个行动主体是 "their acid"（它们的酸液）与 "our casters"（我们的施法者，指后方的恶魔施法单位）；译文将实体人物主体 "our casters" 错译为抽象名词“法术”（“令酸液和法术能够发挥作用”），导致战场作战协同的主体角色发生性质改变。
- **状态**：存在问题。
- **依据与消费逻辑**：源码快照 `sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:514`。恶魔军队战术为前排依靠酸液树魔肉身阻挡敌人并喷洒强酸，掩护后方恶魔施法者进行输出。"casters" 明确指代作战单位角色，不能直接等同于法术。

---



## O071 | entry-03372

### C19 | entry-03372 | 存在问题

原文“dissolving **the ground they walk on**”译为“溶解土地”，漏掉被溶解的是敌人脚下的地面，弱化了酸液树魔攻击对象的空间关系。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:291–295`，`demon-statue-wretchling.lore`。



## O072 | entry-03372

### C20 | entry-03372 | 仅建议
- 原文：“dissolving the ground **they walk on**”；译文只有“溶解土地”，没说溶解的是敌人脚下的地面。
- 开头“极快的速度、庞大的数目以及……的皮肤，”缺少“凭借”之类的连接词，成了残句。
- 为什么只算建议：原文要点（冲锋、逐个扑杀、使敌人无助）都在，只是表达略欠完整。

---



## O073 | entry-03372

### C20 | entry-03372 | 存在问题

原文“their acid and **our casters** do their work”译为“令酸液和**法术**能够发挥作用”。己方施法者被改成法术，参与战斗的单位及所属关系丢失。证据：`sources/dlc/ashes-urhrok/tome-ashes-urhrok/data/lore/demon.lua:295`，`demon-statue-wretchling.lore`。

**读取范围与限制：**读取了冻结包的 `INPUT.md`、`entries.json`、`context.lua`、`source-access.json`，以及 `source-access.json.sections` 指定的六个 Ashes 源码单文件：`achievements/all.lua`、`birth/corrupted.lua`、`birth/doomelf.lua`、`general/grids/demon_statues.lua`、`general/objects/world-artifacts.lua`、`lore/demon.lua`；六个文件的 SHA-256 均与清单一致。按 `achievements/all.lua:87–95` 的恶魔名称，另对清单允许的 `data/general/npcs/major-demon.lua` 做了哈希校验及限定词搜索；按 `world-artifacts.lua:80,90,102` 的 `Obliterating Smash` 符号，另对允许的 `data/talents/corruptions/brutality.lua` 做了相同检查。两次搜索均未命中，未据它们形成结论。未读取引擎仓库，未读取其他报告或模型输出，未创建临时文件，未修改仓库。

**越界记录：**开始时曾对冻结包目录执行一次 `ls`，看到了若干未获准读取的文件及目录名称；没有打开其内容。addon-dev 在清单中列为源码不可用。以上仅为审核观察，不声称生产 `DONE_VERIFIED`。


## O074 | entry-03372

### C21 | entry-03372 | 存在问题

原文：“does an incredible service to our cause”；译文：“为我们的目标奉献了一切”。

原文赞扬每个参战者作出的巨大贡献；译文把贡献程度绝对化为奉献全部。前文分别说明愿意牺牲以及少数能够存活，结尾并未断言每个参战者都已付出一切。

证据：`D/data/lore/demon.lua:295` 的整段论述。状态：**confirmed，贡献程度被加强**。

实际读取范围与限制如下：

- 冻结包根目录 `B`：`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g05-20260923`。
- 读取 `B/INPUT.md`、`B/entries.json`、`B/context.lua`、`B/source-access.json`。核对 entries 恰好40条、顺序正确，原译文与 INPUT 对应；格式检查未发现占位符、模板表达式或显示标记序列差异。
- 读取以下六份 `B/sources/dlc/ashes-urhrok/tome-ashes-urhrok/` 下源码，SHA-256 均与清单完整匹配：`data/achievements/all.lua`、`data/birth/corrupted.lua`、`data/birth/doomelf.lua`、`data/general/grids/demon_statues.lua`、`data/general/objects/world-artifacts.lua`、`data/lore/demon.lua`。
- 附加快照根目录为清单指定的 `/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/ashes-urhrok`。读取并核验哈希的单文件为：
  - `tome-ashes-urhrok/superload/mod/class/Actor.lua`：由装备的 `on_obsidian_power_update`／`artifact_power_obsidian` 引入。
  - `tome-ashes-urhrok/data/talents/corruptions/brutality.lua`：由装备列出的技能类别及 `T_OBLITERATING_SMASH` 定位需要引入；未找到该技能定义。
  - `tome-ashes-urhrok/data/talents/corruptions/wrath.lua`：同一装备列出的另一技能类别；找到破墙消费代码。
  - `tome-ashes-urhrok/data/general/events/demon-statue.lua`：由雕像的 `demon_statues_list`、种类及 `demon_statue_actived` 生成／回调关系引入。
- 本体只通过 `git show` 读取 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 的以下单文件：
  - `game/modules/tome/data/damage_types.lua`：追踪 `FIRE_DRAIN`。
  - `game/modules/tome/class/interface/Combat.lua`：追踪 `combat_spellcrit` 的消费。
  - `game/engines/default/engine/World.lua`、`game/modules/tome/class/World.lua`：定位 `world:gainAchievement`。
  - `game/modules/tome/class/interface/WorldAchievements.lua`、`game/engines/default/engine/interface/WorldAchievements.lua`：沿前者明确的 require／继承和调用继续核验。
- 曾尝试同一固定提交的 `engine/World.lua`；该路径不存在，未读到内容。默认沙箱首次读取失败后，使用获准的只读执行完成读取。
- addon-dev 源码缺失，前三条仅依据冻结文本、参数及允许语境判断。DLC 目标版本适用性未核验；C02、C08 保留待确认。
- 未创建临时文件、子 agent，未修改仓库，未读取其他报告或清单外材料；无已知越界。本结果仅为独立审核观察，不宣称生产 `DONE_VERIFIED`。

