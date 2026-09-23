# 匿名源码核验与归并：40 条 / 82 项观察

你是本任务独立 REVIEWER。用户要求继续三模型实验并归并问题；本阶段依据源码核验，不参与参赛评分。参考是暂定模型裁决，非人工金标准。禁止寻找模型身份或读取来源映射、原始报告、STATE、其他实验目录。不得以多数票、重复次数、报告声称“已证实”替代证据。

唯一允许输入：本文件、同目录 INPUT.md、entries.json、context.lua、source-access.json、source-access.json 明确列出的冻结源码。先阅读INPUT统一判定规则；沿其限定调用链读取单文件。本体使用git show固定commit；DLC只能使用获准的哈希快照，不能把引擎commit套用于DLC，缺少目标版本适用证据则保留pending；无源码组件仅确认文本可证偏差。后续实验的临时文件已获用户授权，可用自己创建的任务专属临时目录；仓库只读，不创建子agent。

下方82项匿名观察按entry和文字排序，包括问题、建议及待确认。各观察C编号仅为原报告局部编号，不跨观察匹配；统一以O编号标识。保持原断言供核验但不采信。请逐项确认、否决、待确认或仅建议；同条同义缺陷合并为canonical D-ID，不同信息或机制错误拆开。注明翻译新增/沿袭上游。遇实质争议要核实双方论据和完整上下文，证据不足保留pending。缺陷边界应考虑完整界面语境，不把单词必然等同为排他机制断言；也不能因玩家猜得出或英文有同错就豁免。

同时独立检查全部40条，包括没有观察或全部观察被否决的条目，补充漏项。只依据INPUT/源码/语境，不能读取其他轮答案。

输出要求：三个Markdown表格，再补充必要解释与读取路径。
1. 恰好40行：entry-ID | 判定（OK/ISSUE/PENDING） | canonical D或P编号/简短依据。OK包括仅建议；有确认缺陷即ISSUE，即使附带pending；无确认但仍有疑点才PENDING。严格冻结顺序。
2. 确认缺陷表：D-ID（D01起） | entry-ID | 内容、归因及固定源码路径:行号/调用链证据。未决用P-ID另列，不混入D。每个D须实际核验。
3. 恰好82行：O-ID | 状态（confirmed/refuted/pending/advisory/mixed） | 命中D-ID（无则—） | 具体证据与理由。mixed须明确哪些部分confirmed、refuted、pending或advisory；不要把未命中的错误问题借用同条其他正确D。若仅有措辞问题则advisory。补充说明所有未决与主要分歧如何处理。

不要给模型排名或分数、不要修改译文，不宣称DONE_VERIFIED。列出实际读取的路径和额外单文件引入依据；未完成的机制核验如实记录。



## O001 | entry-03693

### C01 | entry-03693 | 仅建议
- **原文／译文：** “promptly swallows and eat Melinda” →“吃下了梅琳达”。
- **观察：** “promptly”（立刻）没有译出。
- **依据：** CultsDLC.lua:353。这是寄生兽模式下替换出来的对话选项，动作由 `good_meal()`（:337-344）执行：杀死 NPC，并加 1 点通用天赋点。选项本身描述的动作、对象、结果都没错，缺的只是语气副词，不影响玩家判断，所以只算建议。
- **旁证：** 同节相邻条目（Fillarel、yeek wayist）用的是“直接吃掉了”。



## O002 | entry-03693

### C01 | entry-03693 | 仅建议
- **短引**：原文 `#CRIMSON#[The parasite is hungry and promptly swallows and eat Melinda].` / 译文 `#CRIMSON#[寄生兽很饿，吃下了梅琳达]。`
- **内容与偏好说明**：原文中副词 `promptly`（迅速地/毫不犹豫地/直接）在译文中略去未直译，译文“吃下了梅琳达”虽准确表达了吞噬梅琳达的动作与叙事结局，但在对话分支语气上建议可补充“迅速/直接”（如“迅速吃下了梅琳达”），以更完整体现动作的时效紧迫感；此处不改变游戏机制与主旨信息，属措辞偏好。
- **状态**：仅建议
- **语境证据**：`CultsDLC.lua:353`，对话分支选项文本。



## O003 | entry-03693

### C01 | entry-03693 | 存在问题

原文“**promptly swallows and eat Melinda**”；译文“吃下了梅琳达”。

状态：**confirmed，时序信息遗漏**。“吃下了”保留吞食结果，但没有表达立即发生。证据为冻结文本及 `S/cults/tome-cults/overload/mod/class/CultsDLC.lua:353`：该文本作为寄生兽替换后的对话选项显示，绑定 `good_meal()`。此结论不依赖推断游戏耗时。



## O004 | entry-03693

### C01 | entry-03693 | 存在问题

原文“**promptly** swallows and eat Melinda”中的迅速动作，在“吃下了梅琳达”中消失。这是动作时序的遗漏，不影响被吃的对象。证据：`sources/dlc/cults/tome-cults/overload/mod/class/CultsDLC.lua:350–354`；该句是选择项，选择后的 `good_meal()` 执行动作。



## O005 | entry-03694

### C02 | entry-03694 | 仅建议
- **短引**：原文 `#CRIMSON#[The parasite is hungry and promptly swallows and eat Aeryn].` / 译文 `#CRIMSON#[寄生兽很饿，吃下了艾琳]。`
- **内容与偏好说明**：与 C01 同理，原文 `promptly` 未直接体现，当前译文已达意且信息无损，建议可酌情体现“迅速/立刻”，属措辞偏好。
- **状态**：仅建议
- **语境证据**：`CultsDLC.lua:358`，对话分支选项文本。



## O006 | entry-03694

### C02 | entry-03694 | 仅建议
- 与 C01 相同，“promptly”没有译出。
- **依据：** CultsDLC.lua:358，`good_meal(self.chats.welcome.answers[3].action)`。结果信息没有损失。



## O007 | entry-03694

### C02 | entry-03694 | 存在问题

与 C01 相同的时序遗漏分别发生在艾琳这一条：“**promptly** swallows and eat Aeryn”译为“吃下了艾琳”。证据：同一冻结源码 `CultsDLC.lua:355–359`。



