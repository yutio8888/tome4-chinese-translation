# 匿名源码核验与归并：40 条 / 71 项观察

你是本任务独立 REVIEWER。用户要求继续三模型实验并归并问题；本阶段依据源码核验，不参与参赛评分。参考是暂定模型裁决，非人工金标准。禁止寻找模型身份或读取来源映射、原始报告、STATE、其他实验目录。不得以多数票、重复次数、报告声称“已证实”替代证据。

唯一允许输入：本文件、同目录 INPUT.md、entries.json、context.lua、source-access.json、source-access.json 明确列出的冻结源码。先阅读INPUT统一判定规则；沿其限定调用链读取单文件。本体使用git show固定commit；DLC只能使用获准的哈希快照，不能把引擎commit套用于DLC，缺少目标版本适用证据则保留pending；无源码组件仅确认文本可证偏差。后续实验的临时文件已获用户授权，可用自己创建的任务专属临时目录；仓库只读，不创建子agent。

下方71项匿名观察按entry和文字排序，包括问题、建议及待确认。各观察C编号仅为原报告局部编号，不跨观察匹配；统一以O编号标识。保持原断言供核验但不采信。请逐项确认、否决、待确认或仅建议；同条同义缺陷合并为canonical D-ID，不同信息或机制错误拆开。注明翻译新增/沿袭上游。遇实质争议要核实双方论据和完整上下文，证据不足保留pending。缺陷边界应考虑完整界面语境，不把单词必然等同为排他机制断言；也不能因玩家猜得出或英文有同错就豁免。

同时独立检查全部40条，包括没有观察或全部观察被否决的条目，补充漏项。只依据INPUT/源码/语境，不能读取其他轮答案。

输出要求：三个Markdown表格，再补充必要解释与读取路径。
1. 恰好40行：entry-ID | 判定（OK/ISSUE/PENDING） | canonical D或P编号/简短依据。OK包括仅建议；有确认缺陷即ISSUE，即使附带pending；无确认但仍有疑点才PENDING。严格冻结顺序。
2. 确认缺陷表：D-ID（D01起） | entry-ID | 内容、归因及固定源码路径:行号/调用链证据。未决用P-ID另列，不混入D。每个D须实际核验。
3. 恰好71行：O-ID | 状态（confirmed/refuted/pending/advisory/mixed） | 命中D-ID（无则—） | 具体证据与理由。mixed须明确哪些部分confirmed、refuted、pending或advisory；不要把未命中的错误问题借用同条其他正确D。若仅有措辞问题则advisory。补充说明所有未决与主要分歧如何处理。

不要给模型排名或分数、不要修改译文，不宣称DONE_VERIFIED。列出实际读取的路径和额外单文件引入依据；未完成的机制核验如实记录。



## O001 | entry-03655

### C01 | entry-03655 | 仅建议
- **原文短引**：`The target is starting to get mad (%d stacks), reducing mind damage resistance by %d%%, mental save by %d, confusion resistance by %d%%, generating %0.1f insanity per turn.`
- **译文短引**：`目标开始疯狂 (%d 层), 降低 %d%% 精神伤害抗性 , %d 精神豁免，%d%% 混乱免疫，每回合获得 %0.1f 疯狂值。`
- **问题说明**：译文中逗号格式不一，前两处使用了半角逗号加空格 `(%d 层), `，且第二处逗号前带有异常空格 `精神伤害抗性 , `，后半句则使用了全角中文逗号 `，`。
- **状态**：仅建议。
- **依据与消费逻辑**：源码位置为 `sources/dlc/cults/tome-cults/data/timed_effects.lua:2124`（`ILLUSORY_CASTLE_MADNESS`）。5个格式化参数及类型（`eff.stacks`、`eff.stacks * 6`、`eff.stacks * 5`、`eff.stacks * 4`、`eff.stacks * 0.5`）全部正确消费，机制数值表达准确；标点与空格微调纯属中文排版美化偏好，不影响运行时文本解析与信息传达。

---



## O002 | entry-03655

### C01 | entry-03655 | 仅建议
「目标开始疯狂 (%d 层), 降低 %d%% 精神伤害抗性 , %d 精神豁免，…」这句混用了半角逗号，逗号前还有多余空格。对照 timed_effects.lua:2124 与 2139-2142 的 updateEffect：各数值及其顺序全部正确。confusion_immune −0.04×层数显示为「层数×4 %」，insanity_regen 为 0.5×层数，「精神豁免」「疯狂值」也与术语一致。所以这里只有标点和空格可以统一，属于排版偏好，不是缺陷。



## O003 | entry-03658

### C01 | entry-03658 | 存在问题

原文 “at the sight of the horror” 指目标**看到恐魔**而获得强化；译文“在恐魔的视线中”变成**被恐魔看到**，颠倒了视线关系。`data/timed_effects.lua:2323-2339` 的 `HORRIFIC_FORTRESS` 将增益施于目标，并以来源恐魔 `eff.src` 是否仍存活控制效果。状态：已证实。



## O004 | entry-03658

### C01 | entry-03658 | 存在问题

原文：“bolstered at the sight of the horror”；译文：“在恐魔的视线中被强化”。

**状态：已证实的语义错误。** 原文是目标看见恐魔而受到鼓舞，译文变成目标处于恐魔的视线之中，颠倒了观看者与被观看者。

证据：`data/timed_effects.lua:2330`，`HORRIFIC_FORTRESS.on_gain`。这是效果获得时的提示；`data/talents/misc/races.lua:164–165` 在召唤恐魔后给召唤者施加此效果，并没有把提示写成恐魔注视目标。此处确认语言关系错误，不据此断言目标版本的视线判定机制。



## O005 | entry-03658