## O008 | entry-03694

### C02 | entry-03694 | 存在问题

原文“**promptly swallows and eat Aeryn**”；译文“吃下了艾琳”。

状态：**confirmed，时序信息遗漏**。与上一条相同，立即吞食这一叙事信息没有保留。证据：`S/cults/tome-cults/overload/mod/class/CultsDLC.lua:358`，对应艾琳对话替换选项。



## O009 | entry-03697

### C03 | entry-03697 | 存在问题

“Protector Myssil **of Zigur**”译成“守护者米歇尔”，遗漏来信人的伊格所属信息。信件正文提到“伊格附近”，但不等于补回其身份。证据：`sources/dlc/cults/tome-cults/superload/mod/class/Game.lua:59–69`；整段作为信件弹窗显示。



## O010 | entry-03697

### C03 | entry-03697 | 存在问题

原文“**Protector Myssil of Zigur**”；译文“守护者米歇尔”。

状态：**confirmed，人物所属信息遗漏**。后文的“伊格附近”描述废墟位置，并未表达写信者来自或属于伊格。证据：`S/cults/tome-cults/superload/mod/class/Game.lua:59`；整封信由 `simpleLongPopup` 显示，`%s` 在第69行消费为玩家名字。



## O011 | entry-03697

### C03 | entry-03697 | 存在问题
- **原文／译文：** “a letter from Protector Myssil of Zigur” →“一份来自守护者米歇尔的信”。
- **问题：** “of Zigur”（伊格的）被整段删掉，寄信人的所属地丢了。
- **依据：** Game.lua:59-69，这是 `Dialog:simpleLongPopup` 弹出的信件正文。标题“Urgent affair in Zigur”虽然提到了伊格，但正文开头原本交代“来自伊格的守护者 Myssil”，这是身份和所属关系信息，不能靠标题让玩家自己推断。
- **状态：** 已证实（语境证据）。
- **其余部分核对无误：** %s（`p.name`）、`#{italic}#`、结尾换行都保留；Ziguranth 译“伊格兰斯”、Zigur 译“伊格”，都符合术语快照里的地点／教团区分。



## O012 | entry-03697

### C03 | entry-03697 | 存在问题
- **短引**：原文 `a letter from Protector Myssil of Zigur:` / 译文 `一份来自守护者米歇尔的信：`
- **问题具体内容**：遗漏关键所属地名修饰语 `of Zigur`（伊格的）。米歇尔作为反魔阵营与伊格据点的领袖，其完整头衔与据点指称在信首介绍中至关重要；译文完全漏掉了“伊格的”这一地点/阵营属性。
- **状态**：存在问题
- **源码依据**：`dlc/cults/tome-cults/superload/mod/class/Game.lua:59`（DLC公开快照，源码未固定），`Dialog:simpleLongPopup` 触发克罗格营救任务弹窗，信件开头为身份与任务背景交待。



## O013 | entry-03697

### C04 | entry-03697 | 仅建议
- **原文／译文：** “From what the scouts can tell they were taken by…” →“侦察员看见他们被……带走”。
- **观察：** 原文是“据侦察员判断”的推断语气，译文变成了亲眼所见，确定性略有抬高。
- **为什么只算建议：** “被死灵法师带走”这个事实主张本身没错，后半句的“可能”也保留了，叙事信息没有实质改变。



## O014 | entry-03697

### C04 | entry-03697 | 存在问题

“**From what the scouts can tell**”是侦察员据所得情报作出的判断；“侦察员**看见**他们被……带走”改成了亲眼目睹。后半句的“可能”只限定实验目的，未消除这处证据性质变化。证据：同一 `Game.lua:62–63`。



## O015 | entry-03697

### C04 | entry-03697 | 存在问题

原文“**From what the scouts can tell**”；译文“侦察员看见”。

状态：**confirmed，信息来源被强化**。原文仅归因于侦察员掌握或判断出的情报，没有说明他们亲眼看见绑架过程；译文增加了目击事实。证据：同文件第63行，属于弹窗信件正文。



## O016 | entry-03697

### C04 | entry-03697 | 存在问题
- **短引**：原文 `show the necromancers filth the True Wrath of the Ziguranth!` / 译文 `并让死灵法师见识一下伊格兰斯的愤怒！`
- **问题具体内容**：原文中的名词同位语/定语 `filth`（这些污秽之徒/肮脏的败类）被漏译；此外，修饰教团之怒的定语 `True`（真正的愤怒）亦被漏译，弱化了反魔护卫长对奥术/死灵邪祟的极端憎恶情绪与文本强烈语气。
- **状态**：存在问题
- **源码依据**：`dlc/cults/tome-cults/superload/mod/class/Game.lua:66`（DLC公开快照，源码未固定）。



## O017 | entry-03697

### C05 | entry-03697 | 仅建议
- **原文／译文：** “grave news”→“令人震惊的消息”；“show the necromancers filth the True Wrath of the Ziguranth”→“让死灵法师见识一下伊格兰斯的愤怒”。
- **观察：** “grave”的意思是“严重”，不是“震惊”；贬称“filth”和强调词“True”都没译出。
- **为什么只算建议：** 这些都是语气和修辞层面的差别，行动对象和行动要求（解救、惩戒死灵法师）完整。



## O018 | entry-03698

### C05 | entry-03698 | 存在问题

原文说功能需要在服务器存放数据（“**it needs to store things**”）；译文说“这项功能需要**你**在服务器上存储数据”，把存储动作归给玩家，可能使注册、绑定之外又显得需要玩家手动存储。此项是原译直接可证的主体变化；`items-vault` 源码缺失，未据此断言实际操作机制。语境证据：冻结 `INPUT.md` 的本条，以及 `context.lua:138–145`。



## O019 | entry-03699

### C05 | entry-03699 | 待确认

原文“**sent to the Item’s Vault**”；译文“上传到共享仓库”。

状态：**pending**。“上传”限定为网络传送，而许可语境中同一组件同时存在在线与离线存入提示：`context.lua:167`、`:170`。尚不知道本条是否仅在在线存入后出现，还是两条路径共用。