### C02 | entry-03658 | 存在问题
- **原文短引**：`#Target# is bolstered at the sight of the horror!`
- **译文短引**：`#Target#在恐魔的视线中被强化了！`
- **问题说明**：英文介词短语 `at the sight of [something]` 为常见习语，含义为“当看见/目睹某物时”（perceiving/seeing the object）。译文将其误译为“在恐魔的视线中”（in the horror's field of view/sight），主客体视线感知关系完全倒错，将目标目睹恐魔触发强化误写成了目标处于恐魔的视野内。
- **状态**：存在问题。
- **依据与消费逻辑**：源码位置为 `sources/dlc/cults/tome-cults/data/timed_effects.lua:2330`（`HORRIFIC_FORTRESS`，`on_gain` 回调）。该状态长描述为 `All damages except physical reduced by %d as long as %s is alive.`，效果来源 `eff.src` 为恐魔友军，`Target`（`self`）只要与恐魔同处一室目睹恐魔存活即获得减伤强化；context.lua 同文件第12行类似句式 `Empowered by the sight of black blood` 均正译为“目睹黑血时受到强化”。译文颠倒视线方向属于客观语义错误。

---



## O006 | entry-03658

### C02 | entry-03658 | 存在问题
原文「#Target# is bolstered at the sight of the horror!」，译文「#Target#在恐魔的视线中被强化了！」。
- 原文的「at the sight of」是说目标**看到**恐魔而受到鼓舞。
- 译文变成「处于恐魔的视线之中」，把「看」这个动作归给了恐魔，谁看谁被反转了（所属关系错误）。
- 译文还暗示有一个「在对方视野内」的生效条件，源码里没有。HORRIFIC_FORTRESS 在 timed_effects.lua:2322-2345 中，只要 eff.src 还活着就持续（on_timeout 只检查 src 是否存在、是否死亡），不做任何视线判定。
- 状态：存在问题（纯语义，机制证据见上）。



## O007 | entry-03659

### C03 | entry-03659 | 仅建议
「The rift leads... somewhere.」译作「裂缝通向…某个地方。」。同一实体名在 context.lua:344 译为「时空裂隙」，这里的描述却用「裂缝」；省略号也只用了单个「…」。两者都不改变信息，属于用词和排版统一的偏好（entropic-void/grids.lua:34,39）。



## O008 | entry-03668

### C02 | entry-03668 | 存在问题

“A page **of the tome**”译为“书页”，丢失了书页属于那本特定书册的关系。`data/zones/ft-horrors/objects.lua:25-36` 将这段描述用于同一区域的书页实体，并定义了禁忌之书。状态：已证实的语义遗漏。



## O009 | entry-03668

### C02 | entry-03668 | 存在问题

原文：“A page of the tome.”；译文：“书页。”

**状态：已证实的信息遗漏。** 原文说明这是所指书册中的一页；译文只留下物品类别，没有保留属于该书的关系。

证据：`data/zones/ft-horrors/objects.lua:25–29`，三份 `NOTE` 实体共用此描述，分别关联 `cults-tome-horrors-1/2/3`。冻结 `context.lua:460` 同样仅给出“书页”，没有在这条描述中补回所属关系。



## O010 | entry-03668

### C04 | entry-03668 | 存在问题
「A page of the tome.」只译成「书页。」，丢了「the tome」这层定指归属，即这是**这本**禁忌之书的一页。该条是 ft-horrors/objects.lua:26-29 中 BASE_LORE 笔记「the truth beyond the veil (i)」的 desc，所在区域就是禁忌之书 FORBIDDEN_TOME_HOME（同文件:35）。译文成了泛指的书页，所属关系信息丢失。影响较轻，但按规则不能因为读者能猜出来就忽略。



## O011 | entry-03669

### C03 | entry-03669 | 存在问题

“An object **rolls** from the chest”译成物品从宝箱中“掉了出来”，把滚出写成掉出。`data/zones/ft-illusory-castle/grids.lua:92-97` 在开箱并放置物品时显示这条消息。状态：已证实的动作差异。



## O012 | entry-03672

### C05 | entry-03672 | 仅建议
「tremors in the worm」译作「虫子在颤抖」。godfeaster 是一条巨型蠕虫，intro 文本里用的是「巨型蠕虫」，「虫子」语气偏轻。信息没有错，属于措辞偏好（godfeaster/zone.lua:138）。



## O013 | entry-03673

### C06 | entry-03673 | 待确认
「Swordsmith」（source_tag 为 entity name）译作「铸剑铺」，术语快照中是「长剑铁匠铺」（existing，core，城镇商店实体）。
- existing 本身不强制改名。
- 疑点在运行时：固定 commit 的 engine/I18N.lua:41-69、141-143 中，`_t` 与 `I18N:t` 都以 locale 下的 `[tag][src]` 为键，不含 section。
- 因此 cults 的 ("Swordsmith","entity name") 与本体同键条目若译法不同，会互相覆盖（后加载者生效），造成同名商店显示不一致。
- 缺少的证据：本体当前翻译文件中该键的实际 target，以及加载顺序。按规定这两项都不可读。



## O014 | entry-03678

### C07 | entry-03678 | 待确认
情况同 C06：town-kroshkkur/traps.lua:43 的「Swordsmith」译作「铸剑铺」，与术语快照的「长剑铁匠铺」同键不同译，是否发生运行时覆盖待确认。



## O015 | entry-03681

### C03 | entry-03681 | 存在问题

原文：“creeking and vibrating”；译文：“颤动”。

**状态：已证实的信息遗漏。** 此处 `creeking` 是语境明确的拼写误差，描写骨杖骨骼吱嘎作响；译文只保留振动，丢失声音描写。

证据：`hooks/bonestaff.lua:22–24`，`CommandStaff:SentientOptions` 的 `intro` 分支直接提供这段叙述。不是运行时音效是否播放的问题。



## O016 | entry-03681

### C03 | entry-03681 | 存在问题
- **原文短引**：`You feel the bones of the staff creeking and vibrating in your hand.`
- **译文短引**：`你感受到手中的骨杖在你的手上颤动：`
- **问题说明**：
  1. 原文动作描述为 `creeking and vibrating`（骨节挤压嘎吱作响与震颤），译文仅翻译了 `vibrating`（颤动），完全遗漏了 `creeking`（作者拼写笔误，即 creaking，骨节挤压发出的刺耳嘎吱声）这一核心声音/触觉感知信息。
  2. 译文句式出现“手中的骨杖在你的手上”重叠啰嗦语病。
- **状态**：存在问题。
- **依据与消费逻辑**：源码位置为 `sources/dlc/cults/tome-cults/hooks/bonestaff.lua:24`（`CommandStaff:SentientOptions` 中 `data.mode == "intro"` 的对话文本）。骨杖作为具有独立意志的活物武器，骨骼摩擦作响（creeking）是其拟人化惊悚特征的关键细节，漏译导致感官描写缺失。

---



## O017 | entry-03681

### C04 | entry-03681 | 存在问题

原文骨杖在手中“creeking **and vibrating**”；译文只有“颤动”，遗漏骨头作响的信息。`hooks/bonestaff.lua:22-25` 是骨杖对话的开场文本。状态：已证实。



## O018 | entry-03681

### C08 | entry-03681 | 存在问题
原文「You feel the bones of the staff creeking and vibrating in your hand.」，译文「你感受到手中的骨杖在你的手上颤动」只保留了 vibrating，漏掉了 creeking（骨头嘎吱作响）这个感官信息，属于语义信息遗漏（bonestaff.lua:24）。影响较轻。



## O019 | entry-03681

### C09 | entry-03681 | 仅建议
「手中的骨杖在你的手上」前后重复表达了位置。标记与引号都完整保留，这只是措辞冗余。



## O020 | entry-03683

### C04 | entry-03683 | 存在问题

原文：“Stupid useless pathetic excuse of a … ‘necromancer’”；译文：“像你这样的……‘死灵法师’竟然会用这样蹩脚的借口”。

**状态：已证实的语义错误。** `pathetic excuse of a necromancer` 是直接辱骂对方不配称为死灵法师；译文把 `excuse` 当成对方提出的借口，虚构了“使用借口”的行为，同时丢失“愚蠢、无用”的辱骂内容。

证据：`hooks/bonestaff.lua:114–117`，`bone_horror_disabled` 对话。紧接着的玩家回答为“I have my reasons!”，并不能将前一句的习语解释为对方已经给出了借口。



## O021 | entry-03683

### C04 | entry-03683 | 存在问题
- **原文短引**：`Stupid useless pathetic excuse of a #{italic}#"necromancer"#{normal}#! Why refuse to use true power?!`
- **译文短引**：`像你这样的#{italic}#"死灵法师"#{normal}#竟然会用这样蹩脚的借口！为什么要拒绝使用真正的力量？！`
- **问题说明**：英文成语结构 `a pathetic excuse of a [noun]`（或 `excuse for a ...`）是固定侮辱性修辞，意为“差劲透顶/根本不配称为……的可悲货色”。骨杖在此直斥玩家角色根本不配称作死灵法师（“你这个愚蠢没用、根本不配叫‘死灵法师’的可悲废物！”）。译者望文生义，将 `excuse` 单独按名词“借口”直译，并脑补出“死灵法师竟然会用这样蹩脚的借口”，严重扭曲了骨杖对玩家身份的斥责与对话语境。
- **状态**：存在问题。
- **依据与消费逻辑**：源码位置为 `sources/dlc/cults/tome-cults/hooks/bonestaff.lua:115`（`bone_horror_disabled` 对话节点）。玩家在上一对话中拒绝献出技能点启用骨灵恐魔，骨杖在此表现出轻蔑与愤怒，斥责玩家空有死灵法师之名却拒绝真正的力量；玩家后续回复选项亦为 `I have my reasons!`（我有我的理由！）。译文把对角色名号的贬损误读为指责玩家找借口，属于典型的成语误译与语义失实。

---



## O022 | entry-03683

### C05 | entry-03683 | 存在问题

“pathetic excuse of a ‘necromancer’”是在辱骂**对方不配称为死灵法师**；译文“会用这样蹩脚的借口”却说对方提出了借口，改变了被指责的内容。`hooks/bonestaff.lua:114-117` 显示这是骨杖对玩家的回答。状态：已证实。



## O023 | entry-03683

### C05 | entry-03683 | 存在问题

原文：“The staff stays calm.”；译文：“法杖平静了下来。”

**状态：已证实的状态关系错误。** 原文描述继续保持平静；译文描述从不平静转为平静，新增了状态变化。

证据：`hooks/bonestaff.lua:115`，同一拒绝启用力量的对话叙述。与 C04 属于不同语义缺陷。



## O024 | entry-03683

### C10 | entry-03683 | 存在问题
原文「Stupid useless pathetic excuse of a "necromancer"!」，译文「像你这样的"死灵法师"竟然会用这样蹩脚的借口！」。
- 「pathetic excuse of a X」是固定骂语，意思是「不配称为 X 的可怜货色」，没有「借口」的意思。
- 按对话顺序，这句话在玩家说出理由之前：玩家先选「I want you to stop summoning the bone horror.」（bonestaff.lua:64），法杖回应本句（:114-115），之后玩家才能答「I have my reasons!」（:117）。所以译文里「用借口」这件事在剧情中尚未发生，属于事实错误。
- 另外「Stupid useless」两个侮辱修饰语也被丢掉了。
- 状态：存在问题。



## O025 | entry-03683

### C11 | entry-03683 | 仅建议
「The staff stays calm.」译作「法杖平静了下来」。原文是「保持平静」，译文带有「从躁动转为平静」的意味，但核心信息（法杖没有反应）还在，属于措辞偏好。