缺失证据：`ItemsVaultDLC.lua` 中本字符串的调用位置及在线／离线分支关系。`items-vault` 已列为源码不可用；不能据此确认误译。



## O020 | entry-03699

### C06 | entry-03699 | 待确认

原文仅称物品已“**sent to** the Item’s Vault”，译文称已“**上传到**共享仓库”。同一允许的相邻语境含在线和离线传输提示（`context.lua:160–169`），但缺少 `ItemsVaultDLC.lua` 的实际调用位置，无法确认这条通用提示是否也会在离线路径显示。所缺证据是该提示的触发分支；因此不判为已证实错误。



## O021 | entry-03699

### C06 | entry-03699 | 待确认
- **原文／译文：** “This item has been sent to the Item's Vault.”→“已被上传到共享仓库”。
- **疑点：** 同节（ItemsVaultDLC.lua）同时有“online item's vault”和“offline item's vault”两套传输日志（见 context.lua 的同节 03700、03701）。如果这句提示也会出现在离线仓库的情形，“上传”（隐含上传到服务器）就不准确；原文“sent”是中性的。
- **缺的证据：** items-vault 列在 unavailable_components 中，看不到这句的调用点，也就无法确认它是否只在在线模式下出现。



## O022 | entry-03704

### C05 | entry-03704 | 仅建议
- **短引**：原文 `Once Upon A Time, In the West...` / 译文 `很久很久以前，在西方……`
- **内容与偏好说明**：该成就名与同文件中相邻的一组成就（A Fistful of Gold、For a Few Gold More、The Good, The Bad, and The Yeti）共同致敬著名导演莱昂内的经典西部镖客电影。原文直接化用电影名 *Once Upon a Time in the West*（中文通译《西部往事》）。当前译文采用字面直译在文意上完全成立且通顺，但若能考虑电影片名双关译作《西部往事……》会更具双关趣味；这仅属文化引用风格偏好，字面直译不计作缺陷。
- **状态**：仅建议
- **语境证据**：`dlc/orcs/tome-orcs/data/achievements/special.lua:136`（DLC公开快照，源码未固定）。



## O023 | entry-03714

### C06 | entry-03714 | 仅建议
- **短引**：原文 `increase all their damage for a few turns.` / 译文 `让他们能在几回合内增加伤害。`
- **内容与偏好说明**：原文 `all their damage` 强调提升“所有造成的伤害”（全类型伤害加成），译文略化为“增加伤害”。在种族天赋特性描述中，虽然语义可大致理解，但建议补充“所有”，更精确地对齐游戏底层机制。
- **状态**：仅建议
- **源码依据**：`dlc/orcs/tome-orcs/data/birth/races/orc.lua:115` 与 `[ActorTalents.T_ORC_FURY]` 效果消费逻辑。



## O024 | entry-03714

### C06 | entry-03714 | 存在问题

原文“**increase all their damage**”；译文“增加伤害”。

状态：**confirmed，作用范围信息遗漏**。译文保留增伤，却未明确原文强调的全部伤害范围。

证据：DLC 种族描述 `S/orcs/tome-orcs/data/birth/races/orc.lua:115`，第125行授予 `T_ORC_FURY`。固定本体 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 中：

- `game/modules/tome/data/talents/misc/races.lua:731`：施加 `EFF_ORC_FURY`，持续3回合。
- `game/modules/tome/data/timed_effects/mental.lua:1999`、`:2007`：效果说明明确全部伤害，激活时写入 `inc_damage` 的 `all` 增益。

这是原文范围信息的遗漏；不将本体 commit 视为 DLC 的版本固定依据。



## O025 | entry-03719

### C07 | entry-03719 | 仅建议
- **原文／译文：** “- special whitehoof talents: dead hide, lifeless rush, essence drain” →“- 特殊白蹄天赋：亡者之皮，无生突袭，吸取精华。”
- **观察：** 译文末尾加了句号。同一列表里的其他项（context.lua 同节“- 沉默抗性”“- 流血免疫”等）都不带句号，只是格式不统一，不影响显示或信息。
- **未能核对：** 三个天赋名与天赋定义里的正式中文名是否一致。术语快照没有收录这三项，也不能读取其他翻译文件，所以没有列为 claim。



## O026 | entry-03728

### C08 | entry-03728 | 仅建议
- **原文／译文：** “…#GOLD#蒸汽科技/物理#LAST#, #GOLD#蒸汽科技/化学#LAST#和两项…”
- **观察：** 中文句子里混用了半角逗号加空格，属于排版偏好。
- **已核对无误：** 占位符 %s（npc.name）和颜色标记都完整；aaf.lua:25-28/35 确实学习 steamtech/physics、steamtech/chemistry 两个技能类别，外加 T_SMITH、T_THERAPEUTICS 两个天赋，与“两项入门制造技能”一致；术语 steamtech、physics、chemistry 都匹配。



## O027 | entry-03729

### C07 | entry-03729 | 存在问题

“metallic items into **lumps of metal**”译为“金属物品转化为**铁块**”，把不限定金属种类的产物限定成铁。相关物品说明又称其为“lumps of ore”。证据：`sources/dlc/orcs/tome-orcs/data/chats/aaf.lua:45–49`，以及其 `:55` 加载的哈希固定文件 `tome-orcs/data/general/objects/quest-artifacts.lua:27–30`。



## O028 | entry-03729

### C07 | entry-03729 | 存在问题

原文“**lumps of metal**”；译文“铁块”。

状态：**confirmed，材料范围被缩窄**。金属不限于铁，译文将产物指定成了某一种金属。文本证据：`S/orcs/tome-orcs/data/chats/aaf.lua:47`。

快照辅助证据：`A/tome-orcs/superload/mod/class/Actor.lua:299` 的 `transmoInven` 按物品材质等级构造材料 ID，并调用 `collectIngredient`，没有在这个分支把所有金属固定成铁。这里不凭材料 ID 推断各等级具体名称。



## O029 | entry-03729

### C07 | entry-03729 | 存在问题
- **短引**：原文 `which are used to craft tinkers.` / 译文 `（整句漏译）`
- **问题具体内容**：严重漏译核心功能目的定语从句。原文解释将物品分解为金属块和药草的目的即为“这些材料用于制造蒸汽配件（tinkers）”，译文在“将纹身转化为植物”之后戛然而止，完全丢失了提取材料是为了制作配件这一最关键的引导性信息。
- **状态**：存在问题
- **源码依据**：`dlc/orcs/tome-orcs/data/chats/aaf.lua:42`（DLC公开快照，源码未固定），对话叙述便携提取仪（APE）的核心作用。



## O030 | entry-03729

### C08 | entry-03729 | 存在问题

“infusions into **herbs**”译为“纹身转化为**植物**”，遗漏产物是草药这一材料类别。证据：`aaf.lua:46–47`；这是原译直接可证的类别信息损失。



## O031 | entry-03729

### C08 | entry-03729 | 存在问题

原文“**infusions into herbs**”；译文“将纹身转化为植物”。

状态：**confirmed，产物类别信息丢失**。“植物”没有保留 herbs 所指的草药类别。证据：`S/orcs/tome-orcs/data/chats/aaf.lua:47`；这是物品处理结果说明，并非泛指自然植物的叙事。



## O032 | entry-03729

### C08 | entry-03729 | 存在问题
- **短引**：原文 `when you destroy items.` / 译文 `（从句漏译）`
- **问题具体内容**：漏译关键条件状语 `when you destroy items`（在摧毁/分解物品时）。原文指明玩家必须在摧毁物品的特定场景下二选一（便携提取仪或转化之盒），译文漏译后变成了“你可以选择使用它或者转化之盒”，丢失了该选择生效的前提条件。
- **状态**：存在问题
- **源码依据**：`dlc/orcs/tome-orcs/data/chats/aaf.lua:44`（DLC公开快照，源码未固定）。



## O033 | entry-03729

### C09 | entry-03729 | 存在问题

原文“**which are used to craft tinkers**”；译文无对应内容。

状态：**confirmed，用途信息遗漏**。材料与制造蒸汽工具的关系完全消失，玩家得不到收集这些产物的用途说明。证据：`S/orcs/tome-orcs/data/chats/aaf.lua:47`。

快照中的 `A/tome-orcs/overload/mod/class/interface/PartyTinker.lua:81` 也显示 `canMakeTinker` 会检查配方所需材料；此处仅辅助解释用途，不扩大到具体配方结论。



## O034 | entry-03729

### C09 | entry-03729 | 存在问题

原文说明这些材料“**are used to craft tinkers**”，译文在材料转换后结束句子，遗漏制造蒸汽工具的用途。证据：`aaf.lua:46–49`。



## O035 | entry-03729

### C09 | entry-03729 | 存在问题
- **原文／译文：** “break down metallic items into lumps of metal” →“将金属物品转化为铁块”。
- **问题：** 原文是泛指的“金属块”，译文缩成了“铁”。
- **源码依据：** 提取仪的熔炼逻辑在 orcs 的 superload/mod/class/Actor.lua:299-302：`if o.metallic and o.material_level then local id = "LUMP_ORE"..o.material_level`。产出的矿块按物品材质等级分档，不是固定的铁。
- **状态：** 已证实（DLC 快照，来源未固定）。



## O036 | entry-03729

### C09 | entry-03729 | 存在问题
- **短引**：原文 `metallic items into lumps of metal and infusions into herbs` / 译文 `将金属物品转化为铁块，将纹身转化为植物`
- **问题具体内容**：术语与词义严重不准。
  1. `herbs` 误译为泛化的“植物”（实为用于调配注射药剂的“药草/草药”）；
  2. `lumps of metal` 错误窄化为“铁块”。在游戏机制中，提取仪分解金属物品产出的是对应材质阶级的各级金属块（如钢铁、矮人钢、沃瑞钽等），绝不仅限于生铁块。
- **状态**：存在问题
- **源码依据**：`dlc/orcs/tome-orcs/data/chats/aaf.lua:42` 以及 `dlc/orcs/tome-orcs/data/general/objects/quest-artifacts.lua:28-30` APE 描述。



## O037 | entry-03729

### C10 | entry-03729 | 存在问题

原文“**when you destroy items**”；译文“你可以选择使用它或者转化之盒”。

状态：**confirmed，操作适用情境遗漏**。原文限定的是销毁物品时选择处理工具，译文没有交代这个选择针对什么操作。证据：`S/orcs/tome-orcs/data/chats/aaf.lua:49`，位于加粗的操作说明内。



## O038 | entry-03729

### C10 | entry-03729 | 存在问题

原文是在“**no items to destroy**”时使用提取仪来选默认工具；译文限定为“**在里面没有物品**时”，未涵盖脚下仍有待处理物品的情况。实际 `use_power` 先检查背包中标记待处理的物品，再检查脚下物品；两处都为空才进入默认设置弹窗。证据：`aaf.lua:49–55` 所引入的 `tome-orcs/data/general/objects/quest-artifacts.lua:41–60`。



## O039 | entry-03729

### C10 | entry-03729 | 存在问题
- **原文／译文：** “…and infusions into herbs which are used to craft tinkers.” →“将纹身转化为植物。”
- **问题：** 用途从句“which are used to craft tinkers”（用于制造蒸汽配件）整句漏译，玩家看不到这些产物是做什么用的。
- **依据：** quest-artifacts.lua:28-29 的 APE 描述也写着“lumps of ore to server for the creation of tinkers”；Actor.lua:304-309 显示，熔炼纹身（infusion）后收集的是 `HERBS` 材料。
- **状态：** 已证实。



## O040 | entry-03729

### C10 | entry-03729 | 存在问题
- **短引**：原文 `You can choose the default one by using it with no items to destroy.` / 译文 `在里面没有物品时使用它则设置为默认使用。`
- **问题具体内容**：机制理解错误导致误导性翻译。便携提取仪（APE）是背包中的可使用任务道具（并非带内部格子的容器），其底层逻辑是检测当前背包或地面是否有待分解物品：若背包和地面均无物品，则弹出确认框将 APE 设为默认转化工具。译文“在里面没有物品时使用它”让玩家误以为该道具内部有储物空间且需要先清空内部，造成操作认知偏差。
- **状态**：存在问题
- **源码依据**：`dlc/orcs/tome-orcs/data/chats/aaf.lua:44`；额外引入源码 `dlc/orcs/tome-orcs/data/general/objects/quest-artifacts.lua:45-56` 的 `use` 逻辑：`if nb <= 0 then local floor = ... if floor == 0 then yesnoPopup(_t"Make the Automated Portable Extractor the default item's destroyer?")`。