## O026 | entry-03684

### C06 | entry-03684 | 存在问题

原文外界敌视的是“such **activities**”，即这些研究活动；译文“对这些**知识**并不友好”改了敌视对象。`overload/data/texts/intro-cults.lua:23`。状态：已证实。



## O027 | entry-03684

### C06 | entry-03684 | 存在问题

原文：“the only rules … secrecy and safeguarding the accrued knowledge”；译文：“唯一规则就是必须对在里面学到的知识进行严格的保密和保护”。

**状态：已证实的范围缩减。** 前一句明确说明避难所一旦被发现就会遭毁灭，因此这里的保密要求包括隐匿避难所及其活动；译文把保密对象全部收束为“学到的知识”，丢失这项生存规则的范围。

证据：`overload/data/texts/intro-cults.lua:25`，发现避难所、摧毁避难所与保密规则位于同一段，构成直接语境证据。



## O028 | entry-03684

### C07 | entry-03684 | 存在问题

“Age of **Haze**”译为“**混沌**纪”，将 haze 的含义换成 chaos，改变了所指时代名称。`overload/data/texts/intro-cults.lua:23`。状态：已证实。



## O029 | entry-03684

### C07 | entry-03684 | 存在问题

原文：“a giant worm that is tunneling directly towards Kroshkkur”；译文：“一条直接冲向克诺什库尔的巨型蠕虫”。

**状态：已证实的信息遗漏。** `tunneling` 明确说明蠕虫正在掘进；“冲向”没有保留穿掘通道的移动方式，并带入了冲刺意味。

证据：`overload/data/texts/intro-cults.lua:27`。这是原文直接提供的威胁场景信息，不依赖推测蠕虫的运行时代码。



## O030 | entry-03684

### C08 | entry-03684 | 存在问题

原文：“leave now while it is safe to do so”；译文：“或者就这样离开”。

**状态：已证实的信息遗漏。** 原文明确告知当前离开仍然安全，属于玩家选择的条件信息；译文没有保留这一安全性说明。前段“在蠕虫到来之前离开”保留了时间关系，但不能替代明确的安全性判断。

证据：`overload/data/texts/intro-cults.lua:29`，传送入虫体与安全离开的选择段落。



## O031 | entry-03684

### C12 | entry-03684 | 存在问题
原文「or leave now while it is safe to do so and let Kroshkkur be destroyed」，译文「你可以现在踏入…传送门或者就这样离开任由克诺什库尔被巨型蠕虫摧毁」（intro-cults.lua:29）。
- 「while it is safe to do so」这个条件和时机被整句删除。
- 「now」从「离开」一项移到了「传送门」一项。
- 结果是「趁现在还安全离开」的条件和时序信息丢失，选项的时间归属也变了。



## O032 | entry-03684

### C13 | entry-03684 | 存在问题
「If nothing is done it will collide with…」译作「如果再不迅速做出决断，它将会…」。原文的条件是「不采取行动」，译文改成了「不迅速做出决断」，行动变成了决断，还新增了「迅速」这个时间约束，条件被改写。影响轻微，单独列出以便归并。



## O033 | entry-03684

### C14 | entry-03684 | 仅建议
以下几处是增补、冗余或意象弱化，都没有引入错误事实，所以算措辞层面：
- 「这导致了对许多地表人视为疯狂且被禁止之事的实验，而你们的研究内容也被普通人的社会所禁止」：后半句是译者添加的重复。
- 「希望解开过去的阴影」「追寻禁忌的知识」：属于润色添加。
- 「tunneling directly towards」译作「直接冲向」：失去了「掘地而来」的意象。



## O034 | entry-03685

### C05 | entry-03685 | 存在问题
- **原文短引**：`While much of Maj'Eyal shuns the arcane...`
- **译文短引**：`虽然大部分马基埃亚尔人都远离奥术魔法...`
- **问题说明**：专有名词 `Maj'Eyal` 译为了 `马基埃亚尔`，违反了术语库的明确规定。
- **状态**：存在问题。
- **依据与消费逻辑**：冻结术语快照中明确收录：`Maj'Eyal | 马基·埃亚尔 | T.PN.WORLD | places | _t | preferred | core | 维护者于 2026-08-25 裁定采用“马基·埃亚尔”；“马基埃亚尔”已被取代`。此处属于必须遵循的 `preferred` 术语要求，使用已被取代的旧译构成术语缺陷。

---



## O035 | entry-03685

### C06 | entry-03685 | 存在问题
- **原文短引**：`All Krogs are infused with anti-magic forces as a result of the changes made to their bodies by the Ziguranth.`
- **译文短引**：`作为上面条件的附加作用，克罗格的身体被伊格兰斯的反魔法力量所灌注。`
- **问题说明**：原文 `as a result of the changes made to their bodies by the Ziguranth` 明确表示克罗格体内充满反魔法力量是“伊格兰斯对其身体进行肉体改造/改变的结果”。译文翻译为“作为上面条件的附加作用”，凭空捏造了“上面条件”，不仅丢失了伊格兰斯对食人魔进行外科肉体改造的关键背景叙事，还引入了逻辑荒谬的机械化措辞。
- **状态**：存在问题。
- **依据与消费逻辑**：源码位置为 `sources/dlc/cults/tome-cults/overload/data/texts/intro-krog.lua:26`。结合同文件及 `unlock-race_krog.lua` 叙事（`After lots of painful, but required, experiments Zigur was finally able to create an offshoot...`），伊格兰斯通过对食人魔身体强行剥离符文并注入龙血改造创造了克罗格。译文将肉体改造丢失并误译为“上面条件的附加作用”，属于严重语义失真与无据脑补。

---



## O036 | entry-03685