## O041 | entry-03729

### C11 | entry-03729 | 存在问题

原文“**You can choose the default one by using it**”；译文“使用它则设置为默认使用”。

状态：**confirmed，选择行为被写成自动结果**。原文说使用后可以选择默认工具；译文承诺使用即完成设置，省去了选择这一操作。证据为冻结文本及 `S/orcs/tome-orcs/data/chats/aaf.lua:49`。具体运行条件另列 C12。



## O042 | entry-03729

### C11 | entry-03729 | 存在问题
- **原文／译文：** “You will have to choose to use it or the Transmogrification Chest when you destroy items.” →“你可以选择使用它或者转化之盒。”
- **问题：** “when you destroy items”（在销毁物品时）这个适用场合被删掉，读者不知道这个选择是针对什么的；“will have to”（需要做出选择）也被弱化成“可以选择”。
- **依据：** quest-artifacts.lua:33-36 显示 APE 自带 `has_transmo`；:54-57 显示同时有两个销毁来源时（`has_transmo >= 2`）才弹出默认销毁器的选择。
- **状态：** 已证实。



## O043 | entry-03729

### C12 | entry-03729 | 存在问题
- **原文／译文：** “You can choose the default one by using it with no items to destroy.” →“在里面没有物品时使用它则设置为默认使用。”
- **问题：** 译文把条件缩成了“盒子里没有物品”。
- **源码依据：** quest-artifacts.lua:45-60 的使用逻辑要求两个条件同时满足：背包里没有待熔物品（`nb <= 0`），并且脚下地面也没有物品（`floor == 0`），才会进入“设为默认销毁器”的弹窗。如果地面有物品，:62 会改为询问是否熔炼地面物品。原文“no items to destroy”覆盖了这两处。按译文操作的玩家，盒子是空的但脚下有物品时，会得到与译文不符的结果。
- **状态：** 已证实（DLC 快照，来源未固定）。



## O044 | entry-03729

### C12 | entry-03729 | 待确认

原文“**with no items to destroy**”；译文“在里面没有物品时”。

状态：**pending，目标版本中的条件适用性未固定**。

允许快照内已证事实：`A/tome-orcs/data/general/objects/quest-artifacts.lua:43` 的 `use_power.use` 先统计背包内标记待处理的物品；数量为零后，第52行还检查脚下物品。只有地面也为空、且具备多个处理工具时，第55行才弹出确认框；第56行在确认回调中设置默认工具。有地面物品时，第62行询问是否熔解它们。

因此，该快照中的“里面没有物品”不足以保证进入默认工具选择。缺失的是此 DLC 快照与目标版本的对应证据；不能将这项机制差异直接提升为目标版本已确认缺陷。上游英文也未详述多工具前提，这部分不能归为翻译新增。



## O045 | entry-03729

### C13 | entry-03729 | 仅建议
- “herbs”译作“植物”，“草药”更贴切。产物身份在 C10 已经列为问题，这里只是用词偏好。
- infusions 译“纹身”符合术语快照（infusions 对应“纹身”，existing），不算问题。



## O046 | entry-03730

### C11 | entry-03730 | 存在问题

原文是一串钥匙中“**one**”把钥匙刻有 `DESTRUCTICUS`；“交给你一串钥匙，**上面**写着‘毁灭号’”把刻字归到整串钥匙，失去“其中一把”的所属关系。证据：`sources/dlc/orcs/tome-orcs/data/chats/destructicus-lead.lua:20–23`。



## O047 | entry-03730

### C11 | entry-03730 | 存在问题
- **短引**：原文 `You should probably head there right away!*#WHITE#` / 译文 `你应该马上过去*#WHITE#`
- **问题具体内容**：句末标点符号丢失。原文以感叹号 `right away!` 结尾，译文在闭合星号与颜色标签前未加任何标点符号（漏译感叹号 `！`），导致叙事对话句式残缺。
- **状态**：存在问题
- **语境证据**：`dlc/orcs/tome-orcs/data/chats/destructicus-lead.lua:22`（DLC公开快照，源码未固定）。



## O048 | entry-03730

### C12 | entry-03730 | 存在问题

“**eagerly waiting**”描述迫切期待见面；“**焦急地等待**”加入了忧虑情绪。两种等待状态不同，属于人物状态的改变。证据：同一 `destructicus-lead.lua:21`。



## O049 | entry-03730

### C12 | entry-03730 | 存在问题
- **短引**：原文 `Several loyal Orcs are eagerly waiting ... The word 'DESTRUCTICUS' is etched into one.*` / 译文 `数名忠诚的兽人在宫殿外焦急地等待着你；其中一名兽人走上前，交给你一串钥匙，上面写着“毁灭号”。*`
- **问题具体内容**：
  1. 原文 `eagerly waiting`（热切地/迫不及待地等待）被误译为“焦急地等待”（焦虑担忧），扭曲了兽人士兵急于向酋长展示缴获巨炮钥匙的兴奋与忠诚态度；
  2. 原文 `etched into one` 明确指出字样是“刻在其中一把钥匙上”，译文概括为“交给你一串钥匙，上面写着“毁灭号””，丢失了刻在特定钥匙上的对象所属与雕刻事实。
- **状态**：存在问题
- **语境证据**：`dlc/orcs/tome-orcs/data/chats/destructicus-lead.lua:20`（DLC公开快照，源码未固定）。



## O050 | entry-03730

### C13 | entry-03730 | 存在问题

原文“**etched into one**”；译文“一串钥匙，上面写着‘毁灭号’”。

状态：**confirmed，刻字所属范围遗漏**。原文明确刻在其中一把钥匙上，译文没有保留这一限定。证据：`S/orcs/tome-orcs/data/chats/destructicus-lead.lua:21` 的 `welcome` 对话正文。



## O051 | entry-03730

### C14 | entry-03730 | 仅建议
- **原文／译文：** “Several loyal Orcs are eagerly waiting” →“焦急地等待着你”。
- **观察：** “eagerly”偏向“热切、迫不及待”，“焦急”带有担忧色彩，情绪略有偏移。“焦急地等待”在中文里也常用来表达急切，所以没有列为错误。



## O052 | entry-03730

### C14 | entry-03730 | 存在问题

原文“**just south of Kruk Pride**”；译文“克鲁克部落南边”。

状态：**confirmed，地点邻近信息遗漏**。南方方向保留，但紧邻南侧的定位信息丢失。证据：同文件第22行的前往地点说明。这是轻微的信息遗漏，不只是措辞偏好。



## O053 | entry-03730

### C15 | entry-03730 | 仅建议
- 原文说“'DESTRUCTICUS' is etched into one”（刻在其中一把钥匙上），译文“上面写着”没有交代是哪一把，“etched”（刻）也变成了“写”。
- 末句“You should probably head there right away!”译作“你应该马上过去*”，丢了“probably”和感叹号。
- **依据：** destructicus-lead.lua:21-23。这些都不改变剧情信息或玩家操作（下一步只有“Lead the way.”一个选项，:25-27），所以只算建议。术语“毁灭号”“克鲁克部落”一致，@playername@ 保留。



## O054 | entry-03731

### C13 | entry-03731 | 存在问题

“its base **slightly rotating underneath you**”译成“它的基座开始运转”，遗漏底座在玩家身下轻微旋转这一具体动作。证据：`sources/dlc/orcs/tome-orcs/data/chats/destructicus.lua:36–40`。



## O055 | entry-03731

### C13 | entry-03731 | 存在问题
- **短引**：原文 `whirrs to life, its base slightly rotating underneath you.` / 译文 `启动了它的生命，它的基座开始运转。`
- **问题具体内容**：机器描写严重机翻化与细节遗失。
  1. `whirrs to life` 是英语中描述机械“发出嗡鸣声运转/启动”的常见习语，被生硬直译为“启动了它的生命”；
  2. `its base slightly rotating underneath you`（其底座在你身下微微旋转）被笼统译为“它的基座开始运转”，丢失了“在你身下”的位置关系与“微旋调整”的动作细节。
- **状态**：存在问题
- **语境证据**：`dlc/orcs/tome-orcs/data/chats/destructicus.lua:42`（DLC公开快照，源码未固定）。



## O056 | entry-03731

### C14 | entry-03731 | 存在问题

面板“**slides in front of you**”表示滑到玩家面前；“**从你前方滑过**”表示从面前经过，改变了面板最终所在位置。后续面板供玩家观看、选择目标。证据：`destructicus.lua:36–53`。



## O057 | entry-03731

### C14 | entry-03731 | 存在问题
- **短引**：原文 `A strange beaded panel slides in front of you` / 译文 `一块奇怪的珍珠板从你前方滑过`
- **问题具体内容**：空间方位与显示设备描述错误。
  1. `slides in front of you` 是指操作台面板滑动移至玩家面前就位（以便后续观察锁定目标），误译为“从你前方滑过”（滑走/掠过），造成动作与后续使用逻辑冲突；
  2. `beaded panel` 结合后文的电磁推拉针阵成像机制，指珠状/凸点针阵式显示屏，误译为“珍珠板”（像珍珠饰品板）。
- **状态**：存在问题
- **语境证据**：`dlc/orcs/tome-orcs/data/chats/destructicus.lua:42`（DLC公开快照，源码未固定）。



## O058 | entry-03731

### C15 | entry-03731 | 存在问题

原文“**whirrs to life**”；译文“启动了它的生命”。

状态：**confirmed，动作语义误译**。原文描述机器伴随运转声启动，译文把惯用表达中的 life 当作被启动的“生命”，且未保留声音信息。证据：`S/orcs/tome-orcs/data/chats/destructicus.lua:37`；此前第30行已明确对象是武器装置。



## O059 | entry-03731

### C15 | entry-03731 | 存在问题

显示轮廓的针会“**pushing out and pulling back**”；译文只写“针伸了出来，被电磁力量控制”，遗漏缩回的运动，损失成像方式的一半信息。证据：`destructicus.lua:37`。



## O060 | entry-03731

### C15 | entry-03731 | 存在问题
- **短引**：原文 `pins pushing out and pulling back by magnetic force` / 译文 `针伸了出来，被电磁力量控制`
- **问题具体内容**：关键机械动作漏译。针阵显示屏的原理是通过电磁力推起和拉回（pushing out and pulling back）细针来构成三维轮廓，译文仅译出“针伸了出来”，完全漏译了“回缩/拉回”（pulling back），破坏了动态针阵成像的完整运作描写。
- **状态**：存在问题
- **语境证据**：`dlc/orcs/tome-orcs/data/chats/destructicus.lua:42`（DLC公开快照，源码未固定）。



## O061 | entry-03731

### C16 | entry-03731 | 存在问题

原文“**its base slightly rotating underneath you**”；译文“它的基座开始运转”。

状态：**confirmed，具体动作与空间关系遗漏**。原文包含脚下基座轻微旋转；“开始运转”仅表示工作状态，未表达旋转、幅度及位于玩家下方。证据：同文件第37行，`welcome2` 正文。



## O062 | entry-03731

### C16 | entry-03731 | 存在问题
- **原文／译文：** “A strange beaded panel slides in front of you, … to display the outline of an airship” →“一块奇怪的珍珠板从你前方滑过”。
- **问题：** “slides in front of you”是面板滑到你面前停住；“从你前方滑过”是经过后离开。这与后文面板一直显示目标相矛盾，动作语义错误。
- **依据：** destructicus.lua:37 及后续 :44-50，“The beaded panel is suddenly awash with colors…”说明面板一直在玩家面前。
- **状态：** 已证实（语境证据）。



## O063 | entry-03731