### C07 | entry-03685 | 存在问题
- **原文短引**：`yet you a Krog have been kept alive by the powers of nature coursing through your body.`
- **译文短引**：`而你这样克罗格却可以通过你身体内的自然力量存活。`
- **问题说明**：译文“而你这样克罗格却可以通过……”存在明显的语法语病/错别字（缺失量词或虚词，“这样克罗格”应为“作为克罗格”或“这名克罗格”/“这样的克罗格”）。
- **状态**：存在问题。
- **依据与消费逻辑**：源码位置为 `sources/dlc/cults/tome-cults/overload/data/texts/intro-krog.lua:24`。同类句式为同位语结构（`you, a Krog, have been...`），译文语句不通，属于语法与文本瑕疵。

---



## O037 | entry-03685

### C08 | entry-03685 | 仅建议
- **原文短引**：`You have come to an old ruin named Kor'Pul...`
- **译文短引**：`你来到了一个古老的废墟：卡普尔。`
- **问题说明**：地名 `Kor'Pul` 在术语快照中收录为 `卡·普尔`（带间隔号），译文中译为 `卡普尔`。
- **状态**：仅建议。
- **依据与消费逻辑**：术语快照中 `kor'pul | 卡·普尔 | T.NARRATIVE.LORE | status=existing`。根据规则，`existing` 不单独作为强制改名依据，但考虑到同条目已存在 C05 术语违规，建议地名拼写同步规范为规范译名 `卡·普尔`。

---



## O038 | entry-03685

### C08 | entry-03685 | 存在问题

原文说反魔力量来自伊格兰斯**对克罗格身体所作改造**；译文“作为上面条件的附加作用”将原因接到前句的生存条件上。`overload/data/texts/intro-krog.lua:24-26`。状态：已证实的因果关系差异。



## O039 | entry-03685

### C09 | entry-03685 | 存在问题

冻结术语子集明确要求 `_t` 世界地名 `Maj'Eyal` 使用“马基·埃亚尔”；译文“马基埃亚尔”缺少名称中的间隔点。原文见 `overload/data/texts/intro-krog.lua:26`。状态：已证实的适用术语差异。



## O040 | entry-03685

### C09 | entry-03685 | 存在问题

原文：“as a result of the changes made to their bodies by the Ziguranth”；译文：“作为上面条件的附加作用……被伊格兰斯的反魔法力量所灌注”。

**状态：已证实的因果与修饰关系错误。** 原文明确把反魔力量灌注归因于伊格兰斯对身体的改造；译文用不明确的“上面条件”取代改造行为，并把“伊格兰斯”改成力量的所属者。这超出了单纯措辞不自然。

证据：`overload/data/texts/intro-krog.lua:24–26`。前段讲符文被剥除及自然力量维生，后段另行明确身体改造导致反魔力量灌注。



## O041 | entry-03685

### C10 | entry-03685 | 存在问题

原文：“Maj'Eyal”；译文：“马基埃亚尔”。

**状态：已证实的术语不符合。** 冻结术语子集明确将“马基·埃亚尔”列为 `preferred`，并注明旧写法“马基埃亚尔”已被取代。本条是 `_t` 的世界地名叙述，适用该要求。

证据：INPUT 术语快照的 `Maj'Eyal / T.PN.WORLD / _t` 条目；`overload/data/texts/intro-krog.lua:26`。



## O042 | entry-03685

### C15 | entry-03685 | 存在问题
「While much of Maj'Eyal shuns the arcane」译作「大部分马基埃亚尔人」（intro-krog.lua:26）。术语快照 Maj'Eyal＝「马基·埃亚尔」为 preferred（_t，T.PN.WORLD），备注写明「马基埃亚尔」已被取代。同文件的 title 在 context.lua:717 也已使用「马基·埃亚尔」。这是适用的术语要求未被遵守。



## O043 | entry-03685

### C16 | entry-03685 | 存在问题
原文「All Krogs are infused with anti-magic forces as a result of the changes made to their bodies by the Ziguranth.」，译文「作为上面条件的附加作用，克罗格的身体被伊格兰斯的反魔法力量所灌注。」
- 原文的因果是：伊格兰斯**对其身体所做的改造**，结果使克罗格带有反魔法力量。
- 译文把原因改成「上面条件」（即靠自然之力存活），又把反魔法力量归属给伊格兰斯。
- 因果和所属关系都被改写。



## O044 | entry-03685

### C17 | entry-03685 | 仅建议
- 「Kor'Pul」译作「卡普尔」，术语快照只有 newLore 类目下的「卡·普尔」（existing，标签不同），不构成强制要求。
- 原文段间空行被合并为单换行（原文 7 个 \n，译文 5 个）。段落仍然可以分辨，没有造成信息结构丢失，属于排版差异。



## O045 | entry-03686

### C09 | entry-03686 | 仅建议
- **原文短引**：`New Class: #LIGHT_GREEN#Cultist of Entropy (Demented)`
- **译文短引**：`新职业 : #LIGHT_GREEN#熵教徒（疯狂系）`
- **问题说明**：冒号使用了半角冒号且前后留空 `新职业 : `，与相邻解锁条目（如 entry-03688 `新种族：#LIGHT_GREEN#克罗格`、entry-03690 `新技能树：#LIGHT_GREEN#天谴之龙`）的全角冒号 `：` 不一致。
- **状态**：仅建议。
- **依据与消费逻辑**：源码位置为 `sources/dlc/cults/tome-cults/overload/data/texts/unlock-demented_cultist_entropy.lua:20`。术语 `Cultist of Entropy`（熵教徒）与 `Demented`（疯狂系）消费完全正确无误，标点格式仅属界面一致性与排版偏好建议。

---



## O046 | entry-03686

### C18 | entry-03686 | 仅建议
「新职业 : 」冒号前后带半角空格，同类的 03688 用「新种族：」。纯排版不一致。术语「熵教徒」「疯狂系」与快照一致。



## O047 | entry-03687