### C17 | entry-03731 | 仅建议
以下几处是措辞或细节损失，都不影响剧情理解和后续选择，所以只算建议：
- “whirrs to life”译作“启动了它的生命”，有翻译腔。
- “its base slightly rotating underneath you”译作“基座开始运转”，丢了“微微”和“在你身下”。
- “beaded”译作“珍珠”，更贴切的是“串珠／珠点”。
- “pins pushing out and pulling back”只译了“伸出”，漏了“缩回”。
- “magnetic force”译作“电磁力量”。

标记核对：`#{bold}#…#{normal}#`、`#{italic}#…#{normal}#` 都完整；“裂天者 毁灭号”符合术语备注。



## O064 | entry-03731

### C17 | entry-03731 | 存在问题

原文“**a strange beaded panel**”；译文“一块奇怪的珍珠板”。

状态：**confirmed，构造被误作材质**。beaded 描述珠状或颗粒状构造，不指定珍珠材质；后续同句明确是磁力驱动的显示针形成图像。证据：同文件第37行，不需要外推装置的真实制造材料。



## O065 | entry-03731

### C18 | entry-03731 | 存在问题

原文“**slides in front of you**”；译文“从你前方滑过”。

状态：**confirmed，移动关系改变**。语境是面板滑至玩家面前供其查看，译文写成从面前经过。后续第46行继续显示面板上的观察画面，支持其作为面前显示设备的语境。



## O066 | entry-03731

### C19 | entry-03731 | 存在问题

原文“**pins pushing out and pulling back**”；译文“针伸了出来”。

状态：**confirmed，显示动作遗漏**。原文明确伸出与回缩共同形成图像；译文只剩伸出，后接“被电磁力量控制”也没有表达回缩。证据：同文件第37行。



## O067 | entry-03732

### C16 | entry-03732 | 存在问题

“Steam Giant **families** huddle and weep”译为“蒸汽巨人们拥挤而哭泣”，遗漏他们是家庭成员这一叙事情境。证据：`destructicus.lua:43–48`。



## O068 | entry-03732

### C16 | entry-03732 | 存在问题
- **短引**：原文 `flying in the air near nothing of importance.` / 译文 `在空中无害地飞舞。`
- **问题具体内容**：严重错译与信息替换。原文 `near nothing of importance` 指该火焰小鬼在一片无关紧要的空域飞行（周围没有任何重要目标），译者误将后一句的 `harmless`（以最无害的方式炫耀力量）提前捏造并替换成了“无害地飞舞”，导致原文关于目标所处空旷环境的事实信息完全丢失。
- **状态**：存在问题
- **语境证据**：`dlc/orcs/tome-orcs/data/chats/destructicus.lua:54`（DLC公开快照，源码未固定）。



## O069 | entry-03732

### C17 | entry-03732 | 存在问题

“a few **crew members**”译成“一些成员”，遗漏这些往返船长室与引擎室的人是船员。证据：`destructicus.lua:46`。



## O070 | entry-03732

### C17 | entry-03732 | 存在问题
- **短引**：原文 `a few crew members hurrying between the captain's quarters and the engine room` / 译文 `你看见一些成员匆忙走过船长室和引擎室`
- **问题具体内容**：身份与动作关系描述失真。
  1. `crew members` 指“船员”，被模糊译为“成员”；
  2. `hurrying between A and B` 指“在船长室与轮机室之间匆忙奔波往返”，被错误理解为“走过船长室和引擎室”，改变了船员在飞船关键舱室间来回调度的动作关系。
- **状态**：存在问题
- **语境证据**：`dlc/orcs/tome-orcs/data/chats/destructicus.lua:50`（DLC公开快照，源码未固定）。



## O071 | entry-03732

### C18 | entry-03732 | 存在问题

火焰小鬼是在空中飞行且“**near nothing of importance**”；“在空中**无害地**飞舞”遗漏周围没有重要目标这一空间事实，并把“附近无重要物”改成“小鬼无害”。这关系到射击该目标的附带影响。证据：`destructicus.lua:48–53`；下一选项分别指向飞船和小鬼。



## O072 | entry-03732

### C18 | entry-03732 | 存在问题
- **原文／译文：** “a very lost and very confused Fire Imp, flying in the air near nothing of importance” →“在空中无害地飞舞”。
- **问题：** “near nothing of importance”（附近没有任何重要目标）被换成了“无害地”，位置信息丢失，主语属性也变了。原文紧接着说“Firing on it would have little effect whatsoever”，理由正是它附近空无一物；译文的因果依据因此偏移。
- **状态：** 已证实（destructicus.lua:50 的语境）。



## O073 | entry-03732

### C18 | entry-03732 | 存在问题
- **短引**：原文 `at you.\n \nThis airship appears` / 译文 `看向你。\n飞船似乎正在疏散`
- **问题具体内容**：段落结构丢失。英文原文在第2段（舱内众生相细节描写）与第3段（玩家的战略定性与灭族按钮抉择）之间设计了空行分割（`\n \n`）。译文仅以单个换行相连，导致第2段与第3段在界面排版中紧密粘连，丢失了文本原有的叙事停顿与视觉层次结构。
- **状态**：存在问题
- **语境证据**：`dlc/orcs/tome-orcs/data/chats/destructicus.lua:50-52`（DLC公开快照，源码未固定）。

---



## O074 | entry-03732

### C19 | entry-03732 | 存在问题
- **原文／译文：** “Steam Giant families huddle and weep” →“蒸汽巨人们拥挤而哭泣”。
- **问题：** “families”没有译出。这一段描写的是撤离难民（紧接着是“Atmos Tribe 的残余”），“一家一家的蒸汽巨人”这一平民身份信息丢失；“huddle”（挤成一团）译作“拥挤”，也偏离了原意。
- **状态：** 已证实（destructicus.lua:46 的语境）。



## O075 | entry-03732

### C20 | entry-03732 | 存在问题

原文“**The beaded panel**”；译文“珍珠面板”。

状态：**confirmed，构造被误作材质**。这是上一条叙事中的同一显示面板，仍把 beaded 无依据地具体化为珍珠。证据：`S/orcs/tome-orcs/data/chats/destructicus.lua:46`，并由第37行的磁力显示针说明提供前文语境。



## O076 | entry-03732

### C20 | entry-03732 | 存在问题
- **原文／译文：** “a few crew members hurrying between the captain's quarters and the engine room” →“一些成员匆忙走过船长室和引擎室”。
- **问题：**
  - “crew members”（船员）被泛化成“成员”，身份丢失，容易和前文的难民混淆。
  - “between A and B”（在两处之间往返奔走）被改成“走过”两个房间，行动路径变了。
- **状态：** 已证实（destructicus.lua:46 的语境）。



## O077 | entry-03732

### C21 | entry-03732 | 仅建议
以下几处不改变叙事信息，所以只算建议：
- 原文第 2 段与第 3 段之间有空行（源码是“ \n”行），译文中两段直接相连。只是少了一个段落空隔，不导致错误显示或信息结构丢失。
- 小鬼用了人称代词“他”，同文件其他段落用“它”。
- “The view pans around the cabin”译作“视角切换到船舱”，“pans around”（环视）的意思弱化了。

---



## O078 | entry-03732

### C21 | entry-03732 | 存在问题

原文“**Steam Giant families huddle and weep**”；译文“蒸汽巨人们拥挤而哭泣”。

状态：**confirmed，人物群体关系遗漏**。家庭群体变成不加区分的巨人群，丢失了撤离者以家庭聚集的叙事信息。证据：同文件第46行；第48行继续交代飞船正在撤离部族残余成员。



## O079 | entry-03732

### C22 | entry-03732 | 存在问题

原文“**The view pans around the cabin**”；译文“视角切换到船舱”。

状态：**confirmed，观察动作改变**。原文是视野在船舱内扫动；此前已经显示飞船内部。译文改成切换到船舱这一地点转换。证据：同文件第46行前后连续叙述。



## O080 | entry-03732

### C23 | entry-03732 | 存在问题

原文“**crew members hurrying between the captain’s quarters and the engine room**”；译文“一些成员匆忙走过船长室和引擎室”。

状态：**confirmed，人物身份及移动关系失真**。船员身份没有明确保留，尤其是“在两处之间奔忙”被改成“经过两处”。证据：同文件第46行；这段是在描述飞船撤离中的船员活动。



## O081 | entry-03732

### C24 | entry-03732 | 存在问题

原文“**flying in the air near nothing of importance**”；译文“在空中无害地飞舞”。

状态：**confirmed，环境信息被替换为行为评价**。原文说明小鬼附近没有重要目标，译文却说它的飞行动作无害；两者不等价。附近环境解释了向它开火为何较少造成附带影响。证据：同文件第50行。



## O082 | entry-03732

### C25 | entry-03732 | 存在问题

原文“**Firing on it would have little effect whatsoever**”；译文“向他开火没什么意义”。

状态：**confirmed，后果描述变成价值判断**。原文谈开火造成的影响有限，译文谈这件事没有意义。后半句保留展示威力的用途，仍不能补回对后果大小的说明。证据：同文件第50行及紧随其后的两个射击选择。

实际读取路径与版本如下。为避免重复长路径，定义：

- `P`＝`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g14-20260923`
- `A`＝`/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/orcs`

冻结输入：

- `P/INPUT.md`
- `P/entries.json`
- `P/context.lua`
- `P/source-access.json`

本组源码，全部与 `source-access.json` 的 SHA-256 匹配：

- `P/sources/dlc/cults/tome-cults/overload/mod/class/CultsDLC.lua`
- `P/sources/dlc/cults/tome-cults/overload/mod/dialogs/FontSacrifice.lua`
- `P/sources/dlc/cults/tome-cults/superload/mod/class/Game.lua`
- `P/sources/dlc/orcs/tome-orcs/data/achievements/special.lua`
- `P/sources/dlc/orcs/tome-orcs/data/achievements/story.lua`
- `P/sources/dlc/orcs/tome-orcs/data/birth/classes/empyreal.lua`
- `P/sources/dlc/orcs/tome-orcs/data/birth/classes/tinker.lua`
- `P/sources/dlc/orcs/tome-orcs/data/birth/races/orc.lua`
- `P/sources/dlc/orcs/tome-orcs/data/birth/races/whitehooves.lua`
- `P/sources/dlc/orcs/tome-orcs/data/birth/races/yeti.lua`
- `P/sources/dlc/orcs/tome-orcs/data/chats/aaf.lua`
- `P/sources/dlc/orcs/tome-orcs/data/chats/destructicus-lead.lua`
- `P/sources/dlc/orcs/tome-orcs/data/chats/destructicus.lua`

追加 DLC 源码，全部在白名单内且哈希匹配：

| 路径 | 已读调用或符号来源 |
|---|---|
| `A/tome-orcs/data/general/objects/quest-artifacts.lua` | `aaf.lua:55` 明确加载此文件并创建 `APE` |
| `A/tome-orcs/superload/mod/class/Actor.lua` | APE 使用函数调用 `who:transmoInven` |
| `A/tome-orcs/overload/mod/class/interface/PartyTinker.lua` | 分解逻辑调用 party 材料接口，核查其制造材料消费关系 |
| `A/tome-orcs/data/talents/misc/races.lua` | 种族描述中的 `race/whitehooves`、`T_WHITEHOOVES` 及列出的天赋；同时检查 `T_ORC_FURY` |

本体源码仅通过 `/workspace/t-engine4` 的 `git show` 读取，统一固定 commit 为 `624a67329fe2ad440c5b344785a9c73fcf22ae63`：

- `game/modules/tome/data/talents/misc/races.lua`：追踪种族授予的 `T_ORC_FURY`。
- `game/modules/tome/data/timed_effects/physical.lua`：沿 `EFF_ORC_FURY` 查找，未找到该定义。
- `game/modules/tome/data/timed_effects/mental.lua`：继续追踪同一效果，找到激活与移除逻辑。

共覆盖40条：**8条存在问题、1条待确认、31条未发现问题**。未发现占位符、显示标记或 `@playername@` 丢失；所有条目的 `args_order`、`special` 均为冻结的空值。未把合法标点、段落排版或 existing 术语差异单独判为缺陷。

无法完成的核验限于 items-vault 调用逻辑及 DLC 目标版本对应关系。未创建临时文件、子 agent，未修改仓库，未读取其他报告或越界材料。本输出为独立审核观察，不是生产完成认证。