### C11 | entry-03687 | 待确认

原文：“eliminate cooldown on talents”；译文：“使技能不进入冷却”。

**状态：快照内适用范围差异已证实；目标版本适用性待确认。** 快照中并非所有技能、每次使用都不进入冷却：

- `data/talents/misc/races.lua:36–43`：施加持续三回合的 `DREM_FRENZY`。
- `superload/mod/class/Actor.lua:113–123`：排除刻印、通用技能、超系技能、被动、固定冷却及部分瞬发技能；仅在该技能未记入 `used_talents` 时将 `data.cd` 置零。

英文解锁摘要本身也省略了这些限制，因此不能全部归为翻译新增。尚缺该 DLC 快照与审核目标版本一致的来源证据，故不将此项作为目标版本已确认缺陷。



## O048 | entry-03687

### C12 | entry-03687 | 待确认

原文：“Bleed your black blood on your attackers”；译文：“让黑血溅到攻击你的人身上”。

**状态：快照内流血主体差异已证实；目标版本适用性待确认。** 快照实际给攻击者施加黑血流血效果，而非表现为自身黑血溅到攻击者身上：

- `data/talents/misc/races.lua:57–60`：`callbackOnMeleeHit` 对攻击来源 `src` 调用 `setEffect`。
- `data/timed_effects.lua:85–95`：受效果者“starts to bleed black blood”，并在其坐标结算暗影伤害。

英文摘要也含有自身黑血的表述，存在上游描述与实现不一致，不能只归责译文。缺少目标 DLC 版本与快照对应证明，保留待确认。



## O049 | entry-03689

### C10 | entry-03689 | 存在问题

原文 “**Zigur** was finally able to create…”指据点“伊格”；译文写“**伊格兰斯**终于创造…”，换成教团。冻结术语子集明确区分两者；原文见 `overload/data/texts/unlock-race_krog.lua:25`。状态：已证实。



## O050 | entry-03689

### C10 | entry-03689 | 存在问题
- **原文短引**：`After lots of painful, but required, experiments Zigur was finally able to create an offshoot of the ogre race...`
- **译文短引**：`在经过无数痛苦但不可避免的实验后，伊格兰斯终于创造出食人魔的一个亚种。`
- **问题说明**：原文第3段主语为地点专名 `Zigur`，译文将其翻译为了教团全称 `伊格兰斯`，违反了 `preferred` 术语的严格区分要求。
- **状态**：存在问题。
- **依据与消费逻辑**：冻结术语快照中专门对 `Zigur` 与 `Ziguranth` 作出严格区分判定：
  - `Zigur | 伊格 | T.PN.PLACE | preferred | core | 指地点时一律用「伊格」，不得写成「伊格兰斯」。`
  - `Ziguranth | 伊格兰斯 | T.PN.FACTION | preferred | core | 教团／人群用「伊格兰斯」，地点用「伊格」，两者不得互换。`
  在本条原文中，第2段 `Ziguranth took pity on them` 正确译为 `伊格兰斯同情他们`，第4段 `staunch protectors of Zigur` 正确译为 `伊格的坚实保护者`，唯独第3段 `Zigur was finally able to create...` 将 `Zigur` 错译成了 `伊格兰斯`，造成同一文本内指代混乱且直接违反 preferred 规则。

---



## O051 | entry-03689

### C11 | entry-03689 | 存在问题

原文克罗格是 “protectors of **Zigur**”；译文成了“**伊格兰斯**的坚实保护者”，再次把保护的据点换成教团。`overload/data/texts/unlock-race_krog.lua:26`。状态：已证实。



## O052 | entry-03689

### C11 | entry-03689 | 存在问题
- **原文短引**：`...to crush all foes of Nature!`
- **译文短引**：`...摧毁所有自然的敌人\n\n你从不死生物的魔爪中救下了一群克罗格...`
- **问题说明**：原文段落末尾有明确感叹号 `!`，译文段末完全漏掉了句末标点符号，句子未收束即直接换行换段。
- **状态**：存在问题。
- **依据与消费逻辑**：源码位置为 `sources/dlc/cults/tome-cults/overload/data/texts/unlock-race_krog.lua:26`。排版格式中漏掉句末标点属于文本完整性缺陷。

---



## O053 | entry-03689

### C12 | entry-03689 | 存在问题
- **原文短引**：`- Drake infused blood that lets them resist the elements themselves`
- **译文短引**：`- 他们龙血灌注的身体可以抵抗元素魔法伤害。`
- **问题说明**：原文为“抵抗元素本身”（resist the elements themselves）。译文画蛇添足增加了“魔法”二字，译作“抵抗元素魔法伤害”。这一增译直接违背了游戏设定和技能实际运作机制：克罗格是由伊格兰斯反魔势力创造的反魔种族，其种族天赋 `Drake-Infused Blood`（龙血灌注，源码 `sources/cults/tome-cults/data/talents/misc/races.lua:36`）提供的元素抗性包含物理（Physical）、自然（Nature）、火焰（Fire）、寒冰（Cold）、闪电（Lightning）、酸性（Acid），这些属于各元素能量形态，既非单纯的魔法伤害，更与克罗格敌视奥术魔法（Arcane）的背景冲突。
- **状态**：存在问题。
- **依据与消费逻辑**：克罗格背景强调其反魔法特性（“身体被反魔法力量所灌注”、“摧毁所有自然的敌人”），将龙血抗性误加上“魔法”标签属于机制与设定的双重误导。

---



## O054 | entry-03689

### C12 | entry-03689 | 待确认

“resist the **elements** themselves”译成抵抗“**元素魔法伤害**”，增加了“魔法”这一限制。`overload/data/texts/unlock-race_krog.lua:32` 只给出特色文案；本次允许的已读调用链没有确定该抗性的实际伤害范围，因此不能以文案单独裁定目标版本机制。缺少对应种族能力的目标版本源码证据。



## O055 | entry-03689

### C13 | entry-03689 | 存在问题

原文：“But while they are magic users Ziguranth took pity on them”；译文：“然而，伊格兰斯同情他们被强迫而无法选择的命运”。

**状态：已证实的信息遗漏。** 译文保留了同情的原因，却遗漏“尽管他们使用魔法”的让步条件，削弱了反魔教团为何对这群魔法使用者破例的叙事关系。

证据：`overload/data/texts/unlock-race_krog.lua:24`。前段的符文维生事实不能替代这里明确提出的让步关系。



## O056 | entry-03689

### C14 | entry-03689 | 存在问题

原文：“Zigur was finally able to create an offshoot”；译文：“伊格兰斯终于创造出食人魔的一个亚种”。

**状态：已证实的专名指称替换。** 原文这里使用 `Zigur`，译文却替换成 `Ziguranth` 对应的教团名。即使地点名称在句中借代当地共同体，也不等于英文改用了教团名称。

证据：`overload/data/texts/unlock-race_krog.lua:24–26` 连续分别使用 `Ziguranth`、`Zigur`、`Zigur`；冻结术语子集明确区分“伊格”与“伊格兰斯”，要求不得互换。



## O057 | entry-03689

### C15 | entry-03689 | 存在问题

原文：“resist the elements themselves”；译文：“抵抗元素魔法伤害”。

**状态：已证实的文本范围缩减。** 原文未限定元素伤害来自魔法；译文新增“魔法”条件，把描述范围缩窄。此项文本差异不依赖目标版本机制即可成立。

快照补充证据：`data/talents/misc/races.lua:224–235` 的 `Drake-Infused Blood.passives` 添加按伤害类型索引的 `resists`；该分支没有按攻击来源是否为魔法加条件。这里仅陈述快照中的赋值行为，不将其提升为已固定目标版本的完整抗性消费证明。



## O058 | entry-03689

### C19 | entry-03689 | 存在问题
原文「But while they are magic users Ziguranth took pity on them…」，译文「然而，伊格兰斯同情他们被强迫而无法选择的命运。」，删去了让步条件「尽管他们是魔法使用者」（unlock-race_krog.lua:24）。这个条件交代了反魔教团同情对象的特殊性，属于语义信息遗漏。



## O059 | entry-03689

### C20 | entry-03689 | 待确认
原文「Zigur was finally able to create an offshoot…」（:25）中的 Zigur 被译为「伊格兰斯」（教团名）。术语备注要求地点用「伊格」、教团用「伊格兰斯」，「两者不得互换」。但此处的 Zigur 作施事主语，可能是借地名指代教团。是否属于不得互换的情形，需要术语裁决，缺少针对借代用法的明确依据。



## O060 | entry-03689

### C21 | entry-03689 | 待确认
「Drake infused blood that lets them resist the elements themselves」（:32）译作「可以抵抗元素魔法伤害」。译文比原文多了「魔法」这一限定，把范围收窄或改写为「魔法性质的元素伤害」。是否与实际抗性（应为若干元素伤害类型的抗性）不符，需要克罗格种族天赋定义佐证。本组 sources 中没有该定义，按显式调用链规则也不能从本文件引入，所以待确认。



## O061 | entry-03689

### C22 | entry-03689 | 仅建议
- 「…摧毁所有自然的敌人」句末缺少终止标点（原文为「!」）。
- 「A mastery of infusions like no others」译作「自然纹身的大师」，弱化了「无人能及」的程度，但「大师」已经表达了卓越。
- 「infusions」译「纹身」与术语一致。
- 以上都属于措辞和排版。



## O062 | entry-03691

### C13 | entry-03691 | 存在问题

“corrupted **beyond hope**”指腐化到无可挽回；译文“被**绝望**所腐化”把程度描述改成腐化原因。`overload/data/texts/unlock-wyrmic_scourge.lua:21`。状态：已证实。



## O063 | entry-03691

### C13 | entry-03691 | 存在问题
- **原文短引**：`Drakes are forces of Nature, the ultimate apex predators. But even they can be corrupted beyond hope.`
- **译文短引**：`龙是自然力量的化身，是究极的捕食者。然而，就连他们也能够被绝望所腐化。`
- **问题说明**：英文成语短语 `beyond hope` 表示程度，意为“无可救药地 / 万劫不复地 / 彻底无法挽回地”（hopelessly / without any hope of recovery）。译者看词生义，将其硬译成了“被绝望所腐化”（corrupted by despair），把表示“腐化程度已无法挽救”的副词修饰语错当成了致使腐化的施动者/实体（“绝望”），属于明显的语义误译。
- **状态**：存在问题。
- **依据与消费逻辑**：源码位置为 `sources/dlc/cults/tome-cults/overload/data/texts/unlock-wyrmic_scourge.lua:21`。背景描述天谴龙（Scourge Drake）源自最强大的巨龙库洛塔被枯萎与恐魔彻底腐化变异，原文旨在说明即使是顶级掠食者的龙也会堕落到“不可救药”的地步，并非被抽象的“绝望”概念腐化。

---



## O064 | entry-03691

### C14 | entry-03691 | 存在问题

“Hit where it hurts”结合后半句“伤害随负面效果增加”，指利用对方弱点；译文“击打对手**受伤的地方**”增加了原文没有的实体伤口条件。`overload/data/texts/unlock-wyrmic_scourge.lua:29`。状态：已证实。



## O065 | entry-03691

### C14 | entry-03691 | 存在问题
- **原文短引**：`...that can learn the #LIGHT_GREEN#Scourge Drake talents#WHITE#.\n\nTalents:`
- **译文短引**：`...可以使用新的#LIGHT_GREEN#天谴之龙#WHITE#系技能\n\n技能列表：`
- **问题说明**：第三句句末“技能”二字之后漏标了句末句号 `。`，原文末尾有句号 `.`。
- **状态**：存在问题。
- **依据与消费逻辑**：源码位置为 `sources/dlc/cults/tome-cults/overload/data/texts/unlock-wyrmic_scourge.lua:24`。属于格式与标点漏标缺陷。

---



## O066 | entry-03691

### C16 | entry-03691 | 存在问题

原文：“corrupted beyond hope”；译文：“被绝望所腐化”。

**状态：已证实的语义错误。** `beyond hope` 描述腐化已达到无可挽救的程度；译文却把“绝望”写成造成腐化的原因，改变了程度与因果关系。

证据：`overload/data/texts/unlock-wyrmic_scourge.lua:21`。该判断来自完整句法语境，无需推定任何“绝望”机制。

实际读取材料与边界如下。

冻结包根目录 `P`：

```text
/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-g13-20260923
```

读取了 `P/INPUT.md`、`P/entries.json`、`P/context.lua`、`P/source-access.json`，以及以下全部源码路径；下列路径均相对 `P/sources/dlc/cults/tome-cults/`：

```text
data/timed_effects.lua
data/zones/entropic-void/grids.lua
data/zones/ft-cultist/npcs.lua
data/zones/ft-haze-cave/grids.lua
data/zones/ft-haze-cave/npcs.lua
data/zones/ft-haze-cave/zone.lua
data/zones/ft-home/grids.lua
data/zones/ft-horrors/objects.lua
data/zones/ft-illusory-castle/grids.lua
data/zones/ft-illusory-castle/zone.lua
data/zones/ft-yaech/grids.lua
data/zones/godfeaster/zone.lua
data/zones/test/traps.lua
data/zones/town-kroshkkur/npcs.lua
data/zones/town-kroshkkur/traps.lua
hooks/bonestaff.lua
overload/data/texts/intro-cults.lua
overload/data/texts/intro-krog.lua
overload/data/texts/unlock-demented_cultist_entropy.lua
overload/data/texts/unlock-race_drem.lua
overload/data/texts/unlock-race_krog.lua
overload/data/texts/unlock-wyrmic_scourge.lua
overload/mod/class/CultsDLC.lua
```

额外源码根目录 `A`：

```text
/home/paseo/.paseo/worktrees/2p1pqszt/translation-spotcheck-20260921/evidence/translation-audit/all-modified-review-20260922/experiments/abc20-20260923/sources/cults
```

| 实际额外读取路径（相对 A） | 已读材料中的追查来源 |
|---|---|
| `tome-cults/data/talents/misc/races.lua` | 德瑞姆、克罗格解锁说明中的 Frenzy、黑血及龙血种族能力 |
| `tome-cults/superload/mod/class/Actor.lua` | `CultsDLC.lua:51` 的 `insanityEffectForce()`；并核验 `DREM_FRENZY` 冷却消费 |
| `tome-cults/data/talents/demented/scourge-drake.lua` | 解锁说明明确列出的四个技能名称 |

23 个包内源码文件与3个额外源码文件均核对 SHA-256，与 `source-access.json` 一致。未读取本体源码；清单中的本体固定 commit `624a67329fe2ad440c5b344785a9c73fcf22ae63` 未用于替代 DLC 版本证明。

共覆盖 **40 条：存在问题8条、待确认1条、仅建议0条、未发现问题31条**。无法核验之处为上述 DLC 目标版本对应关系，具体未决观察见 C11、C12。未越界读取，未读取其他报告，未创建临时文件或子 agent，未修改仓库。本输出仅为独立审核观察，不代表生产验收结论。


## O067 | entry-03691

### C23 | entry-03691 | 存在问题
「But even they can be corrupted beyond hope.」译作「就连他们也能够被绝望所腐化。」（unlock-wyrmic_scourge.lua:21）。「beyond hope」意为「无可救药地」，是程度状语；译文把它理解为腐化的施动者「绝望」，意思错误。



## O068 | entry-03691

### C24 | entry-03691 | 待确认
「Augment Despair: …doing more damage based on detrimental effects」（:29）译作「对方负面效果越多伤害越高」。原文只说伤害「基于负面效果」增加，译文补出了「按数量递增」的关系。是否与天赋实际计算一致，需要 Scourge Drake 天赋定义，本组 sources 中没有，也无法经显式调用链引入。



## O069 | entry-03691

### C25 | entry-03691 | 仅建议
- 首段后的空行被合并（原文 10 个 \n，译文 9 个）。段落仍可辨，不影响显示结构。
- 「你创建的新龙战士角色可以使用新的…系技能」句末缺标点。
- 「Scourge Drake magic」译「天谴龙的魔法」，与「天谴之龙」写法不统一。
- 均为排版和用词偏好；标记完整。



## O070 | entry-03692

### C15 | entry-03692 | 存在问题

原文说伤害和冷却时间“**have a chance** to increase or decrease”；译文“将会……上下浮动”遗漏了触发具有概率这一条件。`overload/mod/class/CultsDLC.lua:47-52` 定义资源说明及状态数值显示。状态：已证实。



## O071 | entry-03692

### C26 | entry-03692 | 存在问题
原文「Damage and cooldowns have a chance to increase or decrease by up to chaotic%.」，译文「伤害和冷却时间将会在 混沌度% 的范围内上下浮动。」
- 「have a chance to」被删掉，把按概率发生写成了必然发生；下一句的「浮动的几率」不能补回这句的断言。
- 该文本作为 description 传给 `ActorResource:defineResource`（CultsDLC.lua:47），在固定 commit 的 engine/interface/ActorResource.lua:45,58 中原样存为 description，没有占位替换。所以「chaotic」→「混沌度」只是文字，与 status_text 的译法（context.lua:856「混沌度」）一致，不是格式问题。
- 问题只在被删掉的概率限定词。

---


